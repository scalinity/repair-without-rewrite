from src.data.mixed_reader_v3 import canonical_serialization, native_shape
from src.models.tokenizer import BOS, EOS, RESTORE_REFERENCE, SEP, ByteBPE
from src.data.mixed_reader_v3 import CompletePass, DeficitNode, MixedReader, phase_at
from src.data.mixed_reader_v3 import pilot_lr
from src.generation.stress import CATEGORIES


def test_exact_accounting_and_source_exclusion():
    tokenizer = ByteBPE()
    expected = [257, 308, 259, 97, 259, 97, 258]
    assert canonical_serialization(tokenizer, "a", "a") == expected
    for source in ("a", "x", "longer actual source"):
        shape = native_shape(tokenizer, source, "a", "a")
        assert shape["canonical_sequence"] == expected
        assert shape["canonical_charge"] == 7
        assert shape["source_ids"] == [BOS, RESTORE_REFERENCE, SEP, *tokenizer.encode(source), EOS]
        assert shape["encoder_positions"] == list(range(2, len(source.encode()) + 3))
        assert shape["byte_offsets"] == list(range(len(source.encode()) + 1))


def test_common_native_limits_reject_without_truncation():
    tokenizer = ByteBPE()
    assert native_shape(tokenizer, "x" * 1021, "a", "a") is None
    assert native_shape(tokenizer, "a", "x" * 1021, "a") is None
    assert native_shape(tokenizer, "a", "a", "x" * 1024) is None
    admitted = native_shape(tokenizer, "a", "x" * 1020, "a")
    assert admitted["anchor_bpe"] == 1020
    assert admitted["canonical_charge"] == 1026


def test_utf8_native_boundaries_preserve_legal_pointer_mask():
    tokenizer = ByteBPE()
    shape = native_shape(tokenizer, "éa", "a", "a")
    assert shape["byte_offsets"] == [0, 1, 2, 3]
    assert shape["legal"] == [True, False, True, True]
    assert shape["encoder_positions"] == [2, 3, 4, 5]


def small_reader():
    generated = [{"variant_id": f"{category}/{cell}/{view}/{index}", "category": category,
        "cell": cell, "view": view, "canonical_charge": 13 + index * 7 + cell * 11}
        for category in CATEGORIES for cell in range(4)
        for view in ("clean", "mixed", "two", "empirical1", "empirical2") for index in range(3)]
    natural = [{"variant_id": f"record/{index}", "source_group_id": str(index // 3),
        "canonical_charge": 7 + index * 3} for index in range(12)]
    return MixedReader(generated, natural, natural, {1: 103, 2: 231})


def test_coverage_first_complete_pass_balances_records_before_reuse():
    rows = [{"variant_id": str(index), "source_group_id": str(index // 3)} for index in range(12)]
    pool = CompletePass(rows, "natural", coverage_first=True)
    first = [pool.next() for _ in range(12)]
    assert len({row["source_group_id"] for row in first[:4]}) == 4
    assert len({row["variant_id"] for row in first}) == 12
    for _ in range(53):
        pool.next()
        assert max(pool.uses.values()) - min(pool.uses.values()) <= 1


def test_exact_deficit_tie_order_and_whole_charge_bounds():
    pools = [CompletePass([{"variant_id": str(index), "canonical_charge": 7 + index * 17}], str(index))
             for index in range(4)]
    node = DeficitNode([(str(index), weight, pools[index]) for index, weight in enumerate((3, 2, 1, 4))])
    assert node.next()[1] == ["0"]
    for _ in range(500):
        node.next()
        for index, weight in enumerate((.3, .2, .1, .4)):
            deviation = node.charges[str(index)] - weight * node.total
            assert -(2 + weight) * 58 - 1e-9 <= deviation <= (1 - weight) * 58 + 1e-9


def test_reader_order_phase_reset_and_persistent_leaf_cursor():
    one, two = small_reader(), small_reader()
    assert [one.next() for _ in range(1000)] == [two.next() for _ in range(1000)]
    pool = one.pools["identity/natural"]
    cursor = (pool.pass_number, pool.offset, sum(pool.uses.values()))
    one.exposure = 6_666_667
    first = one.next()
    assert first["phase"] == "P1"
    assert first["channel"] == "identity_minimal"
    assert one.root.total == first["canonical_charge"]
    assert one.pools["identity/natural"] is pool
    assert sum(pool.uses.values()) == cursor[2] + 1
    one.exposure = 9_333_334
    later = [one.next() for _ in range(2000)]
    assert {row["phase"] for row in later} == {"P2"}
    assert any("fresh" in row["subpath"] for row in later)
    assert phase_at(6_666_666) == "P0"
    assert phase_at(9_333_333) == "P1"
    assert phase_at(10_000_001) == "P2"


def test_complete_update_queue_uses_exact_32768_target():
    reader = small_reader()
    queue = reader.queue()
    charges = [row["canonical_charge"] for row in queue]
    assert sum(charges) >= 32_768
    assert sum(charges[:-1]) < 32_768
    assert queue[-1]["end_exposure"] == reader.exposure
    assert [row["ordinal"] for row in queue] == list(range(len(queue)))


def test_pilot_lr_continuous_exposure_clock_and_fixed_grid():
    import pytest
    for peak in (1e-4, 3e-4, 6e-4):
        assert pilot_lr(0, peak) == 0
        assert pilot_lr(100_000, peak) == peak / 2
        assert pilot_lr(200_000, peak) == peak
        assert pilot_lr(10_000_000, peak) == pytest.approx(.1 * peak)
        assert pilot_lr(10_010_000, peak) == pilot_lr(10_000_000, peak)
        for boundary in (6_666_667, 9_333_334):
            assert pilot_lr(boundary - 1, peak) > pilot_lr(boundary, peak) > pilot_lr(boundary + 1, peak)
    with pytest.raises(ValueError):
        pilot_lr(100, .0002)


def test_cold_reader_restore_preserves_next_twenty_complete_queues():
    import json
    import pytest
    for exposure in (0, 6_666_660, 9_333_325):
        control = small_reader()
        control.exposure = exposure
        control.queue()
        saved = json.loads(json.dumps(control.state()))
        resumed = small_reader()
        resumed.restore(saved)
        assert resumed.state() == control.state()
        for _ in range(20):
            assert resumed.queue() == control.queue()
            assert resumed.state() == control.state()
        broken = json.loads(json.dumps(saved))
        broken["deficits"]["total"] += 1
        with pytest.raises(ValueError):
            small_reader().restore(broken)
