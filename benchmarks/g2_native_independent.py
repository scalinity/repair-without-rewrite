"""CPU/NumPy reconstruction of native consumption, persisted states and costs."""
import argparse
import bisect
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path
import time

from src.data.g2_artifacts import ArtifactRoot,read_complete,sha256


def records(path):
    return [json.loads(line) for line in Path(path).open()]


def persisted_hash(path):
    import numpy as np
    meta=json.loads((path/"metadata.json").read_text());digest=hashlib.sha256()
    with np.load(path/"arrays.npz",allow_pickle=False) as arrays:
        for key in sorted(arrays.files):
            value=arrays[key]
            assert str(value.dtype)==meta["dtypes"][key] and list(value.shape)==meta["shapes"][key]
            assert np.isfinite(value).all()
            if key.startswith("acc::") and meta["accumulator_microbatches"]==0:assert not np.any(value)
            digest.update(json.dumps([key,list(value.shape),str(value.dtype)],separators=(",",":")).encode())
            digest.update(value.tobytes())
    digest.update(json.dumps([meta["optimizer_step"],meta["committed_exposure"],meta["pending_charge"],
        meta["completed_microbatches"],meta["denominators"],meta["partition"],meta["loss"]],sort_keys=True).encode())
    combined=hashlib.sha256();combined.update(digest.hexdigest().encode())
    combined.update(json.dumps(meta["stream"],sort_keys=True,separators=(",",":"),allow_nan=False).encode())
    combined.update(json.dumps(meta["actual_consumption"],sort_keys=True,separators=(",",":"),allow_nan=False).encode())
    assert combined.hexdigest()==meta["deterministic_state_sha256"]
    return combined.hexdigest(),meta


def run(binding,attempt):
    root=ArtifactRoot(binding);before=root.preflight();started=time.perf_counter()
    receipt=Path(f"experiments/manifests/generation_2/independent-native.attempt{attempt:02d}.json")
    if receipt.exists():raise FileExistsError(receipt)
    freeze=json.loads(Path("experiments/manifests/generation_2/corpus-freeze.attempt01.json").read_text())
    generated=records("exports/lexical-reader-v2/generated-pool-attempt02/accepted.jsonl")
    summaries={};paired={}
    for data,condition in (("D0","U8"),("D1","U1"),("D1","U8")):
        path=root.path(freeze["conditions"][data]["artifact_relative"]);read_complete(path)
        lookup={row["variant_id"]:row for row in [*generated,*records(path/"natural.jsonl")]}
        ledger=records(path/"presentations.jsonl");masters=json.loads((path/"masters.json").read_text())
        pools=defaultdict(list)
        for index,item in enumerate(masters):
            phase=max(("P0","P1","P2"),key=lambda p:item["phase_segments"].get(p,0));pools[phase].append(index)
        for arm in ("B100","C101"):
            name=f"{arm}-{data}-{condition}.attempt01";bench=root.path("bench-v1/"+name);read_complete(bench)
            report=json.loads(Path(f"experiments/manifests/generation_2/bench-{name}.json").read_text())
            assert report["status"]=="PASS_G2_NATIVE_BENCH_COLD_PENDING"
            phase_cursor=Counter();phase_charge=Counter();selector=exposure=0;selected=None;sub=0
            all_rows=records(bench/"updates.jsonl");prefix=[];phases=Counter()
            assert Counter(row["segment"] for row in all_rows)["warmup"]==5
            assert Counter(row["segment"] for row in all_rows)["timed"]==100
            sustained=[row for row in all_rows if row["segment"]=="sustained"]
            assert sustained and report["sustained_elapsed_seconds"]>=1200
            for step,row in enumerate(all_rows,1):
                if selected is None:
                    weights={"P0":6666667,"P1":2666667,"P2":666666}
                    phase=max(weights,key=lambda p:(weights[p]*selector-10000000*phase_charge[p],-list(weights).index(p)))
                    selected=pools[phase][phase_cursor[phase]%len(pools[phase])];phase_cursor[phase]+=1
                    item=masters[selected];selector+=item["canonical_charge"];phase_charge.update(item["phase_segments"])
                    master=ledger[item["first_ordinal"]:item["last_ordinal"]+1]
                    cumulative=[];total=0
                    for presentation in master:total+=presentation["canonical_charge"];cumulative.append(total)
                    cuts=[] if condition=="U1" else [bisect.bisect_left([8*c for c in cumulative],j*total)+1 for j in range(1,8)]
                    bounds=[0,*cuts,len(master)]
                part=master[bounds[sub]:bounds[sub+1]];charge=sum(item["canonical_charge"] for item in part);exposure+=charge
                assert (row["update"],row["master_queue_index"],row["subqueue_index"])==(step,selected,sub)
                assert row["canonical_charge"]==charge and row["committed_canonical_exposure"]==exposure
                assert row["presentation_ids"]==[item["presentation_id"] for item in part]
                den={"B":sum(len(lookup[item["variant_id"]]["target_ids"])+1 for item in part),
                     "C":{key:sum(len(lookup[item["variant_id"]]["gold_labels"][key]) for item in part)
                           for key in ("action","start","end","vocabulary")}}
                assert den==row["denominators"] and len(row["actual_consumption"])==len(part)
                assert row["microsteps"]==(len(part)+(15 if arm=="B100" else 3))//(16 if arm=="B100" else 4)
                consumed=[];clock=exposure-charge
                for observed,item in zip(row["actual_consumption"],part):
                    accepted=lookup[item["variant_id"]];clock+=item["canonical_charge"]
                    for key in ("presentation_id","variant_id","canonical_charge","phase","channel"):
                        assert observed[key]==item[key]
                    for key in ("source_sha256","target_sha256","anchor_sha256"):
                        assert observed[key]==accepted[key]
                    assert observed["cumulative_canonical_exposure"]==clock
                    assert [value for value in observed["native_source_ids"] if value!=256]==accepted["source_ids"]
                    if arm=="B100":
                        assert [value for value in observed["native_target_ids_with_EOS"] if value!=256]==accepted["target_ids"]+[258]
                    else:
                        assert observed["native_event_labels"]==accepted["gold_labels"]
                        assert observed["native_encoder_positions"]==accepted["encoder_positions"]
                        assert observed["native_legal_pointer_mask"]==accepted["legal"]
                    consumed.append({key:observed[key] for key in ("presentation_id","variant_id","canonical_charge",
                        "phase","channel","source_sha256","target_sha256","anchor_sha256","cumulative_canonical_exposure")})
                    phases[item["phase"]]+=item["canonical_charge"]
                prefix.append(consumed);sub+=1
                if sub==len(bounds)-1:selected=None;sub=0
            assert set(phases)=={"P0","P1","P2"}
            paired[(arm,data,condition)]=prefix
            wall=sum(row["wall_seconds"] for row in sustained);anchors=sum(row["canonical_charge"] for row in sustained)
            last=sustained[-max(1,len(sustained)//4):]
            conservative=min(anchors/wall,anchors/report["sustained_elapsed_seconds"],
                sum(row["canonical_charge"] for row in last)/sum(row["wall_seconds"] for row in last))
            assert conservative==report["conservative_anchors_per_second"]
            control={row["update"]:row for row in all_rows}
            states={}
            for key in ("initial","boundary","mid","final"):
                snapshot=root.path(f"bench-v1/{name}.{key}");read_complete(snapshot)
                identity,meta=persisted_hash(snapshot);assert meta["schema"]=="paired_complete_actual_update_resume_g2_v1"
                assert meta["data_condition"]==data and meta["update_condition"]==condition
                states[key]=identity
            for kind in ("boundary","mid"):
                cold_name=name+"."+kind;directory=root.path("cold-resume-v1/"+cold_name);read_complete(directory)
                cold=json.loads(Path(f"experiments/manifests/generation_2/cold-{cold_name}.json").read_text())
                assert cold["status"]=="PASS_EXACT_G2_COLD_RESUME" and cold["next_twenty_complete_updates"]==20
                matches=records(directory/"matches.jsonl")
                assert [row["update"] for row in matches]==list(range(6,27 if kind=="mid" else 26))
                for row in matches:assert row["state_sha256"]==control[row["update"]]["state_sha256"] and row["status"]=="EXACT_MATCH"
                final=root.path("cold-resume-v1/"+cold_name+".final");read_complete(final)
                identity,meta=persisted_hash(final);assert identity==matches[-1]["state_sha256"]==cold["final_state_sha256"]
                assert meta["optimizer_step"]==matches[-1]["update"]
            summaries[name]={"actual_updates_reconstructed":len(all_rows),"consumed_exposure":exposure,
                "timed_updates":100,"warmups":5,"sustained_seconds":report["sustained_elapsed_seconds"],
                "conservative_anchors_per_second":conservative,"native_labels_masks_padding_denominators_exact":True,
                "boundary_next20_exact":True,"mid_pending_plus_next20_exact":True,"persisted_state_hashes":states}
        a,b=paired[("B100",data,condition)],paired[("C101",data,condition)]
        common=min(len(a),len(b));assert common>=105 and a[:common]==b[:common]
        summaries[f"paired-{data}-{condition}"]={"nonempty_native_actual_update_prefix":common,
            "exact_shared_native_scientific_consumption":True,
            "total_bench_update_counts_may_differ":"fixed elapsed sustained benchmark; no total-equality claim"}
    report={"schema":"g2_independent_native_qualification_v1","status":"PASS_INDEPENDENT_G2_NATIVE_QUALIFICATION",
        "method":"stdlib integer selector, prefix/bisect cuts, label lengths, padding masks and NumPy persisted arrays; no G2 stream/trainer/save/load/hash helpers imported",
        "streams":summaries,"cold_paths":12,"before":before,"after":root.preflight(),
        "code_sha256":sha256(__file__),"elapsed_seconds":time.perf_counter()-started,"scientific_recipes_started":0}
    receipt.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n");return report


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--artifact-binding",required=True)
    parser.add_argument("--attempt",type=int,required=True);args=parser.parse_args()
    result=run(args.artifact_binding,args.attempt);print(json.dumps({"status":result["status"],"cold_paths":12}),flush=True)
