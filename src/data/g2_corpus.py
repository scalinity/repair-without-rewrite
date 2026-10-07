"""Closed-census joins and source requests without model or transport imports."""
from collections import Counter, defaultdict
import hashlib
import json
from decimal import Decimal

COUNTS = {"train": 14113, "calibration": 1900, "hpo_development": 796}


def text_hash(value):
    return hashlib.sha256(value.encode("utf-8", "strict")).hexdigest()


def canonical_hash(value):
    return text_hash(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False))


def validate_census(rows):
    if Counter(row["role"] for row in rows) != COUNTS:
        raise ValueError("complete approved census counts required; no subset admission")
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("duplicate census identity")
    groups, families = defaultdict(set), defaultdict(set)
    for row in rows:
        if not Decimal(2) <= Decimal(str(row["manifest_duration_seconds"])) <= Decimal(12):
            raise ValueError("census duration outside approved envelope")
        if row["reference_field"] != "text_raw" or text_hash(row["target"]) != row["text_raw_sha256"]:
            raise ValueError("changed canonical reference")
        if text_hash(row["official_processed_target"]) != row["text_sha256"]:
            raise ValueError("changed released processed reference")
        groups[row["role"]].add(row["source_group_id"])
        families[row["role"]].update(row["families"].items())
    roles = tuple(COUNTS)
    for i, role in enumerate(roles):
        for other in roles[i + 1:]:
            if groups[role] & groups[other] or families[role] & families[other]:
                raise ValueError("source-group or derivation-family leakage")
    if len(groups["calibration"] | groups["hpo_development"]) != 52:
        raise ValueError("expanded development must retain the frozen 52 groups")


def bind_legacy(census, old_pairs, old_panel):
    admitted = {row["id"]: row for row in census}
    training = [row for row in old_pairs if row["role"] == "train"]
    development = [row for row in old_panel if row["population"] == "natural"]
    if len(training) != 1024 or len(development) != 108:
        raise ValueError("legacy 1024 TRAIN and 108 DEVELOPMENT required")
    result = {}
    for row in [*training, *development]:
        canonical = admitted[row["id"]]
        role = "calibration" if row["role"] == "calibration_development_consumed" else row["role"]
        if (row["target"] != canonical["target"] or role != canonical["role"]
                or row["source_group_id"] != canonical["source_group_id"]
                or text_hash(row["source"]) != row["source_sha256"]):
            raise ValueError("legacy source/reference/role/group bytes changed")
        if row["id"] in result:
            raise ValueError("duplicate legacy source")
        result[row["id"]] = row
    return result


def source_requests(census, legacy, replay_selection):
    unique = [row for row in sorted(census, key=lambda x: x["id"]) if row["id"] not in legacy]
    counts = Counter("TRAIN" if row["role"] == "train" else "DEVELOPMENT" for row in unique)
    if counts != {"TRAIN": 13089, "DEVELOPMENT": 2588}:
        raise ValueError("new recognizer census changed")
    expected_replay = []
    for population in ("TRAIN", "DEVELOPMENT"):
        eligible = [row for row in unique if (row["role"] == "train") == (population == "TRAIN")]
        key = lambda row: canonical_hash(["G2", 42, "PARAKEET_REPLAY", population, row["id"]])
        expected_replay.extend({"id": row["id"], "role": row["role"],
            "source_group_id": row["source_group_id"], "selection_sha256": key(row)}
            for row in sorted(eligible, key=key)[:32])
    if expected_replay != replay_selection["cases"]:
        raise ValueError("one-time replay selection changed after freeze")
    requests = [{"request_id": "unique/" + row["id"], "id": row["id"],
                 "role": row["role"], "kind": "unique"} for row in unique]
    requests.extend({"request_id": "replay/" + row["id"], "id": row["id"],
                     "role": row["role"], "kind": "replay"} for row in expected_replay)
    if len(requests) != 15741 or len({row["request_id"] for row in requests}) != 15741:
        raise ValueError("recognizer call budget mismatch")
    return requests


def check_audio_info(info):
    if (info.samplerate != 16000 or info.channels != 1 or info.format != "FLAC"
            or info.subtype != "PCM_16" or not 32000 <= info.frames <= 192000):
        raise ValueError("required native recording outside pinned source-runtime envelope")


def support_floor(rows):
    from src.scoring.text import lexical
    errors = [row for row in rows if lexical(row["source"]) != lexical(row["target"])]
    result = {"cases": len(rows), "lexical_error_cases": len(errors),
              "lexical_error_groups": len({row["source_group_id"] for row in errors}),
              "lexical_zero_cases": len(rows) - len(errors)}
    result["pass"] = (result["lexical_error_cases"] >= 200
                      and result["lexical_error_groups"] >= 20
                      and result["lexical_zero_cases"] >= 200)
    return result
