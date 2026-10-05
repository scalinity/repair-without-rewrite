"""Inventory an already acquired official LS-PC text archive without decoding audio."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path, PurePosixPath
import re
import tarfile

from src.data.contracts import canonical_hash, make_role_manifest, reference_status, sha256_bytes


def chapter_families(metadata: Path) -> tuple[dict, dict]:
    """Read official parent identities; close families through all released chapters.

    A training chapter outside the bounded text inventory can connect two known
    families. Its metadata therefore participates in closure without reading its
    audio or reference. Titles are neither copied nor used as identities.
    """
    data = metadata.read_bytes()
    rows = {}
    for line in data.decode("utf-8", "strict").splitlines():
        if not line.strip() or line.lstrip().startswith(";"):
            continue
        fields = [field.strip() for field in line.split("|", 7)]
        if len(fields) != 8 or any(not fields[i].isascii() or
                not fields[i].isdecimal() or int(fields[i]) < 1 for i in (0, 1, 4, 5)):
            raise ValueError("malformed official chapter identity")
        chapter, reader, _, split, project, book, _, _ = fields
        if chapter in rows:
            raise ValueError("duplicate official chapter identity")
        rows[chapter] = dict(speaker=reader, split=split, project=project, book=book)
    chapters = sorted(rows)
    parent = list(range(len(chapters)))

    def find(i):
        while i != parent[i]:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    seen = {}
    for i, chapter in enumerate(chapters):
        for family in ("speaker", "project", "book"):
            key = (family, rows[chapter][family])
            if key in seen:
                a, b = find(i), find(seen[key])
                parent[max(a, b)] = min(a, b)
            else:
                seen[key] = i
    groups = {}
    for i, chapter in enumerate(chapters):
        groups.setdefault(find(i), []).append(chapter)
    for group in groups.values():
        identity = canonical_hash(["official_chapter_parent_closure_v1", group])
        for chapter in group:
            rows[chapter]["metadata_component"] = identity
    return rows, {"sha256": sha256_bytes(data), "chapters": len(rows),
        "known_parent_components": len(groups),
        "rule": "official_chapter_parent_closure_v1; full released chapter/speaker/project/book graph",
        "uses_audio_or_reference_payload": False}


def inventory_lspc(archive: Path, chapter_metadata: Path | None = None) -> tuple[dict, list[dict]]:
    summary, selected = {}, []
    mapping, mapping_receipt = chapter_families(chapter_metadata) if chapter_metadata else ({}, None)
    archive_sha256 = sha256_bytes(archive.read_bytes())
    with tarfile.open(archive, "r:gz") as tar:
        for member in sorted(tar.getmembers(), key=lambda x: x.name):
            if not member.name.endswith(".json") or "/" in member.name:
                continue
            split = member.name.removesuffix(".json")
            data = tar.extractfile(member).read()
            rows = [json.loads(line) for line in data.splitlines() if line]
            seen = set()
            speakers, chapters, books, projects = set(), set(), set(), set()
            missing_chapters = set()
            n_empty, n_differences, seconds = 0, 0, 0.
            for row in rows:
                path = PurePosixPath(row["audio_filepath"])
                sid, chapter, uid = path.parts[-3], path.parts[-2], path.stem
                if uid in seen:
                    raise ValueError("duplicate upstream ID")
                seen.add(uid); speakers.add(sid); chapters.add(chapter)
                metadata = mapping.get(chapter)
                if metadata:
                    if metadata["speaker"] != sid or metadata["split"] != split:
                        raise ValueError("official chapter reader/split disagrees with text manifest")
                    books.add(metadata["book"]); projects.add(metadata["project"])
                else:
                    missing_chapters.add(chapter)
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
                metadata = mapping.get(chapter)
                families = {"speaker": sid, "chapter": chapter,
                    "book": metadata["book"] if metadata else None}
                if mapping_receipt:
                    families.update(project=metadata["project"] if metadata else None,
                        chapter_metadata_component=metadata["metadata_component"] if metadata else None)
                selected.append({"corpus": "LibriSpeech-PC", "id": uid, "split": split,
                    "reference": row["text"],
                    "legitimate_empty_reference": row.get("legitimate_empty_reference") is True,
                    "families": families,
                    "audio_qualified": False,
                    "reference_raw_sha256": sha256_bytes(row["text_raw"].encode()),
                    "manifest_duration_seconds": row["duration"],
                    "upstream_audio_filepath": row["audio_filepath"]})
            summary[split] = {"rows": len(rows), "unique_ids": len(seen),
                "speakers": len(speakers), "chapters": len(chapters),
                "books": len(books) if mapping_receipt else None,
                "projects": len(projects) if mapping_receipt else None,
                "unmapped_chapters": sorted(missing_chapters) if mapping_receipt else None,
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
        if mapping_receipt:
            row.update(chapter_metadata_sha256=mapping_receipt["sha256"],
                family_closure_rule=mapping_receipt["rule"])
    return {"status": "METADATA_ONLY_NOT_AUDIO_QUALIFIED", "archive_sha256": archive_sha256,
        "license_sha256": sha256_bytes(notice), "splits": summary,
        "chapter_metadata": mapping_receipt,
        "roles": dict(sorted(Counter(r["role"] for r in manifest).items())),
        "role_groups": {role: len({r["source_group_id"] for r in manifest if r["role"] == role})
                        for role in sorted({r["role"] for r in manifest})},
        "selection": "All official DEV/test metadata; one source-hash-selected whole training speaker per training split",
        "unqualified": ["audio access/decoding"] + ([] if mapping_receipt else ["book/project mapping"]) + ["Parakeet hypotheses", "source-error counts",
                        "full training-source near-duplicate sweep", "educational/tokenizer-corpus overlap",
                        "final field choice and freeze"]}, manifest


def training_parent_bounds(archive: Path, chapter_metadata: Path) -> dict:
    """Count existing full training metadata without assigning or selecting roles.

    Surviving parents are potential supply only: the full training literal/near-text
    sweep and audio/reference qualification have not been performed here.
    """
    mapping, receipt = chapter_families(chapter_metadata)
    component_splits = {}
    for metadata in mapping.values():
        component_splits.setdefault(metadata["metadata_component"], set()).add(metadata["split"])
    counts = Counter()
    identities = {}
    per_split = {}
    with tarfile.open(archive, "r:gz") as tar:
        for member in sorted(tar.getmembers(), key=lambda x: x.name):
            if not member.name.startswith("train-") or not member.name.endswith(".json") or "/" in member.name:
                continue
            split = member.name.removesuffix(".json")
            per_split[split] = Counter()
            for line in tar.extractfile(member).read().splitlines():
                if not line:
                    continue
                path = PurePosixPath(json.loads(line)["audio_filepath"])
                speaker, chapter = path.parts[-3], path.parts[-2]
                metadata = mapping.get(chapter)
                if metadata is None or metadata["speaker"] != speaker or metadata["split"] != split:
                    raise ValueError("full training chapter mapping is absent or mismatched")
                splits = component_splits[metadata["metadata_component"]]
                if splits & {"test-clean", "test-other"}:
                    category = "known_final_parent_overlap"
                elif splits & {"dev-clean", "dev-other"}:
                    category = "known_development_parent_overlap"
                else:
                    category = "potential_supply_pending_full_text_and_audio_qualification"
                counts[category] += 1; per_split[split][category] += 1
                group = identities.setdefault(category, {k: set() for k in
                    ("speaker", "book", "project", "chapter", "metadata_component")})
                for family in group:
                    group[family].add(chapter if family == "chapter" else metadata[family])
    return {"status": "METADATA_BOUNDS_ONLY_NO_TRAINING_ROLE_ASSIGNED_OR_CORPUS_SELECTED",
        "archive_sha256": sha256_bytes(archive.read_bytes()), "chapter_metadata": receipt,
        "training_rows": sum(counts.values()), "rows_by_parent_status": dict(counts),
        "distinct_identities_by_parent_status": {category: {k: len(v) for k, v in group.items()}
            for category, group in identities.items()},
        "per_split": {k: dict(v) for k, v in per_split.items()},
        "pending": ["full training-source literal/near-reference sweep", "audio decoding/admission",
            "raw one-best ASR hypotheses and source-error counts", "reference policy and freeze",
            "contamination qualification", "any new development training/calibration assignment"],
        "audio_qualified_cases": 0, "model_or_candidate_outputs_used": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--chapter-metadata", type=Path)
    parser.add_argument("--attempt", type=str)
    args = parser.parse_args()
    if args.attempt and not re.fullmatch(r"attempt[0-9]{2}", args.attempt):
        parser.error("attempt must be attempt followed by two digits")
    summary, manifest = inventory_lspc(args.archive, args.chapter_metadata)
    args.output.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(r, sort_keys=True) + "\n" for r in manifest)
    suffix = "." + args.attempt if args.attempt else ""
    role_path = args.output / f"public_lspc_roles.development{suffix}.jsonl"
    inventory_path = args.output / f"public_lspc_inventory{suffix}.json"
    if args.attempt and (role_path.exists() or inventory_path.exists()):
        raise FileExistsError("preserve existing attempt artifacts")
    role_path.write_text(payload)
    summary["role_manifest_sha256"] = sha256_bytes(payload.encode())
    summary["role_manifest_path"] = str(role_path)
    inventory_path.write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
