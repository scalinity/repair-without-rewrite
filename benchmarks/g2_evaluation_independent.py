"""Independent group-count bootstrap and complete evaluation table arithmetic."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import time

from src.data.g2_artifacts import ArtifactRoot, read_complete, sha256


def run(binding, attempt):
    root = ArtifactRoot(binding)
    before = root.preflight()
    started = time.perf_counter()
    output = Path(f"experiments/manifests/generation_2/independent-evaluation.attempt{attempt:02d}.json")
    if output.exists():
        raise FileExistsError(output)
    path = Path("experiments/manifests/generation_2/expanded-evaluation-summary.attempt01.json")
    report = json.loads(path.read_text())
    assert report["status"] == "PASS_COMPLETE_FAILURE_INCLUSIVE_QUALIFICATION_TABLES"
    freeze = json.loads(Path("experiments/manifests/generation_2/corpus-freeze.attempt01.json").read_text())
    panel_path = root.path(freeze["panel_relative"])
    read_complete(panel_path)
    panel = json.loads((panel_path / "panel.json").read_text())
    lookup = {row["id"]:row for row in panel}
    groups = sorted({row["source_group_id"] for row in panel if row["population"] == "natural"})
    assert len(groups) == 52 and len(lookup) == 2984
    assert len([row for row in panel if row["population"] == "natural"]) == 2696
    assert report["panel_sha256"] == sha256(panel_path / "panel.json")
    expected_files = {}
    for arm in ("B100", "C101"):
        expected_files[f"archived-G1-{arm}-3e-4-endpoint"] = (
            f"evaluation-v1/archived-{arm}-3e-4-endpoint.attempt01", "archived-endpoint")
        for data, condition in (("D0", "U8"), ("D1", "U1"), ("D1", "U8")):
            for checkpoint in ("initial", "final"):
                expected_files[f"BENCH-{arm}-{data}-{condition}-{checkpoint}"] = (
                    f"bench-v1/{arm}-{data}-{condition}.attempt01", checkpoint)
    for checkpoint in ("initial", "update100"):
        expected_files["ByT5-qualification-" + checkpoint] = (
            "byt5-v1/qualification.attempt01", checkpoint)
    assert len(expected_files) == 16 and set(report["tables"]) == set(expected_files)
    by_metric = {key:{} for key in report["paired_source_group_bootstrap"]}
    raw = None
    for label, table in report["tables"].items():
        relative, checkpoint = expected_files[label]
        directory = root.path(relative)
        read_complete(directory)
        file = directory / f"evaluation-{checkpoint}.jsonl"
        assert sha256(file) == table["records_sha256"]
        assert table["cases"] == 2984 and table["failure_records_retained"] is True
        assert table["quality_selection_performed"] is False
        records = [json.loads(line) for line in file.open()]
        assert len(records) == len({row["id"] for row in records}) == 2984
        assert {row["id"] for row in records} == set(lookup)
        group_totals = defaultdict(lambda: [0]*7)
        baseline = {}
        subsets = defaultdict(list)
        for row in records:
            item = lookup[row["id"]]
            if item["population"] == "natural":
                names = ("natural_all","legacy108" if item["legacy_subset"] else "new2588",
                    item["role"],item["official_split"],"natural-other" if "other" in item["official_split"] else "natural-clean")
                score = row["score"]
                values = [score["eO"],score["reference_words"],score["eS"],
                    *score["completed_repair"],*score["introduced"]]
                totals = group_totals[item["source_group_id"]]
                for index,value in enumerate(values):totals[index] += value
                baseline[row["id"]] = (score["eS"],score["reference_words"])
            else:
                names = ("generated/"+item["view"],)
            for name in names:subsets[name].append(row)
        assert set(subsets) == set(table["subsets"])
        for name, rows in subsets.items():
            expected = table["subsets"][name]
            assert expected["cases"] == len(rows) and expected["status_counts"] == dict(Counter(row["status"] for row in rows))
            observed = expected["aggregate"]
            assert observed["reference_words"] == sum(row["score"]["reference_words"] for row in rows)
            assert observed["source_errors"] == sum(row["score"]["eS"] for row in rows)
            assert observed["output_errors"] == sum(row["score"]["eO"] for row in rows)
            assert observed["invalid_or_incomplete"] == sum(not row["score"]["complete_valid"] for row in rows)
            for field in ("repair","introduced","completed_repair"):
                assert observed[field] == [sum(row["score"][field][i] for row in rows) for i in (0,1)]
        if raw is None:raw = baseline
        assert baseline == raw and set(group_totals) == set(groups)
        for name, numerator, denominator in (("WER",0,1),("completed_repair_lower",3,2),
            ("completed_repair_upper",4,2),("introduced_lower",5,1),("introduced_upper",6,1)):
            by_metric[name][label] = [ (group_totals[group][numerator],group_totals[group][denominator]) for group in groups ]
    by_metric["WER"]["RAW"] = [(sum(value[0] for name,value in raw.items() if lookup[name]["source_group_id"]==group),
        sum(value[1] for name,value in raw.items() if lookup[name]["source_group_id"]==group)) for group in groups]
    import numpy as np
    draws = np.random.Generator(np.random.PCG64(42)).integers(0,52,size=(10000,52))
    # Different arithmetic path: count each draw's group multiplicities, then
    # multiply integer group totals instead of indexed floating-point sums.
    multiplicities = np.stack([np.bincount(draw,minlength=52) for draw in draws])
    assert (multiplicities.sum(axis=1)==52).all()
    digest = hashlib.sha256(draws.astype("<i8").tobytes()).hexdigest()
    for metric, values in by_metric.items():
        expected = report["paired_source_group_bootstrap"][metric]
        assert expected["group_order"] == groups and expected["draw_indices_int64_sha256"] == digest
        samples = {}
        for label, pairs in values.items():
            totals = multiplicities @ np.asarray(pairs,dtype=np.int64)
            assert (totals[:,1]>0).all()
            samples[label] = totals[:,0] / totals[:,1]
            assert np.percentile(samples[label],[2.5,97.5]).tolist() == expected["intervals"][label]
        contrasts=expected["paired_difference_intervals"]
        assert len(contrasts)==len(samples)*(len(samples)-1)//2
        pairs=set()
        for contrast,interval in contrasts.items():
            a,b=contrast.split(" minus ")
            assert a in samples and b in samples and a!=b
            pairs.add(frozenset((a,b)))
            assert np.percentile(samples[a]-samples[b],[2.5,97.5]).tolist()==interval
        assert len(pairs)==len(contrasts)
    result = dict(schema="g2_independent_evaluation_v1",status="PASS_INDEPENDENT_G2_TABLE_BOOTSTRAP_RECONSTRUCTION",
        method="separate JSON membership/status/integer bounds arithmetic and integer multiplicity matrix products; no aggregate or bootstrap producer imported",
        complete_panels=len(report["tables"]),cases_per_panel=2984,natural_groups=52,draws=10000,
        all_shared_draw_intervals_exact=True,draw_indices_int64_sha256=digest,
        summary_sha256=sha256(path),before=before,after=root.preflight(),code_sha256=sha256(__file__),
        elapsed_seconds=time.perf_counter()-started,scientific_recipes_started=0)
    output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-binding",required=True)
    parser.add_argument("--attempt",type=int,required=True)
    args = parser.parse_args()
    result = run(args.artifact_binding,args.attempt)
    print(json.dumps({"status":result["status"],"panels":result["complete_panels"]}),flush=True)
