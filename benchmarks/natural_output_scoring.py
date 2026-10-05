"""All preselected natural DEVELOPMENT outputs; independent caps unchanged."""
import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time
import tracemalloc
from src.scoring.records import prepare_source,score_output,Output,aggregate
from src.scoring.triple import Limits,serialize
from src.scoring.text import lexical,POLICY_HASH


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def validate_panels(rows):
    ids={r['id'] for r in rows}
    if len(ids)!=24:raise ValueError('24 frozen natural requests required')
    for step in {r['step'] for r in rows}:
        panel=[r['id'] for r in rows if r['step']==step]
        if len(panel)!=24 or set(panel)!=ids:raise ValueError('missing or duplicate panel request')
    keys={r['id']:(r['reference'],r['raw_source']) for r in rows}
    if any(keys[r['id']]!=(r['reference'],r['raw_source']) for r in rows):raise ValueError('changed preflight inputs')
    return keys


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--outputs',required=True);parser.add_argument('--out',required=True)
    parser.add_argument('--system',default='ByT5_native_greedy')
    args=parser.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    rows=[r for r in map(json.loads,Path(args.outputs).read_text().splitlines()) if not r['identity_control']]
    keys=validate_panels(rows)
    limits=Limits()
    provenance={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'dirty_status':subprocess.check_output(['git','status','--porcelain'],text=True),
        'dirty_diff':subprocess.check_output(['git','diff','--binary'],text=True),
        'output_sha256':sha(args.outputs),'code_hashes':{p:sha(p) for p in [__file__,*[str(p) for p in sorted(Path('src/scoring').glob('*.py'))]]},
        'limits':asdict(limits),'normalization_tables_hash':POLICY_HASH,'scope':'PRESELECTED_LSPC_NATURAL_DEV_ONLY',
        'panels':sorted({r['step'] for r in rows}),'controls_excluded':True,'seed':'deterministic all-optimal scorer',
        'primary_equal_domain_endpoint':None,'system':args.system}
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    tracemalloc.start();begin=time.perf_counter()
    fixed={i:prepare_source(r,s,limits) for i,(r,s) in sorted(keys.items())}
    (out/'source_preflights.json').write_text(json.dumps({i:{'source_hash':p.source_hash,'reference_hash':p.reference_hash,
        'mask_hash':p.mask_hash,'preflight_hash':p.preflight_hash,'eS':p.eS} for i,p in fixed.items()},indent=2)+'\n')
    preflight_seconds=time.perf_counter()-begin;records=[]
    for row in rows:
        start=time.perf_counter();decoded=row['decoded']
        record=score_output(fixed[row['id']],Output(decoded['text'],decoded['status']),limits)
        record.update(case_id=row['id'],step=row['step'],role=row['role'],cluster_ids=[row['source_group_id']],
            reference_policy_id='text_raw_development_v1',output_view=args.system,
            byte_nonidentity=decoded['text']!=row['raw_source'],
            lexical_nonidentity=lexical(decoded['text'] or '')!=lexical(row['raw_source']),
            seconds=time.perf_counter()-start)
        records.append(record)
        with (out/'records.jsonl').open('a') as f:f.write(serialize(record)+'\n')
        print(json.dumps({'step':row['step'],'id':row['id'],'status':record['status'],'seconds':record['seconds']}),flush=True)
    _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    panels={}
    for step in sorted({r['step'] for r in records}):
        selected=[r for r in records if r['step']==step]
        panels[str(step)]={'cases':len(selected),'byte_nonidentity':sum(r['byte_nonidentity'] for r in selected),
            'lexical_nonidentity':sum(r['lexical_nonidentity'] for r in selected),'complete':sum(r['complete_valid'] for r in selected),
            'aggregate_pooled':aggregate(selected),'status_counts':dict(Counter(r['status'] for r in selected)),
            'point_totals':sum(r['repair'][0]==r['repair'][1] and r['introduced'][0]==r['introduced'][1] for r in selected),
            'caps':sum(r.get('fallback_reason') is not None for r in selected),
            'repair_total_width':sum(r['repair'][1]-r['repair'][0] for r in selected),
            'introduced_total_width':sum(r['introduced'][1]-r['introduced'][0] for r in selected),
            'local_ambiguous_cases':sum(any(len(v)>1 for v in (r['reference_events'] or [])) for r in selected),
            'seconds':sum(r['seconds'] for r in selected),'max_states':max(r['joint_states'] for r in selected),
            'max_edges':max((r['joint_edges'] or 0) for r in selected)}
    summary={'panels':panels,'preflight_seconds':preflight_seconds,'total_seconds':time.perf_counter()-begin,
        'python_traced_peak_bytes':peak,'process_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'records_sha256':sha(out/'records.jsonl'),'distinct_requests':24,
        'source_components':len({r['source_group_id'] for r in rows}),
        'repeated_panels_are_not_new_cases':True,
        'H1_precision':'not established from small LS-only panel; SLUE unavailable'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
