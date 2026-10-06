"""Independent CPU oracle for the approved DEVELOPMENT lexical profile.

This module never imports the production projection or alignment estimator.
Raw and projected utterances are written only to explicitly ignored evidence.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import time

import unicodedata2 as ud


ROOT = Path(__file__).resolve().parents[1]
PAIR = "exports/foundation-repair/development-asr-pairs-attempt01/pairs.jsonl"
PAIR_SHA = "ce4a170a086afee430085c4e6f665e8af58b8c68091afc27f10ee403c81951d8"
RAW_TABLE = "experiments/manifests/frontier_reader/empirical-profile-table.attempt01.json"
RAW_SHA = "5df3800d7a29e370abdce36bd489989482d5d878765612b5a14a4b2cab1fc310"
CLASS_PAIRS = ("SS", "SD", "SI", "DD", "DI", "II")
OP_CLASS = {"substitution": "S", "deletion": "D", "insertion": "I"}
CLASS_ORDER = {"S": 0, "D": 1, "I": 2}
EDIT_FIELDS = ("operation", "reference_position", "hypothesis_position", "reference", "hypothesis")


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def write(path, value):
    Path(path).write_bytes(encoded(value))


class IndependentLexicalScanner:
    """Pinned value scanner; NFC uses Unicode tables, not production origins."""

    def __init__(self):
        if ud.unidata_version != "15.1.0":
            raise ValueError("independent lexical oracle requires Unicode 15.1.0")
        table = ROOT / "docs/design-inputs/unicode-15.1.0"
        self.fold = {}
        for line in (table / "CaseFolding.txt").read_text().splitlines():
            body = line.partition("#")[0].strip()
            if not body:
                continue
            scalar, status, target, *_ = [part.strip() for part in body.split(";")]
            if status in ("C", "F"):
                self.fold[chr(int(scalar, 16))] = "".join(chr(int(v, 16)) for v in target.split())
        self.white = set()
        for line in (table / "PropList.txt").read_text().splitlines():
            body = line.partition("#")[0].strip()
            if not body:
                continue
            span, prop = [part.strip() for part in body.split(";")]
            if prop == "White_Space":
                bounds = span.split("..")
                self.white.update(chr(i) for i in range(int(bounds[0], 16), int(bounds[-1], 16) + 1))
        self.policy_hash = hashlib.sha256(("lexical_eval_v1:15.1.0:" + sha(table / "CaseFolding.txt")
                                         + sha(table / "PropList.txt") + sha(ud.__file__)).encode()).hexdigest()

    def tokens(self, text):
        if not isinstance(text, str):
            raise ValueError("projection input must be present text")
        text.encode("utf-8", "strict")
        text = ud.normalize("NFC", text)
        text = ud.normalize("NFC", "".join(self.fold.get(c, c) for c in text))
        text = text.translate(str.maketrans({"\u2018": "'", "\u2019": "'", "\u2010": "-", "\u2011": "-"}))
        word = lambda c: ud.category(c)[0] in "LMN"
        values = []
        position = 0
        while position < len(text):
            start = position
            c = text[position]
            if word(c):
                position += 1
                while position < len(text):
                    current = text[position]
                    internal_joiner = (current in "'-" and position + 1 < len(text)
                                       and word(text[position - 1]) and word(text[position + 1]))
                    if not (word(current) or internal_joiner):
                        break
                    position += 1
            elif c in self.white or (ud.category(c)[0] == "P" and c not in "-%"):
                position += 1
                continue
            else:
                position += 1
            values.append(text[start:position])
        if any(not value or " " in value for value in values):
            raise ValueError("lexical token violates ASCII separator-safety invariant")
        return tuple(values)

    def projection(self, text):
        return " ".join(self.tokens(text))


def independent_alignment(reference, hypothesis):
    """Intersect edit sets at optimal predecessors; no reverse count product."""
    reference.encode("utf-8", "strict")
    hypothesis.encode("utf-8", "strict")
    if reference == hypothesis:
        return {"distance": 0, "optimal_paths": 1, "consensus": (), "ambiguous": (),
                "possible_edit_edges": 0, "ambiguous_edit_edges": 0, "omitted_unit_edit_mass": 0}
    n, m = len(reference), len(hypothesis)
    distances = [list(range(m + 1))]
    common = [frozenset()]
    counts = [1] * (m + 1)
    for j in range(1, m + 1):
        common.append(common[-1] | {("insertion", 0, j - 1, "", hypothesis[j - 1])})
    for i in range(1, n + 1):
        current = [i] + [0] * m
        unanimous = [common[0] | {("deletion", i - 1, 0, reference[i - 1], "")}]
        ways = [1]
        for j in range(1, m + 1):
            costs = (distances[-1][j - 1] + (reference[i - 1] != hypothesis[j - 1]),
                     distances[-1][j] + 1, current[j - 1] + 1)
            best = min(costs)
            current[j] = best
            candidates = []
            path_count = 0
            if costs[0] == best:
                addition = ({("substitution", i - 1, j - 1, reference[i - 1], hypothesis[j - 1])}
                            if reference[i - 1] != hypothesis[j - 1] else set())
                candidates.append(common[j - 1] | addition)
                path_count += counts[j - 1]
            if costs[1] == best:
                candidates.append(common[j] | {("deletion", i - 1, j, reference[i - 1], "")})
                path_count += counts[j]
            if costs[2] == best:
                candidates.append(unanimous[j - 1] | {("insertion", i, j - 1, "", hypothesis[j - 1])})
                path_count += ways[j - 1]
            intersection = candidates[0]
            for candidate in candidates[1:]:
                intersection &= candidate
            unanimous.append(intersection)
            ways.append(path_count)
        distances.append(current)
        common, counts = unanimous, ways
    certain = set(common[m])
    stack, visited, possible = [(n, m)], {(n, m)}, set()
    while stack:
        i, j = stack.pop()
        predecessors = []
        if i and j and distances[i - 1][j - 1] + (reference[i - 1] != hypothesis[j - 1]) == distances[i][j]:
            predecessors.append((i - 1, j - 1))
            if reference[i - 1] != hypothesis[j - 1]:
                possible.add(("substitution", i - 1, j - 1, reference[i - 1], hypothesis[j - 1]))
        if i and distances[i - 1][j] + 1 == distances[i][j]:
            predecessors.append((i - 1, j))
            possible.add(("deletion", i - 1, j, reference[i - 1], ""))
        if j and distances[i][j - 1] + 1 == distances[i][j]:
            predecessors.append((i, j - 1))
            possible.add(("insertion", i, j - 1, "", hypothesis[j - 1]))
        for predecessor in predecessors:
            if predecessor not in visited:
                visited.add(predecessor)
                stack.append(predecessor)
    return {"distance": distances[n][m], "optimal_paths": counts[m], "consensus": tuple(sorted(certain)),
            "ambiguous": tuple(sorted(possible - certain)), "possible_edit_edges": len(possible),
            "ambiguous_edit_edges": len(possible - certain), "omitted_unit_edit_mass": distances[n][m] - len(certain)}


def elementary_key(edit):
    return edit[0], edit[3], edit[4]


def original_position(edit):
    return ("gap" if edit[0] == "insertion" else "codepoint", edit[1])


def literal_effect(key):
    _, before, after = key
    if before and after and before != after and before.casefold() == after.casefold():
        return "case"
    if any(c.isspace() for c in before + after):
        return "whitespace_boundary"
    if any(ud.category(c).startswith("P") for c in before + after):
        return "punctuation"
    return "other"


def admitted_rows():
    if sha(ROOT / PAIR) != PAIR_SHA or sha(ROOT / RAW_TABLE) != RAW_SHA:
        raise ValueError("frozen pair or preserved raw-table identity changed")
    pairs = [json.loads(line) for line in (ROOT / PAIR).read_text().splitlines()]
    rows = [row for row in pairs if row["role"] == "train"]
    excluded = [row for row in pairs if row["role"] != "train"]
    if len(rows) != 1024 or len({r["source_group_id"] for r in rows}) != 48:
        raise ValueError("approved TRAIN population changed")
    if len(excluded) != 96 or any(row["role"] != "calibration" for row in excluded):
        raise ValueError("excluded CALIBRATION population changed")
    if ({r["id"] for r in rows} & {r["id"] for r in excluded}
            or {r["source_group_id"] for r in rows} & {r["source_group_id"] for r in excluded}):
        raise ValueError("TRAIN/CALIBRATION metadata intersects")
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("duplicate TRAIN input")
    if any(row["status"] != "COMPLETED" for row in rows):
        raise ValueError("incomplete TRAIN input")
    roles_path = ROOT / "experiments/manifests/public_lspc_training_roles.development.jsonl"
    supply = json.loads((ROOT / "experiments/manifests/public_lspc_training_supply_qualification.json").read_text())
    if sha(roles_path) != supply["manifest_sha256"]:
        raise ValueError("admitted role identity changed")
    role_rows = [row for row in map(json.loads, roles_path.read_text().splitlines()) if row["role"] == "train"]
    roles = {row["id"]: row for row in role_rows}
    if len(roles) != len(role_rows):
        raise ValueError("duplicate admitted TRAIN role")
    required = {row["id"] for row in rows}
    archive = ROOT / "exports/source-qualification/ls_pc_manifest.tar.gz"
    if sha(archive) != "96d4eae2222b29b66437a21959252419bcd4762e5042e71e023790171054d1c0":
        raise ValueError("official source archive changed")
    official = {}
    with tarfile.open(archive) as stream:
        for member in stream:
            if member.name.startswith("test-") or not member.name.endswith(".json"):
                continue
            for line in stream.extractfile(member):
                record = json.loads(line)
                identifier = Path(record["audio_filepath"]).stem
                if identifier in required:
                    if identifier in official:
                        raise ValueError("duplicate official TRAIN source")
                    official[identifier] = record
    if set(official) != required:
        raise ValueError("missing official TRAIN source")
    for row in rows:
        role, source = roles[row["id"]], official[row["id"]]
        if role["reference_field"] != "text_raw" or row["target"] != source["text_raw"]:
            raise ValueError("official reference binding failed")
        for key in ("role", "source_group_id", "text_raw_sha256", "text_sha256", "families"):
            if role[key] != row[key]:
                raise ValueError("frozen TRAIN metadata does not rejoin")
        for field, value in (("text_raw_sha256", row["target"]), ("text_sha256", source["text"]),
                             ("source_sha256", row["source"])):
            if hashlib.sha256(value.encode("utf-8", "strict")).hexdigest() != row[field]:
                raise ValueError("frozen reference or hypothesis bytes changed")
    return rows, {"records": len(rows), "groups": len({r["source_group_id"] for r in rows}),
                  "excluded_calibration_records": sum(r["role"] == "calibration" for r in pairs),
                  "pair_sha256": sha(ROOT / PAIR), "old_raw_table_sha256": sha(ROOT / RAW_TABLE),
                  "roles_sha256": sha(roles_path), "archive_sha256": sha(archive)}


def aggregate_marginals(audit):
    values = {}
    for record in audit:
        for certain, field in ((True, "consensus"), (False, "ambiguous")):
            for edit in record[field]:
                item = values.setdefault(elementary_key(edit), {"occurrences": 0, "records": set(), "groups": set(),
                                         "ambiguous_possible_edges": 0, "group_occurrences": Counter(), "group_records": defaultdict(set)})
                if certain:
                    item["occurrences"] += 1
                    item["records"].add(record["id"])
                    item["groups"].add(record["source_group_id"])
                    item["group_occurrences"][record["source_group_id"]] += 1
                    item["group_records"][record["source_group_id"]].add(record["id"])
                else:
                    item["ambiguous_possible_edges"] += 1
    entries = []
    for key, value in sorted(values.items()):
        supported = len(value["records"]) >= 5 and len(value["groups"]) >= 3
        entries.append({"key": list(key), "effect": literal_effect(key), "occurrences": value["occurrences"],
                        "record_count": len(value["records"]), "group_count": len(value["groups"]),
                        "supported": supported, "weight": value["occurrences"] if supported else 0,
                        "ambiguous_possible_edges": value["ambiguous_possible_edges"],
                        "support_rejected_occurrences": 0 if supported else value["occurrences"]})
    return values, entries


def class_pair_support(audit, supported_keys):
    records, groups = defaultdict(set), defaultdict(set)
    for row in audit:
        edits = [edit for edit in row["consensus"] if elementary_key(edit) in supported_keys]
        for left, right in combinations(edits, 2):
            if original_position(left) == original_position(right):
                continue
            pair = "".join(sorted((OP_CLASS[left[0]], OP_CLASS[right[0]]), key=CLASS_ORDER.get))
            records[pair].add(row["id"])
            groups[pair].add(row["source_group_id"])
    return [{"pair": pair, "record_count": len(records[pair]), "group_count": len(groups[pair]),
             "supported": len(records[pair]) >= 5 and len(groups[pair]) >= 3,
             "weight": len(records[pair]) if len(records[pair]) >= 5 and len(groups[pair]) >= 3 else 0,
             "record_ids": sorted(records[pair]), "group_ids": sorted(groups[pair])} for pair in CLASS_PAIRS]


def projected_profile(rows, scanner):
    audit = []
    for row in rows:
        before, after = scanner.projection(row["target"]), scanner.projection(row["source"])
        result = independent_alignment(before, after)
        audit.append({"id": row["id"], "source_group_id": row["source_group_id"],
                      "reference_projection": before, "hypothesis_projection": after, **result})
    values, entries = aggregate_marginals(audit)
    supported = {tuple(entry["key"]) for entry in entries if entry["supported"]}
    distances = Counter(r["distance"] for r in audit)
    positive = len(rows) - distances[0]
    if not positive:
        raise ValueError("FRONTIER_MODEL_REVIEW_REQUIRED: no lexical-positive TRAIN records")
    group_ids = sorted({r["source_group_id"] for r in audit})
    groups = []
    for group in group_ids:
        members = [r for r in audit if r["source_group_id"] == group]
        groups.append({"source_group_id": group, "records": len(members),
                       "lexical_positive": sum(r["distance"] > 0 for r in members),
                       "distance_one": sum(r["distance"] == 1 for r in members),
                       "projected_edit_mass": sum(r["distance"] for r in members),
                       "consensus_occurrences": sum(len(r["consensus"]) for r in members),
                       "retained_occurrences": sum(elementary_key(e) in supported for r in members for e in r["consensus"])})
    leave_out = []
    for group in groups:
        ident = group["source_group_id"]
        marginal = []
        for key, value in sorted(values.items()):
            nrecords = len(value["records"]) - len(value["group_records"].get(ident, set()))
            ngroups = len(value["groups"]) - int(ident in value["groups"])
            noccurrences = value["occurrences"] - value["group_occurrences"][ident]
            marginal.append({"key": list(key), "record_count": nrecords, "group_count": ngroups,
                             "weight": noccurrences if nrecords >= 5 and ngroups >= 3 else 0})
        npositive = positive - group["lexical_positive"]
        none = distances[1] - group["distance_one"]
        leave_out.append({"excluded_group": ident, "remaining_records": len(rows) - group["records"],
                          "positive_records": npositive, "severity_P1_P2": {0: 0, 1: none, 2: npositive - none},
                          "severity_denominator": npositive, "retained_occurrences": sum(e["weight"] for e in marginal),
                          "supported_entries": sum(e["weight"] > 0 for e in marginal), "entry_weights": marginal})
    total = sum(e["weight"] for e in entries)
    separator = sum(e["weight"] for e in entries if tuple(e["key"]) in (("insertion", "", " "), ("deletion", " ", "")))
    alarms = {"empty_supported_table": total == 0,
              "single_entry_strict_majority": bool(total and max(e["weight"] for e in entries) * 2 > total),
              "separator_insertion_deletion_strict_majority": bool(total and separator * 2 > total)}
    result = {"profile_version": "development_lexical_corruption_v2", "lexical_policy_hash": scanner.policy_hash,
              "records": len(rows), "groups": len(group_ids), "lexical_zero": distances[0], "lexical_positive": positive,
              "distance_distribution": dict(sorted(distances.items())), "severity_P0": {0: 0, 1: 1},
              "severity_P1_P2": {0: 0, 1: distances[1], 2: positive - distances[1]}, "severity_denominator": positive,
              "projected_unit_edit_mass": sum(k * v for k, v in distances.items()),
              "consensus_occurrences": sum(len(r["consensus"]) for r in audit),
              "ambiguity_omitted_unit_mass": sum(r["omitted_unit_edit_mass"] for r in audit),
              "support_rejected_occurrences": sum(e["support_rejected_occurrences"] for e in entries),
              "retained_occurrences": total, "separator_insertion_deletion_weight": separator,
              "possible_optimal_edit_edges": sum(r["possible_edit_edges"] for r in audit),
              "ambiguous_optimal_edit_edges": sum(r["ambiguous_edit_edges"] for r in audit),
              "records_with_ambiguous_edits": sum(r["omitted_unit_edit_mass"] > 0 for r in audit),
              "entries": entries, "class_pairs": class_pair_support(audit, supported),
              "group_diagnostics": groups, "leave_one_group_out": leave_out, "table_alarms": alarms}
    if result["projected_unit_edit_mass"] != result["ambiguity_omitted_unit_mass"] + result["support_rejected_occurrences"] + total:
        raise ValueError("independent projected mass fails reconciliation")
    return result, audit


def reproduce_raw_table(rows):
    audit = [{"id": r["id"], "source_group_id": r["source_group_id"], **independent_alignment(r["target"], r["source"])} for r in rows]
    _, entries = aggregate_marginals(audit)
    admitted = {tuple(e["key"]) for e in entries if e["supported"]}
    joints = {}
    for row in audit:
        for left, right in combinations(row["consensus"], 2):
            if original_position(left) == original_position(right):
                continue
            key = tuple(sorted((elementary_key(left), elementary_key(right))))
            item = joints.setdefault(key, {"occurrences": 0, "records": set(), "groups": set()})
            item["occurrences"] += 1
            item["records"].add(row["id"])
            item["groups"].add(row["source_group_id"])
    cooccurrence = []
    for key, value in sorted(joints.items()):
        supported = len(value["records"]) >= 5 and len(value["groups"]) >= 3 and all(k in admitted for k in key)
        cooccurrence.append({"keys": [list(k) for k in key], "occurrences": value["occurrences"],
                            "record_count": len(value["records"]), "group_count": len(value["groups"]),
                            "supported": supported, "weight": value["occurrences"] if supported else 0})
    distances = Counter(r["distance"] for r in audit)
    result = {"alignment_version": "raw-codepoint-all-optimal-edge-consensus-v1", "unicode_version": ud.unidata_version,
              "records": len(rows), "groups": len({r["source_group_id"] for r in rows}),
              "distance_distribution": dict(sorted(distances.items())),
              "severity_P0": {0: distances[0], 1: len(rows) - distances[0]},
              "severity_P1_P2": {0: distances[0], 1: distances[1], 2: len(rows) - distances[0] - distances[1]},
              "possible_optimal_edit_edges": sum(r["possible_edit_edges"] for r in audit),
              "ambiguous_optimal_edit_edges": sum(r["ambiguous_edit_edges"] for r in audit),
              "consensus_occurrences": sum(len(r["consensus"]) for r in audit),
              "omitted_unit_edit_mass": sum(r["omitted_unit_edit_mass"] for r in audit),
              "entries": entries, "cooccurrence": cooccurrence}
    if hashlib.sha256(encoded(result)).hexdigest() != RAW_SHA:
        raise ValueError("independent raw table byte reproduction disagrees")
    return result


def canonical_output(profile, audit, rows, scanner):
    """Serialize independent observations into the agreed public table schema."""
    values, _ = aggregate_marginals(audit)
    entries = []
    for entry in profile["entries"]:
        entries.append({key: entry[key] for key in ("key", "occurrences", "record_count", "group_count",
            "ambiguous_possible_edges", "supported", "support_rejected_occurrences", "weight")}
            | {"source_group_ids": sorted(values[tuple(entry["key"])]["groups"]),
               "separator_only": tuple(entry["key"]) in (("insertion", "", " "), ("deletion", " ", ""))})
    class_pairs = [{"class_pair": pair["pair"], "record_count": pair["record_count"],
        "group_count": pair["group_count"], "source_group_ids": pair["group_ids"],
        "supported": pair["supported"], "weight": pair["weight"]} for pair in profile["class_pairs"]]
    grouped = [{"source_group_id": group["source_group_id"], "records": group["records"],
        "lexical_positive_records": group["lexical_positive"], "projected_unit_edit_mass": group["projected_edit_mass"],
        "consensus_occurrences": group["consensus_occurrences"], "retained_occurrences": group["retained_occurrences"]}
        for group in profile["group_diagnostics"]]
    top = [entry["key"] for entry in sorted(entries, key=lambda entry: (-entry["weight"], entry["key"]))
           if entry["supported"]][:10]
    leave_out = []
    for omitted in profile["leave_one_group_out"]:
        weights = {tuple(entry["key"]): entry["weight"] for entry in omitted["entry_weights"]}
        leave_out.append({"omitted_source_group_id": omitted["excluded_group"],
            "remaining_records": omitted["remaining_records"], "lexical_positive_records": omitted["positive_records"],
            "severity_P1_P2": {str(k): v for k, v in omitted["severity_P1_P2"].items()},
            "retained_occurrences": omitted["retained_occurrences"], "supported_entries": omitted["supported_entries"],
            "top_entry_weights": [{"key": key, "weight": weights[tuple(key)]} for key in top]})
    total = profile["retained_occurrences"]
    maximum = max((entry["weight"] for entry in entries), default=0)
    separator = profile["separator_insertion_deletion_weight"]
    public = {"profile_version": "development_lexical_corruption_v2",
        "alignment_version": "lexical-projected-codepoint-all-optimal-edge-consensus-v2",
        "lexical_policy_id": "lexical_eval_v1", "lexical_policy_sha256": scanner.policy_hash,
        "unicode_version": "15.1.0", "projection": "ASCII-space join of lexical_eval_v1 token values",
        "records": profile["records"], "groups": profile["groups"],
        "raw_zero_records": sum(row["target"] == row["source"] for row in rows),
        "lexical_zero_records": profile["lexical_zero"], "lexical_positive_records": profile["lexical_positive"],
        "lexical_positive_groups": sum(group["lexical_positive_records"] > 0 for group in grouped),
        "distance_distribution": {str(k): v for k, v in profile["distance_distribution"].items()},
        "severity_denominator": profile["severity_denominator"],
        "severity_P0": {"0": 0, "1": profile["severity_denominator"], "2": 0},
        "severity_P1_P2": {str(k): v for k, v in profile["severity_P1_P2"].items()},
        "projected_unit_edit_mass": profile["projected_unit_edit_mass"],
        "omitted_unit_edit_mass": profile["ambiguity_omitted_unit_mass"],
        "consensus_occurrences": profile["consensus_occurrences"],
        "support_rejected_occurrences": profile["support_rejected_occurrences"],
        "retained_occurrences": total, "possible_optimal_edit_edges": profile["possible_optimal_edit_edges"],
        "ambiguous_optimal_edit_edges": profile["ambiguous_optimal_edit_edges"],
        "records_with_ambiguous_edits": profile["records_with_ambiguous_edits"],
        "records_with_multiple_optimal_paths": sum(row["optimal_paths"] > 1 for row in audit),
        "entries": entries, "class_pairs": class_pairs,
        "literal_pair_assumption": "conditional independence of supported marginal payloads in generated composition",
        "group_diagnostics": grouped, "leave_one_group_out": leave_out,
        "concentration_alarms": {"total_weight": total, "largest_entry_weight": maximum,
            "separator_only_weight": separator, "entry_strict_majority": maximum * 2 > total,
            "separator_strict_majority": separator * 2 > total}}
    private = []
    for row in audit:
        private.append({"id": row["id"], "source_group_id": row["source_group_id"],
            "projected_target": row["reference_projection"], "projected_source": row["hypothesis_projection"],
            "projected_target_sha256": hashlib.sha256(row["reference_projection"].encode("utf-8")).hexdigest(),
            "projected_source_sha256": hashlib.sha256(row["hypothesis_projection"].encode("utf-8")).hexdigest(),
            **{key: row[key] for key in ("distance", "optimal_paths", "possible_edit_edges", "ambiguous_edit_edges", "omitted_unit_edit_mass")},
            "consensus_edits": [dict(zip(EDIT_FIELDS, edit)) for edit in row["consensus"]],
            "ambiguous_edits": [dict(zip(EDIT_FIELDS, edit)) for edit in row["ambiguous"]]})
    return public, private


def self_checks(scanner):
    fixtures = {"": "", " A\tB. ": "a b", "can't": "can't", "cant": "cant", "a b": "a b", "ab": "ab",
                "Straße": "strasse", "e\u0301": "é", "LEFT\u2011right": "left-right", "‘A’": "a", "50%": "50 %"}
    for text, expected in fixtures.items():
        if scanner.projection(text) != expected:
            raise ValueError("independent lexical fixture failed")
    strings = ["".join(v) for n in range(3) for v in product("ab", repeat=n)]
    for before, after in product(strings, repeat=2):
        paths = []
        def walk(i, j, cost, edits):
            if i == len(before) and j == len(after):
                paths.append((cost, frozenset(edits)))
                return
            if i < len(before) and j < len(after):
                addition = [("substitution", i, j, before[i], after[j])] if before[i] != after[j] else []
                walk(i + 1, j + 1, cost + int(before[i] != after[j]), edits + addition)
            if i < len(before):
                walk(i + 1, j, cost + 1, edits + [("deletion", i, j, before[i], "")])
            if j < len(after):
                walk(i, j + 1, cost + 1, edits + [("insertion", i, j, "", after[j])])
        walk(0, 0, 0, [])
        best = min(p[0] for p in paths)
        optimal = [set(edits) for cost, edits in paths if cost == best]
        actual = independent_alignment(before, after)
        if (actual["distance"] != best or actual["optimal_paths"] != len(optimal)
                or set(actual["consensus"]) != set.intersection(*optimal)
                or set(actual["ambiguous"]) != set.union(*optimal) - set.intersection(*optimal)):
            raise ValueError("independent alignment disagrees with exhaustive self-oracle")
    return {"projection_fixtures": len(fixtures), "exhaustive_alignment_pairs": len(strings) ** 2}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "exports/lexical-reader-v2/independent-review/attempt01")
    parser.add_argument("--production-table", type=Path)
    parser.add_argument("--production-audit", type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    scanner = IndependentLexicalScanner()
    checks = self_checks(scanner)
    rows, binding = admitted_rows()
    write(args.out / "preflight.json", {"code_sha256": sha(__file__), "input_binding": binding,
          "policy_sha256": scanner.policy_hash, "profile_version": "development_lexical_corruption_v2",
          "seed": "NONE: exhaustive deterministic TRAIN estimation", "neural_execution": "NONE",
          "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()})
    profile, audit = projected_profile(rows, scanner)
    write(args.out / "independent-projected-audit.json", audit)
    write(args.out / "independent-profile.json", profile)
    public, private = canonical_output(profile, audit, rows, scanner)
    write(args.out / "independent-canonical-table.json", public)
    write(args.out / "independent-canonical-projected-audit.json", private)
    raw = reproduce_raw_table(rows)
    write(args.out / "independent-preserved-raw-table.json", raw)
    comparisons = {}
    for label, path, rebuilt in (("table", args.production_table, public), ("private_audit", args.production_audit, private)):
        if path is not None:
            original = Path(path).read_bytes()
            if original != encoded(rebuilt):
                write(args.out / "comparison-failure.json", {"object": label, "expected_sha256": sha(path),
                      "independent_sha256": hashlib.sha256(encoded(rebuilt)).hexdigest()})
                raise ValueError("independent canonical " + label + " bytes disagree")
            comparisons[label] = {"status": "EXACT_BYTE_PARITY", "sha256": sha(path)}
    receipt = {"status": "PASS_INDEPENDENT_EXACT_PARITY" if comparisons else "INDEPENDENT_CANONICAL_OUTPUT_READY_PARITY_PENDING",
               "input_binding": binding, "comparisons": comparisons,
               "method": "own_pinned_scanner_optimal_predecessor_edit_set_intersection_backward_possible_edge_union",
               "code_sha256": sha(__file__), "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "self_checks": checks, "profile_sha256": sha(args.out / "independent-profile.json"),
               "projected_audit_sha256": sha(args.out / "independent-projected-audit.json"),
               "canonical_table_sha256": sha(args.out / "independent-canonical-table.json"),
               "canonical_private_audit_sha256": sha(args.out / "independent-canonical-projected-audit.json"),
               "old_raw_table_sha256": sha(args.out / "independent-preserved-raw-table.json"),
               "seconds": time.perf_counter() - started, "neural_modules_loaded": any(
                   name == "mlx" or name.startswith("mlx.") or name == "torch" or name.startswith("torch.") for name in sys.modules)}
    write(args.out / "receipt.json", receipt)
    compact = {key: value for key, value in profile.items() if key not in {"entries", "class_pairs", "group_diagnostics", "leave_one_group_out"}}
    compact.update({"supported_entries": sum(e["supported"] for e in profile["entries"]),
                    "supported_class_pairs": [p["pair"] for p in profile["class_pairs"] if p["supported"]]})
    print(json.dumps({"receipt": receipt, "measurement": compact}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
