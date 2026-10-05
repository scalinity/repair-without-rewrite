"""Same-cohort numerical localization and explicitly identified frame repair."""
import argparse
from dataclasses import asdict
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import time

import numpy as np

from benchmarks.asr_tts_native_probe import sha, validate_asr_source_barrier


def stats(x):
    import mlx.core as mx
    if x.dtype == mx.complex64:
        x = mx.view(x, mx.float32)
    value = np.asarray(x.astype(mx.float32))
    good = np.isfinite(value)
    return {"shape": list(x.shape), "dtype": str(x.dtype),
            "nonfinite": int((~good).sum()), "elements": int(value.size),
            "sha256": hashlib.sha256(value.tobytes()).hexdigest(),
            "min_finite": float(value[good].min()) if good.any() else None,
            "max_finite": float(value[good].max()) if good.any() else None}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--mode", choices=["localize", "repaired"], required=True)
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    cfgpath = Path("experiments/manifests/asr_tts_probe/asr_book_closed_config.json")
    cfg = json.loads(cfgpath.read_text())
    barrier = validate_asr_source_barrier(cfg)
    for asset in cfg["parakeet"]["assets"]:
        if sha(asset["path"]) != asset["sha256"]:
            raise ValueError("changed model asset")
    provenance = {"head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_status": subprocess.check_output(["git", "status", "--porcelain"], text=True),
        "dirty_diff": subprocess.check_output(["git", "diff", "--binary"], text=True),
        "hashes": {p: sha(p) for p in (str(cfgpath), __file__, "src/data/parakeet_source.py")},
        "config": {"mode": args.mode, "seed": 42, "model": cfg["parakeet"],
                   "single_item": True, "chunking": False, "model_dtype": "bfloat16"},
        "versions": {p: importlib.metadata.version(p) for p in ("mlx", "parakeet-mlx", "numpy", "soundfile")},
        "source_barrier": barrier}
    (out / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    import mlx.core as mx
    import parakeet_mlx.audio as audio
    from parakeet_mlx import from_pretrained
    from src.data.parakeet_source import transcribe_development, RUNTIME_ID
    model = from_pretrained(cfg["parakeet"]["snapshot"], dtype=mx.bfloat16)
    mx.eval(model.parameters())
    cases = json.loads(Path(cfg["public_audio_manifest"]["path"]).read_text())["cases"]
    rows = []
    with (out / "records.jsonl").open("w", buffering=1) as stream:
        schedule = [3,5,4,6,0,1] if args.mode == "localize" else list(range(12)) * 2
        for ordinal, index in enumerate(schedule):
            c = cases[index]
            begin = time.perf_counter()
            row = {"ordinal": ordinal, "case_index": index, "audio_sha256": c["audio_sha256"],
                   "id": Path(c["audio_filepath"]).stem, "mode": args.mode}
            if args.mode == "localize":
                x = audio.load_audio(Path(c["audio_relative_path"]), 16000)
                row["waveform"] = stats(x)
                fft = mx.fft.rfft
                def traced_fft(value, *a, **kw):
                    row["windowed_fft_input"] = stats(value)
                    result = fft(value, *a, **kw)
                    row["fft"] = stats(result)
                    return result
                mx.fft.rfft = traced_fft
                try:
                    mel = audio.get_logmel(x, model.preprocessor_config)
                finally:
                    mx.fft.rfft = fft
                row["logmel"] = stats(mel)
                features, lengths = model.encoder(mel)
                row["encoder"] = stats(features)
                decoder, _ = model.decoder(None)
                row["decoder_initial"] = stats(decoder)
                logits = model.joint(features[:,:1], decoder.astype(features.dtype))
                row["joint_initial"] = stats(logits)
                row["token_argmax"] = int(mx.argmax(logits[0,0,:,:len(model.vocabulary)+1]))
                row["duration_argmax"] = int(mx.argmax(logits[0,0,:,len(model.vocabulary)+1:]))
                row["encoder_lengths"] = np.asarray(lengths).tolist()
            else:
                result = transcribe_development(model, Path(c["audio_relative_path"]))
                row.update(runtime_id=RUNTIME_ID, hypothesis=result.text, aligned_result=asdict(result),
                           confidence_finite=all(np.isfinite(t.confidence) for t in result.tokens),
                           pure_unk=bool(result.text) and result.text.replace("<unk>", "") == "")
            mx.synchronize()
            row["seconds"] = time.perf_counter() - begin
            row["peak_mlx_bytes"] = mx.get_peak_memory()
            stream.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")
            rows.append(row)
            print(json.dumps({k: row[k] for k in ("id", "mode", "seconds")}), flush=True)
    (out / "summary.json").write_text(json.dumps({"mode": args.mode, "calls": len(rows),
        "seconds": sum(r["seconds"] for r in rows), "runtime_id": RUNTIME_ID,
        "cohort": "same preselected twelve; no replacements", "records_sha256": sha(out/"records.jsonl")}, indent=2)+"\n")


if __name__ == "__main__":
    main()
