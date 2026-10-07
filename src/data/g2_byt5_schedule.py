"""Prospectively authorized observations of the unchanged ByT5 training stream."""

LABELS = {
    0: "initialization",
    2: "2-pass nominal milestone — first completed update at/after boundary",
    5: "5-pass nominal milestone — first completed update at/after boundary",
    10: "10-pass exact endpoint",
}


def milestone_states(recipe):
    plan = recipe["accounting"]
    required = {"training_rows": 14113, "passes": 10, "batch_size": 4,
                "presentations": 141130, "optimizer_updates": 35283,
                "final_batch_size": 2, "pass_boundary_flush": False}
    if any(plan.get(key) != value for key, value in required.items()):
        raise ValueError("qualified continuous ByT5 training extent changed")
    if recipe["save_evaluate_pass_milestones"] != [0, 2, 5, 10]:
        raise ValueError("exactly four authorized ByT5 observations required")
    states = []
    for passes, label in LABELS.items():
        nominal = passes * plan["training_rows"]
        update = (nominal + plan["batch_size"] - 1) // plan["batch_size"]
        actual = min(update * plan["batch_size"], plan["presentations"])
        states.append({"nominal_passes": passes, "nominal_presentations": nominal,
                       "optimizer_update": update, "actual_presentations": actual,
                       "presentation_offset": actual - nominal, "label": label})
    return states


def validate_states(recipe, states):
    fields = ("nominal_passes", "nominal_presentations", "optimizer_update",
              "actual_presentations", "presentation_offset", "label")
    if [{key: state[key] for key in fields} for state in states] != milestone_states(recipe):
        raise ValueError("ByT5 observation differs from the frontier milestone binding")
