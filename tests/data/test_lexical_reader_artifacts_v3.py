import hashlib
import json
from pathlib import Path

from benchmarks.paired_qualification_v3 import BenchStream


ROOT = Path(__file__).resolve().parents[2]
SAFE = ROOT / "experiments/manifests/lexical_reader_v2"


def data(name):
    return json.loads((SAFE / name).read_text())


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def test_complete_generated_pool_and_independent_inversion_receipt():
    measured = data("generated-pool-qualification.attempt02.json")
    reviewed = data("independent-pool-validation.attempt02.json")
    assert measured["base_count"] == 8404
    assert measured["accepted_variant_count"] == reviewed["accepted_rows_checked"] == 42020
    assert len(measured["required_strata"]) == 160
    assert all(stratum["accepted"] > 0 for stratum in measured["required_strata"])
    assert not measured["empty_required_strata"] and not measured["scientific_stop_triggered"]
    assert reviewed["status"] == "PASS" and not reviewed["comparison_failures"]
    assert measured["accepted_pool_sha256"] == reviewed["pool_sha256"] == sha(
        ROOT / "exports/lexical-reader-v2/generated-pool-attempt02/accepted.jsonl")


def test_full_dry_run_complete_queues_and_exact_ledger_parity_after_resume_additions():
    old, actual = data("mixed-reader-dry-run.attempt01.json"), data("mixed-reader-dry-run.attempt02.json")
    review = data("independent-reader-validation.attempt03.json")
    assert actual["ledger_sha256"] == old["ledger_sha256"] == review["ledger_sha256"] == sha(
        ROOT / "exports/lexical-reader-v2/mixed-reader-attempt02/presentations.jsonl")
    assert actual["canonical_exposure"] == review["canonical_exposure"] == 10007223
    assert actual["presentations"] == review["presentations_checked"] == 134591
    assert not actual["scientific_stop_triggered"] and not review["scientific_stop"]
    assert actual["realized_edit_concentration"] == review["concentration"]
    updates = data("mixed-reader-update-index.attempt02.json")
    assert len(updates) == actual["complete_updates"] == 305
    next_ordinal = 0
    for update in updates:
        assert update["first_ordinal"] == next_ordinal
        assert 32768 <= update["canonical_charge"] < 32768 + 2048
        assert update["examples"] == update["last_ordinal"] - update["first_ordinal"] + 1
        assert update["B_denominator"] > 0 and update["C_denominators"]["action"] > 0
        next_ordinal = update["last_ordinal"] + 1
    assert next_ordinal == actual["presentations"]


def test_six_configs_share_exact_endpoints_and_do_not_launch_slots():
    prepared = data("pilot-preparation.attempt01.json")
    assert len(prepared["recipes"]) == 6 and prepared["six_probe_slots_consumed"] == 0
    endpoints = []
    for recipe in prepared["recipes"]:
        path = ROOT / recipe["config_path"]
        assert sha(path) == recipe["config_sha256"]
        config = json.loads(path.read_text())
        assert config["seed"] == 42 and config["peak_lr"] in (1e-4, 3e-4, 6e-4)
        assert config["update_target"] == 32768
        assert config["phase_nominal_exposures"] == [6666667, 2666667, 666666]
        assert config["LR_clock"]["warmup"] == 200000 and config["LR_clock"]["floor_fraction"] == .1
        assert config["recipe_status"] == "CONFIGURED_UNSTARTED_UNAUTHORIZED"
        assert not config["probe_slot_consumed"]
        endpoints.append((config["actual_stop_endpoint"], config["save_endpoints"], config["evaluation_endpoints"]))
    assert all(endpoint == endpoints[0] for endpoint in endpoints)
    assert prepared["panel"]["total_cases"] == prepared["panel"]["native_admitted"] == 396
    assert len(prepared["panel"]["calibration_consumed_ids"]) == 96


def test_benchmark_sampler_balances_pilot_phases_without_changing_common_queues():
    updates = data("mixed-reader-update-index.attempt02.json")
    one, two = BenchStream(updates), BenchStream(updates)
    assert [one.next()[0] for _ in range(105)] == [two.next()[0] for _ in range(105)]
    max_charge = max(update["canonical_charge"] for update in updates)
    for phase, weight in one.weights.items():
        assert abs(one.charges[phase] - weight / 10_000_000 * one.total) <= 3 * max_charge
    assert set(one.charges) == {"P0", "P1", "P2"}
