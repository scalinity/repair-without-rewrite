"""CPU-only reconstruction of pass milestones; no training or schedule selection."""
import argparse
import hashlib
import json
from pathlib import Path


def reconstruct(recipe):
    plan = recipe["accounting"]
    rows, passes, batch = (plan[key] for key in ("training_rows", "passes", "batch_size"))
    assert (rows, passes, batch) == (14113, 10, 4)
    assert plan["pass_boundary_flush"] is False
    total = rows * passes
    # Build the finite batch endpoints directly, without the G2 batch generator.
    endpoints = [0, *[min(start + batch, total) for start in range(0, total, batch)]]
    assert len(endpoints) - 1 == plan["optimizer_updates"] == 35283
    assert endpoints[-1] - endpoints[-2] == plan["final_batch_size"] == 2
    milestones = []
    for milestone in recipe["save_evaluate_pass_milestones"]:
        target = milestone * rows
        before = max(index for index, count in enumerate(endpoints) if count <= target)
        after = min(index for index, count in enumerate(endpoints) if count >= target)
        milestones.append({
            "passes": milestone, "nominal_presentations": target,
            "exact_optimizer_boundary": before == after,
            "preceding_update": before, "preceding_presentations": endpoints[before],
            "preceding_offset": endpoints[before] - target,
            "following_update": after, "following_presentations": endpoints[after],
            "following_offset": endpoints[after] - target,
        })
    assert [item["passes"] for item in milestones if not item["exact_optimizer_boundary"]] == [2, 5]
    return {"total_presentations": total, "optimizer_updates": len(endpoints) - 1,
            "final_batch_size": endpoints[-1] - endpoints[-2], "milestones": milestones}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--recipe", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    source = Path(args.recipe)
    result = {
        "schema": "g2_independent_byt5_milestone_geometry_v1",
        "status": "UNBOUND_INTERMEDIATE_MILESTONE_MAPPING",
        "disposition": "FRONTIER_MODEL_REVIEW_REQUIRED",
        "method": "finite integer batch endpoint enumeration; no G2 batch, model or trainer imports",
        "recipe_path": str(source),
        "recipe_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scientific_slots_consumed": 0, "model_execution_performed": False,
        "schedule_selected": False,
        **reconstruct(json.loads(source.read_text())),
    }
    with Path(args.receipt).open("x") as stream:
        json.dump(result, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "milestones": result["milestones"]}))
