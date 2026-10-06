"""Collect descriptive tables from the six prescribed runs without rescoring."""
import argparse
from collections import Counter
import json
from pathlib import Path

from benchmarks.six_10m_results import FREEZE, ROOT, collect, digest, load


def distribution(values):
    ordered = sorted(values)
    if not ordered:
        return {"count": 0, "sum": 0, "minimum": None, "median": None, "maximum": None}
    middle = len(ordered) // 2
    median = ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2
    return {"count": len(ordered), "sum": sum(ordered), "minimum": ordered[0],
        "median": median, "maximum": ordered[-1]}


def output_burden(path, arm, expected_hash, resources):
    if digest(path) != expected_hash:
        raise ValueError(f"output bytes differ: {path}")
    records = [json.loads(line) for line in path.open()]
    if len(records) != 396 or len({record["id"] for record in records}) != 396:
        raise ValueError(f"output population differs: {path}")
    populations = {}
    for population, count in (("natural", 108), ("generated", 288)):
        rows = [row for row in records if row["population"] == population]
        if len(rows) != count:
            raise ValueError(f"output denominator differs: {path}, {population}")
        scores = [row["score"] for row in rows]
        positions = sum(row["decoder_positions"] for row in rows)
        if positions != resources["by_population"][population]["positions"]:
            raise ValueError(f"decode-position sum differs: {path}, {population}")
        value = {
            "cases": count, "decoder_status_counts": dict(Counter(row["status"] for row in rows)),
            "scoring_status_counts": dict(Counter(score["scoring_status"] for score in scores)),
            "alignment_status_counts": dict(Counter(score["alignment_status"] for score in scores)),
            "source_words": distribution([score["source_words"] for score in scores]),
            "reference_words": distribution([score["reference_words"] for score in scores]),
            "output_words": distribution([score["output_words"] for score in scores]),
            "source_output_word_distance": distribution([score["source_output_word_distance"] for score in scores]),
            "empty_string_outputs": sum(row["output"] == "" for row in rows),
            "missing_outputs": sum(row["output"] is None for row in rows),
            "lexically_empty_outputs": sum(score["output_words"] == 0 for score in scores),
            "repair_bound_ambiguous_cases": sum(score["repair"][0] != score["repair"][1] for score in scores),
            "introduced_bound_ambiguous_cases": sum(score["introduced_lower"] != score["introduced_upper"] for score in scores),
            "decoder_positions": distribution([row["decoder_positions"] for row in rows]),
        }
        if arm == "B100":
            value["returned_token_ids_excluding_EOS"] = distribution([
                len(row["raw_decoder"]["token_ids"]) for row in rows])
        else:
            programs = [row["raw_decoder"].get("program") for row in rows]
            value["program_unavailable_cases"] = sum(program is None for program in programs)
            value["edit_events_for_available_programs"] = distribution([
                len(program["edits"]) for program in programs if program is not None])
        populations[population] = value
    return {"output_path": str(path), "output_sha256": expected_hash, "by_population": populations}


def update_resources(path, expected_hash, endpoint):
    if digest(path) != expected_hash:
        raise ValueError(f"update-log bytes differ: {path}")
    sums = Counter()
    peaks = Counter()
    phases = Counter()
    count = 0
    first = None
    last = None
    time_fields = ["update_wall_seconds", "native_update_wall_seconds", "reader_seconds",
        "forward_backward_seconds", "accumulation_seconds", "optimizer_seconds",
        "synchronization_seconds", "component_monitor_seconds"]
    for line in path.open():
        row = json.loads(line)
        if first is None:
            first = row
        count += 1
        if row["update"] != first["update"] + count - 1:
            raise ValueError(f"update sequence differs: {path}")
        for name in time_fields:
            sums[name] += row.get(name, 0)
        for name in ("canonical_charge", "examples", "microsteps", "source_positions", "decoder_event_positions"):
            sums[name] += row[name]
        for name in ("MLX_peak_bytes", "process_peak_rss_bytes"):
            peaks[name] = max(peaks[name], row[name])
        phases[row["phase"]] += 1
        last = row
    if last is None or last["update"] != endpoint["update"] or last["committed_canonical_exposure"] != endpoint["canonical_exposure"]:
        raise ValueError(f"update endpoint differs: {path}")
    start_exposure = first["committed_canonical_exposure"] - first["canonical_charge"]
    if sums["canonical_charge"] != endpoint["canonical_exposure"] - start_exposure:
        raise ValueError(f"exposure sum differs: {path}")
    return {"update_path": str(path), "update_sha256": expected_hash, "updates": count,
        "first_update": first["update"], "start_exposure": start_exposure,
        "whole_recipe_update_sequence_covered": first["update"] == 1 and start_exposure == 0,
        "phase_update_counts": dict(phases), "summed_observed_fields": dict(sums),
        "peak_observed_fields": dict(peaks),
        "canonical_exposures_per_native_update_wall_second": sums["canonical_charge"] / sums["native_update_wall_seconds"],
        "canonical_exposures_per_instrumented_update_wall_second": sums["canonical_charge"] / sums["update_wall_seconds"],
        "exact_accelerator_kernel_time": "UNMEASURED",
        "timing_scope": "Terminal-attempt observed host wall intervals with native synchronization; earlier attempt work is excluded; not a kernel-time trace"}


def describe():
    selection = collect()  # Refuse partial campaigns before producing comparative tables.
    outcomes = []
    for outcome in selection["outcomes"]:
        identity = outcome["recipe_id"]
        terminal = load(outcome["terminal_receipt"])
        item = {key: value for key, value in outcome.items() if key != "learning_curve"}
        item["learning_curve"] = []
        for point in outcome["learning_curve"]:
            evaluation_path = Path(point["receipt"])
            attempt = int(evaluation_path.name.rsplit(".attempt", 1)[1].split(".")[0])
            private = Path("exports/six-10m-probes") / identity / f"attempt{attempt:02d}"
            output_path = private / f"evaluation-update{point['actual_endpoint']['update']:03d}.jsonl"
            item["learning_curve"].append({**point,
                "output_burden": output_burden(output_path, outcome["arm"], point["output_sha256"], point["resources"])})
        if outcome["status"] == "COMPLETED":
            private = Path("exports/six-10m-probes") / identity / f"attempt{terminal['attempt']:02d}"
            item["training_resources"] = update_resources(private / "updates.jsonl",
                terminal["updates_sha256"], terminal["endpoint"])
        item["terminal_attempt_checkpoint_count"] = len(terminal.get("checkpoints", []))
        item["terminal_invocation_wall_seconds"] = terminal.get("recipe_wall_seconds")
        interrupted = list(ROOT.glob(f"interruption-{identity}.attempt*.json"))
        prior_attempts = terminal["attempt"] > 1 or bool(interrupted)
        item["recipe_wall_seconds"] = None if prior_attempts else terminal.get("recipe_wall_seconds")
        item["whole_recipe_wall_coverage"] = "UNAVAILABLE_REQUIRES_PRIOR_ATTEMPT_RECONCILIATION" if prior_attempts else "SINGLE_INVOCATION"
        outcomes.append(item)
    wall_missing = [item["recipe_id"] for item in outcomes if item["recipe_wall_seconds"] is None]
    wall_known = sum(item["recipe_wall_seconds"] for item in outcomes if item["recipe_wall_seconds"] is not None)
    return {"schema": "six10m_descriptive_tables_v1", "campaign_sha256": digest(FREEZE),
        "collector_sha256": digest(Path(__file__)), "selection_collector_sha256": selection["collector_sha256"],
        "evaluation_population": load(FREEZE)["evaluation_population"], "outcomes": outcomes,
        "arms": selection["arms"], "sum_serial_recipe_wall_seconds": None if wall_missing else wall_known,
        "sum_known_recipe_wall_seconds": wall_known, "recipe_wall_unavailable": wall_missing,
        "claims": {"MEASURED_RESULT": "Existing frozen evaluation and execution receipts, without new inference or scoring",
            "DESCRIPTIVE_INFERENCE": "Reserved for the result report; no decision is changed by these tables",
            "FUTURE_SCIENTIFIC_DECISION": "Separate owner-authorized frontier review after this campaign"},
        "disposition": selection["disposition"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    arguments = parser.parse_args()
    result = describe()
    with arguments.receipt.open("x") as stream:
        stream.write(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"recipes": len(result["outcomes"]), "disposition": result["disposition"]}))
