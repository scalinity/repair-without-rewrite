"""Collect the six frozen endpoint decisions and descriptive learning curves."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


ROOT = Path("experiments/manifests/six_10m_probes")
FREEZE = ROOT / "campaign-freeze.attempt01.json"


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while block := stream.read(1048576):
            value.update(block)
    return value.hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def exact(value):
    return {"numerator": value.numerator, "denominator": value.denominator}


def evaluation_curve(identity, attempt, frozen, completed):
    curve = []
    for point in frozen["evaluation_endpoints"]:
        path = ROOT / f"evaluation-{identity}-update{point['update']:03d}.attempt{attempt:02d}.json"
        if not path.exists():
            if completed and point["nominal"] == 10000000:
                raise ValueError(f"missing terminal-attempt 10M evaluation: {identity}")
            earlier = [path for path in sorted(ROOT.glob(f"evaluation-{identity}-update{point['update']:03d}.attempt*.json"))
                if int(path.name.rsplit(".attempt", 1)[1].split(".")[0]) <= attempt]
            if not earlier:
                if completed:
                    raise ValueError(f"missing frozen evaluation: {identity}, {point}")
                continue
            path = earlier[-1]
        value = load(path)
        if value["recipe_id"] != identity or value["panel_sha256"] != frozen["evaluation_panel_sha256"]:
            raise ValueError(f"evaluation binding differs: {path}")
        if value["actual_endpoint"] != point:
            raise ValueError(f"evaluation endpoint differs: {path}")
        curve.append({"receipt": str(path), "receipt_sha256": digest(path), **value})
    return curve


def decision(recipe, terminal, evaluation):
    natural, generated = evaluation["natural"], evaluation["generated"]
    words = natural["reference_words"]
    if words <= 0:
        raise ValueError("natural population is empty")
    wer = Fraction(natural["output_errors"], words)
    raw = Fraction(natural["source_errors"], words)
    introduced = Fraction(natural["introduced"][1], words)
    criteria = {
        "prescribed_completion_resolved": terminal["status"] == "COMPLETED",
        "natural_WER_strictly_below_RAW": wer < raw,
        "completed_natural_repair_lower_positive": natural["completed_repair"][0] > 0,
        "completed_natural_repair_lower_support_at_least_two_groups":
            len(set(natural["repair_support_source_groups_lower"])) >= 2,
        "generated_genuine_required_repair_completed": generated["required_repair_cases_completed"] > 0,
    }
    key = (wer, introduced, -natural["completed_repair"][0],
        natural["invalid_or_incomplete"], -generated["mixed_success"],
        Fraction(str(recipe["config"]["peak_lr"])))
    return {
        "recipe_id": recipe["recipe_id"], "arm": recipe["config"]["arm"],
        "peak_lr": recipe["config"]["peak_lr"], "eligibility_criteria": criteria,
        "eligible": all(criteria.values()),
        "failed_criteria": [name for name, passed in criteria.items() if not passed],
        "rank_values": {"WER": exact(wer), "RAW_WER": exact(raw),
            "introduced_rate_upper": exact(introduced),
            "completed_natural_repair_lower": natural["completed_repair"][0],
            "natural_invalid_or_incomplete": natural["invalid_or_incomplete"],
            "generated_mixed_success": generated["mixed_success"],
            "peak_lr": exact(key[-1])},
    }, key


def collect():
    frozen = load(FREEZE)
    campaign_hash = digest(FREEZE)
    outcomes, rank_keys = [], {}
    for recipe in frozen["recipes"]:
        identity = recipe["recipe_id"]
        terminals = sorted(ROOT.glob(f"recipe-{identity}.attempt*.json"))
        if not terminals:
            raise ValueError(f"unresolved prescribed recipe: {identity}")
        if len(terminals) != 1:
            raise ValueError(f"multiple terminal receipts: {identity}")
        terminal_path = terminals[0]
        terminal = load(terminal_path)
        if terminal.get("campaign_sha256") != campaign_hash or terminal["recipe_id"] != identity:
            raise ValueError(f"campaign binding differs: {identity}")
        if terminal["initial_parameter_sha256"] != frozen["models"][recipe["config"]["arm"]]["initial_parameter_sha256"]:
            raise ValueError(f"initial state differs: {identity}")
        failures = [load(path) for path in ROOT.glob(f"failure-{identity}.attempt*.json")]
        if any(item["disposition"] != "NUMERICAL_FAILURE" or item["type"] != "FloatingPointError" for item in failures):
            raise ValueError(f"implementation defect requires campaign repair: {identity}")
        if any(item["recipe_id"] != identity for item in failures) or len({item["attempt"] for item in failures}) != len(failures):
            raise ValueError(f"failure identity or attempt uniqueness differs: {identity}")
        if any(item["attempt"] > terminal["attempt"] for item in failures):
            raise ValueError(f"failure recorded after terminal attempt: {identity}")
        if terminal["status"] != "COMPLETED":
            if terminal["status"] != "FAILED":
                raise ValueError(f"unknown terminal status: {identity}")
            if len(failures) != 2 or terminal["disposition"] != "NUMERICAL_FAILURE":
                raise ValueError(f"FAILED recipe lacks two qualifying numerical failures: {identity}")
            outcomes.append({"recipe_id": identity, "arm": recipe["config"]["arm"],
                "peak_lr": recipe["config"]["peak_lr"], "eligible": False,
                "failed_criteria": ["prescribed_completion_resolved"],
                "terminal_receipt": str(terminal_path), "terminal_sha256": digest(terminal_path),
                "status": "FAILED", "numerical_replays": 1,
                "initial_parameter_sha256": terminal["initial_parameter_sha256"],
                "learning_curve": evaluation_curve(identity, terminal["attempt"], frozen, False)})
            continue
        if terminal["endpoint"] != recipe["config"]["actual_stop_endpoint"]:
            raise ValueError(f"completed endpoint differs: {identity}")
        if terminal["checkpoints"][-1]["failure_state"] != "NONE":
            raise ValueError(f"unresolved final checkpoint failure: {identity}")
        if len(failures) > 1:
            raise ValueError(f"unresolved scientific failure: {identity}")
        if terminal["numerical_replays"] != len(failures):
            raise ValueError(f"numerical replay accounting differs: {identity}")
        attempt = terminal["attempt"]
        curve = evaluation_curve(identity, attempt, frozen, True)
        outcome, rank_keys[identity] = decision(recipe, terminal, curve[-1])
        outcome.update({"terminal_receipt": str(terminal_path), "terminal_sha256": digest(terminal_path),
            "status": terminal["status"], "initial_parameter_sha256": terminal["initial_parameter_sha256"],
            "final_parameter_sha256": terminal["final_parameter_sha256"],
            "endpoint": terminal["endpoint"], "numerical_replays": terminal["numerical_replays"],
            "recipe_wall_seconds": terminal["recipe_wall_seconds"], "learning_curve": curve})
        outcomes.append(outcome)
    arms = {}
    for arm in ("B100", "C101"):
        eligible = [item for item in outcomes if item["arm"] == arm and item["eligible"]]
        ordered = sorted(eligible, key=lambda item: rank_keys[item["recipe_id"]])
        arms[arm] = {"eligible_ranking": [item["recipe_id"] for item in ordered],
            "selected_recipe": ordered[0]["recipe_id"] if ordered else None,
            "selected_peak_lr": ordered[0]["peak_lr"] if ordered else None,
            "ineligible_recipes": [item["recipe_id"] for item in outcomes if item["arm"] == arm and not item["eligible"]]}
    eligible_arms = sum(bool(value["eligible_ranking"]) for value in arms.values())
    disposition = {2: "BOTH_ARMS_HAVE_ELIGIBLE_10M_RECIPE", 1: "FRONTIER_MODEL_REVIEW_REQUIRED",
        0: "CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE"}[eligible_arms]
    return {"schema": "six10m_endpoint_selection_v1", "campaign_sha256": campaign_hash,
        "collector_sha256": digest(Path(__file__)), "selection_endpoint_only": 10000000,
        "comparison": "Exact rational lexicographic order independently within each arm; eligible endpoints only",
        "outcomes": outcomes, "arms": arms, "disposition": disposition}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    arguments = parser.parse_args()
    result = collect()
    with arguments.receipt.open("x") as stream:
        stream.write(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"arms": result["arms"], "disposition": result["disposition"]}))
