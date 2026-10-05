"""Independent brute-force and adverse-fixture checks for the full supply audit."""
from collections import defaultdict
from decimal import Decimal
import json
from pathlib import Path
import random

import pytest

from src.data.training_supply import (
    independent_parent_graph, lexical_count, near_pairs, qualify,
)
from src.scoring.text import lexical


def source(identity, split, text, raw=None, parent=None, parent_status=None):
    return dict(id=identity, official_split=split, text=text,
                text_raw=text if raw is None else raw, manifest_duration_seconds="1.25",
                families=dict(speaker=identity, chapter=identity, book=identity,
                              project=identity, metadata_component=parent or identity),
                parent_status=parent_status or "potential_supply_pending_full_text_and_audio_qualification")


def test_lossless_prefix_join_matches_independent_all_pairs_including_repetition():
    rng = random.Random(120101)
    values = [frozenset(rng.sample(range(120), rng.randrange(1, 45))) for _ in range(120)]
    # Heavy-overlap families, cardinality-edge cases, identical sets and empty set.
    for i in range(15):
        base = set(range(i, i + 70))
        values += [frozenset(base), frozenset(base | {1000 + i}),
                   frozenset(base - {i, i + 1}), frozenset(base)]
    values += [frozenset(), frozenset(range(9)), frozenset(range(10)),
               frozenset(range(19)), frozenset(range(21))]
    expected = {}
    for i, a in enumerate(values):
        for j in range(i + 1, len(values)):
            b = values[j]
            if a and b:
                numerator, denominator = len(a & b), len(a | b)
                if 10 * numerator >= 9 * denominator:
                    expected[(i, j)] = (numerator, denominator)
    actual, stats = near_pairs(values)
    actual = {tuple(sorted((a, b))): (n, d) for a, b, n, d in actual}
    assert actual == expected
    assert stats["qualifying_variant_pairs"] == len(expected)


def test_long_raw_variant_connects_entire_training_parent_to_final():
    overlap = " ".join("word" + str(i) for i in range(45))
    unrelated = " ".join("different" + str(i) for i in range(45))
    rows = [source("a", "train-clean-100", unrelated, raw=overlap, parent="train-family"),
            source("b", "train-clean-100", "unrelated brief target", parent="train-family"),
            source("c", "test-clean", overlap + " tail")]
    summary, manifest, full = qualify(rows)
    assert not manifest
    assert {r["id"]: r["role"] for r in full} == {
        "a": "excluded_overlap", "b": "excluded_overlap", "c": "sealed_final"}
    assert len({r["source_group_id"] for r in full}) == 1
    assert summary["near_cross_row_edges"] == 1
    assert summary["new_training_exclusions_after_text_closure"] == {
        "known_final_parent_or_long_reference_overlap": 2}


def test_short_exact_final_target_is_row_veto_without_invented_family_merge():
    rows = [source("a", "train-clean-100", "hello", parent="training"),
            source("b", "train-clean-100", "independent", parent="training"),
            source("c", "test-clean", "HELLO", raw="hello"),
            source("d", "dev-clean", "hello")]
    summary, manifest, full = qualify(rows, calibration_fraction=Decimal(0))
    assert {r["id"]: r["role"] for r in full} == {
        "a": "excluded_overlap", "b": "train", "c": "sealed_final", "d": "excluded_overlap"}
    assert manifest[0]["id"] == "b" and len(manifest) == 1
    by_id = {r["id"]: r for r in full}
    assert by_id["a"]["source_group_id"] == by_id["b"]["source_group_id"]
    assert by_id["a"]["source_group_id"] != by_id["c"]["source_group_id"]
    assert summary["exact_final_target_veto_by_split"] == {"dev-clean": 1, "train-clean-100": 1}
    assert summary["long_exact_cross_row_edges"] == 0


def test_short_normalized_match_remains_diagnostic_not_known_final_literal():
    summary, manifest, full = qualify([source("a", "train-clean-100", "Hello!"),
                                      source("b", "test-clean", "HELLO?")],
                                     calibration_fraction=Decimal(0))
    assert manifest[0]["role"] == "train"
    assert len(summary["short_signature_cross_role_collisions"]) == 1
    assert not summary["literal_final_reference_cross_role_collisions"]


def test_whole_group_calibration_and_development_precedence_are_order_independent():
    rows = [source("a", "train-clean-100", "alpha", parent="same"),
            source("b", "train-clean-100", "beta", parent="same"),
            source("c", "dev-clean", "gamma", parent="development"),
            source("d", "train-clean-100", "delta", parent="development")]
    a = qualify(rows)
    b = qualify(list(reversed(rows)))
    assert a == b
    full = {r["id"]: r for r in a[2]}
    assert full["a"]["role"] == full["b"]["role"]
    assert full["c"]["role"] == "hpo_development"
    assert full["d"]["role"] == "excluded_overlap"


def test_bfs_parent_graph_keeps_omitted_chapter_bridge_and_prior_precedence(tmp_path):
    path = tmp_path / "CHAPTERS.TXT"
    path.write_text("1 | 7 | 1 | dev-clean | 10 | 100 | a | b\n"
                    "2 | 7 | 1 | train-clean-100 | 20 | 200 | a | b\n"
                    "3 | 8 | 1 | test-clean | 20 | 200 | a | b\n")
    mapping, summary = independent_parent_graph(path)
    assert summary["known_parent_components"] == 1
    assert {r["parent_status"] for r in mapping.values()} == {"known_final_parent_overlap"}
    assert len({r["metadata_component"] for r in mapping.values()}) == 1
    rows = [source("a", "train-clean-100", "brief", parent="known",
                   parent_status="known_final_parent_overlap")]
    assert qualify(rows)[2][0]["role"] == "excluded_overlap"


@pytest.mark.parametrize("text", ["", "Hello, world!", "don't re-run 3.12 5%", "Straße café é",
    "x_y /tmp/a \u2018hi\u2019 \u2011 \u0301", "路径🙂 ١٢–34 +2\u200btest", "a\u0345\u0300b"])
def test_fast_volume_count_matches_independent_provenance_scanner(text):
    assert lexical_count(text) == len(lexical(text))


def test_candidate_content_and_duplicate_source_ids_block_audit():
    row = source("a", "train-clean-100", "text")
    with pytest.raises(ValueError, match="candidate"):
        qualify([dict(row, output="candidate")])
    with pytest.raises(ValueError, match="duplicate"):
        qualify([row, row])


def test_committed_role_artifact_has_no_payload_and_role_family_separation():
    root = Path(__file__).resolve().parents[2]
    path = root / "experiments/manifests/public_lspc_training_roles.development.jsonl"
    if not path.exists():
        pytest.skip("full candidate-blind supply audit has not been run")
    families = defaultdict(set)
    counts = defaultdict(int)
    forbidden = {"text", "text_raw", "reference", "audio", "hypothesis", "output"}
    with path.open() as stream:
        for line in stream:
            row = json.loads(line)
            assert forbidden.isdisjoint(row)
            assert row["role"] in {"train", "calibration", "hpo_development"}
            families[row["role"]].add(row["source_group_id"])
            counts[row["role"]] += 1
    assert families["train"].isdisjoint(families["calibration"] | families["hpo_development"])
    assert families["calibration"].isdisjoint(families["hpo_development"])
    summary = json.loads((path.parent / "public_lspc_training_supply_qualification.json").read_text())
    assert {k: v["rows"] for k, v in summary["roles"].items() if k in counts} == counts
    assert summary["official_training_rows"] == 256124
    assert summary["prior_parent_bounds_independently_reproduced"] == {
        "known_final_parent_overlap": 202414, "known_development_parent_overlap": 1228,
        "potential_supply_pending_full_text_and_audio_qualification": 52482}


def test_actual_all_shingle_cross_role_check_independent_of_prefix_join():
    """Optional local source integration, using a different exhaustive candidate index."""
    import hashlib
    import re
    import tarfile
    import unicodedata2

    root = Path(__file__).resolve().parents[2]
    archive = root / "exports/source-qualification/ls_pc_manifest.tar.gz"
    manifest = root / "experiments/manifests/public_lspc_training_roles.development.jsonl"
    if not archive.exists() or not manifest.exists():
        pytest.skip("official payload intentionally external to Git")
    roles = {r["id"]: r for r in map(json.loads, manifest.read_text().splitlines())}
    actual, final = {}, set()
    with tarfile.open(archive, "r:gz") as tar:
        for member in tar.getmembers():
            if not member.name.endswith(".json"):
                continue
            for line in tar.extractfile(member):
                source = json.loads(line)
                identity = Path(source["audio_filepath"]).stem
                if identity in roles:
                    actual[identity] = (source, roles[identity]["role"])
                    for field in ("text", "text_raw"):
                        assert hashlib.sha256(source[field].encode()).hexdigest() == roles[identity][field + "_sha256"]
                elif member.name in {"test-clean.json", "test-other.json"}:
                    actual[identity] = (source, "sealed_final")
                    final.update((source["text"], source["text_raw"]))
    assert len(actual) == len(roles) + 5273
    signatures = {}
    for identity, (source, role) in sorted(actual.items()):
        for field in ("text", "text_raw"):
            if role != "sealed_final":
                assert source[field] not in final
            tokens = tuple(re.findall(r"\w+", unicodedata2.normalize("NFC", source[field]).casefold()))
            if len(tokens) < 20:
                continue
            if tokens in signatures:
                assert signatures[tokens]["role"] == role
            else:
                signatures[tokens] = {"id": identity, "role": role,
                    "shingles": frozenset(tokens[i:i + 5] for i in range(len(tokens) - 4))}
    items = list(signatures.values())
    index = defaultdict(list)
    for i, row in enumerate(items):
        if row["role"] != "train":
            for shingle in row["shingles"]:
                index[shingle].append(i)
    for row in items:
        if row["role"] == "sealed_final":
            continue
        candidates = set()
        for shingle in row["shingles"]:
            candidates.update(index.get(shingle, ()))
        for j in candidates:
            other = items[j]
            if row["role"] == other["role"]:
                continue
            a, b = row["shingles"], other["shingles"]
            if 10 * min(len(a), len(b)) < 9 * max(len(a), len(b)):
                continue
            assert 10 * len(a & b) < 9 * len(a | b), (row["id"], other["id"])
