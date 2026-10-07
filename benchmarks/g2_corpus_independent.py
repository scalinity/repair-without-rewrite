"""Independent artifact reconstruction; no G2 construction/geometry helper imports."""
import argparse
import bisect
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import time

from src.data.g2_artifacts import ArtifactRoot, read_complete, sha256


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()


def records(path):
    return [json.loads(line) for line in Path(path).open()]


def run(binding,attempt):
    root=ArtifactRoot(binding);before=root.preflight();started=time.perf_counter()
    receipt=Path(f"experiments/manifests/generation_2/independent-corpus.attempt{attempt:02d}.json")
    if receipt.exists():raise FileExistsError(receipt)
    freeze_path=Path("experiments/manifests/generation_2/corpus-freeze.attempt01.json")
    freeze=json.loads(freeze_path.read_text())
    assert freeze["status"]=="PASS_COMPLETE_G2_CORPUS_PANEL_GEOMETRY_FREEZE"
    source=root.path("asr-hypotheses-v1/construction.attempt01");read_complete(source)
    pairs=records(source/"pairs.jsonl");by_id={row["id"]:row for row in pairs}
    assert len(by_id)==16809 and Counter(row["role"] for row in pairs)=={"train":14113,"calibration":1900,"hpo_development":796}
    for row in pairs:
        assert row["status"]=="COMPLETED"
        assert hashlib.sha256(row["source"].encode()).hexdigest()==row["source_sha256"]
        assert hashlib.sha256(row["target"].encode()).hexdigest()==row["text_raw_sha256"]
    old_pairs=records("exports/foundation-repair/development-asr-pairs-attempt01/pairs.jsonl")
    old_panel=json.loads(Path("exports/lexical-reader-v2/pilot-preparation-attempt01/development-panel.json").read_text())
    legacy=[row for row in old_pairs if row["role"]=="train"]+[row for row in old_panel if row["population"]=="natural"]
    assert len(legacy)==1132
    for row in legacy:
        actual=by_id[row["id"]]
        assert (row["source"],row["target"],row["source_group_id"])==(actual["source"],actual["target"],actual["source_group_id"])
    calls=records(source/"calls.jsonl");assert len(calls)==31482
    unique,replay={},[]
    for intent,result in zip(calls[::2],calls[1::2]):
        assert intent["event"]=="START" and result["event"]=="RESULT" and intent["request"]==result["request"]
        assert result["status"]=="COMPLETED"
        if result["request"]["kind"]=="unique":unique[result["request"]["id"]]=result
        else:replay.append(result)
    assert len(unique)==15677 and len(replay)==64
    expected_replay=[]
    for population in ("TRAIN","DEVELOPMENT"):
        eligible=[row for row in pairs if not row["legacy_reused"] and (row["role"]=="train")== (population=="TRAIN")]
        expected_replay.extend(row["id"] for row in sorted(eligible,key=lambda r:digest(["G2",42,"PARAKEET_REPLAY",population,r["id"]]))[:32])
    assert [row["request"]["id"] for row in replay]==expected_replay
    assert all(row["source"].encode()==unique[row["request"]["id"]]["source"].encode() for row in replay)
    groups,families=defaultdict(set),defaultdict(set)
    for row in pairs:
        groups[row["role"]].add(row["source_group_id"]);families[row["role"]].update(row["families"].items())
    for a,b in (("train","calibration"),("train","hpo_development"),("calibration","hpo_development")):
        assert not groups[a]&groups[b] and not families[a]&families[b]
    assert len(groups["calibration"]|groups["hpo_development"])==52
    panel_path=root.path(freeze["panel_relative"]);read_complete(panel_path)
    panel=json.loads((panel_path/"panel.json").read_text());assert len(panel)==2984
    natural=[row for row in panel if row["population"]=="natural"]
    assert {row["id"] for row in natural}=={row["id"] for row in pairs if row["role"]!="train"}
    assert [row for row in panel if row["population"]=="generated"]==[row for row in old_panel if row["population"]=="generated"]
    from src.scoring.text import lexical
    error=[row for row in natural if lexical(row["source"])!=lexical(row["target"])]
    support={"cases":2696,"lexical_error_cases":len(error),"lexical_error_groups":len({row["source_group_id"] for row in error}),
        "lexical_zero_cases":2696-len(error),"pass":len(error)>=200 and len({row["source_group_id"] for row in error})>=20 and 2696-len(error)>=200}
    assert support==freeze["development_support"] and support["pass"]
    generated=records("exports/lexical-reader-v2/generated-pool-attempt02/accepted.jsonl")
    result={}
    for data in ("D0","D1"):
        path=root.path(freeze["conditions"][data]["artifact_relative"]);read_complete(path)
        natural_rows=records(path/"natural.jsonl");lookup={row["variant_id"]:row for row in [*generated,*natural_rows]}
        ledger=records(path/"presentations.jsonl");masters=json.loads((path/"masters.json").read_text())
        actual=json.loads((path/"actual-updates.json").read_text())
        assert len(masters)==len(actual["U1"]) and len(actual["U8"])==8*len(masters)
        cursor=0
        for ordinal,presentation in enumerate(ledger):
            row=lookup[presentation["variant_id"]]
            charge=len(row["canonical_sequence"])
            assert charge==len(row["target_ids"])+row["anchor_bpe"]+5==presentation["canonical_charge"]
            assert (presentation["ordinal"],presentation["start_exposure"],presentation["end_exposure"])==(ordinal,cursor,cursor+charge)
            assert presentation["phase"]==("P0" if cursor<6666667 else "P1" if cursor<9333334 else "P2")
            cursor+=charge
        for condition in ("U1","U8"):
            actual_clock=0;step=0
            for master_index,master in enumerate(masters):
                queue=ledger[master["first_ordinal"]:master["last_ordinal"]+1]
                cumulative=[];total=0
                for item in queue:total+=item["canonical_charge"];cumulative.append(total)
                assert total>=32768 and total-queue[-1]["canonical_charge"]<32768
                cuts=[] if condition=="U1" else [bisect.bisect_left([8*c for c in cumulative],j*total)+1 for j in range(1,8)]
                bounds=[0,*cuts,len(queue)];assert all(a<b for a,b in zip(bounds,bounds[1:]))
                for sub,(a,b) in enumerate(zip(bounds,bounds[1:])):
                    part=queue[a:b];observed=actual[condition][step];charge=sum(item["canonical_charge"] for item in part);actual_clock+=charge
                    den={"B":sum(len(lookup[item["variant_id"]]["target_ids"])+1 for item in part),
                        "C":{name:sum(len(lookup[item["variant_id"]]["gold_labels"][name]) for item in part)
                              for name in ("action","start","end","vocabulary")}}
                    lr=3e-4*actual_clock/200000 if actual_clock<=200000 else 3e-4*(.1+.45*(1+math.cos(math.pi*(min(actual_clock,10000000)-200000)/9800000)))
                    assert (observed["master_index"],observed["subqueue_index"],observed["optimizer_step_index"])==(master_index,sub,step+1)
                    assert (observed["first_ordinal"],observed["last_ordinal"],observed["examples"])==(part[0]["ordinal"],part[-1]["ordinal"],len(part))
                    assert observed["canonical_charge"]==charge and observed["completed_actual_exposure"]==actual_clock and observed["denominators"]==den
                    assert observed["lr"]==lr
                    for arm,size in (("B100",16),("C101",4)):
                        partitions=observed["microbatch_partitions"][arm]
                        flattened=[i for start,stop in partitions for i in range(start,stop)]
                        assert flattened==list(range(len(part))) and all(0<stop-start<=size for start,stop in partitions)
                    step+=1
            assert actual_clock==cursor
        if data=="D0":
            original=Path("exports/lexical-reader-v2/mixed-reader-attempt02/presentations.jsonl")
            assert sha256(path/"presentations.jsonl")==sha256(original)
            assert (len(masters),cursor,len(ledger)-1)==(305,10007223,134590)
        result[data]={"masters":len(masters),"U8_updates":8*len(masters),"actual_exposure":cursor,
            "ledger_sha256":sha256(path/"presentations.jsonl"),"all_cuts_denominators_microbatches_lr_exact":True}
    report={"schema":"g2_independent_corpus_geometry_v1","status":"PASS_INDEPENDENT_G2_CORPUS_GEOMETRY",
        "path":"stdlib JSON/hash/counts/bisect and label-list lengths; no G2 construction, cut, denominator or LR helpers imported",
        "census_rows":16809,"unique_calls":15677,"exact_replays":64,"legacy_sources_exact":1132,
        "support":support,"conditions":result,"before":before,"after":root.preflight(),
        "code_sha256":sha256(__file__),"freeze_sha256":sha256(freeze_path),"elapsed_seconds":time.perf_counter()-started,
        "scientific_recipes_started":0}
    receipt.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n");return report


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--artifact-binding",required=True)
    parser.add_argument("--attempt",type=int,required=True);args=parser.parse_args()
    result=run(args.artifact_binding,args.attempt);print(json.dumps({"status":result["status"],"conditions":result["conditions"]}),flush=True)
