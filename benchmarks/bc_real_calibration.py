"""Real BPE/ASR workload calibration; no 10M recipe or sealed inference."""
import argparse
from dataclasses import asdict
import gc
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import resource
import subprocess
import time
import numpy as np

from src.data.development_reader import load_targets
from src.models.tokenizer import ByteBPE, BOS, EOS, PAD, SEP, RESTORE_REFERENCE
from src.models.edits import canonical_labels, events, render, update_denominators


def sha(path):
    return hashlib.file_digest(Path(path).open('rb'),'sha256').hexdigest()


def check_anchor_bound(total,queued,cap):
    if total+queued>cap:raise RuntimeError('complete batch would exceed calibration anchor bound')


def decode_literal(tokenizer,answer):
    reason=None
    try:output=tokenizer.decode(answer['token_ids'])
    except (ValueError,UnicodeError) as error:
        output=None;reason={'type':type(error).__name__,'message':str(error)}
    status=answer['status'] if output is not None else 'invalid_byte_decoding'
    return output,status,{'token_ids':answer['token_ids'],'underlying_model_status':answer['status'],'decode_failure':reason}


def shape(row, tokenizer):
    tokenized=tokenizer.source(row['source'])
    program=canonical_labels(row['source'],row['target'],tuple(tokenizer.byte_map[t] for t in tokenized.ids))
    if render(row['source'],program)!=row['target']:raise ValueError('gold render mismatch')
    labels=events(program,tokenizer.encode,{p:i for i,p in enumerate(tokenized.byte_offsets)})
    target=tokenizer.encode(row['target'])
    return {**row,'source_ids':[RESTORE_REFERENCE,SEP,*tokenized.ids,EOS],
        'target_ids':target,'encoder_positions':list(range(1,len(tokenized.ids)+2)),
        'byte_offsets':list(tokenized.byte_offsets),'legal':list(tokenized.legal_pointer_mask),
        'K':len(program.edits),'R':labels.replacement_tokens,'c_positions':len(labels.inputs),
        'density':len(program.edits)/max(1,len(tokenized.ids)),
        'anchors':2+2*len(target)+1,'source_bpe':len(tokenized.ids),'target_bpe':len(target),
        'edits':[asdict(e) for e in program.edits]}


def select_buckets(rows):
    ranked=sorted(rows,key=lambda r:(r['density'],r['id']))
    buckets={}
    for index,name in enumerate(('low','median','high')):
        part=ranked[index*len(ranked)//3:(index+1)*len(ranked)//3]
        ordered=sorted(part,key=lambda r:(r['source_bpe'],r['id']))
        buckets[name]=[{**ordered[min(len(ordered)-1,int(q*(len(ordered)-1)))],'bucket':name} for q in (.15,.4,.65,.9)]
    chosen=[r for part in buckets.values() for r in part]
    if len({r['id'] for r in chosen})!=12:raise ValueError('duplicate preselection')
    return chosen


def prepare(destination):
    roles='experiments/manifests/public_lspc_training_roles.development.jsonl'
    supply='experiments/manifests/public_lspc_training_supply_qualification.json'
    admitted={r['id']:r for r in load_targets(roles,supply,allowed_roles={'train','calibration'})}
    pairpath='exports/foundation-repair/development-asr-pairs-attempt01/pairs.jsonl'
    tokenizer=ByteBPE.load('configs/tokenizer_development')
    rows=[];calibration=[];failures=[]
    for p in map(json.loads,Path(pairpath).read_text().splitlines()):
        if p['role'] not in ('train','calibration'):continue
        r=admitted[p['id']]
        if r['target']!=p['target'] or r['source_group_id']!=p['source_group_id']:raise ValueError('lineage mismatch')
        if p['status']!='COMPLETED':failures.append({'id':p['id'],'reason':'source_failure'});continue
        if hashlib.sha256(p['source'].encode()).hexdigest()!=p['source_sha256']:raise ValueError('source mismatch')
        shaped=shape(p,tokenizer)
        if max(len(shaped['source_ids']),shaped['target_bpe']+1,shaped['c_positions'])>1024:
            failures.append({'id':p['id'],'reason':'context_overflow'});continue
        (rows if p['role']=='train' else calibration).append(shaped)
    selected=select_buckets(rows)
    holdout=select_buckets(calibration)
    if {r['source_group_id'] for r in selected}&{r['source_group_id'] for r in holdout}:
        raise ValueError('calibration group leakage')
    config={'scope':'REAL_TRAIN_SHAPE_CALIBRATION_NOT_10M_RECIPE','seed':42,'batch':4,
        'fit_updates':300,'fit_lr':.0003,'sustained_seconds':1200,'sustained_lr':0.,
        'warmups':5,'minimum_timed_updates':100,'decode_repeats':2,'decode_cap':256,
        'source_padding':'each queued batch pads to maximum source plus8 masked positions',
        'C_loss':'global queued-update component denominators, each source individually encoded',
        'B_loss':'global valid shifted full-target denominator, dynamic target PAD mask',
        'selection':'TRAIN only;density thirds;source-length quantiles .15,.4,.65,.9 within each;no candidate outputs',
        'learning_scope':'12 natural training calibration fixtures; no generalization claim',
        'hard_presented_anchor_cap':8000000,'full_campaign_32k_anchor_update_qualification':False}
    identities={p:sha(p) for p in (pairpath,roles,supply,'configs/tokenizer_development/tokenizer.json')}
    distributions={k:{'min':min(r[k] for r in rows),'median':float(np.median([r[k] for r in rows])),
        'p95':float(np.quantile([r[k] for r in rows],.95)),'max':max(r[k] for r in rows)}
        for k in ('source_bpe','target_bpe','K','R','c_positions','density','anchors')}
    path=Path(destination);path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():raise FileExistsError(path)
    path.write_text(json.dumps({'config':config,'identities':identities,'eligible_rows':len(rows),
        'failures':failures,'distribution':distributions,'selected':selected,'decode_holdout':holdout,
        'calibration_consumption':{'ids':[r['id'] for r in holdout],
            'new_role':'native_decode_development_consumed','fit_forbidden':True}},indent=2)+'\n')
    print(json.dumps({'eligible':len(rows),'selected':len(selected),'distribution':distributions}),flush=True)


def run(arm,prepared,out):
    import mlx.core as mx
    import mlx.nn as nn
    from mlx.utils import tree_unflatten
    from src.models.bc import B100,C101,c_microbatch_loss
    from src.models.core import masked_cross_entropy,parameter_inventory
    from src.models.training import AdamW,GradientAccumulator,flat_parameters
    from benchmarks.model0_correctness import parameter_hash
    if os.environ.get('MLX_ENABLE_TF32')!='0':raise ValueError('explicit TF32 disable required')
    data=json.loads(Path(prepared).read_text());cfg=data['config']
    for p,h in data['identities'].items():
        if sha(p)!=h:raise ValueError('changed data/tokenizer')
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    paths=(__file__,'src/models/bc.py','src/models/core.py','src/models/edits.py','src/models/training.py','src/models/tokenizer.py')
    provenance={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'dirty_status':subprocess.check_output(['git','status','--porcelain'],text=True),
        'dirty_diff':subprocess.check_output(['git','diff','--binary'],text=True),
        'config':cfg,'prepared_sha256':sha(prepared),'data_identities':data['identities'],
        'code_hashes':{p:sha(p) for p in paths},'runtime':{'python':platform.python_version(),
        'mlx':importlib.metadata.version('mlx'),'numpy':importlib.metadata.version('numpy'),
        'TF32':os.environ.get('MLX_ENABLE_TF32'),'platform':platform.platform(),'metal':mx.device_info()},
        'initial_thermal':subprocess.check_output(['pmset','-g','therm'],text=True),
        'arm':arm,'no_concurrent_accelerator':True}
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    tokenizer=ByteBPE.load('configs/tokenizer_development');rows=data['selected']
    cls=B100 if arm=='B100' else C101
    model=cls(seed=42);count=sum(r['count'] for r in parameter_inventory(model))
    if count!=(100686336 if arm=='B100' else 101081859):raise ValueError('exact geometry mismatch')
    optimizer=AdamW(flat_parameters(model));acc=GradientAccumulator(flat_parameters(model))
    (out/'initial_identity.json').write_text(json.dumps({'parameters':count,'model_config':asdict(model.config),
        'initial_weights_sha256':parameter_hash(model),'optimizer':optimizer.policy(),
        'dtypes':{'master':'float32','moments':'float32','accumulation':'float32','working':'bfloat16','loss':'float32'},
        'prepared_sha256':sha(prepared)},indent=2)+'\n')
    totals={'anchors':0,'native_source':0,'padded_source':0,'native_decoder':0,'valid_loss_decisions':0}
    timed=[];thermal=[];allrows=[]
    def update(step,phase,lr):
        queued=[rows[(step*4+j)%len(rows)] for j in range(4)]
        source_width=max(len(r['source_ids']) for r in queued)+8
        source_ids=mx.array([r['source_ids']+[PAD]*(source_width-len(r['source_ids'])) for r in queued])
        source_valid=source_ids!=PAD
        counts={'anchors':sum(r['anchors'] for r in queued),'native_source':sum(len(r['source_ids']) for r in queued),
            'padded_source':source_ids.size,'source_padding':source_ids.size-sum(len(r['source_ids']) for r in queued)}
        check_anchor_bound(totals['anchors'],counts['anchors'],cfg['hard_presented_anchor_cap'])
        if arm=='B100':
            width=max(r['target_bpe']+1 for r in queued)
            decoder=mx.array([[BOS,*r['target_ids']]+[PAD]*(width-r['target_bpe']-1) for r in queued])
            targets=mx.array([[*r['target_ids'],EOS]+[PAD]*(width-r['target_bpe']-1) for r in queued])
            valid=targets!=PAD;den=int(mx.sum(valid))
            def loss(m):return masked_cross_entropy(m(source_ids,decoder,source_valid,dtype=mx.bfloat16),targets,valid)/den
            counts.update(native_decoder=den,padded_decoder=decoder.size,valid_loss_decisions=den)
        else:
            labels=[];examples=[]
            for i,r in enumerate(queued):
                canonical=canonical_labels(r['source'],r['target'],tuple(tokenizer.byte_map[t] for t in tokenizer.encode(r['source'])))
                lab=events(canonical,tokenizer.encode,{p:j for j,p in enumerate(r['byte_offsets'])})
                labels.append(lab)
                examples.append(dict(source_ids=source_ids[i:i+1],labels=lab,
                    encoder_positions=tuple(r['encoder_positions']),legal=mx.array(r['legal']),source_valid=source_valid[i:i+1]))
            den=update_denominators([labels])
            def loss(m):return c_microbatch_loss(m,examples,den,dtype=mx.bfloat16)
            counts.update(native_decoder=sum(len(l.inputs) for l in labels),padded_decoder=sum(len(l.inputs) for l in labels),
                valid_loss_decisions=sum(den.values()),components=den)
        begin=time.perf_counter()
        value,grad=nn.value_and_grad(model,loss)(model);mx.eval(value,grad)
        if not math.isfinite(float(value)):raise ValueError('nonfinite loss')
        acc.add(grad);weights,norm=optimizer.apply(flat_parameters(model),acc.gradients(already_normalized=True),lr)
        model.update(tree_unflatten(list(weights.items())));acc.clear()
        mx.eval(model.parameters(),optimizer.m,optimizer.v,acc.values);mx.synchronize()
        seconds=time.perf_counter()-begin
        item={'step':step,'phase':phase,'lr':lr,'seconds':seconds,'loss':float(value),'gradient_norm':norm,
            'ids':[r['id'] for r in queued],'peak_mlx_bytes':mx.get_peak_memory(),'active_mlx_bytes':mx.get_active_memory(),**counts}
        with (out/'updates.jsonl').open('a') as f:f.write(json.dumps(item)+'\n')
        for k in totals:totals[k]+=counts[k]
        allrows.append(item)
        return item
    for i in range(cfg['fit_updates']):
        item=update(i,'bounded_natural_fixture_fit',cfg['fit_lr'])
        if i%100==0:print(json.dumps({'phase':'fit','arm':arm,'step':i,'loss':item['loss']}),flush=True)
    for i in range(cfg['warmups']):update(cfg['fit_updates']+i,'timing_warmup',0.)
    start=time.perf_counter();last=0;i=cfg['fit_updates']+cfg['warmups']
    while time.perf_counter()-start<cfg['sustained_seconds'] or len(timed)<cfg['minimum_timed_updates']:
        if totals['anchors']>=cfg['hard_presented_anchor_cap']:raise RuntimeError('calibration anchor bound exceeded')
        item=update(i,'sustained_complete_update_zero_lr',0.);timed.append(item);i+=1
        elapsed=time.perf_counter()-start
        if elapsed-last>=60:
            therm={'elapsed_seconds':elapsed,'pmset':subprocess.check_output(['pmset','-g','therm'],text=True)}
            thermal.append(therm);last=elapsed
            (out/'thermal.json').write_text(json.dumps(thermal,indent=2)+'\n')
            print(json.dumps({'arm':arm,'sustained_seconds':elapsed,'updates':len(timed),'last_loss':item['loss']}),flush=True)
    wall=time.perf_counter()-start
    # Same frozen complete requests for both arms; never select by decode success.
    decodes=[]
    for r in rows+data['decode_holdout']:
        for repeat in range(cfg['decode_repeats']):
            ids=mx.array([r['source_ids']+[PAD]*8]);valid=ids!=PAD
            mx.synchronize();begin=time.perf_counter()
            if arm=='B100':
                answer=model.greedy_text(ids,source_valid=valid,max_tokens=cfg['decode_cap'],dtype=mx.bfloat16)
                positions=len(answer['token_ids'])+(answer['status']=='completed')
                output,status,raw=decode_literal(tokenizer,answer)
            else:
                answer=model.greedy_edits(r['source'],ids,tuple(r['encoder_positions']),tuple(r['byte_offsets']),mx.array(r['legal']),
                    lambda t:tokenizer.byte_map[t],source_valid=valid,max_decoder_positions=cfg['decode_cap'],dtype=mx.bfloat16)
                output=answer['output'];status=answer['status'];positions=answer['decoder_positions']
                raw={'program':None if answer['program'] is None else asdict(answer['program']),'reason':answer.get('reason')}
            mx.synchronize();elapsed=time.perf_counter()-begin
            record={'id':r['id'],'role':r['role'],'source_group_id':r['source_group_id'],
                'bucket':r['bucket'],'repeat':repeat,'source':r['source'],'target':r['target'],
                'output':output,'status':status,'seconds':elapsed,'positions':positions,'reference_positions':r['target_bpe']+1,
                'gold_C_positions':r['c_positions'],'K':r['K'],'R':r['R'],'complete_boundary_includes_encoder_renderer':True,**raw}
            decodes.append(record)
            with (out/'decodes.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
    summary={'arm':arm,'scope':cfg['scope'],'timed_updates':len(timed),'sustained_wall_seconds':wall,
        'timed_update_seconds':sum(r['seconds'] for r in timed),'mean_update_seconds':float(np.mean([r['seconds'] for r in timed])),
        'p50_update_seconds':float(np.median([r['seconds'] for r in timed])),'p95_update_seconds':float(np.quantile([r['seconds'] for r in timed],.95)),
        'canonical_anchors_per_wall_second':sum(r['anchors'] for r in timed)/wall,
        'native_source_per_wall_second':sum(r['native_source'] for r in timed)/wall,
        'native_decoder_per_wall_second':sum(r['native_decoder'] for r in timed)/wall,
        'first_100_mean_update_seconds':float(np.mean([r['seconds'] for r in timed[:100]])),
        'last_100_mean_update_seconds':float(np.mean([r['seconds'] for r in timed[-100:]])),
        'peak_mlx_bytes':mx.get_peak_memory(),'total_presentations':totals,
        'peak_process_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'complete_decode_calls':sum(r['status']=='completed' for r in decodes),'decode_calls':len(decodes),
        'decode_total_seconds':sum(r['seconds'] for r in decodes),'exact_target_calls':sum(r['output']==r['target'] for r in decodes),
        'final_weights':parameter_hash(model),'final_thermal':subprocess.check_output(['pmset','-g','therm'],text=True),
        'no_10M_recipe_slot_consumed':True,'full_32k_anchor_campaign_calibration':False}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--prepare');p.add_argument('--arm',choices=['B100','C101'])
    p.add_argument('--prepared');p.add_argument('--out');a=p.parse_args()
    if a.prepare:prepare(a.prepare)
    else:run(a.arm,a.prepared,a.out)


if __name__=='__main__':main()
