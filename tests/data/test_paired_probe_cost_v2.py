import copy
import pytest

from benchmarks.paired_probe_cost_v2 import project_arm


def measured_fixture():
    panels = [{"cases": 396, "decode_seconds": 396 * factor,
        "scorer_seconds": 3.96 * factor, "complete_panel_wall_seconds": 399.96 * factor + 10 * factor,
        "per_case": [{"id": str(index), "decode_seconds": factor, "scorer_seconds": .01 * factor}
            for index in range(396)]} for factor in (1, 2)]
    bench = {"warmups": 5, "timed": {"complete_updates": 100}, "sustained": {"wall_seconds": 1200},
        "no_failures": True, "probe_slots": 0, "conservative_sustained_anchors_per_second": 10000,
        "initial_evaluation": panels[0], "final_evaluation": panels[1],
        "initial_save_seconds": 3, "final_save_seconds": 2, "startup_seconds": 10}
    config = {"actual_stop_endpoint": {"canonical_exposure": 10007223}, "LR_clock": {"warmup": 200000},
        "save_endpoints": [{"update": index} for index in range(13)],
        "evaluation_endpoints": [{"update": index} for index in range(6)],
        "probe_slot_consumed": False, "recipe_status": "CONFIGURED_UNSTARTED_UNAUTHORIZED"}
    controls = [{"canonical_charge": 33000, "committed_canonical_exposure": index * 33000, "wall_seconds": 4}
        for index in range(1, 8)]
    resumes = [{"status": "PASS_EXACT_COLD_RESUME", "matched_complete_updates": 21, "load_seconds": value}
        for value in (1, 2)]
    saves = {"boundary_save_seconds": 4, "mid_save_seconds": 5}
    return bench, config, controls, resumes, saves


def test_cost_counts_actual_endpoint_once_and_prices_all_cases_saves_and_reserve():
    answer = project_arm(*measured_fixture())
    parts = answer["components_seconds"]
    assert parts["training_warmup_at_sustained_rate_seconds"] == 20
    assert parts["training_after_warmup_at_sustained_rate_seconds"] == pytest.approx(980.7223)
    assert parts["routine_atomic_saves_seconds"] == 65
    assert parts["evaluation_decode_seconds"] == 4752
    assert parts["evaluation_scorer_seconds"] == pytest.approx(47.52)
    assert parts["one_interruption_recovery_allowance_seconds"] == pytest.approx(40.3)
    assert answer["one_recipe_seconds_before_reserve"] == pytest.approx(6042.4423)
    assert answer["one_recipe_seconds_with_25_percent_reserve"] == pytest.approx(7553.052875)


def test_declared_396_case_panel_cannot_hide_duplicate_or_missing_case():
    args = measured_fixture()
    args[0]["final_evaluation"]["per_case"][-1]["id"] = "0"
    with pytest.raises(ValueError, match="frozen DEVELOPMENT cases"):
        project_arm(*args)


@pytest.mark.parametrize("problem", ("timed", "sustained", "resume", "started", "duplicate_save"))
def test_incomplete_or_mismatched_qualification_is_not_priced(problem):
    bench, config, controls, resumes, saves = measured_fixture()
    if problem == "timed":
        bench["timed"]["complete_updates"] = 99
    elif problem == "sustained":
        bench["sustained"]["wall_seconds"] = 1199
    elif problem == "resume":
        resumes[0]["matched_complete_updates"] = 20
    elif problem == "started":
        config["probe_slot_consumed"] = True
    else:
        config["save_endpoints"].append(copy.deepcopy(config["save_endpoints"][-1]))
    with pytest.raises(ValueError):
        project_arm(bench, config, controls, resumes, saves)
