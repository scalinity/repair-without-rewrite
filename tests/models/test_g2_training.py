import hashlib
from pathlib import Path
import mlx.core as mx
import pytest

from src.data.g2_artifacts import read_complete
from src.data.g2_stream import G2BenchStream
from src.data.mixed_reader_v3 import native_shape
from src.models.bc import B100, C101
from src.models.core import EncoderDecoderConfig
from src.models.g2_training import G2Native, load_g2_checkpoint, save_g2_checkpoint
from src.models.tokenizer import ByteBPE


class FixtureRoot:
    def __init__(self, path):
        self.root = path
    def preflight(self):
        return dict(volume_uuid_sha256="synthetic", root_binding_sha256="synthetic",
                    policy_sha256="synthetic")
    def path(self, relative):
        return self.root / relative


def fixture(arm):
    row = dict(variant_id="unit", source="a" * 54, anchor="b" * 54, target="b" * 54,
               **native_shape(ByteBPE(), "a" * 54, "b" * 54, "b" * 54))
    for field in ("source", "anchor", "target"):
        row[field + "_sha256"] = hashlib.sha256(row[field].encode()).hexdigest()
    charge = row["canonical_charge"]
    count = (32768 + charge - 1) // charge
    ledger, updates = [], []
    for phase in ("P0", "P1", "P2"):
        first = len(ledger)
        for _ in range(count):
            ordinal = len(ledger)
            ledger.append(dict(presentation_id=f"fixture/{ordinal}", ordinal=ordinal, phase=phase,
                channel="natural", subpath=[], variant_id="unit", canonical_charge=charge,
                start_exposure=ordinal * charge, end_exposure=(ordinal + 1) * charge))
        updates.append(dict(first_ordinal=first, last_ordinal=len(ledger) - 1,
            canonical_charge=count * charge, phase_segments={phase: count * charge}))
    stream = G2BenchStream({"unit": row}, ledger, updates, "D0", "U8")
    config = EncoderDecoderConfig(320, 8, 1, 1, 2, 1, 12, 64)
    model = B100(config, seed=42) if arm == "B100" else C101(config, seed=42, pointer_width=4)
    return G2Native(model, arm, {"ledger": "synthetic_unit_only"}, stream), row


@pytest.mark.parametrize("arm", ("B100", "C101"))
@pytest.mark.parametrize("mid", (False, True))
def test_actual_update_checkpoint_preserves_pending_objective_and_next_updates(tmp_path, arm, mid):
    root = FixtureRoot(tmp_path)
    control, row = fixture(arm)
    first = control.update()
    assert first["canonical_charge"] < 32768
    if mid:
        control.begin(); control.microstep()
        assert control.native.completed_microbatches == 1
        assert control.native.accumulator.microbatches == 1
    save_g2_checkpoint(root, "snapshot", control, row)
    assert read_complete(tmp_path / "snapshot")["schema"] == "g2_atomic_artifact_v1"
    replay, _ = fixture(arm)
    load_g2_checkpoint(root, "snapshot", replay, {"unit": row})
    assert replay.state_hash() == control.state_hash()
    if mid:
        assert list(replay.native.denominators["C"]) == ["action", "start", "end", "vocabulary"]
        a, b = control.update(), replay.update()
        assert a["loss"] == b["loss"] and control.state_hash() == replay.state_hash()
    for _ in range(3):
        a, b = control.update(), replay.update()
        assert a["loss"] == b["loss"] and a["lr"] == b["lr"]
        assert a["denominators"] == b["denominators"]
        assert control.state_hash() == replay.state_hash()
        assert control.native.optimizer.step == replay.native.optimizer.step
    with pytest.raises(ValueError, match="incomplete"):
        read_complete(tmp_path / "snapshot.partial-failure")


def test_actual_native_clock_rejects_noninteger_and_a_master_denominator(tmp_path):
    control, _ = fixture("B100")
    control.begin()
    control.native.denominators["B"] += 1
    with pytest.raises(ValueError, match="denominator"):
        control.validate()
    control, _ = fixture("B100")
    control.native.optimizer.step = 0.0
    with pytest.raises(ValueError, match="integers"):
        control.validate()
