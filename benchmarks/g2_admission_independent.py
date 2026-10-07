"""Read-only admission prerequisite audit; contains no scientific launcher."""
import argparse
import json
from pathlib import Path
import subprocess
import time

from src.data.g2_artifacts import ArtifactRoot, sha256


def assert_unstarted(configs, scientific_area):
    expected = {f"G2-{arm}-{data}-{condition}-seed42-lr3e-4"
        for data, condition in (("D0","U8"),("D1","U1"),("D1","U8"))
        for arm in ("B100","C101")}
    expected.add("G2-ByT5-D1-10pass-seed42-lr3e-4")
    if len(configs) != 7 or {row["recipe_id"] for row in configs} != expected:
        raise ValueError("all seven unique fixed scientific recipes required")
    if any(row["status"] != "AUTHORIZED_UNSTARTED" or row["scientific_slot_consumed"] is not False
            or row["qualification_initializers_forbidden"] is not True
            or row["execution_requires_separate_owner_session"] is not True for row in configs):
        raise ValueError("scientific recipe or initializer boundary changed")
    area = Path(scientific_area)
    if area.exists() and any(area.iterdir()):
        raise ValueError("scientific output area is nonempty; unstarted status requires investigation")
    return {"recipes":7,"status":"AUTHORIZED_UNSTARTED","scientific_slots_consumed":0,
            "qualification_initializers_forbidden":True,"scientific_output_entries":0}


def reconstruct_remaining_storage(root, directory, configs):
    # Read complete manifests and physical file sizes directly; no forecast
    # producer or checkpoint-read helper is imported.
    def size(relative, filename):
        path = root.path(relative)
        complete = json.loads((path / "COMPLETE.json").read_text())
        actual = (path / filename).stat().st_size
        assert actual > 0 and complete["files"][filename]["bytes"] == actual
        return actual
    native = {}
    for arm in ("B100", "C101"):
        arrays, metadata = [], []
        for data, condition in (("D0", "U8"), ("D1", "U1"), ("D1", "U8")):
            bench = json.loads((directory / f"bench-{arm}-{data}-{condition}.attempt01.json").read_text())
            for relative in bench["checkpoint_relatives"].values():
                arrays.append(size(relative, "arrays.npz"))
                metadata.append(size(relative, "metadata.json"))
        count = sum(len({item["master_completed"] for item in row["save_endpoints"]})
            for row in configs if row["recipe_id"].startswith("G2-" + arm + "-"))
        assert count == 39 and len(arrays) == len(metadata) == 12
        native[arm] = count * (max(arrays) + max(16 * 1024**2, max(metadata)))
    by = json.loads((directory / "byt5-qualification.attempt02.json").read_text())
    recipe = next(row for row in configs if row["recipe_id"].startswith("G2-ByT5-"))
    assert recipe["save_evaluate_pass_milestones"] == [0, 2, 5, 10]
    byt5 = (size(by["initial_checkpoint"]["relative"], "state.pt")
        + 3 * size(by["final_checkpoint"]["relative"], "state.pt") + 4 * 16 * 1024**2)
    allowances = {"additional_failed_attempt_reserve":32 * 1024**3,
        "one_writer_atomic_transient":8 * 1024**3,
        "future_evaluation_and_diagnostic_outputs":4 * 1024**3,
        "future_presentation_and_consumption_logs":4 * 1024**3,
        "future_private_logs_and_receipts":8 * 1024**3}
    return sum(native.values()) + byt5 + sum(allowances.values()), allowances


def run(binding, attempt):
    root = ArtifactRoot(binding)
    before = root.preflight()
    started = time.perf_counter()
    directory = Path("experiments/manifests/generation_2")
    output = directory / f"independent-admission.attempt{attempt:02d}.json"
    if output.exists():
        raise FileExistsError(output)
    required = {
        "external-root.attempt01.json":"PASS_STORAGE_PRIMITIVES_ONLY",
        "independent-storage.attempt01.json":"PASS_BOUNDED_STORAGE_RECONSTRUCTION",
        "independent-root-loss.attempt01.json":"PASS_BOUNDED_MECHANICAL_RECONSTRUCTION",
        "source-archives.attempt01.json":"PASS_OFFICIAL_ARCHIVES_ONLY",
        "independent-archives.attempt01.json":"PASS_INDEPENDENT_OFFICIAL_ARCHIVES",
        "parakeet-sources.attempt01.json":"PASS_SOURCE_CONSTRUCTION_ONLY",
        "corpus-freeze.attempt01.json":"PASS_COMPLETE_G2_CORPUS_PANEL_GEOMETRY_FREEZE",
        "independent-corpus.attempt01.json":"PASS_INDEPENDENT_G2_CORPUS_GEOMETRY",
        "compatibility-B100.attempt02.json":"PASS_EXACT_HISTORICAL_COMPATIBILITY",
        "compatibility-C101.attempt02.json":"PASS_EXACT_HISTORICAL_COMPATIBILITY",
        "independent-compatibility.attempt02.json":"PASS_EXACT_ARTIFACT_RECONSTRUCTION",
        "independent-native.attempt01.json":"PASS_INDEPENDENT_G2_NATIVE_QUALIFICATION",
        "archived-evaluation-B100.attempt01.json":"PASS_G2_EXPANDED_ARCHIVED_ENDPOINT_EVALUATION",
        "archived-evaluation-C101.attempt01.json":"PASS_G2_EXPANDED_ARCHIVED_ENDPOINT_EVALUATION",
        "byt5-qualification.attempt02.json":"PASS_G2_BYT5_RUNNER_100_UPDATES",
        "independent-byt5.attempt01.json":"PASS_INDEPENDENT_G2_BYT5_ACCOUNTING_STATE",
        "independent-cost.attempt01.json":"PASS_INDEPENDENT_G2_COST_RECONSTRUCTION",
        "expanded-evaluation-summary.attempt01.json":"PASS_COMPLETE_FAILURE_INCLUSIVE_QUALIFICATION_TABLES",
        "independent-evaluation.attempt01.json":"PASS_INDEPENDENT_G2_TABLE_BOOTSTRAP_RECONSTRUCTION",
        "final-full-tests.attempt01.json":"PASS"}
    records = {}
    identities = {}
    for name, status in required.items():
        path = directory / name
        record = json.loads(path.read_text())
        if record["status"] != status:
            raise ValueError("required qualification/independent prerequisite has not passed: " + name)
        records[name] = record
        identities[name] = sha256(path)
    native = records["independent-native.attempt01.json"]
    assert native["scientific_recipes_started"] == 0
    calibration_path = Path("experiments/manifests/development_calibration_consumption_generation_2.attempt03.json")
    calibration = json.loads(calibration_path.read_text())
    identities[str(calibration_path)] = sha256(calibration_path)
    assert calibration["status"] == "OBSERVED_USE_RECONSTRUCTED"
    assert calibration["calibration_unique_rows"] == calibration["student_evaluated_unique_rows"] == 1900
    repair_path = directory / "byt5-record-repair.attempt01.json"
    repair = json.loads(repair_path.read_text())
    assert repair["status"] == "PASS_MECHANICAL_PRETRAINING_RECORD_REPAIR"
    assert sha256(Path(repair["failed_receipt"])) == repair["failed_receipt_sha256"]
    assert calibration["mechanical_repair_receipt_sha256"] == sha256(repair_path)
    assert repair["completed_optimizer_updates"] == repair["successful_recorded_evaluations"] == 0
    assert calibration["unwritten_failure_reference_uses"] == repair["unwritten_failure_reference_uses"]
    assert len(repair["unwritten_failure_reference_uses"]) == 1
    extra_id = repair["unwritten_failure_reference_uses"][0]["id"]
    assert extra_id in calibration["calibration_ids"]
    assert calibration["recorded_student_neural_case_evaluations"] == 16 * 1900
    assert calibration["new_student_neural_case_evaluations"] == 16 * 1900 + 1
    assert len(calibration["evaluation_files"]) == 16
    assert all(row["completed_artifact"] and row["calibration_evaluations"] == 1900
               for row in calibration["evaluation_files"])
    assert len(calibration["per_id_student_evaluation_counts"]) == 1900
    assert calibration["per_id_student_evaluation_counts"] == {
        name:17 if name == extra_id else 16 for name in calibration["calibration_ids"]}
    assert calibration["source_recognizer_calibration_calls"] == {"unique":1804,"replay":24}
    assert calibration["fit_performed"] is False and calibration["training_use_forbidden"] is True
    assert calibration["sealed_reference_use"] is False and calibration["scientific_recipes_started"] == 0
    baseline = json.loads((directory / "baseline-tests.attempt01.json").read_text())
    assert baseline["passed"] == 379 and baseline["failed"] == baseline["skipped"] == 0
    final = records["final-full-tests.attempt01.json"]
    assert final["passed"] >= 379 and final["failed"] == final["skipped"] == 0
    decision = json.loads((directory / "decision-record.attempt01.json").read_text())
    decision_path = Path("docs/reviews/FRONTIER_POST_10M_SCIENTIFIC_DECISION_V1.md")
    assert sha256(decision_path) == decision["decision_sha256"]
    assert subprocess.run(["git","merge-base","--is-ancestor","98c061066dab728f45ceac865b6d9b75288ef624","HEAD"]).returncode == 0
    freeze = records["corpus-freeze.attempt01.json"]
    configs = []
    for recipe in freeze["recipes"]:
        path = Path(recipe["config_relative"])
        assert sha256(path) == recipe["config_sha256"]
        configs.append(json.loads(path.read_text()))
    unstarted = assert_unstarted(configs,root.path("scientific-checkpoints-v1"))
    for name in ("cost-projection.attempt01.json","storage-reforecast.attempt01.json"):
        path = directory / name
        records[name] = json.loads(path.read_text())
        identities[name] = sha256(path)
    cost = records["cost-projection.attempt01.json"]
    storage = records["storage-reforecast.attempt01.json"]
    assert cost["status"] in ("PASS_G2_COST_CEILING_ONLY","GENERATION_2_COST_BLOCKED")
    assert storage["status"] in ("PASS_G2_RETAINED_STORAGE_FORECAST","GENERATION_2_STORAGE_BLOCKED")
    remaining, allowances = reconstruct_remaining_storage(root, directory, configs)
    assert remaining == storage["calculated_remaining_conservative_bytes"]
    assert allowances == storage["assumed_future_allowances_bytes"]
    expected_high_water = storage["literal_free_bytes_for_forecast"] - storage["calculated_remaining_conservative_bytes"]
    assert expected_high_water == storage["calculated_high_water_literal_free_bytes"]
    assert storage["minimum_literal_free_bytes"] == 250*1024**3
    assert (expected_high_water >= 250*1024**3) == (storage["status"] == "PASS_G2_RETAINED_STORAGE_FORECAST")
    end = root.preflight()
    eligible = cost["within_ceiling"] and storage["status"] == "PASS_G2_RETAINED_STORAGE_FORECAST"
    disposition = ("AUTHORIZE_DEVELOPMENT_GENERATION_2_EXECUTION" if eligible else
        "GENERATION_2_STORAGE_BLOCKED" if storage["status"] == "GENERATION_2_STORAGE_BLOCKED" else "GENERATION_2_COST_BLOCKED")
    result = dict(schema="g2_independent_admission_v1",status="PASS_ARTIFACT_ADMISSION_RECONSTRUCTION",
        disposition=disposition,launch_prerequisites_pass=eligible,
        reviewed_commit=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
        inputs_sha256=identities,baseline_tests=379,final_tests=final["passed"],
        unstarted=unstarted,before=before,after=end,code_sha256=sha256(__file__),
        total_serialized_hours=cost["total_serialized_hours"],
        high_water_literal_free_bytes=expected_high_water,
        independently_reconstructed_remaining_storage_bytes=remaining,
        future_storage_allowances_classification="ASSUMED; explicit planning allowances, not a guaranteed worst-case bound",
        scientific_execution_performed=False,external_model_review_claimed=False,
        scope="read-only artifact coherence and independent prerequisite reconstruction; separate owner execution authorization still required",
        elapsed_seconds=time.perf_counter()-started)
    output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-binding",required=True)
    parser.add_argument("--attempt",type=int,required=True)
    args = parser.parse_args()
    result = run(args.artifact_binding,args.attempt)
    print(json.dumps({"status":result["status"],"disposition":result["disposition"]}),flush=True)
