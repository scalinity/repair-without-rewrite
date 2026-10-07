"""Validate the execution binding with the retained independent integer path."""
import argparse
import json
from pathlib import Path

from benchmarks.g2_byt5_milestone_independent import reconstruct
from src.data.g2_artifacts import sha256


def review(binding_path, receipt_path):
    binding = json.loads(Path(binding_path).read_text())
    recipe_path = Path(binding["original_qualified_recipe_path"])
    decision_path = Path(binding["frontier_decision_path"])
    assert sha256(recipe_path) == binding["original_qualified_recipe_sha256"]
    assert sha256(decision_path) == binding["frontier_decision_sha256"]
    assert binding["disposition"] == "AUTHORIZE_FIRST_COMPLETED_UPDATE_AT_OR_AFTER_MILESTONE"
    geometry = reconstruct(json.loads(recipe_path.read_text()))
    labels = ["initialization",
              "2-pass nominal milestone — first completed update at/after boundary",
              "5-pass nominal milestone — first completed update at/after boundary",
              "10-pass exact endpoint"]
    assert len(binding["states"]) == len(geometry["milestones"]) == 4
    for state, point, label in zip(binding["states"], geometry["milestones"], labels):
        assert state["nominal_passes"] == point["passes"]
        assert state["nominal_presentations"] == point["nominal_presentations"]
        assert state["optimizer_update"] == point["following_update"]
        assert state["actual_presentations"] == point["following_presentations"]
        assert state["presentation_offset"] == point["following_offset"]
        assert state["label"] == label
        assert state["frontier_decision_sha256"] == binding["frontier_decision_sha256"]
        assert state["frontier_decision_commit"] == binding["frontier_decision_commit"]
        assert state["original_qualified_recipe_sha256"] == binding["original_qualified_recipe_sha256"]
        if not point["exact_optimizer_boundary"]:
            assert point["preceding_presentations"] < state["nominal_presentations"] <= state["actual_presentations"]
    result = {"schema": "g2_execution_schedule_independent_v1",
              "status": "PASS_FIRST_COMPLETED_UPDATE_BINDING",
              "binding_path": str(binding_path), "binding_sha256": sha256(binding_path),
              "recipe_sha256": sha256(recipe_path), "decision_sha256": sha256(decision_path),
              "code_sha256": sha256(__file__),
              "independent_geometry_code_sha256": sha256("benchmarks/g2_byt5_milestone_independent.py"),
              "geometry": geometry, "states": binding["states"],
              "model_execution_performed": False, "scientific_slots_consumed": 0}
    with Path(receipt_path).open("x") as stream:
        json.dump(result, stream, sort_keys=True, indent=2)
        stream.write("\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    result = review(args.binding, args.receipt)
    print(json.dumps({"status": result["status"], "states": result["states"]}))
