"""Complete G2 source/panel/ledger freeze; CPU only, with no exclusions."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import time

from src.data.g2_artifacts import ArtifactRoot, atomic_artifact, read_complete, sha256
from src.data.g2_corpus import canonical_hash, support_floor, text_hash, validate_census
from src.data.g2_geometry import actual_denominators, g2_lr, projection_hash, split_master


def lines(path):
    return [json.loads(line) for line in Path(path).open()]


def write(path, value):
    Path(path).write_text(json.dumps(value, sort_keys=True, allow_nan=False) + "\n")


def natural_view(pair, view, tokenizer):
    from src.data.mixed_reader_v3 import native_shape
    from src.scoring.text import lexical
    source = pair["target"] if view == "identity" else pair["source"]
    shape = native_shape(tokenizer, source, pair["target"], pair["target"])
    if shape is None:
        raise ValueError("required natural row exceeds common native capacity; ALL-OR-BLOCK")
    return {"variant_id": view + "/" + pair["id"], "record_id": pair["id"],
        "source_group_id": pair["source_group_id"], "view": view,
        "source": source, "anchor": pair["target"], "target": pair["target"],
        "source_sha256": text_hash(source), "anchor_sha256": text_hash(pair["target"]),
        "target_sha256": text_hash(pair["target"]), "source_equals_target": source == pair["target"],
        "lexical_source_equals_target": lexical(source) == lexical(pair["target"]),
        "operations": [], **shape}


def diagnostics(condition, natural, generated, ledger):
    chosen = []
    for stratum, equal in (("natural_lexical_error", False), ("natural_lexical_zero", True)):
        eligible = [row for row in natural if row["view"] == "natural"
            and row["lexical_source_equals_target"] == equal]
        key = lambda row: canonical_hash(["G2", 42, condition, stratum, row["record_id"]])
        if len(eligible) < 64:
            raise ValueError("required TRAIN diagnostic stratum insufficient; no replacement")
        for row in sorted(eligible, key=key)[:64]:
            chosen.append({"id": row["variant_id"], "variant_id": row["variant_id"],
                "stratum": stratum, "selection_sha256": key(row), "population": "TRAIN_DIAGNOSTIC"})
            chosen.append({"id": "identity/" + row["record_id"],
                "variant_id": "identity/" + row["record_id"], "stratum": stratum + "/identity",
                "selection_sha256": key(row), "population": "TRAIN_DIAGNOSTIC_IDENTITY"})
    from src.generation.stress import CATEGORIES
    present = {item["variant_id"] for item in ledger}
    bases = {row["base_id"] for row in generated if row["variant_id"] in present}
    for category in CATEGORIES:
        for cell in range(3):
            eligible = {row["base_id"] for row in generated
                if row["category"] == category and row["cell"] == cell and row["base_id"] in bases}
            stratum = f"generated/{category}/{cell}"
            key = lambda base: canonical_hash(["G2", 42, condition, stratum, base])
            if not eligible:
                raise ValueError("required generated diagnostic base missing from actual ledger")
            base = min(eligible, key=key)
            for view in ("clean", "mixed"):
                matches = [row for row in generated if row["base_id"] == base and row["view"] == view]
                if len(matches) != 1:
                    raise ValueError("generated diagnostic view identity ambiguous")
                row = matches[0]
                chosen.append({"id": row["variant_id"], "variant_id": row["variant_id"],
                    "stratum": stratum + "/" + view, "selection_sha256": key(base),
                    "base_id": base, "population": "TRAIN_GENERATED_DIAGNOSTIC"})
    if len(chosen) != 304 or len({row["id"] for row in chosen}) != 304:
        raise ValueError("304 unique diagnostic cases required")
    return chosen


def geometry(rows, ledger, updates, data_condition):
    from src.data.g2_stream import G2ScientificStream
    actual = {"U1": [], "U8": []}
    for condition in actual:
        cursor = G2ScientificStream(rows, ledger, updates, data_condition, condition)
        completed = 0
        for index, master in enumerate(updates):
            queue = [{**item, "row": rows[item["variant_id"]]}
                for item in ledger[master["first_ordinal"]:master["last_ordinal"] + 1]]
            parts = split_master(queue, condition)
            if [item for part in parts for item in part] != queue:
                raise ValueError("U8 concatenation changes the immutable U1 stream")
            for sub, part in enumerate(parts):
                if cursor.actual_queue() != part:
                    raise ValueError("sequential scientific cursor changed a frozen actual update")
                restored = G2ScientificStream(rows, ledger, updates, data_condition, condition)
                restored.restore(cursor.state())
                if restored.actual_queue() != part or restored.completed_actual_clock() != cursor.completed_actual_clock():
                    raise ValueError("CPU scientific cursor restore changed its actual queue/clock")
                charge = sum(item["canonical_charge"] for item in part)
                completed += charge
                actual[condition].append({"master_index": index, "subqueue_index": sub,
                    "optimizer_step_index": len(actual[condition]) + 1,
                    "first_ordinal": part[0]["ordinal"], "last_ordinal": part[-1]["ordinal"],
                    "examples": len(part), "canonical_charge": charge,
                    "completed_actual_exposure": completed, "lr": g2_lr(completed),
                    "denominators": actual_denominators(part),
                    "microbatch_partitions": {arm: [[i, min(i + size, len(part))]
                        for i in range(0, len(part), size)] for arm, size in (("B100", 16), ("C101", 4))}})
                cursor.finish_actual()
        if completed != ledger[-1]["end_exposure"]:
            raise ValueError("actual-update clock fails master endpoint")
        if cursor.completed_actual_clock() != (len(actual[condition]), completed):
            raise ValueError("CPU scientific cursor full endpoint mismatch")
    return actual


def run(binding, attempt):
    root = ArtifactRoot(binding); before = root.preflight(); started = time.perf_counter()
    if attempt < 1:
        raise ValueError("positive corpus attempt required")
    receipt = Path(f"experiments/manifests/generation_2/corpus-freeze.attempt{attempt:02d}.json")
    if receipt.exists():
        raise FileExistsError(receipt)
    source = root.path("asr-hypotheses-v1/construction.attempt01")
    read_complete(source)
    pairs = lines(source / "pairs.jsonl"); validate_census(pairs)
    metadata = {row["id"]: row for row in lines("experiments/manifests/generation_2/metadata-census.attempt01.jsonl")}
    if set(metadata) != {row["id"] for row in pairs}:
        raise ValueError("completed sources differ from the prospectively published census")
    for row in pairs:
        public = metadata[row["id"]]
        if any((len(row["target"].encode()) if key == "target_bytes" else row[key]) != value
               for key, value in public.items()):
            raise ValueError("published census member/reference/role/family identity changed")
    if any(row["status"] != "COMPLETED" or text_hash(row["source"]) != row["source_sha256"] for row in pairs):
        raise ValueError("all completed source identities required")
    report = {"schema": "g2_complete_corpus_freeze_v1", "attempt": attempt, "seed": 42,
        "code_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "captured_dirty_status": subprocess.check_output(["git", "status", "--porcelain"], text=True),
        "code_sha256": sha256(__file__), "pairs_sha256": sha256(source / "pairs.jsonl"),
        "source_hashes":{name:sha256(name) for name in ("src/data/g2_artifacts.py",
            "src/data/g2_corpus.py","src/data/g2_geometry.py","src/data/g2_stream.py",
            "src/data/g2_byt5.py","src/data/mixed_reader_v3.py",
            "benchmarks/paired_qualification_v3.py","src/models/tokenizer.py",
            "src/models/edits.py","src/scoring/text.py")},
        "before": before, "scientific_recipes_started": 0, "status": "RUNNING"}
    try:
        from benchmarks.paired_qualification_v3 import common
        from src.data.g2_byt5 import accounting_plan, validate_pairs
        from src.data.lexical_corruption_v2 import serialized
        from src.data.mixed_reader_v3 import MixedReader, PHASE_ENDS, native_shape
        from src.models.tokenizer import ByteBPE
        from src.scoring.text import lexical
        tokenizer = ByteBPE.load("configs/tokenizer_development")
        train = [row for row in pairs if row["role"] == "train"]
        development = [row for row in pairs if row["role"] != "train"]
        support = support_floor(development); report["development_support"] = support
        if not support["pass"]:
            raise ValueError("expanded DEVELOPMENT support floor failed")
        validate_pairs(train); report["byt5_accounting"] = accounting_plan(train)
        old_rows, old_ledger, old_updates, _, old_ids = common()
        generated = [row for row in old_rows.values() if "category" in row]
        old_natural = [row for row in old_rows.values() if "record_id" in row]
        expanded = [natural_view(row, view, tokenizer) for view in ("identity", "natural") for row in train]
        expanded_lookup = {row["variant_id"]: row for row in expanded}
        if any(serialized(row) != serialized(expanded_lookup[row["variant_id"]]) for row in old_natural):
            raise ValueError("original 1024 native pair views changed")
        old_panel = json.loads(Path("exports/lexical-reader-v2/pilot-preparation-attempt01/development-panel.json").read_text())
        panel = []
        for pair in development:
            shape = native_shape(tokenizer, pair["source"], pair["target"], pair["target"])
            if shape is None:
                raise ValueError("required natural DEVELOPMENT native capacity failure")
            panel.append({"id": pair["id"], "role": pair["role"], "source_group_id": pair["source_group_id"],
                "official_split": pair["official_split"], "families": pair["families"],
                "population": "natural", "source": pair["source"], "target": pair["target"],
                "source_sha256": pair["source_sha256"], "target_sha256": text_hash(pair["target"]),
                "native_admitted": True, "shape": shape, "legacy_subset": pair["legacy_reused"]})
        panel.extend(row for row in old_panel if row["population"] == "generated")
        if len(panel) != 2984 or sum(row.get("legacy_subset", False) for row in panel) != 108:
            raise ValueError("expanded/legacy DEVELOPMENT panel count mismatch")
        table = json.loads(Path("experiments/manifests/lexical_reader_v2/lexical-profile-table.attempt01.json").read_text())
        corpus_summary = {}
        for condition, natural in (("D0", old_natural), ("D1", expanded)):
            relative = f"{'frozen-d1-v1' if condition == 'D1' else 'corpus-qualification-v1'}/{condition}.attempt{attempt:02d}"
            lookup = {row["variant_id"]: row for row in [*generated, *natural]}
            with atomic_artifact(root, relative) as out:
                with (out / "natural.jsonl").open("x") as stream:
                    for row in natural: stream.write(json.dumps(row, sort_keys=True) + "\n")
                if condition == "D0":
                    ledger, updates = old_ledger, old_updates
                else:
                    reader = MixedReader(generated, [row for row in natural if row["view"] == "identity"],
                        [row for row in natural if row["view"] == "natural"],
                        {i: table["severity_P1_P2"][str(i)] for i in (1, 2)})
                    ledger, updates = [], []
                    fingerprints = {key: hashlib.sha256(serialized(value)).hexdigest() for key, value in lookup.items()}
                    while reader.exposure < PHASE_ENDS[-1]:
                        queue = reader.queue(); phase_segments = Counter(); channel_charges = Counter()
                        for item in queue:
                            row = item["row"]; frozen = {key: value for key, value in item.items() if key != "row"}
                            frozen.update({key: row[key] for key in ("source_sha256", "target_sha256", "anchor_sha256")})
                            frozen["accepted_row_sha256"] = fingerprints[row["variant_id"]]
                            ledger.append(frozen); phase_segments[item["phase"]] += item["canonical_charge"]
                            channel_charges[item["channel"]] += item["canonical_charge"]
                        den = actual_denominators(queue)
                        updates.append({"update": len(updates), "first_ordinal": queue[0]["ordinal"],
                            "last_ordinal": queue[-1]["ordinal"], "start_exposure": queue[0]["start_exposure"],
                            "end_exposure": reader.exposure, "canonical_charge": sum(item["canonical_charge"] for item in queue),
                            "examples": len(queue), "phase_segments": dict(phase_segments),
                            "channel_charges": dict(channel_charges), "B_denominator": den["B"], "C_denominators": den["C"]})
                    write(out / "reader-final-state.json", reader.state())
                with (out / "presentations.jsonl").open("x") as stream:
                    for row in ledger: stream.write(json.dumps(row, sort_keys=True) + "\n")
                write(out / "masters.json", updates)
                actual = geometry(lookup, ledger, updates, condition); write(out / "actual-updates.json", actual)
                diagnostic = diagnostics(condition, natural, generated, ledger); write(out / "diagnostics.json", diagnostic)
                if condition == "D0" and (len(updates), ledger[-1]["end_exposure"], ledger[-1]["ordinal"]) != (305, 10007223, 134590):
                    raise ValueError("D0 endpoint no longer reproduces G1")
                natural_real = [row for row in natural if row["view"] == "natural"]
                E = sum(not row["lexical_source_equals_target"] for row in natural_real)
                stats = {"condition": condition, "natural_train_rows": len(natural_real), "lexical_error_rows": E,
                    "lexical_zero_rows": len(natural_real)-E,
                    "lexical_error_groups": len({row["source_group_id"] for row in natural_real if not row["lexical_source_equals_target"]}),
                    "master_count": len(updates), "actual_exposure": ledger[-1]["end_exposure"],
                    "final_ordinal": ledger[-1]["ordinal"], "U1_updates": len(actual["U1"]), "U8_updates": len(actual["U8"]),
                    "U8_charge_min": min(row["canonical_charge"] for row in actual["U8"]),
                    "U8_charge_max": max(row["canonical_charge"] for row in actual["U8"]),
                    "projection_sha256": projection_hash(ledger), "diagnostic_count": len(diagnostic),
                    "ledger_sha256": sha256(out / "presentations.jsonl"), "natural_sha256": sha256(out / "natural.jsonl"),
                    "diagnostics_sha256": sha256(out / "diagnostics.json"),
                    "actual_updates_sha256": sha256(out / "actual-updates.json"),
                    "generated_pool_sha256": old_ids["exports/lexical-reader-v2/generated-pool-attempt02/accepted.jsonl"],
                    "target_bpe_per_full_pass": sum(len(row["target_ids"]) for row in natural_real),
                    "canonical_exposure_per_full_natural_pass": sum(row["canonical_charge"] for row in natural_real),
                    "maximum_target_bpe": max(len(row["target_ids"]) for row in natural_real),
                    "masters_sha256": sha256(out / "masters.json"),
                    "scope": "CPU_ONLY_FROZEN_SCIENTIFIC_INPUTS_UNSTARTED"}
                if condition == "D1" and (stats["target_bpe_per_full_pass"],
                        stats["canonical_exposure_per_full_natural_pass"],stats["maximum_target_bpe"]) != (325630,721825,56):
                    raise ValueError("canonical accepted D1 reference token census changed")
                write(out / "summary.json", stats)
            corpus_summary[condition] = {**stats, "artifact_relative": relative}
        relative = f"expanded-development-v1/panel.attempt{attempt:02d}"
        with atomic_artifact(root, relative) as out:
            write(out / "panel.json", panel)
            report["panel_sha256"] = sha256(out / "panel.json")
            report["panel_relative"] = relative
            write(out / "support.json", support)
        report.update(status="PASS_COMPLETE_G2_CORPUS_PANEL_GEOMETRY_FREEZE", conditions=corpus_summary,
            panel_cases=2984, old_natural_development=108, after=root.preflight())
        campaign=json.loads(Path("experiments/manifests/six_10m_probes/campaign-freeze.attempt01.json").read_text())
        recipes=[]
        for data,update_condition in (("D0","U8"),("D1","U1"),("D1","U8")):
            artifact=root.path(corpus_summary[data]["artifact_relative"])
            masters=json.loads((artifact/"masters.json").read_text())
            def endpoint(nominal):
                if nominal==0:return {"nominal_exposure":0,"master_completed":0,"optimizer_updates":0,"actual_exposure":0,"last_ordinal":-1}
                index=next(i for i,row in enumerate(masters) if row["end_exposure"]>=nominal)
                row=masters[index]
                return {"nominal_exposure":nominal,"master_completed":index+1,
                    "optimizer_updates":(index+1)*(8 if update_condition=="U8" else 1),
                    "actual_exposure":row["end_exposure"],"last_ordinal":row["last_ordinal"]}
            for arm in ("B100","C101"):
                recipe_id=f"G2-{arm}-{data}-{update_condition}-seed42-lr3e-4"
                config={"schema":"g2_frozen_scientific_recipe_v1","recipe_id":recipe_id,"status":"AUTHORIZED_UNSTARTED",
                    "seed":42,"arm":arm,"data_condition":data,"update_condition":update_condition,
                    "model":campaign["models"][arm],"peak_lr":3e-4,"microbatch_size":16 if arm=="B100" else 4,
                    "precision":campaign["precision"],"nominal_exposure":10000000,
                    "phase_absolute_ends":[6666667,9333334,10000000],"update_target_master":32768,
                    "LR_clock":{"warmup_exposure":200000,"planned_exposure":10000000,"floor_fraction":.1,
                        "sample_at":"completed actual optimizer update exposure","phase_resets":False},
                    "corpus_geometry":corpus_summary[data],"development_panel_sha256":report["panel_sha256"],
                    "save_endpoints":[endpoint(n) for n in sorted({0,*range(1000000,10000001,1000000),6666667,9333334})],
                    "evaluation_endpoints":[endpoint(n) for n in (0,1000000,3000000,6666667,9333334,10000000)],
                    "stop_endpoint":endpoint(10000000),"scientific_slot_consumed":False,
                    "checkpoint_area":"scientific-checkpoints-v1","qualification_initializers_forbidden":True,
                    "execution_requires_separate_owner_session":True}
                path=Path(f"experiments/manifests/generation_2/recipe-{recipe_id}.attempt{attempt:02d}.json")
                if path.exists():raise FileExistsError(path)
                write(path,config);recipes.append({"recipe_id":recipe_id,"status":"AUTHORIZED_UNSTARTED","config_relative":str(path),"config_sha256":sha256(path)})
        recipe_id="G2-ByT5-D1-10pass-seed42-lr3e-4"
        config={"schema":"g2_frozen_byt5_recipe_v1","recipe_id":recipe_id,"status":"AUTHORIZED_UNSTARTED",
            "model":"google/byt5-small","revision":"68377bdc18a2ffec8a0533fef03b1c513a4dd49d","parameter_count":299637760,
            "seed":42,"prefix":"","lr":3e-4,"device":"FP32 MPS eager; CPU fallback disabled",
            "source_capacity":512,"target_capacity":512,"decode_cap":512,"accounting":report["byt5_accounting"],
            "optimizer":{"beta1":.9,"beta2":.999,"epsilon":1e-8,"weight_decay":.01,"clip":1.},
            "save_evaluate_pass_milestones":[0,2,5,10],"scientific_slot_consumed":False,
            "qualification_initializers_forbidden":True,"execution_requires_separate_owner_session":True}
        path=Path(f"experiments/manifests/generation_2/recipe-{recipe_id}.attempt{attempt:02d}.json")
        if path.exists():raise FileExistsError(path)
        write(path,config);recipes.append({"recipe_id":recipe_id,"status":"AUTHORIZED_UNSTARTED","config_relative":str(path),"config_sha256":sha256(path)})
        report["recipes"]=recipes
    except BaseException as error:
        report.update(status="FAILED_ALL_OR_BLOCK", error_type=type(error).__name__)
        raise
    finally:
        report["elapsed_seconds"] = time.perf_counter()-started
        write(receipt, report)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--artifact-binding", required=True)
    parser.add_argument("--attempt", type=int, required=True); args = parser.parse_args()
    result = run(args.artifact_binding, args.attempt)
    print(json.dumps({key: result[key] for key in ("status", "elapsed_seconds")}), flush=True)
