"""Official approved TRAIN archives, downloaded directly to bound G2 storage."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

from src.data.g2_artifacts import ArtifactRoot, atomic_artifact, read_complete, sha256

POLICY = Path(__file__).resolve().parents[1] / "configs/generation_2/source_archives_v1.json"


def verify_archive(path, specification):
    if Path(path).stat().st_size != specification["bytes"]:
        raise ValueError("official archive length mismatch")
    with Path(path).open("rb") as stream:
        md5 = hashlib.file_digest(stream, "md5").hexdigest()
    if md5 != specification["official_md5"]:
        raise ValueError("official archive MD5 mismatch")
    return {"bytes": Path(path).stat().st_size, "official_md5": md5, "sha256": sha256(path)}


def acquire(binding, attempt, receipt_path):
    root = ArtifactRoot(binding)  # before transport imports or artifact selection
    preflight = root.preflight()
    if Path(receipt_path).exists():
        raise FileExistsError(receipt_path)
    policy = json.loads(POLICY.read_text())
    if attempt < 1 or policy["missing_archive_total_bytes"] != 53642979491:
        raise ValueError("invalid acquisition attempt or approved archive inventory")
    if sum(x["bytes"] for x in policy["archives"]) != policy["missing_archive_total_bytes"]:
        raise ValueError("archive inventory sum mismatch")
    from urllib.request import urlopen
    record = {"schema": "g2_official_archive_acquisition_v1", "attempt": attempt,
        "qualification_id": f"G2-QUAL-SOURCE-ARCHIVES-attempt{attempt:02d}",
        "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "code_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "captured_dirty_status": subprocess.check_output(["git", "status", "--porcelain"], text=True),
        "dirty_diff_sha256": hashlib.sha256(subprocess.check_output(["git", "diff", "--binary"])).hexdigest(),
        "source_hashes": {"benchmarks/g2_source_archives.py": sha256(__file__),
            "src/data/g2_artifacts.py": sha256("src/data/g2_artifacts.py")},
        "config_sha256": sha256(POLICY),
        "data_manifest_sha256": sha256("experiments/manifests/generation_2/metadata-census.attempt01.jsonl"),
        "initial_preflight": preflight, "scientific_seed": None,
        "resume_policy": "reuse verified completed immutable archives; preserve failed partials; no overwrite or internal fallback",
        "archives": [], "recognizer_calls": 0, "scientific_recipes_started": 0}
    logdir = root.path("logs-v1")
    logdir.mkdir(exist_ok=True)
    private_start = logdir / f"archive-acquisition-start.attempt{attempt:02d}.json"
    with private_start.open("x") as stream:
        json.dump(record, stream, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    start = time.perf_counter()
    try:
        for specification in policy["archives"]:
            name = specification["name"]
            # Reuse only a verified completed prior attempt, never a partial.
            existing = sorted(root.path("source-archives-v1").glob(name + ".attempt[0-9][0-9]"))
            if existing:
                previous = existing[-1]
                read_complete(previous)
                identities = verify_archive(previous / (name + ".tar.gz"), specification)
                record["archives"].append({**specification, **identities, "status": "REUSED_VERIFIED_COMPLETE",
                    "artifact_relative_directory": str(previous.relative_to(root.root))})
                continue
            relative = f"source-archives-v1/{name}.attempt{attempt:02d}"
            print(json.dumps({"archive": name, "state": "STARTING", "expected_bytes": specification["bytes"]}), flush=True)
            begun = time.perf_counter()
            with atomic_artifact(root, relative) as pending:
                archive = pending / (name + ".tar.gz")
                digest, received = hashlib.md5(), 0
                with urlopen(specification["official_url"], timeout=60) as response, archive.open("xb") as output:
                    if response.url != specification["official_url"]:
                        raise ValueError("unexpected archive redirect; no mirror fallback authorized")
                    if int(response.headers.get("Content-Length", "-1")) != specification["bytes"]:
                        raise ValueError("official response length identity mismatch")
                    next_progress = 1024**3
                    while block := response.read(4 * 1024**2):
                        output.write(block)
                        digest.update(block)
                        received += len(block)
                        if received > specification["bytes"]:
                            raise ValueError("official archive exceeds frozen length")
                        if received >= next_progress:
                            root.preflight()
                            print(json.dumps({"archive": name, "received_bytes": received,
                                "seconds": time.perf_counter() - begun}), flush=True)
                            next_progress += 1024**3
                    output.flush()
                    os.fsync(output.fileno())
                if received != specification["bytes"] or digest.hexdigest() != specification["official_md5"]:
                    raise ValueError("official archive byte/checksum identity mismatch")
                identities = {"bytes": received, "official_md5": digest.hexdigest(), "sha256": sha256(archive)}
                archive_receipt = {**specification, **identities, "status": "PASS",
                    "seconds_before_publication": time.perf_counter() - begun}
                (pending / "acquisition.json").write_text(json.dumps(archive_receipt, indent=2) + "\n")
            record["archives"].append({**archive_receipt,
                "artifact_relative_directory": relative,
                "seconds_including_publication": time.perf_counter() - begun})
        record["status"] = "PASS_OFFICIAL_ARCHIVES_ONLY"
    except BaseException as error:
        record["status"] = "FAIL"
        record["error_type"] = type(error).__name__
        raise
    finally:
        record["elapsed_seconds"] = time.perf_counter() - start
        record["finished_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        record["final_preflight"] = root.preflight()
        with Path(receipt_path).open("x") as stream:
            json.dump(record, stream, indent=2)
            stream.write("\n")
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-binding", required=True)
    parser.add_argument("--attempt", type=int, required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    result = acquire(args.artifact_binding, args.attempt, args.receipt)
    print(json.dumps({"status": result["status"], "elapsed_seconds": result["elapsed_seconds"]}))
