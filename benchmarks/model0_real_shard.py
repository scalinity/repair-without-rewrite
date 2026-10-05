"""Exact MODEL-0, >=10M admitted real clean-target tokens, source-disjoint eval."""
import argparse
from dataclasses import asdict
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import resource
import subprocess
import time

import mlx.core as mx
import numpy as np

from src.data.development_reader import load_targets
from src.models.core import DecoderLM, causal_loss
from src.models.tokenizer import ByteBPE, BOS, EOS
from src.models.training import Trainer, TokenSchedule, save_checkpoint, load_checkpoint
from benchmarks.model0_correctness import parameter_hash

ROLES="experiments/manifests/public_lspc_training_roles.development.jsonl"
SUPPLY="experiments/manifests/public_lspc_training_supply_qualification.json"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pack(rows, tokenizer):
    ids=[]
    for row in rows:
        ids.extend([BOS,*tokenizer.encode(row["target"]),EOS])
    count=len(ids)//257
    return np.array(ids[:count*257],dtype=np.int32).reshape(count,257)


def evaluate(model, batches):
    total=count=0
    for batch in batches:
        ids=mx.array(batch)
        total+=float(causal_loss(model,ids,dtype=mx.bfloat16,backend="native"))
        count+=ids.shape[0]*(ids.shape[1]-1)
    return {"ce":total/count,"valid_labels":count}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",required=True)
    parser.add_argument("--resume")
    parser.add_argument("--stop-tokens",type=int,default=10000000)
    args=parser.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    rows=load_targets(ROLES,SUPPLY,allowed_roles={"train","hpo_development"})
    train=[r for r in rows if r["role"]=="train"]
    dev=[r for r in rows if r["role"]=="hpo_development"]
    assert not {r["source_group_id"] for r in train}&{r["source_group_id"] for r in dev}
    tokenizer=ByteBPE.load("configs/tokenizer_development")
    assert tokenizer.vocab_size==16384
    train_ids=pack(train,tokenizer);dev_ids=pack(dev,tokenizer)
    rng=np.random.default_rng(42)
    order=rng.permutation(len(train_ids)).tolist()
    dev_batches=[dev_ids[i:i+16] for i in range(0,len(dev_ids),16)]
    identity={"model":"MODEL-0-real-shard-development-v1","tokenizer":sha("configs/tokenizer_development/tokenizer.json"),
              "roles":sha(ROLES),"supply":sha(SUPPLY),"train_tokens":hashlib.sha256(train_ids.tobytes()).hexdigest(),
              "dev_tokens":hashlib.sha256(dev_ids.tobytes()).hexdigest()}
    cfg={"seed":42,"batch":16,"sequence_input":256,"planned_tokens":10000000,"peak_lr":.0003,
         "packing":"BOS/raw_target/EOS; stable-ID order then seed42 block permutation; no padded labels",
         "count":"256 native input positions per block; 256 valid shifted labels; BOS/EOS included explicitly",
         "task":"clean real-shard causal language modeling; not B/C restoration recipe"}
    provenance={"head":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
        "dirty_status":subprocess.check_output(["git","status","--porcelain"],text=True),
        "dirty_diff":subprocess.check_output(["git","diff","--binary"],text=True),"config":cfg,"identities":identity,
        "code_hashes":{p:sha(p) for p in (__file__,"src/models/core.py","src/models/training.py","src/data/development_reader.py",
            "src/models/tokenizer.py","benchmarks/model0_correctness.py")},
        "runtime":{"versions":{p:importlib.metadata.version(p) for p in ("mlx","numpy")},
                   "MLX_ENABLE_TF32":os.environ.get("MLX_ENABLE_TF32"),"device":str(mx.default_device()),
                   "metal":mx.metal.device_info()},
        "source_groups":{"train":len({r["source_group_id"] for r in train}),"dev":len({r["source_group_id"] for r in dev})},
        "documents":{"train":len(train),"dev":len(dev)},"unique_packed_tokens":{"train":int(train_ids.size),"dev":int(dev_ids.size)},
        "initial_thermal":subprocess.check_output(["pmset","-g","therm"],text=True)}
    (out/"provenance.json").write_text(json.dumps(provenance,indent=2)+"\n")
    trainer=Trainer(DecoderLM(seed=42),TokenSchedule(10000000,peak_lr=.0003),dtype=mx.bfloat16,backend="native",seed=42,identities=identity)
    trainer.phase="development_real_shard"
    trainer.data_order=order
    initial_hash=parameter_hash(trainer.model)
    initial=evaluate(trainer.model,dev_batches)
    # Save before the first update, including independently checkable initial
    # weights and complete precision/optimizer/scheduler/model identities.
    (out/"initial_identity.json").write_text(json.dumps({"weights_sha256":initial_hash,
        "model_config":asdict(trainer.model.config),"dtype_inventory":trainer.dtype_inventory(),
        "optimizer":trainer.optimizer.policy(),"schedule":asdict(trainer.schedule),
        "initial_heldout":initial,"source_identities":identity},indent=2)+"\n")
    resume_record=None
    if args.resume:
        load_checkpoint(trainer,args.resume)
        if trainer.data_order!=order:
            raise ValueError("changed reader order")
        resume_record={"checkpoint":args.resume,"restored_tokens":trainer.processed_tokens,"restored_step":trainer.optimizer.step,
                       "restored_weights":parameter_hash(trainer.model),"heldout":evaluate(trainer.model,dev_batches)}
    evaluations=[{"processed_tokens":trainer.processed_tokens,"metric":resume_record["heldout"] if resume_record else initial}]
    begin=time.perf_counter()
    with (out/"steps.jsonl").open("w",buffering=1) as f:
        while trainer.processed_tokens<args.stop_tokens:
            start=time.perf_counter()
            indices=[order[(trainer.data_cursor+i)%len(order)] for i in range(16)]
            trainer.accumulate(mx.array(train_ids[indices]), processed_tokens=16*256)
            update=trainer.update()
            update["seconds"]=time.perf_counter()-start
            update["peak_mlx_bytes"]=mx.get_peak_memory()
            f.write(json.dumps(update)+"\n")
            if trainer.optimizer.step%250==0 or trainer.processed_tokens>=args.stop_tokens:
                metric=evaluate(trainer.model,dev_batches)
                evaluations.append({"processed_tokens":trainer.processed_tokens,"metric":metric})
                print(json.dumps({"step":trainer.optimizer.step,"tokens":trainer.processed_tokens,"train_loss":update["loss"],"heldout":metric}),flush=True)
                (out/"evaluations.json").write_text(json.dumps(evaluations,indent=2)+"\n")
    checkpoint=out/"checkpoint"
    checkpoint_time=time.perf_counter();save_checkpoint(trainer,checkpoint)
    final=evaluate(trainer.model,dev_batches)
    if not math.isfinite(final["ce"]):
        raise ValueError("nonfinite heldout loss")
    report={"processed_tokens":trainer.processed_tokens,"updates":trainer.optimizer.step,"initial":initial,"final":final,
        "evaluations":evaluations,"initial_weights":initial_hash,"final_weights":parameter_hash(trainer.model),
        "model_config":asdict(trainer.model.config),"dtype_inventory":trainer.dtype_inventory(),"optimizer":trainer.optimizer.policy(),
        "schedule":asdict(trainer.schedule),"resume":resume_record,"checkpoint_seconds":time.perf_counter()-checkpoint_time,
        "training_and_evaluation_wall_seconds":time.perf_counter()-begin,"peak_mlx_bytes":mx.get_peak_memory(),
        "peak_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "final_thermal":subprocess.check_output(["pmset","-g","therm"],text=True),
        "status":"PARTIAL_CONTINUE" if trainer.processed_tokens<10000000 else "PASS" if final["ce"]<initial["ce"] and final["ce"]<evaluations[-2]["metric"]["ce"] else "FAIL"}
    (out/"summary.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:report[k] for k in ("status","processed_tokens","initial","final","training_and_evaluation_wall_seconds")}))


if __name__=="__main__":
    main()
