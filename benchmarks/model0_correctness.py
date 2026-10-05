"""Bounded exact MODEL-0 qualification; never BENCH-00 or a language campaign.

Launch with MLX_ENABLE_TF32=0. Every attempted update is recorded. V6 is not
replaced by this synthetic screen. No final seed or external data is used.
"""
import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time

import mlx.core as mx
import mlx.nn as nn
from mlx.utils import tree_flatten
import numpy as np

from src.models.core import DecoderLM, ModelConfig, causal_loss, parameter_inventory
from src.models.training import Trainer, TokenSchedule, flat_parameters, save_checkpoint, load_checkpoint
from src.models.tokenizer import ByteBPE


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT/"docs/reports/raw/model0"


def sha_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parameter_hash(model):
    h = hashlib.sha256()
    for name, value in sorted(flat_parameters(model).items()):
        h.update(name.encode())
        h.update(np.asarray(value).tobytes())
    return h.hexdigest()


def evaluate(model, ids, dtype):
    logits = model(ids[:, :-1], dtype=dtype, backend="native")
    loss = causal_loss(model, ids, dtype=dtype, backend="native")/(ids.shape[0]*(ids.shape[1]-1))
    correct = mx.mean((mx.argmax(logits, axis=-1) == ids[:, 1:]).astype(mx.float32))
    mx.eval(loss, correct)
    return {"ce": float(loss.item()), "teacher_accuracy": float(correct.item())}


def fit(name, ids, seed, maximum, threshold, continuation=False):
    # This learning rate is for the explicit memorization test only, not the
    # paper recipe or a 10M development trial. Decay/dropout are disabled.
    trainer = Trainer(DecoderLM(seed=seed), TokenSchedule(maximum*ids.size, peak_lr=.003),
                      dtype=mx.bfloat16, backend="native", seed=seed,
                      optimizer_options={"weight_decay": 0.},
                      identities={"model": "MODEL-0", "data": hashlib.sha256(np.asarray(ids).tobytes()).hexdigest(),
                                  "tokenizer": "synthetic_token_id_cycle_no_trained_tokenizer"})
    initial_hash = parameter_hash(trainer.model)
    initial = evaluate(trainer.model, ids, mx.bfloat16)
    started, status, decoded = time.perf_counter(), "FAIL_BOUNDED_CEILING", None
    log_path = RAW/(name+"_steps.jsonl")
    if log_path.exists():
        raise FileExistsError("preserve previous attempt; choose a new output name")
    last = initial
    with log_path.open("w") as log:
        for step in range(1, maximum+1):
            step_start = time.perf_counter()
            # Ten unequal-shape-capable microsteps for the corpus; one for V4.
            for start in range(0, ids.shape[0], 4):
                trainer.accumulate(ids[start:start+4])
            update = trainer.update()
            update["elapsed_seconds"] = time.perf_counter()-step_start
            if step % 10 == 0 or step == maximum:
                last = evaluate(trainer.model, ids, mx.bfloat16)
                update.update(last)
                print(name, step, last, flush=True)
            log.write(json.dumps(update, sort_keys=True)+"\n")
            log.flush()
            if last["ce"] < threshold and last["teacher_accuracy"] >= .99:
                if continuation:
                    decoded = []
                    for row in np.asarray(ids):
                        output = trainer.model.greedy(mx.array(row[:8][None, :]), 32,
                            eos_id=258, dtype=mx.bfloat16, backend="native")["token_ids"]
                        decoded.append({"expected": row[8:40].tolist(), "actual": output,
                                        "match": output == row[8:40].tolist()})
                    if sum(x["match"] for x in decoded)/len(decoded) < .95:
                        last = {"ce": last["ce"], "teacher_accuracy": last["teacher_accuracy"]}
                        continue
                status = "PASS"
                break
    result = {"status": status, "seed": seed, "config": asdict(trainer.model.config),
              "parameters": 8621312, "initial_hash": initial_hash, "final_hash": parameter_hash(trainer.model),
              "data_sha256": trainer.identities["data"], "data_shape": list(ids.shape),
              "unique_fixture_tokens": int(ids.size), "processed_tokens": trainer.processed_tokens,
              "valid_targets_per_update": ids.shape[0]*(ids.shape[1]-1),
              "updates": trainer.optimizer.step, "maximum_updates": maximum,
              "initial": initial, "final": last, "elapsed_seconds": time.perf_counter()-started,
              "dtype_inventory": trainer.dtype_inventory(), "optimizer": trainer.optimizer.policy(),
              "schedule": asdict(trainer.schedule), "continuations": decoded,
              "timing_scope": "correctness_only; other CPU tasks may overlap; not BENCH-00"}
    if decoded is not None:
        result["continuation_fraction"] = sum(x["match"] for x in decoded)/len(decoded)
    (RAW/(name+".json")).write_text(json.dumps(result, sort_keys=True, indent=2)+"\n")
    return result


def exact_geometry_checks():
    model, ids = DecoderLM(), mx.array([[1, 2, 3, 4, 5, 6, 7, 8]])
    inventory = parameter_inventory(model)
    result = {"parameter_count": sum(x["count"] for x in inventory), "inventory": inventory,
              "config": asdict(model.config), "checks": {}}
    assert result["parameter_count"] == 8621312
    for dtype in (mx.float32, mx.bfloat16):
        dtype_name = str(dtype)
        ref, native = model(ids, dtype=dtype), model(ids, dtype=dtype, backend="native")
        atol, rtol = (1e-5, 1e-4) if dtype == mx.float32 else (.02, .02)
        np.testing.assert_allclose(np.asarray(ref.astype(mx.float32)), np.asarray(native.astype(mx.float32)), atol=atol, rtol=rtol)
        changed = model(mx.array([[1, 2, 3, 4, 20, 21, 22, 23]]), dtype=dtype, backend="native")
        np.testing.assert_array_equal(np.asarray(native[:, :4].astype(mx.float32)), np.asarray(changed[:, :4].astype(mx.float32)))
        caches, outputs = None, []
        for a, b in ((0, 1), (1, 4), (4, 8)):
            output, caches = model(ids[:, a:b], dtype=dtype, backend="native", caches=caches, return_cache=True)
            outputs.append(output)
        cached = mx.concatenate(outputs, axis=1)
        np.testing.assert_allclose(np.asarray(cached.astype(mx.float32)), np.asarray(native.astype(mx.float32)), atol=atol, rtol=rtol)
        valid_targets = ids.shape[0]*(ids.shape[1]-1)
        loss_ref, grad_ref = nn.value_and_grad(model, lambda m: causal_loss(m, ids, dtype=dtype)/valid_targets)(model)
        loss_nat, grad_nat = nn.value_and_grad(model, lambda m: causal_loss(m, ids, dtype=dtype, backend="native")/valid_targets)(model)
        discrepancies = {}
        for name, grad in tree_flatten(grad_ref):
            a, b = np.asarray(grad), np.asarray(dict(tree_flatten(grad_nat))[name])
            assert grad.dtype == mx.float32 and np.isfinite(a).all() and np.linalg.norm(a) > 0
            np.testing.assert_allclose(a, b, atol=atol, rtol=rtol)
            discrepancies[name] = {"max_abs": float(np.max(np.abs(a-b))),
                                   "direction_dot": float(np.sum(a*b)), "dtype": str(grad.dtype)}
            assert discrepancies[name]["direction_dot"] > 0
        result["checks"][dtype_name] = {"forward_max_abs": float(mx.max(mx.abs(ref.astype(mx.float32)-native.astype(mx.float32))).item()),
            "cache_max_abs": float(mx.max(mx.abs(cached.astype(mx.float32)-native.astype(mx.float32))).item()),
            "reference_loss": loss_ref.item(), "native_loss": loss_nat.item(), "gradients": discrepancies}
    result["status"] = "PASS"
    (RAW/"exact_geometry.json").write_text(json.dumps(result, sort_keys=True, indent=2)+"\n")
    return result


def resume_and_reproducibility(ids):
    options = {"dtype": mx.bfloat16, "backend": "native", "optimizer_options": {"weight_decay": 0.},
               "identities": {"model": "MODEL-0", "tokenizer": "synthetic_id_fixture", "dataset": sha_file(ROOT/"configs/model0.json")}}
    trainer = Trainer(DecoderLM(), TokenSchedule(100000, peak_lr=.003), **options)
    prelude = []
    for _ in range(4):
        trainer.accumulate(ids)
        prelude.append(trainer.update())
    trainer.data_order = [3, 0, 2, 1]
    checkpoint = ROOT/"checkpoints/model0_bounded_resume"
    save_started = time.perf_counter()
    manifest = save_checkpoint(trainer, checkpoint)
    save_seconds = time.perf_counter()-save_started
    control = []
    for _ in range(20):
        trainer.accumulate(ids)
        control.append(trainer.update())
    expected_hash, expected_cursor = parameter_hash(trainer.model), trainer.data_cursor
    resumed = Trainer(DecoderLM(seed=43), TokenSchedule(100000, peak_lr=.003), **options)
    load_started = time.perf_counter()
    load_checkpoint(resumed, checkpoint)
    load_seconds = time.perf_counter()-load_started
    actual = []
    for _ in range(20):
        resumed.accumulate(ids)
        actual.append(resumed.update())
    assert control == actual and parameter_hash(resumed.model) == expected_hash
    assert resumed.data_cursor == expected_cursor and resumed.data_order == [3, 0, 2, 1]
    same_seed_trajectories = []
    for _ in range(2):
        repeat = Trainer(DecoderLM(), TokenSchedule(100000, peak_lr=.003), **options)
        trajectory = []
        for _ in range(4):
            repeat.accumulate(ids)
            trajectory.append(repeat.update())
        same_seed_trajectories.append({"updates": trajectory, "final_hash": parameter_hash(repeat.model)})
    assert same_seed_trajectories[0] == same_seed_trajectories[1]
    result = {"status": "PASS", "geometry": "exact_MODEL0", "resumed_updates": 20,
              "control": control, "resumed": actual, "final_hash": expected_hash,
              "exact_parameter_and_loss_match": True, "checkpoint_manifest": manifest,
              "save_seconds": save_seconds, "load_seconds": load_seconds,
              "checkpoint_bytes": sum(x.stat().st_size for x in checkpoint.iterdir()),
              "same_seed_repeats": same_seed_trajectories,
              "processed_tokens_attempted_total": (4+20+20+4+4)*ids.size}
    (RAW/"resume_reproducibility.json").write_text(json.dumps(result, sort_keys=True, indent=2)+"\n")
    return result


def tokenizer_development_roundtrip():
    templates = ["Plain development prose {i}.", "--count={i}", "v3.12.{i}", "CamelCase{i}", "snake_case_{i}",
                 "kebab-case-{i}", "Homo sapiens {i}", "https://example.invalid/{i}", "/tmp/file_{i}.txt",
                 "C:\\Temp\\file_{i}.txt", "/command {i}", "-0.{i} percent", "${i}.00", "🙂👩‍🔬 {i}",
                 "e\u0301 é \r\n\t {i}", "a7b{i} <BOS> restore_reference"]
    strings = [templates[i % len(templates)].format(i=i) for i in range(10000)]
    train_strings = ["Training-only toy merge corpus paths paths words words 123 123 🙂🙂"]
    results = {}
    for isolate in (False, True):
        tokenizer = ByteBPE.train(train_strings, 16, digit_isolation=isolate)
        started, lengths, bytes_total = time.perf_counter(), [], 0
        for text in strings:
            encoded = tokenizer.encode(text)
            assert tokenizer.decode(encoded) == text
            assert not any(256 <= token <= 319 for token in encoded)
            lengths.append(len(encoded))
            bytes_total += len(text.encode("utf-8"))
        results[str(isolate)] = {"roundtrips": len(strings), "unintended_reserved_ids": 0,
            "vocab_size": tokenizer.vocab_size, "learned_merges": len(tokenizer.merges),
            "elapsed_seconds": time.perf_counter()-started, "tokens_per_utf8_byte": sum(lengths)/bytes_total,
            "tokens_p50": float(np.percentile(lengths, 50)), "tokens_p95": float(np.percentile(lengths, 95)),
            "over_1024": sum(x > 1024 for x in lengths),
            "category_lengths": {templates[c]: {"n": len(lengths[c::16]),
                "mean_tokens": float(np.mean(lengths[c::16]))} for c in range(16)}}
    results["status"] = "PASS_DEVELOPMENT_INTERFACE_ONLY"
    results["data_sha256"] = hashlib.sha256(json.dumps(strings, ensure_ascii=False).encode()).hexdigest()
    results["final_16k_tokenizer_status"] = "NOT_TRAINED; final corpus/merges not qualified"
    (RAW/"tokenizer_roundtrip.json").write_text(json.dumps(results, sort_keys=True, indent=2)+"\n")
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("v4", "remaining"), required=True)
    args = parser.parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    if os.environ.get("MLX_ENABLE_TF32") != "0":
        raise RuntimeError("launch with MLX_ENABLE_TF32=0; do not weaken FP32 tolerances")
    if not mx.metal.is_available():
        raise RuntimeError("native Metal required for this exact-model qualification")
    ids = mx.array(np.stack([(np.arange(64)+row*4) % 16 for row in range(4)]).astype(np.int32))
    identity = {"utc": datetime.now(timezone.utc).isoformat(), "stage": args.stage,
                "python": platform.python_version(), "mlx": mx.__version__, "default_device": str(mx.default_device()),
                "metal_device_info": mx.metal.device_info(), "MLX_ENABLE_TF32": os.environ["MLX_ENABLE_TF32"],
                "artifact_hashes": {str(p.relative_to(ROOT)): sha_file(p) for p in (
                    ROOT/"src/models/core.py", ROOT/"src/models/training.py", ROOT/"src/models/tokenizer.py",
                    ROOT/"configs/model0.json", Path(__file__))}}
    (RAW/(args.stage+"_identity.json")).write_text(json.dumps(identity, default=str, sort_keys=True, indent=2)+"\n")
    if args.stage == "v4":
        exact_geometry_checks()
        result = fit("v4_seed42", ids, 42, 2000, .05)
        print(json.dumps(result, sort_keys=True), flush=True)
        if result["status"] != "PASS":
            return 1
    else:
        previous = json.loads((RAW/"v4_seed42.json").read_text())
        if previous["status"] != "PASS":
            raise RuntimeError("V4 prerequisite not passed")
        resume = resume_and_reproducibility(ids)
        remaining_steps = (1000000-previous["processed_tokens"]-resume["processed_tokens_attempted_total"])//ids.size
        result = fit("v8_seed43", ids, 43, min(2000, remaining_steps), .05)
        corpus = mx.array((np.arange(2000).reshape(20, 100) % 64).astype(np.int32))
        memorization = fit("v5_seed42", corpus, 42, 5000, .1, continuation=True)
        tokenizer_development_roundtrip()
        print(json.dumps({"second_seed": result, "memorization": memorization}, sort_keys=True), flush=True)
        if result["status"] != "PASS" or memorization["status"] != "PASS":
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
