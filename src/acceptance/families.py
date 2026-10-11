"""NONSCIENTIFIC exact connected closure on directly supplied invented metadata."""
from dataclasses import dataclass
from itertools import combinations
import re
import unicodedata2 as unicode
from .features import distance
from .records import Family, Record, _hash
from .allocation import component_id


@dataclass(frozen=True)
class FamilyRecord(Record):
    stable_id: str
    text: str
    speaker: str | None = None
    recording: str | None = None
    verified_recording_aliases: tuple[str, ...] = ()
    prompt: str | None = None
    derivations: tuple[str, ...] = ()
    duplicate_audio_hash: str | None = None

    def __post_init__(self):
        super().__post_init__(); _hash(self.stable_id)
        self.text.encode("utf-8", "strict")
        for value in (self.speaker, self.recording, self.prompt, self.duplicate_audio_hash, *self.verified_recording_aliases, *self.derivations):
            if value is not None and not value: raise ValueError("missing identity is None, not empty")
        if self.duplicate_audio_hash is not None: _hash(self.duplicate_audio_hash)


def signature(text):
    return tuple(re.findall(r"\w+", unicode.normalize("NFC", text).casefold()))


def textual_link(a, b):
    if not a or not b: return False
    if a == b: return True
    if len(a) >= 20 and len(b) >= 20:
        aa = set(tuple(a[i:i+5]) for i in range(len(a)-4))
        bb = set(tuple(b[i:i+5]) for i in range(len(b)-4))
        if 10*len(aa & bb) >= 9*len(aa | bb): return True
    s, t = " ".join(a), " ".join(b)
    return distance(s, t) <= max(len(s), len(t))//10


def close_families(records: tuple[FamilyRecord, ...], known_links=()):
    """No eligibility input: every supplied bridge participates in exact closure."""
    items = sorted(records, key=lambda r: r.stable_id)
    by_id = {r.stable_id: i for i, r in enumerate(items)}
    if len(by_id) != len(items): raise ValueError("duplicate or conflicting identity")
    for row in items: row.__post_init__()
    parent = list(range(len(items)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    def join(i, j):
        a, b = find(i), find(j)
        if a != b: parent[max(a, b)] = min(a, b)
    for a, b in known_links:
        if a not in by_id or b not in by_id: raise ValueError("unknown derivation endpoint")
        join(by_id[a], by_id[b])
    signatures = [signature(r.text) for r in items]
    identifiers = []
    for r in items:
        ids = set()
        for namespace, values in (
            ("speaker", (r.speaker,)), ("recording", (r.recording, *r.verified_recording_aliases)),
            ("prompt", (r.prompt,)), ("derivation", r.derivations), ("audio", (r.duplicate_audio_hash,))):
            ids.update((namespace, v) for v in values if v is not None)
        identifiers.append(ids)
    for i, j in combinations(range(len(items)), 2):
        if identifiers[i] & identifiers[j] or textual_link(signatures[i], signatures[j]):
            join(i, j)
    groups = {}
    for i, record in enumerate(items): groups.setdefault(find(i), []).append(record.stable_id)
    return tuple(sorted((Family(component_id(tuple(members)), tuple(members)) for members in groups.values()), key=lambda f: f.component_id))
