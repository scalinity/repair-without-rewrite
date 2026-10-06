"""CPU-only v2 prerequisite measurement. Never executes a neural model."""
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import time

from src.data.development_reader import load_targets
from src.data.lexical_corruption_v2 import (
    ALIGNMENT_VERSION, PROFILE_VERSION, estimate_lexical_profile, phi, serialized,
)


PAIR_PATH = Path("exports/foundation-repair/development-asr-pairs-attempt01/pairs.jsonl")
PAIR_SHA256 = "ce4a170a086afee430085c4e6f665e8af58b8c68091afc27f10ee403c81951d8"
ROLE_PATH = Path("experiments/manifests/public_lspc_training_roles.development.jsonl")
SUPPLY_PATH = Path("experiments/manifests/public_lspc_training_supply_qualification.json")
RAW_PATH = Path("experiments/manifests/frontier_reader/empirical-profile-table.attempt01.json")
RAW_SHA256 = "5df3800d7a29e370abdce36bd489989482d5d878765612b5a14a4b2cab1fc310"
OUT = Path("exports/lexical-reader-v2/profile-attempt01")
SAFE = Path("experiments/manifests/lexical_reader_v2")


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write(path, value):
    Path(path).write_bytes(serialized(value))


def admitted_rows():
    if sha(PAIR_PATH) != PAIR_SHA256 or sha(RAW_PATH) != RAW_SHA256:
        raise ValueError("frozen pair bytes or preserved raw table changed")
    admitted = {row["id"]: row for row in load_targets(ROLE_PATH, SUPPLY_PATH, allowed_roles={"train"})}
    pairs = [json.loads(line) for line in PAIR_PATH.read_text().splitlines()]
    rows = [row for row in pairs if row["role"] == "train"]
    excluded = [row for row in pairs if row["role"] != "train"]
    if len(rows) != 1024 or len({row["id"] for row in rows}) != 1024 or len({row["source_group_id"] for row in rows}) != 48:
        raise ValueError("approved TRAIN profile population changed")
    if len(excluded) != 96 or any(row["role"] != "calibration" for row in excluded):
        raise ValueError("excluded CALIBRATION population changed")
    if ({row["id"] for row in rows} & {row["id"] for row in excluded}
            or {row["source_group_id"] for row in rows} & {row["source_group_id"] for row in excluded}):
        raise ValueError("TRAIN/CALIBRATION overlap")
    for row in rows:
        current = admitted[row["id"]]
        for key in ("role", "source_group_id", "text_raw_sha256", "text_sha256", "families"):
            if row[key] != current[key]:
                raise ValueError("frozen pair no longer rejoins admitted TRAIN identity")
        if (row["target"] != current["target"]
                or hashlib.sha256(row["target"].encode("utf-8", "strict")).hexdigest() != row["text_raw_sha256"]
                or hashlib.sha256(row["source"].encode("utf-8", "strict")).hexdigest() != row["source_sha256"]):
            raise ValueError("frozen reference/hypothesis bytes changed")
    zero = sum(phi(row["target"]) == phi(row["source"]) for row in rows)
    if zero != 690 or len(rows) - zero != 334:
        raise ValueError("prior lexical-zero/positive evidence did not reproduce")
    return rows


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    code = ["src/data/lexical_corruption_v2.py", "src/data/empirical_corruption.py",
            "src/scoring/text.py", "src/data/development_reader.py",
            "benchmarks/lexical_corruption_profile_v2.py", "tests/data/test_lexical_corruption_v2.py"]
    receipt = {"status": "STARTED_CPU_ONLY", "profile_version": PROFILE_VERSION,
        "alignment_version": ALIGNMENT_VERSION,
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "code_hashes": {path: sha(path) for path in code},
        "pair_file_sha256": sha(PAIR_PATH), "role_manifest_sha256": sha(ROLE_PATH),
        "supply_receipt_sha256": sha(SUPPLY_PATH), "preserved_raw_table_sha256": sha(RAW_PATH),
        "decision_sha256": sha("docs/reviews/FRONTIER_CORRUPTION_PROFILE_DECISION_V2.md"),
        "tokenizer_sha256": sha("configs/tokenizer_development/tokenizer.json"),
        "canonical_source_sha256": sha("docs/design-inputs/EXTRACTED_CANONICAL_SOURCE.md"),
        "registry_sha256": sha("docs/design-inputs/LocalFlow_Publication_Experiment_Registry_v2.txt"),
        "runtime": {"python": platform.python_version(), "platform": platform.platform(),
                    "MLX_ENABLE_TF32": os.environ.get("MLX_ENABLE_TF32")},
        "neural_execution": "NONE", "six_probe_slots_consumed": 0,
        "seed": "NONE: deterministic exhaustive TRAIN profile estimation"}
    write(OUT / "preflight.json", receipt)
    (OUT / "preflight.diff").write_text(subprocess.check_output(["git", "diff", "--binary"], text=True))
    start = time.perf_counter()
    rows = admitted_rows()
    write(OUT / "input-train-hashes.json", [{key: row[key] for key in
        ("id", "source_group_id", "text_raw_sha256", "source_sha256")} for row in rows])
    table, audit = estimate_lexical_profile(rows)
    write(OUT / "private-projected-alignment-audit.json", audit)
    SAFE.mkdir(parents=True, exist_ok=True)
    write(SAFE / "lexical-profile-table.attempt01.json", table)
    operations = Counter()
    for entry in table["entries"]:
        operations[entry["key"][0]] += entry["weight"]
    alarms = table["concentration_alarms"]
    stopped = (not table["retained_occurrences"] or alarms["entry_strict_majority"]
               or alarms["separator_strict_majority"])
    summary = {key: table[key] for key in (
        "profile_version", "alignment_version", "records", "groups", "raw_zero_records",
        "lexical_zero_records", "lexical_positive_records", "lexical_positive_groups",
        "distance_distribution", "severity_denominator", "severity_P0", "severity_P1_P2",
        "projected_unit_edit_mass", "omitted_unit_edit_mass", "consensus_occurrences",
        "support_rejected_occurrences", "retained_occurrences", "possible_optimal_edit_edges",
        "ambiguous_optimal_edit_edges", "records_with_ambiguous_edits", "records_with_multiple_optimal_paths",
        "concentration_alarms")}
    summary.update({"status": "FRONTIER_MODEL_REVIEW_REQUIRED" if stopped else "PROFILE_ESTIMATED_GENERATED_QUALIFICATION_PENDING",
        "excluded_calibration_records": 96, "operations": dict(operations),
        "supported_entries": sum(entry["supported"] for entry in table["entries"]),
        "unsupported_entries": sum(not entry["supported"] for entry in table["entries"]),
        "class_pairs": table["class_pairs"], "profile_table_sha256": sha(SAFE / "lexical-profile-table.attempt01.json"),
        "input_train_hashes_sha256": sha(OUT / "input-train-hashes.json"),
        "private_alignment_audit_sha256": sha(OUT / "private-projected-alignment-audit.json"),
        "measurement_wall_seconds": time.perf_counter() - start,
        "old_raw_table_sha256_after": sha(RAW_PATH), "scientific_stop_triggered": stopped,
        "generated_population": "NOT_CONSTRUCTED", "reader": "NOT_QUALIFIED"})
    if summary["old_raw_table_sha256_after"] != RAW_SHA256:
        raise ValueError("raw table changed during new estimation")
    write(SAFE / "lexical-profile-measurement.attempt01.json", summary)
    receipt.update(status=summary["status"], measurement_sha256=sha(SAFE / "lexical-profile-measurement.attempt01.json"))
    write(SAFE / "lexical-profile-preflight.attempt01.json", receipt)
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
