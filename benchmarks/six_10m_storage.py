"""Reclaim verified zero blocks without changing frozen checkpoint bytes."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import platform
import struct
import subprocess
import time
import zipfile


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while block := stream.read(1048576):
            digest.update(block)
    return digest.hexdigest()


def compact(checkpoint, receipt):
    checkpoint, receipt = Path(checkpoint), Path(receipt)
    if checkpoint.is_absolute() or ".." in checkpoint.parts or checkpoint.parts[0] != "exports":
        raise ValueError("checkpoint must be a repository-relative ignored artifact")
    temporary = receipt.with_suffix(receipt.suffix + ".partial")
    if platform.system() != "Darwin" or receipt.exists() or temporary.exists():
        raise ValueError("requires macOS and a new receipt path")
    source = checkpoint / "arrays.npz"
    expected = json.loads((checkpoint / "COMPLETE.json").read_text())["arrays.npz"]
    before = source.stat()
    if sha(source) != expected:
        raise ValueError("original does not match native checkpoint manifest")
    copy = source.with_name("arrays.npz.hole-partial")
    start = time.perf_counter()
    with source.open("rb") as reader, copy.open("xb") as writer:
        while block := reader.read(1048576):
            writer.write(block)
        writer.flush()
        os.fsync(writer.fileno())
    fd = os.open(copy, os.O_RDWR)
    runs, punched = 0, 0
    try:
        with source.open("rb") as reader:
            offset, zero_start = 0, None
            while block := reader.read(4096):
                zero = len(block) == 4096 and block.count(0) == 4096
                if zero and zero_start is None:
                    zero_start = offset
                if not zero and zero_start is not None:
                    length = offset - zero_start
                    # Installed macOS fcntl(2), F_PUNCHHOLE=99, fpunchhole_t.
                    fcntl.fcntl(fd, 99, struct.pack("=IIqq", 0, 0, zero_start, length))
                    runs += 1
                    punched += length
                    zero_start = None
                offset += len(block)
            if zero_start is not None:
                length = offset - zero_start
                fcntl.fcntl(fd, 99, struct.pack("=IIqq", 0, 0, zero_start, length))
                runs += 1
                punched += length
        os.fsync(fd)
    finally:
        os.close(fd)
    if copy.stat().st_size != before.st_size or sha(copy) != expected or sha(source) != expected:
        raise ValueError("storage operation changed logical checkpoint identity; original retained")
    with zipfile.ZipFile(copy) as archive:
        if archive.testzip() is not None:
            raise ValueError("NPZ entry CRC readback failed; original retained")
        entries = len(archive.infolist())
    os.chmod(copy, before.st_mode & 0o777)
    os.replace(copy, source)
    if sha(source) != expected:
        raise ValueError("published checkpoint identity changed")
    directory = os.open(checkpoint, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)
    after = source.stat()
    value = {"schema": "six10m_exact_checkpoint_storage_v1", "checkpoint": str(checkpoint),
        "utc_unix": time.time(), "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "helper_sha256": sha(Path(__file__)), "native_complete_sha256": sha(checkpoint / "COMPLETE.json"),
        "arrays_sha256": expected, "logical_bytes": after.st_size,
        "physical_bytes_before": before.st_blocks * 512, "physical_bytes_after": after.st_blocks * 512,
        "verified_zero_runs": runs, "verified_zero_bytes": punched, "npz_entries_crc_verified": entries,
        "wall_seconds": time.perf_counter() - start, "accelerator_used": False,
        "native_source_changed": False, "scientific_treatment_changed": False,
        "method": "verified copy; aligned all-zero F_PUNCHHOLE; SHA and full NPZ CRC readback; atomic same-path replacement",
        "disposition": "EXACT_CHECKPOINT_BYTES_PRESERVED"}
    receipt.parent.mkdir(parents=True, exist_ok=True)
    with temporary.open("x") as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.rename(temporary, receipt)
    print(json.dumps(value))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    compact(args.checkpoint, args.receipt)
