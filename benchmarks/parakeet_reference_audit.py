"""CPU-only Parakeet feature audit against pinned official NeMo v2.4.0 code.

The reference source is supplied locally and retains its upstream license header.
Only its FilterbankFeatures, normalize_batch and splice_frames definitions run;
no NeMo installation, MLX import, model load, ASR call or unsafe memory read occurs.
NumPy reconstructions are independently written from the documented operations.
This proves feature-level facts, never full-model transcript equivalence.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import logging
import math
from pathlib import Path
import random
import subprocess
import time
from typing import Optional, Tuple, Union

import librosa
import numpy as np
import scipy.fft
import soundfile as sf
import torch
import torch.nn as nn

REFERENCE_COMMIT = "2381f42f6979449b5b99538f8f80135831009b51"
REFERENCE_URL = ("https://raw.githubusercontent.com/NVIDIA-NeMo/NeMo/"
                 + REFERENCE_COMMIT + "/nemo/collections/asr/parts/preprocessing/features.py")
REFERENCE_SHA256 = "cd25ac7919400771891bd6f0a6827c108c5472b9198aaed1b65824b13eeb0c9c"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def reference_extractor(source_path: Path):
    if sha(source_path) != REFERENCE_SHA256:
        raise ValueError("official reference source does not match reviewed bytes")
    source = ast.parse(source_path.read_bytes())
    definitions = [node for node in source.body
                   if isinstance(node, (ast.FunctionDef, ast.ClassDef))
                   and node.name in {"normalize_batch", "splice_frames", "FilterbankFeatures"}]
    if len(definitions) != 3:
        raise ValueError("unexpected official reference definitions")
    namespace = dict(globals(), CONSTANT=1e-5)
    exec(compile(ast.Module(body=definitions, type_ignores=[]), str(source_path), "exec"), namespace)
    return namespace["FilterbankFeatures"](
        sample_rate=16000, n_window_size=400, n_window_stride=160,
        window="hann", normalize="per_feature", n_fft=512, nfilt=128,
        dither=1e-5, pad_to=0, pad_value=0,
    ).eval()


def numpy_features(wave: np.ndarray, *, official: bool):
    """Use only safe frames; the legacy variant isolates its remaining math."""
    preemphasized = np.concatenate([wave[:1], wave[1:] - np.float32(.97) * wave[:-1]])
    padded = np.pad(preemphasized, (256, 256), mode="reflect")
    frames = np.lib.stride_tricks.sliding_window_view(padded, 512)[::160]
    if official:
        window = np.pad(np.hanning(400).astype(np.float32), (56, 56))
        guard, ddof = np.float32(2 ** -24), 1
    else:
        window = np.pad(np.hanning(401)[:-1].astype(np.float32), (0, 112))
        guard, ddof = np.float32(1e-5), 0
    spectrum = scipy.fft.rfft(frames * window, axis=-1)
    power = (spectrum.real ** 2 + spectrum.imag ** 2 if official
             else (np.abs(spectrum.real) + np.abs(spectrum.imag)) ** 2)
    mel = librosa.filters.mel(sr=16000, n_fft=512, n_mels=128, norm="slaney").astype(np.float32)
    logmel = np.log(mel @ power.T + guard)
    result = ((logmel - logmel.mean(axis=1, keepdims=True))
              / (logmel.std(axis=1, keepdims=True, ddof=ddof) + np.float32(1e-5)))
    return result, spectrum, window, padded, mel


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe-config", required=True, type=Path)
    parser.add_argument("--model-snapshot", required=True, type=Path)
    parser.add_argument("--reference-source", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    torch.set_num_threads(1)
    config = json.loads(args.probe_config.read_text())
    for asset in config["parakeet"]["assets"]:
        path = args.model_snapshot / Path(asset["path"]).name
        if sha(path) != asset["sha256"] or path.stat().st_size != asset["bytes"]:
            raise ValueError("changed pinned model asset: " + path.name)
    manifest_asset = config["public_audio_manifest"]
    manifest_path = Path(manifest_asset["path"])
    if sha(manifest_path) != manifest_asset["sha256"]:
        raise ValueError("changed development audio manifest")
    manifest = json.loads(manifest_path.read_text())
    if len(manifest["cases"]) != 12:
        raise ValueError("this audit requires the unchanged 12-case cohort")
    preprocessor = json.loads((args.model_snapshot / "config.json").read_text())["preprocessor"]
    expected = {"sample_rate": 16000, "window_size": .025, "window_stride": .01,
                "n_fft": 512, "window": "hann", "features": 128, "normalize": "per_feature",
                "dither": 1e-5, "pad_to": 0, "pad_value": 0, "log": True, "frame_splicing": 1}
    if any(preprocessor.get(key) != value for key, value in expected.items()):
        raise ValueError("unexpected pinned preprocessor contract")
    extractor = reference_extractor(args.reference_source)
    args.output_dir.mkdir(parents=True, exist_ok=False)
    import importlib.metadata
    receipt = {
        "scope": "CPU-only exact official preprocessor and safe NumPy reconstruction; no model inference",
        "reference_commit": REFERENCE_COMMIT, "reference_url": REFERENCE_URL,
        "reference_source_sha256": sha(args.reference_source), "script_sha256": sha(Path(__file__)),
        "probe_config_sha256": sha(args.probe_config), "manifest_sha256": sha(manifest_path),
        "pinned_model_asset_hashes_verified": True,
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "git_dirty": subprocess.check_output(["git", "status", "--short"], text=True),
        "versions": {name: importlib.metadata.version(name) for name in
                     ["torch", "numpy", "scipy", "librosa", "soundfile", "mlx", "parakeet-mlx"]},
        "all_input_cases": [], "six_case_comparison": [],
    }
    for index, case in enumerate(manifest["cases"]):
        path = Path(case["audio_relative_path"])
        info = sf.info(path)
        if sha(path) != case["audio_sha256"]:
            raise ValueError("changed audio bytes: " + path.stem)
        pcm = subprocess.run(
            ["ffmpeg", "-nostdin", "-i", str(path), "-threads", "0", "-f", "s16le",
             "-ac", "1", "-acodec", "pcm_s16le", "-ar", "16000", "-"],
            check=True, capture_output=True,
        ).stdout
        integers = np.frombuffer(pcm, dtype=np.int16)
        wave = integers.astype(np.float32) / np.float32(32768.0)
        alternative, sample_rate = sf.read(path, dtype="int16")
        n = len(wave)
        frames, legacy_frames = n // 160 + 1, (n + 512 - 400 + 160) // 160
        overrun = max(0, (legacy_frames - 1) * 160 + 512 - (n + 512))
        receipt["all_input_cases"].append({
            "case_id": path.stem, "audio_sha256": sha(path), "audio_hash_matches": True,
            "sample_rate": info.samplerate, "channels": info.channels, "subtype": info.subtype,
            "samples": n, "duration": n / 16000, "decoded_dtype": str(wave.dtype),
            "amplitude_min": float(wave.min()), "amplitude_max": float(wave.max()),
            "rms": float(np.sqrt(np.mean(wave ** 2))), "nonfinite_input": int((~np.isfinite(wave)).sum()),
            "ffmpeg_and_soundfile_int16_identical": bool(np.array_equal(integers, alternative)),
            "decoded_pcm_sha256": hashlib.sha256(pcm).hexdigest(),
            "nemo_safe_frames": frames, "legacy_declared_frames": legacy_frames,
            "legacy_logical_overrun": overrun,
        })
        if sample_rate != 16000 or info.channels != 1 or not np.array_equal(integers, alternative):
            raise ValueError("unexpected audio contract: " + path.stem)
        if index not in {0, 1, 3, 4, 5, 6}:
            continue
        start = time.perf_counter()
        with torch.no_grad():
            tensor, lengths = extractor(torch.from_numpy(wave)[None], torch.tensor([n]))
        seconds = time.perf_counter() - start
        actual = tensor[0].numpy()
        reference, *_ = numpy_features(wave, official=True)
        legacy, spectrum, window, padded, mel = numpy_features(wave, official=False)
        difference, legacy_difference = reference - actual, legacy - actual
        comparison = {
            "case_id": path.stem,
            "class": "pathological" if index in {3, 5} else "normal_affected" if index in {4, 6} else "normal_unaffected",
            "official_shape": list(actual.shape), "official_valid_frames": int(lengths[0]),
            "official_all_finite": bool(np.isfinite(actual).all()),
            "safe_legacy_all_finite": bool(np.isfinite(legacy).all()),
            "numpy_official_max_abs_error": float(np.abs(difference).max()),
            "numpy_official_rms_error": float(np.sqrt(np.mean(difference ** 2))),
            "safe_legacy_vs_official_max_abs": float(np.abs(legacy_difference).max()),
            "safe_legacy_vs_official_rms": float(np.sqrt(np.mean(legacy_difference ** 2))),
            "official_feature_cpu_seconds": seconds,
        }
        if actual.shape != (128, frames) or not np.isfinite(actual).all():
            raise ValueError("official CPU preprocessor failed on " + path.stem)
        if overrun:
            # Allocate the entire legacy-shaped region; NaNs are deliberate sentinels.
            extended = np.pad(padded, (0, overrun), constant_values=np.nan)
            views = np.lib.stride_tricks.sliding_window_view(extended, 512)[::160][:legacy_frames]
            with np.errstate(invalid="ignore"):
                fft = scipy.fft.rfft(views * window, axis=-1)
                power = (np.abs(fft.real) + np.abs(fft.imag)) ** 2
                logmel = np.log(mel @ power.T + np.float32(1e-5))
                normalized = ((logmel - logmel.mean(axis=1, keepdims=True))
                              / (logmel.std(axis=1, keepdims=True) + np.float32(1e-5)))
            comparison["deliberate_nan_sentinel_not_real_memory_read"] = {
                "nan_extension_samples": overrun,
                "nonfinite_fft_frames": int(np.any(~np.isfinite(fft), axis=1).sum()),
                "normalized_nonfinite_elements": int((~np.isfinite(normalized)).sum()),
                "normalized_total_elements": int(normalized.size),
            }
        receipt["six_case_comparison"].append(comparison)
    (args.output_dir / "reference_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"output_dir": str(args.output_dir), "receipt_sha256": sha(args.output_dir / "reference_receipt.json"),
                      "input_cases": len(receipt["all_input_cases"]), "reference_cases": len(receipt["six_case_comparison"])}))


if __name__ == "__main__":
    main()
