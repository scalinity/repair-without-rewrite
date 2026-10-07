"""Independent reconstruction of seven-recipe time and its single reserve."""
import argparse
import json
import math
from pathlib import Path
import time

from src.data.g2_artifacts import ArtifactRoot, sha256


def run(binding, attempt):
    root = ArtifactRoot(binding)
    before = root.preflight()
    started = time.perf_counter()
    directory = Path("experiments/manifests/generation_2")
    output = directory / f"independent-cost.attempt{attempt:02d}.json"
    if output.exists():
        raise FileExistsError(output)
    path = directory / "cost-projection.attempt01.json"
    result = json.loads(path.read_text())
    for name, digest in result["inputs_sha256"].items():
        assert sha256(directory / name) == digest
    freeze = json.loads((directory / "corpus-freeze.attempt01.json").read_text())
    lines = []
    measured = 0.
    for data, condition in (("D0", "U8"), ("D1", "U1"), ("D1", "U8")):
        for arm in ("B100", "C101"):
            name = f"{arm}-{data}-{condition}.attempt01"
            bench = json.loads((directory / f"bench-{name}.json").read_text())
            assert bench["status"] == "PASS_G2_NATIVE_BENCH_COLD_PENDING"
            measured += bench["elapsed_seconds"]
            config = json.loads((directory / f"recipe-G2-{arm}-{data}-{condition}-seed42-lr3e-4.attempt01.json").read_text())
            assert config["status"] == "AUTHORIZED_UNSTARTED" and not config["scientific_slot_consumed"]
            panel = max(bench["initial_evaluation"]["complete_panel_wall_seconds"], bench["final_evaluation"]["complete_panel_wall_seconds"])
            diagnostic = max(bench["initial_diagnostic_greedy"]["complete_panel_wall_seconds"], bench["final_diagnostic_greedy"]["complete_panel_wall_seconds"])
            forced = max(bench["initial_diagnostic_forced"]["seconds"], bench["final_diagnostic_forced"]["seconds"])
            save_count = len({item["master_completed"] for item in config["save_endpoints"]})
            seconds = (freeze["conditions"][data]["actual_exposure"] / bench["conservative_anchors_per_second"]
                + 6 * panel + 2 * diagnostic + 2 * forced
                + save_count * max(bench["checkpoint_save_seconds"].values()) + bench["startup_seconds"])
            lines.append((config["recipe_id"], seconds))
            for kind in ("boundary", "mid"):
                cold = json.loads((directory / f"cold-{name}.{kind}.json").read_text())
                assert cold["status"] == "PASS_EXACT_G2_COLD_RESUME"
                measured += cold["elapsed_seconds"]
    byt5 = json.loads((directory / "byt5-qualification.attempt01.json").read_text())
    assert byt5["status"] == "PASS_G2_BYT5_RUNNER_100_UPDATES"
    measured += byt5["elapsed_seconds"]
    seconds = (35283 * byt5["conservative_update_seconds"]
        + 4 * max(byt5["initial_evaluation"]["complete_panel_wall_seconds"], byt5["final_evaluation"]["complete_panel_wall_seconds"])
        + 4 * max(byt5["initial_checkpoint"]["seconds"], byt5["final_checkpoint"]["seconds"]) + byt5["startup_seconds"])
    lines.append(("G2-ByT5-D1-10pass-seed42-lr3e-4", seconds))
    future = math.fsum(value for _, value in lines)
    assumed = calculated = 0.
    for item in result["shared_measured_and_assumed"]:
        record = json.loads((directory / item["receipt"]).read_text())
        if item["classification"] == "MEASURED":
            assert item["seconds"] == record[item.get("elapsed_field","elapsed_seconds")]
            measured += item["seconds"]
        elif item["classification"] == "ASSUMED":
            assert item["measured_seconds"] is None and item["seconds"] == 60
            assumed += item["seconds"]
        else:
            assert item["classification"] == "CALCULATION_FROM_FILESYSTEM_CREATION_TIMESTAMPS"
            assert item["seconds"] == record["seconds"]
            calculated += item["seconds"]
    subtotal = math.fsum((measured, future, assumed, calculated))
    reserve = subtotal / 4
    total = subtotal + reserve
    # Microsecond arithmetic reconciliation only; no scoring/model tolerance.
    expected = {row["recipe_id"]: row["total_future_seconds"] for row in result["recipes"]}
    assert set(expected) == {name for name, _ in lines}
    assert all(abs(expected[name] - value) <= 1e-6 for name, value in lines)
    assert abs(result["subtotal_seconds"] - subtotal) <= 1e-6
    assert abs(result["single_reserve_seconds"] - reserve) <= 1e-6
    assert abs(result["total_serialized_seconds"] - total) <= 1e-6
    assert result["reserve_fraction"] == .25 and result["ceiling_hours"] == 96
    status = "PASS_G2_COST_CEILING_ONLY" if total <= 345600 else "GENERATION_2_COST_BLOCKED"
    assert result["status"] == status and result["within_ceiling"] == (total <= 345600)
    review = dict(schema="g2_independent_cost_v1",status="PASS_INDEPENDENT_G2_COST_RECONSTRUCTION",
        cost_disposition=status,total_serialized_hours=total / 3600,single_reserve_fraction=.25,
        measured_seconds=measured,calculated_future_seconds=future,assumed_seconds=assumed,
        calculated_source_startup_seconds=calculated,recipes=7,cost_report_sha256=sha256(path),
        method="separate receipt reads, explicit six-cell and ByT5 formulas, fsum and quarter reserve; no cost producer imported",
        arithmetic_reconciliation_limit_seconds=1e-6,scientific_recipes_started=0,
        before=before,after=root.preflight(),code_sha256=sha256(__file__),elapsed_seconds=time.perf_counter()-started)
    output.write_text(json.dumps(review,sort_keys=True,indent=2)+"\n")
    return review


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-binding",required=True)
    parser.add_argument("--attempt",type=int,required=True)
    args = parser.parse_args()
    result = run(args.artifact_binding,args.attempt)
    print(json.dumps({"status":result["status"],"cost_disposition":result["cost_disposition"]}),flush=True)
