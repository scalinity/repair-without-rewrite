"""Independent completed ByT5 accounting/state reconstruction; CPU only."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import random
import time

from src.data.g2_artifacts import ArtifactRoot, read_complete, sha256


def run(binding, attempt):
    root = ArtifactRoot(binding)
    before = root.preflight()
    started = time.perf_counter()
    receipt = Path(f"experiments/manifests/generation_2/independent-byt5.attempt{attempt:02d}.json")
    if receipt.exists():
        raise FileExistsError(receipt)
    report_path = Path("experiments/manifests/generation_2/byt5-qualification.attempt01.json")
    report = json.loads(report_path.read_text())
    assert report["status"] == "PASS_G2_BYT5_RUNNER_100_UPDATES"
    source = root.path("asr-hypotheses-v1/construction.attempt01")
    read_complete(source)
    training = [row for row in (json.loads(line) for line in (source / "pairs.jsonl").open())
                if row["role"] == "train"]
    assert len(training) == len({row["id"] for row in training}) == 14113
    assert all(row["status"] == "COMPLETED" for row in training)
    assert all(len(row[field].encode()) + 1 <= 512 for row in training for field in ("source", "target"))
    # Independent finite index stream: no G2 batch/interface helpers imported.
    order = list(range(14113))
    random.Random(42).shuffle(order)
    presentations = [(i, i // 14113, i % 14113, training[order[i % 14113]])
                     for i in range(141130)]
    batches = [presentations[i:i + 4] for i in range(0, 141130, 4)]
    assert len(batches) == 35283 and len(batches[-1]) == 2
    assert all(len(batch) == 4 for batch in batches[:-1])
    assert Counter(row[3]["id"] for row in presentations) == {row["id"]: 10 for row in training}
    assert Counter(row[1] for row in presentations) == {i: 14113 for i in range(10)}
    plan = report["config"]["scientific_plan"]
    for key, expected in (("training_rows",14113),("passes",10),("presentations",141130),
                          ("optimizer_updates",35283),("batch_size",4),("final_batch_size",2)):
        assert plan[key] == expected
    assert plan["first_batch_ids"] == [row[3]["id"] for row in batches[0]]
    assert plan["last_batch_ids"] == [row[3]["id"] for row in batches[-1]]
    directory = root.path(report["output_relative"])
    read_complete(directory)
    steps = [json.loads(line) for line in (directory / "steps.jsonl").open()]
    assert len(steps) == 100
    for index, step in enumerate(steps):
        expected = batches[index]
        assert step["update"] == index + 1 and step["lr"] == 3e-4
        assert step["ids"] == [row[3]["id"] for row in expected]
        assert step["presentations"] == [dict(presentation=row[0], pass_index=row[1], pass_offset=row[2]) for row in expected]
        assert step["native_source"] == sum(len(row[3]["source"].encode()) + 1 for row in expected)
        assert step["native_targets"] == sum(len(row[3]["target"].encode()) + 1 for row in expected)
        assert all(math.isfinite(step[key]) for key in ("loss", "gradient_norm", "wall_seconds"))
        assert step["wall_seconds"] > 0
    mean = sum(row["wall_seconds"] for row in steps) / 100
    conservative = max(mean, sum(row["wall_seconds"] for row in steps[-25:]) / 25,
                       report["training_loop_seconds"] / 100)
    assert mean == report["mean_update_seconds"] and conservative == report["conservative_update_seconds"]
    freeze = json.loads(Path("experiments/manifests/generation_2/corpus-freeze.attempt01.json").read_text())
    panel_dir = root.path(freeze["panel_relative"])
    read_complete(panel_dir)
    panel = json.loads((panel_dir / "panel.json").read_text())
    for label in ("initial", "update100"):
        outputs = [json.loads(line) for line in (directory / f"evaluation-{label}.jsonl").open()]
        assert len(outputs) == 2984 and [row["id"] for row in outputs] == [row["id"] for row in panel]
        assert report["initial_evaluation" if label == "initial" else "final_evaluation"]["cases"] == 2984
        for row, item in zip(outputs, panel):
            if len(item["source"].encode()) + 1 > 512 or len(item["target"].encode()) + 1 > 512:
                assert row["decoded"]["reason"] == "retained_evaluation_capacity_overflow"
    # Load portable completed snapshots on CPU; no MPS/model/trainer is built.
    import torch
    snapshots = {}
    for label, key, count in (("initial","initial_checkpoint",0),("update100","final_checkpoint",100)):
        path = root.path(report[key]["relative"])
        read_complete(path)
        assert sha256(path / "state.pt") == report[key]["arrays_sha256"]
        state = torch.load(path / "state.pt", map_location="cpu", weights_only=True)
        assert state["schema"] == "g2_byt5_qualification_checkpoint_v1" and state["completed_updates"] == count
        assert state["config"] == report["config"] and state["corpus_freeze_sha256"] == report["corpus_freeze_sha256"]
        assert state["torch_cpu_rng"].dtype == state["mps_rng"].dtype == torch.uint8
        assert all(value.device.type == "cpu" and value.dtype == torch.float32
                   and bool(torch.isfinite(value).all()) for value in state["model"].values())
        for group in state["optimizer"]["param_groups"]:
            assert group["lr"] == 3e-4 and group["betas"] == (.9,.999)
            assert group["eps"] == 1e-8 and group["weight_decay"] == .01
        states = state["optimizer"]["state"]
        if count == 0:
            assert not states
        else:
            assert sum(item["exp_avg"].numel() for item in states.values()) == 299637760
            for item in states.values():
                assert float(item["step"]) == 100 and item["exp_avg"].shape == item["exp_avg_sq"].shape
                assert all(item[key].dtype == torch.float32 and bool(torch.isfinite(item[key]).all())
                           for key in ("exp_avg", "exp_avg_sq"))
        snapshots[label] = {"completed_updates":count,"portable_cpu_readback":True,"arrays_sha256":sha256(path / "state.pt")}
        del state
    result = dict(schema="g2_independent_byt5_v1",status="PASS_INDEPENDENT_G2_BYT5_ACCOUNTING_STATE",
        method="independent index arithmetic, UTF8-plus-EOS counts, JSON and portable CPU Torch state; no G2 batching, ByT5 interface or trainer helpers",
        official_weights_sha256=report["official_weight_sha256"],qualification_updates=100,
        scientific_presentations=141130,scientific_optimizer_updates=35283,final_batch_rows=2,
        all_training_source_target_capacities_pass=True,initial_final_panel_cases=2984,snapshots=snapshots,
        conservative_update_seconds=conservative,report_sha256=sha256(report_path),code_sha256=sha256(__file__),
        before=before,after=root.preflight(),elapsed_seconds=time.perf_counter()-started,
        scientific_recipes_started=0,external_model_review_claimed=False)
    receipt.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-binding",required=True)
    parser.add_argument("--attempt",type=int,required=True)
    args = parser.parse_args()
    result = run(args.artifact_binding,args.attempt)
    print(json.dumps({"status":result["status"],"elapsed_seconds":result["elapsed_seconds"]}),flush=True)
