"""Candidate-blind full LS-PC text supply; no ASR or training is performed here.

The long-reference policy is the previously declared development policy. A lossless
prefix index accelerates its exact set-Jaccard test; it does not approximate it.
Both released reference variants participate before whole-source role assignment.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from decimal import Decimal
import json
from pathlib import Path, PurePosixPath
import platform
import tarfile
import time

from src.data.contracts import (
    DEV_SPLITS, FINAL_SPLITS, NEAR_DUPLICATE_RULE, SPLIT_RULE, canonical_hash,
    fingerprint_tokens, reference_status, sha256_bytes,
)
from src.scoring.text import FOLD, WHITE, POLICY_HASH, ud

TRAIN_SPLITS = {"train-clean-100", "train-clean-360", "train-other-500"}
RELEASE_SPLITS = TRAIN_SPLITS | {"dev-clean", "dev-other", "test-clean", "test-other"}


class Components:
    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, i: int) -> int:
        while self.parent[i] != i:
            self.parent[i] = self.parent[self.parent[i]]
            i = self.parent[i]
        return i

    def join(self, a: int, b: int) -> bool:
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        self.parent[max(a, b)] = min(a, b)
        return True


def independent_parent_graph(metadata: Path) -> tuple[dict, dict]:
    """Bipartite BFS reconstruction, independently of public_inventory's union-find."""
    data = metadata.read_bytes()
    chapters = {}
    adjacency = defaultdict(set)
    for line in data.decode("utf-8", "strict").splitlines():
        if not line.strip() or line.lstrip().startswith(";"):
            continue
        fields = [x.strip() for x in line.split("|", 7)]
        if len(fields) != 8 or any(not fields[i].isascii() or
                                  not fields[i].isdecimal() or int(fields[i]) < 1
                                  for i in (0, 1, 4, 5)):
            raise ValueError("malformed official chapter identity")
        chapter, speaker, _, split, project, book, _, _ = fields
        if chapter in chapters or split not in RELEASE_SPLITS:
            raise ValueError("duplicate chapter or unknown official split")
        chapters[chapter] = dict(chapter=chapter, speaker=speaker, project=project,
                                 book=book, split=split)
        node = ("chapter", chapter)
        for kind, value in (("speaker", speaker), ("project", project), ("book", book)):
            other = (kind, value)
            adjacency[node].add(other)
            adjacency[other].add(node)
    visited = set()
    groups = []
    for chapter in sorted(chapters):
        node = ("chapter", chapter)
        if node in visited:
            continue
        queue, group = deque([node]), []
        visited.add(node)
        while queue:
            here = queue.popleft()
            if here[0] == "chapter":
                group.append(here[1])
            for other in sorted(adjacency[here]):
                if other not in visited:
                    visited.add(other)
                    queue.append(other)
        group.sort()
        identity = canonical_hash(["official_chapter_parent_closure_v1", group])
        splits = {chapters[c]["split"] for c in group}
        category = ("known_final_parent_overlap" if splits & FINAL_SPLITS else
                    "known_development_parent_overlap" if splits & DEV_SPLITS else
                    "potential_supply_pending_full_text_and_audio_qualification")
        for c in group:
            chapters[c].update(metadata_component=identity, parent_status=category)
        groups.append(group)
    return chapters, {"sha256": sha256_bytes(data), "chapters": len(chapters),
                      "known_parent_components": len(groups),
                      "algorithm": "independent_bipartite_BFS_all_official_chapters"}


def lexical_count(text: str) -> int:
    """Same pinned lexical_eval_v1 scanner, without unnecessary raw-offset tracing."""
    value = ud.normalize("NFC", "".join(FOLD.get(c, c) for c in ud.normalize("NFC", text)))
    value = value.translate(str.maketrans({"\u2018": "'", "\u2019": "'", "\u2010": "-", "\u2011": "-"}))
    def word(c):
        return ud.category(c)[0] in "LMN"
    total, i = 0, 0
    while i < len(value):
        c = value[i]
        if word(c):
            total += 1
            i += 1
            while i < len(value) and (word(value[i]) or
                    (value[i] in "'-" and i + 1 < len(value) and
                     word(value[i - 1]) and word(value[i + 1]))):
                i += 1
        else:
            total += not (c in WHITE or (ud.category(c)[0] == "P" and c not in "-%"))
            i += 1
    return total


def near_pairs(sets: list[frozenset[int]]) -> tuple[list[tuple[int, int, int, int]], dict]:
    """All Jaccard >= 9/10 pairs, exact integer arithmetic and lossless filtering.

    A qualifying pair overlaps in >= ceil(.9*n) elements of each set. Its first
    shared element under one common order must occur in both n-ceil(.9*n)+1
    prefixes, or too few remaining elements could meet that bound. Cardinality
    filtering follows |smaller|/|larger| >= .9. No MinHash or sampling is used.
    """
    frequencies = Counter(element for values in sets for element in values)
    order = {element: rank for rank, element in enumerate(
        sorted(frequencies, key=lambda x: (frequencies[x], x)))}
    postings = defaultdict(list)
    pairs, comparisons, witnesses = [], 0, 0
    for i in sorted(range(len(sets)), key=lambda j: (len(sets[j]), j)):
        values = sets[i]
        n = len(values)
        if not n:
            continue
        prefix_size = n - (9 * n + 9) // 10 + 1
        prefix = sorted(values, key=order.__getitem__)[:prefix_size]
        candidates = set()
        for value in prefix:
            for j in postings[value]:
                if 10 * len(sets[j]) >= 9 * n:
                    candidates.add(j)
        witnesses += len(candidates)
        for j in sorted(candidates):
            comparisons += 1
            intersection = len(values & sets[j])
            union = n + len(sets[j]) - intersection
            if 10 * intersection >= 9 * union:
                pairs.append((j, i, intersection, union))
        for value in prefix:
            postings[value].append(i)
    return pairs, {"unique_long_signatures": len(sets),
                   "distinct_five_word_shingles": len(frequencies),
                   "exact_Jaccard_comparisons": comparisons,
                   "candidate_witnesses": witnesses,
                   "qualifying_variant_pairs": len(pairs),
                   "algorithm": "lossless_common_order_prefix_join_v1_integer_9_over_10"}


def load_release(archive: Path, chapters: dict) -> tuple[list[dict], dict]:
    rows, members, seen = [], {}, set()
    with tarfile.open(archive, "r:gz") as tar:
        for member in sorted(tar.getmembers(), key=lambda x: x.name):
            if not member.name.endswith(".json") or "/" in member.name:
                continue
            split = member.name.removesuffix(".json")
            if split not in RELEASE_SPLITS:
                raise ValueError("unknown official release split")
            payload = tar.extractfile(member).read()
            members[split] = sha256_bytes(payload)
            for line in payload.splitlines():
                if not line:
                    continue
                source = json.loads(line)
                if any(k in source for k in ("output", "candidate", "model_output", "scores")):
                    raise ValueError("candidate data forbidden")
                path = PurePosixPath(source["audio_filepath"])
                if len(path.parts) < 4 or path.parts[-4] != split or path.suffix != ".flac":
                    raise ValueError("malformed released audio path")
                speaker, chapter, stable_id = path.parts[-3], path.parts[-2], path.stem
                if stable_id in seen or not stable_id.startswith(speaker + "-" + chapter + "-"):
                    raise ValueError("duplicate or mismatched stable ID")
                seen.add(stable_id)
                metadata = chapters.get(chapter)
                if metadata is None or metadata["speaker"] != speaker or metadata["split"] != split:
                    raise ValueError("chapter reader/split mismatch or missing mapping")
                for field in ("text", "text_raw"):
                    if not reference_status({"reference": source.get(field),
                            "legitimate_empty_reference": source.get("legitimate_empty_reference") is True}).valid:
                        raise ValueError("invalid released " + field)
                seconds = Decimal(str(source["duration"]))
                if not seconds.is_finite() or seconds <= 0:
                    raise ValueError("invalid manifest duration")
                rows.append({"id": stable_id, "official_split": split,
                             "families": {k: metadata[k] for k in
                                ("speaker", "chapter", "book", "project", "metadata_component")},
                             "parent_status": metadata["parent_status"],
                             "text": source["text"], "text_raw": source["text_raw"],
                             "manifest_duration_seconds": str(seconds)})
    return sorted(rows, key=lambda r: r["id"]), members


def qualify(rows: list[dict], *, partition_seed: int = 120101,
            calibration_fraction: Decimal = Decimal("0.1")) -> tuple[dict, list[dict], list[dict]]:
    """Close full long-text overlaps, then assign candidate-blind whole-group roles."""
    if not Decimal(0) <= calibration_fraction < Decimal(1):
        raise ValueError("invalid calibration fraction")
    rows = sorted(rows, key=lambda r: r["id"])
    if len({r["id"] for r in rows}) != len(rows):
        raise ValueError("duplicate stable source ID")
    graph, parent_first = Components(len(rows)), {}
    final_literal_hashes = {sha256_bytes(row[field].encode()) for row in rows
                            if row["official_split"] in FINAL_SPLITS
                            for field in ("text", "text_raw")}
    for i, row in enumerate(rows):
        if any(k in row for k in ("output", "candidate", "model_output", "scores")):
            raise ValueError("candidate data forbidden")
        key = row["families"]["metadata_component"]
        graph.join(i, parent_first.setdefault(key, i))
    long_first, short_occurrences, literal_occurrences = {}, defaultdict(list), defaultdict(list)
    word_ids, shingle_ids, sets, owners, exact_edges = {}, {}, [], [], []
    variants, long_occurrences, field_differences = Counter(), 0, 0
    for i, row in enumerate(rows):
        field_differences += row["text"] != row["text_raw"]
        for field in ("text", "text_raw"):
            text = row[field]
            tokens = fingerprint_tokens(text)
            signature = canonical_hash(tokens)
            row[field + "_sha256"] = sha256_bytes(text.encode())
            row[field + "_signature_sha256"] = signature
            row[field + "_bytes"] = len(text.encode())
            row[field + "_lexical_tokens"] = lexical_count(text)
            row[field + "_leakage_words"] = len(tokens)
            literal_occurrences[row[field + "_sha256"]].append((i, field))
            if len(tokens) < 20:
                short_occurrences[signature].append((i, field))
                continue
            long_occurrences += 1
            if signature in long_first:
                j, other_field, variant = long_first[signature]
                if i != j:
                    exact_edges.append({"left": rows[j]["id"], "right": row["id"],
                                        "fields": [other_field, field], "signature_sha256": signature})
                    graph.join(i, j)
                variants[variant] += 1
                continue
            encoded = tuple(word_ids.setdefault(word, len(word_ids)) for word in tokens)
            values = frozenset(shingle_ids.setdefault(encoded[j:j + 5], len(shingle_ids))
                               for j in range(len(encoded) - 4))
            variant = len(sets)
            sets.append(values)
            owners.append((i, field))
            long_first[signature] = (i, field, variant)
            variants[variant] += 1
    del word_ids, shingle_ids
    pairs, sweep = near_pairs(sets)
    near_edges, novel_connections = [], 0
    for a, b, numerator, denominator in pairs:
        i, left_field = owners[a]
        j, right_field = owners[b]
        if i == j:
            continue
        novel_connections += graph.join(i, j)
        near_edges.append({"left": rows[i]["id"], "right": rows[j]["id"],
                           "fields": [left_field, right_field],
                           "intersection": numerator, "union": denominator})
    groups = defaultdict(list)
    for i in range(len(rows)):
        groups[graph.find(i)].append(i)
    component_receipts, manifest, full_roles = [], [], []
    for indices in groups.values():
        identity = canonical_hash([("LibriSpeech-PC", rows[i]["id"]) for i in indices])
        splits = {rows[i]["official_split"] for i in indices}
        parent_groups = sorted({rows[i]["families"]["metadata_component"] for i in indices})
        # Metadata chapters absent from restored text still affect role precedence.
        parent_statuses = {rows[i]["parent_status"] for i in indices}
        has_final = bool(splits & FINAL_SPLITS) or "known_final_parent_overlap" in parent_statuses
        has_dev = bool(splits & DEV_SPLITS) or "known_development_parent_overlap" in parent_statuses
        draw = int(canonical_hash([SPLIT_RULE, partition_seed, identity]), 16)
        numerator, denominator = calibration_fraction.as_integer_ratio()
        reserved = draw * denominator < numerator * 2**256
        role_counts = Counter()
        for i in indices:
            row = rows[i]
            split = row["official_split"]
            if split in FINAL_SPLITS:
                role, reason = "sealed_final", None
            elif has_final:
                role, reason = "excluded_overlap", "known_final_parent_or_long_reference_overlap"
            elif any(row[field + "_sha256"] in final_literal_hashes for field in ("text", "text_raw")):
                role, reason = "excluded_overlap", "exact_final_target_literal_any_length_row_veto_v1"
            elif split in DEV_SPLITS:
                role, reason = "hpo_development", None
            elif has_dev:
                role, reason = "excluded_overlap", "known_development_parent_or_long_reference_overlap"
            else:
                role, reason = ("calibration" if reserved else "train"), None
            row.update(role=role, source_group_id=identity, exclusion_reason=reason)
            record = {k: row[k] for k in ("id", "official_split", "role", "source_group_id", "families",
                "exclusion_reason", "manifest_duration_seconds", "text_sha256", "text_raw_sha256",
                "text_bytes", "text_raw_bytes", "text_lexical_tokens", "text_raw_lexical_tokens")}
            record.update(reference_field="text_raw", reference_policy="DEVELOPMENT_TEXT_RAW_RELEASE_SURFACE_NOT_PROTOCOL_FREEZE",
                          audio_qualification="NOT_QUALIFIED")
            full_roles.append(record)
            if role in {"train", "calibration", "hpo_development"}:
                manifest.append(record)
            role_counts[role] += 1
        component_receipts.append({"source_group_id": identity, "parent_components": parent_groups,
                                   "rows": len(indices), "roles": dict(sorted(role_counts.items())),
                                   "has_final": has_final, "has_development": has_dev})
    short_collisions = []
    for signature, occurrences in sorted(short_occurrences.items()):
        indices = sorted({i for i, _ in occurrences})
        if len(indices) < 2:
            continue
        role_set = {rows[i]["role"] for i in indices}
        if len(role_set) > 1:
            short_collisions.append({"signature_sha256": signature,
                "ids": [rows[i]["id"] for i in indices], "roles": sorted(role_set),
                "reason": "below_declared_20_word_source_identity_threshold"})
    literal_final_collisions = []
    for signature, occurrences in sorted(literal_occurrences.items()):
        indices = sorted({i for i, _ in occurrences})
        finals = [rows[i]["id"] for i in indices if rows[i]["role"] == "sealed_final"]
        vetoed = [rows[i]["id"] for i in indices if rows[i]["exclusion_reason"] ==
                  "exact_final_target_literal_any_length_row_veto_v1"]
        if finals and vetoed:
            literal_final_collisions.append({"literal_sha256": signature, "final_ids": finals,
                                            "vetoed_nonfinal_ids": vetoed})
    totals = {}
    for role in sorted({r["role"] for r in rows}):
        selected = [r for r in rows if r["role"] == role]
        distinct_targets = {r["text_raw_sha256"]: r for r in selected}
        totals[role] = {"rows": len(selected), "components": len({r["source_group_id"] for r in selected}),
            **{kind: len({r["families"][kind] for r in selected})
               for kind in ("speaker", "chapter", "book", "project", "metadata_component")},
            "manifest_duration_seconds_not_audio_qualified": str(sum(
                (Decimal(r["manifest_duration_seconds"]) for r in selected), Decimal(0))),
            "audio_qualified_rows": 0,
            "clean_target_field": "text_raw",
            "clean_target_bytes": sum(r["text_raw_bytes"] for r in selected),
            "clean_target_lexical_tokens": sum(r["text_raw_lexical_tokens"] for r in selected),
            "clean_target_project_tokens": None,
            "unique_text_raw_sha256": len(distinct_targets),
            "deduplicated_raw_target_bytes": sum(r["text_raw_bytes"] for r in distinct_targets.values()),
            "deduplicated_raw_target_lexical_tokens": sum(r["text_raw_lexical_tokens"]
                                                         for r in distinct_targets.values()),
            **{field + "_" + metric: sum(r[field + "_" + metric] for r in selected)
               for field in ("text", "text_raw") for metric in ("bytes", "lexical_tokens", "leakage_words")},
            "unique_text_sha256": len({r["text_sha256"] for r in selected})}
    prior_counts = Counter(r["parent_status"] for r in rows if r["official_split"] in TRAIN_SPLITS)
    newly_excluded = defaultdict(list)
    for row in rows:
        if (row["official_split"] in TRAIN_SPLITS and
                row["parent_status"] == "potential_supply_pending_full_text_and_audio_qualification" and
                row["role"] == "excluded_overlap"):
            newly_excluded[row["families"]["metadata_component"]].append(row)
    summary = {"status": "FULL_TEXT_PARENT_QUALIFICATION_DEVELOPMENT_ONLY",
        "model_or_candidate_outputs_used": False, "final_candidate_inference": False,
        "development_reference_field": "text_raw",
        "development_reference_policy": "DEVELOPMENT_TEXT_RAW_RELEASE_SURFACE_NOT_PROTOCOL_FREEZE",
        "training_or_ASR_performed": False, "partition_seed": partition_seed,
        "calibration_fraction": str(calibration_fraction), "split_rule": SPLIT_RULE,
        "near_duplicate_rule": NEAR_DUPLICATE_RULE,
        "exact_group_rule": "same_long_NFC_casefold_word_signature_min20words_v1",
        "variant_policy": "all_text_text_raw_cross_field_pairs_before_role_assignment",
        "lexical_policy": "lexical_eval_v1", "lexical_policy_sha256": POLICY_HASH,
        "rows": len(rows), "official_training_rows": sum(prior_counts.values()),
        "prior_parent_bounds_independently_reproduced": dict(sorted(prior_counts.items())),
        "text_text_raw_different_rows": field_differences,
        "long_variant_occurrences": long_occurrences, "near_sweep": sweep,
        "long_exact_cross_row_edges": len(exact_edges),
        "long_exact_edges": exact_edges,
        "long_exact_unique_row_pairs": len({tuple(sorted((e["left"], e["right"]))) for e in exact_edges}),
        "near_cross_row_edges": len(near_edges), "near_novel_component_connections": novel_connections,
        "near_edges": near_edges,
        "near_unique_row_pairs": len({tuple(sorted((e["left"], e["right"]))) for e in near_edges}),
        "exact_final_target_veto_rule": "raw_or_text_literal_equals_either_final_field_any_length_row_only_v1",
        "exact_final_target_veto_by_split": dict(sorted(Counter(r["official_split"] for r in rows
            if r["exclusion_reason"] == "exact_final_target_literal_any_length_row_veto_v1").items())),
        "roles": totals, "components": sorted(component_receipts, key=lambda r: r["source_group_id"]),
        "role_rows_by_official_split": {split: dict(sorted(Counter(r["role"] for r in rows
            if r["official_split"] == split).items())) for split in sorted(RELEASE_SPLITS)},
        "new_training_exclusion_parent_components": [
            {"metadata_component": component, "rows": len(group),
             "source_group_id": group[0]["source_group_id"],
             "stable_ids_sha256": canonical_hash([r["id"] for r in group]),
             "exclusion_reasons": dict(sorted(Counter(r["exclusion_reason"] for r in group).items()))}
            for component, group in sorted(newly_excluded.items())],
        "new_training_exclusions_after_text_closure": dict(sorted(Counter(
            r["exclusion_reason"] for r in rows if r["official_split"] in TRAIN_SPLITS and
            r["parent_status"] == "potential_supply_pending_full_text_and_audio_qualification" and
            r["role"] == "excluded_overlap").items())),
        "short_signature_cross_role_collisions": short_collisions,
        "literal_final_reference_cross_role_collisions": literal_final_collisions,
        "pending": ["SLUE actual references and cross-corpus sweep", "audio admission and qualified raw ASR pairs",
                    "project tokenizer token totals", "final protocol freeze"]}
    return summary, sorted(manifest, key=lambda r: r["id"]), sorted(full_roles, key=lambda r: r["id"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("chapter_metadata", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--full-output", type=Path, required=True)
    args = parser.parse_args()
    begin = time.perf_counter()
    code_identity = sha256_bytes(Path(__file__).read_bytes())
    chapters, receipt = independent_parent_graph(args.chapter_metadata)
    rows, members = load_release(args.archive, chapters)
    summary, manifest, full = qualify(rows)
    args.output.mkdir(parents=True, exist_ok=True)
    args.full_output.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output / "public_lspc_training_roles.development.jsonl"
    summary_path = args.output / "public_lspc_training_supply_qualification.json"
    full_path = args.full_output / "all_release_roles.development.jsonl"
    for path, records in ((manifest_path, manifest), (full_path, full)):
        with path.open("w") as stream:
            for row in records:
                stream.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
    summary.update(archive_sha256=sha256_bytes(args.archive.read_bytes()), member_sha256=members,
                   chapter_metadata=receipt, manifest_sha256=sha256_bytes(manifest_path.read_bytes()),
                   full_ignored_manifest_sha256=sha256_bytes(full_path.read_bytes()),
                   code_sha256=code_identity,
                   committed_manifest_roles=["train", "calibration", "hpo_development"],
                   python_version=platform.python_version(), unicode_version=ud.unidata_version,
                   elapsed_seconds=time.perf_counter() - begin)
    summary_path.write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("status", "rows", "roles", "near_sweep",
        "long_exact_cross_row_edges", "near_cross_row_edges", "new_training_exclusions_after_text_closure",
        "elapsed_seconds")}, indent=2), flush=True)


if __name__ == "__main__":
    main()
