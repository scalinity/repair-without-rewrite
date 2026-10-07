"""Append-only reconstruction of observed G2 CAL source and decode use."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path

from src.data.g2_artifacts import ArtifactRoot, sha256


def run(binding, attempt):
    root = ArtifactRoot(binding)
    root.preflight()
    output = Path(f"experiments/manifests/development_calibration_consumption_generation_2.attempt{attempt:02d}.json")
    if output.exists():
        raise FileExistsError(output)
    prospective = Path("experiments/manifests/development_calibration_consumption_generation_2.attempt01.json")
    original = json.loads(prospective.read_text())
    ids = set(original["calibration_ids"])
    assert len(ids) == 1900 and original["training_use_forbidden"]
    source = root.path("asr-hypotheses-v1/construction.attempt01/calls.jsonl")
    calls = Counter()
    if source.exists():
        for line in source.open():
            row = json.loads(line)
            if row["event"] == "START" and row["request"]["id"] in ids:
                calls[row["request"]["kind"]] += 1
    files = []
    uses = Counter()
    for area in ("bench-v1", "evaluation-v1", "byt5-v1"):
        directory = root.path(area)
        if not directory.exists():
            continue
        # Include retained failed partials as observed use; never consume their
        # checkpoint states or exclude their completed evaluation records.
        for path in sorted(directory.glob("*/evaluation-*.jsonl")):
            count = 0
            for line in path.open():
                row = json.loads(line)
                if row["id"] in ids:
                    uses[row["id"]] += 1
                    count += 1
            if count:
                files.append(dict(artifact_relative=str(path.relative_to(root.root)),
                    file_sha256=sha256(path),calibration_evaluations=count,
                    completed_artifact=".partial-" not in path.parent.name))
    recorded_uses = sum(uses.values())
    repair_path = Path("experiments/manifests/generation_2/byt5-record-repair.attempt01.json")
    repair = json.loads(repair_path.read_text())
    failed_path = Path(repair["failed_receipt"])
    assert sha256(failed_path) == repair["failed_receipt_sha256"]
    assert repair["completed_optimizer_updates"] == 0 and repair["successful_recorded_evaluations"] == 0
    unwritten = repair["unwritten_failure_reference_uses"]
    assert len(unwritten) == 1 and unwritten[0]["id"] in ids and unwritten[0]["role"] == "calibration"
    uses[unwritten[0]["id"]] += 1
    result = dict(schema="g2_observed_calibration_consumption_v1",created_utc=datetime.now(timezone.utc).isoformat(),
        prospective_receipt=str(prospective),prospective_receipt_sha256=sha256(prospective),
        calibration_ids=sorted(ids),calibration_unique_rows=1900,
        expanded_corpus_support_and_reference_qualification_rows=1900,
        source_recognizer_calibration_calls=dict(calls),source_recognizer_calls=sum(calls.values()),
        new_student_neural_case_evaluations=sum(uses.values()),student_evaluated_unique_rows=len(uses),
        recorded_student_neural_case_evaluations=recorded_uses,
        unwritten_failure_reference_uses=unwritten,mechanical_repair_receipt_sha256=sha256(repair_path),
        per_id_student_evaluation_counts=dict(uses),evaluation_files=files,
        previous_neural_case_evaluations=original["previous_neural_case_evaluations"],
        remaining_untouched_duration_eligible_calibration_rows=0,
        fit_performed=False,training_use_forbidden=True,sealed_reference_use=False,
        scientific_recipes_started=0,status="OBSERVED_USE_RECONSTRUCTED")
    output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-binding",required=True)
    parser.add_argument("--attempt",type=int,required=True)
    args = parser.parse_args()
    result = run(args.artifact_binding,args.attempt)
    print(json.dumps({key:result[key] for key in ("status","source_recognizer_calls","new_student_neural_case_evaluations")}),flush=True)
