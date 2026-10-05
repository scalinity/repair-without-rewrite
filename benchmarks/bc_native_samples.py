"""Bounded exact-B/C BF16 complete-update and event-density samples.

This is not BENCH-00's canonical32k/100-update/20-minute campaign calibration.
Run only after the sealed BC gate passes; all source padding masks stay active.
"""
from pathlib import Path
from dataclasses import asdict
from datetime import datetime,timezone
import argparse,hashlib,json,os,subprocess,time,gc
import numpy as np
import mlx.core as mx
import mlx.nn as nn
from mlx.utils import tree_unflatten
from src.models.bc import B100,C101,c_microbatch_loss
from src.models.core import masked_cross_entropy,parameter_inventory
from src.models.edits import Edit,EditProgram,source_identity,render,events,update_denominators
from src.models.training import AdamW,GradientAccumulator,flat_parameters


def digest_file(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def hash_weights(model):
    digest=hashlib.sha256()
    for name,value in sorted(flat_parameters(model).items()):
        digest.update(name.encode());digest.update(np.asarray(value).tobytes())
    return digest.hexdigest()


def data_recipe(model_name,length,k=0,r=0):
    source='a'*(length-2)
    source_ids=mx.array([[308,259,*source.encode(),*([256]*8)]],dtype=mx.int32)
    source_valid=mx.array([[True]*length+[False]*8])
    positions=tuple(range(1,len(source)+2))
    offsets=tuple(range(len(source)+1))
    legal=mx.array([True]*(len(source)+1))
    if model_name=='B100':
        target='b'+'a'*(length-2)
        decoder_ids=mx.array([[257,*target.encode()]],dtype=mx.int32)
        targets=mx.array([[*target.encode(),258]],dtype=mx.int32)
        valid=mx.ones(targets.shape,dtype=mx.bool_)
        def loss(model):
            logits=model(source_ids,decoder_ids,source_valid,dtype=mx.bfloat16)
            return masked_cross_entropy(logits,targets,valid)/targets.size
        labels=None
        counts={'vocabulary':targets.size,'decoder_positions':decoder_ids.size,'actions':0,'pointers':0,'replacement_ordinary':0,'delimiters':0}
    else:
        if k==0 and r!=0 or k and r%k:raise ValueError('integer replacement budget per edit required')
        edits=tuple(Edit(2*i,2*i+1,'b'*(r//k)) for i in range(k)) if k else ()
        program=EditProgram(*source_identity(source),edits)
        target=render(source,program)
        labels=events(program,lambda text:list(text.encode()),{i:i for i in offsets})
        example=dict(source_ids=source_ids,labels=labels,encoder_positions=positions,legal=legal,source_valid=source_valid)
        denominators=update_denominators([[labels]])
        def loss(model):return c_microbatch_loss(model,[example],denominators,dtype=mx.bfloat16)
        counts={'component_denominators':denominators,'decoder_positions':len(labels.inputs),'actions':k+1,
                'pointers':2*k,'replacement_ordinary':r,'delimiters':k,'vocabulary':r+k}
    # Development-only base-byte anchor. Full reference serves both the clean
    # spoken accounting anchor and full-target text; it is never encoder input.
    canonical_anchors=2+2*len(target.encode())+1
    metadata={'model':model_name,'source_nonpadding_positions':length,'source_padding_positions':8,
              'source_padded_positions':length+8,'source_bytes':len(source),'target_bytes':len(target),
              'synthetic_byte_canonical_anchors':canonical_anchors,
              'canonical_anchor_definition':'2 trusted source controls + clean reference bytes + full target bytes + EOS',
              'tokenizer_status':'base-byte DEVELOPMENT accounting; 16k trained BPE not frozen',
              'source':source,'target':target,'K':k,'R':r,**counts}
    return source_ids,source_valid,positions,offsets,legal,loss,metadata


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    parser.add_argument('--gate',default='docs/reports/raw/bc_final_gate.json')
    args=parser.parse_args()
    if os.environ.get('MLX_ENABLE_TF32')!='0':raise ValueError('launch with MLX_ENABLE_TF32=0')
    gate=json.loads(Path(args.gate).read_text())
    if not gate.get('mechanical_pass') or not gate.get('same_pair_exact_overfit_pass'):
        raise ValueError('BC correctness gate is not passed')
    for name,expected in gate['code_hashes'].items():
        if digest_file(name)!=expected:raise ValueError(f'BC gate code changed: {name}')
    out=Path(args.output);out.mkdir(parents=True,exist_ok=False)
    recipe_configs=[('B100',64,0,0),('B100',256,0,0),('C101',256,0,0),('C101',256,1,1),('C101',256,8,8),('C101',256,8,64)]
    identity={'started_utc':datetime.now(timezone.utc).isoformat(),'classification':'BOUNDED_RANDOM_WEIGHT_COMPLETE_UPDATE_SAMPLES',
              'code_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
              'dirty_state':subprocess.check_output(['git','status','--porcelain'],text=True).splitlines(),
              'seed':42,'dtype':'bfloat16 working; float32 master/moments/accumulator','backend':'transparent reference with FP32 score/softmax',
              'warmups':5,'timed_updates':20,'microbatches_per_update':1,'LR':3e-4,
              'source_padding_positions':8,'source_masks':'real bool key masks retained','gate_sha256':digest_file(args.gate),
              'code_hashes':{p:digest_file(p) for p in ['benchmarks/bc_native_samples.py','src/models/bc.py','src/models/edits.py','src/models/core.py','src/models/training.py']},
              'TF32':os.environ['MLX_ENABLE_TF32'],'final_10M_or_campaign_projection':False,'concurrent_accelerator_work_allowed':False}
    (out/'identity.json').write_text(json.dumps(identity,indent=2)+'\n')
    summaries=[];decoded_lengths=set()
    with (out/'steps.jsonl').open('x') as step_log,(out/'decode_calls.jsonl').open('x') as decode_log:
        for ordinal,(name,length,k,r) in enumerate(recipe_configs):
            mx.reset_peak_memory()
            data=data_recipe(name,length,k,r)
            source_ids,source_valid,positions,offsets,legal,loss_fn,metadata=data
            cls=B100 if name=='B100' else C101
            model=cls(seed=42);inventory=parameter_inventory(model)
            expected=100686336 if name=='B100' else 101081859
            if sum(x['count'] for x in inventory)!=expected:raise ValueError('exact parameter mismatch')
            mx.eval(model.parameters(),source_ids,source_valid,legal)
            recipe_id=f'{ordinal:02d}_{name}_s{length}_K{k}_R{r}'
            optimizer=AdamW(flat_parameters(model));accumulator=GradientAccumulator(flat_parameters(model))
            metadata.update({'recipe_id':recipe_id,'model_config':asdict(model.config),'exact_parameter_count':expected,
                             'initial_weight_sha256':hash_weights(model),'optimizer_policy':optimizer.policy(),
                             'actual_dtype_inventory':{'master':sorted({str(v.dtype) for v in flat_parameters(model).values()}),
                                'moment_m':sorted({str(v.dtype) for v in optimizer.m.values()}),
                                'moment_v':sorted({str(v.dtype) for v in optimizer.v.values()}),
                                'accumulator':sorted({str(v.dtype) for v in accumulator.values.values()}),
                                'working':'mlx.core.bfloat16','loss_and_sensitive_reductions':'mlx.core.float32'}})
            (out/f'{recipe_id}_data.json').write_text(json.dumps(metadata,indent=2)+'\n')
            (out/f'{recipe_id}_input_identity.json').write_text(json.dumps({'data_sha256':digest_file(out/f'{recipe_id}_data.json'),
                'identity_sha256':digest_file(out/'identity.json'),'captured_before_updates':True},indent=2)+'\n')
            value_grad=nn.value_and_grad(model,loss_fn);times=[]
            for step in range(25):
                begin=time.perf_counter()
                value,gradient=value_grad(model);mx.eval(value,gradient)
                accumulator.add(gradient)
                del gradient
                weights,norm=optimizer.apply(flat_parameters(model),accumulator.gradients(already_normalized=True),3e-4)
                model.update(tree_unflatten(list(weights.items())));accumulator.clear()
                mx.eval(model.parameters(),optimizer.m,optimizer.v,accumulator.values,value)
                mx.synchronize()
                elapsed=time.perf_counter()-begin
                if step>=5:times.append(elapsed)
                entry={'recipe_id':recipe_id,'step':step+1,'timed':step>=5,'seconds':elapsed,
                       'loss':float(value.item()),'gradient_norm':norm,'MLX_active_bytes':mx.get_active_memory(),
                       'MLX_cache_bytes':mx.get_cache_memory(),'MLX_peak_bytes':mx.get_peak_memory(),
                       'synthetic_byte_canonical_anchors':metadata['synthetic_byte_canonical_anchors']}
                step_log.write(json.dumps(entry)+'\n');step_log.flush()
            # Fresh random weights for bounded decode; never report these as a
            # trained-quality/inference-rate frontier or completed campaign.
            del model,optimizer,accumulator,value_grad,weights;gc.collect();mx.clear_cache()
            model=cls(seed=42);mx.eval(model.parameters())
            call_count=0 if (name,length) in decoded_lengths else 2
            decoded_lengths.add((name,length))
            for call in range(call_count):
                begin=time.perf_counter()
                if name=='B100':
                    answer=model.greedy_text(source_ids,source_valid=source_valid,max_tokens=32,dtype=mx.bfloat16)
                    output_positions=len(answer['token_ids'])+(answer['status']=='completed')
                    record={'status':answer['status'],'generated_token_ids':answer['token_ids'],'decoder_positions':output_positions}
                else:
                    answer=model.greedy_edits(metadata['source'],source_ids,positions,offsets,legal,lambda token:bytes([token]),
                        source_valid=source_valid,max_edits=8,max_decoder_positions=32,dtype=mx.bfloat16)
                    record={'status':answer['status'],'decoder_positions':answer['decoder_positions'],'output':answer['output'],'reason':answer.get('reason')}
                mx.synchronize();record.update({'recipe_id':recipe_id,'call':call+1,'seconds':time.perf_counter()-begin,
                                                'random_weights':True,'complete_boundary_includes_encoder_and_greedy_and_C_renderer':True})
                decode_log.write(json.dumps(record)+'\n');decode_log.flush()
            summary={'recipe_id':recipe_id,'mean_update_seconds':sum(times)/len(times),'p50_update_seconds':float(np.median(times)),
                     'p95_update_seconds':float(np.quantile(times,.95)),'timed_updates':len(times),'timed_seconds':sum(times),
                     'synthetic_byte_canonical_anchors_per_second':20*metadata['synthetic_byte_canonical_anchors']/sum(times),
                     'peak_allocation_bytes':mx.get_peak_memory(),'classification':'SHORT_SYNTHETIC_SAMPLE_NOT_CAMPAIGN_RATE'}
            summaries.append(summary);print(json.dumps(summary),flush=True)
            del model;gc.collect();mx.clear_cache()
    (out/'summary.json').write_text(json.dumps({'identity':identity,'recipes':summaries,'finished_utc':datetime.now(timezone.utc).isoformat()},indent=2)+'\n')
    (out/'SHA256SUMS.json').write_text(json.dumps({p.name:digest_file(p) for p in out.iterdir() if p.is_file()},indent=2)+'\n')


if __name__=='__main__':main()
