"""New expanded-panel evaluation of the two immutable G1 3e-4 endpoints."""
import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import time

from src.data.g2_artifacts import ArtifactRoot, atomic_artifact, offline_model_environment, read_complete, sha256


def run(binding,arm,attempt):
    root=ArtifactRoot(binding);before=root.preflight();started=time.perf_counter();offline_model_environment()
    if arm not in {"B100","C101"} or attempt<1:raise ValueError("fixed historical arm and numbered attempt required")
    for control_arm in ("B100","C101"):
        control=json.loads(Path(f"experiments/manifests/generation_2/compatibility-{control_arm}.attempt02.json").read_text())
        if control["status"]!="PASS_EXACT_HISTORICAL_COMPATIBILITY":raise ValueError("exact historical compatibility required")
    receipt=Path(f"experiments/manifests/generation_2/archived-evaluation-{arm}.attempt{attempt:02d}.json")
    if receipt.exists():raise FileExistsError(receipt)
    from benchmarks.g2_native_qualification import frozen
    rows,ledger,updates,panel,diagnostics,g2_ids=frozen(root,"D0")
    campaign_path=Path("experiments/manifests/six_10m_probes/campaign-freeze.attempt01.json")
    campaign=json.loads(campaign_path.read_text())
    if any(sha256(path)!=expected for path,expected in campaign["source_hashes"].items()):
        raise ValueError("archived G1 source implementation changed")
    recipe=next(row for row in campaign["recipes"] if row["recipe_id"]==arm+"-seed42-lr3e-04")
    checkpoint=Path("exports/six-10m-probes")/recipe["recipe_id"]/"attempt01/checkpoint-update305"
    meta=json.loads((checkpoint/"metadata.json").read_text())
    expected=json.loads((checkpoint/"COMPLETE.json").read_text())
    if any(sha256(checkpoint/name)!=value for name,value in expected.items()):raise ValueError("archived endpoint bytes changed")
    report={"schema":"g2_archived_endpoint_evaluation_v1","attempt":attempt,"arm":arm,"seed":42,
        "code_commit":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
        "captured_dirty_status":subprocess.check_output(["git","status","--porcelain"],text=True),
        "code_sha256":sha256(__file__),"checkpoint_relative":str(checkpoint),"checkpoint_files":expected,
        "panel_sha256":g2_ids["panel"],"before":before,"scientific_recipes_started":0,"status":"RUNNING",
        "output_relative":f"evaluation-v1/archived-{arm}-3e-4-endpoint.attempt{attempt:02d}",
        "resume_policy":"immutable original checkpoint loaded read-only; no G1 result mutation or extra training"}
    try:
        with atomic_artifact(root,report["output_relative"]) as out:
            (out/"start.json").write_text(json.dumps(report,sort_keys=True)+"\n")
            from benchmarks.six_10m_campaign import trainer_for
            from src.models.paired_training_v3 import load_paired_checkpoint
            from benchmarks.paired_qualification_v3 import evaluation_timing
            from src.scoring.records import aggregate
            trainer=trainer_for(arm,3e-4,meta["identities"])
            tick=time.perf_counter();load_paired_checkpoint(trainer,checkpoint,rows)
            report["load_seconds"]=time.perf_counter()-tick
            if (trainer.optimizer.step,trainer.committed_exposure)!=(305,10007223):raise ValueError("wrong archived endpoint clock")
            report["evaluation"]=evaluation_timing(trainer,panel,out,"archived-endpoint")
            outputs=[json.loads(line) for line in (out/"evaluation-archived-endpoint.jsonl").open()]
            mapping={row["id"]:row for row in panel}
            subsets={"natural_all":[row for row in outputs if row["population"]=="natural"],
                "legacy108":[row for row in outputs if mapping[row["id"]].get("legacy_subset",False)],
                "new2588":[row for row in outputs if row["population"]=="natural" and not mapping[row["id"]].get("legacy_subset",False)]}
            for role in ("calibration","hpo_development"):
                subsets[role]=[row for row in outputs if mapping[row["id"]].get("role")==role]
            for split in ("train-clean-100","train-clean-360","train-other-500","dev-clean","dev-other"):
                subsets[split]=[row for row in outputs if mapping[row["id"]].get("official_split")==split]
            for label,is_other in (("natural-clean",False),("natural-other",True)):
                subsets[label]=[row for row in outputs if row["population"]=="natural"
                    and ("other" in mapping[row["id"]]["official_split"])==is_other]
            for label,view in (("clean","clean_preservation"),("mixed","mixed_repair_preservation"),
                               ("required","uniquely_recoverable_repair")):
                subsets["generated/"+label]=[row for row in outputs if row["population"]=="generated" and mapping[row["id"]]["view"]==view]
            if any(not items for items in subsets.values()):raise ValueError("required expanded evaluation subset is empty")
            report["subsets"]={name:{"cases":len(items),"aggregate":aggregate(row["score"] for row in items),
                "status_counts":dict(Counter(row["status"] for row in items))} for name,items in subsets.items()}
            report.update(status="PASS_G2_EXPANDED_ARCHIVED_ENDPOINT_EVALUATION",native_updates_performed=0)
            (out/"summary.json").write_text(json.dumps(report,sort_keys=True)+"\n")
        report["after"]=root.preflight()
    except BaseException as error:
        report.update(status="FAILED_QUALIFICATION_REPAIR_REQUIRED",error_type=type(error).__name__);raise
    finally:
        report["elapsed_seconds"]=time.perf_counter()-started
        report["evaluation"]={k:v for k,v in report.get("evaluation",{}).items() if k!="per_case"}
        receipt.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    return report


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--artifact-binding",required=True)
    parser.add_argument("--arm",required=True);parser.add_argument("--attempt",type=int,required=True);args=parser.parse_args()
    result=run(args.artifact_binding,args.arm,args.attempt);print(json.dumps({"status":result["status"],"elapsed_seconds":result["elapsed_seconds"]}),flush=True)
