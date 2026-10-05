"""TRAIN-only literal/codepoint profile from all optimal raw alignments.

This estimates the approved table; it does not admit a generated reader pool.
"""
from collections import Counter
from dataclasses import dataclass
from itertools import combinations
import unicodedata2 as unicode


ALIGNMENT_VERSION = "raw-codepoint-all-optimal-edge-consensus-v1"


@dataclass(frozen=True, order=True)
class Edit:
    operation: str
    reference_position: int
    hypothesis_position: int
    reference: str
    hypothesis: str

    @property
    def key(self):
        return (self.operation, self.reference, self.hypothesis)


def _prefix_lattice(reference, hypothesis):
    n, m = len(reference), len(hypothesis)
    distance = [[0] * (m + 1) for _ in range(n + 1)]
    count = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        distance[i][0], count[i][0] = i, 1
    for j in range(m + 1):
        distance[0][j], count[0][j] = j, 1
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diagonal = distance[i - 1][j - 1] + (reference[i - 1] != hypothesis[j - 1])
            deletion = distance[i - 1][j] + 1
            insertion = distance[i][j - 1] + 1
            best = min(diagonal, deletion, insertion)
            distance[i][j] = best
            count[i][j] = ((count[i - 1][j - 1] if diagonal == best else 0)
                           + (count[i - 1][j] if deletion == best else 0)
                           + (count[i][j - 1] if insertion == best else 0))
    return distance, count


def alignment_consensus(reference, hypothesis):
    """Return exact distance and edit edges present on EVERY optimal path.

    An edge includes both raw coordinates and payload. Prefix/suffix path counts
    prove unanimity without enumerating or arbitrarily selecting tracebacks.
    """
    reference.encode("utf-8", "strict")
    hypothesis.encode("utf-8", "strict")
    forward, prefixes = _prefix_lattice(reference, hypothesis)
    reverse, suffixes = _prefix_lattice(reference[::-1], hypothesis[::-1])
    n, m = len(reference), len(hypothesis)
    distance, total_paths = forward[n][m], prefixes[n][m]
    certain, uncertain = [], []
    possible_edit_edges = 0
    for i in range(n + 1):
        for j in range(m + 1):
            edges = []
            if i < n and j < m and reference[i] != hypothesis[j]:
                edges.append((i + 1, j + 1, Edit("substitution", i, j, reference[i], hypothesis[j])))
            if i < n:
                edges.append((i + 1, j, Edit("deletion", i, j, reference[i], "")))
            if j < m:
                edges.append((i, j + 1, Edit("insertion", i, j, "", hypothesis[j])))
            for ni, nj, edit in edges:
                if forward[i][j] + 1 + reverse[n - ni][m - nj] != distance:
                    continue
                possible_edit_edges += 1
                if prefixes[i][j] * suffixes[n - ni][m - nj] == total_paths:
                    certain.append(edit)
                else:
                    uncertain.append(edit)
    return {"distance": distance, "optimal_paths": total_paths,
            "consensus": tuple(sorted(certain)), "ambiguous": tuple(sorted(uncertain)),
            "possible_edit_edges": possible_edit_edges,
            "ambiguous_edit_edges": possible_edit_edges - len(certain),
            "omitted_unit_edit_mass": distance - len(certain)}


def effect_tag(key):
    _, reference, hypothesis = key
    if reference and hypothesis and reference != hypothesis and reference.casefold() == hypothesis.casefold():
        return "case"
    if any(c.isspace() for c in reference + hypothesis):
        return "whitespace_boundary"
    if any(unicode.category(c).startswith("P") for c in reference + hypothesis):
        return "punctuation"
    return "other"


def nonoverlapping(left, right):
    """Distinct positions in original text: codepoint slots or insertion gaps."""
    def position(edit):
        return ("gap" if edit.operation == "insertion" else "codepoint", edit.reference_position)
    return position(left) != position(right)


def estimate_profile(rows):
    """Each unique, completed TRAIN record contributes exactly once."""
    rows = list(rows)
    ids = set()
    entries, joints = {}, {}
    distances = Counter()
    record_audit = []
    possible = ambiguous = consensus_count = omitted = 0
    for row in rows:
        if row["role"] != "train" or row.get("status") != "COMPLETED":
            raise ValueError("profile requires completed TRAIN records only")
        identifier, group = row["id"], row["source_group_id"]
        if identifier in ids:
            raise ValueError("profile record reused")
        ids.add(identifier)
        result = alignment_consensus(row["target"], row["source"])
        edits = result["consensus"]
        distances[result["distance"]] += 1
        possible += result["possible_edit_edges"]
        ambiguous += result["ambiguous_edit_edges"]
        omitted += result["omitted_unit_edit_mass"]
        consensus_count += len(edits)
        for edit in edits:
            item = entries.setdefault(edit.key, {"occurrences": 0, "records": set(), "groups": set(),
                                                  "ambiguous_possible_edges": 0})
            item["occurrences"] += 1
            item["records"].add(identifier)
            item["groups"].add(group)
        for edit in result["ambiguous"]:
            item = entries.setdefault(edit.key, {"occurrences": 0, "records": set(), "groups": set(),
                                                  "ambiguous_possible_edges": 0})
            item["ambiguous_possible_edges"] += 1
        for left, right in combinations(edits, 2):
            if not nonoverlapping(left, right):
                continue
            key = tuple(sorted((left.key, right.key)))
            item = joints.setdefault(key, {"occurrences": 0, "records": set(), "groups": set()})
            item["occurrences"] += 1
            item["records"].add(identifier)
            item["groups"].add(group)
        record_audit.append({"id": identifier, "source_group_id": group,
                             "distance": result["distance"], "optimal_paths": result["optimal_paths"],
                             "consensus_edits": [vars(e) for e in edits],
                             "ambiguous_edits": [vars(e) for e in result["ambiguous"]],
                             "possible_edit_edges": result["possible_edit_edges"],
                             "ambiguous_edit_edges": result["ambiguous_edit_edges"],
                             "omitted_unit_edit_mass": result["omitted_unit_edit_mass"]})

    table = []
    for key, item in sorted(entries.items()):
        supported = len(item["records"]) >= 5 and len(item["groups"]) >= 3
        table.append({"key": list(key), "effect": effect_tag(key),
                      "occurrences": item["occurrences"], "record_count": len(item["records"]),
                      "group_count": len(item["groups"]), "supported": supported,
                      "ambiguous_possible_edges": item["ambiguous_possible_edges"],
                      "support_rejected_occurrences": 0 if supported else item["occurrences"],
                      "weight": item["occurrences"] if supported else 0})
    supported_keys = {tuple(item["key"]) for item in table if item["supported"]}
    cooccurrence = []
    for key, item in sorted(joints.items()):
        supported = (len(item["records"]) >= 5 and len(item["groups"]) >= 3
                     and all(k in supported_keys for k in key))
        cooccurrence.append({"keys": [list(k) for k in key], "occurrences": item["occurrences"],
                             "record_count": len(item["records"]), "group_count": len(item["groups"]),
                             "supported": supported, "weight": item["occurrences"] if supported else 0})
    return {"alignment_version": ALIGNMENT_VERSION, "unicode_version": unicode.unidata_version,
            "records": len(rows), "groups": len({r["source_group_id"] for r in rows}),
            "distance_distribution": dict(sorted(distances.items())),
            "severity_P0": dict(sorted(Counter({0: distances[0], 1: len(rows) - distances[0]}).items())),
            "severity_P1_P2": {0: distances[0], 1: distances[1], 2: len(rows) - distances[0] - distances[1]},
            "possible_optimal_edit_edges": possible, "ambiguous_optimal_edit_edges": ambiguous,
            "consensus_occurrences": consensus_count, "omitted_unit_edit_mass": omitted,
            "entries": table, "cooccurrence": cooccurrence, "record_audit": record_audit}
