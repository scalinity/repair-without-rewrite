"""G2 actual-update training/resume; G1 mathematics and validation stay intact."""
from dataclasses import asdict
import hashlib
import json
import math
import random

from src.data.g2_artifacts import atomic_artifact, read_complete
from src.data.g2_geometry import actual_denominators
from src.data.g2_stream import canonical_cursor

SCHEMA = "paired_complete_actual_update_resume_g2_v1"


class G2Native:
    def __init__(self, model, arm, identities, stream):
        from src.models.paired_training_v3 import PairedTrainer
        self.native = PairedTrainer(model, arm, identities,
            microbatch_size=16 if arm == "B100" else 4, peak_lr=3e-4, enforce_complete_target=False)
        self.stream = stream
        self.native.reader_state = stream.state()

    def begin(self):
        self.native.begin(self.stream.actual_queue(), self.stream.state())
        self.validate()

    def microstep(self):
        return self.native.microstep()

    def finish(self):
        self.validate()
        result = self.native.finish()
        result.update(data_condition=self.stream.data_condition, update_condition=self.stream.update_condition,
            master_queue_index=self.stream.master_queue_index, subqueue_index=self.stream.subqueue_index)
        self.stream.finish_actual()
        self.native.reader_state = self.stream.state()
        self.validate()
        return result

    def update(self):
        if not self.native.queue:
            self.begin()
        while self.native.completed_microbatches < len(self.native.partition):
            self.microstep()
        return self.finish()

    def validate(self):
        native = self.native
        counters = (native.optimizer.step, native.committed_exposure, native.pending_charge,
                    native.completed_microbatches, native.accumulator.microbatches)
        if any(type(value) is not int or value < 0 for value in counters):
            raise ValueError("G2 native counters must be nonnegative integers")
        step, exposure = self.stream.completed_actual_clock()
        if native.optimizer.step != step or native.committed_exposure != exposure:
            raise ValueError("G2 actual optimizer/exposure clock mismatch")
        if native.reader_state != self.stream.state():
            raise ValueError("G2 native/reader cursor mismatch")
        if not math.isfinite(native.loss) or native.completed_microbatches != native.accumulator.microbatches:
            raise ValueError("G2 finite loss/accumulated microbatch mismatch")
        if native.queue:
            actual = self.stream.actual_queue()
            if ([row["presentation_id"] for row in native.queue] != [row["presentation_id"] for row in actual]
                    or native.pending_charge != sum(row["canonical_charge"] for row in actual)
                    or native.denominators != actual_denominators(actual)):
                raise ValueError("G2 pending actual queue/denominator mismatch")
            partition = [(start, min(start + native.microbatch_size, len(actual)))
                for start in range(0, len(actual), native.microbatch_size)]
            if native.partition != partition or not 0 <= native.completed_microbatches <= len(partition):
                raise ValueError("G2 pending microbatch cursor/partition mismatch")
        elif (native.pending_charge or native.partition or native.denominators
              or native.completed_microbatches or native.loss):
            raise ValueError("G2 complete actual boundary has pending work")

    def state_hash(self):
        digest = hashlib.sha256()
        digest.update(self.native.state_hash().encode())
        digest.update(canonical_cursor(self.stream.state()).encode())
        digest.update(json.dumps(self.native.consumption, sort_keys=True, separators=(",", ":"),
                                 allow_nan=False).encode())
        return digest.hexdigest()


def save_g2_checkpoint(root, relative, trainer, probe):
    root.preflight()
    import mlx.core as mx
    from mlx.utils import tree_unflatten
    import numpy as np
    from src.models.paired_training_v3 import forward_probe
    trainer.validate()
    native = trainer.native
    mx.eval(native.arrays())
    arrays = {key: np.asarray(value) for key, value in native.arrays().items()}
    if any(not np.isfinite(value).all() for value in arrays.values()):
        raise FloatingPointError("nonfinite G2 checkpoint array")
    if native.accumulator.microbatches == 0 and any(np.any(value) for key, value in arrays.items() if key.startswith("acc::")):
        raise ValueError("G2 empty accumulator has nonzero gradients")
    with atomic_artifact(root, relative) as pending:
        np.savez(pending / "arrays.npz", **arrays)
        with np.load(pending / "arrays.npz", allow_pickle=False) as saved:
            if set(saved.files) != set(arrays) or any(not np.array_equal(saved[key], value) for key, value in arrays.items()):
                raise ValueError("G2 exact checkpoint readback failed")
            rebound = {key: mx.array(saved[key]) for key in arrays if key.startswith("model::")}
        native.model.update(tree_unflatten([(key.removeprefix("model::"), value) for key, value in rebound.items()]))
        state = trainer.stream.state()
        meta = {"schema": SCHEMA, "data_condition": state["data_condition"], "update_condition": state["update_condition"],
            "master_queue_index": state["master_queue_index"], "subqueue_index": state["subqueue_index"],
            "stream": state, "arm": native.arm, "config": asdict(native.model.config),
            "identities": native.identities, "root_identity": root.preflight(),
            "working_dtype": str(native.dtype), "backend": "native", "optimizer_policy": native.optimizer.policy(),
            "optimizer_step": native.optimizer.step, "committed_exposure": native.committed_exposure,
            "pending_charge": native.pending_charge, "microbatch_size": native.microbatch_size,
            "queue": [{key: value for key, value in row.items() if key != "row"} for row in native.queue],
            "pending_presentation_range": None if not native.queue else [native.queue[0]["ordinal"], native.queue[-1]["ordinal"]],
            "partition": native.partition, "denominators": native.denominators,
            "completed_microbatches": native.completed_microbatches, "accumulator_microbatches": native.accumulator.microbatches,
            "loss": native.loss, "clock": native.clock, "metrics": native.metrics, "actual_consumption": native.consumption,
            "rng_policy": "inherited explicit model keys; restore process Python/NumPy RNG separately",
            "python_rng": random.getstate(), "numpy_rng": [np.random.get_state()[0], np.random.get_state()[1].tolist(),
                *np.random.get_state()[2:]], "shapes": {key: list(value.shape) for key, value in arrays.items()},
            "dtypes": {key: str(value.dtype) for key, value in arrays.items()}, "probe_variant_id": probe["variant_id"],
            "forward_probe_sha256": forward_probe(native, probe), "deterministic_state_sha256": trainer.state_hash()}
        (pending / "metadata.json").write_text(json.dumps(meta, sort_keys=True, indent=2, allow_nan=False) + "\n")
    return read_complete(root.path(relative))


def load_g2_checkpoint(root, relative, trainer, rows):
    root.preflight()
    path = root.path(relative)
    complete = read_complete(path)
    if set(complete["files"]) != {"arrays.npz", "metadata.json"}:
        raise ValueError("G2 native checkpoint inventory mismatch")
    import mlx.core as mx
    from mlx.utils import tree_unflatten
    import numpy as np
    from src.models.paired_training_v3 import forward_probe, _tuples
    native = trainer.native
    meta = json.loads((path / "metadata.json").read_text())
    expected = {"schema": SCHEMA, "data_condition": trainer.stream.data_condition,
        "update_condition": trainer.stream.update_condition, "arm": native.arm, "config": asdict(native.model.config),
        "identities": native.identities, "working_dtype": str(native.dtype), "backend": "native",
        "optimizer_policy": native.optimizer.policy(), "clock": native.clock, "microbatch_size": native.microbatch_size}
    if any(meta[key] != value for key, value in expected.items()):
        raise ValueError("G2 checkpoint condition/model/clock identity mismatch")
    physical = root.preflight()
    if any(meta["root_identity"][key] != physical[key] for key in ("volume_uuid_sha256", "root_binding_sha256", "policy_sha256")):
        raise ValueError("G2 checkpoint physical root identity mismatch")
    templates = native.arrays()
    with np.load(path / "arrays.npz", allow_pickle=False) as saved:
        if set(saved.files) != set(templates):
            raise ValueError("G2 checkpoint array inventory mismatch")
        arrays = {}
        for key, template in templates.items():
            value = saved[key]
            expected_dtype = np.uint32 if key == "rng" else np.float32
            if (value.shape != template.shape or value.dtype != expected_dtype or not np.isfinite(value).all()
                    or list(value.shape) != meta["shapes"][key] or str(value.dtype) != meta["dtypes"][key]):
                raise ValueError("G2 checkpoint shape/dtype/finite-state mismatch")
            arrays[key] = mx.array(value)
    native.model.update(tree_unflatten([(key.removeprefix("model::"), value) for key, value in arrays.items() if key.startswith("model::")]))
    for prefix, destination in (("m", native.optimizer.m), ("v", native.optimizer.v), ("acc", native.accumulator.values)):
        for key in destination:
            destination[key] = arrays[prefix + "::" + key]
    native.rng = arrays["rng"]
    native.optimizer.step = meta["optimizer_step"]
    native.committed_exposure, native.pending_charge, native.loss = meta["committed_exposure"], meta["pending_charge"], meta["loss"]
    native.completed_microbatches = meta["completed_microbatches"]
    native.accumulator.microbatches = meta["accumulator_microbatches"]
    native.queue = [{**item, "row": rows[item["variant_id"]]} for item in meta["queue"]]
    native.partition = [tuple(pair) for pair in meta["partition"]]
    den = meta["denominators"]
    native.denominators = None if den is None else {"B": den["B"], "C": {
        name: den["C"][name] for name in ("action", "start", "end", "vocabulary")}}
    native.metrics, native.consumption = meta["metrics"], meta["actual_consumption"]
    trainer.stream.restore(meta["stream"])
    native.reader_state = trainer.stream.state()
    if meta["master_queue_index"] != trainer.stream.master_queue_index or meta["subqueue_index"] != trainer.stream.subqueue_index:
        raise ValueError("G2 checkpoint master/subqueue metadata mismatch")
    expected_range = None if not native.queue else [native.queue[0]["ordinal"], native.queue[-1]["ordinal"]]
    if expected_range != meta["pending_presentation_range"]:
        raise ValueError("G2 checkpoint pending presentation range mismatch")
    random.setstate(_tuples(meta["python_rng"]))
    state = meta["numpy_rng"]
    np.random.set_state((state[0], np.array(state[1], dtype=np.uint32), *state[2:]))
    mx.eval(native.arrays()); mx.synchronize()
    trainer.validate()
    if native.accumulator.microbatches == 0 and any(np.any(np.asarray(value)) for key, value in native.arrays().items() if key.startswith("acc::")):
        raise ValueError("G2 restored empty accumulator has nonzero gradients")
    if trainer.state_hash() != meta["deterministic_state_sha256"] or forward_probe(native, rows[meta["probe_variant_id"]]) != meta["forward_probe_sha256"]:
        raise ValueError("G2 restored exact state/forward identity mismatch")
    return meta
