"""Inventory an already acquired official LS-PC text archive without decoding audio."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path, PurePosixPath
import tarfile

from src.data.contracts import canonical_hash, make_role_manifest, reference_status, sha256_bytes


def inventory_lspc(archive: Path) -> tuple[dict, list[dict]]:
    summary, selected = {}, []
    archive_sha256 = sha256_bytes(archive.read_bytes())
    with tarfile.open(archive, "r:gz") as tar:
        for member in sorted(tar.getmembers(), key=lambda x: x.name):
            if not member.name.endswith(".json") or "/" in member.name:
                continue
            split = member.name.removesuffix(".json")
            data = tar.extractfile(member).read()
            rows = [json.loads(line) for line in data.splitlines() if line]
            seen = set()
            speakers, chapters = set(), set()
            n_empty, n_differences, seconds = 0, 0, 0.
            for row in rows:
                path = PurePosixPath(row["audio_filepath"])
                sid, chapter, uid = path.parts[-3], path.parts[-2], path.stem
                if uid in seen:
                    raise ValueError("duplicate upstream ID")
                seen.add(uid); speakers.add(sid); chapters.add(chapter)
                ref = row["text"]
                if not reference_status({"reference": ref,
                    "legitimate_empty_reference": row.get("legitimate_empty_reference") is True}).valid:
                    raise ValueError("invalid released reference")
                n_empty += ref == ""
                n_differences += ref != row["text_raw"]
                seconds += float(row["duration"])
            # One whole speaker from each training partition, independent source hash.
            training = split.startswith("train-")
            chosen = min(speakers, key=lambda s: canonical_hash([120101, split, s])) if training else None
            for row in rows:
                path = PurePosixPath(row["audio_filepath"])
                sid, chapter, uid = path.parts[-3], path.parts[-2], path.stem
                if training and sid != chosen:
                    continue
                selected.append({"corpus": "LibriSpeech-PC", "id": uid, "split": split,
                    "reference": row["text"],
                    "legitimate_empty_reference": row.get("legitimate_empty_reference") is True,
                    "families": {"speaker": sid, "chapter": chapter, "book": None},
                    "audio_qualified": False,
                    "reference_raw_sha256": sha256_bytes(row["text_raw"].encode()),
                    "manifest_duration_seconds": row["duration"],
                    "upstream_audio_filepath": row["audio_filepath"]})
            summary[split] = {"rows": len(rows), "unique_ids": len(seen),
                "speakers": len(speakers), "chapters": len(chapters), "books": None,
                "manifest_duration_seconds": seconds, "empty_text_rows": n_empty,
                "text_text_raw_difference_rows": n_differences,
                "json_sha256": sha256_bytes(data), "selected_training_speaker": chosen,
                "audio_qualified_cases": 0, "source_error_denominator": None}
        notice = tar.extractfile("LICENSE.txt").read()
    manifest = make_role_manifest(selected)
    extra = {r["id"]: r for r in selected}
    for row in manifest:
        r = extra[row["id"]]
        row.update(reference_raw_sha256=r["reference_raw_sha256"],
            manifest_duration_seconds=r["manifest_duration_seconds"],
            upstream_audio_filepath=r["upstream_audio_filepath"],
            reference_field="text", reference_policy="PROVISIONAL_NOT_FROZEN",
            source_revision=archive_sha256)
    return {"status": "METADATA_ONLY_NOT_AUDIO_QUALIFIED", "archive_sha256": archive_sha256,
        "license_sha256": sha256_bytes(notice), "splits": summary,
        "roles": dict(sorted(Counter(r["role"] for r in manifest).items())),
        "role_groups": {role: len({r["source_group_id"] for r in manifest if r["role"] == role})
                        for role in sorted({r["role"] for r in manifest})},
        "selection": "All official DEV/test metadata; one source-hash-selected whole training speaker per training split",
        "unqualified": ["audio access/decoding", "book mapping", "Parakeet hypotheses", "source-error counts",
                        "full training-source near-duplicate sweep", "educational/tokenizer-corpus overlap",
                        "final field choice and freeze"]}, manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary, manifest = inventory_lspc(args.archive)
    args.output.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(r, sort_keys=True) + "\n" for r in manifest)
    (args.output / "public_lspc_roles.development.jsonl").write_text(payload)
    summary["role_manifest_sha256"] = sha256_bytes(payload.encode())
    (args.output / "public_lspc_inventory.json").write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
