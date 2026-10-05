"""Hash-bound released targets; only explicit development roles can be read."""
import hashlib
import json
from pathlib import Path
import tarfile


def join_target(source, role, *, allowed_roles):
    if role["role"] not in allowed_roles or role["role"] not in {"train", "hpo_development", "calibration"}:
        raise ValueError("forbidden source role")
    if Path(source["audio_filepath"]).stem != role["id"]:
        raise ValueError("source identity mismatch")
    if role["reference_field"] != "text_raw":
        raise ValueError("unqualified target field")
    for field in ("text", "text_raw"):
        if hashlib.sha256(source[field].encode("utf-8", "strict")).hexdigest() != role[field + "_sha256"]:
            raise ValueError("changed reference bytes")
    return {**role, "target": source["text_raw"], "official_processed_target": source["text"],
            "audio_filepath": source["audio_filepath"]}


def load_targets(roles_path, qualification_path, *, allowed_roles):
    roles_path = Path(roles_path)
    qualification = json.loads(Path(qualification_path).read_text())
    if hashlib.sha256(roles_path.read_bytes()).hexdigest() != qualification["manifest_sha256"]:
        raise ValueError("role manifest changed after qualification")
    selected = {r["id"]:r for r in (json.loads(s) for s in roles_path.read_text().splitlines())
                if r["role"] in allowed_roles}
    result = {}
    archive = Path("exports/source-qualification/ls_pc_manifest.tar.gz")
    if hashlib.file_digest(archive.open("rb"),"sha256").hexdigest() != "96d4eae2222b29b66437a21959252419bcd4762e5042e71e023790171054d1c0":
        raise ValueError("official release changed")
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            if not member.name.endswith(".json") or member.name.startswith("test-"):
                continue
            for line in tar.extractfile(member):
                source = json.loads(line)
                identifier = Path(source["audio_filepath"]).stem
                if identifier not in selected:
                    continue
                if identifier in result:
                    raise ValueError("duplicate admitted source")
                result[identifier] = join_target(source, selected[identifier], allowed_roles=allowed_roles)
    if result.keys() != selected.keys():
        raise ValueError("missing admitted source")
    return [result[k] for k in sorted(result)]
