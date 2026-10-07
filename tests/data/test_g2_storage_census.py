import pytest

from benchmarks.g2_storage_reforecast import retained_census


def test_internal_directory_alias_counts_link_without_recounting_payload(tmp_path):
    area = tmp_path / "qualification-v1"
    target = area / "test-0"
    target.mkdir(parents=True)
    payload = target / "payload.bin"
    payload.write_bytes(b"retained")
    alias = area / "test-current"
    alias.symlink_to(target.name, target_is_directory=True)

    result = retained_census(tmp_path, [area.name])[area.name]
    assert result == {
        "files": 1,
        "symlinks": 1,
        "logical_bytes": 8 + alias.lstat().st_size,
        "allocated_bytes": (payload.stat().st_blocks + alias.lstat().st_blocks) * 512,
    }


@pytest.mark.parametrize("outside", [True, False])
def test_external_or_unresolved_alias_stops_census(tmp_path, outside):
    root = tmp_path / "root"
    area = root / "qualification-v1"
    area.mkdir(parents=True)
    target = tmp_path / "outside"
    if outside:
        target.mkdir()
    else:
        target = area / "absent"
    (area / "test-current").symlink_to(target, target_is_directory=True)

    with pytest.raises((ValueError, FileNotFoundError)):
        retained_census(root, [area.name])
