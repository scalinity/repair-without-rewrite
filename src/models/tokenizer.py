"""Reversible byte-BPE development interface with the canonical v1.2 ID map.

An untrained instance has 320 entries, not a fabricated 16k tokenizer. A final
artifact must supply all 16,064 learned merges from permitted training material.
"""
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

PAD, BOS, EOS, SEP = 256, 257, 258, 259
IDENTITY, ABSTAIN, EDIT, END_EDIT = 264, 265, 266, 267
RESTORE_REFERENCE = 308
SPECIAL_TOKENS = {256: "PAD", 257: "BOS", 258: "EOS", 259: "SEP",
                  260: "lm", 261: "clean", 262: "corrections", 263: "denoise",
                  264: "IDENTITY", 265: "ABSTAIN", 266: "EDIT", 267: "END-EDIT"}
SPECIAL_TOKENS.update({268+i: x for i, x in enumerate(
    ("path", "URL", "identifier", "flag", "command", "version", "number", "term"))})
SPECIAL_TOKENS.update({276+i: f"SLOT-{i}" for i in range(32)})
SPECIAL_TOKENS[308] = "restore_reference"
SPECIAL_TOKENS.update({309+i: f"EXTENSION-{i}" for i in range(11)})


@dataclass(frozen=True)
class TokenizedSource:
    text: str
    ids: tuple
    byte_offsets: tuple
    legal_pointer_mask: tuple
    codepoint_byte_offsets: tuple
    source_hash: str


def _replace(tokens, pair, replacement):
    result, i = [], 0
    while i < len(tokens):
        if i+1 < len(tokens) and (tokens[i], tokens[i+1]) == pair:
            result.append(replacement)
            i += 2
        else:
            result.append(tokens[i])
            i += 1
    return result


class ByteBPE:
    def __init__(self, merges=(), *, digit_isolation=False):
        if type(digit_isolation) is not bool:
            raise ValueError("digit isolation must be a boolean")
        self.merges = tuple(tuple(p) for p in merges)
        self.digit_isolation = digit_isolation
        self.byte_map = {i: bytes([i]) for i in range(256)}
        self.ranks = {}
        for rank, pair in enumerate(self.merges):
            if len(pair) != 2 or any(type(v) is not int or v not in self.byte_map for v in pair) or pair in self.ranks:
                raise ValueError("invalid or duplicate BPE merge")
            self.ranks[pair] = rank
            self.byte_map[320+rank] = self.byte_map[pair[0]]+self.byte_map[pair[1]]
        if len(self.merges) > 16064:
            raise ValueError("v1.2 vocabulary exceeded")

    @property
    def vocab_size(self):
        return 320+len(self.merges)

    def _segments(self, data):
        if not self.digit_isolation:
            return [list(data)]
        result, chunk = [], []
        for byte in data:
            if 48 <= byte <= 57:
                if chunk:
                    result.append(chunk)
                    chunk = []
                result.append([byte])
            else:
                chunk.append(byte)
        if chunk:
            result.append(chunk)
        return result

    def encode(self, text):
        data = text.encode("utf-8", errors="strict")
        result = []
        for tokens in self._segments(data):
            while len(tokens) > 1:
                ranked = [(self.ranks[p], p) for p in zip(tokens, tokens[1:]) if p in self.ranks]
                if not ranked:
                    break
                rank, pair = min(ranked)
                tokens = _replace(tokens, pair, 320+rank)
            result.extend(tokens)
        return result

    def decode_bytes(self, ids):
        try:
            pieces = []
            for token_id in ids:
                if type(token_id) is not int:
                    raise ValueError("literal token IDs must be integers")
                pieces.append(self.byte_map[token_id])
            return b"".join(pieces)
        except KeyError as error:
            raise ValueError("reserved or unknown ID in literal byte decoding") from error

    def decode(self, ids):
        return self.decode_bytes(ids).decode("utf-8", errors="strict")

    def source(self, text):
        ids = self.encode(text)
        offsets = [0]
        for token in ids:
            offsets.append(offsets[-1]+len(self.byte_map[token]))
        codepoints = [0]
        for char in text:
            codepoints.append(codepoints[-1]+len(char.encode("utf-8")))
        legal = set(codepoints)
        return TokenizedSource(text, tuple(ids), tuple(offsets), tuple(x in legal for x in offsets),
                               tuple(codepoints), hashlib.sha256(text.encode("utf-8")).hexdigest())

    @classmethod
    def train(cls, texts, merge_count, *, digit_isolation=False):
        if type(merge_count) is not int or not 0 <= merge_count <= 16064:
            raise ValueError("merge count outside canonical vocabulary")
        tokenizer = cls(digit_isolation=digit_isolation)
        sequences = [segment for text in texts for segment in tokenizer._segments(text.encode("utf-8"))]
        merges = []
        for rank in range(merge_count):
            counts = Counter(pair for seq in sequences for pair in zip(seq, seq[1:]))
            if not counts:
                raise ValueError("training supply exhausted before requested merges")
            pair = min(counts, key=lambda p: (-counts[p], p))
            merges.append(pair)
            sequences = [_replace(seq, pair, 320+rank) for seq in sequences]
        return cls(merges, digit_isolation=digit_isolation)

    def save(self, directory, training_manifest_hash):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        artifact = {"schema": "localflow_byte_bpe_v1", "merges": self.merges,
                    "byte_map_hex": {str(k): v.hex() for k, v in self.byte_map.items()},
                    "vocab_size": self.vocab_size, "digit_isolation": self.digit_isolation,
                    "training_manifest_hash": training_manifest_hash,
                    "status": "DEVELOPMENT_NOT_FROZEN"}
        (directory/"tokenizer.json").write_text(json.dumps(artifact, sort_keys=True, indent=2)+"\n")
        (directory/"special_tokens.json").write_text(json.dumps(SPECIAL_TOKENS, sort_keys=True, indent=2)+"\n")
        return {name: hashlib.sha256((directory/name).read_bytes()).hexdigest()
                for name in ("tokenizer.json", "special_tokens.json")}

    @classmethod
    def load(cls, directory):
        directory = Path(directory)
        artifact = json.loads((directory/"tokenizer.json").read_text())
        specials = json.loads((directory/"special_tokens.json").read_text())
        if artifact["schema"] != "localflow_byte_bpe_v1" or specials != {str(k): v for k, v in SPECIAL_TOKENS.items()}:
            raise ValueError("tokenizer schema/reserved-map mismatch")
        tokenizer = cls(artifact["merges"], digit_isolation=artifact["digit_isolation"])
        if type(artifact["vocab_size"]) is not int or artifact["vocab_size"] != tokenizer.vocab_size or artifact["byte_map_hex"] != {str(k): v.hex() for k, v in tokenizer.byte_map.items()}:
            raise ValueError("tokenizer byte map or vocabulary mismatch")
        return tokenizer


def frame_source(tokenizer, text, task_id=RESTORE_REFERENCE):
    """Trusted development serializer; literal strings never allocate control IDs."""
    if type(task_id) is not int or task_id not in (260, 261, 262, 263, 308):
        raise ValueError("unsupported trusted task")
    source = tokenizer.source(text)
    return {"version": "dev_source_frame_v1_not_frozen", "ids": [BOS, task_id, SEP, *source.ids, EOS],
            "content_start": 3, "source_start_state": 2, "source": source}
