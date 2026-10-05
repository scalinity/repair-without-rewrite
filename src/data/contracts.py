"""Development-only, candidate-independent reference and provenance contracts."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from collections import defaultdict
from collections.abc import Iterable, Mapping

import unicodedata2 as unicode

SPLIT_RULE = "development_source_groups_v1"
NEAR_DUPLICATE_RULE = "NFC-casefold-Unicode-word-regex-5gram-Jaccard>=0.90;min20words-v1"
ROLES = {"train", "hpo_development", "calibration", "sealed_final", "excluded_overlap"}
FINAL_SPLITS = {"test", "test-clean", "test-other"}
DEV_SPLITS = {"validation", "dev", "dev-clean", "dev-other"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_hash(value: object) -> str:
    return sha256_bytes(json.dumps(value, sort_keys=True, ensure_ascii=True,
                                  separators=(",", ":")).encode())


@dataclass(frozen=True)
class ReferenceStatus:
    valid: bool
    reason: str
    genuine_empty: bool = False


def reference_status(row: Mapping, *, documented_sentinels: Iterable[str] = ()) -> ReferenceStatus:
    """F03: only an explicitly designated empty string is a legitimate empty R."""
    if "reference" not in row:
        return ReferenceStatus(False, "reference_missing")
    ref = row["reference"]
    if ref is None:
        return ReferenceStatus(False, "reference_null")
    if not isinstance(ref, str):
        return ReferenceStatus(False, "reference_not_string")
    try:
        ref.encode("utf-8", "strict")
    except UnicodeEncodeError:
        return ReferenceStatus(False, "reference_invalid_utf8")
    if ref in set(documented_sentinels):
        return ReferenceStatus(False, "reference_documented_sentinel")
    if ref == "":
        legitimate = row.get("legitimate_empty_reference") is True
        return ReferenceStatus(legitimate, "legitimate_empty_reference" if legitimate
                               else "empty_reference_not_designated", legitimate)
    return ReferenceStatus(True, "reference_present")


def fingerprint_tokens(text: str) -> tuple[str, ...]:
    """Leakage signature only, NOT lexical_eval_v1 or a model-input normalizer."""
    return tuple(re.findall(r"\w+", unicode.normalize("NFC", text).casefold()))


def shingles(tokens: tuple[str, ...]) -> frozenset[tuple[str, ...]]:
    if len(tokens) < 20:
        return frozenset()
    return frozenset(tokens[i:i + 5] for i in range(len(tokens) - 4))


def make_role_manifest(rows: Iterable[Mapping], *, calibration_fraction: float = .1,
                       partition_seed: int = 120101) -> list[dict]:
    """Group before augmentation; preserve final membership and exclude its relatives.

    Missing book/video identities stay null. Final references are represented by hashes
    in returned manifests; no training-facing API reads the sealed payload.
    """
    if not 0 <= calibration_fraction < 1:
        raise ValueError("calibration_fraction must be in [0,1)")
    items = [dict(r) for r in rows]
    items.sort(key=lambda r: (r["corpus"], r["id"]))
    ids = [(r["corpus"], r["id"]) for r in items]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate stable source ID; resolve before role assignment")
    parent = list(range(len(items)))

    def find(i):
        while i != parent[i]:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def join(a, b):
        ra, rb = find(a), find(b)
        parent[max(ra, rb)] = min(ra, rb)

    seen = {}
    near_index = defaultdict(list)
    token_sets = []
    for i, row in enumerate(items):
        if any(k in row for k in ("output", "candidate", "model_output", "scores")):
            raise ValueError("candidate data forbidden in source manifest")
        if not row["id"] or not row.get("split"):
            raise ValueError("stable ID and official split are required")
        status = reference_status(row)
        if not status.valid:
            raise ValueError(status.reason)
        families = row.get("families", {})
        keys = [(row["corpus"], k, v) for k, v in families.items() if v is not None]
        if row.get("audio_sha256"):
            keys.append(("global", "audio_sha256", row["audio_sha256"]))
        tokens = fingerprint_tokens(row["reference"])
        if len(tokens) >= 20:
            keys.append(("global", "long_reference_exact", canonical_hash(tokens)))
        for key in keys:
            if key in seen:
                join(i, seen[key])
            else:
                seen[key] = i
        ss = shingles(tokens)
        token_sets.append(ss)
        # Only same-corpus long-text similarity; candidate content never enters.
        candidates = set()
        for shingle in ss:
            candidates.update(near_index[(row["corpus"], shingle)])
        for j in sorted(candidates):
            other = token_sets[j]
            if len(ss & other) / len(ss | other) >= .9:
                join(i, j)
        for shingle in ss:
            near_index[(row["corpus"], shingle)].append(i)
    components = defaultdict(list)
    for i in range(len(items)):
        components[find(i)].append(i)
    output = []
    for indices in components.values():
        identities = [ids[i] for i in indices]
        group = canonical_hash(identities)
        splits = {items[i]["split"] for i in indices}
        has_final = bool(splits & FINAL_SPLITS)
        has_dev = bool(splits & DEV_SPLITS)
        number = int(canonical_hash([SPLIT_RULE, partition_seed, group]), 16) / 2**256
        training_role = "calibration" if number < calibration_fraction else "train"
        for i in indices:
            row = items[i]
            split = row["split"]
            reason = None
            if split in FINAL_SPLITS:
                role = "sealed_final"
            elif has_final:
                role, reason = "excluded_overlap", "known_final_source_family_or_long_text_overlap"
            elif split in DEV_SPLITS:
                role = "hpo_development"
            elif has_dev:
                role, reason = "excluded_overlap", "known_development_source_family_or_long_text_overlap"
            elif split in {"train", "fine-tune", "train-clean-100", "train-clean-360", "train-other-500"}:
                role = training_role
            else:
                raise ValueError("unrecognized official split")
            output.append({
                "corpus": row["corpus"], "id": row["id"], "official_split": split,
                "role": role, "source_group_id": group, "families": row.get("families", {}),
                "reference_sha256": sha256_bytes(row["reference"].encode()),
                "reference_signature_sha256": canonical_hash(fingerprint_tokens(row["reference"])),
                "legitimate_empty_reference": row["reference"] == "",
                "audio_sha256": row.get("audio_sha256"),
                "audio_qualification": "PENDING" if not row.get("audio_qualified") else "VERIFIED",
                "exclusion_reason": reason, "split_rule": SPLIT_RULE,
                "near_duplicate_rule": NEAR_DUPLICATE_RULE,
            })
    return sorted(output, key=lambda r: (r["corpus"], r["id"]))


def require_development_role(record: Mapping) -> None:
    if record.get("role") not in {"train", "hpo_development"}:
        raise ValueError("sealed, reserved calibration or excluded record is forbidden for development")
