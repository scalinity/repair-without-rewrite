"""Physical Generation-2 storage only; no model or scientific imports."""
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import plistlib
import subprocess
import tempfile

MINIMUM_FREE_BYTES = 250 * 1024**3
POLICY_PATH = Path(__file__).resolve().parents[2] / "configs/generation_2/artifact_policy_v1.json"


def sha256(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def offline_model_environment():
    """Call after storage preflight and before importing model libraries."""
    for key in ("HF_HUB_OFFLINE", "HF_DATASETS_OFFLINE", "TRANSFORMERS_OFFLINE"):
        os.environ[key] = "1"
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "0"
    os.environ["MLX_ENABLE_TF32"] = "0"


def _volume_info(path):
    return plistlib.loads(subprocess.check_output(
        ["diskutil", "info", "-plist", str(path)]))


class ArtifactRoot:
    def __init__(self, binding_path, policy_path=POLICY_PATH):
        # No mkdir, network, library import or alternate path precedes this check.
        self.binding_path = Path(binding_path)
        self.policy_path = Path(policy_path)
        self.policy = json.loads(self.policy_path.read_text())
        self.binding = json.loads(self.binding_path.read_text())
        self.root = Path(self.binding["root"])
        self.mount = Path(self.binding["mount"])
        self.preflight()

    def preflight(self):
        p, b = self.policy, self.binding
        if p.get("minimum_free_bytes") != MINIMUM_FREE_BYTES:
            raise ValueError("Generation-2 minimum storage capacity must remain 250 GiB")
        if b.get("schema") != "g2_artifact_binding_v1" or b.get("policy_sha256") != sha256(self.policy_path):
            raise ValueError("Generation-2 artifact binding/policy identity mismatch")
        if (not self.root.is_absolute() or not self.mount.is_absolute()
                or self.root.is_symlink() or self.mount.is_symlink()
                or not self.root.is_dir() or not self.mount.is_dir()):
            raise FileNotFoundError("Generation-2 artifact volume/root unavailable; no fallback")
        root, mount = self.root.resolve(strict=True), self.mount.resolve(strict=True)
        if root.parent != mount or root.stat().st_dev != mount.stat().st_dev:
            raise ValueError("Generation-2 root is outside the bound volume")
        if (hashlib.sha256(str(root).encode()).hexdigest() != p["root_path_sha256"]
                or hashlib.sha256(str(mount).encode()).hexdigest() != p["mount_path_sha256"]):
            raise ValueError("Generation-2 physical path identity mismatch")
        if root.stat().st_ino != b["root_inode"]:
            raise ValueError("Generation-2 root directory identity changed")
        v = _volume_info(mount)
        if (hashlib.sha256(v["VolumeUUID"].encode()).hexdigest() != p["volume_uuid_sha256"]
                or v["MountPoint"] != str(mount) or v["Internal"]
                or v["FilesystemName"] != "Case-sensitive APFS" or not v["Writable"]
                or not os.access(root, os.R_OK | os.W_OK | os.X_OK)):
            raise ValueError("Generation-2 external volume identity/filesystem/access mismatch")
        free = os.statvfs(root)
        available = free.f_bavail * free.f_frsize
        if available < p["minimum_free_bytes"]:
            raise OSError("GENERATION_2_STORAGE_BLOCKED: literal external free space below 250 GiB")
        return {"volume_uuid_sha256": p["volume_uuid_sha256"],
                "filesystem": v["FilesystemName"], "literal_free_bytes": available,
                "root_binding_sha256": sha256(self.binding_path),
                "policy_sha256": sha256(self.policy_path)}

    def path(self, relative):
        self.preflight()
        relative = Path(relative)
        if relative.is_absolute() or not relative.parts or any(x in ("..", ".") for x in relative.parts):
            raise ValueError("Generation-2 artifacts require an in-root relative path")
        if relative.parts[0] not in self.policy["versioned_areas"]:
            raise ValueError("unknown Generation-2 versioned artifact area")
        target = self.root / relative
        # Existing ancestors must not redirect even when the final file is absent.
        if not target.resolve().is_relative_to(self.root.resolve()):
            raise ValueError("Generation-2 artifact path escapes the bound root")
        return target


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def read_complete(path):
    path = Path(path)
    if ".partial-" in path.name or path.is_symlink() or not path.is_dir():
        raise ValueError("incomplete/redirected Generation-2 checkpoint")
    manifest = json.loads((path / "COMPLETE.json").read_text())
    if manifest.get("schema") != "g2_atomic_artifact_v1" or not manifest.get("files"):
        raise ValueError("incomplete Generation-2 completion inventory")
    files = manifest["files"]
    if set(files) != {p.name for p in path.iterdir() if p.name != "COMPLETE.json"}:
        raise ValueError("Generation-2 checkpoint inventory mismatch")
    for name, identity in files.items():
        p = path / name
        if (Path(name).name != name or p.is_symlink() or not p.is_file()
                or p.stat().st_size != identity["bytes"] or sha256(p) != identity["sha256"]):
            raise ValueError("Generation-2 checkpoint file identity mismatch")
    return manifest


@contextmanager
def atomic_artifact(root, relative):
    """Publish an immutable directory after payload fsync and COMPLETE readback.

    The caller writes its existing payload format into the yielded directory.
    Failed partial directories remain evidence until fixture-specific cleanup.
    """
    destination = root.path(relative)
    # Never recreate the bound root or its mount after a disconnect. Create
    # only one child at a time beneath an already-existing bound parent.
    parent = root.root
    for component in destination.relative_to(root.root).parts[:-1]:
        parent = parent / component
        parent.mkdir(exist_ok=True)
        if parent.is_symlink() or parent.stat().st_dev != root.root.stat().st_dev:
            raise ValueError("Generation-2 artifact parent is redirected or outside the bound volume")
    sync_directory(destination.parent)
    if destination.exists():
        raise FileExistsError(destination)
    temporary = Path(tempfile.mkdtemp(prefix=destination.name + ".partial-", dir=destination.parent))
    yield temporary
    root.preflight()
    entries = list(temporary.iterdir())
    if not entries or any(p.name == "COMPLETE.json" or p.is_symlink() or not p.is_file() for p in entries):
        raise ValueError("Generation-2 atomic payload must contain flat regular files")
    identities = {}
    for p in sorted(entries):
        with p.open("rb") as stream:
            os.fsync(stream.fileno())
        identities[p.name] = {"sha256": sha256(p), "bytes": p.stat().st_size}
    manifest = {"schema": "g2_atomic_artifact_v1", "files": identities}
    with (temporary / "COMPLETE.json").open("x") as stream:
        json.dump(manifest, stream, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    sync_directory(temporary)
    # A completed temporary directory still cannot be consumed as published.
    if destination.exists():
        raise FileExistsError(destination)
    os.rename(temporary, destination)
    sync_directory(destination.parent)
    if read_complete(destination) != manifest:
        raise ValueError("Generation-2 published artifact readback mismatch")


def replace_fixture_file(path, payload):
    """Atomic single-file replacement, used only for disposable qualification fixtures."""
    path = Path(path)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".partial-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        sync_directory(path.parent)
    finally:
        if Path(temporary).exists():
            Path(temporary).unlink()
