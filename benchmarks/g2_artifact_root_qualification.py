"""Bounded synthetic-only qualification on the actual bound external volume."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import time

from src.data.g2_artifacts import (ArtifactRoot, atomic_artifact, read_complete,
    replace_fixture_file, sha256, sync_directory)


def cold_readback(path):
    # Separate fresh process and separate implementation of completion checks.
    code = """import hashlib,json,os,sys
from pathlib import Path
p=Path(sys.argv[1]);m=json.loads((p/'COMPLETE.json').read_text())
assert '.partial-' not in p.name
assert set(m['files'])=={x.name for x in p.iterdir() if x.name!='COMPLETE.json'}
for name,expected in m['files'].items():
 q=p/name
 assert q.is_file() and not q.is_symlink() and q.stat().st_size==expected['bytes']
 with q.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==expected['sha256']
print(json.dumps({'status':'PASS','files':len(m['files']),'process':os.getpid()}))
"""
    started = time.perf_counter()
    output = subprocess.check_output([sys.executable, "-c", code, str(path)], text=True)
    result = json.loads(output)
    result["seconds"] = time.perf_counter() - started
    return result


def qualify(binding_path, receipt_path):
    root = ArtifactRoot(binding_path)
    initial = root.preflight()
    area = root.path("qualification-v1")
    area.mkdir(exist_ok=True)
    fixture = Path(tempfile.mkdtemp(prefix="storage-attempt01-", dir=area))
    relative = fixture.relative_to(root.root)
    result = {"schema": "g2_external_artifact_qualification_v1", "scope": "NON_SCIENTIFIC_SYNTHETIC_FIXTURES_ONLY",
        "initial_preflight": initial, "fixture_identity": hashlib.sha256(str(fixture).encode()).hexdigest(),
        "fixture_payloads_retained": False, "scientific_weights_used": False}
    try:
        block = bytes(range(256)) * 8192
        size = 2 * 1024**3
        started = time.perf_counter()
        with atomic_artifact(root, relative / "dense-checkpoint") as temporary:
            payload = temporary / "arrays.fixture"
            write_started = time.perf_counter()
            with payload.open("xb") as stream:
                for _ in range(size // len(block)):
                    stream.write(block)
                stream.flush()
                before_sync = time.perf_counter()
                os.fsync(stream.fileno())
                after_sync = time.perf_counter()
            (temporary / "metadata.json").write_text(json.dumps({"fixture": True, "scientific": False}))
        destination = root.path(relative / "dense-checkpoint")
        publication_seconds = time.perf_counter() - started
        payload = destination / "arrays.fixture"
        read_started = time.perf_counter()
        checksum = sha256(payload)
        read_seconds = time.perf_counter() - read_started
        result["dense_io"] = {"bytes": size, "sequential_write_seconds_before_fsync": before_sync - write_started,
            "file_fsync_seconds": after_sync - before_sync,
            "sequential_write_seconds_including_fsync": after_sync - write_started,
            "full_atomic_publication_seconds_including_hash_and_readback": publication_seconds,
            "read_seconds_including_sha256": read_seconds, "payload_sha256": checksum,
            "write_MiB_per_second_including_fsync": size / 2**20 / (after_sync - write_started),
            "read_MiB_per_second_including_sha256": size / 2**20 / read_seconds,
            "cold_device_cache_claimed": False}
        result["cold_readback"] = cold_readback(destination)
        sparse_size = 256 * 1024**2
        with atomic_artifact(root, relative / "sparse-checkpoint") as pending:
            with (pending / "sparse.fixture").open("xb") as stream:
                stream.write(b"start" + bytes(4091))
                stream.seek(sparse_size - 4096)
                stream.write(bytes(4093) + b"end")
            (pending / "metadata.json").write_text('{"synthetic_sparse":true}')
        sparse = root.path(relative / "sparse-checkpoint")
        stat = (sparse / "sparse.fixture").stat()
        result["sparse_fixture"] = {"logical_bytes": stat.st_size,
            "allocated_bytes": stat.st_blocks * 512, "fresh_process_readback": cold_readback(sparse)}
        result["directory_fsync"] = "PASS"
        interrupted = None
        try:
            with atomic_artifact(root, relative / "interrupted") as pending:
                interrupted = pending
                (pending / "arrays.fixture").write_bytes(b"unfinished")
                raise InterruptedError("dedicated fixture interruption")
        except InterruptedError:
            pass
        try:
            read_complete(interrupted)
            raise AssertionError("partial fixture accepted")
        except ValueError:
            result["incomplete_fixture_rejected"] = True
        assert not root.path(relative / "interrupted").exists()
        replacement = fixture / "replacement.fixture"
        old, new = b"a" * 8192, b"b" * 8192
        replacement.write_bytes(old)
        failures, observations = [], []
        stop = threading.Event()

        def observe():
            while not stop.is_set():
                try:
                    data = replacement.read_bytes()
                    if data not in (old, new):
                        failures.append("partial bytes")
                    observations.append(hashlib.sha256(data).hexdigest())
                except Exception as error:
                    failures.append(type(error).__name__)

        reader = threading.Thread(target=observe)
        reader.start()
        try:
            for index in range(32):
                replace_fixture_file(replacement, new if index % 2 == 0 else old)
        finally:
            stop.set()
            reader.join()
        assert observations and not failures
        result["atomic_replacement"] = {"replacements": 32, "reader_observations": len(observations),
            "partial_or_missing_observations": len(failures), "status": "PASS"}
        metadata = fixture / "small-files"
        metadata.mkdir()
        started = time.perf_counter()
        for index in range(128):
            with (metadata / f"{index:04}.fixture").open("xb") as stream:
                stream.write(block[:4096])
                stream.flush()
                os.fsync(stream.fileno())
        sync_directory(metadata)
        result["metadata_io"] = {"files": 128, "bytes_each": 4096,
            "write_fsync_directory_seconds": time.perf_counter() - started}
        missing_binding = fixture / "missing-root-binding.json"
        binding = json.loads(Path(binding_path).read_text())
        binding["root"] = str(fixture / "never-create-missing-root")
        missing_binding.write_text(json.dumps(binding))
        try:
            ArtifactRoot(missing_binding)
            raise AssertionError("missing root accepted")
        except FileNotFoundError:
            assert not Path(binding["root"]).exists()
            result["missing_root"] = {"status": "PASS", "simulation": "bound root absent; volume remains mounted",
                "models_initialized": 0, "network_calls": 0, "fallback_files_created": 0,
                "runner_integration": "separate future runner qualification required"}
        result["final_preflight"] = root.preflight()
        result["status"] = "PASS_STORAGE_PRIMITIVES_ONLY"
    except BaseException as error:
        result["status"] = "FAIL"
        result["error_type"] = type(error).__name__
        # Exact error/path text remains in the private launch log.
        raise
    finally:
        # Only the unique synthetic fixture directory created by this invocation.
        assert fixture.parent == area and fixture.name.startswith("storage-attempt01-")
        shutil.rmtree(fixture)
        result["dedicated_fixture_cleanup"] = "COMPLETE"
        result["free_after_fixture_cleanup"] = root.preflight()["literal_free_bytes"]
        with Path(receipt_path).open("x") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-binding", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    result = qualify(args.artifact_binding, args.receipt)
    print(json.dumps({"status": result["status"], "dense_io": result["dense_io"],
        "cold_readback": result["cold_readback"]}))
