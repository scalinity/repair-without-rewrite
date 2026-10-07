"""Faithful serial execution of the seven prospectively authorized G2 recipes."""
import argparse
import datetime
import fcntl
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import signal
import subprocess
import time

from src.data.g2_artifacts import ArtifactRoot, atomic_artifact, offline_model_environment, read_complete, sha256
from src.data.g2_byt5_schedule import validate_states

SAFE = Path("experiments/manifests/generation_2")
FREEZE = SAFE / "execution-campaign-freeze.attempt01.json"
SCHEDULE = SAFE / "byt5-execution-schedule.attempt01.json"
QUALIFIED = "2c27cff28a31ae64220df9b06094a914e94dd0f3"
PREFLIGHT = "1300a7c50f2b97eed477d2b2c464fcd80e4fbba3"
DECISION = "b1c565e341c1571fec15d4f918049c584246517b"
ORDER = tuple(f"G2-{arm}-{data}-{condition}-seed42-lr3e-4"
              for data, condition in (("D0", "U8"), ("D1", "U1"), ("D1", "U8"))
              for arm in ("B100", "C101")) + ("G2-ByT5-D1-10pass-seed42-lr3e-4",)


def write(path, value):
    with Path(path).open("x") as stream:
        json.dump(value, stream, sort_keys=True, ensure_ascii=False, allow_nan=False)
        stream.write("\n"); stream.flush(); os.fsync(stream.fileno())


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def recipe_path(name):
    if name not in ORDER:
        raise ValueError("only the seven authorized G2 recipes exist")
    return SAFE / f"recipe-{name}.attempt01.json"


def execution_outcomes(name):
    return [json.loads(path.read_text()) for path in sorted(SAFE.glob(f"scientific-outcome-{name}.attempt*.json"))]


def accelerator_lock(root):
    handle = root.path("logs-v1/scientific-accelerator.lock").open("a")
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close()
        raise ValueError("another scientific accelerator job is active")
    return handle


def previous_observation(root, name, step, state_hash):
    receipts = sorted(SAFE.glob(f"scientific-observation-{name}.update{step:05d}.attempt*.json"))
    for path in receipts:
        record = json.loads(path.read_text())
        if record["state_sha256"] != state_hash:
            raise ValueError("replayed observation state differs from retained trained state")
        for relative, identity in record["payload_hashes"].items():
            if sha256(root.path(relative)) != identity:
                raise ValueError("retained scientific observation payload changed")
    return str(receipts[0]) if receipts else None


def record_observation(root, name, attempt, step, state_hash, out, record, payloads):
    record.update(optimizer_update=step, state_sha256=state_hash,
                  payload_hashes={str(path.relative_to(root.root)): sha256(path) for path in payloads})
    path = SAFE / f"scientific-observation-{name}.update{step:05d}.attempt{attempt:02d}.json"
    write(path, record)
    consumption = Path("experiments/manifests") / f"development_calibration_consumption_generation_2_scientific-{name}.update{step:05d}.attempt{attempt:02d}.json"
    write(consumption, {"schema": "g2_scientific_calibration_consumption_v1", "status": "OBSERVED_USE_RECORDED",
                        "recipe_id": name, "attempt": attempt, "optimizer_update": step,
                        "observation_receipt": str(path), "observation_receipt_sha256": sha256(path),
                        **record["calibration_use"], "purpose": "frozen descriptive endpoint evaluation",
                        "training_use": False, "recipe_or_checkpoint_selection": False, "sealed_reference_use": False})
    return str(path)


def calibration_use(panel):
    ids = sorted(row["id"] for row in panel if row.get("role") == "calibration")
    if len(ids) != 1900 or len(set(ids)) != 1900:
        raise ValueError("scientific observation must retain all frozen CAL rows")
    return {"calibration_evaluations": 1900,
            "calibration_ids_sha256": hashlib.sha256(json.dumps(ids, separators=(",", ":")).encode()).hexdigest()}


def verify_corpus(root, corpus):
    from src.data.g2_geometry import projection_hash
    expected_files = {"natural.jsonl": "natural_sha256", "presentations.jsonl": "ledger_sha256",
                      "masters.json": "masters_sha256", "actual-updates.json": "actual_updates_sha256",
                      "diagnostics.json": "diagnostics_sha256"}
    checked = {}
    for data, condition in corpus["conditions"].items():
        directory = root.path(condition["artifact_relative"]); read_complete(directory)
        for filename, field in expected_files.items():
            if sha256(directory / filename) != condition[field]:
                raise ValueError("qualified corpus/geometry/diagnostic changed")
            checked[f"{condition['artifact_relative']}/{filename}"] = condition[field]
        ledger = [json.loads(line) for line in (directory / "presentations.jsonl").open()]
        if projection_hash(ledger) != condition["projection_sha256"]:
            raise ValueError("qualified whole-presentation projection changed")
    panel = root.path(corpus["panel_relative"]); read_complete(panel)
    if sha256(panel / "panel.json") != corpus["panel_sha256"]:
        raise ValueError("qualified DEVELOPMENT panel changed")
    pairs = root.path("asr-hypotheses-v1/construction.attempt01"); read_complete(pairs)
    if sha256(pairs / "pairs.jsonl") != corpus["pairs_sha256"]:
        raise ValueError("qualified D1 census changed")
    checked[f"{corpus['panel_relative']}/panel.json"] = corpus["panel_sha256"]
    checked["asr-hypotheses-v1/construction.attempt01/pairs.jsonl"] = corpus["pairs_sha256"]
    return checked


def verify_qualification():
    preflight = json.loads((SAFE / "execution-preflight.attempt01.json").read_text())
    checked = {}
    for name, expected in preflight["qualification_receipts"].items():
        path = SAFE / name
        if sha256(path) != expected["sha256"] or json.loads(path.read_text())["status"] != expected["status"]:
            raise ValueError("qualification/independent/cold-resume receipt changed")
        checked[str(path)] = expected["sha256"]
    runtimes = {}
    for filename in ("byt5-qualification.attempt02.json", "bench-B100-D0-U8.attempt01.json"):
        record = json.loads((SAFE / filename).read_text())
        expected = record.get("runtime", record.get("identities", {}).get("runtime", {}))
        if not expected:
            raise ValueError("qualified runtime identity absent")
        for name, version in expected.items():
            if importlib.metadata.version(name) != version:
                raise ValueError("qualified native runtime version changed")
            runtimes[name] = version
    return checked, runtimes


def validate_launch_order(name, outcomes):
    if name not in ORDER:
        raise ValueError("unauthorized scientific recipe")
    for previous in ORDER[:ORDER.index(name)]:
        resolved = outcomes.get(previous, [])
        if not resolved or resolved[-1]["status"] not in {"COMPLETED", "FAILED_NUMERICAL"}:
            raise ValueError("preceding scientific recipe has no resolved prescribed outcome")


def boundary_actions(step, pending, resumed_step, saves, evaluations):
    """An interrupted accumulator never supplies a trained observation."""
    return (not pending and step in saves and step != resumed_step,
            not pending and step in evaluations)


def freeze(binding):
    root = ArtifactRoot(binding)
    if git("branch", "--show-current") != "codex/g2-execution" or git("status", "--porcelain"):
        raise ValueError("freeze requires the clean execution branch")
    for ancestor in (QUALIFIED, PREFLIGHT, DECISION):
        subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, "HEAD"], check=True)
    source = git("rev-parse", "HEAD")
    if git("ls-remote", "--heads", "origin", "codex/g2-execution").split()[0] != source:
        raise ValueError("execution implementation must be published before freeze")
    corpus_path = SAFE / "corpus-freeze.attempt01.json"
    corpus = json.loads(corpus_path.read_text())
    if corpus["status"] != "PASS_COMPLETE_G2_CORPUS_PANEL_GEOMETRY_FREEZE":
        raise ValueError("qualified source corpus required")
    artifact_hashes = verify_corpus(root, corpus)
    qualification_hashes, runtimes = verify_qualification()
    recipes = []
    for name in ORDER:
        path = recipe_path(name); recipe = json.loads(path.read_text())
        original = subprocess.check_output(["git", "show", f"{QUALIFIED}:{path}"])
        if path.read_bytes() != original or recipe["status"] != "AUTHORIZED_UNSTARTED" or recipe["scientific_slot_consumed"]:
            raise ValueError("qualified original recipe/state changed")
        if list(SAFE.glob(f"scientific-start-{name}.attempt*.json")):
            raise ValueError("a scientific slot is already consumed")
        recipes.append({"recipe_id": name, "path": str(path), "sha256": sha256(path), "config": recipe,
                        "status": "AUTHORIZED_UNSTARTED", "scientific_slot_consumed": False})
    scientific = root.path("scientific-checkpoints-v1")
    if scientific.exists() and any(scientific.iterdir()):
        raise ValueError("scientific checkpoint area is not empty")
    for area in ("evaluation-v1", "byt5-v1"):
        if list(root.path(area).glob("scientific-*")):
            raise ValueError("a scientific trajectory already exists")
    schedule = json.loads(SCHEDULE.read_text())
    validate_states(recipes[-1]["config"], schedule["states"])
    if sha256(schedule["frontier_decision_path"]) != schedule["frontier_decision_sha256"]:
        raise ValueError("frontier milestone decision identity changed")
    storage_path = SAFE / "storage-reforecast.attempt03.json"
    storage = json.loads(storage_path.read_text())
    if storage["status"] != "PASS_G2_RETAINED_STORAGE_FORECAST":
        raise ValueError("live storage forecast does not pass")
    live = root.preflight()
    if live["literal_free_bytes"] - storage["calculated_remaining_conservative_bytes"] < 250 * 1024**3:
        raise ValueError("live forecast falls below protected storage floor")
    tests_path = SAFE / "execution-launcher-final-tests.attempt03.json"
    tests = json.loads(tests_path.read_text())
    if tests["status"] != "PASS" or tests["passed"] < 477 or tests["skipped"] or tests["failed"]:
        raise ValueError("complete nonregressing execution tests required")
    if any(sha256(path) != identity for path, identity in tests["source_hashes"].items()):
        raise ValueError("execution implementation changed after its complete suite")
    independent_path = SAFE / "execution-launcher-independent.attempt03.json"
    independent = json.loads(independent_path.read_text())
    if (independent["status"] != "PASS_INDEPENDENT_EXECUTION_PREREQUISITES"
            or any(sha256(path) != identity for path, identity in independent["launcher_source_hashes"].items())):
        raise ValueError("independent execution prerequisite reconstruction required")
    sources = sorted({*map(str, Path("src").rglob("*.py")),
                      *map(str, Path("configs").rglob("*.json")),
                      "benchmarks/g2_scientific_campaign.py", "benchmarks/g2_scientific_byt5.py", "benchmarks/g2_scientific_serial.py",
                      "benchmarks/g2_native_qualification.py", "benchmarks/paired_qualification_v3.py",
                      "benchmarks/six_10m_campaign.py", "configs/tokenizer_development/tokenizer.json",
                      "uv.lock", "pyproject.toml"})
    decisions = {path: sha256(path) for path in (
        "docs/reviews/FRONTIER_POST_10M_SCIENTIFIC_DECISION_V1.md", schedule["frontier_decision_path"],
        "docs/reviews/PROSPECTIVE_AMENDMENTS.md")}
    result = {"schema": "g2_scientific_execution_campaign_v1", "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "status": "SEVEN_RECIPES_AUTHORIZED_UNSTARTED", "execution_source_sha": source,
              "qualified_source_sha": QUALIFIED, "preflight_sha": PREFLIGHT, "frontier_decision_commit": DECISION,
              "frontier_decision_hashes": decisions, "source_hashes": {p: sha256(p) for p in sources},
              "scientific_input_hashes": {
                  "exports/lexical-reader-v2/generated-pool-attempt02/accepted.jsonl": corpus["conditions"]["D0"]["generated_pool_sha256"],
                  "exports/byt5-68377bdc18a2ffec8a0533fef03b1c513a4dd49d/pytorch_model.bin": "5c5aaf56299d6f2d4eaadad550a40765198828ead4d74f0a15f91cbe0961931a",
                  "exports/byt5-68377bdc18a2ffec8a0533fef03b1c513a4dd49d/config.json": "7845fb21b320f3fa05392ce151143502cf08729c8c89732da3293615885d3e83"},
              "qualification_hashes": qualification_hashes, "runtime_versions": runtimes,
              "corpus_freeze_path": str(corpus_path), "corpus_freeze_sha256": sha256(corpus_path),
              "data_conditions": corpus["conditions"], "artifact_hashes": artifact_hashes,
              "development_panel_sha256": corpus["panel_sha256"],
              "development_panel_cases": 2984, "natural_cases": 2696, "generated_cases": 288,
              "generated_latents_path": "experiments/manifests/stress_split_repair_20261005T054436Z/latents.jsonl",
              "generated_latents_sha256": sha256("experiments/manifests/stress_split_repair_20261005T054436Z/latents.jsonl"),
              "corruption_profile_path": "experiments/manifests/lexical_reader_v2/lexical-profile-table.attempt01.json",
              "corruption_profile_sha256": sha256("experiments/manifests/lexical_reader_v2/lexical-profile-table.attempt01.json"),
              "byt5_schedule_path": str(SCHEDULE), "byt5_schedule_sha256": sha256(SCHEDULE), "byt5_schedule": schedule,
              "recipes": recipes, "execution_order": list(ORDER), "seed": 42,
              "phase_absolute_ends": [6666667, 9333334, 10000000], "allocation": [15, 15, 20, 10, 40],
              "diagnostic_schedule": "initialization and exact endpoint only; 304 frozen TRAIN cases per data condition",
              "B_C_viability": ["resolved prescribed completion", "failure-inclusive natural WER strictly below RAW",
                                "positive completed natural repair lower bound", "repair supported in at least two source groups",
                                "genuine generated required repair"],
              "ByT5_viability": ["resolved ten-pass completion", "natural WER strictly below RAW",
                                 "positive completed repair lower bound", "repair in at least two source groups"],
              "adequacy_candidate": "D1-U8 separately for B100 and C101; ByT5 exact ten-pass endpoint only",
              "numerical_failure_policy": "retain failure; one identical replay from verified state; repeated numerical failure fails recipe",
              "defect_policy": "stop affected execution; GENERATION_2_EXECUTION_REPAIR_REQUIRED; escalate any scientific choice",
              "storage_policy_path": "configs/generation_2/artifact_policy_v1.json", "artifact_root_identity": live,
              "storage_forecast_sha256": sha256(storage_path), "engineering_tests_sha256": sha256(tests_path),
              "independent_prerequisites_sha256": sha256(independent_path),
              "checkpoint_policy": "qualified complete-actual-update G2 contract; exact pending microbatch resume; no qualification initializer",
              "scientific_slots_consumed": 0, "final_training_started": False, "sealed_inference_performed": False,
              "paper_protocol_v2_frozen": False, "teacher_or_TTS_calls": 0}
    for path, identity in result["scientific_input_hashes"].items():
        if sha256(path) != identity: raise ValueError("pinned scientific model/data input changed")
    write(FREEZE, result)
    return result


def load_campaign(root, name):
    campaign = json.loads(FREEZE.read_text())
    if campaign["execution_order"] != list(ORDER):
        raise ValueError("scientific execution order changed")
    for path, identity in campaign["source_hashes"].items():
        if sha256(path) != identity:
            raise ValueError(f"frozen execution source changed: {path}")
    for path, identity in campaign["scientific_input_hashes"].items():
        if sha256(path) != identity: raise ValueError("pinned scientific model/data input changed")
    for path, identity in campaign["frontier_decision_hashes"].items():
        if sha256(path) != identity:
            raise ValueError("frozen frontier decision or amendment changed")
    if verify_qualification() != (campaign["qualification_hashes"], campaign["runtime_versions"]):
        raise ValueError("frozen qualification/runtime changed")
    if sha256(SCHEDULE) != campaign["byt5_schedule_sha256"]:
        raise ValueError("frozen ByT5 schedule changed")
    freeze_commit = git("log", "-1", "--format=%H", "--", str(FREEZE))
    remote = git("ls-remote", "--heads", "origin", "codex/g2-execution").split()[0]
    subprocess.run(["git", "merge-base", "--is-ancestor", freeze_commit, remote], check=True)
    if git("show", f"{freeze_commit}:{FREEZE}") != FREEZE.read_text().strip():
        raise ValueError("campaign freeze is not exactly the published artifact")
    root.preflight()
    if git("branch", "--show-current") != "codex/g2-execution":
        raise ValueError("scientific launch requires the execution branch")
    corpus = json.loads(Path(campaign["corpus_freeze_path"]).read_text())
    if sha256(campaign["corpus_freeze_path"]) != campaign["corpus_freeze_sha256"]:
        raise ValueError("qualified corpus freeze changed")
    if verify_corpus(root, corpus) != campaign["artifact_hashes"]:
        raise ValueError("frozen scientific artifact identity changed")
    recipe = next(row for row in campaign["recipes"] if row["recipe_id"] == name)
    if sha256(recipe["path"]) != recipe["sha256"]:
        raise ValueError("original qualified recipe changed")
    validate_launch_order(name, {previous: execution_outcomes(previous) for previous in ORDER})
    return campaign, recipe


def claim(root, name, recipe, attempt, resume):
    starts = sorted(SAFE.glob(f"scientific-start-{name}.attempt*.json"))
    outcomes = execution_outcomes(name)
    if attempt != len(starts) + 1:
        raise ValueError("attempt numbering must preserve every prior launch")
    if starts and resume is None:
        raise ValueError("an existing scientific recipe must resume, never restart from scratch")
    if attempt > 1 and (not outcomes or outcomes[-1]["status"] not in {"NUMERICAL_FAILURE", "INTERRUPTED"}):
        raise ValueError("unresolved defect/completion cannot start another attempt")
    if sum(r["status"] == "NUMERICAL_FAILURE" for r in outcomes) >= 2:
        raise ValueError("numerical replay budget exhausted")
    if resume:
        if not resume.startswith(f"scientific-checkpoints-v1/{name}."):
            raise ValueError("resume must use this recipe's scientific checkpoint")
        read_complete(root.path(resume))
        if resume != outcomes[-1]["latest_verified_checkpoint"]:
            raise ValueError("resume must use the latest retained verified state")
    report = {"schema": "g2_scientific_recipe_attempt_v1", "recipe_id": name, "attempt": attempt,
              "status": "RUNNING", "scientific_slot_consumed": True, "seed": 42,
              "code_commit": git("rev-parse", "HEAD"), "captured_dirty_status": git("status", "--porcelain"),
              "config_sha256": recipe["sha256"], "campaign_sha256": sha256(FREEZE),
              "data_manifest_sha256": sha256(SAFE / "corpus-freeze.attempt01.json"),
              "resume_relative": resume, "before": root.preflight(), "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "no_concurrent_accelerator": True}
    write(SAFE / f"scientific-start-{name}.attempt{attempt:02d}.json", report)
    return report


def run_native(binding, name, attempt=1, resume=None):
    root = ArtifactRoot(binding); offline_model_environment()
    lock = accelerator_lock(root)
    campaign, recipe = load_campaign(root, name); cfg = recipe["config"]
    report = claim(root, name, recipe, attempt, resume); started = time.perf_counter()
    relative = f"evaluation-v1/scientific-{name}.attempt{attempt:02d}"
    report["output_relative"] = relative; latest = resume; trainer = None; out = None
    stopped = []
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda signum, frame: stopped.append(signum))
    try:
        with atomic_artifact(root, relative) as out:
            write(out / "start.json", report)
            from benchmarks.g2_native_qualification import frozen, forced_losses
            from benchmarks.paired_qualification_v3 import evaluation_timing
            from benchmarks.six_10m_campaign import tensor_hash
            from src.models.g2_training import G2Native, save_g2_checkpoint, load_g2_checkpoint
            from src.data.g2_stream import G2ScientificStream
            from src.models.bc import B100, C101
            import mlx.core as mx
            rows, ledger, masters, panel, diagnostic, identities = frozen(root, cfg["data_condition"])
            identities.update(campaign_sha256=sha256(FREEZE), recipe_sha256=recipe["sha256"])
            arm = cfg["arm"]; model = B100(seed=42) if arm == "B100" else C101(seed=42)
            trainer = G2Native(model, arm, identities, G2ScientificStream(rows, ledger, masters, cfg["data_condition"], cfg["update_condition"]))
            mx.eval(trainer.native.arrays()); mx.synchronize()
            initial = tensor_hash(trainer.native, "model::")
            moments = tensor_hash(trainer.native, "m::") + ":" + tensor_hash(trainer.native, "v::")
            if (initial != cfg["model"]["initial_parameter_sha256"]
                    or moments != cfg["model"]["initial_optimizer_sha256"]
                    or sum(v.size for v in trainer.native.optimizer.m.values()) != cfg["model"]["parameter_count"]):
                raise ValueError("fresh seed42 model differs from qualified initialization")
            report["fresh_initial_parameter_sha256"] = initial
            probe = rows[ledger[0]["variant_id"]]
            if resume:
                report["resume_readback"] = load_g2_checkpoint(root, resume, trainer, rows)
            saves = {p["optimizer_updates"]: p for p in cfg["save_endpoints"]}
            evaluations = {p["optimizer_updates"]: p for p in cfg["evaluation_endpoints"]}
            snapshots, observations = [], []
            def checkpoint(label):
                nonlocal latest
                point = f"scientific-checkpoints-v1/{name}.attempt{attempt:02d}.{label}"
                tick = time.perf_counter(); complete = save_g2_checkpoint(root, point, trainer, probe)
                latest = point
                result = {"relative": point, "optimizer_update": trainer.native.optimizer.step,
                          "actual_exposure": trainer.native.committed_exposure, "seconds": time.perf_counter() - tick,
                          "complete": complete, "state_sha256": trainer.state_hash()}
                snapshots.append(result); write(out / f"checkpoint-{label}.json", result)
                return result
            def observe(step):
                point = evaluations[step]; label = f"update{step:04d}"
                prior = trainer.state_hash(); tick = time.perf_counter()
                relative = f"evaluation-v1/scientific-observation-{name}.update{step:05d}.attempt{attempt:02d}"
                with atomic_artifact(root, relative) as evaluation_out:
                    panel_result = evaluation_timing(trainer.native, panel, evaluation_out, label)
                    if prior != trainer.state_hash():
                        raise ValueError("heldout observation changed trained state")
                    record = {"endpoint": point, "panel": panel_result, "calibration_use": calibration_use(panel)}
                    if step in (0, cfg["stop_endpoint"]["optimizer_updates"]):
                        record["diagnostic_greedy"] = evaluation_timing(trainer.native, diagnostic, evaluation_out, f"diagnostic-{label}")
                        record["diagnostic_forced"] = forced_losses(trainer.native, diagnostic, evaluation_out, label)
                        if prior != trainer.state_hash():
                            raise ValueError("TRAIN diagnostic changed trained state")
                    record["seconds"] = time.perf_counter() - tick
                    write(evaluation_out / "observation.json", record)
                final = root.path(relative)
                payloads = [path for path in final.iterdir() if path.name != "COMPLETE.json"]
                observations.append(record_observation(root, name, attempt, step, prior, final, record, payloads))
            resumed_step = trainer.native.optimizer.step if resume else None
            while True:
                root.preflight(); step = trainer.native.optimizer.step
                label = f"update{step:04d}"
                save_now, observe_now = boundary_actions(step, bool(trainer.native.queue), resumed_step, saves, evaluations)
                if save_now:
                    checkpoint(label)
                if observe_now:
                    retained = previous_observation(root, name, step, trainer.state_hash())
                    if retained:
                        observations.append(retained)
                    else:
                        observe(step)
                if step == cfg["stop_endpoint"]["optimizer_updates"]:
                    break
                tick = time.perf_counter()
                if not trainer.native.queue:
                    trainer.begin()
                while trainer.native.completed_microbatches < len(trainer.native.partition):
                    trainer.microstep()
                    if stopped:
                        checkpoint(f"interruption-update{step:04d}-micro{trainer.native.completed_microbatches:04d}")
                        raise InterruptedError("safe interruption at completed microbatch")
                result = trainer.finish(); mx.synchronize()
                result["update_wall_seconds"] = time.perf_counter() - tick
                with (out / "updates.jsonl").open("a") as stream:
                    stream.write(json.dumps(result, sort_keys=True, allow_nan=False) + "\n"); stream.flush()
                if trainer.stream.subqueue_index == 0:
                    print(json.dumps({"phase": "G2-scientific-training", "recipe_id": name,
                                      "update": result["update"], "exposure": result["committed_canonical_exposure"]}), flush=True)
            if trainer.native.committed_exposure != cfg["stop_endpoint"]["actual_exposure"]:
                raise ValueError("scientific final exposure differs from qualified endpoint")
            report.update(status="COMPLETED", completed_updates=trainer.native.optimizer.step,
                          actual_exposure=trainer.native.committed_exposure, checkpoints=snapshots, evaluations=observations,
                          updates_sha256=sha256(out / "updates.jsonl") if (out / "updates.jsonl").exists() else None,
                          final_state_sha256=trainer.state_hash(),
                          latest_verified_checkpoint=latest, elapsed_seconds=time.perf_counter() - started, after=root.preflight())
            write(out / "finish.json", report)
        report["artifact_complete_sha256"] = sha256(root.path(relative) / "COMPLETE.json")
    except Exception as error:
        numerical = isinstance(error, FloatingPointError)
        previous_numerical = sum(r["status"] == "NUMERICAL_FAILURE" for r in execution_outcomes(name))
        status = "INTERRUPTED" if isinstance(error, InterruptedError) else ("FAILED_NUMERICAL" if numerical and previous_numerical else "NUMERICAL_FAILURE" if numerical else "STOPPED_DEFECT")
        try:
            root.preflight()
            if out is not None and out.exists():
                (out / "failure.txt").write_text(repr(error) + "\n")
                report["failure_sha256"] = sha256(out / "failure.txt")
                report["retained_partial_relative"] = str(out.relative_to(root.root))
                if trainer is not None:
                    import numpy as np
                    np.savez(out / "failed-arrays.npz", **{k: np.asarray(v) for k, v in trainer.native.arrays().items()})
                    report["failed_arrays_sha256"] = sha256(out / "failed-arrays.npz")
        except Exception as retention_error:
            report["failure_retention_error_type"] = type(retention_error).__name__
        report.update(status=status, exception_type=type(error).__name__, latest_verified_checkpoint=latest,
                      completed_updates=None if trainer is None else trainer.native.optimizer.step,
                      elapsed_seconds=time.perf_counter() - started,
                      disposition="EXACT_REPLAY_REQUIRED" if status == "NUMERICAL_FAILURE" else "GENERATION_2_EXECUTION_REPAIR_REQUIRED" if status == "STOPPED_DEFECT" else status)
        write(SAFE / f"scientific-outcome-{name}.attempt{attempt:02d}.json", report)
        lock.close()
        raise
    write(SAFE / f"scientific-outcome-{name}.attempt{attempt:02d}.json", report)
    lock.close()
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("freeze", "run"))
    parser.add_argument("--artifact-binding", required=True)
    parser.add_argument("--recipe", choices=ORDER)
    parser.add_argument("--attempt", type=int, default=1)
    parser.add_argument("--resume")
    args = parser.parse_args()
    if args.mode == "freeze":
        result = freeze(args.artifact_binding)
    elif args.recipe == ORDER[-1]:
        from benchmarks.g2_scientific_byt5 import run
        result = run(args.artifact_binding, args.attempt, args.resume)
    else:
        result = run_native(args.artifact_binding, args.recipe, args.attempt, args.resume)
    print(json.dumps({"status": result["status"]}), flush=True)
