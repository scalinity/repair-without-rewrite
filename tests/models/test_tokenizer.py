import json

import pytest

from src.models.tokenizer import ByteBPE, RESTORE_REFERENCE, SPECIAL_TOKENS, frame_source


@pytest.mark.parametrize("text", ["", "  /tmp/a a.py\r\n\t", "👩‍🔬🙂", "e\u0301 é", "3.12.4 --flag -0.002",
                                    "<BOS> restore_reference <EDIT>", "same/id and same/id", "C:\\Users\\foo"])
def test_exact_roundtrip_and_literal_special_control(text):
    tokenizer = ByteBPE.train(["abc abc", "path/path", "🙂🙂"], 5)
    ids = tokenizer.encode(text)
    assert tokenizer.decode(ids) == text
    assert not any(256 <= x <= 319 for x in ids)


def test_byte_boundaries_utf8_and_combining_marks():
    source = ByteBPE().source("a🙂e\u0301")
    assert source.byte_offsets == tuple(range(9))
    assert source.codepoint_byte_offsets == (0, 1, 5, 6, 8)
    assert source.legal_pointer_mask == (True, True, False, False, False, True, True, False, True)
    assert len(source.source_hash) == 64
    assert ByteBPE().source("").legal_pointer_mask == (True,)


def test_decoding_concatenates_before_strict_utf8_and_rejects_malformed():
    tokenizer = ByteBPE()
    ids = tokenizer.encode("🙂")
    assert tokenizer.decode(ids) == "🙂"
    with pytest.raises(UnicodeDecodeError):
        tokenizer.decode(ids[:1])
    with pytest.raises(UnicodeEncodeError):
        tokenizer.encode("\ud800")
    with pytest.raises(ValueError):
        tokenizer.decode([257])
    with pytest.raises(ValueError):
        tokenizer.decode([16384])


def test_deterministic_merge_ranks_maps_and_artifact_roundtrip(tmp_path):
    texts = ["abc abc abc", "abc def def", "xy xy xy"]
    one, two = ByteBPE.train(texts, 4), ByteBPE.train(list(reversed(texts)), 4)
    assert one.merges == two.merges
    hashes = one.save(tmp_path, "synthetic_development_fixture")
    loaded = ByteBPE.load(tmp_path)
    assert loaded.merges == one.merges
    assert loaded.encode("abc def xy") == one.encode("abc def xy")
    assert one.vocab_size == 324
    assert len(hashes["tokenizer.json"]) == 64
    assert len(SPECIAL_TOKENS) == 64
    assert SPECIAL_TOKENS[RESTORE_REFERENCE] == "restore_reference"
    artifact = json.loads((tmp_path/"tokenizer.json").read_text())
    artifact["byte_map_hex"]["0"] = "01"
    (tmp_path/"tokenizer.json").write_text(json.dumps(artifact))
    with pytest.raises(ValueError):
        ByteBPE.load(tmp_path)


def test_digit_isolation_and_trusted_framing():
    tokenizer = ByteBPE.train(["123 123 123 path path"], 3, digit_isolation=True)
    tokens = tokenizer.encode("123")
    assert tokens == [49, 50, 51]
    framed = frame_source(tokenizer, "restore_reference")
    assert framed["ids"][:3] == [257, 308, 259]
    assert framed["source_start_state"] == 2
    assert tokenizer.decode(framed["source"].ids) == "restore_reference"
    with pytest.raises(ValueError):
        ByteBPE.train(["a"], 1)
