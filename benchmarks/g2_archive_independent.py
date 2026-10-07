"""Independent streaming official archive checksum reconstruction; no network."""
import argparse
import hashlib
import json
from pathlib import Path
import time

from src.data.g2_artifacts import ArtifactRoot, sha256


def run(binding, attempt):
    root = ArtifactRoot(binding)
    before = root.preflight()
    started = time.perf_counter()
    output = Path(f"experiments/manifests/generation_2/independent-archives.attempt{attempt:02d}.json")
    if output.exists():
        raise FileExistsError(output)
    config_path = Path("configs/generation_2/source_archives_v1.json")
    config = json.loads(config_path.read_text())
    report_path = Path("experiments/manifests/generation_2/source-archives.attempt01.json")
    report = json.loads(report_path.read_text())
    assert report["status"] == "PASS_OFFICIAL_ARCHIVES_ONLY" and report["config_sha256"] == sha256(config_path)
    result = []
    for expected in config["archives"]:
        original = next(row for row in report["archives"] if row["name"] == expected["name"])
        path = root.path(original["artifact_relative_directory"])
        assert path.is_dir() and not path.is_symlink() and ".partial-" not in path.name
        inventory = json.loads((path / "COMPLETE.json").read_text())
        payload = path / (expected["name"] + ".tar.gz")
        assert payload.is_file() and not payload.is_symlink() and payload.stat().st_size == expected["bytes"]
        md5 = hashlib.md5(usedforsecurity=False)
        digest = hashlib.sha256()
        count = 0
        with payload.open("rb") as stream:
            while block := stream.read(8 * 1024**2):
                count += len(block)
                md5.update(block)
                digest.update(block)
        assert count == expected["bytes"] == original["bytes"]
        assert md5.hexdigest() == expected["official_md5"] == original["official_md5"]
        assert digest.hexdigest() == original["sha256"] == inventory["files"][payload.name]["sha256"]
        assert inventory["files"][payload.name]["bytes"] == count
        result.append(dict(name=expected["name"],bytes=count,official_md5=md5.hexdigest(),sha256=digest.hexdigest(),status="PASS"))
    record = dict(schema="g2_independent_official_archives_v1",status="PASS_INDEPENDENT_OFFICIAL_ARCHIVES",
        method="one independent bounded-block full-byte MD5/SHA256 stream; no acquisition or completion reader imported",
        archives=result,total_bytes=sum(row["bytes"] for row in result),config_sha256=sha256(config_path),
        acquisition_receipt_sha256=sha256(report_path),before=before,after=root.preflight(),
        elapsed_seconds=time.perf_counter()-started,code_sha256=sha256(__file__),network_calls=0,scientific_recipes_started=0)
    output.write_text(json.dumps(record,sort_keys=True,indent=2)+"\n")
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-binding",required=True)
    parser.add_argument("--attempt",type=int,required=True)
    args = parser.parse_args()
    result = run(args.artifact_binding,args.attempt)
    print(json.dumps({"status":result["status"],"total_bytes":result["total_bytes"],"elapsed_seconds":result["elapsed_seconds"]}),flush=True)
