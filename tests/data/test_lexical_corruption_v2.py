import hashlib
import json
from pathlib import Path

import pytest

from src.data.lexical_corruption_v2 import (
    concentration_alarms, estimate_lexical_profile, phi, serialized,
)


def rows(n=5, groups=3, target="abc", source="abx", prefix="r"):
    return [{"id": f"{prefix}{i}", "source_group_id": str(i % groups),
             "role": "train", "status": "COMPLETED", "target": target, "source": source}
            for i in range(n)]


def test_projection_uses_frozen_lexical_policy_and_safe_serialization():
    assert phi("") == ""
    assert phi(' “HELLO,”  world! ') == "hello world"
    assert phi("Straße e\u0301 can’t co‑operate") == "strasse é can't co-operate"
    assert phi("a  b") == "a b"
    assert phi("can't") != phi("cant")
    assert phi("a b") != phi("ab")


@pytest.mark.parametrize("tokens", [("a b",), ("",)])
def test_separator_safety_is_checked(monkeypatch, tokens):
    monkeypatch.setattr("src.data.lexical_corruption_v2.lexical", lambda _: tokens)
    with pytest.raises(ValueError, match="separator safety"):
        phi("anything")


def test_projected_consensus_collapses_only_scorer_invariant_differences():
    table, audit = estimate_lexical_profile(rows(target="ABC.", source="abc"))
    assert table["lexical_zero_records"] == 5
    assert table["projected_unit_edit_mass"] == 0
    assert table["entries"] == []
    assert table["raw_zero_records"] == 0
    table, audit = estimate_lexical_profile(rows(target="can't", source="cant"))
    assert table["entries"][0]["key"] == ["deletion", "'", ""]
    assert table["entries"][0]["weight"] == 5
    assert audit[0]["consensus_edits"][0]["reference_position"] == 3


@pytest.mark.parametrize("n,groups,supported", [(5, 3, True), (4, 3, False), (5, 2, False)])
def test_both_support_floors_are_required(n, groups, supported):
    table, _ = estimate_lexical_profile(rows(n=n, groups=groups))
    entry = table["entries"][0]
    assert entry["supported"] is supported
    assert entry["weight"] == (n if supported else 0)
    assert entry["source_group_ids"] == sorted({str(i % groups) for i in range(n)})


def test_ambiguity_cannot_supply_literal_support():
    table, audit = estimate_lexical_profile(rows(target="AA", source="a"))
    assert table["projected_unit_edit_mass"] == 5
    assert table["omitted_unit_edit_mass"] == 5
    assert table["consensus_occurrences"] == 0
    assert table["retained_occurrences"] == 0
    assert table["ambiguous_optimal_edit_edges"] == 10
    assert all(not entry["supported"] for entry in table["entries"])
    assert audit[0]["optimal_paths"] == 2


def test_class_pairs_are_record_weighted_not_combination_weighted():
    table, _ = estimate_lexical_profile(rows(target="abc", source="xyz"))
    ss = next(pair for pair in table["class_pairs"] if pair["class_pair"] == "SS")
    assert ss["record_count"] == 5
    assert ss["group_count"] == 3
    assert ss["weight"] == 5
    assert len(table["class_pairs"]) == 6
    assert sum(pair["weight"] for pair in table["class_pairs"]) == 5


def test_two_insertions_at_same_original_gap_do_not_support_pair():
    table, _ = estimate_lexical_profile(rows(target="a", source="abc"))
    assert sum(entry["supported"] for entry in table["entries"]) == 2
    ii = next(pair for pair in table["class_pairs"] if pair["class_pair"] == "II")
    assert ii["record_count"] == 0
    assert ii["weight"] == 0


def test_unsupported_elementary_entries_cannot_support_class_pair():
    table, _ = estimate_lexical_profile(rows(n=4, target="abc", source="xyz"))
    assert all(pair["record_count"] == 0 for pair in table["class_pairs"])


def test_severity_is_conditional_projected_distance_before_support():
    records = rows(n=4, target="ABC.", source="abc", prefix="zero")
    records += rows(n=4, prefix="one")
    records += rows(n=4, target="abc", source="xyz", prefix="tail")
    table, _ = estimate_lexical_profile(records)
    assert table["distance_distribution"] == {"0": 4, "1": 4, "3": 4}
    assert table["severity_denominator"] == 8
    assert table["severity_P0"] == {"0": 0, "1": 8, "2": 0}
    assert table["severity_P1_P2"] == {"0": 0, "1": 4, "2": 4}
    assert table["retained_occurrences"] == 0


def test_leave_one_group_out_requalifies_support_without_realigning(monkeypatch):
    from src.data.empirical_corruption import alignment_consensus
    calls = []
    def counted(reference, hypothesis):
        calls.append((reference, hypothesis))
        return alignment_consensus(reference, hypothesis)
    monkeypatch.setattr("src.data.lexical_corruption_v2.alignment_consensus", counted)
    table, _ = estimate_lexical_profile(rows())
    assert len(calls) == 5
    assert len(table["leave_one_group_out"]) == 3
    assert all(item["retained_occurrences"] == 0 for item in table["leave_one_group_out"])
    assert all(item["severity_P1_P2"]["0"] == 0 for item in table["leave_one_group_out"])


def test_strict_majority_alarms_use_exact_integer_comparisons():
    half = concentration_alarms([(("deletion", "x", ""), 5), (("insertion", "", "a"), 5)])
    assert not half["entry_strict_majority"]
    majority = concentration_alarms([(("deletion", "x", ""), 6), (("insertion", "", "a"), 4)])
    assert majority["entry_strict_majority"]
    assert not majority["separator_strict_majority"]
    boundary = concentration_alarms([(("deletion", " ", ""), 5), (("insertion", "", " "), 5)])
    assert boundary["separator_strict_majority"]
    assert not boundary["entry_strict_majority"]
    mixed = concentration_alarms([(("substitution", " ", "a"), 5), (("deletion", "x", ""), 5)])
    assert not mixed["separator_strict_majority"]
    with pytest.raises(ValueError, match="aggregated"):
        concentration_alarms([(("deletion", "x", ""), 1), (("deletion", "x", ""), 1)])


@pytest.mark.parametrize("role", ["calibration", "hpo_development", "sealed_final", "excluded_overlap"])
def test_nontraining_records_are_rejected(role):
    records = rows()
    records[0]["role"] = role
    with pytest.raises(ValueError, match="TRAIN"):
        estimate_lexical_profile(records)


def test_reused_and_failed_records_are_rejected():
    records = rows()
    with pytest.raises(ValueError, match="reused"):
        estimate_lexical_profile(records + records[:1])
    records[0]["status"] = "FAILED"
    with pytest.raises(ValueError, match="completed"):
        estimate_lexical_profile(records)


def test_table_serialization_is_stable_after_json_roundtrip():
    table, _ = estimate_lexical_profile(rows(target="abcdefghijk", source="xyz"))
    assert serialized(table) == serialized(json.loads(serialized(table)))


def test_old_raw_table_hash_is_preserved():
    root = Path(__file__).resolve().parents[2]
    path = root / "experiments/manifests/frontier_reader/empirical-profile-table.attempt01.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == "5df3800d7a29e370abdce36bd489989482d5d878765612b5a14a4b2cab1fc310"


def test_frozen_train_projection_counts_and_calibration_exclusion():
    from benchmarks.lexical_corruption_profile_v2 import PAIR_PATH, admitted_rows
    if not PAIR_PATH.exists():
        pytest.skip("ignored frozen TRAIN/CALIBRATION pair payload unavailable")
    records = admitted_rows()
    assert len(records) == len({row["id"] for row in records}) == 1024
    assert {row["role"] for row in records} == {"train"}
    assert sum(phi(row["target"]) == phi(row["source"]) for row in records) == 690
