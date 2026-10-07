"""CPU-only execution prerequisite reconstruction without the launcher."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import time

from benchmarks.g2_admission_independent import reconstruct_remaining_storage
from benchmarks.g2_byt5_milestone_independent import reconstruct
from src.data.g2_artifacts import ArtifactRoot, sha256


def run(binding, attempt):
    root = ArtifactRoot(binding); started = time.perf_counter()
    directory = Path("experiments/manifests/generation_2")
    receipt = directory / f"execution-launcher-independent.attempt{attempt:02d}.json"
    if receipt.exists(): raise FileExistsError(receipt)
    qualified = "2c27cff28a31ae64220df9b06094a914e94dd0f3"
    before = root.preflight(); preserved = []
    originals = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", qualified], text=True).splitlines()
    for name in originals:
        if (name.startswith(("src/", "configs/", "tests/")) or name in ("uv.lock", "pyproject.toml",
                "benchmarks/g2_native_qualification.py", "benchmarks/paired_qualification_v3.py", "benchmarks/six_10m_campaign.py")
                or name.startswith("experiments/manifests/generation_2/recipe-")):
            if Path(name).read_bytes() != subprocess.check_output(["git", "show", f"{qualified}:{name}"]):
                raise ValueError("qualified scientific function/configuration/test changed")
            preserved.append(name)
    corpus = json.loads((directory / "corpus-freeze.attempt01.json").read_text())
    files = {}
    for condition in corpus["conditions"].values():
        physical = root.path(condition["artifact_relative"])
        completion = json.loads((physical / "COMPLETE.json").read_text())
        for name, identity in completion["files"].items():
            path = physical / name
            if path.stat().st_size != identity["bytes"] or sha256(path) != identity["sha256"]:
                raise ValueError("independent corpus payload reconstruction failed")
            files[str(path.relative_to(root.root))] = identity["sha256"]
        for name, key in (("natural.jsonl", "natural_sha256"), ("presentations.jsonl", "ledger_sha256"),
                          ("masters.json", "masters_sha256"), ("actual-updates.json", "actual_updates_sha256"),
                          ("diagnostics.json", "diagnostics_sha256")):
            if files[f"{condition['artifact_relative']}/{name}"] != condition[key]:
                raise ValueError("independent qualified corpus identity failed")
    panel = root.path(corpus["panel_relative"]) / "panel.json"
    if sha256(panel) != corpus["panel_sha256"]: raise ValueError("DEVELOPMENT panel changed")
    rows = json.loads(panel.read_text())
    if len(rows) != 2984 or sum(r["population"] == "natural" for r in rows) != 2696:
        raise ValueError("frozen evaluation population changed")
    recipes = [json.loads((directory / row["config_relative"].split("/")[-1]).read_text()) for row in corpus["recipes"]]
    if any(row["status"] != "AUTHORIZED_UNSTARTED" or row["scientific_slot_consumed"] for row in recipes):
        raise ValueError("a scientific recipe started before freeze")
    for area in ("scientific-checkpoints-v1", "evaluation-v1", "byt5-v1"):
        path = root.path(area)
        if path.exists() and (any(path.iterdir()) if area == "scientific-checkpoints-v1" else any(path.glob("scientific-*"))):
            raise ValueError("scientific trajectory exists before campaign freeze")
    if list(directory.glob("scientific-start-*.json")): raise ValueError("a scientific slot is consumed")
    schedule = json.loads((directory / "byt5-execution-schedule.attempt01.json").read_text())
    exact = [(0, 0, 0, 0), (28226, 7057, 28228, 2), (70565, 17642, 70568, 3), (141130, 35283, 141130, 0)]
    actual = [(r["nominal_presentations"], r["optimizer_update"], r["actual_presentations"], r["presentation_offset"]) for r in schedule["states"]]
    if actual != exact: raise ValueError("frontier completed-state schedule differs")
    independent = reconstruct(next(row for row in recipes if row["recipe_id"].startswith("G2-ByT5-")))
    remaining, allowances = reconstruct_remaining_storage(root, directory, recipes)
    forecast = json.loads((directory / "storage-reforecast.attempt03.json").read_text())
    if remaining != forecast["calculated_remaining_conservative_bytes"] or allowances != forecast["assumed_future_allowances_bytes"]:
        raise ValueError("independent storage projection differs")
    after = root.preflight(); free = min(before["literal_free_bytes"], after["literal_free_bytes"])
    if free - remaining < 250 * 1024**3: raise ValueError("independent live high-water storage floor fails")
    sources = {}
    for name in ("benchmarks/g2_scientific_campaign.py", "benchmarks/g2_scientific_byt5.py", "benchmarks/g2_scientific_serial.py"):
        tree = ast.parse(Path(name).read_text())
        # Model/trainer/generator calls remain inside functions, beyond the published-freeze guard.
        for node in tree.body:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                raise ValueError("launcher imports execute a module-level call")
        sources[name] = sha256(name)
    result = {"schema": "g2_execution_prerequisite_independent_v1", "status": "PASS_INDEPENDENT_EXECUTION_PREREQUISITES",
              "reviewed_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
              "preserved_qualified_paths": preserved, "corpus_payload_hashes": files, "panel_sha256": sha256(panel),
              "launcher_source_hashes": sources, "milestones": exact, "independent_milestone_reconstruction": independent,
              "remaining_conservative_bytes": remaining, "live_high_water_free_bytes": free - remaining,
              "recipes": 7, "recipe_status": "AUTHORIZED_UNSTARTED", "scientific_slots_consumed": 0,
              "model_execution_performed": False, "before": before, "after": after,
              "elapsed_seconds": time.perf_counter() - started}
    with receipt.open("x") as stream: json.dump(result, stream, sort_keys=True); stream.write("\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--artifact-binding", required=True)
    parser.add_argument("--attempt", type=int, required=True); args = parser.parse_args()
    result = run(args.artifact_binding, args.attempt)
    print(json.dumps({"status": result["status"], "elapsed_seconds": result["elapsed_seconds"]}))
