"""CPU-only independent G2 output/count/contrast reconstruction.

This path does not import the scientific launcher, summary producer, model,
trainer or bootstrap implementation. All prescribed outcomes are required.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import time

from benchmarks.six_10m_metrics_independent import integer_distance, generated_fields, normalized, STATUS_MAP
from src.data.g2_artifacts import ArtifactRoot, read_complete, sha256
from src.scoring.records import Output, prepare_source, score_output
from src.scoring.text import lexical

BASE = Path("experiments/manifests/generation_2")


def require(condition, message):
    if not condition: raise ValueError(message)


def natural_counts(rows, panel):
    scores = [row["score"] for row in rows]
    result = {"cases": len(rows), "reference_words": sum(s["reference_words"] for s in scores),
        "source_errors": sum(s["eS"] for s in scores), "output_errors": sum(s["eO"] for s in scores),
        "invalid_or_incomplete": sum(not s["complete_valid"] for s in scores),
        "status_counts": dict(Counter(row["status"] for row in rows)),
        "source_byte_identity": sum(row["score"]["complete_valid"] and row["output"] == panel[row["id"]]["source"] for row in rows),
        "source_lexical_identity": sum(row["score"]["complete_valid"] and lexical(row["output"]) == lexical(panel[row["id"]]["source"]) for row in rows),
        "target_byte_exact": sum(s["raw_byte_exact"] for s in scores), "target_lexical_exact": sum(s["lexical_exact"] for s in scores)}
    require(result["reference_words"] > 0, "empty or undefined natural population")
    for key in ("repair", "introduced", "completed_repair"):
        result[key] = [sum(s[key][index] for s in scores) for index in (0, 1)]
    result["wer"] = result["output_errors"]/result["reference_words"]
    result["RAW_WER"] = result["source_errors"]/result["reference_words"]
    result["introduced_rate"] = [n/result["reference_words"] for n in result["introduced"]]
    result["completed_repair_rate"] = [n/result["source_errors"] for n in result["completed_repair"]] if result["source_errors"] else None
    for index, name in enumerate(("lower", "upper")):
        result["repair_support_source_groups_"+name] = sorted({panel[row["id"]]["source_group_id"] for row in rows if row["score"]["completed_repair"][index] > 0})
    covered = [s for s in scores if s["fixed_correct_damage"] is not None]
    correct = sum((s["source_consensus_eligible_counts"] or {}).get("correct", 0) for s in covered)
    damage = [sum(s["fixed_correct_damage"][index] for s in covered) for index in (0, 1)]
    result["source_correct_damage_bounds"] = damage if len(covered) == len(scores) else None
    result["source_correct_preservation_coverage"] = {"covered_cases": len(covered), "unavailable_cases": len(scores)-len(covered),
        "covered_correct_counts": correct, "covered_damage_bounds": damage, "covered_preserved_bounds": [correct-damage[1], correct-damage[0]]}
    return result


def verify_table(records, table, panel, latents, prepared):
    rows = [{**row, "output": row["decoded"]["text"]} if "decoded" in row else row for row in records]
    require(len(rows) == len({row["id"] for row in rows}) == 2984 and {row["id"] for row in rows} == set(panel), "failure-inclusive complete panel required")
    subsets = defaultdict(list); groups = defaultdict(lambda: [0]*7)
    generated = {"cases": 288, "complete": 0, "structure_invalid": 0, "invalid_or_incomplete": 0,
        "required_repair_fields_completed": 0, "required_repair_cases_completed": 0,
        "whole_case_conformance": 0, "mixed_success": 0, "by_view": {}, "by_category_view": {}}
    for row in rows:
        item = panel[row["id"]]
        source = prepared.setdefault(row["id"], None)
        if source is None:
            source = prepared[row["id"]] = prepare_source(item["target"], item["source"])
        rescored = score_output(source, Output(row["output"], STATUS_MAP.get(row["status"], row["status"])))
        require(normalized(rescored) == row["score"], "retained canonical score differs from re-scoring")
        observed = row["output"] if rescored["failure_reason"] in (None, "capped", "timeout_prefix") else ""
        require(integer_distance(lexical(item["target"]), lexical(observed)) == rescored["eO"], "independent two-row output distance differs")
        require(integer_distance(lexical(item["target"]), lexical(item["source"])) == rescored["eS"], "independent two-row source distance differs")
        if item["population"] == "natural":
            for name in ("natural_all", "legacy108" if item["legacy_subset"] else "new2588", item["role"], item["official_split"],
                         "natural-other" if "other" in item["official_split"] else "natural-clean"):
                subsets[name].append(row)
            values = [rescored["eO"], rescored["reference_words"], rescored["eS"], *rescored["completed_repair"], *rescored["introduced"]]
            for index, value in enumerate(values): groups[item["source_group_id"]][index] += value
        else:
            latent = latents[row["id"]]; field = generated_fields(latent, row["output"], rescored["complete_valid"])
            invalid = not (field["complete"] and field["structure_valid"])
            for key, value in (("complete", field["complete"]), ("structure_invalid", not field["structure_valid"]),
                ("invalid_or_incomplete", invalid), ("required_repair_fields_completed", field["repaired_fields"]),
                ("required_repair_cases_completed", field["repaired_fields"] > 0), ("whole_case_conformance", field["whole_case_conformance"]),
                ("mixed_success", field["mixed_success"])): generated[key] += value
            for mapping, name in ((generated["by_view"], latent["view_kind"]), (generated["by_category_view"], latent["primary_category"]+":"+latent["view_kind"])):
                counts = mapping.setdefault(name, {"cases": 0, "complete": 0, "invalid_or_incomplete": 0, "status_counts": {},
                    "conformant": 0, "preserved_fields": 0, "preserve_denominator": 0, "repaired_fields": 0, "repair_denominator": 0})
                counts["cases"] += 1; counts["complete"] += field["complete"]; counts["invalid_or_incomplete"] += invalid
                counts["conformant"] += field["whole_case_conformance"]
                counts["status_counts"][row["status"]] = counts["status_counts"].get(row["status"], 0)+1
                for key in ("preserved_fields", "preserve_denominator", "repaired_fields", "repair_denominator"): counts[key] += field[key]
    require(set(subsets) == set(table["natural_subsets"]), "natural subgroup membership changed")
    for name, values in subsets.items(): require(natural_counts(values, panel) == table["natural_subsets"][name], "natural subgroup integer ledger differs")
    require(table["natural"] == table["natural_subsets"]["natural_all"], "full natural ledger differs")
    generated["decoder_invalid_or_incomplete"] = 288-generated["complete"]
    require(generated == table["generated"], "independent full-consumption generated parse/count differs")
    metrics = {}
    for name, numerator, denominator in (("WER", 0, 1), ("completed_repair_lower", 3, 2), ("completed_repair_upper", 4, 2), ("introduced_lower", 5, 1), ("introduced_upper", 6, 1)):
        metrics[name] = {group: [counts[numerator], counts[denominator]] for group, counts in groups.items()}
    require(metrics == table["group_metric_totals"], "source-group integer ledger differs")
    return metrics


def verify_bootstrap(tables, report):
    import numpy as np
    groups = report["paired_group_bootstrap"]["WER"]["group_order"]
    require(len(groups) == len(set(groups)) == 52, "complete frozen source groups required")
    draws = np.random.Generator(np.random.PCG64(42)).integers(0, 52, size=(10000, 52))
    multiplicities = np.stack([np.bincount(draw, minlength=52) for draw in draws])
    digest = hashlib.sha256(draws.astype("<i8").tobytes()).hexdigest()
    for metric, expected in report["paired_group_bootstrap"].items():
        require(expected["draw_indices_int64_sha256"] == digest and expected["group_order"] == groups, "registered shared draws differ")
        values = {name: table[metric] for name, table in tables.items()}
        if metric == "WER":
            values["RAW"] = {group: [tables["archived-B100-D0-U1"]["completed_repair_lower"][group][1], tables["archived-B100-D0-U1"]["WER"][group][1]] for group in groups}
        samples = {}
        for name, totals in values.items():
            counts = multiplicities @ np.asarray([totals[group] for group in groups], dtype=np.int64)
            require((counts[:, 1] > 0).all(), "undefined bootstrap draw")
            samples[name] = counts[:, 0]/counts[:, 1]
            require(np.percentile(samples[name], [2.5, 97.5]).tolist() == expected["intervals"][name], "integer multiplicity interval differs")
        require(set(samples) == set(expected["intervals"]), "bootstrap table membership differs")
        contrasts = expected["paired_difference_intervals"]
        require(len(contrasts) == len(samples)*(len(samples)-1)//2, "paired contrast missing")
        pairs = set()
        for name, interval in contrasts.items():
            left, right = name.split(" minus "); require(left != right, "self contrast")
            pairs.add(frozenset((left, right)))
            require(np.percentile(samples[left]-samples[right], [2.5, 97.5]).tolist() == interval, "paired difference interval differs")
        require(len(pairs) == len(contrasts), "duplicate paired contrast")
        for arm, analysis in report["factorial_analysis"].items():
            if "cells" not in analysis: continue
            cells = analysis["cells"]; a, b, c, d = [samples[cells[name]] for name in ("D0-U1", "D0-U8", "D1-U1", "D1-U8")]
            effects = {"D1_effect_at_U1": c-a, "D1_effect_at_U8": d-b, "U8_effect_at_D0": b-a, "U8_effect_at_D1": d-c, "difference_in_differences": d-c-b+a}
            expected_effect = analysis["effects"][metric]
            require(expected_effect["paired_group_bootstrap"]["draw_indices_int64_sha256"] == digest, "factorial draws differ")
            for name, values in effects.items():
                # Match the registered parenthesized arithmetic without changing counts.
                if name == "difference_in_differences": values = (d-c)-(b-a)
                require(np.percentile(values, [2.5, 97.5]).tolist() == expected_effect["paired_group_bootstrap"]["intervals"][name], "factorial paired interval differs")
            rates = {}
            for cell, label in cells.items():
                totals = tables[label][metric]
                rates[cell] = Fraction(sum(v[0] for v in totals.values()), sum(v[1] for v in totals.values()))
            a, b, c, d = [rates[name] for name in ("D0-U1", "D0-U8", "D1-U1", "D1-U8")]
            exact = {"D1_effect_at_U1": c-a, "D1_effect_at_U8": d-b, "U8_effect_at_D0": b-a, "U8_effect_at_D1": d-c, "difference_in_differences": (d-c)-(b-a)}
            for name, value in exact.items(): require(expected_effect["exact_effects"][name] == {"numerator": value.numerator, "denominator": value.denominator, "value": float(value)}, "exact factorial fraction differs")
    return digest


def verify_diagnostic(greedy, forced, expected, panel):
    require(len(greedy) == len(forced) == len(panel) == 304, "complete TRAIN diagnostic required")
    require({r["id"] for r in greedy} == {r["id"] for r in forced} == set(panel), "TRAIN diagnostic IDs differ")
    groups = defaultdict(list); losses = defaultdict(lambda: defaultdict(list))
    for row in greedy:
        item = panel[row["id"]]
        rescored = score_output(prepare_source(item["target"], item["source"]), Output(row["output"], STATUS_MAP[row["status"]]))
        require(normalized(rescored) == row["score"], "TRAIN diagnostic re-scoring differs")
        groups[item["stratum"]].append(row)
    require(set(groups) == set(expected["greedy_fit_copy_by_stratum"]), "TRAIN diagnostic strata differ")
    for name, rows in groups.items():
        scores = [r["score"] for r in rows]; count = {"reference_words": sum(s["reference_words"] for s in scores),
            "source_errors": sum(s["eS"] for s in scores), "output_errors": sum(s["eO"] for s in scores),
            "invalid_or_incomplete": sum(not s["complete_valid"] for s in scores)}
        for key in ("repair", "introduced", "completed_repair"): count[key] = [sum(s[key][i] for s in scores) for i in (0, 1)]
        count["wer"] = count["output_errors"]/count["reference_words"] if count["reference_words"] else None
        count["introduced_rate"] = [v/count["reference_words"] for v in count["introduced"]] if count["reference_words"] else None
        count["completed_repair_rate"] = [v/count["source_errors"] for v in count["completed_repair"]] if count["source_errors"] else None
        fit = {"cases": len(rows), "status_counts": dict(Counter(r["status"] for r in rows)), "counts": count,
            "source_byte_identity": sum(r["score"]["complete_valid"] and r["output"] == panel[r["id"]]["source"] for r in rows),
            "source_lexical_identity": sum(r["score"]["complete_valid"] and lexical(r["output"]) == lexical(panel[r["id"]]["source"]) for r in rows),
            "target_byte_exact": sum(s["raw_byte_exact"] for s in scores), "target_lexical_exact": sum(s["lexical_exact"] for s in scores)}
        require(fit == expected["greedy_fit_copy_by_stratum"][name], "TRAIN greedy fit/copy ledger differs")
    for row in forced:
        for key, value in row["losses"].items():
            den = row["denominators"]["B"] if key == "target" else row["denominators"]["C"][key]
            require(den > 0 if value is not None else den == 0, "teacher-forced loss coverage differs")
            losses[panel[row["id"]]["stratum"]][key].append((value, den))
    require(set(losses) == set(expected["teacher_forced_components_by_stratum"]), "forced strata differ")
    for name, components in losses.items():
        require(set(components) == set(expected["teacher_forced_components_by_stratum"][name]), "forced components differ")
        for key, pairs in components.items():
            covered = [(value, den) for value, den in pairs if value is not None]; count = sum(den for _, den in covered)
            values = {"covered_cases": len(covered), "unavailable_cases": len(pairs)-len(covered), "component_denominator": count,
                "mean_of_case_losses": sum(value for value, _ in covered)/len(covered) if covered else None,
                "denominator_weighted_loss": sum(value*den for value, den in covered)/count if count else None}
            require(values == expected["teacher_forced_components_by_stratum"][name][key], "forced component arithmetic differs")
    require(expected["TRAIN_diagnostic_only"] and not expected["counts_toward_heldout_viability"], "diagnostic entered heldout gate")


def run(binding, attempt, summary_attempt):
    root = ArtifactRoot(binding); before = root.preflight(); started = time.perf_counter()
    path = BASE/f"scientific-results.attempt{summary_attempt:02d}.json"
    output = BASE/f"scientific-results-independent.attempt{attempt:02d}.json"
    if output.exists(): raise FileExistsError(output)
    report = json.loads(path.read_text()); campaign_path = BASE/"execution-campaign-freeze.attempt01.json"
    require(report["campaign_sha256"] == sha256(campaign_path), "campaign identity differs")
    campaign = json.loads(campaign_path.read_text()); corpus = json.loads(Path(campaign["corpus_freeze_path"]).read_text())
    panel_path = root.path(corpus["panel_relative"])/"panel.json"; read_complete(panel_path.parent)
    require(sha256(panel_path) == corpus["panel_sha256"], "heldout identity differs")
    panel = {row["id"]: row for row in json.loads(panel_path.read_text())}
    require(sha256(campaign["generated_latents_path"]) == campaign["generated_latents_sha256"], "latents identity differs")
    latents = {row["case_id"]: row for row in (json.loads(line) for line in Path(campaign["generated_latents_path"]).open()) if row["case_id"] in panel and panel[row["case_id"]]["population"] == "generated"}
    tables = {}; prepared = {}
    for label, table in report["tables"].items():
        if label.startswith("archived-"):
            arm = label.split("-")[1]; file = root.path(f"evaluation-v1/archived-{arm}-3e-4-endpoint.attempt01/evaluation-archived-endpoint.jsonl")
        else:
            receipt_path = Path(table["observation_receipt"])
            require(sha256(receipt_path) == table["observation_receipt_sha256"], "observation receipt differs")
            receipt = json.loads(receipt_path.read_text())
            payload = [p for p in receipt["payload_hashes"] if p.endswith(".jsonl") and "diagnostic" not in Path(p).name]
            require(len(payload) == 1, "exactly one heldout payload required"); file = root.path(payload[0])
        read_complete(file.parent); require(sha256(file) == table["records_sha256"], "retained output differs")
        tables[label] = verify_table([json.loads(line) for line in file.open()], table, panel, latents, prepared)
        print(json.dumps({"phase": "CPU-independent-output-reconstruction", "panel": label}), flush=True)
    digest = verify_bootstrap(tables, report)
    diagnostic_panels = {}
    for label, expected in report["TRAIN_diagnostics"].items():
        name, _ = label.split("/"); recipe = next(r for r in campaign["recipes"] if r["recipe_id"] == name)
        data = recipe["config"]["data_condition"]
        if data not in diagnostic_panels:
            directory = root.path(recipe["config"]["corpus_geometry"]["artifact_relative"]); read_complete(directory)
            sources = {r["variant_id"]: r for p in (directory/"natural.jsonl", Path("exports/lexical-reader-v2/generated-pool-attempt02/accepted.jsonl")) for r in (json.loads(line) for line in p.open())}
            diagnostic_panels[data] = {item["id"]: {**sources[item["variant_id"]], **item} for item in json.loads((directory/"diagnostics.json").read_text())}
        receipt = json.loads(Path(report["tables"][label]["observation_receipt"]).read_text())
        greedy = [p for p in receipt["payload_hashes"] if p.endswith(".jsonl") and "diagnostic" in Path(p).name]
        forced = [p for p in receipt["payload_hashes"] if Path(p).name.startswith("diagnostic-forced-")]
        require(len(greedy) == len(forced) == 1, "TRAIN diagnostic payload missing")
        require(sha256(root.path(greedy[0])) == expected["greedy_sha256"] and sha256(root.path(forced[0])) == expected["forced_sha256"], "TRAIN diagnostic hash differs")
        verify_diagnostic([json.loads(line) for line in root.path(greedy[0]).open()], json.loads(root.path(forced[0]).read_text()), expected, diagnostic_panels[data])
    for recipe in campaign["recipes"]:
        name = recipe["recipe_id"]; terminal = report["terminals"][name]
        require(sha256(terminal["receipt"]) == terminal["receipt_sha256"] and terminal["status"] in ("COMPLETED", "FAILED_NUMERICAL"), "unresolved or altered outcome")
        step = 35283 if name.startswith("G2-ByT5") else recipe["config"]["stop_endpoint"]["optimizer_updates"]
        label = f"{name}/update{step}"
        if label not in report["tables"]:
            require(terminal["status"] == "FAILED_NUMERICAL" and not report["endpoint_viability"][name]["viable"], "missing successful endpoint"); continue
        summary = report["tables"][label]; natural = summary["natural"]
        checks = {"prescribed_completion_resolved": terminal["status"] == "COMPLETED",
            "natural_WER_strictly_below_RAW": natural["output_errors"] < natural["source_errors"],
            "completed_natural_repair_lower_positive": natural["completed_repair"][0] > 0,
            "completed_natural_repair_lower_support_at_least_two_groups": len(natural["repair_support_source_groups_lower"]) >= 2}
        if not name.startswith("G2-ByT5"): checks["generated_genuine_required_repair_completed"] = summary["generated"]["required_repair_cases_completed"] > 0
        require(checks == report["endpoint_viability"][name]["criteria"] and all(checks.values()) == report["endpoint_viability"][name]["viable"], "endpoint-only gate differs")
    both = all(report["endpoint_viability"][f"G2-{arm}-D1-U8-seed42-lr3e-4"]["viable"] for arm in ("B100", "C101"))
    require(report["disposition"] == ("GENERATION_2_BOTH_ARMS_VIABLE" if both else "FRONTIER_MODEL_REVIEW_REQUIRED"), "unregistered interpretation")
    result = {"schema": "g2_scientific_results_independent_v1", "status": "PASS_INDEPENDENT_SCIENTIFIC_RESULTS",
        "summary_sha256": sha256(path), "campaign_sha256": sha256(campaign_path), "panels_reconstructed": len(tables),
        "cases_per_panel": 2984, "canonical_scores_rescored": True, "independent_two_row_distances": True,
        "independent_generated_full_consumption_parser": True, "integer_multiplicity_bootstrap_exact": True,
        "exact_factorial_fractions": True, "endpoint_only_viability_exact": True,
        "TRAIN_diagnostics_rescored_separately": True,
        "draw_indices_int64_sha256": digest, "before": before, "after": root.preflight(),
        "code_sha256": sha256(__file__), "elapsed_seconds": time.perf_counter()-started}
    with output.open("x") as stream: json.dump(result, stream, sort_keys=True, allow_nan=False); stream.write("\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--artifact-binding", required=True)
    parser.add_argument("--attempt", type=int, required=True); parser.add_argument("--summary-attempt", type=int, required=True)
    args = parser.parse_args(); print(json.dumps({"status": run(args.artifact_binding, args.attempt, args.summary_attempt)["status"]}))
