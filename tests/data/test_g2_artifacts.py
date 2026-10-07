import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.data import g2_artifacts as g2


@pytest.fixture
def bound_root(tmp_path, monkeypatch):
    mount = tmp_path / "volume"
    root = mount / "g2"
    root.mkdir(parents=True)
    policy = tmp_path / "policy.json"
    policy.write_text(json.dumps({"minimum_free_bytes": g2.MINIMUM_FREE_BYTES,
        "root_path_sha256": hashlib.sha256(str(root).encode()).hexdigest(),
        "mount_path_sha256": hashlib.sha256(str(mount).encode()).hexdigest(),
        "volume_uuid_sha256": hashlib.sha256(b"fixture-uuid").hexdigest(),
        "versioned_areas": ["qualification-v1"]}))
    binding = tmp_path / "binding.json"
    binding.write_text(json.dumps({"schema": "g2_artifact_binding_v1", "root": str(root),
        "mount": str(mount), "root_inode": root.stat().st_ino,
        "policy_sha256": g2.sha256(policy)}))
    monkeypatch.setattr(g2, "_volume_info", lambda _: {"VolumeUUID": "fixture-uuid",
        "MountPoint": str(mount), "Internal": False,
        "FilesystemName": "Case-sensitive APFS", "Writable": True})
    monkeypatch.setattr(g2.os, "statvfs", lambda _: SimpleNamespace(
        f_bavail=g2.MINIMUM_FREE_BYTES + 1, f_frsize=1))
    return g2.ArtifactRoot(binding, policy)


def test_missing_binding_does_not_create_or_import_model(tmp_path):
    with pytest.raises(FileNotFoundError):
        g2.ArtifactRoot(tmp_path / "missing.json")
    assert list(tmp_path.iterdir()) == []


def test_missing_root_fails_before_volume_query(bound_root, monkeypatch):
    bound_root.root.rmdir()
    monkeypatch.setattr(g2, "_volume_info", lambda _: pytest.fail("volume query after missing root"))
    with pytest.raises(FileNotFoundError, match="no fallback"):
        bound_root.preflight()
    assert not bound_root.root.exists()


@pytest.mark.parametrize("field,value", [("Internal", True), ("Writable", False),
    ("VolumeUUID", "wrong"), ("FilesystemName", "APFS")])
def test_changed_volume_is_rejected(bound_root, monkeypatch, field, value):
    original = g2._volume_info(bound_root.mount)
    monkeypatch.setattr(g2, "_volume_info", lambda _: original | {field: value})
    with pytest.raises(ValueError, match="identity/filesystem/access"):
        bound_root.preflight()


def test_literal_capacity_cannot_use_purgeable_space(bound_root, monkeypatch):
    monkeypatch.setattr(g2.os, "statvfs", lambda _: SimpleNamespace(
        f_bavail=g2.MINIMUM_FREE_BYTES - 1, f_frsize=1))
    with pytest.raises(OSError, match="GENERATION_2_STORAGE_BLOCKED"):
        bound_root.preflight()


def test_no_absolute_parent_or_symlink_fallback(bound_root, tmp_path):
    with pytest.raises(ValueError):
        bound_root.path(tmp_path / "internal-fallback")
    with pytest.raises(ValueError):
        bound_root.path("qualification-v1/../../internal-fallback")
    (bound_root.root / "qualification-v1").symlink_to(tmp_path, target_is_directory=True)
    with pytest.raises(ValueError, match="escapes"):
        bound_root.path("qualification-v1/internal-fallback")
    assert not (tmp_path / "internal-fallback").exists()


def test_atomic_completion_and_inventory(bound_root):
    relative = "qualification-v1/published"
    with g2.atomic_artifact(bound_root, relative) as pending:
        (pending / "arrays.fixture").write_bytes(b"synthetic arrays")
        (pending / "metadata.json").write_text('{"fixture":true}')
        assert not bound_root.path(relative).exists()
        with pytest.raises(ValueError, match="incomplete"):
            g2.read_complete(pending)
    destination = bound_root.path(relative)
    manifest = g2.read_complete(destination)
    assert set(manifest["files"]) == {"arrays.fixture", "metadata.json"}
    with pytest.raises(FileExistsError):
        with g2.atomic_artifact(bound_root, relative):
            pytest.fail("existing immutable checkpoint accepted")
    (destination / "arrays.fixture").write_bytes(b"corrupted")
    with pytest.raises(ValueError, match="identity mismatch"):
        g2.read_complete(destination)


def test_interruption_preserves_partial_and_rejects_it(bound_root):
    with pytest.raises(RuntimeError, match="simulated interruption"):
        with g2.atomic_artifact(bound_root, "qualification-v1/interrupted") as pending:
            (pending / "arrays.fixture").write_bytes(b"unfinished")
            raise RuntimeError("simulated interruption")
    assert pending.exists() and not bound_root.path("qualification-v1/interrupted").exists()
    with pytest.raises(ValueError, match="incomplete"):
        g2.read_complete(pending)


def test_extra_inventory_entry_rejected(bound_root):
    with g2.atomic_artifact(bound_root, "qualification-v1/extra") as pending:
        (pending / "payload").write_bytes(b"synthetic")
    destination = bound_root.path("qualification-v1/extra")
    (destination / "unrecorded").write_bytes(b"extra")
    with pytest.raises(ValueError, match="inventory"):
        g2.read_complete(destination)


def test_atomic_replacement_and_offline_controls(tmp_path, monkeypatch):
    path = tmp_path / "replace"
    path.write_bytes(b"old")
    g2.replace_fixture_file(path, b"new")
    assert path.read_bytes() == b"new" and list(tmp_path.iterdir()) == [path]
    for key in ("HF_HUB_OFFLINE", "HF_DATASETS_OFFLINE", "TRANSFORMERS_OFFLINE"):
        monkeypatch.delenv(key, raising=False)
    g2.offline_model_environment()
    assert all(g2.os.environ[key] == "1" for key in
        ("HF_HUB_OFFLINE", "HF_DATASETS_OFFLINE", "TRANSFORMERS_OFFLINE"))
    assert g2.os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] == "0"
