from collections import Counter
import pytest
from src.data.g2_byt5 import accounting_plan, training_batches, validate_pairs


@pytest.fixture
def pairs():
    return [dict(id=str(index), role="train", status="COMPLETED", source="a", target="b")
            for index in range(14113)]


def test_all_ten_passes_cross_boundaries_without_extra_short_batches(pairs):
    batches = list(training_batches(pairs))
    assert len(batches) == 35283
    assert len(batches[-1]) == 2 and all(len(batch) == 4 for batch in batches[:-1])
    counts = Counter(item["row"]["id"] for batch in batches for item in batch)
    assert counts == {str(index): 10 for index in range(14113)}
    crossing = batches[14113 // 4]
    assert [item["pass_index"] for item in crossing] == [0, 1, 1, 1]
    assert accounting_plan(pairs)["per_pass_presentations"] == [14113] * 10
    assert [[item["row"]["id"] for item in batch] for batch in batches[:10]] == [
        [item["row"]["id"] for item in batch] for batch in list(training_batches(pairs))[:10]]


@pytest.mark.parametrize("field", ["source", "target"])
def test_any_required_byte_overflow_rejects_the_full_recipe_without_truncation(pairs, field):
    pairs[500][field] = "x" * 512
    with pytest.raises(ValueError, match="do not truncate"):
        validate_pairs(pairs)
    assert len(pairs[500][field]) == 512


def test_no_short_census_or_development_row_is_admitted(pairs):
    with pytest.raises(ValueError, match="every unique"):
        validate_pairs(pairs[:-1])
    pairs[0]["role"] = "calibration"
    with pytest.raises(ValueError, match="non-TRAIN"):
        validate_pairs(pairs)
