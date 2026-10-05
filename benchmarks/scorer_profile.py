"""Development-only computational qualification; no natural population claim."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import resource
import subprocess
import time
import tracemalloc
from src.scoring.triple import score_tokens, serialize


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    destination=Path(args.out)
    destination.mkdir(parents=True,exist_ok=False)
    manifest=Path('experiments/manifests/scorer_development_parity.json')
    inputs=json.loads(manifest.read_text())['triples']
    inputs += [{'id':'repeated-64-32-32','r':['a']*64,'s':['a']*32,'o':['b']*32},
               {'id':'fixed-insertion-gap-tie','r':['L','R'],'s':['L','a','b','R'],'o':['L','b','c','R']}]
    provenance={'commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
                'dirty':subprocess.check_output(['git','status','--porcelain=v1'],text=True),
                'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),
                'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'seed':20261004,'population':'synthetic development only',
                'cpu_interference':'parallel coding/correctness possible; not exclusive native campaign',
                'configuration':{'pair_cells':4000000,'joint_states':250000,'joint_moves':1750000}}
    tracemalloc.start();start=time.perf_counter();rows=[]
    with (destination/'per_case.jsonl').open('w') as output:
        for row in inputs:
            then=time.perf_counter()
            result=score_tokens(row['r'],row['s'],row['o'])
            result['case_id']=row['id'];result['elapsed_seconds']=time.perf_counter()-then
            output.write(serialize(result)+'\n')
            rows.append(result)
    elapsed=time.perf_counter()-start
    _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    summary=provenance|{'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'cases':len(rows),'elapsed_seconds':elapsed,'cases_per_second':len(rows)/elapsed,
        'python_traced_peak_bytes':peak,'process_peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'cap_cases':sum(r['status']=='resource_envelope' for r in rows),
        'count_ambiguous_cases':sum(r['repair'][0]!=r['repair'][1] for r in rows),
        'local_ambiguous_cases':sum(r['reference_events'] is not None and any(len(v)>1 for v in r['reference_events']) for r in rows),
        'max_joint_states':max(r['joint_states'] for r in rows),
        'max_joint_edges':max(r['joint_edges'] or 0 for r in rows),
        'max_examined_moves':max(r['joint_moves'] for r in rows),
        'max_repair_bound_width':max(r['repair'][1]-r['repair'][0] for r in rows),
        'per_case_sha256':hashlib.sha256((destination/'per_case.jsonl').read_bytes()).hexdigest()}
    (destination/'summary.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
