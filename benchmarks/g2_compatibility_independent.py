"""Read-only reconstruction, independent of native training/comparison helpers."""
import argparse
import hashlib
import json
from pathlib import Path
import time

from src.data.g2_artifacts import ArtifactRoot


def reconstruct(binding, attempt):
    root = ArtifactRoot(binding)
    before = root.preflight()
    import numpy as np
    receipt = Path(f"experiments/manifests/generation_2/independent-compatibility.attempt{attempt:02d}.json")
    if receipt.exists():
        raise FileExistsError(receipt)
    started = time.perf_counter()
    result = {"schema": "g2_historical_artifact_reconstruction_v1", "before": before,
        "root_training_helpers_imported": False, "arms": {}, "source_code_sha256":
        hashlib.file_digest(Path(__file__).open("rb"), "sha256").hexdigest()}
    keys = ("arm", "update", "canonical_charge", "committed_canonical_exposure", "lr", "loss",
        "gradient_norm", "microsteps", "examples", "denominators", "presentation_ids", "actual_consumption")
    for arm in ("B100", "C101"):
        old = Path("exports/six-10m-probes") / (arm + "-seed42-lr3e-04") / "attempt01"
        new = root.path("compatibility-v1/" + arm + ".attempt02")
        original_steps = [json.loads(line) for line in (old / "updates.jsonl").open()][:31]
        actual_steps = [json.loads(line) for line in (new / "updates.jsonl").open()]
        if len(actual_steps) != 31:
            raise ValueError("complete historical control required")
        for original, actual in zip(original_steps, actual_steps):
            if any(original[key] != actual[key] for key in keys):
                raise ValueError("persisted historical native update mismatch")
            if actual["canonical_charge"] != sum(item["canonical_charge"] for item in actual["actual_consumption"]):
                raise ValueError("independent native exposure reconstruction failed")
        checkpoints = []
        for step, name in ((0, "initial"), (31, "endpoint-update031")):
            archive, current = old / f"checkpoint-update{step:03d}", new / name
            metadata = json.loads((archive / "metadata.json").read_text())
            observed = json.loads((current / "metadata.json").read_text())
            if any(metadata[key] != observed[key] for key in (
                    "reader_state", "committed_exposure", "optimizer_step", "forward_probe_sha256")):
                raise ValueError("independent historical state/reader mismatch")
            scalars = 0
            with np.load(archive / "arrays.npz", allow_pickle=False) as first, np.load(current / "arrays.npz", allow_pickle=False) as second:
                if set(first.files) != set(second.files):
                    raise ValueError("historical array inventory mismatch")
                for key in first.files:
                    left, right = first[key], second[key]
                    if left.shape != right.shape or left.dtype != right.dtype or left.tobytes() != right.tobytes():
                        raise ValueError("historical scalar bytes mismatch")
                    scalars += left.size
            digest = lambda path: hashlib.file_digest(path.open("rb"), "sha256").hexdigest()
            if digest(archive / "arrays.npz") != digest(current / "arrays.npz"):
                raise ValueError("historical serialized array bytes mismatch")
            checkpoints.append({"step": step, "scalars_compared_exactly": scalars,
                "arrays_sha256": digest(current / "arrays.npz"), "array_bytes_exact": True,
                "reader_exact": True, "forward_probe_exact": True})
        result["arms"][arm] = {"updates_compared_exactly": 31, "native_consumption_exact": True,
            "loss_denominators_lr_gradient_norm_exact": True, "checkpoints": checkpoints,
            "committed_exposure": actual_steps[-1]["committed_canonical_exposure"], "pass": True}
    result.update(status="PASS_EXACT_ARTIFACT_RECONSTRUCTION", scientific_recipes_started=0,
                  seconds=time.perf_counter() - started, after=root.preflight())
    with receipt.open("x") as stream:
        json.dump(result, stream, indent=2, sort_keys=True); stream.write("\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-binding", required=True)
    parser.add_argument("--attempt", required=True, type=int)
    args = parser.parse_args()
    print(json.dumps(reconstruct(args.artifact_binding, args.attempt)), flush=True)
