import copy
from src.data.g2_stream import G2BenchStream, G2ScientificStream
import pytest


def stream(condition="U8"):
    rows, ledger, updates = {}, [], []
    for phase_index, phase in enumerate(("P0", "P1", "P2")):
        start = len(ledger)
        for index in range(16):
            ordinal = len(ledger)
            variant = f"v{ordinal}"
            rows[variant] = {"target_ids": [1], "C_denominators": dict(action=1, start=0, end=0, vocabulary=0)}
            ledger.append(dict(presentation_id=f"p{ordinal}", ordinal=ordinal, phase=phase,
                channel="natural", subpath=["natural"], start_exposure=ordinal * 2048,
                end_exposure=(ordinal + 1) * 2048, variant_id=variant, canonical_charge=2048))
        updates.append(dict(first_ordinal=start, last_ordinal=len(ledger) - 1,
            canonical_charge=32768, phase_segments={phase: 32768}))
    return G2BenchStream(rows, ledger, updates, "D0", condition)


def test_u8_mid_master_resume_preserves_next_whole_presentations_and_actual_clock():
    original = stream()
    for _ in range(3):
        assert len(original.actual_queue()) == 2
        original.finish_actual()
    assert original.completed_actual_clock() == (3, 12288)
    state = original.state()
    replay = stream(); replay.restore(state)
    assert replay.state() == state
    for _ in range(30):
        a, b = original.actual_queue(), replay.actual_queue()
        assert a == b
        original.finish_actual(); replay.finish_actual()
        assert original.completed_actual_clock() == replay.completed_actual_clock()
        assert original.state() == replay.state()


def test_u1_u8_select_identical_masters_and_cover_all_populations():
    u1, u8 = stream("U1"), stream("U8")
    seen = set()
    for _ in range(25):
        master = u1.actual_queue()
        parts = []
        for _ in range(8):
            parts.extend(u8.actual_queue()); u8.finish_actual()
        assert parts == master
        seen.update(row["phase"] for row in master)
        u1.finish_actual()
        assert u1.completed_actual_clock()[1] == u8.completed_actual_clock()[1]
    assert seen == {"P0", "P1", "P2"}
    assert u8.completed_actual_clock()[0] == 8 * u1.completed_actual_clock()[0]


@pytest.mark.parametrize("field,value", [("subqueue_index", 8), ("subqueue_index", 1.0),
    ("master_committed_exposure", 12), ("selector_exposure", 1), ("master_queue_index", -1)])
def test_corrupt_resume_geometry_and_clocks_are_rejected(field, value):
    original = stream(); original.actual_queue()
    state = copy.deepcopy(original.state()); state[field] = value
    with pytest.raises(ValueError):
        stream().restore(state)


def test_scientific_cursor_consumes_each_frozen_master_once_and_rejects_bench_initializers():
    base = stream()
    u1 = G2ScientificStream(base.rows, base.ledger, base.updates, "D0", "U1")
    u8 = G2ScientificStream(base.rows, base.ledger, base.updates, "D0", "U8")
    seen = []
    for master in range(3):
        whole = u1.actual_queue(); parts = []
        for sub in range(8):
            queue = u8.actual_queue()
            replay = G2ScientificStream(base.rows, base.ledger, base.updates, "D0", "U8")
            replay.restore(u8.state())
            assert replay.actual_queue() == queue
            assert replay.completed_actual_clock() == u8.completed_actual_clock()
            parts.extend(queue); u8.finish_actual()
        assert parts == whole and u1.master_queue_index == master
        seen.extend(item["ordinal"] for item in parts); u1.finish_actual()
    assert seen == list(range(48))
    assert u1.completed_actual_clock() == (3, 98304)
    assert u8.completed_actual_clock() == (24, 98304)
    with pytest.raises(StopIteration): u8.actual_queue()
    with pytest.raises(ValueError, match="BENCH"):
        u8.restore(base.state())
    with pytest.raises(ValueError, match="scope"):
        base.restore(u8.state())


def test_scientific_cursor_rejects_a_skipped_frozen_master():
    base = stream()
    scientific = G2ScientificStream(base.rows, base.ledger, base.updates, "D0", "U8")
    scientific.actual_queue(); state = scientific.state()
    state["master_completed"] = 1
    with pytest.raises(ValueError, match="exposure"):
        scientific.restore(state)
