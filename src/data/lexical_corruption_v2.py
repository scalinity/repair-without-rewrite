"""Approved TRAIN-only lexical-projected character corruption estimator.

The table is a controlled DEVELOPMENT intervention, not a word/phonetic model.
Raw strings remain model inputs/targets; projection is only an estimation view.
"""
from collections import Counter, defaultdict
from itertools import combinations
import hashlib
import json

from src.data.empirical_corruption import Edit, alignment_consensus, nonoverlapping
from src.scoring.text import POLICY_HASH, lexical


PROFILE_VERSION = "development_lexical_corruption_v2"
ALIGNMENT_VERSION = "lexical-projected-codepoint-all-optimal-edge-consensus-v2"
OPERATION_CODES = {"substitution": "S", "deletion": "D", "insertion": "I"}
CLASS_PAIRS = ("SS", "SD", "SI", "DD", "DI", "II")


def phi(text):
    tokens = lexical(text)
    if any(not token or " " in token for token in tokens):
        raise ValueError("lexical token violates ASCII-separator safety")
    return " ".join(tokens)


def serialized(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2,
                       allow_nan=False) + "\n").encode("utf-8")


def class_pair(left, right):
    codes = (OPERATION_CODES[left.operation], OPERATION_CODES[right.operation])
    return "".join(sorted(codes, key="SDI".index))


def separator_only(key):
    return tuple(key) in (("insertion", "", " "), ("deletion", " ", ""))


def concentration_alarms(weighted_entries):
    """Exact strict-majority triggers; callers supply table or realized weights."""
    entries = [(tuple(key), weight) for key, weight in weighted_entries]
    if any(weight < 0 for _, weight in entries):
        raise ValueError("negative edit weight")
    if len({key for key, _ in entries}) != len(entries):
        raise ValueError("entry weights must be aggregated")
    total = sum(weight for _, weight in entries)
    largest = max((weight for _, weight in entries), default=0)
    separator = sum(weight for key, weight in entries if separator_only(key))
    return {"total_weight": total, "largest_entry_weight": largest,
            "separator_only_weight": separator,
            "entry_strict_majority": largest * 2 > total,
            "separator_strict_majority": separator * 2 > total}


def _entry_table(audits, omitted_group=None):
    observations = {}
    for row in audits:
        if row["source_group_id"] == omitted_group:
            continue
        for name, count_name in (("consensus_edits", "occurrences"),
                                 ("ambiguous_edits", "ambiguous_possible_edges")):
            for edit in row[name]:
                key = (edit["operation"], edit["reference"], edit["hypothesis"])
                item = observations.setdefault(key, {"occurrences": 0,
                    "ambiguous_possible_edges": 0, "records": set(), "groups": set()})
                item[count_name] += 1
                if name == "consensus_edits":
                    item["records"].add(row["id"])
                    item["groups"].add(row["source_group_id"])
    entries = []
    for key, item in sorted(observations.items()):
        supported = len(item["records"]) >= 5 and len(item["groups"]) >= 3
        entries.append({"key": list(key), "occurrences": item["occurrences"],
                        "record_count": len(item["records"]),
                        "group_count": len(item["groups"]),
                        "source_group_ids": sorted(item["groups"]),
                        "ambiguous_possible_edges": item["ambiguous_possible_edges"],
                        "supported": supported,
                        "support_rejected_occurrences": 0 if supported else item["occurrences"],
                        "weight": item["occurrences"] if supported else 0,
                        "separator_only": separator_only(key)})
    return entries


def estimate_lexical_profile(rows):
    rows = list(rows)
    ids, audits = set(), []
    groups = sorted({row["source_group_id"] for row in rows})
    raw_zero = 0
    for row in rows:
        if row["role"] != "train" or row.get("status") != "COMPLETED":
            raise ValueError("profile requires completed TRAIN records only")
        if row["id"] in ids:
            raise ValueError("profile record reused")
        ids.add(row["id"])
        target, source = phi(row["target"]), phi(row["source"])
        result = alignment_consensus(target, source)
        raw_zero += row["target"] == row["source"]
        audits.append({"id": row["id"], "source_group_id": row["source_group_id"],
            "projected_target": target, "projected_source": source,
            "projected_target_sha256": hashlib.sha256(target.encode()).hexdigest(),
            "projected_source_sha256": hashlib.sha256(source.encode()).hexdigest(),
            "distance": result["distance"], "optimal_paths": result["optimal_paths"],
            "consensus_edits": [vars(edit) for edit in result["consensus"]],
            "ambiguous_edits": [vars(edit) for edit in result["ambiguous"]],
            "possible_edit_edges": result["possible_edit_edges"],
            "ambiguous_edit_edges": result["ambiguous_edit_edges"],
            "omitted_unit_edit_mass": result["omitted_unit_edit_mass"]})
    entries = _entry_table(audits)
    supported_keys = {tuple(entry["key"]) for entry in entries if entry["supported"]}
    pairs = {name: {"records": set(), "groups": set()} for name in CLASS_PAIRS}
    retained_by_group = Counter()
    for row in audits:
        retained = [Edit(**edit) for edit in row["consensus_edits"]
                    if (edit["operation"], edit["reference"], edit["hypothesis"]) in supported_keys]
        retained_by_group[row["source_group_id"]] += len(retained)
        observed = {class_pair(left, right) for left, right in combinations(retained, 2)
                    if nonoverlapping(left, right)}
        for name in observed:
            pairs[name]["records"].add(row["id"])
            pairs[name]["groups"].add(row["source_group_id"])
    cooccurrence = []
    for name in CLASS_PAIRS:
        item = pairs[name]
        supported = len(item["records"]) >= 5 and len(item["groups"]) >= 3
        cooccurrence.append({"class_pair": name, "record_count": len(item["records"]),
            "group_count": len(item["groups"]), "source_group_ids": sorted(item["groups"]),
            "supported": supported, "weight": len(item["records"]) if supported else 0})
    distances = Counter(row["distance"] for row in audits)
    positive = len(rows) - distances[0]
    retained = sum(entry["weight"] for entry in entries)
    omitted = sum(row["omitted_unit_edit_mass"] for row in audits)
    consensus = sum(len(row["consensus_edits"]) for row in audits)
    rejected = sum(entry["support_rejected_occurrences"] for entry in entries)
    mass = sum(distance * count for distance, count in distances.items())
    if mass != omitted + rejected + retained or consensus != rejected + retained:
        raise ValueError("projected edit mass does not reconcile")
    grouped = defaultdict(list)
    for row in audits:
        grouped[row["source_group_id"]].append(row)
    group_diagnostics = [{"source_group_id": group, "records": len(grouped[group]),
        "lexical_positive_records": sum(row["distance"] > 0 for row in grouped[group]),
        "projected_unit_edit_mass": sum(row["distance"] for row in grouped[group]),
        "consensus_occurrences": sum(len(row["consensus_edits"]) for row in grouped[group]),
        "retained_occurrences": retained_by_group[group]} for group in groups]
    top_keys = [entry["key"] for entry in sorted(entries, key=lambda item: (-item["weight"], item["key"]))
                if entry["supported"]][:10]
    sensitivity = []
    for group in groups:
        remaining = [row for row in audits if row["source_group_id"] != group]
        counts = Counter(row["distance"] for row in remaining)
        denominator = len(remaining) - counts[0]
        reduced_entries = _entry_table(audits, omitted_group=group)
        weights = {tuple(entry["key"]): entry["weight"] for entry in reduced_entries}
        sensitivity.append({"omitted_source_group_id": group,
            "remaining_records": len(remaining), "lexical_positive_records": denominator,
            "severity_P1_P2": {"0": 0, "1": counts[1], "2": denominator - counts[1]},
            "retained_occurrences": sum(weights.values()),
            "supported_entries": sum(entry["supported"] for entry in reduced_entries),
            "top_entry_weights": [{"key": key, "weight": weights.get(tuple(key), 0)} for key in top_keys]})
    table = {"profile_version": PROFILE_VERSION, "alignment_version": ALIGNMENT_VERSION,
        "lexical_policy_id": "lexical_eval_v1", "lexical_policy_sha256": POLICY_HASH,
        "unicode_version": "15.1.0", "projection": "ASCII-space join of lexical_eval_v1 token values",
        "records": len(rows), "groups": len(groups), "raw_zero_records": raw_zero,
        "lexical_zero_records": distances[0], "lexical_positive_records": positive,
        "lexical_positive_groups": sum(row["lexical_positive_records"] > 0 for row in group_diagnostics),
        "distance_distribution": {str(key): value for key, value in sorted(distances.items())},
        "severity_denominator": positive, "severity_P0": {"0": 0, "1": positive, "2": 0},
        "severity_P1_P2": {"0": 0, "1": distances[1], "2": positive - distances[1]},
        "projected_unit_edit_mass": mass, "omitted_unit_edit_mass": omitted,
        "consensus_occurrences": consensus, "support_rejected_occurrences": rejected,
        "retained_occurrences": retained,
        "possible_optimal_edit_edges": sum(row["possible_edit_edges"] for row in audits),
        "ambiguous_optimal_edit_edges": sum(row["ambiguous_edit_edges"] for row in audits),
        "records_with_ambiguous_edits": sum(row["omitted_unit_edit_mass"] > 0 for row in audits),
        "records_with_multiple_optimal_paths": sum(row["optimal_paths"] > 1 for row in audits),
        "entries": entries, "class_pairs": cooccurrence,
        "literal_pair_assumption": "conditional independence of supported marginal payloads in generated composition",
        "group_diagnostics": group_diagnostics, "leave_one_group_out": sensitivity,
        "concentration_alarms": concentration_alarms((entry["key"], entry["weight"]) for entry in entries)}
    return table, audits
