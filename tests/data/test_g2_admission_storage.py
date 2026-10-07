import json
from types import SimpleNamespace

import pytest

from benchmarks.g2_admission_independent import reconstruct_remaining_storage


def fixture(tmp_path):
    directory = tmp_path / "receipts"
    directory.mkdir()
    root = SimpleNamespace(path=lambda relative: tmp_path / relative)
    configs = []
    def snapshot(relative, files):
        path = tmp_path / relative
        path.mkdir()
        for name, count in files.items():
            (path / name).write_bytes(b"x" * count)
        (path / "COMPLETE.json").write_text(json.dumps({"files":{
            name:{"bytes":count} for name, count in files.items()}}))
    for arm, count in (("B100", 10), ("C101", 20)):
        for data, condition in (("D0", "U8"), ("D1", "U1"), ("D1", "U8")):
            tag = f"{arm}-{data}-{condition}"
            paths = {label:tag + "-" + label for label in ("initial", "boundary", "mid", "final")}
            for relative in paths.values():
                snapshot(relative, {"arrays.npz":count, "metadata.json":3})
            (directory / f"bench-{tag}.attempt01.json").write_text(json.dumps({"checkpoint_relatives":paths}))
            configs.append({"recipe_id":"G2-" + tag, "save_endpoints":[
                {"master_completed":i} for i in [*range(13), 12]]})
    snapshot("by-initial", {"state.pt":30})
    snapshot("by-trained", {"state.pt":90})
    (directory / "byt5-qualification.attempt02.json").write_text(json.dumps({
        "initial_checkpoint":{"relative":"by-initial"}, "final_checkpoint":{"relative":"by-trained"}}))
    configs.append({"recipe_id":"G2-ByT5-fixed", "save_evaluate_pass_milestones":[0, 2, 5, 10]})
    return root, directory, configs


def test_future_storage_counts_unique_native_saves_and_three_trained_byt5_states(tmp_path):
    result, allowances = reconstruct_remaining_storage(*fixture(tmp_path))
    assert result == 82 * 16 * 1024**2 + 1470 + 56 * 1024**3
    assert sum(allowances.values()) == 56 * 1024**3


def test_storage_audit_rejects_false_complete_byte_count(tmp_path):
    inputs = fixture(tmp_path)
    (tmp_path / "by-trained" / "state.pt").write_bytes(b"truncated")
    with pytest.raises(AssertionError):
        reconstruct_remaining_storage(*inputs)
