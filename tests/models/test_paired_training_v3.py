import hashlib
import json
from pathlib import Path
import shutil

import mlx.core as mx
import numpy as np
import pytest

from src.data.mixed_reader_v3 import native_shape
from src.models.bc import B100, C101
from src.models.core import EncoderDecoderConfig
from src.models.paired_training_v3 import (
    PairedTrainer, file_hash, load_paired_checkpoint, queue_denominators, save_paired_checkpoint,
    validate_checkpoint_clock,
)
from src.models.tokenizer import ByteBPE


def fixture_rows():
    tokenizer = ByteBPE()
    rows = []
    for index, (source, target) in enumerate((("abc", "abc"), ("axc", "abc"), ("ab", "abc"), ("éa", "é"))):
        row = {"variant_id": f"tiny/{index}", "source": source, "anchor": target, "target": target,
            **native_shape(tokenizer, source, target, target)}
        for field in ("source", "anchor", "target"):
            row[field + "_sha256"] = hashlib.sha256(row[field].encode()).hexdigest()
        rows.append(row)
    return rows


def queue(rows, ordinal=0):
    return [{"presentation_id": f"tiny/{ordinal}/{index}", "variant_id": row["variant_id"],
        "canonical_charge": row["canonical_charge"], "row": row} for index, row in enumerate(rows)]


def trainer(arm, *, microbatch=1, dtype=mx.bfloat16):
    config = EncoderDecoderConfig(320, 8, 1, 1, 2, 1, 12, 64)
    model = B100(config, seed=42) if arm == "B100" else C101(config, seed=42, pointer_width=4)
    return PairedTrainer(model, arm, {"ledger": "tiny_unit_fixture", "code": "fixture_v3"},
        microbatch_size=microbatch, dtype=dtype, enforce_complete_target=False)


@pytest.mark.parametrize("arm", ("B100", "C101"))
def test_whole_update_denominators_uneven_microbatch_gradient_and_one_step(arm):
    rows = fixture_rows()
    scientific_queue = queue(rows)
    den = queue_denominators(scientific_queue)
    assert den["B"] == sum(len(row["target_ids"]) + 1 for row in rows)
    assert den["C"] == {key: sum(row["C_denominators"][key] for row in rows)
                         for key in ("action", "start", "end", "vocabulary")}
    full, split = trainer(arm, microbatch=4, dtype=mx.float32), trainer(arm, microbatch=3, dtype=mx.float32)
    for instance in (full, split):
        instance.begin(scientific_queue, {"next_id": 4})
        while instance.completed_microbatches < len(instance.partition):
            instance.microstep()
        assert instance.denominators == den
        assert instance.optimizer.step == 0
        assert all(value.dtype == mx.float32 for value in instance.accumulator.values.values())
    for name, left in full.accumulator.values.items():
        a, b = np.asarray(left), np.asarray(split.accumulator.values[name])
        assert np.linalg.norm(a - b) / max(np.linalg.norm(a), 1e-12) < 1e-5
    for instance in (full, split):
        result = instance.finish()
        assert result["canonical_charge"] == sum(row["canonical_charge"] for row in rows)
        assert instance.optimizer.step == 1
        assert instance.accumulator.microbatches == 0
        assert instance.pending_charge == 0
        assert result["lr"] > 0


@pytest.mark.parametrize("arm", ("B100", "C101"))
@pytest.mark.parametrize("mid_update", (False, True))
def test_cold_boundary_and_mid_resume_pending_objective_then_next_twenty(tmp_path, arm, mid_update):
    rows = fixture_rows()
    lookup = {row["variant_id"]: row for row in rows}
    control = trainer(arm)
    control.update(queue(rows), {"cursor": 4, "phase": "P0"})
    if mid_update:
        control.begin(queue(rows, 1), {"cursor": 8, "phase": "P0"})
        control.microstep()
        assert control.pending_charge > 0 and control.committed_exposure == 42
    path = tmp_path / "checkpoint"
    saved_state = control.state_hash()
    save_paired_checkpoint(control, path, rows[0])
    resumed = trainer(arm)
    meta = load_paired_checkpoint(resumed, path, lookup)
    assert resumed.state_hash() == saved_state
    assert resumed.reader_state == control.reader_state
    assert meta["working_dtype"] == "mlx.core.bfloat16"
    if mid_update:
        for instance in (control, resumed):
            while instance.completed_microbatches < len(instance.partition):
                instance.microstep()
            instance.finish()
        assert resumed.state_hash() == control.state_hash()
    for index in range(20):
        next_queue = queue(rows, index + 2)
        state = {"cursor": (index + 3) * 4, "phase": "P0", "pool_cursors": {"fixture": index}}
        a, b = control.update(next_queue, state), resumed.update(next_queue, state)
        assert a["presentation_ids"] == b["presentation_ids"]
        assert a["denominators"] == b["denominators"]
        assert a["committed_canonical_exposure"] == b["committed_canonical_exposure"]
        assert a["loss"] == b["loss"]
        assert control.state_hash() == resumed.state_hash()


def rehash(directory):
    (directory / "COMPLETE.json").write_text(json.dumps({name: file_hash(directory / name)
        for name in ("arrays.npz", "metadata.json")}, sort_keys=True) + "\n")


def test_cold_mid_restore_keeps_original_c_component_reduction_order(tmp_path):
    rows = fixture_rows()
    control = trainer("C101", microbatch=3)
    control.update(queue(rows), {"exposure": 42})
    control.begin(queue(rows, 1), {"exposure": 84})
    control.microstep()
    path = tmp_path / "ordered-component-checkpoint"
    save_paired_checkpoint(control, path, rows[0])
    saved = json.loads((path / "metadata.json").read_text())
    assert list(saved["denominators"]["C"]) == ["action", "end", "start", "vocabulary"]
    resumed = trainer("C101", microbatch=3)
    load_paired_checkpoint(resumed, path, {row["variant_id"]: row for row in rows})
    assert list(resumed.denominators["C"]) == ["action", "start", "end", "vocabulary"]
    for instance in (control, resumed):
        while instance.completed_microbatches < len(instance.partition):
            instance.microstep()
    a, b = control.finish(), resumed.finish()
    assert a["loss"] == b["loss"]
    assert control.state_hash() == resumed.state_hash()


@pytest.mark.parametrize("arm", ("B100", "C101"))
@pytest.mark.parametrize("corruption", ("accumulator_counter", "accumulator_array", "saved_loss"))
def test_rehashed_boundary_cannot_carry_unqueued_gradient_state(tmp_path, arm, corruption):
    rows = fixture_rows()
    instance = trainer(arm)
    instance.update(queue(rows), {"exposure": 42})
    path = tmp_path / "boundary"
    save_paired_checkpoint(instance, path, rows[0])
    if corruption == "accumulator_array":
        with np.load(path / "arrays.npz", allow_pickle=False) as data:
            arrays = {key: data[key] for key in data.files}
        key = next(key for key in arrays if key.startswith("acc::"))
        arrays[key].flat[0] = 1.
        np.savez(path / "arrays.npz", **arrays)
    else:
        meta = json.loads((path / "metadata.json").read_text())
        meta["accumulator_microbatches" if corruption == "accumulator_counter" else "loss"] = 1
        (path / "metadata.json").write_text(json.dumps(meta))
    rehash(path)
    with pytest.raises(ValueError, match="microbatches differ|pending state|nonzero gradients"):
        load_paired_checkpoint(trainer(arm), path, {row["variant_id"]: row for row in rows})


@pytest.mark.parametrize("arm", ("B100", "C101"))
def test_atomic_save_rejects_nonzero_empty_gradient_accumulator(tmp_path, arm):
    rows = fixture_rows()
    instance = trainer(arm)
    key = next(iter(instance.accumulator.values))
    instance.accumulator.values[key] = mx.ones_like(instance.accumulator.values[key])
    destination = tmp_path / "invalid-boundary"
    with pytest.raises(ValueError, match="nonzero gradients"):
        save_paired_checkpoint(instance, destination, rows[0])
    assert not destination.exists()


@pytest.mark.parametrize("corruption", ("bytes", "dtype", "nonfinite", "queue_charge", "partition", "identity",
    "committed_clock", "reader_clock", "negative_clock", "noninteger_clock", "optimizer_clock"))
def test_corrupted_checkpoint_is_rejected(tmp_path, corruption):
    rows = fixture_rows()
    instance = trainer("C101")
    instance.begin(queue(rows), {"cursor": 4, "exposure": 42})
    instance.microstep()
    path = tmp_path / "checkpoint"
    save_paired_checkpoint(instance, path, rows[0])
    if corruption in ("bytes", "dtype", "nonfinite"):
        if corruption == "bytes":
            with (path / "arrays.npz").open("ab") as stream:
                stream.write(b"corruption")
        else:
            with np.load(path / "arrays.npz", allow_pickle=False) as data:
                arrays = {key: data[key] for key in data.files}
            key = next(key for key in arrays if key.startswith("acc::"))
            arrays[key] = arrays[key].astype(np.float64) if corruption == "dtype" else np.full_like(arrays[key], np.nan)
            np.savez(path / "arrays.npz", **arrays)
            rehash(path)
    else:
        meta = json.loads((path / "metadata.json").read_text())
        if corruption == "queue_charge":
            meta["queue"][0]["canonical_charge"] += 1
        elif corruption == "partition":
            meta["partition"][0][1] += 1
        elif corruption == "identity":
            meta["identities"]["ledger"] = "wrong"
        elif corruption == "committed_clock":
            meta["committed_exposure"] += 1
        elif corruption == "reader_clock":
            meta["reader_state"]["exposure"] += 1
        elif corruption == "negative_clock":
            meta["committed_exposure"] = -1
        elif corruption == "noninteger_clock":
            meta["pending_charge"] = 42.0
        elif corruption == "optimizer_clock":
            meta["optimizer_step"] = 1
        (path / "metadata.json").write_text(json.dumps(meta))
        rehash(path)
    with pytest.raises(ValueError):
        load_paired_checkpoint(trainer("C101"), path, {row["variant_id"]: row for row in rows})


def test_benchmark_reader_clock_is_preserved_and_inconsistent_rehash_rejected(tmp_path):
    rows = fixture_rows()
    instance = trainer("B100")
    instance.update(queue(rows), {"immutable_benchmark_queue_selector": {"phase_charges": {"P0": 42}}})
    path = tmp_path / "bench-boundary"
    save_paired_checkpoint(instance, path, rows[0])
    lookup = {row["variant_id"]: row for row in rows}
    load_paired_checkpoint(trainer("B100"), path, lookup)
    meta = json.loads((path / "metadata.json").read_text())
    meta["reader_state"]["immutable_benchmark_queue_selector"]["phase_charges"]["P0"] += 1
    (path / "metadata.json").write_text(json.dumps(meta))
    rehash(path)
    with pytest.raises(ValueError, match="BENCH reader/exposure clock"):
        load_paired_checkpoint(trainer("B100"), path, lookup)


@pytest.mark.parametrize("mid_update", (False, True))
def test_positive_committed_clock_change_rejected_at_boundary_and_mid_update(tmp_path, mid_update):
    rows = fixture_rows()
    instance = trainer("C101")
    instance.update(queue(rows), {"exposure": 42})
    if mid_update:
        instance.begin(queue(rows, 1), {"exposure": 84})
        instance.microstep()
    path = tmp_path / "positive-clock"
    save_paired_checkpoint(instance, path, rows[0])
    meta = json.loads((path / "metadata.json").read_text())
    meta["committed_exposure"] += 1
    (path / "metadata.json").write_text(json.dumps(meta))
    rehash(path)
    with pytest.raises(ValueError, match="shared reader/exposure clock"):
        load_paired_checkpoint(trainer("C101"), path, {row["variant_id"]: row for row in rows})


def test_positive_optimizer_step_cannot_exceed_completed_32768_queues():
    meta = {"optimizer_step": 1, "committed_exposure": 32815, "pending_charge": 0,
        "completed_microbatches": 0, "accumulator_microbatches": 0, "enforce_complete_target": True,
        "reader_state": {"exposure": 32815}, "loss": 0.}
    validate_checkpoint_clock(meta)
    meta["optimizer_step"] = 2
    with pytest.raises(ValueError, match="step exceeds completed canonical exposure"):
        validate_checkpoint_clock(meta)


def test_missing_or_changed_accepted_row_stops_without_replacement():
    rows = fixture_rows()
    rows[0]["source"] = "changed"
    with pytest.raises(ValueError, match="bytes changed"):
        trainer("B100").begin(queue(rows), {})


def test_qualification_requires_actual_32768_queue():
    instance = trainer("B100")
    instance.enforce_complete_target = True
    with pytest.raises(ValueError, match="32768"):
        instance.begin(queue(fixture_rows()), {})
