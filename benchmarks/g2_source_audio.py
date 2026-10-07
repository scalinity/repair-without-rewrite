"""Extract only the frozen G2 census from verified official native archives."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import time

from src.data.g2_artifacts import ArtifactRoot, atomic_artifact, read_complete, sha256
from src.data.g2_corpus import check_audio_info, validate_census

REPO = Path(__file__).resolve().parents[1]
EXISTING = {
    "train-clean-100": ("exports/foundation-repair/train-clean-100-acquisition-attempt01/train-clean-100.tar.gz",
        6387309499, "2a93770f6d5c6c964bc36631d331a522", "d4ddd1d5a6ab303066f14971d768ee43278a5f2a0aa43dc716b0e64ecbbbf6e2"),
    "dev-clean": ("exports/public-audio-development/dev-clean.tar.gz", 337926286,
        "42e2234ba48799c1f50f24a7926300a1", "76f87d090650617fca0cac8f88b9416e0ebf80350acb97b343a85fa903728ab3"),
    "dev-other": ("exports/public-audio-development/dev-other.tar.gz", 314305928,
        "c8d0bcc9cca99d4f8b62fcc847357931", "12661c48e8c3fe1de2c1caa4c3e135193bfb1811584f11f569dd12645aa84365")}


def extract(binding, split, attempt):
    root = ArtifactRoot(binding)
    before = root.preflight()
    receipt = Path(f"experiments/manifests/generation_2/audio-{split}.attempt{attempt:02d}.json")
    if receipt.exists() or attempt < 1:
        raise FileExistsError("new positive audio extraction attempt required")
    census_path = root.path("corpus-qualification-v1/candidate-census.attempt01.jsonl")
    census = [json.loads(line) for line in census_path.read_text().splitlines()]
    validate_census(census)
    selected = {"LibriSpeech/" + row["audio_filepath"]: row
                for row in census if row["official_split"] == split}
    if not selected:
        raise ValueError("unknown/empty approved source split")
    if split in EXISTING:
        relative, size, md5, expected_sha = EXISTING[split]
        archive = Path(relative)
    else:
        specifications = json.loads(Path("configs/generation_2/source_archives_v1.json").read_text())["archives"]
        specification = next(item for item in specifications if item["name"] == split)
        finished = sorted(root.path("source-archives-v1").glob(split + ".attempt[0-9][0-9]"))
        if len(finished) != 1:
            raise ValueError("one verified completed source archive required")
        complete = read_complete(finished[0])
        archive = finished[0] / "native.tar.gz"
        size, md5 = specification["bytes"], specification["md5"]
        expected_sha = complete["files"]["native.tar.gz"]["sha256"]
    output_relative = f"source-audio-v1/{split}.attempt{attempt:02d}"
    provenance = {"schema": "g2_audio_extraction_provenance_v1",
        "qualification_id": f"G2-QUAL-AUDIO-{split}-attempt{attempt:02d}", "seed": None,
        "code_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "captured_dirty_status": subprocess.check_output(["git", "status", "--porcelain"], text=True),
        "dirty_diff_sha256": hashlib.sha256(subprocess.check_output(["git", "diff", "--binary"])).hexdigest(),
        "code_hashes": {name: sha256(name) for name in (str(Path(__file__).relative_to(REPO)),
            "src/data/g2_corpus.py", "src/data/g2_artifacts.py")},
        "config_sha256": sha256("configs/generation_2/source_archives_v1.json"),
        "data_manifest_sha256": sha256("experiments/manifests/generation_2/metadata-census.attempt01.jsonl"),
        "private_census_sha256": sha256(census_path), "selected_records": len(selected),
        "output_relative": output_relative, "before": before,
        "resume_policy": "immutable completed extraction reused; failed partial retained; new attempt required",
        "scientific_recipes_started": 0, "recognizer_calls": 0}
    private_start = root.path(f"logs-v1/audio-{split}-start.attempt{attempt:02d}.json")
    with private_start.open("x") as stream:
        json.dump(provenance, stream, sort_keys=True); stream.write("\n")
        stream.flush(); os.fsync(stream.fileno())
    start = time.perf_counter()
    report = {**provenance, "official_split": split,
        "official_url": f"https://www.openslr.org/resources/12/{split}.tar.gz",
        "status": "RUNNING", "source_archive_bytes": size, "expected_official_md5": md5}
    # Storage and all identities precede this native audio import.
    try:
        import soundfile as sf
        if archive.stat().st_size != size or sha256(archive) != expected_sha:
            raise ValueError("official native archive size/SHA256 mismatch")
        with archive.open("rb") as stream:
            if hashlib.file_digest(stream, "md5").hexdigest() != md5:
                raise ValueError("official native archive MD5 mismatch")
        report["archive_sha256"] = expected_sha
        inventory, seen = [], set()
        with atomic_artifact(root, output_relative) as output:
            with tarfile.open(archive, "r|gz") as tar:
                for member in tar:
                    if member.name not in selected:
                        continue
                    row = selected[member.name]
                    if not member.isfile() or row["id"] in seen or Path(row["id"]).name != row["id"]:
                        raise ValueError("duplicate/unsafe/nonregular required native member")
                    destination = output / (row["id"] + ".flac")
                    with tar.extractfile(member) as source, destination.open("xb") as stream:
                        shutil.copyfileobj(source, stream)
                        stream.flush(); os.fsync(stream.fileno())
                    info = sf.info(destination)
                    check_audio_info(info)
                    seen.add(row["id"])
                    inventory.append({"id": row["id"], "role": row["role"],
                        "source_group_id": row["source_group_id"], "families": row["families"],
                        "archive_member": member.name, "audio_bytes": destination.stat().st_size,
                        "audio_sha256": sha256(destination), "frames": info.frames,
                        "sample_rate": info.samplerate, "channels": info.channels,
                        "format": info.format, "subtype": info.subtype,
                        "manifest_duration_seconds": row["manifest_duration_seconds"]})
                    if len(seen) % 500 == 0:
                        root.preflight()
                        print(json.dumps({"split": split, "extracted": len(seen),
                            "elapsed_seconds": time.perf_counter() - start}), flush=True)
            if seen != {row["id"] for row in selected.values()}:
                raise ValueError("required census native archive member missing")
            (output / "inventory.json").write_text(json.dumps(inventory, sort_keys=True) + "\n")
        report.update(status="PASS_AUDIO_ONLY", extracted=len(inventory),
            audio_bytes=sum(row["audio_bytes"] for row in inventory),
            decoded_seconds=sum(row["frames"] for row in inventory) / 16000,
            inventory_sha256=sha256(root.path(output_relative) / "inventory.json"),
            elapsed_seconds=time.perf_counter() - start, after=root.preflight())
    except Exception as error:
        report.update(status="FAILED_ALL_OR_BLOCK", error_type=type(error).__name__,
            elapsed_seconds=time.perf_counter() - start)
        raise
    finally:
        with receipt.open("x") as stream:
            json.dump(report, stream, indent=2, sort_keys=True); stream.write("\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-binding", required=True)
    parser.add_argument("--split", required=True)
    parser.add_argument("--attempt", type=int, required=True)
    args = parser.parse_args()
    result = extract(args.artifact_binding, args.split, args.attempt)
    print(json.dumps({key: result[key] for key in ("status", "extracted", "elapsed_seconds")}), flush=True)
