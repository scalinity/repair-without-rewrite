"""Bounded, pinned public-development Parakeet and Kokoro native cost probes.

Each arm runs separately with an exclusive accelerator slot. No listening,
private audio, acoustic-truth certification or campaign forecast is performed.
"""
import argparse
from dataclasses import asdict
import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time
import traceback


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def rss_peak():
    # macOS reports bytes, not Linux's KiB.
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return {"process_peak_rss_bytes": value if sys.platform == "darwin" else value * 1024}


def parakeet(config, out):
    then = time.perf_counter()
    import mlx.core as mx
    from mlx.utils import tree_flatten
    from parakeet_mlx import from_pretrained, DecodingConfig
    import soundfile as sf
    imported = time.perf_counter() - then
    if not mx.metal.is_available():
        raise RuntimeError("Metal unavailable; this probe requires native Metal execution")
    mx.set_default_device(mx.gpu)
    spec = config["parakeet"]
    if spec.get("source_barrier_status") != "PASS_BOOK_PROJECT_DEVELOPMENT_CLOSURE":
        raise ValueError("ASR source barrier has not passed book/project development closure")
    audio_manifest = json.loads(Path(config["public_audio_manifest"]["path"]).read_text())
    cases = audio_manifest["cases"]
    if not 2 <= len(cases) <= 20 or len(cases) != spec["development_cases"] or len({case["speaker"] for case in cases}) != len(cases):
        raise ValueError("exact preselected 2–20-speaker development panel required")
    if audio_manifest["classification"] != "PUBLIC_DEVELOPMENT_AUDIO_ONLY_NOT_SEALED":
        raise ValueError("unqualified audio population")
    then = time.perf_counter()
    model = from_pretrained(spec["snapshot"], dtype=mx.bfloat16)
    mx.eval(model.parameters())
    mx.synchronize()
    load = time.perf_counter() - then
    weights = dict(tree_flatten(model.parameters()))
    memory = lambda: {"mlx_active_bytes": mx.get_active_memory(), "mlx_cache_bytes": mx.get_cache_memory(),
                      "mlx_peak_bytes": mx.get_peak_memory(), **rss_peak()}
    write_json(out / "load.json", {"runtime_import_seconds": imported, "load_materialized_seconds": load,
        "device": str(mx.default_device()), "metal_available": True,
        "weight_dtypes": sorted({str(v.dtype) for v in weights.values()}),
        "parameter_count": sum(v.size for v in weights.values()), "memory": memory()})
    rows = []
    with (out / "calls.jsonl").open("w", buffering=1) as stream:
        schedule = [("microprobe", i) for i in spec["microprobe_case_indices"]] + [("development", i) for i in range(len(cases))]
        for ordinal, (segment, index) in enumerate(schedule):
            case = cases[index]
            path = Path(case["audio_relative_path"])
            if sha(path) != case["audio_sha256"]:
                raise ValueError("changed public audio: " + str(path))
            info = sf.info(path)
            duration = info.frames / info.samplerate
            if not 2 <= duration <= 12:
                raise ValueError("public clip outside bounded duration")
            mx.synchronize()
            then = time.perf_counter()
            row = {"ordinal": ordinal, "segment": segment, "case_index": index,
                   "audio_relative_path": str(path), "audio_sha256": case["audio_sha256"],
                   "audio_seconds": duration, "speaker": case["speaker"],
                   "reference_text": case["text"], "reference_text_raw": case["text_raw"],
                   "reference_policy": case["reference_policy"]}
            try:
                result = model.transcribe(path, dtype=mx.bfloat16, decoding_config=DecodingConfig(), chunk_duration=None)
                mx.synchronize()
                row.update(status="COMPLETED", hypothesis=result.text, aligned_result=asdict(result))
            except Exception as error:
                mx.synchronize()
                row.update(status="FAILED", hypothesis=None, error_type=type(error).__name__,
                           error=str(error), traceback=traceback.format_exc())
            row["elapsed_seconds"] = time.perf_counter() - then
            row["real_time_factor"] = row["elapsed_seconds"] / duration
            row["memory"] = memory()
            stream.write(json.dumps(row, sort_keys=True) + "\n")
            rows.append(row)
            print(json.dumps({"arm": "parakeet", "segment": segment, "ordinal": ordinal, "status": row["status"]}), flush=True)
    dev = [row for row in rows if row["segment"] == "development"]
    return {"status": "COMPLETED_BOUNDED_DEV_PROBE" if all(r["status"] == "COMPLETED" for r in rows) else "PARTIAL_FAILURE",
            "microprobe_calls": len(spec["microprobe_case_indices"]), "development_attempts": len(cases),
            "development_target_quota": 20,
            "development_completed": sum(r["status"] == "COMPLETED" for r in dev),
            "development_audio_seconds": sum(r["audio_seconds"] for r in dev),
            "development_audio_hours": sum(r["audio_seconds"] for r in dev) / 3600,
            "development_elapsed_seconds": sum(r["elapsed_seconds"] for r in dev),
            "development_aggregate_RTF": sum(r["elapsed_seconds"] for r in dev) / sum(r["audio_seconds"] for r in dev),
            "first_call_seconds": rows[0]["elapsed_seconds"], "second_call_seconds": rows[1]["elapsed_seconds"],
            "runtime_import_seconds": imported, "load_materialized_seconds": load,
            "total_attempted_audio_seconds_including_repeats": sum(r["audio_seconds"] for r in rows),
            "memory": memory(), "interpretation": "preselected public DEV speakers; source errors scored separately under both supplied text policies"}


def kokoro(config, out):
    then = time.perf_counter()
    import torch
    import numpy as np
    import soundfile as sf
    from kokoro import KModel, KPipeline
    imported = time.perf_counter() - then
    spec = config["kokoro"]
    device = spec["device"]
    if device not in ("mps", "cpu"):
        raise ValueError("unsupported predeclared Kokoro device")
    if device == "mps" and not torch.backends.mps.is_available():
        raise RuntimeError("MPS unavailable; CPU rate will not be mislabeled as this MPS path")
    if device == "cpu":
        torch.set_num_threads(spec["cpu_threads"])
    synchronize = torch.mps.synchronize if device == "mps" else lambda: None
    assets = {Path(a["path"]).name: a["path"] for a in spec["assets"]}
    torch.manual_seed(config["seed"])
    then = time.perf_counter()
    # The official library offers this real-valued STFT implementation for
    # backends without complex operators; record its selection explicitly.
    model = KModel(repo_id=spec["repository"], config=assets["config.json"],
                   model=assets["kokoro-v1_0.pth"], disable_complex=spec["disable_complex"]).to(device).eval()
    pipeline = KPipeline(lang_code=spec["lang_code"], repo_id=spec["repository"], model=model, trf=False)
    voice = torch.load(assets["af_heart.pt"], map_location="cpu", weights_only=True)
    pipeline.voices[spec["voice"]] = voice
    if pipeline.g2p.fallback is None:
        raise RuntimeError("English OOD phoneme fallback unavailable; do not silently skip words")
    synchronize()
    load = time.perf_counter() - then
    memory = lambda: ({"mps_current_allocated_bytes": torch.mps.current_allocated_memory(),
                      "mps_driver_allocated_bytes": torch.mps.driver_allocated_memory(), **rss_peak()}
                     if device == "mps" else {"device": "cpu", **rss_peak()})
    write_json(out / "load.json", {"runtime_import_seconds": imported, "load_materialized_seconds": load,
        "device": str(model.device), "parameter_count": sum(p.numel() for p in model.parameters()),
        "parameter_dtypes": sorted({str(p.dtype) for p in model.parameters()}),
        "disable_complex": spec["disable_complex"], "cpu_threads": torch.get_num_threads(), "memory": memory()})
    rows = []
    audio_out = Path("exports/asr-tts-generated") / out.name
    audio_out.mkdir(parents=True, exist_ok=False)
    with (out / "calls.jsonl").open("w", buffering=1) as stream:
        for ordinal, text in enumerate(spec["intended_texts"]):
            synchronize()
            then = time.perf_counter()
            row = {"ordinal": ordinal, "intended_text": text,
                   "intended_text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                   "voice": spec["voice"], "speed": spec["speed"]}
            try:
                with torch.inference_mode():
                    pieces = list(pipeline(text, voice=spec["voice"], speed=spec["speed"]))
                synchronize()
                audio = np.concatenate([piece.audio.numpy() for piece in pieces])
                if not audio.size or not np.isfinite(audio).all():
                    raise ValueError("empty/nonfinite generated waveform")
                row.update(status="COMPLETED", audio_samples=int(audio.size),
                           audio_seconds=float(audio.size / spec["audio_sample_rate"]),
                           graphemes=[piece.graphemes for piece in pieces], phonemes=[piece.phonemes for piece in pieces])
                elapsed = time.perf_counter() - then
                target = audio_out / ("intended-%02d.wav" % ordinal)
                save_start = time.perf_counter()
                sf.write(target, audio, spec["audio_sample_rate"], subtype="FLOAT")
                row.update(audio_relative_path=str(target), audio_sha256=sha(target),
                           write_and_hash_seconds=time.perf_counter() - save_start,
                           real_time_factor=elapsed / row["audio_seconds"])
            except Exception as error:
                synchronize()
                elapsed = time.perf_counter() - then
                row.update(status="FAILED", error_type=type(error).__name__, error=str(error), traceback=traceback.format_exc())
            row["elapsed_seconds"] = elapsed
            row["memory"] = memory()
            stream.write(json.dumps(row, sort_keys=True) + "\n")
            rows.append(row)
            print(json.dumps({"arm": "kokoro", "ordinal": ordinal, "status": row["status"]}), flush=True)
    return {"status": "COMPLETED_BOUNDED_TTS_PROBE" if all(r["status"] == "COMPLETED" for r in rows) else "PARTIAL_FAILURE",
            "calls": len(rows), "completed": sum(r["status"] == "COMPLETED" for r in rows),
            "first_call_seconds": rows[0]["elapsed_seconds"], "second_call_seconds": rows[1]["elapsed_seconds"],
            "generated_audio_seconds": sum(r.get("audio_seconds", 0) for r in rows),
            "runtime_import_seconds": imported, "load_materialized_seconds": load,
            "memory": memory(), "interpretation": "2 intended-text timing probes; waveform content/quality and acoustic truth unverified"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--arm", choices=("parakeet", "kokoro"), required=True)
    args = parser.parse_args()
    process_start = time.perf_counter()
    config = json.loads(Path(args.manifest).read_text())
    if args.arm == "parakeet" and config["parakeet"].get("source_barrier_status") != "PASS_BOOK_PROJECT_DEVELOPMENT_CLOSURE":
        raise ValueError("ASR source barrier has not passed book/project development closure")
    input_assets = config[args.arm]["assets"]
    if args.arm == "parakeet":
        input_assets = input_assets + [config["public_audio_manifest"]]
    for asset in input_assets:
        if sha(asset["path"]) != asset["sha256"]:
            raise ValueError("changed pinned input: " + asset["path"])
    verification_seconds = time.perf_counter() - process_start
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "0"
    versions = {name: importlib.metadata.version(name) for name in (
        "mlx", "parakeet-mlx", "torch", "kokoro", "misaki", "en-core-web-sm", "numpy", "soundfile")}
    provenance = {"started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "arm": args.arm, "seed": config["seed"], "manifest_sha256": sha(args.manifest),
        "input_verification_seconds": verification_seconds,
        "script_sha256": sha(__file__), "runtime_wheels_sha256": sha("experiments/manifests/asr_tts_probe/runtime_wheels.json"),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "git_dirty": subprocess.check_output(["git", "status", "--porcelain=v1"], text=True),
        "python": sys.version, "platform": platform.platform(), "versions": versions,
        "network_during_calls": "HF/transformers offline; all model/voice/G2P assets local",
        "explicit_compile_calls": False, "memory_policy": "process peak RSS; device allocator metrics separately",
        "initial_power": subprocess.check_output(["pmset", "-g", "batt"], text=True),
        "initial_thermal": subprocess.check_output(["pmset", "-g", "therm"], text=True)}
    write_json(out / "provenance.json", provenance)
    try:
        summary = parakeet(config, out) if args.arm == "parakeet" else kokoro(config, out)
    except Exception as error:
        summary = {"status": "FAILED_LOAD_OR_RUNTIME", "error_type": type(error).__name__,
                   "error": str(error), "traceback": traceback.format_exc(), "memory": rss_peak()}
    summary["finished_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    summary["total_process_wall_seconds"] = time.perf_counter() - process_start
    write_json(out / "summary.json", summary)
    print(json.dumps(summary, sort_keys=True), flush=True)
    if summary["status"].startswith("FAILED") or summary["status"] == "PARTIAL_FAILURE":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
