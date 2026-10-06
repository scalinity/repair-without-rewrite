"""Execute the six authorized DEVELOPMENT recipes around the frozen native trainer."""
import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
import gc
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import random
import resource
import signal
import subprocess
import time

from benchmarks.paired_qualification_v3 import (
    common, exact_queue, frozen_queue, evaluation_timing, runtime_identities, sha, system_snapshot,
)
from src.data.lexical_corruption_v2 import serialized
from src.generation.stress import score as generated_score
from src.models.tokenizer import ByteBPE
from src.scoring.records import aggregate
from src.scoring.text import lexical

SAFE = Path("experiments/manifests/six_10m_probes")
PRIVATE = Path("exports/six-10m-probes")
FREEZE = SAFE / "campaign-freeze.attempt01.json"
AUTHORIZED = "7868302afc43e3cbd475464452f57912a9c2cf97"
PANEL = Path("exports/lexical-reader-v2/pilot-preparation-attempt01/development-panel.json")
LATENTS = Path("experiments/manifests/stress_split_repair_20261005T054436Z/latents.jsonl")
ORDER = [(arm, peak) for peak in (1e-4, 3e-4, 6e-4) for arm in ("B100", "C101")]


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(path)
    temporary = path.with_suffix(path.suffix + ".partial")
    with temporary.open("xb") as stream:
        stream.write(serialized(value))
        stream.flush()
        os.fsync(stream.fileno())
    os.rename(temporary, path)


def trainer_for(arm, peak, identities):
    import mlx.core as mx
    from src.models.bc import B100, C101
    from src.models.core import parameter_inventory
    from src.models.paired_training_v3 import PairedTrainer
    model = B100(seed=42) if arm == "B100" else C101(seed=42)
    expected = 100686336 if arm == "B100" else 101081859
    if sum(item["count"] for item in parameter_inventory(model)) != expected:
        raise ValueError("frozen architecture parameter count changed")
    trainer = PairedTrainer(model, arm, identities, microbatch_size=16 if arm == "B100" else 4,
        peak_lr=peak)
    mx.eval(trainer.arrays())
    return trainer


def tensor_hash(trainer, prefix):
    import numpy as np
    h = hashlib.sha256()
    for key, value in sorted(trainer.arrays().items()):
        if not key.startswith(prefix):
            continue
        array = np.asarray(value)
        h.update(json.dumps([key, list(array.shape), str(array.dtype)], separators=(",", ":")).encode())
        h.update(array.tobytes())
    return h.hexdigest()


def sparse_exact(path, expected):
    """Keep the exact checkpoint bytes while avoiding physical zero-filled blocks."""
    path = Path(path)
    temporary = path.with_name(path.name + ".sparse-partial")
    with path.open("rb") as source, temporary.open("xb") as target:
        while block := source.read(65536):
            if block.count(0) == len(block):
                target.seek(len(block), 1)
            else:
                target.write(block)
        target.truncate(source.tell())
        target.flush()
        os.fsync(target.fileno())
    if sha(temporary) != expected or sha(path) != expected:
        raise ValueError("sparse checkpoint copy changed logical bytes")
    os.replace(temporary, path)
    return {"logical_bytes": path.stat().st_size, "physical_bytes": path.stat().st_blocks * 512,
        "sha256": expected, "logical_bytes_preserved": True}


def freeze():
    import mlx.core as mx
    SAFE.mkdir(exist_ok=True)
    PRIVATE.mkdir(exist_ok=True)
    rows, ledger, updates, reader, data = common()
    identities = runtime_identities(data)
    if sha(PANEL) != "5043ed60d6ce8f891ee8e30255fabaa40fcac37b0a043c1a85dd88178832ce4e":
        raise ValueError("frozen panel identity changed")
    if len(updates) != 305 or updates[-1]["end_exposure"] != 10007223 or updates[-1]["last_ordinal"] != 134590:
        raise ValueError("common endpoint identity changed")
    recipes = []
    definitions = {}
    for arm in ("B100", "C101"):
        trainer = trainer_for(arm, 1e-4, identities)
        definitions[arm] = {"config": asdict(trainer.model.config),
            "parameter_count": 100686336 if arm == "B100" else 101081859,
            "initial_parameter_sha256": tensor_hash(trainer, "model::"),
            "initial_optimizer_sha256": tensor_hash(trainer, "m::") + ":" + tensor_hash(trainer, "v::"),
            "optimizer": trainer.optimizer.policy(), "microbatch_examples": trainer.microbatch_size}
        del trainer
        gc.collect()
        mx.clear_cache()
    for arm, peak in ORDER:
        path = Path(f"experiments/manifests/lexical_reader_v2/pilot-{arm}-seed42-lr{peak:.0e}.json")
        config = json.loads(path.read_text())
        if config["probe_slot_consumed"] or config["arm"] != arm or config["peak_lr"] != peak:
            raise ValueError("recipe identity or slot state changed")
        if any(sha(p) != h for p, h in config["data_identities"].items()):
            raise ValueError("recipe data binding changed")
        recipes.append({"recipe_id": path.stem.removeprefix("pilot-"), "status": "AUTHORIZED_UNSTARTED",
            "config_path": str(path), "config_sha256": sha(path), "config": config})
    source_paths = sorted({*identities["code"], *map(str, Path("src").rglob("*.py")),
        *map(str, Path("docs/design-inputs/unicode-15.1.0").glob("*.txt")),
        "benchmarks/six_10m_campaign.py", "uv.lock", "pyproject.toml"})
    value = {"schema": "six_10m_development_campaign_v1", "authorized_checkpoint": AUTHORIZED,
        "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_status_at_freeze": subprocess.check_output(["git", "status", "--porcelain"], text=True),
        "source_hashes": {p: sha(p) for p in source_paths}, "runtime_identities": identities,
        "data_identities": data, "evaluation_panel_path": str(PANEL), "evaluation_panel_sha256": sha(PANEL),
        "generated_evaluation_latents_sha256": sha(LATENTS), "evaluation_population": {"natural":108,"generated":288},
        "models": definitions, "seed":42, "recipes":recipes, "execution_order": [r["recipe_id"] for r in recipes],
        "order_reason":"No frozen field prescribes execution order; prospectively alternate arms within ascending peak LR",
        "precision":{"master":"float32","moments":"float32","accumulation":"float32","working":"bfloat16","TF32":"0"},
        "checkpoint_policy":"13 frozen endpoints; atomic native save/readback; exact sparse logical bytes; interruption after completed microbatch",
        "numerical_failure_policy":"Preserve attempt; one exact replay from last verified checkpoint; second numerical failure marks FAILED; no treatment change",
        "defect_policy":"Stop affected campaign; preserve artifacts; PROBE_CAMPAIGN_REPAIR_REQUIRED or FRONTIER_MODEL_REVIEW_REQUIRED",
        "selection":{"endpoint_only":10000000,"eligibility":["resolved prescribed completion","natural WER strictly below RAW","positive completed repair lower bound","completed repair supported in at least two source groups","at least one genuine generated required repair"],
            "lexicographic":["natural WER ascending","introduced rate upper ascending","completed repair lower descending","natural invalid/incomplete ascending","generated mixed success descending","peak LR ascending"],"comparison":"exact integer/rational independently within each arm"},
        "caps":{"source_context":1024,"decode_positions":256,"C_edits":64},
        "runtime":{"python":platform.python_version(), **{p:importlib.metadata.version(p) for p in ("mlx","numpy","pytest")}},
        "hardware":{"platform":platform.platform(),"chip":subprocess.check_output(["sysctl","-n","machdep.cpu.brand_string"],text=True).strip(),"memory_bytes":int(subprocess.check_output(["sysctl","-n","hw.memsize"],text=True)),"logical_cpus":os.cpu_count()},
        "baseline_receipt_sha256":sha(SAFE/"baseline-validation.attempt01.json"),
        "owner_ledger_correction_receipt_sha256":sha(SAFE/"preflight-identities.attempt02.json"),
        "save_endpoints":recipes[0]["config"]["save_endpoints"],"evaluation_endpoints":recipes[0]["config"]["evaluation_endpoints"],
        "scientific_recipe_slots_consumed":0,"final_training_started":False,"sealed_inference_performed":False,"paper_protocol_v2_frozen":False,
        "disposition":"SIX_RECIPES_AUTHORIZED_UNSTARTED"}
    write(FREEZE,value)
    print(json.dumps({"campaign_sha256":sha(FREEZE),"models":definitions,"recipes":len(recipes)}),flush=True)


def summarize_evaluation(path, panel, nominal, endpoint, recipe_id):
    records = [json.loads(line) for line in Path(path).read_text().splitlines()]
    if [r["id"] for r in records] != [r["id"] for r in panel]:
        raise ValueError("evaluation IDs/order differ from frozen panel")
    lookup = {r["id"]:r for r in panel}
    natural = [r for r in records if r["population"] == "natural"]
    gen = [r for r in records if r["population"] == "generated"]
    if len(natural) != 108 or len(gen) != 288:
        raise ValueError("frozen evaluation denominator changed")
    result = aggregate(r["score"] for r in natural)
    result["RAW_WER"] = result["source_errors"] / result["reference_words"]
    result["repair_support_source_groups_lower"] = sorted({lookup[r["id"]]["source_group_id"] for r in natural if r["score"]["completed_repair"][0] > 0})
    result["repair_support_source_groups_upper"] = sorted({lookup[r["id"]]["source_group_id"] for r in natural if r["score"]["completed_repair"][1] > 0})
    result["source_byte_identity"] = sum(r["score"]["complete_valid"] and r["output"] == lookup[r["id"]]["source"] for r in natural)
    result["source_lexical_identity"] = sum(r["score"]["complete_valid"] and lexical(r["output"]) == lexical(lookup[r["id"]]["source"]) for r in natural)
    result["source_correct_counts"] = sum((r["score"]["source_consensus_eligible_counts"] or {}).get("correct",0) for r in natural)
    covered = [r for r in natural if r["score"]["fixed_correct_damage"] is not None]
    covered_correct = sum((r["score"]["source_consensus_eligible_counts"] or {}).get("correct",0) for r in covered)
    covered_damage = [sum(r["score"]["fixed_correct_damage"][i] for r in covered) for i in (0,1)]
    result["source_correct_preservation_coverage"] = {"covered_cases":len(covered),"unavailable_cases":108-len(covered),"covered_correct_counts":covered_correct,"covered_damage_bounds":covered_damage,"covered_preserved_bounds":[covered_correct-covered_damage[i] for i in (1,0)]}
    result["source_correct_damage_bounds"] = covered_damage if len(covered)==108 else None
    result["source_correct_preserved_bounds"] = [covered_correct-covered_damage[i] for i in (1,0)] if len(covered)==108 else None
    result["target_byte_exact"] = sum(r["score"]["raw_byte_exact"] for r in natural)
    result["target_lexical_exact"] = sum(r["score"]["lexical_exact"] for r in natural)
    result["scorer_caps"] = sum(r["score"]["fallback_reason"] is not None for r in natural)
    result["repair_width"] = sum(r["score"]["repair"][1]-r["score"]["repair"][0] for r in natural)
    result["introduced_width"] = sum(r["score"]["introduced"][1]-r["score"]["introduced"][0] for r in natural)
    result["status_counts"] = dict(Counter(r["status"] for r in natural))
    generated_ids = {r["id"] for r in panel if r["population"] == "generated"}
    latents = {r["case_id"]:r for r in map(json.loads,LATENTS.read_text().splitlines()) if r["case_id"] in generated_ids}
    if set(latents) != generated_ids or any(r["partition"] != "dev" for r in latents.values()):
        raise ValueError("generated scorer must use exactly frozen DEVELOPMENT latents")
    generated = {"cases":288,"complete":0,"structure_invalid":0,"invalid_or_incomplete":0,"required_repair_fields_completed":0,"required_repair_cases_completed":0,"whole_case_conformance":0,"mixed_success":0,"by_view":{},"by_category_view":{}}
    for r in gen:
        latent = latents[r["id"]]
        scored = generated_score(latent,r["output"],complete=r["score"]["complete_valid"])
        generated["complete"] += scored["complete"]
        generated["structure_invalid"] += not scored["structure_valid"]
        generated["invalid_or_incomplete"] += not (scored["complete"] and scored["structure_valid"])
        generated["required_repair_fields_completed"] += scored["repaired"]
        generated["required_repair_cases_completed"] += scored["repaired"] > 0
        generated["whole_case_conformance"] += scored["whole_case_conformance"]
        generated["mixed_success"] += scored["mixed_success"]
        for mapping,key in ((generated["by_view"],latent["view_kind"]),(generated["by_category_view"],latent["primary_category"]+":"+latent["view_kind"])):
            counts = mapping.setdefault(key,{"cases":0,"complete":0,"invalid_or_incomplete":0,"status_counts":{},"conformant":0,"preserved_fields":0,"preserve_denominator":0,"repaired_fields":0,"repair_denominator":0})
            counts["cases"] += 1
            counts["complete"] += scored["complete"]
            counts["invalid_or_incomplete"] += not (scored["complete"] and scored["structure_valid"])
            counts["status_counts"][r["status"]] = counts["status_counts"].get(r["status"],0)+1
            counts["conformant"] += scored["whole_case_conformance"]
            for name,source in (("preserved_fields","preserved"),("preserve_denominator","preserve_denominator"),("repaired_fields","repaired"),("repair_denominator","repair_denominator")):
                counts[name] += scored[source]
    generated["decoder_invalid_or_incomplete"] = 288-generated["complete"]
    value={"recipe_id":recipe_id,"nominal_endpoint":nominal,"actual_endpoint":endpoint,
        "panel_sha256":sha(PANEL),"output_sha256":sha(path),"natural":result,"generated":generated,
        "resources":{"decoder_positions":sum(r["decoder_positions"] for r in records),"decode_seconds":sum(r["decode_seconds"] for r in records),"scorer_seconds":sum(r["scorer_seconds"] for r in records),"by_population":{pop:{"positions":sum(r["decoder_positions"] for r in records if r["population"]==pop),"decode_seconds":sum(r["decode_seconds"] for r in records if r["population"]==pop)} for pop in ("natural","generated")}},
        "DET":"UNMEASURED_ON_THIS_PANEL","disposition":"FROZEN_DEVELOPMENT_EVALUATION_COMPLETE"}
    return value


def run(recipe_id, resume=None):
    import mlx.core as mx
    import numpy as np
    from src.models.paired_training_v3 import save_paired_checkpoint, load_paired_checkpoint
    campaign = json.loads(FREEZE.read_text())
    recipe = next(r for r in campaign["recipes"] if r["recipe_id"] == recipe_id)
    if any(sha(path) != digest for path,digest in campaign["source_hashes"].items()):
        raise ValueError("campaign runtime/source hash changed")
    if (sha(recipe["config_path"]) != recipe["config_sha256"] or sha(PANEL) != campaign["evaluation_panel_sha256"]
            or sha(LATENTS) != campaign["generated_evaluation_latents_sha256"]):
        raise ValueError("campaign config/panel hash changed")
    prior = list(SAFE.glob("recipe-*.attempt*.json"))
    consumed = {json.loads(p.read_text())["recipe_id"] for p in prior}
    expected_prefix = campaign["execution_order"][:campaign["execution_order"].index(recipe_id)]
    if consumed != set(expected_prefix):
        raise ValueError("execution order/slot accounting violation")
    if any(json.loads(p.read_text()).get("status") not in ("COMPLETED","FAILED") for p in prior):
        raise ValueError("previous recipe is not resolved")
    if subprocess.check_output(["git","status","--porcelain"],text=True):
        raise ValueError("each recipe requires a clean captured start")
    config = recipe["config"]
    arm,peak = config["arm"],config["peak_lr"]
    rows,ledger,updates,reader,data = common()
    if data != campaign["data_identities"]:
        raise ValueError("campaign frozen data identities changed")
    identities = runtime_identities(data)
    identities["campaign_sha256"] = sha(FREEZE)
    identities["recipe_config_sha256"] = recipe["config_sha256"]
    if identities["runtime"] != campaign["runtime_identities"]["runtime"]:
        raise ValueError("qualified runtime changed")
    panel = json.loads(PANEL.read_text())
    saves = {r["update"]:r for r in config["save_endpoints"]}
    evaluations = {r["update"]:r for r in config["evaluation_endpoints"]}
    latest = None if resume is None else Path(resume)
    if latest is not None and latest.parent.parent != PRIVATE/recipe_id:
        raise ValueError("resume checkpoint belongs to another recipe")
    previous_attempts = list((PRIVATE/recipe_id).glob("attempt*"))
    if previous_attempts and resume is None:
        raise ValueError("partial recipe exists; resume it rather than restart from scratch")
    base_attempt = 1+max((int(p.name.removeprefix("attempt")) for p in previous_attempts),default=0)
    previous_failures = [json.loads(p.read_text()) for p in SAFE.glob(f"failure-{recipe_id}.attempt*.json")]
    numerical_failures = sum(f["disposition"] == "NUMERICAL_FAILURE" for f in previous_failures)
    if any(f["disposition"] != "NUMERICAL_FAILURE" for f in previous_failures) or numerical_failures >= 2:
        raise ValueError("recorded defect/repeated numerical failure blocks execution")
    stop_requested = []
    def request_stop(signum, frame):
        stop_requested.append(signum)
    for signum in (signal.SIGINT, signal.SIGTERM):
        signal.signal(signum,request_stop)
    started = time.time()
    for attempt in range(base_attempt,base_attempt+2-numerical_failures):
        _, _, _, reader, replay_data = common()
        if replay_data != data:
            raise ValueError("replay data identities changed")
        out = PRIVATE / recipe_id / f"attempt{attempt:02d}"
        out.mkdir(parents=True,exist_ok=False)
        start = time.perf_counter()
        trainer = trainer_for(arm,peak,identities)
        initial_hash = tensor_hash(trainer,"model::")
        if initial_hash != campaign["models"][arm]["initial_parameter_sha256"]:
            raise ValueError("seed42 initialization identity changed")
        preflight={"recipe_id":recipe_id,"attempt":attempt,"head":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),"dirty_status":subprocess.check_output(["git","status","--porcelain"],text=True),"config_sha256":recipe["config_sha256"],"campaign_sha256":sha(FREEZE),"initial_parameter_sha256":initial_hash,"runtime_identities":identities,"hardware":campaign["hardware"],"output_directory":str(out),"resume_path":None if latest is None else str(latest),"seed":42,"start_unix":time.time(),"no_concurrent_accelerator":True}
        write(out/"preflight.json",preflight)
        write(SAFE/f"start-{recipe_id}.attempt{attempt:02d}.json",{**preflight,"status":"STARTED"})
        endpoints = []
        try:
            if latest is None:
                trainer.reader_state = reader.state()
            else:
                meta=load_paired_checkpoint(trainer,latest,rows)
                reader.restore(meta["reader_state"])
                restored_receipt = json.loads(latest.with_name(latest.name+"-receipt.json").read_text())
                endpoints.append(restored_receipt)
                summary = restored_receipt["last_update_metrics"]
            with (out/"updates.jsonl").open("x") as stream:
                fresh_endpoint = latest is None
                while True:
                    index=trainer.optimizer.step
                    if index in saves and fresh_endpoint:
                        point=saves[index]
                        checkpoint=out/f"checkpoint-update{index:03d}"
                        manifest=save_paired_checkpoint(trainer,checkpoint,rows[ledger[0]["variant_id"]])
                        storage=sparse_exact(checkpoint/"arrays.npz",manifest["arrays.npz"])
                        latest=checkpoint
                        endpoint={**point,"recipe_id":recipe_id,"arm":arm,"peak_lr":peak,"seed":42,"phase":reader.phase,"parameter_sha256":tensor_hash(trainer,"model::"),"optimizer_sha256":{"m":tensor_hash(trainer,"m::"),"v":tensor_hash(trainer,"v::")},"checkpoint_complete_sha256":sha(checkpoint/"COMPLETE.json"),"checkpoint_path":str(checkpoint),"storage":storage,"lr":trainer.clock,"last_update_metrics":None if index==0 else summary,"failure_state":"NONE","runtime_identities":identities}
                        write(out/f"checkpoint-update{index:03d}-receipt.json",endpoint)
                        endpoints.append(endpoint)
                    if stop_requested:
                        if not (out/f"checkpoint-update{index:03d}").exists():
                            checkpoint=out/f"interruption-update{index:03d}"
                            manifest=save_paired_checkpoint(trainer,checkpoint,rows[ledger[0]["variant_id"]])
                            storage=sparse_exact(checkpoint/"arrays.npz",manifest["arrays.npz"])
                            endpoint={"recipe_id":recipe_id,"update":index,"canonical_exposure":trainer.committed_exposure,"checkpoint_path":str(checkpoint),"parameter_sha256":tensor_hash(trainer,"model::"),"last_update_metrics":None if index==0 else summary,"storage":storage}
                            write(checkpoint.with_name(checkpoint.name+"-receipt.json"),endpoint)
                        else:
                            checkpoint=out/f"checkpoint-update{index:03d}"
                        write(SAFE/f"interruption-{recipe_id}.attempt{attempt:02d}.json",{"recipe_id":recipe_id,"attempt":attempt,"verified_resume_path":str(checkpoint),"completed_update":index,"exposure":trainer.committed_exposure,"signals":stop_requested,"disposition":"FAITHFUL_RESUME_REQUIRED"})
                        raise SystemExit(130)
                    prior_evaluation = list(SAFE.glob(f"evaluation-{recipe_id}-update{index:03d}.attempt*.json"))
                    if index in evaluations and (fresh_endpoint or not prior_evaluation):
                        point=evaluations[index]
                        label=f"update{index:03d}"
                        evaluation_timing(trainer,panel,out,label)
                        metrics=summarize_evaluation(out/f"evaluation-{label}.jsonl",panel,point["nominal"],point,recipe_id)
                        metrics["training"] = None if index == 0 else summary
                        write(out/f"evaluation-{label}-metrics.json",metrics)
                        write(SAFE/f"evaluation-{recipe_id}-{label}.attempt{attempt:02d}.json",metrics)
                        print(json.dumps({"recipe_id":recipe_id,"evaluation":point,"natural_wer":metrics["natural"]["wer"],"completed_repair":metrics["natural"]["completed_repair"],"generated_conformance":metrics["generated"]["whole_case_conformance"]}),flush=True)
                    if index==config["actual_stop_endpoint"]["update"]:
                        break
                    item=updates[index]
                    begin=time.perf_counter()
                    queue=trainer.queue if trainer.queue else exact_queue(rows,ledger,item,reader)
                    if trainer.queue and [p["presentation_id"] for p in queue] != [p["presentation_id"] for p in frozen_queue(rows,ledger,item)]:
                        raise ValueError("resumed pending queue differs from frozen ledger")
                    component_losses = None
                    monitor_start = time.perf_counter()
                    if arm == "C101" and index+1 in evaluations:
                        from src.models.paired_training_v3 import pack, queue_denominators
                        denominators = queue_denominators(queue)["C"]
                        component_totals = {key:0. for key in denominators}
                        for offset in range(0,len(queue),trainer.microbatch_size):
                            packed,_ = pack([p["row"] for p in queue[offset:offset+trainer.microbatch_size]],arm)
                            for example in packed:
                                measured = trainer.model.component_sums(**example,dtype=mx.bfloat16)
                                mx.eval(measured)
                                for key in component_totals:
                                    component_totals[key] += float(measured[key])
                        component_losses = {key:component_totals[key]/count if count else None for key,count in denominators.items()}
                    monitor_seconds = time.perf_counter()-monitor_start if component_losses is not None else 0.
                    train_begin = time.perf_counter()
                    if trainer.queue:
                        while trainer.completed_microbatches < len(trainer.partition):
                            trainer.microstep()
                        result=trainer.finish()
                    else:
                        result=trainer.update(queue,reader.state())
                    result["native_update_wall_seconds"] = time.perf_counter()-train_begin
                    result["component_monitor_seconds"] = monitor_seconds
                    result["component_losses"] = {"target_EOS":result["loss"]} if arm == "B100" else component_losses
                    result["component_measurement"] = "pre-update monitoring forward on the same whole queue; no gradients or state updates" if component_losses is not None else "native training total only"
                    if result["committed_canonical_exposure"] != item["end_exposure"] or result["update"] != index+1:
                        raise ValueError("executed common endpoint differs from frozen ledger")
                    result["update_wall_seconds"]=time.perf_counter()-begin
                    result["phase"]=reader.phase
                    result["MLX_peak_bytes"]=mx.get_peak_memory()
                    result["process_peak_rss_bytes"]=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                    stream.write(json.dumps(result,sort_keys=True,allow_nan=False)+"\n")
                    stream.flush()
                    summary={k:v for k,v in result.items() if k not in ("actual_consumption","presentation_ids")}
                    fresh_endpoint = True
                    if result["update"]%10==0:
                        print(json.dumps({"recipe_id":recipe_id,"attempt":attempt,**summary}),flush=True)
            receipt={"recipe_id":recipe_id,"attempt":attempt,"status":"COMPLETED","source_commit":preflight["head"],"campaign_sha256":sha(FREEZE),"initial_parameter_sha256":initial_hash,"endpoint":config["actual_stop_endpoint"],"final_parameter_sha256":endpoints[-1]["parameter_sha256"],"final_checkpoint_complete_sha256":endpoints[-1]["checkpoint_complete_sha256"],"checkpoints":endpoints,"updates_sha256":sha(out/"updates.jsonl"),"private_output_directory":str(out),"attempt_wall_seconds":time.perf_counter()-start,"recipe_wall_seconds":time.time()-started,"numerical_replays":numerical_failures,"last_system_snapshot":system_snapshot(),"disposition":"PRESCRIBED_10M_RECIPE_COMPLETE"}
            write(out/"recipe-complete.json",receipt)
            write(SAFE/f"recipe-{recipe_id}.attempt{attempt:02d}.json",receipt)
            print(json.dumps({k:v for k,v in receipt.items() if k not in ("checkpoints","last_system_snapshot")}),flush=True)
            return
        except Exception as error:
            failure={"recipe_id":recipe_id,"attempt":attempt,"type":type(error).__name__,"message":str(error),"completed_update":trainer.optimizer.step,"committed_exposure":trainer.committed_exposure,"pending_charge":trainer.pending_charge,"completed_microbatches":trainer.completed_microbatches,"last_verified_checkpoint":None if latest is None else str(latest),"wall_seconds":time.perf_counter()-start,"disposition":"NUMERICAL_FAILURE" if isinstance(error,FloatingPointError) else "PROBE_CAMPAIGN_REPAIR_REQUIRED"}
            np.savez(out/"failed-state-arrays.npz",**{k:np.asarray(v) for k,v in trainer.arrays().items()})
            failure["failed_arrays_sha256"] = sha(out/"failed-state-arrays.npz")
            raw_state = {"queue":[{k:v for k,v in p.items() if k != "row"} for p in trainer.queue],
                "partition":trainer.partition,"denominators":trainer.denominators,"loss":trainer.loss,
                "reader_state":reader.state(),"clock":trainer.clock,"optimizer_step":trainer.optimizer.step,
                "optimizer_policy":trainer.optimizer.policy(),"runtime_identities":identities,
                "actual_consumption":trainer.consumption,"python_rng":random.getstate(),
                "numpy_rng":[np.random.get_state()[0],np.random.get_state()[1].tolist(),*np.random.get_state()[2:]],
                "failed_arrays_sha256":failure["failed_arrays_sha256"]}
            (out/"failed-state-metadata.json").write_text(json.dumps(raw_state,sort_keys=True,allow_nan=True)+"\n")
            failure["failed_metadata_sha256"] = sha(out/"failed-state-metadata.json")
            write(out/"failure.json",failure)
            write(SAFE/f"failure-{recipe_id}.attempt{attempt:02d}.json",failure)
            if not isinstance(error,FloatingPointError):
                raise
            numerical_failures += 1
            if numerical_failures==2:
                write(SAFE/f"recipe-{recipe_id}.attempt{attempt:02d}.json",{**failure,"status":"FAILED","initial_parameter_sha256":initial_hash,"campaign_sha256":sha(FREEZE)})
                return
            del trainer
            gc.collect()
            mx.clear_cache()


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("mode",choices=("freeze","run"))
    parser.add_argument("--recipe")
    parser.add_argument("--resume",help="Verified checkpoint of this same partial recipe; never starts another slot")
    args=parser.parse_args()
    if args.mode=="freeze":
        freeze()
    elif args.recipe:
        run(args.recipe,args.resume)
    else:
        parser.error("run requires one registered --recipe")
