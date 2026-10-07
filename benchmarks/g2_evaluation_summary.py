"""Failure-inclusive expanded-panel tables and descriptive paired intervals."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import time

from src.data.g2_artifacts import ArtifactRoot, read_complete, sha256


def run(binding, attempt):
    root = ArtifactRoot(binding)
    before = root.preflight()
    started = time.perf_counter()
    output = Path(f"experiments/manifests/generation_2/expanded-evaluation-summary.attempt{attempt:02d}.json")
    if output.exists():
        raise FileExistsError(output)
    freeze = json.loads(Path("experiments/manifests/generation_2/corpus-freeze.attempt01.json").read_text())
    panel_dir = root.path(freeze["panel_relative"])
    read_complete(panel_dir)
    panel = json.loads((panel_dir / "panel.json").read_text())
    mapping = {row["id"]: row for row in panel}
    assert len(mapping) == 2984
    natural = {row["id"] for row in panel if row["population"] == "natural"}
    groups = {mapping[name]["source_group_id"] for name in natural}
    assert len(natural) == 2696 and len(groups) == 52
    inputs = []
    for arm in ("B100", "C101"):
        inputs.append((f"archived-G1-{arm}-3e-4-endpoint",f"evaluation-v1/archived-{arm}-3e-4-endpoint.attempt01","archived-endpoint"))
    for data, condition in (("D0","U8"),("D1","U1"),("D1","U8")):
        for arm in ("B100","C101"):
            for label in ("initial","final"):
                inputs.append((f"BENCH-{arm}-{data}-{condition}-{label}",f"bench-v1/{arm}-{data}-{condition}.attempt01",label))
    for label in ("initial","update100"):
        inputs.append(("ByT5-qualification-"+label,"byt5-v1/qualification.attempt01",label))
    from src.scoring.records import aggregate
    from src.scoring.g2_bootstrap import paired_group_intervals
    tables = {}
    metrics = {key:{} for key in ("WER","completed_repair_lower","completed_repair_upper","introduced_lower","introduced_upper")}
    raw = None
    for name, relative, label in inputs:
        directory = root.path(relative)
        read_complete(directory)
        path = directory / f"evaluation-{label}.jsonl"
        records = [json.loads(line) for line in path.open()]
        assert len(records) == 2984 and {row["id"] for row in records} == set(mapping)
        subsets = {"natural_all":[],"legacy108":[],"new2588":[],"calibration":[],"hpo_development":[],
            "train-clean-100":[],"train-clean-360":[],"train-other-500":[],
            "dev-clean":[],"dev-other":[],"natural-clean":[],"natural-other":[],"generated/clean_preservation":[],
            "generated/mixed_repair_preservation":[],"generated/uniquely_recoverable_repair":[]}
        by_group = defaultdict(list)
        source = {}
        for row in records:
            item = mapping[row["id"]]
            if row["id"] in natural:
                subsets["natural_all"].append(row)
                subsets["legacy108" if item["legacy_subset"] else "new2588"].append(row)
                subsets[item["role"]].append(row)
                subsets[item["official_split"]].append(row)
                subsets["natural-other" if "other" in item["official_split"] else "natural-clean"].append(row)
                by_group[item["source_group_id"]].append(row["score"])
                source[row["id"]] = (row["score"]["eS"],row["score"]["reference_words"])
            else:
                subsets["generated/"+item["view"]].append(row)
        assert all(subsets.values()) and set(by_group) == groups
        if raw is None:
            raw = source
        assert source == raw
        tables[name] = dict(records_sha256=sha256(path),cases=2984,
            subsets={key:dict(cases=len(rows),status_counts=dict(Counter(row["status"] for row in rows)),
                aggregate=aggregate(row["score"] for row in rows)) for key,rows in subsets.items()},
            failure_records_retained=True,quality_selection_performed=False)
        for key, field, index, denominator in (("WER","eO",None,"reference_words"),
            ("completed_repair_lower","completed_repair",0,"eS"),
            ("completed_repair_upper","completed_repair",1,"eS"),
            ("introduced_lower","introduced",0,"reference_words"),
            ("introduced_upper","introduced",1,"reference_words")):
            metrics[key][name] = {group:(sum(row[field] if index is None else row[field][index] for row in rows),
                sum(row[denominator] for row in rows)) for group,rows in by_group.items()}
    metrics["WER"]["RAW"] = {group:(sum(raw[name][0] for name in natural if mapping[name]["source_group_id"]==group),
        sum(raw[name][1] for name in natural if mapping[name]["source_group_id"]==group)) for group in groups}
    bootstrap = {key:paired_group_intervals(groups,values) for key,values in metrics.items()}
    hashes = {row["draw_indices_int64_sha256"] for row in bootstrap.values()}
    assert len(hashes) == 1
    result = dict(schema="g2_expanded_qualification_evaluation_v1",status="PASS_COMPLETE_FAILURE_INCLUSIVE_QUALIFICATION_TABLES",
        tables=tables,paired_source_group_bootstrap=bootstrap,
        bootstrap_scope="full natural DEVELOPMENT only; 52 groups, 10000 shared PCG64 seed42 draws; descriptive, not training-seed uncertainty or H1 evidence",
        alignment_bounds_reported_separately=True,qualification_quality_selection_performed=False,
        scientific_initializers_selected=False,scientific_recipes_started=0,
        panel_sha256=sha256(panel_dir/"panel.json"),before=before,after=root.preflight(),
        code_sha256=sha256(__file__),elapsed_seconds=time.perf_counter()-started)
    output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-binding",required=True)
    parser.add_argument("--attempt",type=int,required=True)
    args = parser.parse_args()
    result = run(args.artifact_binding,args.attempt)
    print(json.dumps({"status":result["status"],"panels":len(result["tables"])}),flush=True)
