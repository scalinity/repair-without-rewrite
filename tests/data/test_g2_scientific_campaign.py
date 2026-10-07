import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from benchmarks import g2_scientific_campaign as campaign
from benchmarks.g2_scientific_byt5 import incorporated_presentations


def test_seven_recipe_order_is_fixed():
    assert campaign.ORDER == (
        "G2-B100-D0-U8-seed42-lr3e-4", "G2-C101-D0-U8-seed42-lr3e-4",
        "G2-B100-D1-U1-seed42-lr3e-4", "G2-C101-D1-U1-seed42-lr3e-4",
        "G2-B100-D1-U8-seed42-lr3e-4", "G2-C101-D1-U8-seed42-lr3e-4",
        "G2-ByT5-D1-10pass-seed42-lr3e-4")
    campaign.validate_launch_order(campaign.ORDER[0], {})
    with pytest.raises(ValueError): campaign.validate_launch_order(campaign.ORDER[-1], {})


@pytest.mark.parametrize("status", ["RUNNING", "INTERRUPTED", "NUMERICAL_FAILURE", "STOPPED_DEFECT"])
def test_unresolved_recipe_blocks_successor(status):
    with pytest.raises(ValueError):
        campaign.validate_launch_order(campaign.ORDER[1], {campaign.ORDER[0]: [{"status": status}]})


@pytest.mark.parametrize("status", ["COMPLETED", "FAILED_NUMERICAL"])
def test_resolved_prescribed_recipe_allows_successor(status):
    campaign.validate_launch_order(campaign.ORDER[1], {campaign.ORDER[0]: [{"status": status}]})


def test_pending_microbatch_resume_cannot_save_or_evaluate_nominal_boundary():
    assert campaign.boundary_actions(248, True, 248, {248}, {248}) == (False, False)
    assert campaign.boundary_actions(248, False, 248, {248}, {248}) == (False, True)
    assert campaign.boundary_actions(249, False, 248, {248}, {248}) == (False, False)
    assert campaign.boundary_actions(248, False, None, {248}, {248}) == (True, True)


def test_observation_reuse_checks_state_and_payload(tmp_path, monkeypatch):
    safe = tmp_path / "receipts"; safe.mkdir(); monkeypatch.setattr(campaign, "SAFE", safe)
    monkeypatch.chdir(tmp_path); (tmp_path / "experiments/manifests").mkdir(parents=True)
    payload = tmp_path / "records.jsonl"; payload.write_text("retained output\n")
    root = SimpleNamespace(root=tmp_path, path=lambda relative: tmp_path / relative)
    receipt = campaign.record_observation(root, "recipe", 1, 248, "state1", tmp_path,
        {"calibration_use": {"calibration_evaluations": 1900, "calibration_ids_sha256": "ids"}}, [payload])
    assert campaign.previous_observation(root, "recipe", 248, "state1") == receipt
    with pytest.raises(ValueError): campaign.previous_observation(root, "recipe", 248, "changed-state")
    payload.write_text("changed output\n")
    with pytest.raises(ValueError): campaign.previous_observation(root, "recipe", 248, "state1")


def test_accelerator_lock_prevents_second_job(tmp_path):
    root = SimpleNamespace(path=lambda _: tmp_path / "lock")
    first = campaign.accelerator_lock(root)
    try:
        with pytest.raises(ValueError): campaign.accelerator_lock(root)
    finally:
        first.close()
    second = campaign.accelerator_lock(root); second.close()


@pytest.mark.parametrize("step,count", [(0, 0), (7056, 28224), (7057, 28228),
    (17641, 70564), (17642, 70568), (35282, 141128), (35283, 141130)])
def test_byt5_resume_cursor_uses_incorporated_presentations(step, count):
    assert incorporated_presentations(step) == count


@pytest.mark.parametrize("step", [-1, 35284, 7057.0, True])
def test_byt5_invalid_resume_cursor_rejected(step):
    with pytest.raises(ValueError): incorporated_presentations(step)


def test_claim_rejects_stale_checkpoint_and_attempt_number(tmp_path, monkeypatch):
    monkeypatch.setattr(campaign, "SAFE", tmp_path)
    name = campaign.ORDER[0]
    (tmp_path / f"scientific-start-{name}.attempt01.json").write_text("{}")
    outcome = {"status": "INTERRUPTED", "latest_verified_checkpoint": f"scientific-checkpoints-v1/{name}.latest"}
    (tmp_path / f"scientific-outcome-{name}.attempt01.json").write_text(json.dumps(outcome))
    monkeypatch.setattr(campaign, "read_complete", lambda path: {})
    root = SimpleNamespace(path=Path)
    with pytest.raises(ValueError): campaign.claim(root, name, {}, 1, None)
    with pytest.raises(ValueError): campaign.claim(root, name, {}, 2, None)
    with pytest.raises(ValueError): campaign.claim(root, name, {}, 2, f"scientific-checkpoints-v1/{name}.old")


def test_unauthorized_recipe_rejected():
    with pytest.raises(ValueError): campaign.recipe_path("G2-B100-D1-U8-seed1729-lr3e-4")
    with pytest.raises(ValueError): campaign.validate_launch_order("extra-recipe", {})


def test_calibration_consumption_requires_the_whole_frozen_panel():
    panel = [{"id": str(i), "role": "calibration"} for i in range(1900)]
    assert campaign.calibration_use(panel)["calibration_evaluations"] == 1900
    with pytest.raises(ValueError): campaign.calibration_use(panel[:-1])
    with pytest.raises(ValueError): campaign.calibration_use(panel + [panel[0]])


def test_portable_byt5_readback_rejects_equal_values_with_changed_dtype():
    import torch
    from benchmarks.g2_scientific_byt5 import assert_equal_tree
    state = {"model": {"weight": torch.tensor([1., 2.], dtype=torch.float32)}, "step": 7, "groups": [[0, 1]]}
    restored = {"model": {"weight": state["model"]["weight"].clone()}, "step": 7, "groups": [[0, 1]]}
    assert_equal_tree(state, restored, torch)
    restored["model"]["weight"] = restored["model"]["weight"].double()
    with pytest.raises(ValueError): assert_equal_tree(state, restored, torch)


def test_portable_byt5_readback_rejects_changed_optimizer_cursor():
    import torch
    from benchmarks.g2_scientific_byt5 import assert_equal_tree
    with pytest.raises(ValueError): assert_equal_tree({"step": 7, "groups": [[0, 1]]}, {"step": 8, "groups": [[0, 1]]}, torch)
