import hashlib
import json
from types import SimpleNamespace

import pytest
from src.data.g2_corpus import bind_legacy, check_audio_info, source_requests, validate_census


@pytest.fixture
def census():
    rows = []
    digest = hashlib.sha256(b"synthetic reference").hexdigest()
    for role, count, groups in (("train", 14113, 4), ("calibration", 1900, 32),
                                ("hpo_development", 796, 20)):
        for index in range(count):
            group = f"{role}/group-{index % groups}"
            rows.append(dict(id=f"{role}-{index:05d}", role=role, source_group_id=group,
                families={"book": group}, manifest_duration_seconds="2.000",
                target="synthetic reference", official_processed_target="synthetic reference",
                reference_field="text_raw", text_raw_sha256=digest, text_sha256=digest))
    return rows


def test_complete_census_rejects_subsets_duplicate_ids_and_changed_gold(census):
    validate_census(census)
    with pytest.raises(ValueError, match="no subset"):
        validate_census(census[:-1])
    census[-1]["target"] += " changed"
    with pytest.raises(ValueError, match="canonical reference"):
        validate_census(census)


def test_family_values_are_joined_without_treating_common_field_names_as_leakage(census):
    validate_census(census)
    census[-1]["families"]["book"] = census[0]["families"]["book"]
    with pytest.raises(ValueError, match="derivation-family leakage"):
        validate_census(census)


def test_duration_envelope_rejects_a_required_row_without_excluding_it(census):
    census[0]["manifest_duration_seconds"] = "12.00001"
    with pytest.raises(ValueError, match="duration"):
        validate_census(census)


def test_requests_preserve_legacy_and_match_independent_blind_replay_hashes(census):
    train = [row for row in census if row["role"] == "train"][:1024]
    cal = [row for row in census if row["role"] == "calibration"][:96]
    hpo = [row for row in census if row["role"] == "hpo_development"][:12]
    def old(row):
        return {**row, "source": "synthetic hypothesis", "source_sha256":
                hashlib.sha256(b"synthetic hypothesis").hexdigest(), "population": "natural"}
    pairs = list(map(old, train))
    panel = list(map(old, [*cal, *hpo]))
    for row in panel[:96]:
        row["role"] = "calibration_development_consumed"
    legacy = bind_legacy(census, pairs, panel)
    replay = []
    new = [row for row in census if row["id"] not in legacy]
    for name, is_train in (("TRAIN", True), ("DEVELOPMENT", False)):
        def key(row):
            return hashlib.sha256(json.dumps(["G2", 42, "PARAKEET_REPLAY", name, row["id"]],
                separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        eligible = [row for row in new if (row["role"] == "train") == is_train]
        replay.extend(dict(id=row["id"], role=row["role"], source_group_id=row["source_group_id"],
                           selection_sha256=key(row)) for row in sorted(eligible, key=key)[:32])
    requests = source_requests(census, legacy, {"cases": replay})
    assert len(requests) == 15741
    assert not {row["id"] for row in requests} & legacy.keys()
    assert sum(row["kind"] == "replay" for row in requests) == 64
    replay[0]["selection_sha256"] = "changed"
    with pytest.raises(ValueError, match="selection changed"):
        source_requests(census, legacy, {"cases": replay})
    pairs[0]["source"] += " rerun"
    with pytest.raises(ValueError, match="bytes changed"):
        bind_legacy(census, pairs, panel)


@pytest.mark.parametrize("changed", [dict(frames=192001), dict(frames=31999),
    dict(samplerate=8000), dict(channels=2), dict(format="WAV"), dict(subtype="PCM_24")])
def test_actual_native_audio_admission(changed):
    info = dict(frames=160000, samplerate=16000, channels=1, format="FLAC", subtype="PCM_16")
    check_audio_info(SimpleNamespace(**info))
    with pytest.raises(ValueError):
        check_audio_info(SimpleNamespace(**{**info, **changed}))
