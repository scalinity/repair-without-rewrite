"""Exactly 100 native G2 runner updates; future ten-pass recipe stays unstarted."""
import argparse
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import resource
import subprocess
import time

from src.data.g2_artifacts import ArtifactRoot, atomic_artifact, offline_model_environment, read_complete, sha256
from src.data.g2_byt5 import accounting_plan, training_batches, validate_pairs
from src.scoring.triple import serialize


def write(path, value):
    Path(path).write_text(json.dumps(value, sort_keys=True, allow_nan=False)+"\n")


def run(binding, attempt):
    root=ArtifactRoot(binding);before=root.preflight();started=time.perf_counter();offline_model_environment()
    if attempt<1:raise ValueError("positive ByT5 qualification attempt required")
    receipt=Path(f"experiments/manifests/generation_2/byt5-qualification.attempt{attempt:02d}.json")
    if receipt.exists():raise FileExistsError(receipt)
    freeze_path=Path("experiments/manifests/generation_2/corpus-freeze.attempt01.json")
    freeze=json.loads(freeze_path.read_text())
    if freeze["status"]!="PASS_COMPLETE_G2_CORPUS_PANEL_GEOMETRY_FREEZE" or not freeze["development_support"]["pass"]:
        raise ValueError("complete source/support qualification required")
    independent=json.loads(Path("experiments/manifests/generation_2/independent-corpus.attempt01.json").read_text())
    if independent["status"]!="PASS_INDEPENDENT_G2_CORPUS_GEOMETRY" or independent["freeze_sha256"]!=sha256(freeze_path):
        raise ValueError("independent complete corpus/accounting qualification required before model work")
    path=root.path("asr-hypotheses-v1/construction.attempt01");read_complete(path)
    training=[row for row in (json.loads(line) for line in (path/"pairs.jsonl").open()) if row["role"]=="train"]
    validate_pairs(training);plan=accounting_plan(training)
    panel_path=root.path(freeze["panel_relative"]);read_complete(panel_path)
    panel=json.loads((panel_path/"panel.json").read_text())
    weights=Path("exports/byt5-68377bdc18a2ffec8a0533fef03b1c513a4dd49d")
    if (sha256(weights/"pytorch_model.bin")!="5c5aaf56299d6f2d4eaadad550a40765198828ead4d74f0a15f91cbe0961931a"
            or sha256(weights/"config.json")!="7845fb21b320f3fa05392ce151143502cf08729c8c89732da3293615885d3e83"):
        raise ValueError("official pinned ByT5 assets changed")
    cfg={"scope":"G2_QUALIFICATION_ONLY_NOT_SCIENTIFIC","updates":100,"scientific_plan":plan,
        "source_capacity":512,"target_capacity":512,"decode_cap":512,"prefix":"","batch_size":4,
        "lr":3e-4,"optimizer":{"beta1":.9,"beta2":.999,"epsilon":1e-8,"weight_decay":.01,"clip":1.},
        "training_wall_cap_seconds":None,"legacy_600_update_900_second_limits":"replaced by approved G2 ten-pass extent; this qualification remains exactly 100 updates"}
    report={"schema":"g2_byt5_qualification_v1","attempt":attempt,"seed":42,"config":cfg,
        "code_commit":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
        "captured_dirty_status":subprocess.check_output(["git","status","--porcelain"],text=True),
        "code_sha256":sha256(__file__),"config_sha256":hashlib.sha256(json.dumps(cfg,sort_keys=True).encode()).hexdigest(),
        "corpus_freeze_sha256":sha256(freeze_path),"pairs_sha256":sha256(path/"pairs.jsonl"),
        "identities":{name:sha256(name) for name in ("src/data/g2_byt5.py",
            "src/data/g2_artifacts.py","src/data/comparator_interfaces.py",
            "src/inference/byt5_probe.py","src/scoring/records.py",
            "src/scoring/text.py","src/scoring/triple.py")},
        "panel_sha256":sha256(panel_path/"panel.json"),
        "official_weight_sha256":sha256(weights/"pytorch_model.bin"),
        "official_config_sha256":sha256(weights/"config.json"),
        "runtime":{name:importlib.metadata.version(name) for name in ("torch","transformers","numpy")},
        "before":before,"status":"RUNNING","scientific_recipes_started":0,
        "discard_as_scientific_initializer":True,"output_relative":f"byt5-v1/qualification.attempt{attempt:02d}",
        "resume_policy":"retain every attempt; no automatic neural retry; future recipe starts from official pinned weights"}
    try:
        with atomic_artifact(root,report["output_relative"]) as out:
            write(out/"start.json",report)
            import torch
            from transformers import T5ForConditionalGeneration
            from src.inference.byt5_probe import native_batch,decode_ids
            from src.scoring.records import Output,prepare_source,score_output
            from src.data.comparator_interfaces import byt5_ids
            torch.manual_seed(42);torch.set_num_threads(2)
            if not torch.backends.mps.is_available():raise RuntimeError("required native MPS device unavailable")
            model=T5ForConditionalGeneration.from_pretrained(str(weights),local_files_only=True,weights_only=True,
                trust_remote_code=False,attn_implementation="eager",torch_dtype=torch.float32).to("mps")
            if sum(value.numel() for value in model.parameters())!=299637760:raise ValueError("fixed ByT5 parameter count changed")
            optimizer=torch.optim.AdamW(model.parameters(),lr=3e-4,betas=(.9,.999),eps=1e-8,weight_decay=.01)
            torch.mps.synchronize();report["startup_seconds"]=time.perf_counter()-started
            def checkpoint(label):
                tick=time.perf_counter()
                relative=f"byt5-v1/qualification.attempt{attempt:02d}.{label}"
                with atomic_artifact(root,relative) as saved:
                    torch.save({"schema":"g2_byt5_qualification_checkpoint_v1","model":model.state_dict(),
                        "optimizer":optimizer.state_dict(),"torch_cpu_rng":torch.get_rng_state(),
                        "mps_rng":torch.mps.get_rng_state(),"completed_updates":0 if label=="initial" else 100,
                        "config":cfg,"corpus_freeze_sha256":report["corpus_freeze_sha256"]},saved/"state.pt")
                    loaded=torch.load(saved/"state.pt",map_location="cpu",weights_only=True)
                    if (not torch.equal(torch.get_rng_state(),loaded["torch_cpu_rng"])
                            or not torch.equal(torch.mps.get_rng_state(),loaded["mps_rng"])):
                        raise ValueError("ByT5 checkpoint exact RNG readback mismatch")
                    for key,value in model.state_dict().items():
                        if not torch.equal(value.detach().cpu(),loaded["model"][key]):raise ValueError("ByT5 checkpoint exact model readback mismatch")
                    for index,state in optimizer.state_dict()["state"].items():
                        for key,value in state.items():
                            other=loaded["optimizer"]["state"][index][key]
                            if torch.is_tensor(value):
                                if not torch.equal(value.detach().cpu(),other):raise ValueError("ByT5 optimizer readback mismatch")
                            elif value!=other:raise ValueError("ByT5 optimizer scalar readback mismatch")
                return {"seconds":time.perf_counter()-tick,"relative":relative,
                    "arrays_sha256":sha256(root.path(relative)/"state.pt")}
            def evaluate(label):
                tick=time.perf_counter();decode_total=score_total=0.;counts={};model.eval()
                with (out/f"evaluation-{label}.jsonl").open("x") as stream:
                    for index,row in enumerate(panel):
                        root.preflight();begin=time.perf_counter();answer=None
                        try:
                            byt5_ids(row["source"],qualified_capacity=512)
                            byt5_ids(row["target"],qualified_capacity=512)
                        except ValueError:
                            decoded={"status":"invalid_utf8","text":None,"reason":"retained_evaluation_capacity_overflow"}
                        else:
                            batch,_=native_batch([{**row,"reference":row["target"]}],cfg,"mps")
                            with torch.inference_mode():
                                answer=model.generate(input_ids=batch["input_ids"],attention_mask=batch["attention_mask"],
                                    do_sample=False,num_beams=1,max_new_tokens=512,use_cache=True,
                                    eos_token_id=1,pad_token_id=0,decoder_start_token_id=0)[0].tolist()
                            torch.mps.synchronize();decoded=decode_ids(answer)
                        decode_seconds=time.perf_counter()-begin;decode_total+=decode_seconds;begin=time.perf_counter()
                        prepared=prepare_source(row["target"],row["source"])
                        scored=score_output(prepared,Output(decoded["text"],decoded["status"]))
                        score_seconds=time.perf_counter()-begin;score_total+=score_seconds
                        record={"id":row["id"],"population":row["population"],"status":decoded["status"],
                            "decoded":decoded,"generated_ids":answer,"score":scored,"decode_seconds":decode_seconds,"scorer_seconds":score_seconds}
                        stream.write(serialize(record)+"\n");counts[decoded["status"]]=counts.get(decoded["status"],0)+1
                        if (index+1)%100==0:print(json.dumps({"phase":"byt5-evaluation","label":label,"cases":index+1}),flush=True)
                return {"cases":len(panel),"decode_seconds":decode_total,"scorer_seconds":score_total,
                    "complete_panel_wall_seconds":time.perf_counter()-tick,"status_counts":counts,
                    "records_sha256":sha256(out/f"evaluation-{label}.jsonl")}
            report["initial_checkpoint"]=checkpoint("initial")
            report["initial_evaluation"]=evaluate("initial")
            batches=training_batches(training);steps=[];training_tick=time.perf_counter()
            for step in range(1,101):
                root.preflight();selected=next(batches);tick=time.perf_counter();model.train()
                batch,count=native_batch([{**item["row"],"reference":item["row"]["target"]} for item in selected],cfg,"mps")
                optimizer.zero_grad(set_to_none=True);prediction=model(**batch,use_cache=False);loss=prediction.loss
                loss.backward();norm=float(torch.nn.utils.clip_grad_norm_(model.parameters(),1.));value=float(loss.detach())
                if not math.isfinite(value) or not math.isfinite(norm):raise FloatingPointError("nonfinite ByT5 qualification update")
                optimizer.step();torch.mps.synchronize()
                if any(not bool(torch.isfinite(value).all()) for value in model.parameters()):raise FloatingPointError("nonfinite ByT5 parameters")
                record={"update":step,"lr":3e-4,"loss":value,"gradient_norm":norm,"wall_seconds":time.perf_counter()-tick,
                    "presentations":[{k:item[k] for k in ("presentation","pass_index","pass_offset")} for item in selected],
                    "ids":[item["row"]["id"] for item in selected],"native_targets":count,
                    "native_source":int(batch["attention_mask"].sum()),"mps_allocated_bytes":torch.mps.current_allocated_memory(),
                    "mps_driver_bytes":torch.mps.driver_allocated_memory()}
                steps.append(record)
                with (out/"steps.jsonl").open("a") as stream:stream.write(json.dumps(record,sort_keys=True)+"\n")
                print(json.dumps({"phase":"byt5-update","update":step,"wall_seconds":record["wall_seconds"]}),flush=True)
            training_loop_seconds=time.perf_counter()-training_tick
            report["final_checkpoint"]=checkpoint("update100")
            report["final_evaluation"]=evaluate("update100")
            final_batch=list(training_batches(training))[-1]
            # Verify final short-batch tensor/loss geometry without a 101st optimizer update.
            short,count=native_batch([{**item["row"],"reference":item["row"]["target"]} for item in final_batch],cfg,"mps")
            with torch.inference_mode():short_loss=model(**short,use_cache=False).loss
            torch.mps.synchronize()
            if len(final_batch)!=2 or short["input_ids"].shape[0]!=2 or count<=0 or not bool(torch.isfinite(short_loss)):
                raise ValueError("final two-row native batch capacity/loss geometry failed")
            report.update(status="PASS_G2_BYT5_RUNNER_100_UPDATES",updates=100,qualification_presentations=400,
                mean_update_seconds=sum(row["wall_seconds"] for row in steps)/100,
                conservative_update_seconds=max(sum(row["wall_seconds"] for row in steps)/100,
                    sum(row["wall_seconds"] for row in steps[-25:])/25,training_loop_seconds/100),
                training_loop_seconds=training_loop_seconds,
                final_short_batch={"rows":2,"native_targets":count,"forward_only_loss":float(short_loss)},
                optimizer_state_dtypes=sorted({str(value.dtype) for state in optimizer.state.values() for value in state.values() if torch.is_tensor(value)}),
                peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            write(out/"summary.json",report)
        report["after"]=root.preflight()
    except BaseException as error:
        report.update(status="FAILED_QUALIFICATION_REPAIR_REQUIRED",error_type=type(error).__name__)
        raise
    finally:
        report["elapsed_seconds"]=time.perf_counter()-started;write(receipt,report)
    return report


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--artifact-binding",required=True)
    parser.add_argument("--attempt",type=int,required=True);args=parser.parse_args()
    result=run(args.artifact_binding,args.attempt);print(json.dumps({"status":result["status"],"elapsed_seconds":result["elapsed_seconds"]}),flush=True)
