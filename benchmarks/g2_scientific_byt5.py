"""The fixed G2 ByT5 trajectory, with four completed-update observations."""
import hashlib
import json
import math
from pathlib import Path
import signal
import time

from benchmarks.g2_scientific_campaign import (FREEZE, ORDER, SAFE, accelerator_lock, calibration_use, claim,
    execution_outcomes, load_campaign, previous_observation, record_observation, write)
from src.data.g2_artifacts import ArtifactRoot, atomic_artifact, offline_model_environment, read_complete, sha256
from src.data.g2_byt5 import accounting_plan, training_batches
from src.data.g2_byt5_schedule import validate_states


def incorporated_presentations(step):
    if type(step) is not int or not 0 <= step <= 35283:
        raise ValueError("invalid fixed ByT5 update cursor")
    return min(4 * step, 141130)


def assert_equal_tree(left, right, torch):
    if torch.is_tensor(left):
        if not torch.is_tensor(right) or left.dtype != right.dtype or not torch.equal(left.detach().cpu(), right.detach().cpu()):
            raise ValueError("exact ByT5 portable tensor readback mismatch")
    elif isinstance(left, dict):
        if not isinstance(right, dict) or left.keys() != right.keys():
            raise ValueError("exact ByT5 portable inventory mismatch")
        for key in left:
            assert_equal_tree(left[key], right[key], torch)
    elif isinstance(left, (tuple, list)):
        if type(left) is not type(right) or len(left) != len(right):
            raise ValueError("exact ByT5 portable sequence mismatch")
        for a, b in zip(left, right):
            assert_equal_tree(a, b, torch)
    elif left != right:
        raise ValueError("exact ByT5 portable scalar readback mismatch")


def tree_hash(value, torch):
    digest = hashlib.sha256()
    def visit(item):
        if torch.is_tensor(item):
            tensor = item.detach().cpu().contiguous()
            digest.update(str((str(tensor.dtype), tuple(tensor.shape))).encode())
            digest.update(tensor.numpy().tobytes())
        elif isinstance(item, dict):
            for key in sorted(item, key=str):
                digest.update(str(key).encode()); visit(item[key])
        elif isinstance(item, (tuple, list)):
            digest.update(type(item).__name__.encode())
            for child in item: visit(child)
        else:
            digest.update(json.dumps(item, sort_keys=True, allow_nan=False).encode())
    visit(value)
    return digest.hexdigest()


def run(binding, attempt=1, resume=None):
    root = ArtifactRoot(binding); offline_model_environment(); lock = accelerator_lock(root)
    name = ORDER[-1]; campaign, recipe = load_campaign(root, name)
    cfg = recipe["config"]; states = campaign["byt5_schedule"]["states"]
    validate_states(cfg, states)
    report = claim(root, name, recipe, attempt, resume); started = time.perf_counter()
    relative = f"byt5-v1/scientific-{name}.attempt{attempt:02d}"
    report["output_relative"] = relative
    latest = resume; step = 0; out = model = optimizer = None; interrupted = []
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda signum, frame: interrupted.append(signum))
    try:
        with atomic_artifact(root, relative) as out:
            write(out / "start.json", report)
            import torch
            from transformers import T5ForConditionalGeneration
            from src.inference.byt5_probe import native_batch, decode_ids
            from src.data.comparator_interfaces import byt5_ids
            from src.scoring.records import Output, prepare_source, score_output
            from src.scoring.triple import serialize
            corpus = json.loads(Path(campaign["corpus_freeze_path"]).read_text())
            pairs = root.path("asr-hypotheses-v1/construction.attempt01")
            training = [row for row in (json.loads(line) for line in (pairs / "pairs.jsonl").open()) if row["role"] == "train"]
            if accounting_plan(training) != corpus["byt5_accounting"]:
                raise ValueError("qualified complete ByT5 sequence changed")
            panel = json.loads((root.path(corpus["panel_relative"]) / "panel.json").read_text())
            weights = Path("exports/byt5-68377bdc18a2ffec8a0533fef03b1c513a4dd49d")
            identities = {"campaign_sha256": sha256(FREEZE), "recipe_sha256": recipe["sha256"],
                          "pairs_sha256": sha256(pairs / "pairs.jsonl"), "panel_sha256": corpus["panel_sha256"],
                          "official_weight_sha256": sha256(weights / "pytorch_model.bin"),
                          "official_config_sha256": sha256(weights / "config.json")}
            if (identities["official_weight_sha256"] != "5c5aaf56299d6f2d4eaadad550a40765198828ead4d74f0a15f91cbe0961931a"
                    or identities["official_config_sha256"] != "7845fb21b320f3fa05392ce151143502cf08729c8c89732da3293615885d3e83"):
                raise ValueError("official pinned ByT5 assets changed")
            torch.manual_seed(42); torch.set_num_threads(2)
            if not torch.backends.mps.is_available():
                raise RuntimeError("required native MPS device unavailable")
            model = T5ForConditionalGeneration.from_pretrained(str(weights), local_files_only=True, weights_only=True,
                trust_remote_code=False, attn_implementation="eager", torch_dtype=torch.float32).to("mps")
            if sum(value.numel() for value in model.parameters()) != 299637760:
                raise ValueError("fixed ByT5 parameter count changed")
            optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, betas=(.9, .999), eps=1e-8, weight_decay=.01)
            native_cfg = {"source_capacity": 512, "target_capacity": 512}
            def portable():
                return {"schema": "g2_byt5_scientific_checkpoint_v1", "model": model.state_dict(),
                        "optimizer": optimizer.state_dict(), "torch_cpu_rng": torch.get_rng_state(),
                        "mps_rng": torch.mps.get_rng_state(), "completed_updates": step,
                        "actual_presentations": incorporated_presentations(step), "identities": identities,
                        "training": model.training,
                        "gradient_resume_policy": "completed-update only; inherited zero_grad before the next batch"}
            def state_hash():
                return tree_hash(portable(), torch)
            if resume:
                checkpoint_path = root.path(resume); read_complete(checkpoint_path)
                saved = torch.load(checkpoint_path / "state.pt", map_location="cpu", weights_only=True)
                if saved["schema"] != "g2_byt5_scientific_checkpoint_v1" or saved["identities"] != identities:
                    raise ValueError("ByT5 scientific resume identity mismatch")
                step = saved["completed_updates"]
                if saved["actual_presentations"] != incorporated_presentations(step):
                    raise ValueError("ByT5 exact presentation/update cursor mismatch")
                model.load_state_dict(saved["model"], strict=True); optimizer.load_state_dict(saved["optimizer"])
                model.train(saved["training"])
                torch.set_rng_state(saved["torch_cpu_rng"]); torch.mps.set_rng_state(saved["mps_rng"])
                assert_equal_tree(portable(), saved, torch)
                del saved
                report["resume_readback"] = {"optimizer_update": step, "actual_presentations": incorporated_presentations(step),
                                            "state_sha256": state_hash(), "exact_portable_state_equal": True}
            snapshots, observations = [], []
            def checkpoint(label):
                nonlocal latest
                root.preflight(); tick = time.perf_counter()
                point = f"scientific-checkpoints-v1/{name}.attempt{attempt:02d}.{label}"
                with atomic_artifact(root, point) as pending:
                    torch.save(portable(), pending / "state.pt")
                    saved = torch.load(pending / "state.pt", map_location="cpu", weights_only=True)
                    assert_equal_tree(portable(), saved, torch)
                    del saved
                latest = point
                result = {"relative": point, "optimizer_update": step, "actual_presentations": incorporated_presentations(step),
                          "seconds": time.perf_counter() - tick, "state_pt_sha256": sha256(root.path(point) / "state.pt")}
                snapshots.append(result)
                return result
            def observe(state):
                before = state_hash(); was_training = model.training
                cpu_rng, mps_rng = torch.get_rng_state(), torch.mps.get_rng_state()
                gradients = tree_hash([value.grad for value in model.parameters()], torch)
                label = f"update{step:05d}"; tick = time.perf_counter(); decode_total = score_total = 0.; counts = {}
                point = f"evaluation-v1/scientific-observation-{name}.{label}.attempt{attempt:02d}"
                with atomic_artifact(root, point) as observation_out:
                    model.eval()
                    with (observation_out / "records.jsonl").open("x") as stream:
                        for index, row in enumerate(panel):
                            root.preflight(); begin = time.perf_counter(); answer = None
                            try:
                                byt5_ids(row["source"], qualified_capacity=512)
                                byt5_ids(row["target"], qualified_capacity=512)
                            except ValueError:
                                decoded = {"status": "invalid_utf8", "text": None, "reason": "retained_evaluation_capacity_overflow"}
                            else:
                                batch, _ = native_batch([{**row, "reference": row["target"]}], native_cfg, "mps")
                                with torch.inference_mode():
                                    answer = model.generate(input_ids=batch["input_ids"], attention_mask=batch["attention_mask"],
                                        do_sample=False, num_beams=1, max_new_tokens=512, use_cache=True,
                                        eos_token_id=1, pad_token_id=0, decoder_start_token_id=0)[0].tolist()
                                torch.mps.synchronize(); decoded = decode_ids(answer)
                            decode_seconds = time.perf_counter() - begin; decode_total += decode_seconds; begin = time.perf_counter()
                            scored = score_output(prepare_source(row["target"], row["source"]), Output(decoded["text"], decoded["status"]))
                            score_seconds = time.perf_counter() - begin; score_total += score_seconds
                            stream.write(serialize({"id": row["id"], "population": row["population"], "milestone": state,
                                "status": decoded["status"], "decoded": decoded, "generated_ids": answer, "score": scored,
                                "decode_seconds": decode_seconds, "scorer_seconds": score_seconds}) + "\n")
                            counts[decoded["status"]] = counts.get(decoded["status"], 0) + 1
                            if (index + 1) % 100 == 0:
                                print(json.dumps({"phase": "ByT5-scientific-evaluation", "optimizer_update": step, "cases": index + 1}), flush=True)
                    model.train(was_training); torch.set_rng_state(cpu_rng); torch.mps.set_rng_state(mps_rng)
                    if before != state_hash() or gradients != tree_hash([value.grad for value in model.parameters()], torch):
                        raise ValueError("descriptive ByT5 observation changed training state")
                    record = {"milestone": state, "cases": len(panel), "calibration_use": calibration_use(panel), "decode_seconds": decode_total,
                              "scorer_seconds": score_total, "seconds": time.perf_counter() - tick,
                              "status_counts": counts, "descriptive_only": step != 35283}
                    write(observation_out / "observation.json", record)
                final = root.path(point)
                observations.append(record_observation(root, name, attempt, step, before, final, record,
                    [path for path in final.iterdir() if path.name != "COMPLETE.json"]))
            scheduled = {state["optimizer_update"]: state for state in states}
            batches = training_batches(training)
            for _ in range(step): next(batches)
            resumed_step = step if resume else None
            while True:
                root.preflight()
                if step in scheduled:
                    if step != resumed_step: checkpoint(f"update{step:05d}")
                    retained = previous_observation(root, name, step, state_hash())
                    if retained: observations.append(retained)
                    else: observe(scheduled[step])
                if step == 35283: break
                if interrupted:
                    checkpoint(f"interruption-update{step:05d}")
                    raise InterruptedError("ByT5 safe interruption at completed optimizer state")
                selected = next(batches); tick = time.perf_counter(); model.train()
                batch, count = native_batch([{**item["row"], "reference": item["row"]["target"]} for item in selected], native_cfg, "mps")
                optimizer.zero_grad(set_to_none=True); prediction = model(**batch, use_cache=False); loss = prediction.loss
                loss.backward(); norm = float(torch.nn.utils.clip_grad_norm_(model.parameters(), 1.)); value = float(loss.detach())
                if not math.isfinite(value) or not math.isfinite(norm): raise FloatingPointError("nonfinite ByT5 scientific update")
                optimizer.step(); torch.mps.synchronize(); step += 1
                if any(not bool(torch.isfinite(value).all()) for value in model.parameters()):
                    raise FloatingPointError("nonfinite ByT5 scientific parameters")
                record = {"update": step, "actual_presentations": incorporated_presentations(step), "lr": 3e-4,
                          "loss": value, "gradient_norm": norm, "wall_seconds": time.perf_counter() - tick,
                          "presentations": [{k: item[k] for k in ("presentation", "pass_index", "pass_offset")} for item in selected],
                          "ids": [item["row"]["id"] for item in selected], "native_targets": count,
                          "native_source": int(batch["attention_mask"].sum())}
                with (out / "steps.jsonl").open("a") as stream:
                    stream.write(json.dumps(record, sort_keys=True, allow_nan=False) + "\n"); stream.flush()
                if step % 100 == 0: print(json.dumps({"phase": "ByT5-scientific-training", "update": step}), flush=True)
            if next(batches, None) is not None: raise ValueError("ByT5 iterator extends beyond ten-pass endpoint")
            report.update(status="COMPLETED", completed_updates=step, actual_presentations=incorporated_presentations(step),
                          milestones=states, checkpoints=snapshots, evaluations=observations, latest_verified_checkpoint=latest,
                          final_state_sha256=state_hash(), elapsed_seconds=time.perf_counter() - started, after=root.preflight())
            write(out / "finish.json", report)
        report["artifact_complete_sha256"] = sha256(root.path(relative) / "COMPLETE.json")
    except Exception as error:
        numerical = isinstance(error, FloatingPointError)
        prior = sum(r["status"] == "NUMERICAL_FAILURE" for r in execution_outcomes(name))
        status = "INTERRUPTED" if isinstance(error, InterruptedError) else "FAILED_NUMERICAL" if numerical and prior else "NUMERICAL_FAILURE" if numerical else "STOPPED_DEFECT"
        try:
            root.preflight()
            if out is not None and out.exists():
                (out / "failure.txt").write_text(repr(error) + "\n")
                report["failure_sha256"] = sha256(out / "failure.txt")
                report["retained_partial_relative"] = str(out.relative_to(root.root))
                if model is not None and optimizer is not None:
                    torch.save(portable(), out / "failed-state.pt")
                    report["failed_state_sha256"] = sha256(out / "failed-state.pt")
        except Exception as retention_error:
            report["failure_retention_error_type"] = type(retention_error).__name__
        report.update(status=status, exception_type=type(error).__name__, completed_updates=step,
                      latest_verified_checkpoint=latest, elapsed_seconds=time.perf_counter() - started,
                      disposition="EXACT_REPLAY_REQUIRED" if status == "NUMERICAL_FAILURE" else "GENERATION_2_EXECUTION_REPAIR_REQUIRED" if status == "STOPPED_DEFECT" else status)
        write(SAFE / f"scientific-outcome-{name}.attempt{attempt:02d}.json", report); lock.close()
        raise
    write(SAFE / f"scientific-outcome-{name}.attempt{attempt:02d}.json", report); lock.close()
    return report
