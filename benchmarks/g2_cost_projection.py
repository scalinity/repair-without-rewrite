"""Artifact-derived seven-recipe forecast, with exactly one 25% reserve."""
import argparse
import json
import math
from pathlib import Path
import time

from src.data.g2_artifacts import ArtifactRoot,sha256


def load(name):
    path=Path("experiments/manifests/generation_2")/name
    return json.loads(path.read_text()),sha256(path)


def reserve_and_gate(subtotal):
    if not math.isfinite(subtotal) or subtotal < 0:
        raise ValueError("finite nonnegative serialized time required")
    reserve=.25*subtotal
    total=subtotal+reserve
    return reserve,total,"PASS_G2_COST_CEILING_ONLY" if total<=96*3600 else "GENERATION_2_COST_BLOCKED"


def run(binding,attempt):
    root=ArtifactRoot(binding);before=root.preflight();started=time.perf_counter()
    path=Path(f"experiments/manifests/generation_2/cost-projection.attempt{attempt:02d}.json")
    if path.exists():raise FileExistsError(path)
    freeze,freeze_sha=load("corpus-freeze.attempt01.json");lines=[];inputs={"corpus-freeze.attempt01.json":freeze_sha}
    qualification=0.;scientific=0.
    for data,condition in (("D0","U8"),("D1","U1"),("D1","U8")):
        for arm in ("B100","C101"):
            name=f"{arm}-{data}-{condition}.attempt01"
            bench,identity=load("bench-"+name+".json");inputs["bench-"+name+".json"]=identity
            if bench["status"]!="PASS_G2_NATIVE_BENCH_COLD_PENDING":raise ValueError("complete native BENCH required for every cell")
            elapsed=bench["elapsed_seconds"];qualification+=elapsed
            exposure=freeze["conditions"][data]["actual_exposure"]
            train_seconds=exposure/bench["conservative_anchors_per_second"]
            panel=max(bench["initial_evaluation"]["complete_panel_wall_seconds"],bench["final_evaluation"]["complete_panel_wall_seconds"])
            diagnostic=max(bench["initial_diagnostic_greedy"]["complete_panel_wall_seconds"],bench["final_diagnostic_greedy"]["complete_panel_wall_seconds"])
            forced=max(bench["initial_diagnostic_forced"]["seconds"],bench["final_diagnostic_forced"]["seconds"])
            config,config_sha=load(f"recipe-G2-{arm}-{data}-{condition}-seed42-lr3e-4.attempt01.json")
            inputs[f"recipe-G2-{arm}-{data}-{condition}-seed42-lr3e-4.attempt01.json"]=config_sha
            saves=len({item["master_completed"] for item in config["save_endpoints"]})
            save_seconds=max(bench["checkpoint_save_seconds"].values())*saves
            future=train_seconds+6*panel+2*diagnostic+2*forced+save_seconds+bench["startup_seconds"]
            scientific+=future
            lines.append({"recipe_id":config["recipe_id"],"classification":"CALCULATED_FROM_MEASURED_QUALIFICATION",
                "training_seconds":train_seconds,"evaluation_seconds":6*panel,"diagnostic_greedy_seconds":2*diagnostic,
                "diagnostic_forced_seconds":2*forced,"save_seconds":save_seconds,"save_count":saves,
                "startup_seconds":bench["startup_seconds"],"total_future_seconds":future,
                "conservative_anchors_per_second":bench["conservative_anchors_per_second"],"actual_exposure":exposure,
                "forecast_assumption":"use larger complete initialization/endpoint panel cost at all six future endpoints; no quality-based speed reduction"})
            for kind in ("boundary","mid"):
                name_cold=f"cold-{name}.{kind}.json";cold,identity=load(name_cold);inputs[name_cold]=identity
                if cold["status"]!="PASS_EXACT_G2_COLD_RESUME":raise ValueError("every cold qualification cost and status required")
                qualification+=cold["elapsed_seconds"]
    byt5,identity=load("byt5-qualification.attempt01.json");inputs["byt5-qualification.attempt01.json"]=identity
    if byt5["status"]!="PASS_G2_BYT5_RUNNER_100_UPDATES":raise ValueError("native ByT5 runner qualification required")
    qualification+=byt5["elapsed_seconds"]
    by_train=35283*byt5["conservative_update_seconds"]
    by_panel=max(byt5["initial_evaluation"]["complete_panel_wall_seconds"],byt5["final_evaluation"]["complete_panel_wall_seconds"])
    by_save=max(byt5["initial_checkpoint"]["seconds"],byt5["final_checkpoint"]["seconds"])*4
    by_future=by_train+4*by_panel+by_save+byt5["startup_seconds"];scientific+=by_future
    lines.append({"recipe_id":"G2-ByT5-D1-10pass-seed42-lr3e-4","classification":"CALCULATED_FROM_MEASURED_QUALIFICATION",
        "training_seconds":by_train,"evaluation_seconds":4*by_panel,"save_seconds":by_save,"save_count":4,
        "startup_seconds":byt5["startup_seconds"],"total_future_seconds":by_future,
        "conservative_update_seconds":byt5["conservative_update_seconds"],"optimizer_updates":35283,
        "forecast_assumption":"charge final short batch at full-batch conservative rate; charge larger complete panel at all four endpoints"})
    shared=[]
    for name in ("source-archives.attempt01.json","audio-train-clean-100.attempt02.json","audio-train-clean-360.attempt03.json",
            "audio-train-other-500.attempt01.json","audio-dev-clean.attempt01.json","audio-dev-other.attempt01.json",
            "parakeet-sources.attempt01.json","corpus-freeze.attempt01.json","compatibility-B100.attempt02.json",
            "compatibility-C101.attempt01.json","compatibility-C101.attempt02.json","archived-evaluation-B100.attempt01.json",
            "archived-evaluation-C101.attempt01.json","independent-archives.attempt01.json",
            "independent-corpus.attempt01.json","independent-native.attempt01.json",
            "independent-byt5.attempt01.json","storage-reforecast.attempt01.json",
            "expanded-evaluation-summary.attempt01.json","independent-evaluation.attempt01.json"):
        record,identity=load(name);inputs[name]=identity
        seconds=record["elapsed_seconds"];qualification+=seconds
        shared.append({"receipt":name,"classification":"MEASURED","seconds":seconds})
    name="independent-compatibility.attempt02.json"
    record,identity=load(name);inputs[name]=identity
    qualification+=record["seconds"]
    shared.append({"receipt":name,"classification":"MEASURED","seconds":record["seconds"],"elapsed_field":"seconds"})
    # Failed pre-model commands without dedicated wall timers are retained and
    # shown explicitly. Their planning allowance is not presented as a measurement.
    failures=("audio-train-clean-100.attempt01.json","audio-train-clean-360.attempt01.json",
              "audio-train-clean-360.attempt02.json","compatibility-B100.attempt01.json")
    untimed_storage=("external-root.attempt01.json","artifact-root-io.attempt02.json",
                     "independent-storage.attempt01.json","independent-root-loss.attempt01.json")
    assumed=60*(len(failures)+len(untimed_storage))
    for name in (*failures,*untimed_storage):
        record,identity=load(name);inputs[name]=identity
        shared.append({"receipt":name,"classification":"ASSUMED","seconds":60,
            "measured_seconds":None,"reason":"retained pre-model failure or bounded storage check without a dedicated total timer; conservative one-minute planning allowance"})
    startup,startup_sha=load("source-startup-creation-gap.attempt01.json")
    inputs["source-startup-creation-gap.attempt01.json"]=startup_sha
    shared.append({"receipt":"source-startup-creation-gap.attempt01.json","classification":startup["classification"],"seconds":startup["seconds"]})
    subtotal=qualification+scientific+assumed+startup["seconds"]
    reserve,total,status=reserve_and_gate(subtotal)
    report={"schema":"g2_cost_projection_v1","status":status,"scope":"cost gate only; independent admission still required",
        "inputs_sha256":inputs,"recipes":lines,"shared_measured_and_assumed":shared,
        "measured_qualification_and_shared_seconds":qualification,"calculated_future_recipe_seconds":scientific,
        "assumed_mechanical_failure_seconds":assumed,"subtotal_seconds":subtotal,"reserve_fraction":.25,
        "calculated_source_startup_creation_gap_seconds":startup["seconds"],
        "single_reserve_seconds":reserve,"total_serialized_seconds":total,"total_serialized_hours":total/3600,
        "ceiling_hours":96,"within_ceiling":total<=96*3600,
        "unpriced":["researcher/implementation time and engineering unit/full-suite tests","electricity","unrelated host activity","final campaign or paper completion"],
        "before":before,"after":root.preflight(),"code_sha256":sha256(__file__),
        "projection_execution_seconds":time.perf_counter()-started,"scientific_recipes_started":0}
    path.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n");return report


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--artifact-binding",required=True)
    parser.add_argument("--attempt",type=int,required=True);args=parser.parse_args()
    result=run(args.artifact_binding,args.attempt);print(json.dumps({"status":result["status"],"hours":result["total_serialized_hours"]}),flush=True)
