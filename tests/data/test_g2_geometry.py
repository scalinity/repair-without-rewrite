import itertools
import pytest

from src.data.g2_geometry import actual_denominators, g2_lr, split_master


def queue(charges):
    return [{"canonical_charge": value, "ordinal": index} for index, value in enumerate(charges)]


def test_first_crossing_cuts_are_whole_and_preserve_order():
    master = queue([2, 5, 3, 1, 6, 2, 4, 3, 2, 5, 4, 3, 2, 4, 2, 2])
    actual = split_master(master, "U8")
    assert len(actual) == 8 and all(actual)
    assert list(itertools.chain.from_iterable(actual)) == master
    total = sum(row["canonical_charge"] for row in master)
    for j, subqueues in enumerate((actual[:j] for j in range(1, 8)), 1):
        consumed = list(itertools.chain.from_iterable(subqueues))
        charge = sum(row["canonical_charge"] for row in consumed)
        assert 8 * charge >= j * total
        assert 8 * (charge - consumed[-1]["canonical_charge"]) < j * total


@pytest.mark.parametrize("charges", [[], [0] * 8, [1] * 7, [100, 1, 1, 1, 1, 1, 1, 1]])
def test_unrepresentable_u8_is_rejected_without_splitting_a_presentation(charges):
    with pytest.raises(ValueError):
        split_master(queue(charges), "U8")


def test_u1_retains_the_master_boundary():
    master = queue([4, 9])
    assert split_master(master, "U1") == [master]


def test_denominators_are_subqueue_local_including_b_eos():
    master = [{"canonical_charge": 1, "row": {"target_ids": list(range(index + 1)),
                "C_denominators": dict(action=index + 2, start=index, end=index,
                                       vocabulary=2 * index)}} for index in range(8)]
    updates = split_master(master, "U8")
    assert [actual_denominators(x)["B"] for x in updates] == list(range(2, 10))
    assert [actual_denominators(x)["C"]["vocabulary"] for x in updates] == list(range(0, 16, 2))
    assert sum(actual_denominators(x)["B"] for x in updates) == actual_denominators(master)["B"]


def test_lr_tracks_completed_exposure_without_a_phase_or_subqueue_reset():
    assert g2_lr(200000) == 3e-4
    assert g2_lr(10000000) == pytest.approx(3e-5)
    assert g2_lr(6666668) < g2_lr(6666667)
    assert g2_lr(9333335) < g2_lr(9333334)
    assert g2_lr(4000) == pytest.approx(6e-6)
