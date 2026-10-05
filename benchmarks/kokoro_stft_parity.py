"""Replay the preserved isolated Kokoro original/alternate inverse-STFT check.

Original receipt used --device mps --phase-bound 3.14. The generator-domain
follow-up used --device cpu --phase-bound 1. The program was saved after those
inline checks; it does not claim a pre-execution code hash for those receipts.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    parser.add_argument("--device", choices=("cpu", "mps"), required=True)
    parser.add_argument("--phase-bound", type=float, choices=(1.0, 3.14), required=True)
    args = parser.parse_args()
    if Path(args.out).exists():
        raise FileExistsError("preserve original parity receipt")
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "0"
    import torch
    from kokoro.istftnet import TorchSTFT
    from kokoro.custom_stft import CustomSTFT
    then = time.perf_counter()
    rng = torch.Generator(device="cpu").manual_seed(42)
    reference = TorchSTFT(filter_length=20, hop_length=5, win_length=20)
    alternate = CustomSTFT(filter_length=20, hop_length=5, win_length=20)
    native = CustomSTFT(filter_length=20, hop_length=5, win_length=20).to(args.device)
    rows = []
    for frames in (20, 128):
        magnitude = torch.rand((1, 11, frames), generator=rng) + .1
        phase = torch.rand((1, 11, frames), generator=rng) * (2 * args.phase_bound) - args.phase_bound
        with torch.inference_mode():
            expected = reference.inverse(magnitude, phase)
            actual = alternate.inverse(magnitude, phase)
            device_actual = native.inverse(magnitude.to(args.device), phase.to(args.device)).cpu()
        if args.device == "mps":
            torch.mps.synchronize()
        rows.append({"frames": frames,
            "original_vs_alternate_max_abs": float((expected - actual).abs().max()),
            "reference_rms": float(torch.sqrt((expected * expected).mean())),
            "alternate_rms": float(torch.sqrt((actual * actual).mean())),
            "alternate_CPU_vs_device_max_abs": float((actual - device_actual).abs().max()),
            "original_path_allclose_atol_rtol_1e-4": bool(torch.allclose(expected, actual, atol=1e-4, rtol=1e-4)),
            "alternate_device_allclose_atol_rtol_1e-4": bool(torch.allclose(actual, device_actual, atol=1e-4, rtol=1e-4))})
    result = {"status": "PASS" if all(r["original_path_allclose_atol_rtol_1e-4"] and
                r["alternate_device_allclose_atol_rtol_1e-4"] for r in rows) else "FAIL_ORIGINAL_PATH_EQUIVALENCE",
        "seed": 42, "device": args.device, "phase_range": [-args.phase_bound, args.phase_bound],
        "geometry": {"n_fft": 20, "hop": 5, "window": 20}, "rows": rows,
        "scope": "isolated inverse STFT; no model generation or whole-waveform parity claim",
        "elapsed_seconds": time.perf_counter() - then,
        "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    Path(args.out).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True), flush=True)
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
