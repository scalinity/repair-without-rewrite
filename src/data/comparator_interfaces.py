"""Weight-free development conformance for official comparator interfaces."""
from __future__ import annotations

BYT5_PAD, BYT5_EOS, BYT5_OFFSET, IGNORE_INDEX = 0, 1, 3, -100


def byt5_ids(text: str, *, qualified_capacity: int | None = None) -> list[int]:
    ids = [b + BYT5_OFFSET for b in text.encode("utf-8", "strict")] + [BYT5_EOS]
    if qualified_capacity is not None and len(ids) > qualified_capacity:
        raise ValueError("native byte length exceeds qualified capacity; do not truncate")
    return ids


def byt5_batch(sources: list[str], targets: list[str], *, source_capacity: int,
               target_capacity: int) -> dict[str, list[list[int]]]:
    if not sources or len(sources) != len(targets):
        raise ValueError("nonempty paired source/target batch required")
    inputs = [byt5_ids(s, qualified_capacity=source_capacity) for s in sources]
    labels = [byt5_ids(t, qualified_capacity=target_capacity) for t in targets]
    source_len, target_len = max(map(len, inputs)), max(map(len, labels))
    padded = [s + [BYT5_PAD] * (source_len - len(s)) for s in inputs]
    masked = [t + [IGNORE_INDEX] * (target_len - len(t)) for t in labels]
    decoder = [[BYT5_PAD] + [BYT5_PAD if i == IGNORE_INDEX else i for i in t[:-1]] for t in masked]
    return {"input_ids": padded,
            "attention_mask": [[int(i != BYT5_PAD) for i in s] for s in padded],
            "labels": masked, "decoder_input_ids": decoder,
            "valid_target_counts": [len(t) for t in labels]}


def byt5_complete_text(ids: list[int]) -> str:
    if not ids or ids[-1] != BYT5_EOS or BYT5_EOS in ids[:-1]:
        raise ValueError("missing or nonterminal EOS")
    if any(not BYT5_OFFSET <= i <= 258 for i in ids[:-1]):
        raise ValueError("nonbyte generation requires explicit failure mapping")
    return bytes(i - BYT5_OFFSET for i in ids[:-1]).decode("utf-8", "strict")
