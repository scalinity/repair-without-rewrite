"""CPU-only complete finite generated-pool qualification before any BENCH."""
import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import time

from src.data.lexical_corruption_v2 import serialized
from src.data.mixed_reader_v3 import native_shape
from src.generation.lexical_v2 import (
    RENDERER_VERSION, SourceOnlyUnionInverse, digest, generated_bases,
    qualify_empirical_variant, rule_views,
)
from src.generation.stress import CATEGORIES
from src.models.tokenizer import ByteBPE
from src.scoring.triple import distance as edit_distance
from src.scoring.text import lexical


SAFE = Path("experiments/manifests/lexical_reader_v2")
TABLE = SAFE / "lexical-profile-table.attempt01.json"
TABLE_SHA = "bc14b7ca5e8299ee8004cefb6deb67151ea93f1d44f48ea48d0b4619a9549b87"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempt", type=int, required=True)
    args = parser.parse_args()
    if args.attempt < 1:
        raise ValueError("attempt must be positive")
    tag = f"attempt{args.attempt:02d}"
    OUT = Path("exports/lexical-reader-v2/generated-pool-" + tag)
    if sha(TABLE) != TABLE_SHA:
        raise ValueError("independently reproduced profile changed")
    table = json.loads(TABLE.read_text())
    if any(table["concentration_alarms"][key] for key in ("entry_strict_majority", "separator_strict_majority")):
        raise ValueError("profile stop rules block generated construction")
    OUT.mkdir(parents=True, exist_ok=False)
    preflight = {"scope": "CPU_GENERATED_POOL_QUALIFICATION_NOT_PROBE", "head": subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True).strip(), "profile_sha256": sha(TABLE),
        "decision_sha256": sha("docs/reviews/FRONTIER_CORRUPTION_PROFILE_DECISION_V2.md"),
        "tokenizer_sha256": sha("configs/tokenizer_development/tokenizer.json"),
        "code_hashes": {path: sha(path) for path in (
            "src/generation/lexical_v2.py", "src/generation/stress.py", "src/data/mixed_reader_v3.py",
            "src/models/tokenizer.py", "src/models/edits.py", "benchmarks/lexical_generated_pool_v2.py",
            "tests/generation/test_lexical_v2.py")}, "renderer": RENDERER_VERSION,
        "inverse_state_semantics": "compatible grammar plus all complete candidate field tuples before rejection/target deduplication",
        "inverse_bound": 500, "proposal_bound": 50, "neural_execution": "NONE", "probe_slots": 0}
    (OUT / "preflight.json").write_bytes(serialized(preflight))
    tokenizer = ByteBPE.load("configs/tokenizer_development")
    inverse = SourceOnlyUnionInverse(table)
    bases = generated_bases()
    reasons, strata, unavailable = Counter(), Counter(), Counter()
    attempts, max_states, accepted_count = 0, 0, 0
    public_bases, public_rows = [], []
    start = time.perf_counter()
    with (OUT / "accepted.jsonl").open("w") as accepted_stream, (OUT / "proposal-rejection-audit.jsonl").open("w") as audit_stream:
        for base_index, base in enumerate(bases):
            common = {key: base[key] for key in ("base_id", "family_id", "category", "cell", "field_type", "typed_bundle_id")}
            public_bases.append({**common, "target_sha256": digest(base["target"]), "anchor_sha256": digest(base["anchor"])})
            variants = []
            for view, (source, operations) in rule_views(base).items():
                result = inverse(source)
                shape = native_shape(tokenizer, source, base["anchor"], base["target"])
                if result.unique_target != base["target"] or shape is None:
                    reason = result.status if result.unique_target != base["target"] else "common_capacity_failed"
                    audit_stream.write(json.dumps({**common, "view": view, "reason": reason,
                        "source": source, "inverse": asdict(result)}, sort_keys=True) + "\n")
                    reasons[reason] += 1
                    unavailable[(base["category"], base["cell"], view)] += 1
                    continue
                variants.append((view, source, operations, None, result.examined_states, shape))
            for severity in (1, 2):
                if not table["severity_P0"].get(str(severity), 0) and not table["severity_P1_P2"].get(str(severity), 0):
                    continue
                shaped = {}
                def eligible(source):
                    value = native_shape(tokenizer, source, base["anchor"], base["target"])
                    if value is not None:
                        shaped[source] = value
                    return value is not None
                accepted, audit = qualify_empirical_variant(base, severity, table, inverse, eligible=eligible)
                attempts += len(audit)
                for row in audit:
                    reasons[row["reason"]] += 1
                    max_states = max(max_states, row.get("examined_states", 0))
                    audit_stream.write(json.dumps({**common, "view": f"empirical{severity}", **row}, sort_keys=True) + "\n")
                if accepted is None:
                    unavailable[(base["category"], base["cell"], f"empirical{severity}")] += 1
                    continue
                variants.append((f"empirical{severity}", accepted["source"], accepted["operations"], severity,
                                 accepted["examined_states"], shaped[accepted["source"]]))
            for view, source, operations, severity, states, shape in variants:
                metadata = {**common, "variant_id": base["base_id"] + "/" + view, "view": view,
                    "severity": severity, "source_sha256": digest(source), "target_sha256": digest(base["target"]),
                    "anchor_sha256": digest(base["anchor"]), "operations": operations,
                    "examined_states": states, "lexical_distance_source_anchor": edit_distance(lexical(source), lexical(base["anchor"])),
                    "lexical_distance_source_target": edit_distance(lexical(source), lexical(base["target"])),
                    "raw_codepoint_distance_source_anchor": edit_distance(source, base["anchor"]),
                    "source_equals_target": source == base["target"],
                    "lexical_source_equals_target": lexical(source) == lexical(base["target"]),
                    "applied_operation_count": len(operations), **shape}
                accepted_stream.write(json.dumps({**metadata, "source": source, "anchor": base["anchor"], "target": base["target"]}, sort_keys=True) + "\n")
                public_rows.append({key: value for key, value in metadata.items() if key not in
                    ("operations", "source_ids", "target_ids", "encoder_positions", "byte_offsets", "legal",
                     "gold_program", "gold_labels", "canonical_sequence")})
                strata[(base["category"], base["cell"], view)] += 1
                accepted_count += 1
                max_states = max(max_states, states)
            if (base_index + 1) % 500 == 0:
                print(json.dumps({"bases_completed": base_index + 1, "accepted_variants": accepted_count,
                                  "empirical_proposals": attempts, "elapsed_seconds": time.perf_counter() - start}), flush=True)
    required_views = ("clean", "mixed", "two", "empirical1", "empirical2")
    required = [{"category": category, "cell": cell, "view": view,
        "accepted": strata[(category, cell, view)], "unavailable": unavailable[(category, cell, view)]}
        for category in CATEGORIES for cell in range(4) for view in required_views
        if not view.startswith("empirical") or table["severity_P0"].get(view[-1], 0) or table["severity_P1_P2"].get(view[-1], 0)]
    empty = [row for row in required if row["accepted"] == 0]
    base_index_path = SAFE / f"generated-base-index.{tag}.json"
    accepted_index_path = SAFE / f"generated-accepted-index.{tag}.json"
    base_index_path.write_bytes(serialized(public_bases))
    accepted_index_path.write_bytes(serialized(public_rows))
    summary = {"status": "FRONTIER_MODEL_REVIEW_REQUIRED" if empty else "GENERATED_POOL_QUALIFIED_READER_PENDING",
        "base_count": len(bases), "accepted_variant_count": accepted_count, "required_strata": required,
        "empty_required_strata": empty, "proposal_count": attempts, "proposal_reasons": dict(reasons),
        "max_examined_states": max_states, "source_only_unique_inverse_required": True,
        "accepted_pool_sha256": sha(OUT / "accepted.jsonl"), "proposal_audit_sha256": sha(OUT / "proposal-rejection-audit.jsonl"),
        "base_index_sha256": sha(base_index_path),
        "accepted_index_sha256": sha(accepted_index_path),
        "profile_sha256": sha(TABLE), "wall_seconds": time.perf_counter() - start,
        "realized_reader_concentration": "UNMEASURED", "scientific_stop_triggered": bool(empty), "probe_slots": 0}
    (SAFE / f"generated-pool-qualification.{tag}.json").write_bytes(serialized(summary))
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
