import pytest
from src.scoring.g2_bootstrap import paired_group_intervals


def test_paired_draws_share_groups_and_are_reproducible():
    groups = [f"g{index:02d}" for index in range(52)]
    first = {group: (index + 1, 100) for index, group in enumerate(groups)}
    second = {group: (index + 11, 100) for index, group in enumerate(groups)}
    a = paired_group_intervals(groups, {"B": first, "C": second})
    b = paired_group_intervals(list(reversed(groups)), {"B": first, "C": second})
    assert a == b
    assert a["paired_difference_intervals"]["B minus C"] == pytest.approx([-.1, -.1])
    assert a["eligibility_affected"] is False
    assert a["intervals"]["B"][0] < sum(x[0] for x in first.values()) / 5200 < a["intervals"]["B"][1]


def test_missing_or_zero_denominator_group_is_rejected():
    groups = [str(index) for index in range(52)]
    values = {group: (0, 1) for group in groups}
    with pytest.raises(ValueError, match="complete groups"):
        paired_group_intervals(groups, {"B": values, "C": {group: values[group] for group in groups[:-1]}})
    values["0"] = (0, 0)
    assert paired_group_intervals(groups, {"B": values})["intervals"]["B"] == [0., 0.]
    values = {group: (0, 0) for group in groups}
    with pytest.raises(ValueError, match="positive population denominator"):
        paired_group_intervals(groups, {"B": values})
