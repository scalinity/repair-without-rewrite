"""Shared complete queues, unchanged B/C objectives and atomic cold resume."""
from dataclasses import asdict
import hashlib
import json
import math
import os
from pathlib import Path
import random
import tempfile
import time

import mlx.core as mx
import mlx.nn as nn
from mlx.utils import tree_unflatten
import numpy as np

from src.data.mixed_reader_v3 import pilot_lr
from src.data.lexical_corruption_v2 import serialized
from .bc import c_microbatch_loss
from .core import masked_cross_entropy
from .edits import EventInput, EventLabels
from .tokenizer import BOS, EOS, PAD
from .training import AdamW, GradientAccumulator, flat_parameters


def labels_from_row(row):
    value = row["gold_labels"]
    return EventLabels(tuple(EventInput(**event) for event in value["inputs"]),
        *(tuple(tuple(item) for item in value[key]) for key in ("action", "start", "end", "vocabulary")),
        value["replacement_tokens"])


def queue_denominators(queue):
    return {"B": sum(len(presentation["row"]["target_ids"]) + 1 for presentation in queue),
        "C": {key: sum(presentation["row"]["C_denominators"][key] for presentation in queue)
              for key in ("action", "start", "end", "vocabulary")}}


def validate_queue(queue):
    for presentation in queue:
        row = presentation["row"]
        if presentation["canonical_charge"] != row["canonical_charge"] or len(row["canonical_sequence"]) != row["canonical_charge"]:
            raise ValueError("accepted canonical charge changed")
        for key in ("source", "target", "anchor"):
            actual = hashlib.sha256(row[key].encode("utf-8", "strict")).hexdigest()
            if actual != row[key + "_sha256"] or presentation.get(key + "_sha256", actual) != actual:
                raise ValueError("accepted literal bytes changed")
        if "accepted_row_sha256" in presentation and hashlib.sha256(serialized(row)).hexdigest() != presentation["accepted_row_sha256"]:
            raise ValueError("frozen accepted row changed")
        if labels_from_row(row).denominators != row["C_denominators"]:
            raise ValueError("accepted C component denominators changed")


def pack(rows, arm):
    width = max(len(row["source_ids"]) for row in rows)
    source_ids = mx.array([row["source_ids"] + [PAD] * (width - len(row["source_ids"])) for row in rows])
    source_valid = source_ids != PAD
    counts = {"source_positions": sum(len(row["source_ids"]) for row in rows),
        "padded_source_positions": source_ids.size, "source_padding": source_ids.size - sum(len(row["source_ids"]) for row in rows)}
    if arm == "B100":
        target_width = max(len(row["target_ids"]) + 1 for row in rows)
        decoder = mx.array([[BOS, *row["target_ids"], *([PAD] * (target_width - len(row["target_ids"]) - 1))] for row in rows])
        target = mx.array([[*row["target_ids"], EOS, *([PAD] * (target_width - len(row["target_ids"]) - 1))] for row in rows])
        valid = target != PAD
        counts.update(decoder_event_positions=sum(len(row["target_ids"]) + 1 for row in rows),
            padded_decoder_positions=target.size, decoder_padding=target.size - sum(len(row["target_ids"]) + 1 for row in rows))
        return (source_ids, source_valid, decoder, target, valid), counts
    examples = [{"source_ids": source_ids[index:index+1], "source_valid": source_valid[index:index+1],
        "labels": labels_from_row(row), "encoder_positions": tuple(row["encoder_positions"]),
        "legal": mx.array(row["legal"], dtype=mx.bool_), "backend": "native"}
        for index, row in enumerate(rows)]
    positions = sum(row["native_C_positions"] for row in rows)
    counts.update(decoder_event_positions=positions, padded_decoder_positions=positions, decoder_padding=0)
    return examples, counts


def objective(model, packed, arm, denominators, dtype):
    if arm == "C101":
        return c_microbatch_loss(model, packed, denominators["C"], dtype=dtype)
    source, source_valid, decoder, target, valid = packed
    logits = model(source, decoder, source_valid, valid, dtype=dtype, backend="native")
    return masked_cross_entropy(logits, target, valid) / denominators["B"]


class PairedTrainer:
    def __init__(self, model, arm, identities, *, microbatch_size, peak_lr=3e-4,
                 dtype=mx.bfloat16, enforce_complete_target=True):
        if arm not in ("B100", "C101") or microbatch_size < 1:
            raise ValueError("invalid arm/microbatch")
        self.model, self.arm, self.identities = model, arm, identities
        self.microbatch_size, self.peak_lr, self.dtype = microbatch_size, peak_lr, dtype
        self.enforce_complete_target = enforce_complete_target
        self.optimizer = AdamW(flat_parameters(model))
        self.accumulator = GradientAccumulator(flat_parameters(model))
        self.queue, self.partition, self.completed_microbatches, self.denominators = [], [], 0, None
        self.committed_exposure, self.pending_charge, self.loss = 0, 0, 0.
        self.reader_state = None
        self.clock = {"planned_exposure": 10_000_000, "warmup": 200_000, "floor_fraction": .1, "peak": peak_lr}
        self.rng = mx.random.key(42)
        self.metrics = {}
        self.consumption = []

    def begin(self, queue, reader_state):
        if self.queue or self.accumulator.microbatches:
            raise ValueError("unfinished common queue")
        charges = [item["canonical_charge"] for item in queue]
        if not charges or any(type(charge) is not int or charge <= 0 for charge in charges):
            raise ValueError("invalid queued canonical charge")
        if self.enforce_complete_target and (sum(charges) < 32768 or sum(charges[:-1]) >= 32768):
            raise ValueError("queue does not stop at the first whole presentation reaching 32768")
        if len({item["presentation_id"] for item in queue}) != len(queue):
            raise ValueError("duplicate common presentation ID")
        validate_queue(queue)
        self.queue = queue
        self.partition = [(offset, min(offset + self.microbatch_size, len(queue))) for offset in range(0, len(queue), self.microbatch_size)]
        self.denominators = queue_denominators(queue)
        self.pending_charge, self.loss = sum(charges), 0.
        self.completed_microbatches = 0
        self.reader_state = reader_state
        self.consumption = []
        self.metrics = {key: 0 for key in ("reader_seconds", "forward_backward_seconds", "synchronization_seconds",
            "optimizer_seconds", "accumulation_seconds", "source_positions", "padded_source_positions", "source_padding",
            "decoder_event_positions", "padded_decoder_positions", "decoder_padding")}

    def microstep(self):
        if self.completed_microbatches >= len(self.partition):
            raise ValueError("no remaining completed-microbatch boundary")
        start, stop = self.partition[self.completed_microbatches]
        begin = time.perf_counter()
        packed, counts = pack([presentation["row"] for presentation in self.queue[start:stop]], self.arm)
        self.metrics["reader_seconds"] += time.perf_counter() - begin
        begin = time.perf_counter()
        value, gradients = nn.value_and_grad(self.model, lambda model: objective(
            model, packed, self.arm, self.denominators, self.dtype))(self.model)
        mx.eval(value, gradients)
        self.metrics["forward_backward_seconds"] += time.perf_counter() - begin
        if not math.isfinite(float(value)):
            raise FloatingPointError("nonfinite queued objective")
        begin = time.perf_counter()
        self.accumulator.add(gradients)
        self.metrics["accumulation_seconds"] += time.perf_counter() - begin
        begin = time.perf_counter()
        mx.synchronize()
        self.metrics["synchronization_seconds"] += time.perf_counter() - begin
        self.loss += float(value)
        self.completed_microbatches += 1
        source_arrays = packed[0].tolist() if self.arm == "B100" else [example["source_ids"].tolist()[0] for example in packed]
        target_arrays = packed[3].tolist() if self.arm == "B100" else None
        cumulative = self.committed_exposure + sum(item["canonical_charge"] for item in self.queue[:start])
        for index, presentation in enumerate(self.queue[start:stop]):
            row = presentation["row"]
            cumulative += presentation["canonical_charge"]
            native = {key: presentation[key] for key in ("presentation_id", "variant_id", "canonical_charge")}
            native.update({key: row[key] for key in ("source_sha256", "target_sha256", "anchor_sha256")})
            native.update(phase=presentation.get("phase"), channel=presentation.get("channel"),
                cumulative_canonical_exposure=cumulative, native_source_ids=source_arrays[index])
            if self.arm == "B100":
                native["native_target_ids_with_EOS"] = target_arrays[index]
            else:
                native["native_event_labels"] = asdict(packed[index]["labels"])
                native["native_encoder_positions"] = list(packed[index]["encoder_positions"])
                native["native_legal_pointer_mask"] = packed[index]["legal"].tolist()
            self.consumption.append(native)
        for key, value in counts.items():
            self.metrics[key] += value
        return float(self.loss)

    def finish(self):
        if not self.queue or self.completed_microbatches != len(self.partition):
            raise ValueError("optimizer update attempted before common queue completion")
        endpoint = self.committed_exposure + self.pending_charge
        lr = pilot_lr(endpoint, self.peak_lr)
        begin = time.perf_counter()
        weights, norm = self.optimizer.apply(flat_parameters(self.model),
            self.accumulator.gradients(already_normalized=True), lr)
        self.model.update(tree_unflatten(list(weights.items())))
        self.accumulator.clear()
        mx.eval(self.model.parameters(), self.optimizer.m, self.optimizer.v, self.accumulator.values)
        mx.synchronize()
        self.metrics["optimizer_seconds"] += time.perf_counter() - begin
        result = {"arm": self.arm, "update": self.optimizer.step, "canonical_charge": self.pending_charge,
            "committed_canonical_exposure": endpoint, "lr": lr, "loss": self.loss, "gradient_norm": norm,
            "microsteps": self.completed_microbatches, "examples": len(self.queue),
            "overshoot": self.pending_charge - 32768, "denominators": self.denominators,
            "presentation_ids": [row["presentation_id"] for row in self.queue],
            "actual_consumption": self.consumption, **self.metrics}
        self.committed_exposure = endpoint
        self.pending_charge, self.completed_microbatches, self.loss = 0, 0, 0.
        self.queue, self.partition, self.denominators = [], [], None
        return result

    def update(self, queue, reader_state):
        self.begin(queue, reader_state)
        while self.completed_microbatches < len(self.partition):
            self.microstep()
        return self.finish()

    def arrays(self):
        result = {prefix + "::" + name: value for prefix, values in (
            ("model", flat_parameters(self.model)), ("m", self.optimizer.m),
            ("v", self.optimizer.v), ("acc", self.accumulator.values)) for name, value in values.items()}
        result["rng"] = self.rng
        return result

    def state_hash(self):
        digest = hashlib.sha256()
        for key, value in sorted(self.arrays().items()):
            array = np.asarray(value)
            digest.update(json.dumps([key, list(array.shape), str(array.dtype)], separators=(",", ":")).encode())
            digest.update(array.tobytes())
        digest.update(json.dumps([self.optimizer.step, self.committed_exposure, self.pending_charge,
            self.completed_microbatches, self.denominators, self.partition, self.loss], sort_keys=True).encode())
        return digest.hexdigest()


def file_hash(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def forward_probe(trainer, row):
    probe = dict(row)
    if len(row["source_ids"]) < trainer.model.config.max_context:
        probe["source_ids"] = [*row["source_ids"], PAD]
    packed, _ = pack([probe], trainer.arm)
    denominators = queue_denominators([{"row": row}])
    value = objective(trainer.model, packed, trainer.arm, denominators, trainer.dtype)
    mx.eval(value)
    if not math.isfinite(float(value)):
        raise FloatingPointError("checkpoint masked forward is nonfinite")
    return hashlib.sha256(np.asarray(value.astype(mx.float32)).tobytes()).hexdigest()


def validate_checkpoint_clock(meta):
    for key in ("optimizer_step", "committed_exposure", "pending_charge", "completed_microbatches", "accumulator_microbatches"):
        if type(meta[key]) is not int or meta[key] < 0:
            raise ValueError("checkpoint clock counter must be a nonnegative integer")
    if (meta["optimizer_step"] == 0) != (meta["committed_exposure"] == 0):
        raise ValueError("checkpoint optimizer/exposure clock mismatch")
    if meta["enforce_complete_target"] and meta["committed_exposure"] < meta["optimizer_step"] * 32768:
        raise ValueError("checkpoint optimizer step exceeds completed canonical exposure")
    endpoint = meta["committed_exposure"] + meta["pending_charge"]
    reader = meta["reader_state"] or {}
    if "exposure" in reader:
        if type(reader["exposure"]) is not int or reader["exposure"] != endpoint:
            raise ValueError("checkpoint shared reader/exposure clock mismatch")
    if "immutable_benchmark_queue_selector" in reader:
        charges = reader["immutable_benchmark_queue_selector"]["phase_charges"]
        if any(type(value) is not int or value < 0 for value in charges.values()) or sum(charges.values()) != endpoint:
            raise ValueError("checkpoint BENCH reader/exposure clock mismatch")
    if not math.isfinite(meta["loss"]):
        raise ValueError("checkpoint loss is nonfinite")


def validate_checkpoint_accumulator(meta, arrays):
    if meta["accumulator_microbatches"] != meta["completed_microbatches"]:
        raise ValueError("checkpoint completed/accumulated microbatches differ")
    if not meta["queue"] and (meta["pending_charge"] or meta["completed_microbatches"]
            or meta["denominators"] or meta["partition"] or meta["loss"]):
        raise ValueError("checkpoint boundary has pending state")
    if meta["accumulator_microbatches"] == 0 and any(
            np.any(value) for key, value in arrays.items() if key.startswith("acc::")):
        raise ValueError("checkpoint empty accumulator has nonzero gradients")


def save_paired_checkpoint(trainer, destination, probe_row):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError(destination)
    temporary = Path(tempfile.mkdtemp(prefix=destination.name + ".partial-", dir=destination.parent))
    mx.eval(trainer.arrays())
    arrays = {key: np.asarray(value) for key, value in trainer.arrays().items()}
    if any(not np.isfinite(value).all() for value in arrays.values()):
        raise FloatingPointError("nonfinite checkpoint array")
    np.savez(temporary / "arrays.npz", **arrays)
    with np.load(temporary / "arrays.npz", allow_pickle=False) as readback:
        if set(readback.files) != set(arrays) or any(not np.array_equal(readback[key], value) for key, value in arrays.items()):
            raise ValueError("checkpoint array readback mismatch")
        loaded = {key: mx.array(readback[key]) for key in arrays}
    trainer.model.update(tree_unflatten([(key.removeprefix("model::"), value) for key, value in loaded.items() if key.startswith("model::")]))
    meta = {"schema": "paired_complete_queue_resume_v3", "arm": trainer.arm, "config": asdict(trainer.model.config),
        "identities": trainer.identities, "working_dtype": str(trainer.dtype), "backend": "native",
        "optimizer_policy": trainer.optimizer.policy(), "optimizer_step": trainer.optimizer.step,
        "clock": trainer.clock, "microbatch_size": trainer.microbatch_size, "enforce_complete_target": trainer.enforce_complete_target,
        "queue": [{key: value for key, value in row.items() if key != "row"} for row in trainer.queue],
        "partition": trainer.partition, "completed_microbatches": trainer.completed_microbatches,
        "denominators": trainer.denominators, "pending_charge": trainer.pending_charge,
        "committed_exposure": trainer.committed_exposure, "loss": trainer.loss,
        "accumulator_microbatches": trainer.accumulator.microbatches, "metrics": trainer.metrics,
        "actual_consumption": trainer.consumption,
        "reader_state": trainer.reader_state, "python_rng": random.getstate(),
        "numpy_rng": [np.random.get_state()[0], np.random.get_state()[1].tolist(), *np.random.get_state()[2:]],
        "rng_policy": "explicit model construction keys; no global MLX RNG consumed by training",
        "shapes": {key: list(value.shape) for key, value in arrays.items()},
        "dtypes": {key: str(value.dtype) for key, value in arrays.items()},
        "probe_variant_id": probe_row["variant_id"], "forward_probe_sha256": forward_probe(trainer, probe_row)}
    validate_checkpoint_clock(meta)
    validate_checkpoint_accumulator(meta, arrays)
    (temporary / "metadata.json").write_text(json.dumps(meta, sort_keys=True, indent=2, allow_nan=False) + "\n")
    manifest = {name: file_hash(temporary / name) for name in ("arrays.npz", "metadata.json")}
    (temporary / "COMPLETE.json").write_text(json.dumps(manifest, sort_keys=True) + "\n")
    os.rename(temporary, destination)
    return manifest


def _tuples(value):
    return tuple(_tuples(item) for item in value) if isinstance(value, list) else value


def load_paired_checkpoint(trainer, source, rows):
    source = Path(source)
    manifest = json.loads((source / "COMPLETE.json").read_text())
    if set(manifest) != {"arrays.npz", "metadata.json"} or any(file_hash(source / name) != expected for name, expected in manifest.items()):
        raise ValueError("checkpoint checksum/inventory mismatch")
    meta = json.loads((source / "metadata.json").read_text())
    expected = {"schema": "paired_complete_queue_resume_v3", "arm": trainer.arm, "config": asdict(trainer.model.config),
        "identities": trainer.identities, "working_dtype": str(trainer.dtype), "backend": "native",
        "optimizer_policy": trainer.optimizer.policy(), "clock": trainer.clock,
        "microbatch_size": trainer.microbatch_size, "enforce_complete_target": trainer.enforce_complete_target}
    if any(meta[key] != value for key, value in expected.items()):
        raise ValueError("checkpoint configuration identity mismatch")
    validate_checkpoint_clock(meta)
    shapes = trainer.arrays()
    with np.load(source / "arrays.npz", allow_pickle=False) as saved:
        if set(saved.files) != set(shapes):
            raise ValueError("checkpoint array inventory mismatch")
        arrays = {}
        for key, template in shapes.items():
            array = saved[key]
            expected_dtype = np.uint32 if key == "rng" else np.float32
            if (array.shape != template.shape or array.dtype != expected_dtype
                    or list(array.shape) != meta["shapes"][key] or str(array.dtype) != meta["dtypes"][key]
                    or not np.isfinite(array).all()):
                raise ValueError("checkpoint shape/dtype/finite-state mismatch")
            arrays[key] = array
    validate_checkpoint_accumulator(meta, arrays)
    arrays = {key: mx.array(value) for key, value in arrays.items()}
    trainer.model.update(tree_unflatten([(key.removeprefix("model::"), value) for key, value in arrays.items() if key.startswith("model::")]))
    for prefix, destination in (("m", trainer.optimizer.m), ("v", trainer.optimizer.v), ("acc", trainer.accumulator.values)):
        for key in destination:
            destination[key] = arrays[prefix + "::" + key]
    trainer.rng = arrays["rng"]
    trainer.optimizer.step = meta["optimizer_step"]
    trainer.committed_exposure, trainer.pending_charge, trainer.loss = meta["committed_exposure"], meta["pending_charge"], meta["loss"]
    trainer.completed_microbatches = meta["completed_microbatches"]
    trainer.partition = [tuple(part) for part in meta["partition"]]
    trainer.denominators, trainer.metrics, trainer.reader_state = meta["denominators"], meta["metrics"], meta["reader_state"]
    trainer.consumption = meta["actual_consumption"]
    trainer.accumulator.microbatches = meta["accumulator_microbatches"]
    trainer.accumulator.denominator = 0
    trainer.queue = [{**item, "row": rows[item["variant_id"]]} for item in meta["queue"]]
    if trainer.queue:
        validate_queue(trainer.queue)
        reconstructed_denominators = queue_denominators(trainer.queue)
        expected_partition = [(offset, min(offset + trainer.microbatch_size, len(trainer.queue)))
            for offset in range(0, len(trainer.queue), trainer.microbatch_size)]
        if (reconstructed_denominators != trainer.denominators
                or sum(item["canonical_charge"] for item in trainer.queue) != trainer.pending_charge
                or trainer.completed_microbatches != trainer.accumulator.microbatches
                or not 0 <= trainer.completed_microbatches <= len(trainer.partition)
                or trainer.partition != expected_partition
                or not math.isfinite(trainer.loss)):
            raise ValueError("checkpoint common queue objective mismatch")
        # JSON key sorting must not change the approved component reduction order.
        trainer.denominators = reconstructed_denominators
    elif trainer.pending_charge or trainer.completed_microbatches or trainer.denominators or trainer.partition:
        raise ValueError("checkpoint boundary has pending state")
    random.setstate(_tuples(meta["python_rng"]))
    state = meta["numpy_rng"]
    np.random.set_state((state[0], np.array(state[1], dtype=np.uint32), *state[2:]))
    if forward_probe(trainer, rows[meta["probe_variant_id"]]) != meta["forward_probe_sha256"]:
        raise ValueError("checkpoint real masked-forward readback mismatch")
    return meta
