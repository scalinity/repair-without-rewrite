import hashlib
import pytest
from src.data.development_reader import join_target


def fixture(role="train"):
    source = {"audio_filepath":"train-clean-100/1/2/1-2-3.flac", "text":"a b .", "text_raw":"a  b."}
    row = {"id":"1-2-3", "role":role, "reference_field":"text_raw", "text_sha256":hashlib.sha256(source["text"].encode()).hexdigest(),
           "text_raw_sha256":hashlib.sha256(source["text_raw"].encode()).hexdigest()}
    return source,row


def test_target_reader_preserves_raw_bytes_and_checks_both_released_fields():
    source,role=fixture()
    assert join_target(source,role,allowed_roles={"train"})["target"] == "a  b."
    source["text"]="changed secondary field"
    with pytest.raises(ValueError,match="changed reference"):
        join_target(source,role,allowed_roles={"train"})


@pytest.mark.parametrize("bad_role", ["sealed_final","excluded_overlap","calibration","hpo_development"])
def test_training_reader_rejects_other_roles_even_with_valid_target_hash(bad_role):
    source,role=fixture(bad_role)
    with pytest.raises(ValueError):
        join_target(source,role,allowed_roles={"train"})


def test_final_role_cannot_be_admitted_even_by_callers_role_allowlist():
    source,role=fixture("sealed_final")
    with pytest.raises(ValueError):
        join_target(source,role,allowed_roles={"sealed_final"})
