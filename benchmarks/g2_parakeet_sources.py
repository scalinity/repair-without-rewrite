"""Execute only the frozen source-construction calls; never teacher/student work."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import time

from src.data.g2_artifacts import ArtifactRoot, atomic_artifact, offline_model_environment, read_complete, sha256
from src.data.g2_corpus import bind_legacy, canonical_hash, check_audio_info, source_requests, text_hash, validate_census

REPO = Path(__file__).resolve().parents[1]
SPLITS = ("train-clean-100", "train-clean-360", "train-other-500", "dev-clean", "dev-other")


def append_durable(path, row):
    with Path(path).open("a") as stream:
        stream.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")
        stream.flush(); os.fsync(stream.fileno())


def run(binding, attempt, resume_relative=None):
    root = ArtifactRoot(binding)
    before = root.preflight()
    if attempt < 1:
        raise ValueError("positive source attempt required")
    receipt = Path(f"experiments/manifests/generation_2/parakeet-sources.attempt{attempt:02d}.json")
    if receipt.exists():
        raise FileExistsError(receipt)
    offline_model_environment()
    census_path = root.path("corpus-qualification-v1/candidate-census.attempt01.jsonl")
    census = [json.loads(line) for line in census_path.read_text().splitlines()]
    validate_census(census)
    admitted = {row["id"]: row for row in census}
    legacy = bind_legacy(census, [json.loads(line) for line in Path(
        "exports/foundation-repair/development-asr-pairs-attempt01/pairs.jsonl").read_text().splitlines()],
        json.loads(Path("exports/lexical-reader-v2/pilot-preparation-attempt01/development-panel.json").read_text()))
    request_path = Path("experiments/manifests/generation_2/parakeet-requests.attempt01.json")
    request_freeze = json.loads(request_path.read_text())
    requests = source_requests(census, legacy, json.loads(Path(
        "experiments/manifests/generation_2/parakeet-replay-selection.attempt01.json").read_text()))
    if requests != request_freeze["requests"] or canonical_hash(requests) != request_freeze["requests_sha256"]:
        raise ValueError("frozen source request identity changed")
    audio, inventories = {}, {}
    for split in SPLITS:
        directories = sorted(root.path("source-audio-v1").glob(split + ".attempt[0-9][0-9]"))
        if len(directories) != 1:
            raise ValueError("every required source split needs one completed native extraction")
        directory = directories[0]
        complete = read_complete(directory)
        inventory = json.loads((directory / "inventory.json").read_text())
        inventories[split] = complete["files"]["inventory.json"]["sha256"]
        for item in inventory:
            if item["id"] in audio:
                raise ValueError("duplicate native census recording")
            if (item["role"] != admitted[item["id"]]["role"]
                    or item["families"] != admitted[item["id"]]["families"]
                    or item["source_group_id"] != admitted[item["id"]]["source_group_id"]):
                raise ValueError("native source-role/family binding changed")
            audio[item["id"]] = (directory / (item["id"] + ".flac"), item)
    if audio.keys() != admitted.keys():
        raise ValueError("complete native census required before recognition")
    cfgpath = Path("experiments/manifests/asr_tts_probe/asr_book_closed_config.json")
    cfg = json.loads(cfgpath.read_text())["parakeet"]
    for asset in cfg["assets"]:
        if Path(asset["path"]).stat().st_size != asset["bytes"] or sha256(asset["path"]) != asset["sha256"]:
            raise ValueError("pinned Parakeet model asset changed")
    completed, inherited_journal_sha = [], None
    if resume_relative:
        resume = root.path(resume_relative)
        if resume.parent != root.path("asr-hypotheses-v1") or ".partial-" not in resume.name:
            raise ValueError("only retained source-construction staging journal can resume")
        prior = json.loads((resume / "start.json").read_text())
        if prior["requests_sha256"] != canonical_hash(requests) or prior["inventories"] != inventories:
            raise ValueError("source resume request/audio identities changed")
        journal = [json.loads(line) for line in (resume / "calls.jsonl").read_text().splitlines()]
        if len(journal) % 2:
            raise ValueError("interrupted in-flight recognizer call cannot be retried within the frozen one-call contract")
        for index in range(0, len(journal), 2):
            intent, result = journal[index:index + 2]
            expected = requests[index // 2]
            if (intent["event"] != "START" or result["event"] != "RESULT"
                    or intent["request"] != expected or result["request"] != expected
                    or result["status"] != "COMPLETED" or text_hash(result["source"]) != result["source_sha256"]):
                raise ValueError("failed/ambiguous source-call journal blocks census; no automatic rerun")
            completed.append(result)
        inherited_journal_sha = sha256(resume / "calls.jsonl")
    from src.data.parakeet_source import RUNTIME_ID
    report = {"schema": "g2_parakeet_construction_v1", "attempt": attempt,
        "qualification_id": f"G2-QUAL-PARAKEET-attempt{attempt:02d}", "seed": 42,
        "code_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "captured_dirty_status": subprocess.check_output(["git", "status", "--porcelain"], text=True),
        "dirty_diff_sha256": hashlib.sha256(subprocess.check_output(["git", "diff", "--binary"])).hexdigest(),
        "code_hashes": {name: sha256(name) for name in (str(Path(__file__).relative_to(REPO)),
            "src/data/parakeet_source.py", "src/data/g2_corpus.py", "src/data/g2_artifacts.py")},
        "config_sha256": sha256(cfgpath), "data_manifest_sha256": sha256(request_path),
        "requests_sha256": canonical_hash(requests), "inventories": inventories,
        "runtime_id": RUNTIME_ID, "runtime": {name: importlib.metadata.version(name)
            for name in ("mlx", "numpy", "parakeet-mlx", "soundfile")},
        "before": before, "maximum_calls": 15741, "completed_calls": len(completed),
        "inherited_completed_calls": len(completed), "inherited_journal_sha256": inherited_journal_sha,
        "legacy_train_sources_reused": 1024, "legacy_development_sources_reused": 108,
        "output_relative": f"asr-hypotheses-v1/construction.attempt{attempt:02d}",
        "resume_policy": "only exact durable START/RESULT pairs reused; an ambiguous or failed call blocks rather than reruns; staging journal never admitted as a completed corpus",
        "scientific_recipes_started": 0, "teacher_calls": 0, "tts_calls": 0, "status": "RUNNING"}
    started = time.perf_counter()
    unique = {row["request"]["id"]: row for row in completed if row["request"]["kind"] == "unique"}
    replay_checks = []
    try:
        with atomic_artifact(root, report["output_relative"]) as out:
            (out / "start.json").write_text(json.dumps(report, sort_keys=True) + "\n")
            with (out / "start.json").open("rb") as stream: os.fsync(stream.fileno())
            for item in completed:
                append_durable(out / "calls.jsonl", {"event": "START", "request": item["request"]})
                append_durable(out / "calls.jsonl", item)
            # All storage, corpus, asset and resume checks precede native model imports.
            import mlx.core as mx
            import soundfile as sf
            from parakeet_mlx import from_pretrained
            from src.data.parakeet_source import transcribe_development
            mx.random.seed(42)
            model = from_pretrained(cfg["snapshot"], dtype=mx.bfloat16)
            mx.eval(model.parameters()); mx.synchronize()
            for request in requests[len(completed):]:
                identifier = request["id"]
                path, item = audio[identifier]
                if sha256(path) != item["audio_sha256"]:
                    raise ValueError("native audio changed before source call")
                check_audio_info(sf.info(path))
                root.preflight()
                append_durable(out / "calls.jsonl", {"event": "START", "request": request})
                tick = time.perf_counter()
                result = {"event": "RESULT", "request": request, "audio_sha256": item["audio_sha256"]}
                try:
                    recognized = transcribe_development(model, path)
                    mx.synchronize()
                    result.update(status="COMPLETED", source=recognized.text,
                        source_sha256=text_hash(recognized.text), source_utf8_bytes=len(recognized.text.encode()))
                except Exception as error:
                    result.update(status="FAILED", source=None, source_sha256=None,
                        error_type=type(error).__name__, private_error=str(error))
                result["seconds"] = time.perf_counter() - tick
                append_durable(out / "calls.jsonl", result)
                completed.append(result)
                report["completed_calls"] = len(completed)
                if result["status"] != "COMPLETED":
                    raise ValueError("required frozen source call failed; ALL-OR-BLOCK")
                if request["kind"] == "unique":
                    unique[identifier] = result
                if len(completed) % 100 == 0:
                    print(json.dumps({"completed_calls": len(completed), "maximum_calls": 15741,
                        "elapsed_seconds": time.perf_counter() - started}), flush=True)
            if len(completed) != 15741 or len(unique) != 15677:
                raise ValueError("source construction census/call budget mismatch")
            for result in completed:
                if result["request"]["kind"] == "replay":
                    first = unique[result["request"]["id"]]
                    replay_checks.append({"id": result["request"]["id"],
                        "exact_utf8_match": first["source"] == result["source"],
                        "original_source_sha256": first["source_sha256"], "replay_source_sha256": result["source_sha256"]})
            (out / "replay.json").write_text(json.dumps(replay_checks, sort_keys=True) + "\n")
            if len(replay_checks) != 64 or not all(item["exact_utf8_match"] for item in replay_checks):
                raise ValueError("one-time source replay failed exact determinism")
            with (out / "pairs.jsonl").open("x") as stream:
                for row in census:
                    source = legacy[row["id"]]["source"] if row["id"] in legacy else unique[row["id"]]["source"]
                    stream.write(json.dumps({**row, "source": source, "source_sha256": text_hash(source),
                        "source_runtime": RUNTIME_ID, "status": "COMPLETED", "legacy_reused": row["id"] in legacy,
                        "audio_sha256": audio[row["id"]][1]["audio_sha256"]}, sort_keys=True) + "\n")
                stream.flush(); os.fsync(stream.fileno())
        final = root.path(report["output_relative"])
        report.update(status="PASS_SOURCE_CONSTRUCTION_ONLY", pairs_sha256=sha256(final / "pairs.jsonl"),
            calls_sha256=sha256(final / "calls.jsonl"), replay_sha256=sha256(final / "replay.json"),
            replay_checks=replay_checks, unique_hypotheses=15677, after=root.preflight())
    except BaseException as error:
        report.update(status="FAILED_ALL_OR_BLOCK", error_type=type(error).__name__)
        raise
    finally:
        report["elapsed_seconds"] = time.perf_counter() - started
        with receipt.open("x") as stream:
            json.dump(report, stream, indent=2, sort_keys=True); stream.write("\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-binding", required=True)
    parser.add_argument("--attempt", required=True, type=int)
    parser.add_argument("--resume-relative")
    args = parser.parse_args()
    result = run(args.artifact_binding, args.attempt, args.resume_relative)
    print(json.dumps({name: result[name] for name in ("status", "completed_calls", "elapsed_seconds")}), flush=True)
