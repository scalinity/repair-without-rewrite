import pytest

from src.data.contracts import make_role_manifest, reference_status, require_development_role


def row(id, split, ref="one two", speaker=None, **extra):
    return dict(corpus="fixture", id=id, split=split, reference=ref,
                families={"speaker": speaker, "book": None}, **extra)


@pytest.mark.parametrize("record,reason", [({}, "reference_missing"),
    ({"reference": None}, "reference_null"), ({"reference": 1}, "reference_not_string"),
    ({"reference": "\ud800"}, "reference_invalid_utf8"),
    ({"reference": ""}, "empty_reference_not_designated")])
def test_invalid_reference_states_remain_distinct(record, reason):
    status = reference_status(record)
    assert not status.valid and status.reason == reason


def test_legitimate_empty_reference_and_documented_sentinel():
    status = reference_status({"reference": "", "legitimate_empty_reference": True})
    assert status.valid and status.genuine_empty
    assert reference_status({"reference": "N/A"}).valid
    assert reference_status({"reference": "N/A"}, documented_sentinels=["N/A"]).reason == "reference_documented_sentinel"
    assert not reference_status({"reference": "", "legitimate_empty_reference": 1}).valid


def test_final_family_keeps_final_and_excludes_its_training_derivative():
    records = [row("train", "train", speaker="x"), row("final", "test", speaker="x")]
    manifest = make_role_manifest(records)
    assert {r["id"]: r["role"] for r in manifest} == {"final": "sealed_final", "train": "excluded_overlap"}
    assert len({r["source_group_id"] for r in manifest}) == 1
    assert all("reference" not in r for r in manifest)
    assert all(r["audio_qualification"] == "PENDING" for r in manifest)


def test_crossed_book_speaker_connected_components_before_augmentation():
    records = [row("a", "train", speaker="x"), row("b", "train", speaker="x"), row("c", "test", speaker="y")]
    records[1]["families"]["book"] = records[2]["families"]["book"] = "book"
    manifest = make_role_manifest(records)
    assert len({r["source_group_id"] for r in manifest}) == 1
    assert [r["role"] for r in manifest] == ["excluded_overlap", "excluded_overlap", "sealed_final"]


def test_role_order_and_input_order_do_not_change_manifest():
    records = [row(str(i), "train", speaker=str(i)) for i in range(20)]
    a, b = make_role_manifest(records), make_role_manifest(reversed(records))
    assert a == b
    assert {r["role"] for r in a} == {"train", "calibration"}


def test_short_generic_sentence_does_not_invent_shared_source_identity():
    manifest = make_role_manifest([row("a", "train"), row("b", "test")])
    assert len({r["source_group_id"] for r in manifest}) == 2
    assert manifest[0]["role"] in {"train", "calibration"}
    assert all(r["families"]["book"] is None for r in manifest)


def test_long_near_duplicate_keeps_final_and_excludes_training():
    text = " ".join("word" + str(i) for i in range(60))
    manifest = make_role_manifest([row("a", "train", ref=text), row("b", "test", ref=text + " end")])
    assert len({r["source_group_id"] for r in manifest}) == 1
    assert manifest[0]["role"] == "excluded_overlap"


def test_candidate_data_and_duplicate_ids_are_rejected():
    with pytest.raises(ValueError, match="candidate"):
        make_role_manifest([row("a", "train", output="out")])
    with pytest.raises(ValueError, match="duplicate"):
        make_role_manifest([row("a", "train"), row("a", "test")])


@pytest.mark.parametrize("role", ["sealed_final", "calibration", "excluded_overlap", None])
def test_development_loader_rejects_reserved_and_final_roles(role):
    with pytest.raises(ValueError): require_development_role({"role": role})

from src.data.comparator_interfaces import byt5_batch, byt5_complete_text, byt5_ids


def test_byt5_native_bytes_unicode_literal_controls_and_completed_empty():
    for text in ["", "é", "路径", "<extra_id_0>"]:
        ids = byt5_ids(text)
        assert len(ids) == len(text.encode()) + 1
        assert byt5_complete_text(ids) == text


def test_byt5_masked_padding_shift_and_eos_remain_supervised():
    batch = byt5_batch(["é", "x"], ["", "ab"], source_capacity=8, target_capacity=8)
    assert batch["input_ids"] == [[198, 172, 1], [123, 1, 0]]
    assert batch["attention_mask"] == [[1, 1, 1], [1, 1, 0]]
    assert batch["labels"] == [[1, -100, -100], [100, 101, 1]]
    assert batch["decoder_input_ids"] == [[0, 1, 0], [0, 100, 101]]
    assert batch["valid_target_counts"] == [1, 3]


def test_byt5_no_silent_capacity_truncation_or_invalid_byte_success():
    with pytest.raises(ValueError, match="truncate"):
        byt5_ids("é", qualified_capacity=2)
    with pytest.raises(UnicodeDecodeError): byt5_complete_text([258, 1])
    for ids in [[100], [1, 100, 1], [259, 1], [0, 1]]:
        with pytest.raises(ValueError): byt5_complete_text(ids)


def test_inventory_preserves_field_uncertainty_without_audio_claim(tmp_path):
    import io
    import json
    import tarfile
    from src.data.public_inventory import inventory_lspc

    archive = tmp_path / "synthetic.tar.gz"
    payload = json.dumps({"audio_filepath": "dev-clean/7/9/7-9-1.flac",
        "text": "Hello.", "text_raw": "HELLO.", "duration": 1.5}).encode() + b"\n"
    with tarfile.open(archive, "w:gz") as tar:
        for name, data in [("dev-clean.json", payload), ("LICENSE.txt", b"synthetic fixture")]:
            member = tarfile.TarInfo(name); member.size = len(data)
            tar.addfile(member, io.BytesIO(data))
    summary, manifest = inventory_lspc(archive)
    assert summary["splits"]["dev-clean"]["rows"] == 1
    assert summary["splits"]["dev-clean"]["text_text_raw_difference_rows"] == 1
    assert summary["splits"]["dev-clean"]["audio_qualified_cases"] == 0
    assert manifest[0]["reference_policy"] == "PROVISIONAL_NOT_FROZEN"
    assert manifest[0]["reference_raw_sha256"] != manifest[0]["reference_sha256"]
    assert manifest[0]["families"] == {"speaker": "7", "chapter": "9", "book": None}


def test_official_parent_metadata_closes_through_an_unselected_training_chapter(tmp_path):
    import io
    import json
    import tarfile
    from src.data.public_inventory import inventory_lspc

    metadata = tmp_path / "CHAPTERS.TXT"
    metadata.write_text("; official format fixture\n"
        "9 | 7 | 1 | dev-clean | 10 | 100 | title | title\n"
        "10 | 7 | 1 | train-clean-100 | 20 | 200 | title | title\n"
        "11 | 8 | 1 | test-clean | 20 | 200 | title | title\n")
    archive = tmp_path / "synthetic.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        payloads = [("LICENSE.txt", b"fixture")]
        for split, speaker, chapter in [("dev-clean", "7", "9"), ("test-clean", "8", "11")]:
            payloads.append((split + ".json", (json.dumps({
                "audio_filepath": f"{split}/{speaker}/{chapter}/{speaker}-{chapter}-1.flac",
                "text": "brief", "text_raw": "BRIEF", "duration": 1.}) + "\n").encode()))
        for name, data in payloads:
            member = tarfile.TarInfo(name); member.size = len(data)
            tar.addfile(member, io.BytesIO(data))
    summary, manifest = inventory_lspc(archive, metadata)
    assert summary["chapter_metadata"]["chapters"] == 3
    assert summary["chapter_metadata"]["known_parent_components"] == 1
    assert {r["id"]: r["role"] for r in manifest} == {
        "7-9-1": "excluded_overlap", "8-11-1": "sealed_final"}
    assert manifest[0]["families"]["book"] != manifest[1]["families"]["book"]
    assert manifest[0]["families"]["chapter_metadata_component"] == manifest[1]["families"]["chapter_metadata_component"]
    metadata.write_text(metadata.read_text().replace("9 | 7", "9 | 99"))
    with pytest.raises(ValueError, match="reader/split"):
        inventory_lspc(archive, metadata)


@pytest.mark.parametrize("line", ["1 | 2 | 1 | dev-clean | 3 | 4 | a | b\n" * 2,
    "1 | 2 | 1 | dev-clean | 3 | unknown | a | b\n"])
def test_official_chapter_duplicate_or_malformed_identity_is_not_guessed(tmp_path, line):
    from src.data.public_inventory import chapter_families
    path = tmp_path / "CHAPTERS.TXT"; path.write_text(line)
    with pytest.raises(ValueError): chapter_families(path)


def test_actual_attempt02_book_project_closure_excludes_all_known_final_relatives():
    import json
    from pathlib import Path
    from src.data.contracts import sha256_bytes

    root = Path(__file__).resolve().parents[2]
    initial = root / "experiments/manifests/public_lspc_roles.development.jsonl"
    assert sha256_bytes(initial.read_bytes()) == "fb5cd642d59d23c86a4bf1bb86e47cf07a6e748c5433749423c392bec375e32d"
    path = root / "experiments/manifests/public_lspc_roles.development.attempt02.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    assert len(rows) == 10842
    final = [r for r in rows if r["role"] == "sealed_final"]
    dev = [r for r in rows if r["role"] == "hpo_development"]
    assert len(final) == 5273 and len(dev) == 898
    for key in ("speaker", "chapter", "book", "project", "chapter_metadata_component"):
        assert {r["families"][key] for r in dev}.isdisjoint({r["families"][key] for r in final})
        assert all(r["families"][key] is not None for r in rows)
    assert len({r["families"]["book"] for r in final}) == 97
    assert len({r["source_group_id"] for r in dev}) == 12
    assert all("reference" not in r and "text" not in r for r in rows)


def test_training_parent_bounds_are_not_training_roles_or_audio_qualification(tmp_path):
    import io
    import json
    import tarfile
    from src.data.public_inventory import training_parent_bounds

    metadata = tmp_path / "CHAPTERS.TXT"
    metadata.write_text("1 | 7 | 1 | train-clean-100 | 10 | 100 | a | b\n"
        "2 | 8 | 1 | train-clean-100 | 20 | 200 | a | b\n"
        "3 | 9 | 1 | test-clean | 20 | 200 | a | b\n")
    # No references or model outputs are needed for parent-only inventory.
    payload = "".join(json.dumps({"audio_filepath": f"train-clean-100/{s}/{c}/{s}-{c}-1.flac"})
        + "\n" for s, c in [(7, 1), (8, 2)]).encode()
    archive = tmp_path / "metadata.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        member = tarfile.TarInfo("train-clean-100.json"); member.size = len(payload)
        tar.addfile(member, io.BytesIO(payload))
    result = training_parent_bounds(archive, metadata)
    assert result["training_rows"] == 2
    assert result["rows_by_parent_status"] == {"known_final_parent_overlap": 1,
        "potential_supply_pending_full_text_and_audio_qualification": 1}
    assert result["audio_qualified_cases"] == 0
    assert result["status"] == "METADATA_BOUNDS_ONLY_NO_TRAINING_ROLE_ASSIGNED_OR_CORPUS_SELECTED"
