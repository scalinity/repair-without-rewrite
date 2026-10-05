"""Gated BENCH-00 full-update geometry/thermal/resume measurement.

This random-token geometry workload is not a learning experiment or a measured
public-data length distribution. B/C and comparator rates require separate runs.
"""
import argparse
from dataclasses import asdict
import datetime
import hashlib
import json
import os
from pathlib import Path
import statistics
import subprocess
import time

import mlx.core as mx
import numpy as np
from src.models.core import ModelConfig, DecoderLM, parameter_inventory
from src.models.training import Trainer, TokenSchedule, save_checkpoint, load_checkpoint, flat_parameters


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',required=True)
    parser.add_argument('--gate-evidence',required=True)
    parser.add_argument('--length',type=int,default=256)
    parser.add_argument('--accumulation',type=int,default=4)
    parser.add_argument('--thermal-seconds',type=int,default=1200)
    args=parser.parse_args()
    gates=json.loads(Path(args.gate_evidence).read_text())
    if not all(gates.get('gates',{}).get(v)=='PASS' for v in ('V0','V1','V2','V3','V4')):
        raise RuntimeError('MODEL0 V0-V4 evidence prerequisite has not passed')
    for path in ('src/models/core.py','src/models/training.py'):
        if gates.get('code_hashes',{}).get(path)!=sha(path):
            raise RuntimeError('qualified model/training code changed: '+path)
    if os.environ.get('MLX_ENABLE_TF32')!='0':
        raise RuntimeError('FP32 qualification requires MLX_ENABLE_TF32=0')
    if args.length<64 or args.length>1024 or args.accumulation<1 or args.thermal_seconds<1200:
        raise ValueError('benchmark workload cannot weaken declared bounds')
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    config=ModelConfig(width=768,num_layers=14,q_heads=12,kv_heads=4,ffn_width=2048)
    recipe={'geometry':asdict(config),'microbatch':1,'accumulation':args.accumulation,
            'sequence_length':args.length,'valid_targets_per_microbatch':args.length-1,
            'working_dtype':'bfloat16','master_moment_accumulator':'float32',
            'backend':'explicit_reference','tf32':False,'compile':'disabled',
            'seed':42,'weight_decay':.1,'clip_norm':1.,'beta1':.9,'beta2':.95,'epsilon':1e-8,
            'thermal_seconds':args.thermal_seconds,'warmups':5,'timed_updates':100,
            'input_kind':'random-token geometry; not public-data learning',
            'mask':'full causal mask; all targets valid; no padding; no mask removal'}
    (out/'config.json').write_text(json.dumps(recipe,sort_keys=True,indent=2)+'\n')
    rng=np.random.default_rng(42)
    batches=[mx.array(rng.integers(384,16384,size=(1,args.length),dtype=np.int32)) for _ in range(args.accumulation)]
    data=np.stack([np.asarray(v) for v in batches]);np.save(out/'native_token_manifest.npy',data)
    provenance={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
                'dirty':subprocess.check_output(['git','status','--porcelain=v1'],text=True),
                'config_sha256':sha(out/'config.json'),'manifest_sha256':sha(out/'native_token_manifest.npy'),
                'gate_evidence_sha256':sha(args.gate_evidence),'seed':42,
                'initial_thermal':subprocess.check_output(['pmset','-g','therm'],text=True),
                'power':subprocess.check_output(['pmset','-g','batt'],text=True),
                'environment_reference':'docs/reports/ENVIRONMENT_INITIAL.json',
                'runtime_lock_sha256':sha('uv.lock'),'resume_policy':'checkpoint then 20 control/20 restored updates'}
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    then=time.perf_counter()
    model=DecoderLM(config,seed=42);inventory=parameter_inventory(model)
    assert sum(v['count'] for v in inventory)==100685568
    trainer=Trainer(model,TokenSchedule(150000000),dtype=mx.bfloat16,backend='reference',
                    identities={'config':sha(out/'config.json'),'data':sha(out/'native_token_manifest.npy')})
    trainer.phase='BENCH00_GEOMETRY_NOT_FINAL_TRAINING'
    mx.eval(model.parameters(),trainer.optimizer.m,trainer.optimizer.v,trainer.accumulator.values)
    initialization=time.perf_counter()-then
    initial=hashlib.sha256()
    for name,value in sorted(flat_parameters(model).items()):
        initial.update(name.encode());initial.update(np.asarray(value).tobytes())
    (out/'parameter_inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
    provenance['initial_weight_sha256']=initial.hexdigest()
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    def update():
        start=time.perf_counter()
        for ids in batches:
            trainer.accumulate(ids)
        result=trainer.update()
        mx.eval(trainer.model.parameters(),trainer.optimizer.m,trainer.optimizer.v,trainer.accumulator.values)
        mx.synchronize()
        return result|{'elapsed_seconds':time.perf_counter()-start,
                       'peak_memory_bytes':mx.get_peak_memory()}
    all_rows=[]
    with (out/'updates.jsonl').open('w',buffering=1) as log:
        for ordinal in range(5):
            row=update()|{'segment':'warmup','ordinal':ordinal};all_rows.append(row);log.write(json.dumps(row)+'\n')
        for ordinal in range(100):
            row=update()|{'segment':'timed','ordinal':ordinal};all_rows.append(row);log.write(json.dumps(row)+'\n')
            if ordinal%20==19:
                print(json.dumps({'segment':'timed','updates':ordinal+1}),flush=True)
        thermal_start=time.perf_counter();ordinal=0;last_notice=thermal_start
        while time.perf_counter()-thermal_start<args.thermal_seconds:
            row=update()|{'segment':'thermal','ordinal':ordinal};all_rows.append(row);log.write(json.dumps(row)+'\n');ordinal+=1
            if time.perf_counter()-last_notice>=60:
                print(json.dumps({'segment':'thermal','elapsed_seconds':time.perf_counter()-thermal_start,'updates':ordinal}),flush=True)
                last_notice=time.perf_counter()
        thermal_elapsed=time.perf_counter()-thermal_start
    checkpoint=Path('checkpoints')/out.name/'bench-end'
    then=time.perf_counter();checkpoint_hashes=save_checkpoint(trainer,checkpoint);checkpoint_cost=time.perf_counter()-then
    for _ in range(20):update()
    control=trainer
    then=time.perf_counter()
    restored=Trainer(DecoderLM(config,seed=42),TokenSchedule(150000000),dtype=mx.bfloat16,backend='reference',
                     identities=control.identities)
    load_checkpoint(restored,checkpoint);load_cost=time.perf_counter()-then
    trainer=restored
    for _ in range(20):update()
    maximum=max(float(mx.max(mx.abs(flat_parameters(control.model)[k]-v)).item())
                for k,v in flat_parameters(restored.model).items())
    moments=max(float(mx.max(mx.abs(control.optimizer.m[k]-v)).item()) for k,v in restored.optimizer.m.items())
    timed=[r['elapsed_seconds'] for r in all_rows if r['segment']=='timed']
    thermal=[r['elapsed_seconds'] for r in all_rows if r['segment']=='thermal']
    summary={'status':'PASS_GEOMETRY_THERMAL_RESUME' if maximum==0 and moments==0 else 'FAIL_RESUME',
             'initialization_seconds':initialization,'parameter_count':100685568,
             'timed_updates':100,'timed_seconds':sum(timed),'timed_mean_seconds':statistics.mean(timed),
             'timed_median_seconds':statistics.median(timed),'thermal_updates':len(thermal),
             'thermal_wall_seconds':thermal_elapsed,'thermal_update_seconds':sum(thermal),
             'thermal_tokens_per_second':len(thermal)*args.length*args.accumulation/sum(thermal),
             'peak_memory_bytes':mx.get_peak_memory(),'checkpoint_seconds':checkpoint_cost,
             'load_resume_seconds':load_cost,'checkpoint_hashes':checkpoint_hashes,
             'resume_20_updates_max_abs_parameter':maximum,'resume_20_updates_max_abs_moment':moments,
             'final_thermal':subprocess.check_output(['pmset','-g','therm'],text=True),
             'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'limitations':['no representative public-data length distribution','no B/C throughput or event density',
                            'no ByT5/Qwen/ASR/TTS native timing','no campaign calendar projection justified']}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
