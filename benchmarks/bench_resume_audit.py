"""Two fresh-process, 20-complete-update continuation audit of a BENCH fixture.

This supplements native_calibration.py; it does not qualify its random geometry
as the representative BENCH-00 grid. Run only with the accelerator slot released.
"""
import argparse
from dataclasses import asdict
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def json_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def compare_runs(control_rows, restored_rows, control_end, restored_end):
    """Compare numerical/state evidence, excluding measurement-only elapsed time."""
    trajectory = []
    for index, (control, restored) in enumerate(zip(control_rows, restored_rows)):
        for key in ("update", "state"):
            if control[key] != restored[key]:
                trajectory.append({"ordinal": index, "field": key})
    return {
        "exact_20_step_count": len(control_rows) == len(restored_rows) == 20,
        "trajectory_mismatches": trajectory,
        "end_state_exact": control_end["state"] == restored_end["state"],
        "all_tensor_digests_exact": control_end["tensor_digests"] == restored_end["tensor_digests"],
        "dtype_inventory_exact": control_end["dtype_inventory"] == restored_end["dtype_inventory"],
        "distinct_process_ids": control_end["process_id"] != restored_end["process_id"],
    }


def worker(args):
    # Imported only in an explicitly launched numerical worker, never --help.
    import random
    import numpy as np
    import mlx.core as mx
    from src.models.core import ModelConfig, DecoderLM
    from src.models.training import Trainer, TokenSchedule, flat_parameters, load_checkpoint, save_checkpoint

    if os.environ.get("MLX_ENABLE_TF32") != "0":
        raise RuntimeError("resume audit requires MLX_ENABLE_TF32=0")
    base, out = Path(args.benchmark_root), Path(args.out)
    checkpoint = Path(args.source_checkpoint)
    meta = json.loads((checkpoint / "metadata.json").read_text())
    recipe = json.loads((base / "config.json").read_text())
    identities = {"config": sha(base / "config.json"), "data": sha(base / "native_token_manifest.npy")}
    if meta["identities"] != identities or meta["config"] != recipe["geometry"]:
        raise ValueError("benchmark fixture/checkpoint identity mismatch")
    if meta["working_dtype"] != "mlx.core.bfloat16" or meta["backend"] != "reference":
        raise ValueError("audit only supports the declared BF16 reference fixture")
    if meta["acc_microbatches"] or meta["acc_denominator"] or meta["pending_tokens"]:
        raise ValueError("audit requires an optimizer-boundary checkpoint")
    then = time.perf_counter()
    trainer = Trainer(DecoderLM(ModelConfig(**meta["config"]), seed=42),
                      TokenSchedule(**meta["schedule"]), dtype=mx.bfloat16,
                      backend=meta["backend"], identities=identities,
                      optimizer_options=meta["optimizer_policy"])
    load_checkpoint(trainer, checkpoint)
    load_seconds = time.perf_counter() - then
    token_blocks = np.load(base / "native_token_manifest.npy", allow_pickle=False)
    if token_blocks.shape != (recipe["accumulation"], 1, recipe["sequence_length"]):
        raise ValueError("unexpected fixed fixture shape")
    batches = [mx.array(block) for block in token_blocks]
    mx.eval(batches)
    mx.synchronize()

    def state():
        nr = np.random.get_state()
        rng = {"python": random.getstate(),
               "numpy": [nr[0], nr[1].tolist(), *nr[2:]],
               "augmentation": trainer.augmentation_rng.bit_generator.state,
               "mlx_explicit_key": trainer.rng.key.tolist()}
        return {"optimizer_step": trainer.optimizer.step,
                "processed_tokens": trainer.processed_tokens,
                "pending_tokens": trainer.pending_tokens, "loss_sum": trainer.loss_sum,
                "data_cursor": trainer.data_cursor, "data_order": trainer.data_order,
                "phase": trainer.phase, "acc_denominator": trainer.accumulator.denominator,
                "acc_microbatches": trainer.accumulator.microbatches,
                "rng_sha256": json_sha(rng), "schedule": asdict(trainer.schedule),
                "optimizer_policy": trainer.optimizer.policy(), "identities": trainer.identities}

    def tree_digest(values):
        digest = hashlib.sha256()
        for name, value in sorted(values.items()):
            array = np.asarray(value)
            digest.update(json.dumps([name, list(array.shape), str(array.dtype)], separators=(",", ":")).encode())
            digest.update(memoryview(array).cast("B"))
        return digest.hexdigest()

    start_state = state()
    checkpoint_seconds = None
    if args.worker == "control":
        then = time.perf_counter()
        checkpoint_hashes = save_checkpoint(trainer, args.audit_checkpoint)
        checkpoint_seconds = time.perf_counter() - then
        if state() != start_state:
            raise AssertionError("checkpoint save changed continuation state")
        write_json(out / "audit_start_checkpoint.json", {
            "path": args.audit_checkpoint, "hashes": checkpoint_hashes,
            "bytes": sum(p.stat().st_size for p in Path(args.audit_checkpoint).iterdir() if p.is_file()),
            "checkpoint_seconds": checkpoint_seconds, "state": start_state})
    with (out / (args.worker + "_steps.jsonl")).open("w", buffering=1) as stream:
        for ordinal in range(20):
            then = time.perf_counter()
            for ids in batches:
                trainer.accumulate(ids)
            update = trainer.update()
            mx.eval(trainer.model.parameters(), trainer.optimizer.m,
                    trainer.optimizer.v, trainer.accumulator.values, trainer.rng.key)
            mx.synchronize()
            row = {"ordinal": ordinal, "update": update, "state": state(),
                   "elapsed_seconds": time.perf_counter() - then}
            stream.write(json.dumps(row, sort_keys=True) + "\n")
    end = {"process_id": os.getpid(), "load_and_initialization_seconds": load_seconds,
           "parameter_count": sum(v.size for v in flat_parameters(trainer.model).values()),
           "state": state(), "start_state": start_state,
           "dtype_inventory": trainer.dtype_inventory(),
           "tensor_digests": {"parameters": tree_digest(flat_parameters(trainer.model)),
                              "moment_m": tree_digest(trainer.optimizer.m),
                              "moment_v": tree_digest(trainer.optimizer.v),
                              "accumulator": tree_digest(trainer.accumulator.values)},
           "peak_mlx_memory_bytes": mx.get_peak_memory(),
           "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    write_json(out / (args.worker + "_end.json"), end)
    print(json.dumps({"worker": args.worker, "status": "COMPLETE", "process_id": os.getpid()}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark-root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--source-checkpoint", required=True)
    parser.add_argument("--audit-checkpoint", required=True)
    parser.add_argument("--worker", choices=("control", "restored"))
    args = parser.parse_args()
    if args.worker:
        worker(args)
        return
    if os.environ.get("MLX_ENABLE_TF32") != "0":
        raise RuntimeError("resume audit requires MLX_ENABLE_TF32=0")
    base, out = Path(args.benchmark_root).resolve(), Path(args.out).resolve()
    # The parent has no MLX import/model. Each child terminates before the next.
    provenance = json.loads((base / "provenance.json").read_text())
    if sha("uv.lock") != provenance["runtime_lock_sha256"]:
        raise ValueError("research runtime lock changed after the benchmark")
    gate_path = Path("docs/reports/raw/model0/gate_evidence.json")
    gate = json.loads(gate_path.read_text())
    if sha(gate_path) != provenance["gate_evidence_sha256"]:
        raise ValueError("qualified gate evidence changed")
    for path in ("src/models/core.py", "src/models/training.py"):
        if sha(path) != gate["code_hashes"][path]:
            raise ValueError("qualified code changed: " + path)
    for name, expected in (("config.json", "config_sha256"), ("native_token_manifest.npy", "manifest_sha256")):
        if sha(base / name) != provenance[expected]:
            raise ValueError("changed benchmark input: " + name)
    checkpoint = Path(args.source_checkpoint).resolve()
    audit_checkpoint = Path(args.audit_checkpoint).resolve()
    if audit_checkpoint.exists():
        raise FileExistsError("audit checkpoint destination already exists")
    complete = json.loads((checkpoint / "COMPLETE.json").read_text())
    for name in ("arrays.npz", "metadata.json"):
        if sha(checkpoint / name) != complete[name]:
            raise ValueError("incomplete/changed source checkpoint")
    out.mkdir(parents=True, exist_ok=False)
    write_json(out / "provenance.json", {
        "schema": "bench_resume_fresh_process_v1", "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "git_dirty": subprocess.check_output(["git", "status", "--porcelain=v1"], text=True),
        "seed": 42,
        "parent_benchmark": str(base), "parent_provenance_sha256": sha(base / "provenance.json"),
        "parent_summary_sha256": sha(base / "summary.json") if (base / "summary.json").exists() else None,
        "source_checkpoint": str(checkpoint), "source_checkpoint_hashes": complete,
        "config_sha256": provenance["config_sha256"], "manifest_sha256": provenance["manifest_sha256"],
        "runtime_lock_sha256": sha("uv.lock"), "python": sys.version,
        "script_sha256": sha(__file__), "core_sha256": sha("src/models/core.py"),
        "training_sha256": sha("src/models/training.py"),
        "updates_per_process": 20, "same_fixed_batches_in_original_order": True,
        "scope": "fresh-process resume of random-token geometry; full BENCH-00 remains unqualified"})
    command = [sys.executable, "-m", "benchmarks.bench_resume_audit",
               "--benchmark-root", str(base), "--out", str(out),
               "--audit-checkpoint", str(audit_checkpoint)]
    for phase, source in (("control", str(checkpoint)), ("restored", str(audit_checkpoint))):
        with (out / (phase + "_process.txt")).open("w") as stream:
            result = subprocess.run(command + ["--source-checkpoint", source, "--worker", phase],
                                    stdout=stream, stderr=subprocess.STDOUT)
        if result.returncode:
            write_json(out / "summary.json", {"status": "FAIL_PROCESS", "phase": phase, "returncode": result.returncode})
            raise RuntimeError("audit child failed; preserve its raw process receipt")
    rows = {phase: [json.loads(line) for line in (out / (phase + "_steps.jsonl")).read_text().splitlines()]
            for phase in ("control", "restored")}
    ends = {phase: json.loads((out / (phase + "_end.json")).read_text()) for phase in rows}
    comparison = compare_runs(rows["control"], rows["restored"], ends["control"], ends["restored"])
    start_exact = ends["control"]["start_state"] == ends["restored"]["start_state"]
    passed = start_exact and all(comparison[key] for key in (
        "exact_20_step_count", "end_state_exact", "all_tensor_digests_exact",
        "dtype_inventory_exact", "distinct_process_ids")) and not comparison["trajectory_mismatches"]
    recipe = json.loads((base / "config.json").read_text())
    summary = {"status": "PASS_FRESH_PROCESS_20_UPDATE_RESUME" if passed else "FAIL_RESUME",
               "start_state_exact": start_exact, **comparison,
               "additional_complete_updates": 40,
               "parameter_count": ends["control"]["parameter_count"],
               "additional_processed_fixture_tokens": sum(r["update"]["microbatches"] *
                   recipe["sequence_length"] for phase in rows for r in rows[phase]),
               "limitations": ["same four fixed random blocks; no data-reader/random augmentation exercised",
                               "digest equality establishes bitwise equality only on this pinned backend/hardware",
                               "audit elapsed time includes per-step state receipts; not a throughput benchmark"],
               "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    write_json(out / "summary.json", summary)
    print(json.dumps(summary, sort_keys=True), flush=True)
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
