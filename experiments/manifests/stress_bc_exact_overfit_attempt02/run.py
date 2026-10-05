"""Bounded SAME-pair exact-geometry B/C correctness rehearsal; not a 10M probe."""
from pathlib import Path
import gc, hashlib, json, os, subprocess, time
from dataclasses import asdict
from datetime import datetime, timezone
import numpy as np
import mlx.core as mx
import mlx.nn as nn
from mlx.utils import tree_unflatten
from src.models.bc import B100,C101,c_microbatch_loss
from src.models.core import masked_cross_entropy,parameter_inventory
from src.models.training import AdamW,GradientAccumulator,flat_parameters
from src.models.edits import canonical_labels,events,update_denominators

assert os.environ.get('MLX_ENABLE_TF32') == '0', 'True FP32 parity requires MLX_ENABLE_TF32=0 before import'
OUTPUT=Path(__file__).parent
PAIRS=(('aa','ba'),('ab','ab'),('bb','b'),('ba','aa'))
UPDATES=160
LR=3e-4

def file_hash(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def weight_hash(model):
    value=hashlib.sha256()
    for name,tensor in sorted(flat_parameters(model).items()):
        value.update(name.encode());value.update(np.asarray(tensor).tobytes())
    return value.hexdigest()

def c_example(source,target):
    program=canonical_labels(source,target,tuple(bytes([b]) for b in source.encode()))
    labels=events(program,lambda text:list(text.encode()),{i:i for i in range(len(source)+1)})
    return dict(source_ids=mx.array([[308,259,*source.encode()]],dtype=mx.int32),
                labels=labels,encoder_positions=tuple(range(1,len(source)+2)),
                legal=mx.array([True]*(len(source)+1)))

rows=[c_example(s,t) for s,t in PAIRS]
denom=update_denominators([[row['labels'] for row in rows]])
valid_b=sum(len(t.encode())+1 for s,t in PAIRS)

def b_loss(model,index):
    source,target=PAIRS[index]
    ids=mx.array([[257,*target.encode()]],dtype=mx.int32)
    labels=mx.array([[*target.encode(),258]],dtype=mx.int32)
    logits=model(rows[index]['source_ids'],ids)
    return masked_cross_entropy(logits,labels,mx.ones(labels.shape,dtype=mx.bool_))/valid_b

def c_loss(model,index):return c_microbatch_loss(model,[rows[index]],denom)

def diagnose(model,name):
    observations=[]
    for i,(source,target) in enumerate(PAIRS):
        encoded=model.encode(rows[i]['source_ids'])
        perturbed=rows[i]['source_ids'].at[0,-1].add(1)
        changed=model.encode(perturbed)
        encoder_source_effect=float(mx.max(mx.abs(encoded-changed)).item())
        if name=='B100':
            decoder=mx.array([[257,*target.encode()]],dtype=mx.int32)
            hidden,_=model.decode(decoder,encoded)
            teacher_logits=model.logits(hidden)
            targets=[*target.encode(),258]
            predictions=mx.argmax(teacher_logits,axis=-1).tolist()[0]
            token_losses=(mx.logsumexp(teacher_logits.astype(mx.float32),axis=-1)-mx.take_along_axis(teacher_logits,mx.array([targets])[...,None],axis=-1)[...,0]).tolist()[0]
            current=mx.array([[257]],dtype=mx.int32);cache=None;prefix=[257];differences=[]
            for step in range(8):
                h,cache=model.decode(current,encoded,caches=cache)
                full,_=model.decode(mx.array([prefix],dtype=mx.int32),encoded)
                cached_logits=model.logits(h[:,-1:]);full_logits=model.logits(full[:,-1:])
                differences.append(float(mx.max(mx.abs(cached_logits-full_logits)).item()))
                token=int(mx.argmax(cached_logits[0,-1]).item())
                if token==258:break
                prefix.append(token);current=mx.array([[token]],dtype=mx.int32)
            first,_=model.decode(mx.array([[257]]),encoded)
            other,_=model.decode(mx.array([[257]]),changed)
            observation={'teacher_targets':targets,'teacher_predictions':predictions,'token_cross_entropy':token_losses,
                         'greedy_cache_vs_full_max_abs':max(differences),
                         'first_logits_source_perturbation_max_abs':float(mx.max(mx.abs(model.logits(first)-model.logits(other))).item())}
        else:
            from src.models.bc import boundary_features
            labels=rows[i]['labels'];boundaries=boundary_features(encoded,rows[i]['encoder_positions'])
            inputs=model.teacher_inputs(labels,boundaries)
            hidden,_=model.decode(None,encoded,inputs=inputs)
            pieces=[];cache=None
            for position in range(inputs.shape[1]):
                piece,cache=model.decode(None,encoded,caches=cache,inputs=inputs[:,position:position+1])
                pieces.append(piece)
            cache_error=float(mx.max(mx.abs(hidden-mx.concatenate(pieces,axis=1))).item())
            predictions={'action':[],'start':[],'end':[],'vocabulary':[]};previous=0
            for position,target_action in labels.action:
                predictions['action'].append([target_action,int(mx.argmax(model.action_logits(hidden[:,position:position+1])[0,0]).item())])
            for (position,a),(end_position,b) in zip(labels.start,labels.end):
                for key,pos,tgt,minimum in [('start',position,a,previous),('end',end_position,b,a)]:
                    logits=model.pointer_logits(hidden[:,pos:pos+1],boundaries,end=key=='end',legal=rows[i]['legal'],minimum_index=minimum)
                    predictions[key].append([tgt,int(mx.argmax(logits[0,0]).item())])
                previous=b
            for position,tgt in labels.vocabulary:
                predictions['vocabulary'].append([tgt,int(mx.argmax(model.logits(hidden[:,position:position+1])[0,0]).item())])
            component={k:float(v.item()) for k,v in model.component_sums(**rows[i]).items()}
            denominator=labels.denominators
            first,_=model.decode(mx.array([[257]]),encoded)
            other,_=model.decode(mx.array([[257]]),changed)
            observation={'teacher_target_prediction_pairs':predictions,'component_sums':component,
                         'component_denominators':denominator,
                         'component_mean_ce':{k:component[k]/denominator[k] if denominator[k] else 0. for k in component},
                         'teacher_feedback_cache_vs_full_max_abs':cache_error,
                         'first_action_logits_source_perturbation_max_abs':float(mx.max(mx.abs(model.action_logits(first)-model.action_logits(other))).item())}
        observation.update({'source':source,'reference':target,'encoder_source_perturbation_max_abs':encoder_source_effect})
        observations.append(observation)
    return observations

started=datetime.now(timezone.utc).isoformat()
config={'classification':'BOUNDED_EXACT_GEOMETRY_CORRECTNESS_NOT_10M','pairs':PAIRS,'updates_per_arm':UPDATES,
        'seed':42,'learning_rate':LR,'working_dtype':'float32','microbatches_per_update':4,
        'B_valid_targets_per_update':valid_b,'C_component_denominators':denom,'C_decoder_call_cap':24,
        'C_max_edits_per_call':4,'actual_source_positions_per_update':sum(r['source_ids'].size for r in rows),
        'C_event_positions_per_update':sum(len(r['labels'].inputs) for r in rows),
        'B100_config':asdict(B100().config),'TF32':os.environ['MLX_ENABLE_TF32'],
        'code_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'dirty_state':subprocess.check_output(['git','status','--porcelain'],text=True).splitlines(),
        'hashes':{p:file_hash(p) for p in ('src/models/core.py','src/models/training.py','src/models/bc.py',
                        'src/models/edits.py',__file__)}}
(OUTPUT/'config.json').write_text(json.dumps(config,indent=2)+'\n')
(OUTPUT/'pairs.json').write_text(json.dumps(PAIRS)+'\n')
(OUTPUT/'input_identity.json').write_text(json.dumps({'config_sha256':file_hash(OUTPUT/'config.json'),'data_sha256':file_hash(OUTPUT/'pairs.json'),'captured_before_updates':True},indent=2)+'\n')
if (OUTPUT/'results.json').exists():raise FileExistsError('never overwrite previous run evidence')
results=[]
with (OUTPUT/'steps.jsonl').open('x') as log:
    for name,cls,fn in [('B100',B100,b_loss),('C101',C101,c_loss)]:
        model=cls(seed=42)
        mx.eval(model.parameters())
        inventory=parameter_inventory(model)
        initial=weight_hash(model)
        optimizer=AdamW(flat_parameters(model))
        accumulator=GradientAccumulator(flat_parameters(model))
        get_grad=nn.value_and_grad(model,fn)
        initial_diagnostics=diagnose(model,name)
        (OUTPUT/f'{name}_initial_diagnostics.json').write_text(json.dumps(initial_diagnostics,indent=2)+'\n')
        initial_loss=sum(float(fn(model,i).item()) for i in range(len(PAIRS)))
        begin=time.perf_counter()
        for step in range(UPDATES):
            losses=[]
            for i in range(len(PAIRS)):
                value,grad=get_grad(model,i)
                mx.eval(value,grad)
                losses.append(float(value.item()))
                accumulator.add(grad)
                del grad
            weights,norm=optimizer.apply(flat_parameters(model),accumulator.gradients(already_normalized=True),LR)
            model.update(tree_unflatten(list(weights.items())))
            accumulator.clear();mx.eval(model.parameters(),optimizer.m,optimizer.v,accumulator.values)
            entry={'model':name,'step':step+1,'loss':sum(losses),'gradient_norm':norm,
                   'seconds_since_start':time.perf_counter()-begin,'MLX_active_bytes':mx.get_active_memory(),
                   'MLX_peak_bytes':mx.get_peak_memory()}
            log.write(json.dumps(entry)+'\n');log.flush()
            if step in (0,19,39,79,159):print(json.dumps(entry),flush=True)
        train_seconds=time.perf_counter()-begin
        predictions=[]
        for i,(source,target) in enumerate(PAIRS):
            if name=='B100':
                generated=model.greedy_text(rows[i]['source_ids'],max_tokens=8)
                try: output=bytes(generated['token_ids']).decode('utf-8')
                except (ValueError,UnicodeError):output=None
                prediction={'source':source,'reference':target,'output':output,'status':generated['status']}
            else:
                generated=model.greedy_edits(source,rows[i]['source_ids'],rows[i]['encoder_positions'],
                    tuple(range(len(source)+1)),rows[i]['legal'],lambda token:bytes([token]),
                    max_edits=4,max_decoder_positions=24)
                prediction={'source':source,'reference':target,'output':generated['output'],
                            'status':generated['status'],'decoder_positions':generated['decoder_positions']}
            prediction['completed_exact']=prediction['status']=='completed' and prediction['output']==target
            predictions.append(prediction)
        final_diagnostics=diagnose(model,name)
        (OUTPUT/f'{name}_final_diagnostics.json').write_text(json.dumps(final_diagnostics,indent=2)+'\n')
        final_loss=sum(float(fn(model,i).item()) for i in range(len(PAIRS)))
        result={'model':name,'initial_weight_sha256':initial,'final_weight_sha256':weight_hash(model),
                'parameter_count':sum(x['count'] for x in inventory),'inventory':inventory,
                'initial_loss':initial_loss,'final_loss':final_loss,'updates':UPDATES,
                'training_seconds':train_seconds,'predictions':predictions,
                'completed_exact':sum(p['completed_exact'] for p in predictions),
                'optimizer_policy':optimizer.policy(),'final_diagnostics':final_diagnostics,
                'pass':sum(p['completed_exact'] for p in predictions)==4,
                'master_dtypes':sorted({str(v.dtype) for v in flat_parameters(model).values()}),
                'moment_dtypes':sorted({str(v.dtype) for v in optimizer.m.values()}),
                'accumulator_dtypes':sorted({str(v.dtype) for v in accumulator.values.values()}),
                'maximum_peak_bytes':mx.get_peak_memory()}
        results.append(result)
        print(json.dumps({k:v for k,v in result.items() if k!='inventory'}),flush=True)
        (OUTPUT/f'{name}_result.json').write_text(json.dumps(result,indent=2)+'\n')
        del model,optimizer,accumulator,get_grad,weights
        gc.collect();mx.clear_cache();mx.reset_peak_memory()
receipt={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'results':results,
         'no_heldout_data':True,'no_10M_probe':True,'no_final_seed':True,'no_BENCH00_claim':True}
(OUTPUT/'results.json').write_text(json.dumps(receipt,indent=2)+'\n')
