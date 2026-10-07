"""Exactly 31 inherited D0-U1 updates; no G2 scientific recipe launcher."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

from src.data.g2_artifacts import ArtifactRoot, atomic_artifact, offline_model_environment, sha256

REPO = Path(__file__).resolve().parents[1]
DETERMINISTIC_UPDATE_FIELDS = ("arm", "update", "canonical_charge", "committed_canonical_exposure",
    "lr", "loss", "gradient_norm", "microsteps", "examples", "denominators", "presentation_ids",
    "actual_consumption")
DETERMINISTIC_CHECKPOINT_FIELDS = ("schema", "arm", "config", "identities", "working_dtype", "backend",
    "optimizer_policy", "optimizer_step", "clock", "microbatch_size", "enforce_complete_target",
    "queue", "partition", "completed_microbatches", "denominators", "pending_charge",
    "committed_exposure", "loss", "accumulator_microbatches", "actual_consumption", "reader_state",
    "rng_policy", "shapes", "dtypes", "probe_variant_id", "forward_probe_sha256")


class HistoricalMismatch(ValueError):
    """A measured original/control scientific state mismatch."""


def differing_update_fields(observed, expected):
    # Compare the exact persisted contract. Dataclass tuples become JSON lists;
    # floats, labels, masks and every consumption record retain exact equality.
    encoded = lambda value: json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return [field for field in DETERMINISTIC_UPDATE_FIELDS if encoded(observed[field]) != encoded(expected[field])]


def save_control(root, relative, trainer, probe):
    from src.models.paired_training_v3 import save_paired_checkpoint
    with atomic_artifact(root, relative) as temporary:
        # The original serializer's readback/rebinding is preserved. Its inner
        # manifest has a distinct name within the G2 physical publication envelope.
        source = temporary / "native"
        save_paired_checkpoint(trainer, source, probe)
        for name in ("arrays.npz", "metadata.json"):
            os.rename(source / name, temporary / name)
        os.rename(source / "COMPLETE.json", temporary / "native-COMPLETE.json")
        source.rmdir()
    return root.path(relative)


def run(binding, arm, attempt):
    root = ArtifactRoot(binding)
    before = root.preflight()
    if arm not in {"B100", "C101"} or attempt < 1:
        raise ValueError("one bounded historical B100/C101 control required")
    receipt = Path(f"experiments/manifests/generation_2/compatibility-{arm}.attempt{attempt:02d}.json")
    if receipt.exists():
        raise FileExistsError(receipt)
    offline_model_environment()
    # All native/model imports follow the bound external-storage preflight.
    from benchmarks.paired_qualification_v3 import common, exact_queue, runtime_identities
    from benchmarks.six_10m_campaign import trainer_for, tensor_hash
    from src.models.paired_training_v3 import file_hash, validate_checkpoint_clock
    campaign_path = Path("experiments/manifests/six_10m_probes/campaign-freeze.attempt01.json")
    campaign = json.loads(campaign_path.read_text())
    if any(sha256(path) != expected for path, expected in campaign["source_hashes"].items()):
        raise ValueError("inherited G1 implementation changed")
    recipe = next(item for item in campaign["recipes"] if item["recipe_id"] == arm + "-seed42-lr3e-04")
    rows, ledger, updates, reader, data = common()
    if data != campaign["data_identities"]:
        raise ValueError("inherited D0 ledger changed")
    identities = runtime_identities(data)
    identities["campaign_sha256"] = sha256(campaign_path)
    identities["recipe_config_sha256"] = recipe["config_sha256"]
    if identities["runtime"] != campaign["runtime_identities"]["runtime"]:
        raise ValueError("historical native runtime identity changed")
    original = Path("exports/six-10m-probes") / recipe["recipe_id"] / "attempt01"
    original_checkpoints = {}
    for step in (0, 31):
        path = original / f"checkpoint-update{step:03d}"
        complete = json.loads((path / "COMPLETE.json").read_text())
        if any(file_hash(path / name) != digest for name, digest in complete.items()):
            raise ValueError("archived original checkpoint changed")
        meta = json.loads((path / "metadata.json").read_text())
        validate_checkpoint_clock(meta)
        original_checkpoints[step] = (path, complete, meta)
    expected_updates = {}
    with (original / "updates.jsonl").open() as stream:
        for line in stream:
            item = json.loads(line)
            if item["update"] <= 31:
                expected_updates[item["update"]] = item
    if set(expected_updates) != set(range(1, 32)):
        raise ValueError("all original 31 update records required")
    relative = f"compatibility-v1/{arm}.attempt{attempt:02d}"
    out = root.path(relative)
    if out.exists():
        raise FileExistsError(out)
    report = {"schema": "g2_historical_compatibility_v1", "arm": arm,
        "qualification_id": f"G2-QUAL-COMPATIBILITY-{arm}-attempt{attempt:02d}",
        "attempt": attempt, "seed": 42, "data_condition": "D0", "update_condition": "U1", "peak_lr": 3e-4,
        "code_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "captured_dirty_status": subprocess.check_output(["git", "status", "--porcelain"], text=True),
        "dirty_diff_sha256": hashlib.sha256(subprocess.check_output(["git", "diff", "--binary"])).hexdigest(),
        "code_hashes": {str(Path(__file__).relative_to(REPO)): sha256(__file__),
            "src/data/g2_artifacts.py": sha256("src/data/g2_artifacts.py")},
        "config_sha256": recipe["config_sha256"], "data_manifest_sha256": sha256(
            "experiments/manifests/generation_2/metadata-census.attempt01.jsonl"),
        "historical_campaign_sha256": sha256(campaign_path), "identities": identities,
        "output_relative": relative, "before": before, "completed_updates": 0, "checks": [],
        "scientific_recipes_started": 0, "qualification_weights_are_scientific_initializers": False,
        "deterministic_checkpoint_identity": "exact arrays.npz and the inherited scientific/optimizer/reader fields; host timings and unused process-global Python/NumPy RNG are separately retained in original metadata under the inherited explicit-model-key RNG policy",
        "resume_policy": "verified immutable external initial control snapshot; incomplete publications rejected; no automatic restart or recipe substitution",
        "status": "RUNNING"}
    # Create the area under the existing bound root, never recreate the root.
    out.parent.mkdir(exist_ok=True)
    out.mkdir()
    with (out / "start.json").open("x") as stream:
        json.dump(report, stream, sort_keys=True); stream.write("\n"); stream.flush(); os.fsync(stream.fileno())
    started = time.perf_counter()
    def compare_checkpoint(step, path):
        old_path, old_complete, old_meta = original_checkpoints[step]
        current = json.loads((path / "metadata.json").read_text())
        arrays_equal = sha256(path / "arrays.npz") == old_complete["arrays.npz"]
        differences = [field for field in DETERMINISTIC_CHECKPOINT_FIELDS if current[field] != old_meta[field]]
        check = {"step": step, "arrays_npz_exact": arrays_equal, "differing_state_fields": differences,
                 "original_arrays_sha256": old_complete["arrays.npz"], "control_arrays_sha256": sha256(path / "arrays.npz"),
                 "original_metadata_sha256": old_complete["metadata.json"], "control_metadata_sha256": sha256(path / "metadata.json")}
        report["checks"].append(check)
        if not arrays_equal or differences:
            raise HistoricalMismatch("historical deterministic checkpoint identity mismatch")
    try:
        trainer = trainer_for(arm, 3e-4, identities)
        initial = tensor_hash(trainer, "model::")
        if initial != campaign["models"][arm]["initial_parameter_sha256"]:
            raise HistoricalMismatch("historical seed42 initialization mismatch")
        trainer.reader_state = reader.state()
        first = save_control(root, relative + "/initial", trainer, rows[ledger[0]["variant_id"]])
        compare_checkpoint(0, first)
        report["verified_initial_snapshot_relative"] = relative + "/initial"
        with (out / "updates.jsonl").open("x") as stream:
            for index in range(31):
                queue = exact_queue(rows, ledger, updates[index], reader)
                observed = trainer.update(queue, reader.state())
                expected = expected_updates[index + 1]
                different = differing_update_fields(observed, expected)
                observed["historical_differing_fields"] = different
                stream.write(json.dumps(observed, sort_keys=True, allow_nan=False) + "\n")
                stream.flush(); os.fsync(stream.fileno())
                report["completed_updates"] = index + 1
                if different:
                    report["first_mismatch"] = {"update": index + 1, "fields": different,
                        "expected_loss": expected["loss"], "observed_loss": observed["loss"]}
                    raise HistoricalMismatch("historical exact native update mismatch")
                if (index + 1) % 5 == 0:
                    root.preflight()
                    print(json.dumps({"arm": arm, "updates": index + 1,
                        "elapsed_seconds": time.perf_counter() - started}), flush=True)
        final = save_control(root, relative + "/endpoint-update031", trainer, rows[ledger[0]["variant_id"]])
        compare_checkpoint(31, final)
        expected = json.loads((original / "checkpoint-update031-receipt.json").read_text())
        report["parameter_sha256"] = tensor_hash(trainer, "model::")
        report["optimizer_sha256"] = {name: tensor_hash(trainer, name + "::") for name in ("m", "v")}
        if (report["parameter_sha256"] != expected["parameter_sha256"]
                or report["optimizer_sha256"] != expected["optimizer_sha256"]
                or trainer.reader_state != original_checkpoints[31][2]["reader_state"]):
            raise HistoricalMismatch("historical parameter/optimizer/reader endpoint mismatch")
        report.update(status="PASS_EXACT_HISTORICAL_COMPATIBILITY", committed_exposure=trainer.committed_exposure,
            updates_sha256=sha256(out / "updates.jsonl"), after=root.preflight())
    except Exception as error:
        report.update(status="FRONTIER_MODEL_REVIEW_REQUIRED" if isinstance(error, (HistoricalMismatch,
            FloatingPointError)) else "GENERATION_2_QUALIFICATION_REPAIR_REQUIRED", error_type=type(error).__name__)
        raise
    finally:
        report["elapsed_seconds"] = time.perf_counter() - started
        with (out / "result.json").open("x") as stream:
            json.dump(report, stream, indent=2, sort_keys=True); stream.write("\n"); stream.flush(); os.fsync(stream.fileno())
        with receipt.open("x") as stream:
            json.dump(report, stream, indent=2, sort_keys=True); stream.write("\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-binding", required=True)
    parser.add_argument("--arm", choices=("B100", "C101"), required=True)
    parser.add_argument("--attempt", type=int, required=True)
    args = parser.parse_args()
    result = run(args.artifact_binding, args.arm, args.attempt)
    print(json.dumps({name: result[name] for name in ("status", "arm", "completed_updates", "elapsed_seconds")}), flush=True)
