"""CPU-only registered G2 summaries; never select a cell or alter a trajectory."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import time
import math

from src.data.g2_artifacts import ArtifactRoot, read_complete, sha256
from src.scoring.records import aggregate
from src.scoring.text import lexical
from src.generation.stress import score as generated_score

BASE = Path("experiments/manifests/generation_2")


def natural_summary(records, panel):
    value = aggregate(row["score"] for row in records)
    if not records or value["reference_words"] <= 0:
        raise ValueError("natural summary requires a nonempty fixed population")
    value.update(cases=len(records), RAW_WER=value["source_errors"] / value["reference_words"],
                 status_counts=dict(Counter(row["status"] for row in records)))
    for index, label in ((0, "lower"), (1, "upper")):
        value["repair_support_source_groups_" + label] = sorted({panel[row["id"]]["source_group_id"]
            for row in records if row["score"]["completed_repair"][index] > 0})
    value["source_byte_identity"] = sum(row["score"]["complete_valid"] and
        row["output"] == panel[row["id"]]["source"] for row in records)
    value["source_lexical_identity"] = sum(row["score"]["complete_valid"] and
        lexical(row["output"]) == lexical(panel[row["id"]]["source"]) for row in records)
    covered = [row["score"] for row in records if row["score"]["fixed_correct_damage"] is not None]
    correct = sum((score["source_consensus_eligible_counts"] or {}).get("correct", 0) for score in covered)
    damage = [sum(score["fixed_correct_damage"][bound] for score in covered) for bound in (0, 1)]
    value["source_correct_preservation_coverage"] = {"covered_cases": len(covered),
        "unavailable_cases": len(records) - len(covered), "covered_correct_counts": correct,
        "covered_damage_bounds": damage, "covered_preserved_bounds": [correct - damage[1], correct - damage[0]]}
    value["source_correct_damage_bounds"] = damage if len(covered) == len(records) else None
    value["target_byte_exact"] = sum(row["score"]["raw_byte_exact"] for row in records)
    value["target_lexical_exact"] = sum(row["score"]["lexical_exact"] for row in records)
    return value


def generated_summary(records, latents):
    if len(records) != 288 or {row["id"] for row in records} != set(latents):
        raise ValueError("exact frozen 288 generated cases required")
    value = {"cases": 288, "complete": 0, "structure_invalid": 0, "invalid_or_incomplete": 0,
             "required_repair_fields_completed": 0, "required_repair_cases_completed": 0,
             "whole_case_conformance": 0, "mixed_success": 0, "by_view": {}, "by_category_view": {}}
    for row in records:
        latent = latents[row["id"]]
        scored = generated_score(latent, row["output"], complete=row["score"]["complete_valid"])
        invalid = not (scored["complete"] and scored["structure_valid"])
        value["complete"] += scored["complete"]; value["structure_invalid"] += not scored["structure_valid"]
        value["invalid_or_incomplete"] += invalid
        value["required_repair_fields_completed"] += scored["repaired"]
        value["required_repair_cases_completed"] += scored["repaired"] > 0
        value["whole_case_conformance"] += scored["whole_case_conformance"]
        value["mixed_success"] += scored["mixed_success"]
        for mapping, key in ((value["by_view"], latent["view_kind"]),
                             (value["by_category_view"], latent["primary_category"] + ":" + latent["view_kind"])):
            counts = mapping.setdefault(key, {"cases": 0, "complete": 0, "invalid_or_incomplete": 0,
                "status_counts": {}, "conformant": 0, "preserved_fields": 0, "preserve_denominator": 0,
                "repaired_fields": 0, "repair_denominator": 0})
            counts["cases"] += 1; counts["complete"] += scored["complete"]
            counts["invalid_or_incomplete"] += invalid; counts["conformant"] += scored["whole_case_conformance"]
            counts["status_counts"][row["status"]] = counts["status_counts"].get(row["status"], 0) + 1
            for field, source in (("preserved_fields", "preserved"), ("preserve_denominator", "preserve_denominator"),
                                  ("repaired_fields", "repaired"), ("repair_denominator", "repair_denominator")):
                counts[field] += scored[source]
    value["decoder_invalid_or_incomplete"] = 288 - value["complete"]
    return value


def normalize_records(records):
    # The qualified comparator writes decoded.text; native B/C writes output.
    return [{**row, "output": row["decoded"]["text"]} if "decoded" in row else row for row in records]


def summarize(records, panel, latents):
    records = normalize_records(records)
    if len(records) != 2984 or len({row["id"] for row in records}) != 2984 or {row["id"] for row in records} != set(panel):
        raise ValueError("every frozen heldout case must have one retained output")
    natural = [row for row in records if panel[row["id"]]["population"] == "natural"]
    generated = [row for row in records if panel[row["id"]]["population"] == "generated"]
    if len(natural) != 2696: raise ValueError("frozen natural population changed")
    subsets = {"natural_all": natural, "legacy108": [], "new2588": [], "calibration": [], "hpo_development": [],
               "natural-clean": [], "natural-other": []}
    for row in natural:
        item = panel[row["id"]]
        subsets["legacy108" if item["legacy_subset"] else "new2588"].append(row)
        subsets[item["role"]].append(row)
        subsets.setdefault(item["official_split"], []).append(row)
        subsets["natural-other" if "other" in item["official_split"] else "natural-clean"].append(row)
    by_group = defaultdict(list)
    for row in natural: by_group[panel[row["id"]]["source_group_id"]].append(row["score"])
    if len(by_group) != 52: raise ValueError("all frozen natural groups required")
    metrics = {}
    for name, field, index, denominator in (("WER", "eO", None, "reference_words"),
            ("completed_repair_lower", "completed_repair", 0, "eS"), ("completed_repair_upper", "completed_repair", 1, "eS"),
            ("introduced_lower", "introduced", 0, "reference_words"), ("introduced_upper", "introduced", 1, "reference_words")):
        metrics[name] = {group: [sum(score[field] if index is None else score[field][index] for score in scores),
                                 sum(score[denominator] for score in scores)] for group, scores in by_group.items()}
    return {"natural": natural_summary(natural, panel), "generated": generated_summary(generated, latents),
            "natural_subsets": {name: natural_summary(rows, panel) for name, rows in subsets.items()},
            "group_metric_totals": metrics, "failure_inclusive": True, "alignment_bounds_are_not_confidence_intervals": True}


def viability(terminal, summary, byt5=False):
    natural = summary["natural"]
    conditions = {"prescribed_completion_resolved": terminal["status"] == "COMPLETED",
        "natural_WER_strictly_below_RAW": natural["output_errors"] < natural["source_errors"],
        "completed_natural_repair_lower_positive": natural["completed_repair"][0] > 0,
        "completed_natural_repair_lower_support_at_least_two_groups": len(natural["repair_support_source_groups_lower"]) >= 2}
    if not byt5: conditions["generated_genuine_required_repair_completed"] = summary["generated"]["required_repair_cases_completed"] > 0
    return {"criteria": conditions, "viable": all(conditions.values()), "endpoint_only": True}


def factorial(values):
    if set(values) != {"D0-U1", "D0-U8", "D1-U1", "D1-U8"}:
        raise ValueError("all four predeclared factorial cells required")
    a, b, c, d = [values[key] for key in ("D0-U1", "D0-U8", "D1-U1", "D1-U8")]
    return {"D1_effect_at_U1": c-a, "D1_effect_at_U8": d-b, "U8_effect_at_D0": b-a,
            "U8_effect_at_D1": d-c, "difference_in_differences": (d-c)-(b-a)}


def factorial_intervals(groups, cells, metric_totals):
    """Reuse the registered draws; contrasts never affect eligibility."""
    import numpy as np
    groups = sorted(groups)
    if len(groups) != 52 or len(set(groups)) != 52:
        raise ValueError("all 52 frozen groups required")
    draws = np.random.Generator(np.random.PCG64(42)).integers(0, 52, size=(10000, 52))
    samples = {}
    for cell, name in cells.items():
        if set(metric_totals[name]) != set(groups): raise ValueError("factorial group membership changed")
        values = np.asarray([metric_totals[name][group] for group in groups], dtype=np.float64)
        if values.shape != (52, 2) or not np.isfinite(values).all() or (values < 0).any():
            raise ValueError("invalid factorial counts")
        totals = values[draws].sum(axis=1)
        if (totals[:, 1] <= 0).any(): raise ValueError("undefined fixed draw; no redraw or exclusion")
        samples[cell] = totals[:, 0] / totals[:, 1]
    return {"intervals": {effect: np.percentile(values, [2.5, 97.5]).tolist()
                          for effect, values in factorial(samples).items()},
            "draw_indices_int64_sha256": hashlib.sha256(draws.astype("<i8").tobytes()).hexdigest(),
            "draws": 10000, "groups": 52, "seed": 42, "generator": "PCG64", "eligibility_affected": False}


def diagnostic_summary(greedy, forced, panel):
    """Separate fixed TRAIN fit/copy counts from heldout adequacy."""
    if len(panel) != 304 or len({row["id"] for row in greedy}) != 304 or {row["id"] for row in greedy} != set(panel):
        raise ValueError("complete fixed 304-case TRAIN diagnostic required")
    if len(forced) != 304 or len({row["id"] for row in forced}) != 304 or {row["id"] for row in forced} != set(panel):
        raise ValueError("complete fixed teacher-forced diagnostic required")
    strata = defaultdict(list)
    for row in greedy: strata[panel[row["id"]]["stratum"]].append(row)
    fit = {}
    for name, rows in strata.items():
        fit[name] = {"cases": len(rows), "status_counts": dict(Counter(row["status"] for row in rows)),
                    "counts": aggregate(row["score"] for row in rows),
                    "source_byte_identity": sum(row["score"]["complete_valid"] and row["output"] == panel[row["id"]]["source"] for row in rows),
                    "source_lexical_identity": sum(row["score"]["complete_valid"] and lexical(row["output"]) == lexical(panel[row["id"]]["source"]) for row in rows),
                    "target_byte_exact": sum(row["score"]["raw_byte_exact"] for row in rows),
                    "target_lexical_exact": sum(row["score"]["lexical_exact"] for row in rows)}
    losses = defaultdict(lambda: defaultdict(list))
    for row in forced:
        for component, value in row["losses"].items():
            if value is not None and not math.isfinite(value): raise ValueError("nonfinite diagnostic loss")
            losses[panel[row["id"]]["stratum"]][component].append((value, row["denominators"]))
    components = {}
    for name, by_component in losses.items():
        components[name] = {}
        for key, pairs in by_component.items():
            observed = [(value, den) for value, den in pairs if value is not None]
            def denominator(den):
                return den["B"] if key == "target" else den["C"][key]
            count = sum(denominator(den) for _, den in observed)
            components[name][key] = {"covered_cases": len(observed), "unavailable_cases": len(pairs)-len(observed),
                "mean_of_case_losses": sum(value for value, _ in observed)/len(observed) if observed else None,
                "component_denominator": count,
                "denominator_weighted_loss": sum(value*denominator(den) for value, den in observed)/count if count else None}
    return {"greedy_fit_copy_by_stratum": fit, "teacher_forced_components_by_stratum": components,
            "TRAIN_diagnostic_only": True, "counts_toward_heldout_viability": False}


def run(binding, attempt):
    root = ArtifactRoot(binding); started = time.perf_counter(); freeze_path = BASE / "execution-campaign-freeze.attempt01.json"
    campaign = json.loads(freeze_path.read_text()); corpus = json.loads(Path(campaign["corpus_freeze_path"]).read_text())
    output = BASE / f"scientific-results.attempt{attempt:02d}.json"
    if output.exists(): raise FileExistsError(output)
    for path, identity in campaign["source_hashes"].items():
        if sha256(path) != identity: raise ValueError("frozen scientific source changed")
    panel_path = root.path(corpus["panel_relative"]) / "panel.json"
    if sha256(panel_path) != corpus["panel_sha256"]: raise ValueError("frozen heldout panel changed")
    panel = {row["id"]: row for row in json.loads(panel_path.read_text())}
    if sha256(campaign["generated_latents_path"]) != campaign["generated_latents_sha256"]: raise ValueError("generated latents changed")
    ids = {name for name, row in panel.items() if row["population"] == "generated"}
    latents = {row["case_id"]: row for row in (json.loads(line) for line in Path(campaign["generated_latents_path"]).open()) if row["case_id"] in ids}
    if set(latents) != ids or any(row["partition"] != "dev" for row in latents.values()): raise ValueError("frozen DEVELOPMENT latents only")
    terminals = {}
    for name in campaign["execution_order"]:
        paths = sorted(BASE.glob(f"scientific-outcome-{name}.attempt*.json"))
        if not paths: raise ValueError("all seven prescribed outcomes must exist before campaign analysis")
        value = json.loads(paths[-1].read_text())
        if value["status"] not in ("COMPLETED", "FAILED_NUMERICAL"): raise ValueError("an unresolved scientific attempt remains")
        terminals[name] = {"receipt": str(paths[-1]), "receipt_sha256": sha256(paths[-1]), **value}
    tables, criteria = {}, {}
    diagnostics = {}
    diagnostic_panels = {}
    for recipe in campaign["recipes"]:
        name = recipe["recipe_id"]; cfg = recipe["config"]; terminal = terminals[name]
        schedule = campaign["byt5_schedule"]["states"] if name.startswith("G2-ByT5") else cfg["evaluation_endpoints"]
        for state in schedule:
            step = state["optimizer_update"] if "optimizer_update" in state else state["optimizer_updates"]
            paths = sorted(BASE.glob(f"scientific-observation-{name}.update{step:05d}.attempt*.json"))
            if not paths:
                if terminal["status"] == "FAILED_NUMERICAL": continue
                raise ValueError("a completed prescribed evaluation is missing")
            observation = json.loads(paths[0].read_text())
            if observation.get("milestone", observation.get("endpoint")) != state:
                raise ValueError("actual evaluation schedule binding changed")
            files = [path for path in observation["payload_hashes"] if Path(path).suffix == ".jsonl" and "diagnostic" not in Path(path).name]
            if len(files) != 1: raise ValueError("one exact heldout output payload required")
            file = root.path(files[0]); read_complete(file.parent)
            if sha256(file) != observation["payload_hashes"][files[0]]: raise ValueError("heldout output changed")
            summary = summarize([json.loads(line) for line in file.open()], panel, latents)
            summary.update(observation_receipt=str(paths[0]), observation_receipt_sha256=sha256(paths[0]), records_sha256=sha256(file), state=state)
            tables[f"{name}/update{step}"] = summary
            if not name.startswith("G2-ByT5") and step in (0, cfg["stop_endpoint"]["optimizer_updates"]):
                data = cfg["data_condition"]
                if data not in diagnostic_panels:
                    directory = root.path(cfg["corpus_geometry"]["artifact_relative"]); read_complete(directory)
                    diagnostic_path = directory / "diagnostics.json"
                    if sha256(diagnostic_path) != cfg["corpus_geometry"]["diagnostics_sha256"]: raise ValueError("TRAIN diagnostic identity changed")
                    sources = {row["variant_id"]: row for p in (directory / "natural.jsonl", Path("exports/lexical-reader-v2/generated-pool-attempt02/accepted.jsonl"))
                               for row in (json.loads(line) for line in p.open())}
                    diagnostic_panels[data] = {item["id"]: {**sources[item["variant_id"]], **item} for item in json.loads(diagnostic_path.read_text())}
                diagnostic = diagnostic_panels[data]
                greedy_files = [p for p in observation["payload_hashes"] if Path(p).suffix == ".jsonl" and "diagnostic" in Path(p).name]
                forced_files = [p for p in observation["payload_hashes"] if Path(p).name.startswith("diagnostic-forced-")]
                if len(greedy_files) != 1 or len(forced_files) != 1: raise ValueError("scheduled TRAIN diagnostics missing")
                for p in greedy_files + forced_files:
                    if sha256(root.path(p)) != observation["payload_hashes"][p]: raise ValueError("TRAIN diagnostic payload changed")
                diagnostics[f"{name}/update{step}"] = {**diagnostic_summary(
                    [json.loads(line) for line in root.path(greedy_files[0]).open()],
                    json.loads(root.path(forced_files[0]).read_text()), diagnostic),
                    "greedy_sha256": observation["payload_hashes"][greedy_files[0]],
                    "forced_sha256": observation["payload_hashes"][forced_files[0]], "state": state}
            if state == schedule[-1]: criteria[name] = viability(terminal, summary, name.startswith("G2-ByT5"))
        if name not in criteria: criteria[name] = {"viable": False, "criteria": {"prescribed_completion_resolved": False}, "endpoint_missing_after_repeated_numerical_failure": True}
    # Expanded-panel archived controls supply only the original D0-U1 cells.
    for arm in ("B100", "C101"):
        directory = root.path(f"evaluation-v1/archived-{arm}-3e-4-endpoint.attempt01"); read_complete(directory)
        file = directory / "evaluation-archived-endpoint.jsonl"
        tables[f"archived-{arm}-D0-U1"] = {**summarize([json.loads(line) for line in file.open()], panel, latents), "records_sha256": sha256(file)}
    from src.scoring.g2_bootstrap import paired_group_intervals
    groups = sorted({r["source_group_id"] for r in panel.values() if r["population"] == "natural"})
    totals = {metric: {name: table["group_metric_totals"][metric] for name, table in tables.items()}
              for metric in ("WER", "completed_repair_lower", "completed_repair_upper", "introduced_lower", "introduced_upper")}
    # The frozen source-error numerator is shared across every system.
    totals["WER"]["RAW"] = {group: [tables["archived-B100-D0-U1"]["group_metric_totals"]["completed_repair_lower"][group][1],
                                   tables["archived-B100-D0-U1"]["group_metric_totals"]["WER"][group][1]] for group in groups}
    bootstrap = {metric: paired_group_intervals(groups, values) for metric, values in totals.items()}
    factorials = {}
    endpoint_keys = {recipe["recipe_id"]: f'{recipe["recipe_id"]}/update{recipe["config"]["stop_endpoint"]["optimizer_updates"]}'
                     for recipe in campaign["recipes"] if not recipe["recipe_id"].startswith("G2-ByT5")}
    for arm in ("B100", "C101"):
        cells = {"D0-U1": f"archived-{arm}-D0-U1", **{f"{data}-{update}": endpoint_keys[f"G2-{arm}-{data}-{update}-seed42-lr3e-4"]
            for data, update in (("D0", "U8"), ("D1", "U1"), ("D1", "U8"))}}
        if any(name not in tables for name in cells.values()):
            factorials[arm] = {"status": "UNAVAILABLE_PRESCRIBED_ENDPOINT_MISSING", "no_replacement_or_selection": True}; continue
        effects = {}
        for metric, field, index, denominator in (("WER", "output_errors", None, "reference_words"),
                ("completed_repair_lower", "completed_repair", 0, "source_errors"), ("completed_repair_upper", "completed_repair", 1, "source_errors"),
                ("introduced_lower", "introduced", 0, "reference_words"), ("introduced_upper", "introduced", 1, "reference_words")):
            values = {cell: Fraction(tables[name]["natural"][field] if index is None else tables[name]["natural"][field][index], tables[name]["natural"][denominator]) for cell, name in cells.items()}
            effects[metric] = {"exact_effects": {key: {"numerator": value.numerator, "denominator": value.denominator, "value": float(value)} for key, value in factorial(values).items()},
                               "paired_group_bootstrap": factorial_intervals(groups, cells, totals[metric])}
        factorials[arm] = {"cells": cells, "effects": effects, "scope": "D1 changes diversity/error prevalence/domain composition; not pure sample count"}
    candidates = [criteria[f"G2-{arm}-D1-U8-seed42-lr3e-4"]["viable"] for arm in ("B100", "C101")]
    disposition = "GENERATION_2_BOTH_ARMS_VIABLE" if all(candidates) else "FRONTIER_MODEL_REVIEW_REQUIRED"
    result = {"schema": "g2_scientific_results_v1", "status": "SEVEN_PRESCRIBED_OUTCOMES_RECONSTRUCTED",
              "campaign_sha256": sha256(freeze_path), "tables": tables, "endpoint_viability": criteria,
              "factorial_analysis": factorials, "paired_group_bootstrap": bootstrap, "terminals": terminals, "TRAIN_diagnostics": diagnostics,
              "model_or_cell_selection_performed": False, "D1_U8_remains_predeclared_candidate": True,
              "bootstrap_is_descriptive_not_training_seed_or_H1_inference": True,
              "disposition": disposition, "elapsed_seconds": time.perf_counter() - started, "code_sha256": sha256(__file__)}
    with output.open("x") as stream: json.dump(result, stream, sort_keys=True, allow_nan=False); stream.write("\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--artifact-binding", required=True)
    parser.add_argument("--attempt", type=int, required=True); args = parser.parse_args()
    value = run(args.artifact_binding, args.attempt)
    print(json.dumps({"status": value["status"], "disposition": value["disposition"]}))
