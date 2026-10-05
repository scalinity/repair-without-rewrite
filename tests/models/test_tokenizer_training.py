"""Fixture parity only: no released development/final material enters training."""
import hashlib
import json
import random

import pytest

from src.models.tokenizer import ByteBPE
from src.models.tokenizer_training import train_development_byte_bpe


def trained(texts, count, *, digit_isolation=False):
    manifest = hashlib.sha256(json.dumps(texts, ensure_ascii=False).encode()).hexdigest()
    return train_development_byte_bpe(texts, count,
                                     training_manifest_sha256=manifest,
                                     digit_isolation=digit_isolation)


@pytest.mark.parametrize("texts,count", [
    (["aaaaa", "aaaab", "ababa"], 5),
    (["ab", "ba", "aa", "bb"], 3),
    (["abc abc abc", "abc def def", "xy xy xy"], 12),
    (["", "🙂🙂", "e\u0301 é", "<BOS> --dry-run", "  a\t\r\n"], 12),
])
@pytest.mark.parametrize("digit_isolation", [False, True])
def test_incremental_exact_merge_and_encoding_parity(texts, count, digit_isolation):
    oracle = ByteBPE.train(texts, count, digit_isolation=digit_isolation)
    actual, _ = trained(texts, count, digit_isolation=digit_isolation)
    assert actual.merges == oracle.merges
    for text in texts + ["unseen 🙂 --flag e\u0301 123 abc"]:
        assert actual.encode(text) == oracle.encode(text)
        assert actual.decode(actual.encode(text)) == text


def test_incremental_random_fixture_parity_and_order_invariance():
    rng = random.Random(20261005)
    for _ in range(30):
        texts = ["".join(rng.choice("aaabbbcde 012🙂é") for _ in range(60)) for _ in range(4)]
        for policy in (False, True):
            actual, _ = trained(texts, 24, digit_isolation=policy)
            oracle = ByteBPE.train(texts, 24, digit_isolation=policy)
            reordered, _ = trained(list(reversed(texts)), 24, digit_isolation=policy)
            assert actual.merges == oracle.merges == reordered.merges


def test_document_boundaries_and_overlapping_pair_counts():
    with pytest.raises(ValueError, match="exhausted"):
        trained(["a", "b"], 1)
    actual, _ = trained(["aaa", "bc", "bc"], 1)
    assert actual.merges == ((97, 97),)  # Both pairs occur twice; numeric tie chooses aa.


def test_receipt_determinism_hashes_bytes_and_unique_documents():
    texts = ["🙂", "a\r\n", "🙂", ""]
    one, receipt = trained(texts, 2)
    two, again = trained(texts, 2)
    assert one.merges == two.merges and receipt == again
    assert receipt["input_documents"] == 4
    assert receipt["unique_document_contents"] == 3
    assert receipt["training_utf8_bytes"] == 11
    assert receipt["vocab_size"] == 322
    assert receipt["config"]["normalization"] == "none"
    assert receipt["status"] == "DEVELOPMENT_ONLY_NOT_PAPER_FROZEN"
    for key in ("training_manifest_sha256", "trainer_implementation_sha256",
                "tokenizer_implementation_sha256", "ordered_corpus_content_sha256",
                "reserved_map_canonical_sha256", "merge_list_canonical_sha256"):
        assert len(receipt[key]) == 64
    _, reversed_receipt = trained(list(reversed(texts)), 2)
    assert receipt["ordered_corpus_content_sha256"] != reversed_receipt["ordered_corpus_content_sha256"]


def test_stream_input_matches_list_and_rejects_invalid_types():
    texts = ["abc abc", "xyz xyz"]
    expected, receipt = trained(texts, 4)
    actual, streamed = train_development_byte_bpe(iter(texts), 4,
        training_manifest_sha256=receipt["training_manifest_sha256"])
    assert actual.merges == expected.merges and streamed == receipt
    for count in (True, 1.0, "1", -1, 16065):
        with pytest.raises(ValueError):
            trained(texts, count)
    for manifest in ("", "synthetic_fixture", "f" * 63, "F" * 64):
        with pytest.raises(ValueError):
            train_development_byte_bpe(texts, 1, training_manifest_sha256=manifest)
    with pytest.raises(ValueError):
        trained(texts, 1, digit_isolation="false")
    with pytest.raises(UnicodeEncodeError):
        trained(["\ud800"], 0)
