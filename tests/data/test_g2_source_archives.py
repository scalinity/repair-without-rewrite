import hashlib
import json
from pathlib import Path

import pytest

from benchmarks import g2_source_archives as acquisition


def test_missing_root_precedes_network_and_output(tmp_path, monkeypatch):
    calls = []
    def missing(_):
        calls.append("root")
        raise FileNotFoundError("missing bound volume")
    monkeypatch.setattr(acquisition, "ArtifactRoot", missing)
    import urllib.request
    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: pytest.fail("network before preflight"))
    with pytest.raises(FileNotFoundError):
        acquisition.acquire(tmp_path / "missing-binding", 1, tmp_path / "receipt")
    assert calls == ["root"] and list(tmp_path.iterdir()) == []


def test_approved_inventory_and_no_sealed_archive():
    policy = json.loads(acquisition.POLICY.read_text())
    assert sum(x["bytes"] for x in policy["archives"]) == 53642979491
    assert [x["name"] for x in policy["archives"]] == ["train-clean-360", "train-other-500"]
    assert all(x["official_url"].startswith("https://www.openslr.org/resources/12/train-") for x in policy["archives"])
    assert policy["scientific_recipes"] == "AUTHORIZED_UNSTARTED"


def test_archive_identity_rejects_truncation_and_changed_bytes(tmp_path):
    p = tmp_path / "synthetic-archive"
    p.write_bytes(b"fixture")
    specification = {"bytes": 7, "official_md5": hashlib.md5(b"fixture").hexdigest()}
    assert acquisition.verify_archive(p, specification)["bytes"] == 7
    p.write_bytes(b"wrong!!")
    with pytest.raises(ValueError, match="MD5"):
        acquisition.verify_archive(p, specification)
    p.write_bytes(b"short")
    with pytest.raises(ValueError, match="length"):
        acquisition.verify_archive(p, specification)
