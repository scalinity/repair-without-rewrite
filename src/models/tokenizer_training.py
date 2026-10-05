"""Incremental byte-BPE training with the educational trainer's exact merge rule.

The caller must admit the supplied training documents before invoking this
trainer. A manifest hash records lineage; it does not establish admission.
"""
from array import array
import hashlib
import heapq
import json
from pathlib import Path

from src.models.tokenizer import ByteBPE, SPECIAL_TOKENS


def _hash_json(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def train_development_byte_bpe(texts, merge_count=16064, *,
                               training_manifest_sha256, digit_isolation=False):
    """Return a tokenizer and deterministic lineage receipt without saving files.

    Count all adjacent pairs, including overlapping occurrences. Select the
    most frequent pair, breaking ties by its ascending numeric symbol tuple;
    replace nonoverlapping occurrences from left to right within each segment.
    These are the rules in ByteBPE.train, with no changed pretokenization.
    """
    if type(merge_count) is not int or not 0 <= merge_count <= 16064:
        raise ValueError("merge count outside canonical vocabulary")
    if (not isinstance(training_manifest_sha256, str) or
            len(training_manifest_sha256) != 64 or
            any(c not in "0123456789abcdef" for c in training_manifest_sha256)):
        raise ValueError("training manifest must have a lowercase SHA256 hash")
    initial = ByteBPE(digit_isolation=digit_isolation)
    symbols, previous, following = (array("i") for _ in range(3))
    document_count = training_bytes = 0
    unique_documents = set()
    corpus_hash = hashlib.sha256()
    for text in texts:
        data = text.encode("utf-8", errors="strict")
        document_count += 1
        training_bytes += len(data)
        unique_documents.add(hashlib.sha256(data).hexdigest())
        corpus_hash.update(len(data).to_bytes(8, "big"))
        corpus_hash.update(data)
        for segment in initial._segments(data):
            if not segment:
                continue
            start, length = len(symbols), len(segment)
            if start + length > 2**31 - 1:
                raise ValueError("training input exceeds signed node-index capacity")
            symbols.extend(segment)
            previous.extend(range(start - 1, start + length - 1))
            following.extend(range(start + 1, start + length + 1))
            previous[start] = following[-1] = -1

    positions = {}
    for left, right in enumerate(following):
        if right != -1:
            positions.setdefault((symbols[left], symbols[right]), set()).add(left)
    heap = [(-len(nodes), pair) for pair, nodes in positions.items()]
    heapq.heapify(heap)
    merges = []
    for rank in range(merge_count):
        while heap:
            negative_count, pair = heapq.heappop(heap)
            if -negative_count == len(positions.get(pair, ())) and negative_count < 0:
                break
        else:
            raise ValueError("training supply exhausted before requested merges")
        merges.append(pair)
        changed = set()

        def remove_edge(left):
            if left == -1 or following[left] == -1:
                return
            edge = (symbols[left], symbols[following[left]])
            positions[edge].remove(left)
            changed.add(edge)

        def add_edge(left):
            if left == -1 or following[left] == -1:
                return
            edge = (symbols[left], symbols[following[left]])
            positions.setdefault(edge, set()).add(left)
            changed.add(edge)

        # Node indices preserve segment order; deleted overlap nodes are skipped.
        for left in sorted(positions[pair]):
            right = following[left]
            if symbols[left] == -1 or right == -1 or (symbols[left], symbols[right]) != pair:
                continue
            before, after = previous[left], following[right]
            remove_edge(before)
            remove_edge(left)
            remove_edge(right)
            symbols[left] = 320 + rank
            symbols[right] = -1
            following[left] = after
            if after != -1:
                previous[after] = left
            add_edge(before)
            add_edge(left)
        for edge in changed:
            if positions[edge]:
                heapq.heappush(heap, (-len(positions[edge]), edge))
            else:
                del positions[edge]

    tokenizer = ByteBPE(merges, digit_isolation=digit_isolation)
    receipt = {
        "schema": "development_byte_bpe_training_receipt_v1",
        "status": "DEVELOPMENT_ONLY_NOT_PAPER_FROZEN",
        "training_manifest_sha256": training_manifest_sha256,
        "trainer_implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "tokenizer_implementation_sha256": hashlib.sha256(Path(__file__).with_name("tokenizer.py").read_bytes()).hexdigest(),
        "config": {"trainer": "incremental_linked_occurrences_v1", "merge_count": merge_count,
                   "digit_isolation": digit_isolation, "encoding": "UTF-8-strict",
                   "normalization": "none", "document_boundaries": "never_merge_across",
                   "pair_counts": "all_adjacent_including_overlaps",
                   "tie_policy": "descending_count_then_ascending_numeric_pair",
                   "replacement_policy": "left_to_right_nonoverlapping",
                   "seed": None, "order_policy": "ordered_length_prefixed_UTF8_documents"},
        "input_documents": document_count,
        "unique_document_contents": len(unique_documents),
        "training_utf8_bytes": training_bytes,
        "ordered_corpus_content_sha256": corpus_hash.hexdigest(),
        "reserved_map_canonical_sha256": _hash_json(SPECIAL_TOKENS),
        "merge_list_canonical_sha256": _hash_json(merges),
        "vocab_size": tokenizer.vocab_size,
    }
    return tokenizer, receipt
