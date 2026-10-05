from itertools import product
import pytest

from src.data.empirical_corruption import Edit, alignment_consensus, effect_tag, estimate_profile


def enumerated_oracle(reference, hypothesis):
    """Independent tiny path enumeration; no implementation lattice calls."""
    paths = []

    def visit(i, j, cost, edits):
        if i == len(reference) and j == len(hypothesis):
            paths.append((cost, frozenset(edits)))
            return
        if i < len(reference) and j < len(hypothesis):
            changed = reference[i] != hypothesis[j]
            e = [Edit("substitution", i, j, reference[i], hypothesis[j])] if changed else []
            visit(i + 1, j + 1, cost + int(changed), edits + e)
        if i < len(reference):
            visit(i + 1, j, cost + 1, edits + [Edit("deletion", i, j, reference[i], "")])
        if j < len(hypothesis):
            visit(i, j + 1, cost + 1, edits + [Edit("insertion", i, j, "", hypothesis[j])])

    visit(0, 0, 0, [])
    best = min(c for c, _ in paths)
    optimal = [e for c, e in paths if c == best]
    return best, len(optimal), set.intersection(*(set(e) for e in optimal)), set.union(*(set(e) for e in optimal))


def test_all_optimal_consensus_exhaustively_matches_independent_path_enumeration():
    strings = ["".join(chars) for length in range(4) for chars in product("ab", repeat=length)]
    for reference, hypothesis in product(strings, repeat=2):
        distance, count, common, union = enumerated_oracle(reference, hypothesis)
        actual = alignment_consensus(reference, hypothesis)
        assert actual["distance"] == distance
        assert actual["optimal_paths"] == count
        assert set(actual["consensus"]) == common
        assert actual["possible_edit_edges"] == len(union)
        assert actual["omitted_unit_edit_mass"] == distance - len(common)


def test_raw_codepoints_keep_case_punctuation_whitespace_and_unicode():
    assert alignment_consensus("A", "a")["distance"] == 1
    assert alignment_consensus("x.", "x")["consensus"] == (Edit("deletion", 1, 1, ".", ""),)
    assert alignment_consensus("a a", "aa")["distance"] == 1
    assert alignment_consensus("é", "e\u0301")["distance"] == 2
    assert alignment_consensus("aa", "a")["consensus"] == ()
    with pytest.raises(UnicodeEncodeError):
        alignment_consensus("\ud800", "")


def rows(n=5, groups=3, target="A", source="a"):
    return [{"id": str(i), "source_group_id": str(i % groups), "role": "train",
             "status": "COMPLETED", "target": target, "source": source} for i in range(n)]


@pytest.mark.parametrize("n,groups,supported", [(5, 3, True), (4, 3, False), (5, 2, False)])
def test_entry_requires_both_distinct_record_and_group_support(n, groups, supported):
    profile = estimate_profile(rows(n, groups))
    entry = profile["entries"][0]
    assert entry["supported"] is supported
    assert entry["weight"] == (n if supported else 0)
    assert entry["effect"] == "case"


def test_severity_preserves_zeros_raw_tail_and_joint_support():
    profile = estimate_profile(rows(target="AB", source="ab") + [
        {"id": "zero", "source_group_id": "0", "role": "train", "status": "COMPLETED",
         "target": "same", "source": "same"},
        {"id": "tail", "source_group_id": "0", "role": "train", "status": "COMPLETED",
         "target": "XYZ", "source": "xyz"}])
    assert profile["distance_distribution"] == {0: 1, 2: 5, 3: 1}
    assert profile["severity_P0"] == {0: 1, 1: 6}
    assert profile["severity_P1_P2"] == {0: 1, 1: 0, 2: 6}
    supported = [p for p in profile["cooccurrence"] if p["supported"]]
    assert len(supported) == 1
    assert supported[0]["record_count"] == 5
    assert supported[0]["group_count"] == 3
    assert sum(e["weight"] for e in profile["entries"]) == 10


def test_ambiguous_observations_cannot_supply_entry_support():
    profile = estimate_profile(rows(target="aa", source="a"))
    assert all(e["weight"] == 0 for e in profile["entries"])
    assert sum(e["ambiguous_possible_edges"] for e in profile["entries"]) == 10
    assert profile["consensus_occurrences"] == 0
    assert profile["omitted_unit_edit_mass"] == 5
    assert profile["ambiguous_optimal_edit_edges"] == 10


@pytest.mark.parametrize("role", ["calibration", "hpo_development", "sealed_final", "excluded_overlap"])
def test_nontraining_records_cannot_estimate_profile(role):
    records = rows()
    records[0]["role"] = role
    with pytest.raises(ValueError, match="TRAIN"):
        estimate_profile(records)


def test_duplicate_or_failed_records_are_rejected():
    records = rows()
    with pytest.raises(ValueError, match="reused"):
        estimate_profile(records + records[:1])
    records[0]["status"] = "FAILED"
    with pytest.raises(ValueError, match="completed"):
        estimate_profile(records)


@pytest.mark.parametrize("key,expected", [
    (("substitution", "A", "a"), "case"),
    (("deletion", ".", ""), "punctuation"),
    (("insertion", "", " "), "whitespace_boundary"),
    (("substitution", "a", "b"), "other"),
])
def test_effect_tags_are_descriptive_only(key, expected):
    assert effect_tag(key) == expected
