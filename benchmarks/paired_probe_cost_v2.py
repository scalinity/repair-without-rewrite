"""Project six unstarted recipes from complete paired BENCH measurements."""
import argparse
import hashlib
import json
import math
from pathlib import Path


SAFE = Path("experiments/manifests/lexical_reader_v2")
PRIVATE = Path("exports/lexical-reader-v2")


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def project_arm(summary, config, controls, resume_summaries, control_summary):
    if summary["warmups"] != 5 or summary["timed"]["complete_updates"] != 100 or summary["sustained"]["wall_seconds"] < 1200:
        raise ValueError("complete BENCH is required for projection")
    if not summary["no_failures"] or summary["probe_slots"]:
        raise ValueError("failed or scientific-recipe BENCH is not eligible")
    if any(item["status"] != "PASS_EXACT_COLD_RESUME" or item["matched_complete_updates"] != 21 for item in resume_summaries):
        raise ValueError("exact cold-resume qualification is required")
    rate = summary["conservative_sustained_anchors_per_second"]
    if not math.isfinite(rate) or not rate > 0:
        raise ValueError("positive measured sustained rate required")
    exposure = config["actual_stop_endpoint"]["canonical_exposure"]
    warmup_exposure = config["LR_clock"]["warmup"]
    saves = {item["update"] for item in config["save_endpoints"]}
    evaluations = {item["update"] for item in config["evaluation_endpoints"]}
    if config["probe_slot_consumed"] or config["recipe_status"] != "CONFIGURED_UNSTARTED_UNAUTHORIZED":
        raise ValueError("future recipe must remain unstarted")
    if len(saves) != len(config["save_endpoints"]) or len(evaluations) != len(config["evaluation_endpoints"]):
        raise ValueError("duplicate whole-update endpoint")
    panels = [summary["initial_evaluation"], summary["final_evaluation"]]
    indexed = [{item["id"]: item for item in panel["per_case"]} for panel in panels]
    if any(panel["cases"] != 396 for panel in panels) or any(len(index) != 396 for index in indexed) or set(indexed[0]) != set(indexed[1]):
        raise ValueError("all frozen DEVELOPMENT cases must be retained")
    decode_envelope = sum(max(index[id_]["decode_seconds"] for index in indexed) for id_ in indexed[0])
    scorer_envelope = sum(max(index[id_]["scorer_seconds"] for index in indexed) for id_ in indexed[0])
    panel_overhead = max(max(0., panel["complete_panel_wall_seconds"] - panel["decode_seconds"] - panel["scorer_seconds"])
        for panel in panels)
    save_cost = max(summary["initial_save_seconds"], summary["final_save_seconds"],
        control_summary["boundary_save_seconds"], control_summary["mid_save_seconds"])
    load_cost = max(item["load_seconds"] for item in resume_summaries)
    initial_controls = []
    for item in controls:
        initial_controls.append(item)
        if item["committed_canonical_exposure"] >= warmup_exposure:
            break
    if not initial_controls or initial_controls[-1]["committed_canonical_exposure"] < warmup_exposure:
        raise ValueError("measured initial warmup control missing")
    warmup_endpoint = initial_controls[-1]["committed_canonical_exposure"]
    cold_start_excess = max(0., sum(item["wall_seconds"] for item in initial_controls) - warmup_endpoint / rate)
    components = {
        "training_warmup_at_sustained_rate_seconds": warmup_exposure / rate,
        "training_after_warmup_at_sustained_rate_seconds": (exposure - warmup_exposure) / rate,
        "measured_initial_control_excess_seconds": cold_start_excess,
        "routine_atomic_saves_seconds": len(saves) * save_cost,
        "initial_load_seconds": load_cost,
        "evaluation_decode_seconds": len(evaluations) * decode_envelope,
        "evaluation_scorer_seconds": len(evaluations) * scorer_envelope,
        "evaluation_panel_overhead_seconds": len(evaluations) * panel_overhead,
        "reader_data_model_startup_seconds": summary["startup_seconds"],
        "one_interruption_recovery_allowance_seconds": save_cost + load_cost +
            max(item["canonical_charge"] for item in controls) / rate + 30.,
    }
    return {"actual_exposure": exposure, "conservative_sustained_anchors_per_second": rate,
        "save_endpoints": len(saves), "evaluation_endpoints": len(evaluations), "evaluation_cases": 396,
        "measured_save_seconds_per_endpoint": save_cost, "measured_load_seconds": load_cost,
        "measured_decode_envelope_seconds_per_panel": decode_envelope,
        "measured_scorer_envelope_seconds_per_panel": scorer_envelope,
        "measured_panel_overhead_seconds": panel_overhead,
        "components_seconds": components, "one_recipe_seconds_before_reserve": sum(components.values()),
        "one_recipe_seconds_with_25_percent_reserve": 1.25 * sum(components.values())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempt", type=int, required=True)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error("positive completed qualification attempt required")
    projections, identities = {}, {}
    def read(path):
        identities[str(path)] = sha(path)
        return json.loads(Path(path).read_text())
    for arm in ("B100", "C101"):
        bench_root = PRIVATE / f"bench-{arm}-attempt{args.attempt:02d}"
        control_root = PRIVATE / f"resume-{arm}-control-attempt{args.attempt:02d}"
        summary = read(bench_root / "summary.json")
        control_meta = read(control_root / "control-complete.json")
        first = read(control_root / "first-complete-update.json")
        path = control_root / "controls.jsonl"
        identities[str(path)] = sha(path)
        controls = [first, *[json.loads(line) for line in path.read_text().splitlines()]]
        resumes = [read(PRIVATE / f"resume-{arm}-{kind}-cold-attempt{args.attempt:02d}/summary.json")
            for kind in ("boundary", "mid")]
        config = read(SAFE / f"pilot-{arm}-seed42-lr3e-04.json")
        projections[arm] = project_arm(summary, config, controls, resumes, control_meta)
    profile = read(SAFE / "lexical-profile-measurement.attempt01.json")
    generated = read(SAFE / "generated-pool-qualification.attempt02.json")
    reader = read(SAFE / "mixed-reader-dry-run.attempt02.json")
    preparation = read(SAFE / "panel-preparation-timing.attempt01.json")
    shared = {"profile_measurement_seconds": profile["measurement_wall_seconds"],
        "generated_accepted_pool_seconds": generated["wall_seconds"],
        "full_10M_CPU_ledger_seconds": reader["wall_seconds"],
        "frozen_DEVELOPMENT_panel_construction_seconds": preparation["wall_seconds"]}
    total = 3 * sum(item["one_recipe_seconds_before_reserve"] for item in projections.values()) + sum(shared.values())
    output = {"scope": "SERIALIZED_M5_PRO_SIX_FUTURE_DEVELOPMENT_RECIPES_NOT_FINAL_PAPER_FORECAST",
        "qualification_attempt": args.attempt, "per_arm": projections, "shared_one_time_components_seconds": shared,
        "all_six_seconds_before_reserve": total, "reserve_fraction": .25,
        "all_six_seconds_with_25_percent_reserve": 1.25 * total,
        "MEASURED": ["complete BENCH pipeline and conservative sustained rates", "initial/final396-case decode and scorer timings",
            "atomic save/readback and cold loads", "startup and frozen pool/profile/ledger/panel construction",
            "initial control warmup timing including diagnostic hashing"],
        "CALCULATED": ["actual whole-update10M endpoint divided by sustained rate", "13deduplicated saves and6evaluation endpoints per recipe",
            "one-B and one-C component sums", "three recipes per arm plus shared costs, then25% reserve"],
        "ASSUMED": ["sustained and per-case initial/final decode timing envelopes apply to all three LR recipes",
            "one planned interruption per recipe with a successful atomic save/load, one complete update replay,30seconds restart allowance",
            "scratch shared construction is repeated once even when frozen private artifacts are already present",
            "one initial load charged conservatively although seed42 recipes start fresh"],
        "UNPRICED": ["unmeasured decode-latency changes at future intermediate checkpoints beyond the observed envelope",
            "additional interruptions or unsaved crash recovery beyond the one-update allowance", "final150M training, baselines, sealed evaluation and paper production"],
        "warmup_accounting": "200k LR warmup is included in recipe exposure; five BENCH warmups are not added as extra training",
        "reader_accounting": "native reader/pack/capture costs are included in sustained pipeline; scratch CPU construction is shared once",
        "identities": identities, "six_probe_slots_consumed": 0, "paper_protocol_v2_frozen": False}
    path = SAFE / f"six-probe-cost-projection.attempt{args.attempt:02d}.json"
    if path.exists():
        raise FileExistsError(path)
    path.write_text(json.dumps(output, sort_keys=True, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"all_six_hours_with_reserve": 1.25 * total / 3600,
        "one_recipe_hours_before_reserve": {arm: item["one_recipe_seconds_before_reserve"] / 3600
            for arm, item in projections.items()}, "six_probe_slots_consumed": 0}))


if __name__ == "__main__":
    main()
