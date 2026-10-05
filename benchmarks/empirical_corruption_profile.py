"""CPU-only prerequisite measurement; never trains, decodes, or admits a reader."""
from collections import Counter
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import time

from src.data.development_reader import load_targets
from src.data.empirical_corruption import ALIGNMENT_VERSION, estimate_profile


PAIR_PATH = Path("exports/foundation-repair/development-asr-pairs-attempt01/pairs.jsonl")
PAIR_SHA256 = "ce4a170a086afee430085c4e6f665e8af58b8c68091afc27f10ee403c81951d8"
ROLE_PATH = Path("experiments/manifests/public_lspc_training_roles.development.jsonl")
SUPPLY_PATH = Path("experiments/manifests/public_lspc_training_supply_qualification.json")
OUT = Path("exports/frontier-reader/empirical-profile-attempt01")
SAFE = Path("experiments/manifests/frontier_reader")


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2, allow_nan=False) + "\n")


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    if sha(PAIR_PATH) != PAIR_SHA256:
        raise ValueError("frozen TRAIN/CAL pair bytes changed")
    runner = str(Path(__file__).resolve().relative_to(Path.cwd().resolve()))
    code = ["src/data/empirical_corruption.py", "src/data/development_reader.py", runner,
            "tests/data/test_empirical_corruption.py"]
    receipt = {"status": "STARTED", "head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
               "dirty_status": subprocess.check_output(["git", "status", "--porcelain"], text=True),
               "code_hashes": {p: sha(p) for p in code}, "pair_file_sha256": sha(PAIR_PATH),
               "roles_sha256": sha(ROLE_PATH), "supply_sha256": sha(SUPPLY_PATH),
               "decision_sha256": sha("docs/reviews/FRONTIER_READER_CURRICULUM_DECISION_V1.md"),
               "tokenizer_sha256": sha("configs/tokenizer_development/tokenizer.json"),
               "alignment_version": ALIGNMENT_VERSION, "normalization": "NONE",
               "seed": "NONE: exhaustive deterministic TRAIN estimation",
               "model_initialization": "NONE: no neural execution", "reader": "NOT_IMPLEMENTED",
               "renderer": "NOT_IMPLEMENTED", "profile": "PENDING_MEASUREMENT",
               "runtime": {"python": platform.python_version(), "platform": platform.platform(),
                           "unicode": importlib.metadata.version("unicodedata2"),
                           "MLX_ENABLE_TF32": os.environ.get("MLX_ENABLE_TF32")}}
    write(OUT / "preflight.json", receipt)
    (OUT / "preflight.diff").write_text(subprocess.check_output(["git", "diff", "--binary"], text=True))
    start = time.perf_counter()
    admitted = {r["id"]: r for r in load_targets(ROLE_PATH, SUPPLY_PATH, allowed_roles={"train"})}
    pair_rows = [json.loads(line) for line in PAIR_PATH.read_text().splitlines()]
    rows = [r for r in pair_rows if r["role"] == "train"]
    if len(rows) != 1024 or len({r["source_group_id"] for r in rows}) != 48:
        raise ValueError("approved 1024-record/48-group TRAIN pool changed")
    selected = []
    for r in rows:
        current = admitted[r["id"]]
        for key in ("role", "source_group_id", "text_raw_sha256", "text_sha256", "families"):
            if r[key] != current[key]:
                raise ValueError("frozen pair does not rejoin admitted source")
        if r["target"] != current["target"] or hashlib.sha256(r["target"].encode("utf-8", "strict")).hexdigest() != r["text_raw_sha256"]:
            raise ValueError("official reference bytes changed")
        if hashlib.sha256(r["source"].encode("utf-8", "strict")).hexdigest() != r["source_sha256"]:
            raise ValueError("frozen hypothesis bytes changed")
        selected.append({k: r[k] for k in ("id", "source_group_id", "text_raw_sha256", "source_sha256")})
    write(OUT / "input-train-hashes.json", selected)
    profile = estimate_profile(rows)
    write(OUT / "profile-with-private-alignment-audit.json", profile)
    table = {k: v for k, v in profile.items() if k != "record_audit"}
    tags, operations = Counter(), Counter()
    for entry in table["entries"]:
        tags[entry["effect"]] += entry["weight"]
        operations[entry["key"][0]] += entry["weight"]
    retained = sum(tags.values())
    raw_mass = sum(int(k) * v for k, v in profile["distance_distribution"].items())
    support_rejected = sum(e["support_rejected_occurrences"] for e in table["entries"])
    summary = {"status": "PROFILE_ESTIMATED_READER_ADMISSION_PENDING", "records": len(rows), "groups": 48,
               "excluded_calibration_records": len(pair_rows) - len(rows),
               "supported_entries": sum(e["supported"] for e in table["entries"]),
               "unsupported_entries": sum(not e["supported"] for e in table["entries"]),
               "supported_cooccurrence_entries": sum(e["supported"] for e in table["cooccurrence"]),
               "raw_unit_edit_mass": raw_mass, "consensus_occurrences": profile["consensus_occurrences"],
               "ambiguity_omitted_unit_mass": profile["omitted_unit_edit_mass"],
               "support_rejected_consensus_occurrences": support_rejected,
               "retained_occurrences": retained, "effects": dict(tags), "operations": dict(operations),
               "distance_distribution": profile["distance_distribution"],
               "severity_P0": profile["severity_P0"], "severity_P1_P2": profile["severity_P1_P2"],
               "records_with_ambiguous_edits": sum(r["omitted_unit_edit_mass"] > 0 for r in profile["record_audit"]),
               "records_with_multiple_optimal_paths": sum(r["optimal_paths"] > 1 for r in profile["record_audit"]),
               "possible_optimal_edit_edges": profile["possible_optimal_edit_edges"],
               "ambiguous_optimal_edit_edges": profile["ambiguous_optimal_edit_edges"],
               "input_train_hashes_sha256": sha(OUT / "input-train-hashes.json"),
               "alignment_audit_sha256": sha(OUT / "profile-with-private-alignment-audit.json"),
               "estimation_seconds": time.perf_counter() - start}
    if raw_mass != profile["omitted_unit_edit_mass"] + support_rejected + retained:
        raise ValueError("edit mass does not reconcile")
    SAFE.mkdir(parents=True, exist_ok=True)
    write(SAFE / "empirical-profile-table.attempt01.json", table)
    summary["empirical_table_sha256"] = sha(SAFE / "empirical-profile-table.attempt01.json")
    write(SAFE / "empirical-profile-measurement.attempt01.json", summary)
    receipt.update(status="COMPLETED_CPU_PROFILE_MEASUREMENT", summary_sha256=sha(SAFE / "empirical-profile-measurement.attempt01.json"))
    write(SAFE / "empirical-profile-preflight.attempt01.json", receipt)
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
