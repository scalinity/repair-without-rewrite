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
        "byt5-qualification.attempt01.json":"PASS_G2_BYT5_RUNNER_100_UPDATES",
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
