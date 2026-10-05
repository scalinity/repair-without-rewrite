"""Train and qualify a DEVELOPMENT tokenizer from hash-admitted train rows only."""
import hashlib
import argparse
import json
from pathlib import Path
import random
import subprocess
import tarfile
import time

from src.models.tokenizer import ByteBPE, SPECIAL_TOKENS, frame_source
from src.models.tokenizer_training import train_development_byte_bpe


def sha(path):
    return hashlib.file_digest(Path(path).open("rb"), "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempt", required=True)
    args = parser.parse_args()
    out = Path("exports/foundation-repair") / ("development-tokenizer-" + args.attempt)
    out.mkdir(parents=True, exist_ok=False)
    roles_path = Path("experiments/manifests/public_lspc_training_roles.development.jsonl")
    qualification_path = Path("experiments/manifests/public_lspc_training_supply_qualification.json")
    roles = [json.loads(s) for s in roles_path.read_text().splitlines()]
    qualification = json.loads(qualification_path.read_text())
    if qualification["manifest_sha256"] != sha(roles_path):
        raise ValueError("training role/qualification hash mismatch")
    admitted = {r["id"]: r for r in roles if r["role"] == "train"}
    if not admitted or any(r["reference_field"] != "text_raw" for r in admitted.values()):
        raise ValueError("no admitted raw-reference train corpus")
    archive = Path("exports/source-qualification/ls_pc_manifest.tar.gz")
    if sha(archive) != "96d4eae2222b29b66437a21959252419bcd4762e5042e71e023790171054d1c0":
        raise ValueError("changed official reference archive")
    texts = {}
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            if not member.name.endswith(".json") and not member.name.endswith(".jsonl"):
                continue
            # No DEV/final payload is read by this training runner.
            if not any(s in member.name for s in ("train-clean-100", "train-clean-360", "train-other-500")):
                continue
            for line in tar.extractfile(member):
                row = json.loads(line)
                identifier = Path(row["audio_filepath"]).stem
                if identifier not in admitted:
                    continue
                role = admitted[identifier]
                for field, key in (("text", "text_sha256"), ("text_raw", "text_raw_sha256")):
                    if hashlib.sha256(row[field].encode()).hexdigest() != role[key]:
                        raise ValueError("target identity mismatch")
                texts[identifier] = row["text_raw"]
    if texts.keys() != admitted.keys():
        raise ValueError("missing/duplicate admitted training target")
    manifest = Path("experiments/manifests/development_tokenizer_corpus.attempt01.jsonl")
    if manifest.exists():
        raise FileExistsError("preserve previous attempt")
    with manifest.open("w") as f:
        for identifier in sorted(texts):
            r = admitted[identifier]
            f.write(json.dumps({"id": identifier, "source_group_id": r["source_group_id"],
                "role": "train", "field": "text_raw", "sha256": r["text_raw_sha256"],
                "utf8_bytes": len(texts[identifier].encode())}, sort_keys=True)+"\n")
    lineage = {"head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_status": subprocess.check_output(["git", "status", "--porcelain"], text=True),
        "dirty_diff": subprocess.check_output(["git", "diff", "--binary"], text=True),
        "code_hashes": {p: sha(p) for p in (__file__, "src/models/tokenizer.py", "src/models/tokenizer_training.py")},
        "roles_sha256": sha(roles_path), "supply_qualification_sha256": sha(qualification_path),
        "corpus_manifest_sha256": sha(manifest), "archive_sha256": sha(archive),
        "seed": None, "source_components": len({r["source_group_id"] for r in admitted.values()}),
        "role_admission": "only train rows; reserved calibration and official HPO not read or fitted"}
    (out / "launch.json").write_text(json.dumps(lineage, indent=2)+"\n")
    start = time.perf_counter()
    tokenizer, receipt = train_development_byte_bpe((texts[k] for k in sorted(texts)),
        training_manifest_sha256=sha(manifest))
    receipt.update(lineage=lineage, trainer_seconds=time.perf_counter()-start)
    if tokenizer.vocab_size != 16384 or len(tokenizer.merges) != 16064:
        raise ValueError("incomplete canonical vocabulary")
    artifact = Path("configs/tokenizer_development")
    if artifact.exists():
        raise FileExistsError("preserve prior artifact")
    receipt["artifact_hashes"] = tokenizer.save(artifact, sha(manifest))
    reloaded = ByteBPE.load(artifact)
    fixtures = ["e\u0301", "é", "👨‍👩‍👧‍👦", "/usr/local/a_b/../c", "https://example.org/a?q=x#y",
        "--no-cache --version=3.12.4", "snake_case", "CamelCase", "  a   b  ",
        "<restore_reference><PAD><extra_id_0>\r\n\t", "", "a\x00b", "C:\\Users\\Example\\a.txt"]
    rng = random.Random(120202)
    alphabet = "abcABC_-/ 0123456789é中🙂\u0301\n\r\t<>=."
    fixtures += ["".join(rng.choices(alphabet, k=rng.randrange(1,96))) for _ in range(10000-len(fixtures))]
    start = time.perf_counter()
    lengths = []
    for value in fixtures:
        ids = reloaded.encode(value)
        assert reloaded.decode(ids) == value
        assert not any(i in SPECIAL_TOKENS for i in ids)
        source = reloaded.source(value)
        assert source.byte_offsets[-1] == len(value.encode())
        lengths.append(len(ids))
    for control in (True, 308.0, "308", None, 320, -1):
        try:
            frame_source(reloaded, "literal", control)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid control accepted")
    receipt.update(roundtrip_count=len(fixtures), roundtrip_failures=0, unintended_reserved_ids=0,
        invalid_control_attempts_rejected=6, roundtrip_seconds=time.perf_counter()-start,
        fixture_sha256=hashlib.sha256(json.dumps(fixtures, ensure_ascii=False).encode()).hexdigest(),
        seed_order_policy="no trainer randomness; documents sorted stable ID; fixture seed120202",
        status="QUALIFIED_DEVELOPMENT_TOKENIZER_FROZEN_BY_HASH_NOT_PAPER_FREEZE")
    # This separate receipt is the development freeze; the unchanged artifact
    # schema's historical DEVELOPMENT_NOT_FROZEN label is not a paper freeze.
    (out/"receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True)+"\n")
    print(json.dumps({k:receipt[k] for k in ("status", "vocab_size", "training_utf8_bytes", "input_documents", "trainer_seconds", "roundtrip_count", "artifact_hashes")}))


if __name__ == "__main__":
    main()
