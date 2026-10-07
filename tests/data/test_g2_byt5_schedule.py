import copy
import json
from pathlib import Path
import random

import pytest

from src.data.g2_byt5 import training_batches
from src.data.g2_byt5_schedule import milestone_states, validate_states

RECIPE = Path("experiments/manifests/generation_2/recipe-G2-ByT5-D1-10pass-seed42-lr3e-4.attempt01.json")


@pytest.fixture
def recipe():
    return json.loads(RECIPE.read_text())


@pytest.mark.parametrize("passes,nominal,update,actual,offset,label", [
    (0, 0, 0, 0, 0, "initialization"),
    (2, 28226, 7057, 28228, 2, "2-pass nominal milestone — first completed update at/after boundary"),
    (5, 70565, 17642, 70568, 3, "5-pass nominal milestone — first completed update at/after boundary"),
    (10, 141130, 35283, 141130, 0, "10-pass exact endpoint"),
])
def test_exact_first_completed_state_and_truthful_label(recipe, passes, nominal, update, actual, offset, label):
    state = next(item for item in milestone_states(recipe) if item["nominal_passes"] == passes)
    assert state == dict(nominal_passes=passes, nominal_presentations=nominal,
                         optimizer_update=update, actual_presentations=actual,
                         presentation_offset=offset, label=label)
    if update:
        assert min((update - 1) * 4, 141130) < nominal <= actual


@pytest.mark.parametrize("field", ["nominal_passes", "nominal_presentations", "optimizer_update",
                                   "actual_presentations", "presentation_offset", "label"])
def test_any_changed_observation_field_is_rejected(recipe, field):
    states = copy.deepcopy(milestone_states(recipe))
    states[1][field] = "changed" if field == "label" else states[1][field] - 1
    with pytest.raises(ValueError, match="frontier milestone"):
        validate_states(recipe, states)


def test_schedule_observation_preserves_the_entire_qualified_training_stream(recipe):
    pairs = [dict(id=str(index), role="train", status="COMPLETED", source="a", target="b")
             for index in range(14113)]
    order = list(range(14113)); random.Random(42).shuffle(order)
    before = list(training_batches(pairs))
    states = milestone_states(recipe); validate_states(recipe, states)
    after = list(training_batches(pairs))
    assert after == before
    assert len(after) == 35283 and sum(map(len, after)) == 141130
    assert all(len(batch) == 4 for batch in after[:-1]) and len(after[-1]) == 2
    flat = [item for batch in after for item in batch]
    assert [int(item["row"]["id"]) for item in flat] == order * 10
    assert [item["presentation"] for item in flat] == list(range(141130))
    assert [item["pass_index"] for item in after[7057 - 1]] == [1, 1, 2, 2]
    assert [item["pass_index"] for item in after[17642 - 1]] == [4, 5, 5, 5]
    assert [item["pass_index"] for item in after[-1]] == [9, 9]


def test_no_extra_observation_or_pass_boundary_flush_is_accepted(recipe):
    states = milestone_states(recipe)
    with pytest.raises(ValueError):
        validate_states(recipe, states + [states[-1]])
    recipe["accounting"]["pass_boundary_flush"] = True
    with pytest.raises(ValueError, match="continuous"):
        milestone_states(recipe)
