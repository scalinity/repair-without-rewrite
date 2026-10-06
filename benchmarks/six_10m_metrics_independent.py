"""CPU-only reconstruction of frozen DEVELOPMENT scores and LR decisions.

This review never imports the campaign runner or an accelerator runtime. It
re-scores retained outputs, aggregates integer counts through a separate path,
and independently parses generated fields. Partial evidence cannot select an LR.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time

from src.scoring.records import Output, prepare_source, score_output
from src.scoring.text import lexical
from src.scoring.oracle import dense_triple
from src.generation.stress import GRAMMARS


SAFE = Path("experiments/manifests/six_10m_probes")
FREEZE = SAFE / "campaign-freeze.attempt01.json"
PRIVATE = Path("exports/six-10m-probes")
LATENTS = Path("experiments/manifests/stress_split_repair_20261005T054436Z/latents.jsonl")
PILOT = Path("docs/reviews/FRONTIER_READER_CURRICULUM_DECISION_V1.md")
AMENDMENTS = Path("docs/reviews/PROSPECTIVE_AMENDMENTS.md")
STATUS_MAP = {"completed": "complete", "invalid_byte_decoding": "invalid_utf8",
              "abstained": "abstain", "invalid_or_capped": "invalid_c", "capped": "capped"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def byte_sha(value):
    return hashlib.sha256(value.encode("utf-8", errors="strict")).hexdigest()


def normalized(value):
    if isinstance(value, dict):
        return {key: normalized(item) for key, item in value.items()}
    if isinstance(value, set):
        return sorted((normalized(item) for item in value), key=lambda item: json.dumps(item, sort_keys=True))
    if isinstance(value, (list, tuple)):
        return [normalized(item) for item in value]
    return value


def ratio(numerator, denominator):
    require(denominator > 0, "undefined endpoint denominator")
    value = Fraction(numerator, denominator)
    return {"numerator": value.numerator, "denominator": value.denominator}


def integer_distance(left, right):
    """Independent two-row edit distance for failure-inclusive WER numerators."""
    previous = list(range(len(left) + 1))
    for column, other in enumerate(right, 1):
        current = [column]
        for row, item in enumerate(left, 1):
            current.append(min(current[-1] + 1, previous[row] + 1,
                               previous[row - 1] + int(item != other)))
        previous = current
    return previous[-1]


def read_inputs():
    campaign = json.loads(FREEZE.read_text())
    require(len(campaign["recipes"]) == 6, "campaign must bind exactly six recipes")
    require(len(set(campaign["execution_order"])) == 6, "recipe IDs must be unique")
    require({row["recipe_id"] for row in campaign["recipes"]} == set(campaign["execution_order"]),
            "campaign recipe IDs/order mismatch")
    require(all(row["status"] == "AUTHORIZED_UNSTARTED" for row in campaign["recipes"]),
            "original freeze does not enumerate six unstarted slots")
    panel_path = Path(campaign["evaluation_panel_path"])
    require(sha(panel_path) == campaign["evaluation_panel_sha256"], "frozen panel hash mismatch")
    require(sha(LATENTS) == campaign["generated_evaluation_latents_sha256"], "frozen latent hash mismatch")
    for path, expected in campaign["source_hashes"].items():
        require(sha(path) == expected, "frozen source hash mismatch: " + path)
    panel = json.loads(panel_path.read_text())
    require(len(panel) == 396 and len({row["id"] for row in panel}) == 396, "panel identity/cardinality mismatch")
    require(Counter(row["population"] for row in panel) == {"natural": 108, "generated": 288},
            "natural/generated population cardinality mismatch")
    for row in panel:
        require(byte_sha(row["source"]) == row["source_sha256"], "panel source bytes mismatch: " + row["id"])
        require(byte_sha(row["target"]) == row["target_sha256"], "panel target bytes mismatch: " + row["id"])
        require(row["native_admitted"], "frozen panel contains an unhandled native rejection")
    wanted = {row["id"] for row in panel if row["population"] == "generated"}
    latents = {}
    for line in LATENTS.read_text().splitlines():
        row = json.loads(line)
        if row["case_id"] in wanted:
            require(row["case_id"] not in latents, "duplicate generated latent ID")
            latents[row["case_id"]] = row
    require(set(latents) == wanted, "generated latent membership mismatch")
    grammar_by_id = {grammar.family_id: grammar for grammar in GRAMMARS}
    for row in panel:
        if row["population"] == "generated":
            latent = latents[row["id"]]
            require(latent["partition"] == "dev", "non-DEVELOPMENT generated latent")
            require(latent["source_sha256"] == row["source_sha256"] and
                    latent["reference_sha256"] == row["target_sha256"], "generated latent/panel hash mismatch")
            require(len(latent["scaffold"]) == 3 and len(latent["fields"]) == 2,
                    "frozen generated grammar has unexpected arity")
            require(tuple(latent["scaffold"]) == grammar_by_id[latent["template_id"]].scaffold,
                    "latent scaffold differs from frozen grammar catalog")
            require(all(field["inverse_candidate_count"] == 1 for field in latent["fields"]),
                    "generated inverse qualification mismatch")
            require(all(field["repair_required"] == (not field["initial_field_match"]) and
                        field["preserve_required"] == field["initial_field_match"] and
                        field["recoverability_class"] == "unique_public_inverse"
                        for field in latent["fields"]), "generated genuine-repair/preservation flags mismatch")
    pilot = PILOT.read_text()
    require("Natural failure-inclusive WER is strictly below RAW." in pilot and
            "lowest natural WER;" in pilot and
            "These are DEVELOPMENT viability screens, not H1 significance or final-paper acceptance gates." in pilot,
            "controlling pilot selection text changed")
    require("Adopt the complete Frontier Reader/Curriculum Decision v1 as the normative DEVELOPMENT reader contract." in AMENDMENTS.read_text(),
            "prospective DEVELOPMENT contract adoption missing")
    return campaign, panel, latents


def generated_fields(latent, output, complete):
    """Full-consumption two-field parse, independent of stress.score/Grammar.parse."""
    parsed = None
    if isinstance(output, str):
        try:
            output.encode("utf-8", errors="strict")
            prefix, middle, suffix = latent["scaffold"]
            match = re.fullmatch(re.escape(prefix) + r"([^;\n]*)" + re.escape(middle)
                                 + r"([^;\n]*)" + re.escape(suffix), output)
            if match:
                parsed = match.groups()
        except UnicodeError:
            pass
    successes = [bool(complete and parsed is not None and
                      parsed[index] in field["allowed_target_surfaces"])
                 for index, field in enumerate(latent["fields"])]
    preserve = [index for index, field in enumerate(latent["fields"]) if field["preserve_required"]]
    repairs = [index for index, field in enumerate(latent["fields"]) if field["repair_required"]]
    return {"complete": bool(complete), "structure_valid": parsed is not None,
            "whole_case_conformance": bool(complete and parsed is not None and all(successes)),
            "mixed_success": bool(complete and preserve and repairs and all(successes)),
            "preserved_fields": sum(successes[index] for index in preserve),
            "preserve_denominator": len(preserve),
            "repaired_fields": sum(successes[index] for index in repairs),
            "repair_denominator": len(repairs)}


def aggregate_natural(rows, panel_by_id):
    scores = [row["score"] for row in rows]
    counts = {"reference_words": sum(score["reference_words"] for score in scores),
              "source_errors": sum(score["eS"] for score in scores),
              "output_errors": sum(score["eO"] for score in scores),
              "invalid_or_incomplete": sum(not score["complete_valid"] for score in scores)}
    for name in ("repair", "introduced", "completed_repair"):
        counts[name] = [sum(score[name][bound] for score in scores) for bound in range(2)]
    counts["wer"] = counts["output_errors"] / counts["reference_words"]
    counts["RAW_WER"] = counts["source_errors"] / counts["reference_words"]
    counts["introduced_rate"] = [value / counts["reference_words"] for value in counts["introduced"]]
    counts["completed_repair_rate"] = [value / counts["source_errors"] for value in counts["completed_repair"]]
    for bound, label in ((0, "lower"), (1, "upper")):
        counts["repair_support_source_groups_" + label] = sorted({panel_by_id[row["id"]]["source_group_id"]
            for row in rows if row["score"]["completed_repair"][bound] > 0})
    counts["source_byte_identity"] = sum(row["score"]["complete_valid"] and
        row["output"] == panel_by_id[row["id"]]["source"] for row in rows)
    counts["source_lexical_identity"] = sum(row["score"]["complete_valid"] and
        lexical(row["output"]) == lexical(panel_by_id[row["id"]]["source"]) for row in rows)
    counts["source_correct_counts"] = sum((score["source_consensus_eligible_counts"] or {}).get("correct", 0)
                                           for score in scores)
    covered = [score for score in scores if score["fixed_correct_damage"] is not None]
    correct = sum((score["source_consensus_eligible_counts"] or {}).get("correct", 0) for score in covered)
    damage = [sum(score["fixed_correct_damage"][bound] for score in covered) for bound in range(2)]
    preserved = [correct - damage[1], correct - damage[0]]
    counts["source_correct_preservation_coverage"] = {"covered_cases": len(covered),
        "unavailable_cases": 108 - len(covered), "covered_correct_counts": correct,
        "covered_damage_bounds": damage, "covered_preserved_bounds": preserved}
    counts["source_correct_damage_bounds"] = damage if len(covered) == 108 else None
    counts["source_correct_preserved_bounds"] = preserved if len(covered) == 108 else None
    counts["target_byte_exact"] = sum(score["raw_byte_exact"] for score in scores)
    counts["target_lexical_exact"] = sum(score["lexical_exact"] for score in scores)
    counts["scorer_caps"] = sum(score["fallback_reason"] is not None for score in scores)
    counts["repair_width"] = sum(score["repair"][1] - score["repair"][0] for score in scores)
    counts["introduced_width"] = sum(score["introduced"][1] - score["introduced"][0] for score in scores)
    counts["status_counts"] = dict(Counter(row["status"] for row in rows))
    return counts


def aggregate_generated(rows, latents):
    counts = {"cases": 288, "complete": 0, "structure_invalid": 0, "invalid_or_incomplete": 0,
              "required_repair_fields_completed": 0, "required_repair_cases_completed": 0,
              "whole_case_conformance": 0, "mixed_success": 0, "by_view": {}, "by_category_view": {}}
    for row in rows:
        latent = latents[row["id"]]
        result = generated_fields(latent, row["output"], row["score"]["complete_valid"])
        invalid = not (result["complete"] and result["structure_valid"])
        counts["complete"] += result["complete"]
        counts["structure_invalid"] += not result["structure_valid"]
        counts["invalid_or_incomplete"] += invalid
        counts["required_repair_fields_completed"] += result["repaired_fields"]
        counts["required_repair_cases_completed"] += result["repaired_fields"] > 0
        counts["whole_case_conformance"] += result["whole_case_conformance"]
        counts["mixed_success"] += result["mixed_success"]
        for mapping, key in ((counts["by_view"], latent["view_kind"]),
                             (counts["by_category_view"], latent["primary_category"] + ":" + latent["view_kind"])):
            group = mapping.setdefault(key, {"cases": 0, "complete": 0, "invalid_or_incomplete": 0,
                "status_counts": {}, "conformant": 0, "preserved_fields": 0,
                "preserve_denominator": 0, "repaired_fields": 0, "repair_denominator": 0})
            group["cases"] += 1
            group["complete"] += result["complete"]
            group["invalid_or_incomplete"] += invalid
            group["status_counts"][row["status"]] = group["status_counts"].get(row["status"], 0) + 1
            group["conformant"] += result["whole_case_conformance"]
            for name in ("preserved_fields", "preserve_denominator", "repaired_fields", "repair_denominator"):
                group[name] += result[name]
    counts["decoder_invalid_or_incomplete"] = 288 - counts["complete"]
    return counts


def audit_evaluation(receipt_path, campaign, panel, latents):
    receipt = json.loads(receipt_path.read_text())
    recipe_id = receipt["recipe_id"]
    recipe = next(row for row in campaign["recipes"] if row["recipe_id"] == recipe_id)
    endpoint = next(row for row in campaign["evaluation_endpoints"] if row["nominal"] == receipt["nominal_endpoint"])
    require(receipt["actual_endpoint"] == endpoint, "evaluation common endpoint mismatch")
    require(receipt["panel_sha256"] == campaign["evaluation_panel_sha256"], "evaluation panel receipt mismatch")
    label = "update{:03d}".format(endpoint["update"])
    candidates = list((PRIVATE / recipe_id).glob("attempt*/evaluation-" + label + ".jsonl"))
    matches = [path for path in candidates if sha(path) == receipt["output_sha256"]]
    require(matches, "hash-bound raw evaluation is unavailable: " + str(receipt_path))
    path = sorted(matches)[0]
    records = [json.loads(line) for line in path.read_text().splitlines()]
    require([row["id"] for row in records] == [row["id"] for row in panel], "raw evaluation IDs/order mismatch")
    rescore_digest = hashlib.sha256()
    independent_distance_checks = 0
    dense_oracle_checks = 0
    oracle_envelope_checks = 0
    for row, frozen in zip(records, panel):
        identifier = row["id"]
        require(row["population"] == frozen["population"] and row["arm"] == recipe["config"]["arm"]
                and row["checkpoint_label"] == label, "raw evaluation identity mismatch: " + identifier)
        require(row["source_sha256"] == frozen["source_sha256"] and row["target_sha256"] == frozen["target_sha256"],
                "raw evaluation source/reference hash mismatch: " + identifier)
        require(row["status"] in STATUS_MAP, "unexpected frozen decoder status: " + identifier)
        rescored = normalized(score_output(prepare_source(frozen["target"], frozen["source"]),
                                          Output(row["output"], STATUS_MAP[row["status"]])))
        require(rescored == row["score"], "canonical scorer reproduction mismatch: " + identifier)
        payload = json.dumps({"id": identifier, "score": rescored}, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":")).encode("utf-8")
        rescore_digest.update(payload + b"\n")
        reference = lexical(frozen["target"])
        source = lexical(frozen["source"])
        observed = lexical(row["output"]) if rescored["observed_text_policy"] == "emitted" else ()
        require(integer_distance(reference, source) == rescored["eS"] and
                integer_distance(reference, observed) == rescored["eO"] and
                integer_distance(source, observed) == rescored["eSO"], "independent edit-distance mismatch: " + identifier)
        independent_distance_checks += 3
        if (len(reference) + 1) * (len(source) + 1) * (len(observed) + 1) <= 20000:
            independent = dense_triple(reference, source, observed)
            if rescored["fallback_reason"] is None or rescored["status"] == "closed_form_point":
                require(list(independent["repair"]) == rescored["repair"] and
                        list(independent["introduced"]) == rescored["introduced"] and
                        independent["h"] == rescored["h"], "dense scorer-oracle mismatch: " + identifier)
                dense_oracle_checks += 1
            else:
                require(all(rescored[name][0] <= independent[name][0] <= independent[name][1] <= rescored[name][1]
                            for name in ("repair", "introduced")), "scorer cap envelope mismatch: " + identifier)
                oracle_envelope_checks += 1
    by_id = {row["id"]: row for row in panel}
    natural = aggregate_natural([row for row in records if row["population"] == "natural"], by_id)
    generated = aggregate_generated([row for row in records if row["population"] == "generated"], latents)
    require(natural == receipt["natural"], "independent natural aggregate mismatch: " + str(receipt_path))
    require(generated == receipt["generated"], "independent generated aggregate mismatch: " + str(receipt_path))
    return {"receipt_path": str(receipt_path), "receipt_sha256": sha(receipt_path),
            "output_path": str(path), "output_sha256": sha(path), "recipe_id": recipe_id,
            "nominal_endpoint": receipt["nominal_endpoint"], "actual_endpoint": endpoint,
            "canonical_score_records_reproduced": 396, "canonical_rescore_sha256": rescore_digest.hexdigest(),
            "independent_edit_distance_checks": independent_distance_checks,
            "bounded_dense_oracle_exact_checks": dense_oracle_checks,
            "bounded_dense_oracle_envelope_checks": oracle_envelope_checks,
            "natural": natural, "generated": generated,
            "wer_rational": ratio(natural["output_errors"], natural["reference_words"]),
            "raw_wer_rational": ratio(natural["source_errors"], natural["reference_words"]),
            "introduced_upper_rational": ratio(natural["introduced"][1], natural["reference_words"])}


def decision(campaign, evaluations):
    resolved = {}
    for path in sorted(SAFE.glob("recipe-*.attempt*.json")):
        row = json.loads(path.read_text())
        require(row["recipe_id"] in campaign["execution_order"], "unregistered recipe receipt")
        require(row["recipe_id"] not in resolved, "duplicate resolved recipe outcome")
        require(row["campaign_sha256"] == sha(FREEZE), "resolved recipe campaign hash mismatch")
        require(row["status"] in ("COMPLETED", "FAILED"), "unresolved recipe outcome")
        resolved[row["recipe_id"]] = row
    failures = [json.loads(path.read_text()) for path in SAFE.glob("failure-*.attempt*.json")]
    require(all(row["disposition"] == "NUMERICAL_FAILURE" for row in failures),
            "campaign implementation/data defect blocks eligibility reconstruction")
    if set(resolved) != set(campaign["execution_order"]):
        return {"status": "PENDING_SIX_RESOLVED_OUTCOMES", "resolved_recipe_ids": sorted(resolved),
                "missing_recipe_ids": sorted(set(campaign["execution_order"]) - set(resolved)),
                "selected_LR": None, "ranking": None}
    final_by_recipe = {}
    for evaluation in evaluations:
        if evaluation["nominal_endpoint"] == 10000000:
            identifier = evaluation["recipe_id"]
            if identifier in final_by_recipe:
                require(evaluation["output_sha256"] == final_by_recipe[identifier]["output_sha256"],
                        "multiple different final evaluation outputs require explicit accounting")
            final_by_recipe[identifier] = evaluation
    recipes = {}
    keys = {}
    for frozen in campaign["recipes"]:
        identifier = frozen["recipe_id"]
        outcome = resolved[identifier]
        completed = outcome["status"] == "COMPLETED"
        if completed:
            require(sum(row["recipe_id"] == identifier for row in failures) <= 1,
                    "completed recipe has repeated numerical failure")
            require(outcome["endpoint"] == frozen["config"]["actual_stop_endpoint"], "resolved common endpoint mismatch")
            final_checkpoint = outcome["checkpoints"][-1]
            checkpoint_path = Path(final_checkpoint["checkpoint_path"])
            require(sha(checkpoint_path / "COMPLETE.json") == outcome["final_checkpoint_complete_sha256"],
                    "final checkpoint publication identity mismatch")
            complete = json.loads((checkpoint_path / "COMPLETE.json").read_text())
            require(sha(checkpoint_path / "metadata.json") == complete["metadata.json"],
                    "final checkpoint metadata bytes mismatch")
            metadata = json.loads((checkpoint_path / "metadata.json").read_text())
            require(metadata["optimizer_step"] == outcome["endpoint"]["update"] and
                    metadata["committed_exposure"] == outcome["endpoint"]["canonical_exposure"] and
                    not metadata["pending_charge"] and not metadata["queue"],
                    "final checkpoint is not the prescribed completed optimizer boundary")
            require(metadata["identities"]["campaign_sha256"] == sha(FREEZE) and
                    metadata["identities"]["recipe_config_sha256"] == frozen["config_sha256"],
                    "final checkpoint campaign/config identity mismatch")
            require(identifier in final_by_recipe, "completed recipe final evaluation unavailable")
            evaluation = final_by_recipe[identifier]
            natural, generated = evaluation["natural"], evaluation["generated"]
            checks = [True, natural["output_errors"] < natural["source_errors"],
                      natural["completed_repair"][0] > 0,
                      len(natural["repair_support_source_groups_lower"]) >= 2,
                      generated["required_repair_fields_completed"] > 0]
            keys[identifier] = (Fraction(natural["output_errors"], natural["reference_words"]),
                Fraction(natural["introduced"][1], natural["reference_words"]),
                -natural["completed_repair"][0], natural["invalid_or_incomplete"],
                -generated["mixed_success"], Fraction(str(frozen["config"]["peak_lr"])))
        else:
            checks = [False, None, None, None, None]
        recipes[identifier] = {"status": outcome["status"], "criteria": checks,
                               "eligible": all(value is True for value in checks)}
    ranking, selected = {}, {}
    for arm in ("B100", "C101"):
        eligible = [row["recipe_id"] for row in campaign["recipes"] if row["config"]["arm"] == arm
                    and recipes[row["recipe_id"]]["eligible"]]
        ranking[arm] = sorted(eligible, key=keys.__getitem__)
        selected[arm] = None if not ranking[arm] else ranking[arm][0]
    both = all(selected.values())
    one = any(selected.values())
    disposition = "BOTH_ARMS_HAVE_ELIGIBLE_10M_RECIPE" if both else (
        "FRONTIER_MODEL_REVIEW_REQUIRED" if one else "CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE")
    exact_keys = {identifier: [ratio(value.numerator, value.denominator) if isinstance(value, Fraction) else value
                              for value in key] for identifier, key in keys.items()}
    return {"status": "SIX_RESOLVED_OUTCOMES_RECONSTRUCTED", "recipes": recipes,
            "lexicographic_keys": exact_keys, "ranking": ranking, "selected_recipe": selected,
            "selected_LR": {arm: None if identifier is None else next(row["config"]["peak_lr"]
                for row in campaign["recipes"] if row["recipe_id"] == identifier)
                for arm, identifier in selected.items()}, "campaign_disposition": disposition}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "audit"))
    parser.add_argument("--receipt", type=Path, help="Audit one completed evaluation receipt; never select from partial evidence")
    args = parser.parse_args()
    start = time.perf_counter()
    campaign, panel, latents = read_inputs()
    evidence = {"schema": "six_10m_independent_metrics_v1", "campaign_sha256": sha(FREEZE),
        "review_source_sha256": sha(Path(__file__)), "reviewed_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "cpu_only": True, "accelerator_runtime_imported": False, "panel_sha256": campaign["evaluation_panel_sha256"],
        "panel_cases": 396, "natural_cases": 108, "generated_cases": 288,
        "panel_ordered_ids_sha256": byte_sha("\n".join(row["id"] for row in panel) + "\n"),
        "controlling_selection": {"path": str(PILOT), "sha256": sha(PILOT), "lines": [438, 479],
            "eligibility_quote": "Natural failure-inclusive WER is strictly below RAW.",
            "ranking_quote": "lowest natural WER;",
            "scope_quote": "These are DEVELOPMENT viability screens, not H1 significance or final-paper acceptance gates.",
            "aggregation": "Pooled failure-inclusive corpus WER over the 108 frozen LS-PC DEVELOPMENT natural pairs; natural/generated denominators separate",
            "final_primary": "The final equal-domain LS-PC/SLUE H1 primary is a later scientific endpoint; SLUE is absent from this approved pilot panel.",
            "adoption_path": str(AMENDMENTS), "adoption_sha256": sha(AMENDMENTS)},
        "evaluation_reconstructions": []}
    if args.mode == "audit":
        paths = [args.receipt] if args.receipt else sorted(SAFE.glob("evaluation-*.attempt*.json"))
        for path in paths:
            evidence["evaluation_reconstructions"].append(audit_evaluation(path, campaign, panel, latents))
            print(json.dumps({"verified_evaluation": str(path), "cases": 396}), flush=True)
    evidence["decision"] = (decision(campaign, evidence["evaluation_reconstructions"])
        if args.mode == "audit" and args.receipt is None else
        {"status": "PREPARATION_OR_SINGLE_EVALUATION_NO_SELECTION", "selected_LR": None, "ranking": None})
    evidence["elapsed_seconds"] = time.perf_counter() - start
    evidence["accelerator_runtime_imported"] = any(name.split(".")[0] in ("mlx", "torch")
                                                   for name in sys.modules)
    require(not evidence["accelerator_runtime_imported"], "independent review imported an accelerator runtime")
    evidence["disposition"] = ("INDEPENDENT_METRICS_PREPARATION_COMPLETE_RESULTS_PENDING" if args.mode == "prepare"
        else "INDEPENDENT_METRICS_RECONSTRUCTED" if evidence["decision"]["status"] == "SIX_RESOLVED_OUTCOMES_RECONSTRUCTED"
        else "AVAILABLE_EVALUATIONS_RECONSTRUCTED_SIX_OUTCOMES_PENDING")
    attempt = 1
    while (SAFE / ("independent-metrics.attempt{:02d}.json".format(attempt))).exists():
        attempt += 1
    destination = SAFE / ("independent-metrics.attempt{:02d}.json".format(attempt))
    with destination.open("x") as stream:
        json.dump(evidence, stream, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"receipt_path": str(destination), "receipt_sha256": sha(destination),
                      "disposition": evidence["disposition"]}), flush=True)


if __name__ == "__main__":
    main()
