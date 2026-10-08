from fractions import Fraction

import pytest

from benchmarks.g2_scientific_results import factorial, factorial_intervals, natural_summary, viability
from src.scoring.records import Output, prepare_source, score_output
from benchmarks.g2_scientific_accounting_independent import byt5_update, incorporate
from benchmarks.g2_scientific_results_independent import verify_bootstrap
from src.scoring.g2_bootstrap import paired_group_intervals


def test_failure_inclusive_repairs_and_variable_population_coverage():
    panel = {"repaired": {"source": "red green", "source_group_id": "g1"},
             "capped": {"source": "red green", "source_group_id": "g2"},
             "missing": {"source": "red green", "source_group_id": "g3"}}
    prepared = prepare_source("red blue", "red green")
    rows = [{"id": key, "output": output.text, "status": output.status,
             "score": score_output(prepared, output)} for key, output in (
        ("repaired", Output("red blue")), ("capped", Output("red blue", "capped")),
        ("missing", Output(None, "missing")))]
    result = natural_summary(rows, panel)
    assert result["cases"] == 3 and result["invalid_or_incomplete"] == 2
    assert result["completed_repair"] == (1, 1)
    assert result["repair_support_source_groups_lower"] == ["g1"]
    coverage = result["source_correct_preservation_coverage"]
    assert coverage["covered_cases"] + coverage["unavailable_cases"] == 3
    assert result["status_counts"] == {"complete": 1, "capped": 1, "missing": 1}


def test_factorial_exact_contrasts_keep_both_interventions_and_interaction():
    values = {"D0-U1": Fraction(1, 2), "D0-U8": Fraction(1, 3),
              "D1-U1": Fraction(1, 4), "D1-U8": Fraction(1, 8)}
    result = factorial(values)
    assert result["D1_effect_at_U1"] == Fraction(-1, 4)
    assert result["U8_effect_at_D0"] == Fraction(-1, 6)
    assert result["U8_effect_at_D1"] == Fraction(-1, 8)
    assert result["difference_in_differences"] == Fraction(1, 24)


def test_factorial_bootstrap_shares_registered_draws_and_constant_ratios():
    groups = [str(i) for i in range(52)]
    cells = {cell: cell for cell in ("D0-U1", "D0-U8", "D1-U1", "D1-U8")}
    totals = {cell: {group: [count, 16] for group in groups}
              for cell, count in zip(cells, (8, 4, 6, 1))}
    result = factorial_intervals(groups, cells, totals)
    assert result["draws"] == 10000 and result["eligibility_affected"] is False
    assert result["intervals"]["difference_in_differences"] == [-1/16, -1/16]
    assert result["intervals"]["D1_effect_at_U1"] == [-2/16, -2/16]
    with pytest.raises(ValueError): factorial_intervals(groups[:-1], cells, totals)
    totals["D0-U1"][groups[0]] = [-1, 16]
    with pytest.raises(ValueError): factorial_intervals(groups, cells, totals)


def test_viability_requires_completed_endpoint_and_two_groups_without_bootstrap_gate():
    summary = {"natural": {"output_errors": 1, "source_errors": 2, "completed_repair": [1, 1],
                           "repair_support_source_groups_lower": ["g1", "g2"]},
               "generated": {"required_repair_cases_completed": 1}}
    assert viability({"status": "COMPLETED"}, summary)["viable"]
    assert not viability({"status": "FAILED_NUMERICAL"}, summary)["viable"]
    summary["generated"]["required_repair_cases_completed"] = 0
    assert not viability({"status": "COMPLETED"}, summary)["viable"]
    assert viability({"status": "COMPLETED"}, summary, byt5=True)["viable"]
    summary["natural"]["repair_support_source_groups_lower"] = ["g1"]
    assert not viability({"status": "COMPLETED"}, summary, byt5=True)["viable"]


@pytest.mark.parametrize("step,size", [(7057, 4), (17642, 4), (35283, 2)])
def test_independent_accounting_reconstructs_crossing_batches_and_final_pair(step, size):
    ordering = [str(i) for i in range(14113)]
    first, last = (step-1)*4, min(step*4, 141130)
    row = {"update": step, "actual_presentations": last, "lr": 3e-4,
           "ids": [ordering[i % 14113] for i in range(first, last)],
           "presentations": [{"presentation": i, "pass_index": i//14113, "pass_offset": i%14113} for i in range(first, last)],
           "native_source": 10, "native_targets": 10, "loss": 1., "gradient_norm": 1.}
    assert len(row["ids"]) == size and len(byt5_update(row, ordering)) == 64
    row["actual_presentations"] -= 1
    with pytest.raises(ValueError): byt5_update(row, ordering)


def test_identical_replay_deduplicates_scientific_extent_and_rejects_changed_identity():
    unique = {}
    incorporate(unique, 1, "identity"); incorporate(unique, 1, "identity")
    assert len(unique) == 1
    with pytest.raises(ValueError): incorporate(unique, 1, "changed")


def test_integer_multiplicity_review_matches_shared_draws_and_detects_changed_interval():
    groups = [str(i) for i in range(52)]
    names = ["archived-B100-D0-U1", "d0-u8", "d1-u1", "d1-u8"]
    cells = dict(zip(("D0-U1", "D0-U8", "D1-U1", "D1-U8"), names))
    totals = {name: {group: [index+int(group)%5, 20+int(group)%3] for group in groups}
              for index, name in enumerate(names)}
    tables = {name: {"WER": value, "completed_repair_lower": {group: [0, 5] for group in groups}}
              for name, value in totals.items()}
    baseline = {group: [5, totals[names[0]][group][1]] for group in groups}
    bootstrap = paired_group_intervals(groups, {**totals, "RAW": baseline})
    values = {cell: Fraction(sum(v[0] for v in totals[name].values()), sum(v[1] for v in totals[name].values())) for cell, name in cells.items()}
    exact = {key: {"numerator": value.numerator, "denominator": value.denominator, "value": float(value)} for key, value in factorial(values).items()}
    report = {"paired_group_bootstrap": {"WER": bootstrap}, "factorial_analysis": {"B100": {"cells": cells,
              "effects": {"WER": {"exact_effects": exact, "paired_group_bootstrap": factorial_intervals(groups, cells, totals)}}}}}
    assert verify_bootstrap(tables, report) == bootstrap["draw_indices_int64_sha256"]
    bootstrap["intervals"][names[0]][0] += .01
    with pytest.raises(ValueError): verify_bootstrap(tables, report)
