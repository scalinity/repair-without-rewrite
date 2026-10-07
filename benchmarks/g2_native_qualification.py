"""Six fixed BENCH streams and twelve fresh-process replays; no recipe launcher."""
import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import time

from src.data.g2_artifacts import ArtifactRoot, atomic_artifact, offline_model_environment, read_complete, sha256

FIELDS = ("arm", "update", "canonical_charge", "committed_canonical_exposure", "lr", "loss",
          "gradient_norm", "microsteps", "examples", "denominators", "presentation_ids", "actual_consumption",
          "data_condition", "update_condition", "master_queue_index", "subqueue_index",
          "legacy_32768_charge_difference", "master_overshoot")
CONFIGURATIONS = tuple((arm, data, update) for data, update in (("D0", "U8"), ("D1", "U1"), ("D1", "U8"))
                       for arm in ("B100", "C101"))


def write(path, value):
    Path(path).write_text(json.dumps(value, sort_keys=True, allow_nan=False) + "\n")


def append(path, value):
    with Path(path).open("a") as stream: stream.write(json.dumps(value, sort_keys=True, allow_nan=False) + "\n")


def frozen(root, data):
    report_path = Path("experiments/manifests/generation_2/corpus-freeze.attempt01.json")
    freeze = json.loads(report_path.read_text())
    if freeze["status"] != "PASS_COMPLETE_G2_CORPUS_PANEL_GEOMETRY_FREEZE" or not freeze["development_support"]["pass"]:
        raise ValueError("complete corpus/support freeze must precede student qualification")
    path = root.path(freeze["conditions"][data]["artifact_relative"]); read_complete(path)
    generated_path = Path("exports/lexical-reader-v2/generated-pool-attempt02/accepted.jsonl")
    if sha256(generated_path) != freeze["conditions"][data]["generated_pool_sha256"]:
        raise ValueError("unchanged generated source identity failed")
    rows = {row["variant_id"]: row for file in (generated_path, path / "natural.jsonl")
            for row in (json.loads(line) for line in file.open())}
    ledger = [json.loads(line) for line in (path / "presentations.jsonl").open()]
    updates = json.loads((path / "masters.json").read_text())
    panel_path = root.path(freeze["panel_relative"]); read_complete(panel_path)
    panel = json.loads((panel_path / "panel.json").read_text())
    diagnostic = [{**rows[item["variant_id"]], "id": item["id"], "population": item["population"],
        "native_admitted": True, "shape": rows[item["variant_id"]]}
        for item in json.loads((path / "diagnostics.json").read_text())]
    source_files = ("src/models/g2_training.py", "src/data/g2_stream.py", "src/data/g2_geometry.py",
        "src/models/paired_training_v3.py", "src/models/bc.py", "src/models/core.py", "src/models/training.py",
        "src/models/edits.py", "src/models/tokenizer.py", "src/data/mixed_reader_v3.py",
        "configs/tokenizer_development/tokenizer.json")
    identities = {name: sha256(name) for name in source_files}
    identities.update({"corpus_freeze": sha256(report_path), "natural": sha256(path / "natural.jsonl"),
        "ledger": sha256(path / "presentations.jsonl"), "masters": sha256(path / "masters.json"),
        "actual_updates": sha256(path / "actual-updates.json"), "diagnostics": sha256(path / "diagnostics.json"),
        "panel": sha256(panel_path / "panel.json"), "generated": sha256(generated_path),
        "runtime": {name: importlib.metadata.version(name) for name in ("mlx", "numpy")}})
    return rows, ledger, updates, panel, diagnostic, identities


def create(arm, data, condition, rows, ledger, updates, identities):
    import mlx.core as mx
    from src.data.g2_stream import G2BenchStream
    from src.models.g2_training import G2Native
    from src.models.bc import B100, C101
    model = B100(seed=42) if arm == "B100" else C101(seed=42)
    trainer = G2Native(model, arm, identities, G2BenchStream(rows, ledger, updates, data, condition))
    if sum(value.size for value in trainer.native.optimizer.m.values()) != (100686336 if arm == "B100" else 101081859):
        raise ValueError("fixed full model parameter inventory mismatch")
    mx.eval(trainer.native.arrays()); mx.synchronize()
    return trainer


def forced_losses(trainer, panel, out, label):
    import mlx.core as mx
    from src.models.paired_training_v3 import pack, queue_denominators, objective
    begin = time.perf_counter(); records = []
    for row in panel:
        packed, _ = pack([row["shape"]], trainer.arm)
        den = queue_denominators([{"row": row["shape"]}])
        if trainer.arm == "C101":
            sums = trainer.model.component_sums(**packed[0], dtype=mx.bfloat16)
            mx.eval(sums)
            losses = {key: float(value.item()) / den["C"][key] if den["C"][key] else 0.
                      for key, value in sums.items()}
        else:
            loss = objective(trainer.model, packed, trainer.arm, den, mx.bfloat16)
            mx.eval(loss); losses = {"target": float(loss.item())}
        records.append({"id": row["id"], "population": row["population"], "losses": losses, "denominators": den})
    mx.synchronize(); write(out / f"diagnostic-forced-{label}.json", records)
    return {"cases": len(records), "seconds": time.perf_counter()-begin,
            "records_sha256": sha256(out / f"diagnostic-forced-{label}.json")}


def provenance(arm, data, condition, mode, attempt, before, identities):
    return {"schema": "g2_native_qualification_v1", "arm": arm, "data_condition": data,
        "update_condition": condition, "mode": mode, "attempt": attempt, "seed": 42,
        "code_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "captured_dirty_status": subprocess.check_output(["git", "status", "--porcelain"], text=True),
        "entrypoint_sha256": sha256(__file__), "identities": identities, "before": before,
        "scope": "QUALIFICATION_ONLY_NOT_SCIENTIFIC", "scientific_recipes_started": 0,
        "discard_as_scientific_initializers": True, "status": "RUNNING"}


def run(binding, arm, data, condition, mode, attempt=1, kind=None):
    root = ArtifactRoot(binding); before = root.preflight(); offline_model_environment()
    if (arm, data, condition) not in CONFIGURATIONS or attempt < 1 or mode not in {"bench", "cold"}:
        raise ValueError("only the six fixed BENCH configurations are authorized")
    if mode == "cold" and kind not in {"boundary", "mid"}:
        raise ValueError("one boundary or mid cold path required")
    name = f"{arm}-{data}-{condition}.attempt{attempt:02d}"
    tag = name if mode == "bench" else name + "." + kind
    receipt = Path(f"experiments/manifests/generation_2/{mode}-{tag}.json")
    if receipt.exists(): raise FileExistsError(receipt)
    rows, ledger, updates, panel, diagnostic, identities = frozen(root, data)
    report = provenance(arm, data, condition, mode, attempt, before, identities)
    started = time.perf_counter()
    area = "native-bench-v1" if mode == "bench" else "cold-resume-v1"
    checkpoints = {key: f"native-bench-v1/{name}.{key}" for key in ("initial", "boundary", "mid", "final")}
    report.update(output_relative=f"{area}/{tag}", checkpoint_relatives=checkpoints,
        resume_policy="cold replay of verified completed qualification snapshots only; never a scientific initializer")
    try:
        with atomic_artifact(root, report["output_relative"]) as out:
            write(out / "start.json", report)
            import mlx.core as mx
            from src.models.g2_training import save_g2_checkpoint, load_g2_checkpoint
            from benchmarks.paired_qualification_v3 import evaluation_timing, system_snapshot
            trainer = create(arm, data, condition, rows, ledger, updates, identities)
            probe = rows[ledger[0]["variant_id"]]
            report["startup_seconds"] = time.perf_counter()-started
            if mode == "cold":
                control = root.path(f"native-bench-v1/{name}"); read_complete(control)
                expected = {row["update"]: row for row in (json.loads(line) for line in (control / "updates.jsonl").open())}
                tick = time.perf_counter(); load_g2_checkpoint(root, checkpoints[kind], trainer, rows)
                report["load_seconds"] = time.perf_counter()-tick
                initial_step = trainer.native.optimizer.step
                count = 21 if kind == "mid" else 20
                if initial_step != 5 or bool(trainer.native.queue) != (kind == "mid"):
                    raise ValueError("wrong frozen cold replay boundary/pending actual update")
                matches = []
                for _ in range(count):
                    tick = time.perf_counter(); result = trainer.update(); wall = time.perf_counter()-tick
                    reference = expected[result["update"]]
                    if (trainer.state_hash() != reference["state_sha256"]
                            or any(json.loads(json.dumps(result[key])) != reference[key] for key in FIELDS)):
                        raise ValueError("exact G2 cold replay mismatch; no numeric tolerance")
                    record = {"update": result["update"], "state_sha256": reference["state_sha256"],
                        "status": "EXACT_MATCH", "wall_seconds": wall,
                        "actual_consumption_sha256": hashlib.sha256(json.dumps(result["actual_consumption"],sort_keys=True).encode()).hexdigest()}
                    matches.append(record); append(out / "matches.jsonl", record)
                    print(json.dumps({"configuration": name, "kind": kind, "update": result["update"], "status": "EXACT_MATCH"}),flush=True)
                tick = time.perf_counter(); save_g2_checkpoint(root, f"cold-resume-v1/{tag}.final", trainer, probe)
                report.update(status="PASS_EXACT_G2_COLD_RESUME", final_save_seconds=time.perf_counter()-tick,
                    pending_completion=kind == "mid", next_twenty_complete_updates=20,
                    complete_actual_matches=len(matches), final_state_sha256=trainer.state_hash())
            else:
                save_times = {}
                def save(key):
                    tick = time.perf_counter(); save_g2_checkpoint(root, checkpoints[key], trainer, probe)
                    save_times[key] = time.perf_counter()-tick
                save("initial")
                report["initial_evaluation"] = evaluation_timing(trainer.native, panel, out, "initial")
                report["initial_diagnostic_greedy"] = evaluation_timing(trainer.native, diagnostic, out, "diagnostic-initial")
                report["initial_diagnostic_forced"] = forced_losses(trainer.native, diagnostic, out, "initial")
                snapshots = [system_snapshot()]; records = []; state_hash_seconds = 0.; checkpoint_micro_seconds = 0.
                phase_segments = Counter()
                def one(segment):
                    nonlocal state_hash_seconds, checkpoint_micro_seconds
                    root.preflight(); tick = time.perf_counter()
                    if trainer.native.optimizer.step == 5:
                        trainer.begin(); micro_tick = time.perf_counter(); trainer.microstep()
                        checkpoint_micro_seconds = time.perf_counter()-micro_tick
                        preparation_seconds = time.perf_counter()-tick
                        save("mid"); tick = time.perf_counter()
                        result = trainer.update(); wall = preparation_seconds + time.perf_counter()-tick
                    else:
                        result = trainer.update(); wall = time.perf_counter()-tick
                    queue = trainer.stream._queue(result["master_queue_index"])
                    from src.data.g2_geometry import split_master
                    part = split_master(queue, condition)[result["subqueue_index"]]
                    phases = Counter()
                    for item in part: phases[item["phase"]] += item["canonical_charge"]
                    phase_segments.update(phases)
                    record = {**result, "segment": segment, "wall_seconds": wall, "phase_segments": dict(phases)}
                    if 6 <= result["update"] <= 26:
                        tick = time.perf_counter(); record["state_sha256"] = trainer.state_hash()
                        state_hash_seconds += time.perf_counter()-tick
                    append(out / "updates.jsonl", record)
                    records.append({k:v for k,v in record.items() if k not in ("actual_consumption", "presentation_ids")})
                    if result["update"] == 5: save("boundary")
                    if result["update"] % 25 == 0:
                        snapshots.append(system_snapshot()); write(out / "system-snapshots.json", snapshots)
                    print(json.dumps({"configuration":name,"segment":segment,"update":result["update"],"wall_seconds":wall,
                        "exposure":result["committed_canonical_exposure"]}),flush=True)
                    return record
                for _ in range(5): one("warmup")
                timed_start = time.perf_counter()
                for _ in range(100): one("timed")
                report["timed_elapsed_seconds"] = time.perf_counter()-timed_start
                tick = time.perf_counter()
                while time.perf_counter()-tick < 1200: one("sustained")
                report["sustained_elapsed_seconds"] = time.perf_counter()-tick
                save("final")
                report["final_evaluation"] = evaluation_timing(trainer.native, panel, out, "final")
                report["final_diagnostic_greedy"] = evaluation_timing(trainer.native, diagnostic, out, "diagnostic-final")
                report["final_diagnostic_forced"] = forced_losses(trainer.native, diagnostic, out, "final")
                sustained = [row for row in records if row["segment"] == "sustained"]
                import numpy as np
                timed = [row for row in records if row["segment"] == "timed"]
                def metrics(items):
                    wall = sum(row["wall_seconds"] for row in items); charge = sum(row["canonical_charge"] for row in items)
                    return {"complete_updates":len(items),"update_wall_seconds":wall,"canonical_charge":charge,
                        "anchors_per_second":charge/wall,"mean_update_seconds":wall/len(items),
                        "p95_update_seconds":float(np.quantile([row["wall_seconds"] for row in items],.95))}
                quartile = sustained[-max(1,len(sustained)//4):]
                conservative = min(metrics(sustained)["anchors_per_second"],metrics(quartile)["anchors_per_second"],
                    sum(row["canonical_charge"] for row in sustained)/report["sustained_elapsed_seconds"])
                if set(phase_segments) != {"P0","P1","P2"}: raise ValueError("BENCH did not cover all phase populations")
                report.update(status="PASS_G2_NATIVE_BENCH_COLD_PENDING",warmups=5,timed=metrics(timed),
                    sustained=metrics(sustained),conservative_anchors_per_second=conservative,
                    phase_segments=dict(phase_segments),checkpoint_save_seconds=save_times,
                    state_hash_overhead_seconds=state_hash_seconds,mid_microstep_seconds=checkpoint_micro_seconds,
                    complete_updates=len(records),consumed_exposure=trainer.native.committed_exposure,
                    peak_mlx_allocation_bytes=mx.get_peak_memory(),snapshots=snapshots)
            write(out / "summary.json", report)
        report.update(after=root.preflight())
    except BaseException as error:
        report.update(status="FAILED_QUALIFICATION_REPAIR_REQUIRED",error_type=type(error).__name__)
        raise
    finally:
        report["elapsed_seconds"] = time.perf_counter()-started
        # Per-case hashes/counts/time are public; raw outputs remain in the external artifact.
        compact={k:v for k,v in report.items() if k != "snapshots"}
        for key,value in list(compact.items()):
            if isinstance(value,dict) and "per_case" in value:
                compact[key]={k:v for k,v in value.items() if k != "per_case"}
        write(receipt,compact)
    return report


if __name__ == "__main__":
    parser=argparse.ArgumentParser();parser.add_argument("mode",choices=("bench","cold"))
    parser.add_argument("--artifact-binding",required=True);parser.add_argument("--arm",required=True)
    parser.add_argument("--data",required=True);parser.add_argument("--condition",required=True)
    parser.add_argument("--attempt",type=int,default=1);parser.add_argument("--kind",choices=("boundary","mid"))
    args=parser.parse_args();result=run(args.artifact_binding,args.arm,args.data,args.condition,args.mode,args.attempt,args.kind)
    print(json.dumps({"status":result["status"],"elapsed_seconds":result["elapsed_seconds"]}),flush=True)
