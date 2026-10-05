"""C's source-relative byte renderer and canonical teacher-forced events.

The minimum-edit label alignment uses Unicode scalar values, with the earliest
optimal edit chosen by the fixed DELETE, INSERT, REPLACE, MATCH order. It never
normalizes the text. Pointer coordinates are original UTF-8 bytes.
"""
from dataclasses import dataclass
import hashlib

BOS, EDIT, END_EDIT = 257, 266, 267


class EditContractError(ValueError):
    pass


@dataclass(frozen=True)
class Edit:
    start: int
    end: int
    replacement: str


@dataclass(frozen=True)
class EditProgram:
    source_sha256: str
    source_byte_length: int
    edits: tuple[Edit, ...]
    terminal: str = "END"


def source_identity(source: str) -> tuple[str, int]:
    raw = source.encode("utf-8", errors="strict")
    return hashlib.sha256(raw).hexdigest(), len(raw)


def codepoint_boundaries(source: str) -> tuple[int, ...]:
    offsets = [0]
    for char in source:
        offsets.append(offsets[-1] + len(char.encode("utf-8", errors="strict")))
    return tuple(offsets)


def legal_token_boundaries(source: str, token_bytes: tuple[bytes, ...]) -> tuple[int, ...]:
    raw = source.encode("utf-8", errors="strict")
    if b"".join(token_bytes) != raw or any(not token for token in token_bytes):
        raise EditContractError("token byte map does not reproduce exact source")
    boundaries, offset = [0], 0
    legal = set(codepoint_boundaries(source))
    for token in token_bytes:
        offset += len(token)
        if offset in legal:
            boundaries.append(offset)
    return tuple(boundaries)


def render(source: str, program: EditProgram, *, pointer_boundaries=None) -> str:
    """Validate the complete program before copying any source gap."""
    raw = source.encode("utf-8", errors="strict")
    if (program.source_sha256, program.source_byte_length) != source_identity(source):
        raise EditContractError("source hash or byte length mismatch")
    if program.terminal != "END":
        raise EditContractError("ABSTAIN" if program.terminal == "ABSTAIN" else "missing or unknown terminal END")
    legal = set(codepoint_boundaries(source))
    if pointer_boundaries is not None:
        legal &= set(pointer_boundaries)
    cursor = 0
    replacements = []
    for edit in program.edits:
        if not isinstance(edit.start, int) or not isinstance(edit.end, int):
            raise EditContractError("pointer is not an integer")
        if not 0 <= edit.start <= edit.end <= len(raw):
            raise EditContractError("illegal byte interval")
        if edit.start not in legal or edit.end not in legal:
            raise EditContractError("illegal UTF-8 or token boundary")
        if edit.start < cursor:
            raise EditContractError("unordered or overlapping edits")
        replacements.append(edit.replacement.encode("utf-8", errors="strict"))
        cursor = edit.end
    # Original coordinates are used throughout, including repeated literals.
    parts, cursor = [], 0
    for edit, replacement in zip(program.edits, replacements):
        parts.extend((raw[cursor:edit.start], replacement))
        cursor = edit.end
    parts.append(raw[cursor:])
    return b"".join(parts).decode("utf-8", errors="strict")


def canonical_labels(source: str, target: str, token_bytes: tuple[bytes, ...]) -> EditProgram:
    """Minimal scalar-value edits, expanded/merged onto legal BPE boundaries."""
    sb, tb = codepoint_boundaries(source), codepoint_boundaries(target)
    legal = legal_token_boundaries(source, token_bytes)
    n, m = len(source), len(target)
    distance = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n:
                distance[i][j] = m - j
            elif j == m:
                distance[i][j] = n - i
            else:
                distance[i][j] = min(1 + distance[i+1][j], 1 + distance[i][j+1],
                                     (source[i] != target[j]) + distance[i+1][j+1])
    i = j = 0
    vertices = {0: [0]}
    changed = []
    active = None
    while i < n or j < m:
        old_i, old_j = i, j
        best = distance[i][j]
        if i < n and best == 1 + distance[i+1][j]:
            i += 1; kind = "edit"
        elif j < m and best == 1 + distance[i][j+1]:
            j += 1; kind = "edit"
        elif i < n and j < m and source[i] != target[j] and best == 1 + distance[i+1][j+1]:
            i += 1; j += 1; kind = "edit"
        else:
            i += 1; j += 1; kind = "match"
        if kind == "edit":
            if active is None:
                active = [sb[old_i], sb[i]]
            active[1] = sb[i]
        elif active is not None:
            changed.append(active); active = None
        vertices.setdefault(sb[i], []).append(tb[j])
    if active is not None:
        changed.append(active)
    expanded = []
    for a, b in changed:
        a = max(p for p in legal if p <= a)
        b = min(p for p in legal if p >= b)
        if expanded and a <= expanded[-1][1]:
            expanded[-1][1] = max(b, expanded[-1][1])
        else:
            expanded.append([a, b])
    target_raw = target.encode("utf-8", errors="strict")
    edits = tuple(Edit(a, b, target_raw[min(vertices[a]):max(vertices[b])].decode("utf-8"))
                  for a, b in expanded)
    identity = source_identity(source)
    program = EditProgram(*identity, edits)
    if render(source, program, pointer_boundaries=legal) != target:
        raise EditContractError("canonical alignment failed exact reconstruction")
    return program


@dataclass(frozen=True)
class EventInput:
    kind: str  # token, start_feedback, end_feedback
    value: int


@dataclass(frozen=True)
class EventLabels:
    inputs: tuple[EventInput, ...]
    action: tuple[tuple[int, int], ...]  # EDIT=0, END=1, ABSTAIN=2
    start: tuple[tuple[int, int], ...]
    end: tuple[tuple[int, int], ...]
    vocabulary: tuple[tuple[int, int], ...]
    replacement_tokens: int

    @property
    def denominators(self):
        return {"action": len(self.action), "start": len(self.start),
                "end": len(self.end), "vocabulary": len(self.vocabulary)}


def events(program: EditProgram, encode, byte_boundary_to_index: dict[int, int],
           *, max_context: int = 1024) -> EventLabels:
    if program.terminal not in ("END", "ABSTAIN"):
        raise EditContractError("missing or unknown terminal")
    inputs = [EventInput("token", BOS)]
    action, start, end, vocabulary = [], [], [], []
    count, previous_end = 0, 0
    for edit in program.edits:
        if not 0 <= previous_end <= edit.start <= edit.end <= program.source_byte_length:
            raise EditContractError("illegal ordered event interval")
        if edit.start not in byte_boundary_to_index or edit.end not in byte_boundary_to_index:
            raise EditContractError("event pointer is not a legal source boundary")
        previous_end = edit.end
        a, b = byte_boundary_to_index[edit.start], byte_boundary_to_index[edit.end]
        position = len(inputs) - 1
        action.append((position, 0)); start.append((position, a))
        inputs.append(EventInput("start_feedback", a))
        end.append((len(inputs) - 1, b))
        inputs.append(EventInput("end_feedback", b))
        replacement = tuple(encode(edit.replacement))
        if any(token < 0 or 256 <= token < 320 for token in replacement):
            raise EditContractError("reserved control emitted as ordinary replacement")
        count += len(replacement)
        for token in replacement + (END_EDIT,):
            vocabulary.append((len(inputs) - 1, token))
            inputs.append(EventInput("token", token))
    action.append((len(inputs) - 1, 1 if program.terminal == "END" else 2))
    if len(inputs) > max_context:
        raise EditContractError(f"decoder context overflow: {len(inputs)} > {max_context}")
    result = EventLabels(tuple(inputs), tuple(action), tuple(start), tuple(end), tuple(vocabulary), count)
    k = len(program.edits)
    assert len(inputs) == 1 + count + 3*k and len(vocabulary) == count + k
    return result


def update_denominators(label_batches) -> dict[str, int]:
    result = {key: 0 for key in ("action", "start", "end", "vocabulary")}
    for batch in label_batches:
        for label in batch:
            for key, count in label.denominators.items():
                result[key] += count
    return result


def normalized_component_loss(loss_sums, denominators, weights=None):
    """One microbatch's differentiable loss; the accumulator needs no division."""
    if set(loss_sums) != set(denominators):
        raise EditContractError("component sums and whole-update counts differ")
    result = 0.0
    for key, denominator in denominators.items():
        if denominator < 0:
            raise EditContractError("negative component count")
        if denominator:
            result = result + (weights or {}).get(key, 1.0) * loss_sums[key] / denominator
    return result
