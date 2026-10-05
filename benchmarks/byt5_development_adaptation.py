"""Finite native recipe screen on admitted natural pairs, never sealed data."""
import argparse
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import random
import resource
import subprocess
import time

from src.data.comparator_interfaces import byt5_ids
from src.data.development_reader import load_targets
from src.inference.byt5_probe import decode_ids, native_batch
from src.models.tokenizer import ByteBPE
from src.scoring.text import lexical


def sha(p):
    return hashlib.file_digest(Path(p).open("rb"),"sha256").hexdigest()


def distance(reference,output):
    a,b=lexical(reference),lexical(output)
    prior=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        current=[i]
        for j,y in enumerate(b,1):
            current.append(min(current[-1]+1,prior[j]+1,prior[j-1]+(x!=y)))
        prior=current
    return prior[-1]


def validate_recipe(lr,prefix,updates):
    if not 1<=updates<=600 or (lr,prefix) not in ((.0003,""),(.0001,"Restore transcript: ")):
        raise ValueError("outside predeclared two-recipe bounded screen")


def admit(row):
    byt5_ids(row["source"],qualified_capacity=512)
    byt5_ids(row["reference"],qualified_capacity=512)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",required=True)
    parser.add_argument("--lr",type=float,default=.0003)
    parser.add_argument("--updates",type=int,default=600)
    parser.add_argument("--prefix",default="")
    args=parser.parse_args()
    validate_recipe(args.lr,args.prefix,args.updates)
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    pairpath=Path("exports/foundation-repair/development-asr-pairs-attempt01/pairs.jsonl")
    pairs=[json.loads(s) for s in pairpath.read_text().splitlines()]
    roles="experiments/manifests/public_lspc_training_roles.development.jsonl"
    supply="experiments/manifests/public_lspc_training_supply_qualification.json"
    admitted={r["id"]:r for r in load_targets(roles,supply,allowed_roles={"train","calibration","hpo_development"})}
    training=[];calibration=[];failures=[]
    for p in pairs:
        role=admitted[p["id"]]
        if p["role"]!=role["role"] or p["source_group_id"]!=role["source_group_id"] or p["target"]!=role["target"]:
            raise ValueError("pair source-role-target binding mismatch")
        if p["status"]!="COMPLETED":
            failures.append({"id":p["id"],"reason":"source_failure"});continue
        if hashlib.sha256(p["source"].encode()).hexdigest()!=p["source_sha256"]:
            raise ValueError("source hypothesis checksum mismatch")
        row={**p,"reference":p["target"],"source":args.prefix+p["source"],"raw_source":p["source"]}
        try:
            admit(row)
        except ValueError:
            failures.append({"id":p["id"],"reason":"capacity_overflow"});continue
        (training if p["role"]=="train" else calibration).append(row)
    # Original twelve HPO source hypotheses: exact repaired pass, no redraw.
    devpath=Path("exports/foundation-repair/parakeet-frame-repair-attempt01/records.jsonl")
    audio=json.loads(Path("experiments/manifests/public_audio_development/manifest.book_closed.attempt03.json").read_text())["cases"]
    dev=[]
    for s in devpath.read_text().splitlines()[:12]:
        p=json.loads(s);role=admitted[p["id"]]
        if role["role"]!="hpo_development" or audio[p["case_index"]]["text_raw"]!=role["target"]:
            raise ValueError("original HPO source reference mismatch")
        dev.append({"id":p["id"],"role":"hpo_development","source_group_id":role["source_group_id"],
            "source":args.prefix+p["hypothesis"],"raw_source":p["hypothesis"],"reference":role["target"]})
    dev+=sorted(calibration,key=lambda r:hashlib.sha256(("byt5-screen-120202:"+r["id"]).encode()).hexdigest())[:12]
    for row in dev:admit(row)
    if {r["source_group_id"] for r in training}&{r["source_group_id"] for r in dev}:
        raise ValueError("source group leakage")
    order=list(range(len(training)));random.Random(42).shuffle(order)
    cfg={"seed":42,"lr":args.lr,"updates":args.updates,"batch_size":4,"source_capacity":512,"target_capacity":512,
        "prefix":args.prefix,"decode_cap":512,"training_wall_cap_seconds":900,
        "optimizer":{"name":"AdamW","beta1":.9,"beta2":.999,"epsilon":1e-8,"weight_decay":.01,"clip":1.},
        "screen_panels":[0,200,args.updates],"credible_decision":"completed nonidentity natural restoration; aggregate lexical error improves over RAW, useful corrections and identity control reported; no final recipe selection"}
    weights=Path("exports/byt5-68377bdc18a2ffec8a0533fef03b1c513a4dd49d")
    if sha(weights/"pytorch_model.bin")!="5c5aaf56299d6f2d4eaadad550a40765198828ead4d74f0a15f91cbe0961931a":
        raise ValueError("official pinned ByT5 weight mismatch")
    if sha(weights/"config.json")!="7845fb21b320f3fa05392ce151143502cf08729c8c89732da3293615885d3e83":
        raise ValueError("official pinned ByT5 config mismatch")
    tokenizer=ByteBPE.load("configs/tokenizer_development")
    provenance={"head":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
        "dirty_status":subprocess.check_output(["git","status","--porcelain"],text=True),
        "dirty_diff":subprocess.check_output(["git","diff","--binary"],text=True),"config":cfg,
        "hashes":{p:sha(p) for p in (str(pairpath),str(devpath),roles,supply,__file__,"src/data/comparator_interfaces.py",
            "src/inference/byt5_probe.py","src/models/tokenizer.py","configs/tokenizer_development/tokenizer.json")},
        "weight_sha256":sha(weights/"pytorch_model.bin"),"model_config_sha256":sha(weights/"config.json"),
        "runtime":{p:importlib.metadata.version(p) for p in ("torch","transformers","numpy")},
        "device":"mps FP32 no fallback", "training_ids":[r["id"] for r in training],"dev_ids":[r["id"] for r in dev],"excluded_training":failures}
    provenance["calibration_consumption"]={"ids":[r["id"] for r in dev if r["role"]=="calibration"],
        "new_role":"comparator_development_consumed", "untouched_calibration_remaining":[r["id"] for r in calibration if r["id"] not in {d["id"] for d in dev}]}
    (out/"provenance.json").write_text(json.dumps(provenance,indent=2)+"\n")
    import torch
    from transformers import T5ForConditionalGeneration
    if os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK")!="0":
        raise ValueError("native screen requires explicitly disabled fallback")
    torch.manual_seed(42);torch.set_num_threads(2)
    model=T5ForConditionalGeneration.from_pretrained(str(weights),local_files_only=True,weights_only=True,
        trust_remote_code=False,attn_implementation="eager",torch_dtype=torch.float32).to("mps")
    model.eval();torch.mps.synchronize()
    assert sum(p.numel() for p in model.parameters())==299637760
    (out/"initial_identity.json").write_text(json.dumps({"config":model.config.to_dict(),"parameter_count":299637760,
        "loaded_weight_file_sha256":provenance["weight_sha256"],"parameter_dtypes":sorted({str(p.dtype) for p in model.parameters()}),
        "native_device":str(next(model.parameters()).device)},indent=2)+"\n")
    steps=[];outputs=[];presented_anchor=native_source=native_targets=0
    def panel(step):
        model.eval()
        # Synthetic self-copy controls use HPO source bytes, never gold as input.
        controls=[{**r,"id":r["id"]+":raw-copy-control","reference":r["raw_source"],"identity_control":True} for r in dev[:4]]
        for r in dev+controls:
            batch,_=native_batch([r],cfg,"mps")
            torch.mps.synchronize();tick=time.perf_counter()
            with torch.inference_mode():
                ids=model.generate(input_ids=batch["input_ids"],attention_mask=batch["attention_mask"],
                    do_sample=False,num_beams=1,max_new_tokens=512,use_cache=True,eos_token_id=1,pad_token_id=0,decoder_start_token_id=0)[0].tolist()
            torch.mps.synchronize();decoded=decode_ids(ids)
            observed=decoded["text"] or ""
            item={"step":step,"id":r["id"],"role":r["role"],"source_group_id":r["source_group_id"],
                "raw_source":r["raw_source"],"reference":r["reference"],"ids":ids,"decoded":decoded,
                "seconds":time.perf_counter()-tick,"eS":distance(r["reference"],r["raw_source"]),
                "eO":distance(r["reference"],observed),"reference_words":len(lexical(r["reference"])),
                "identity_control":r.get("identity_control",False),"byte_changed":observed!=r["raw_source"],
                "generated_positions":len(ids)-1,"source_native_tokens":int(batch["attention_mask"].sum())}
            outputs.append(item)
            with (out/"outputs.jsonl").open("a") as f:f.write(json.dumps(item,sort_keys=True)+"\n")
        natural=[r for r in outputs if r["step"]==step and not r["identity_control"]]
        print(json.dumps({"step":step,"valid":sum(r["decoded"]["status"]=="complete" for r in natural),
            "cases":len(natural),"eS":sum(r["eS"] for r in natural),"eO":sum(r["eO"] for r in natural)}),flush=True)
    baseline_start=time.perf_counter();panel(0);baseline_seconds=time.perf_counter()-baseline_start
    optimizer=torch.optim.AdamW(model.parameters(),lr=args.lr,weight_decay=.01)
    start=time.perf_counter()
    for step in range(1,args.updates+1):
        if time.perf_counter()-start>900:
            raise TimeoutError("bounded adaptation window exceeded")
        selected=[training[order[((step-1)*4+j)%len(order)]] for j in range(4)]
        model.train();batch,count=native_batch(selected,cfg,"mps")
        optimizer.zero_grad(set_to_none=True);tick=time.perf_counter()
        prediction=model(**batch,use_cache=False);loss=prediction.loss
        loss.backward();norm=float(torch.nn.utils.clip_grad_norm_(model.parameters(),1.))
        value=float(loss.detach())
        if not math.isfinite(value) or not math.isfinite(norm):raise ValueError("nonfinite adaptation")
        optimizer.step();torch.mps.synchronize()
        anchors=sum(2*len(tokenizer.encode(r["reference"]))+3 for r in selected)
        presented_anchor+=anchors;native_targets+=count;native_source+=int(batch["attention_mask"].sum())
        item={"step":step,"loss":value,"gradient_norm":norm,"seconds":time.perf_counter()-tick,
            "canonical_anchors":anchors,"native_targets":count,"native_source":int(batch["attention_mask"].sum()),
            "mps_allocated_bytes":torch.mps.current_allocated_memory(),"mps_driver_bytes":torch.mps.driver_allocated_memory()}
        steps.append(item)
        with (out/"steps.jsonl").open("a") as f:f.write(json.dumps(item)+"\n")
        if step in (200,args.updates):panel(step)
    torch.save(model.state_dict(),out/"adapted_weights.pt")
    final=[r for r in outputs if r["step"]==args.updates and not r["identity_control"]]
    valid=sum(r["decoded"]["status"]=="complete" for r in final)
    summary={"updates":args.updates,"canonical_anchors":presented_anchor,"native_source_tokens":native_source,
        "native_supervised_tokens":native_targets,"wall_seconds_including_panels":time.perf_counter()-start,
        "training_rows":len(training),"dev_rows":len(dev),"valid_completions":valid,
        "pre_adaptation_panel_seconds":baseline_seconds,
        "source_errors":sum(r["eS"] for r in final),"output_errors":sum(r["eO"] for r in final),
        "useful_cases":sum(r["decoded"]["status"]=="complete" and r["eO"]<r["eS"] for r in final),
        "damaged_cases":sum(r["eO"]>r["eS"] for r in final),"parameter_dtype":"FP32",
        "optimizer_state_dtypes":sorted({str(v.dtype) for s in optimizer.state.values() for v in s.values() if torch.is_tensor(v)}),
        "peak_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,"checkpoint_sha256":sha(out/"adapted_weights.pt")}
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary),flush=True)


if __name__=="__main__":
    try:main()
    except Exception as error:
        import sys
        if "--out" in sys.argv:
            failure=Path(sys.argv[sys.argv.index("--out")+1])/"failure.json"
            if failure.parent.exists():failure.write_text(json.dumps({"type":type(error).__name__,"message":str(error)},indent=2)+"\n")
        raise
