"""B100/C101 exact backbone and C teacher forcing, masks, component losses.

Development correctness code. Raw failures stay failures; the byte-copy
renderer carries no claim about which edit decisions are semantically safe.
"""
import math
import mlx.core as mx
from .core import EncoderDecoder, EncoderDecoderConfig, Linear, MLXRNG, masked_cross_entropy
from .edits import (BOS, EDIT, END_EDIT, Edit, EditProgram, EditContractError,
                    source_identity, codepoint_boundaries, render, normalized_component_loss)

B100_CONFIG = EncoderDecoderConfig()


class B100(EncoderDecoder):
    def greedy_text(self, source_ids, *, source_valid=None, max_tokens=1024,
                    eos_id=258, dtype=mx.float32, backend="reference"):
        if source_ids.shape[0] != 1:
            raise ValueError("greedy accepts one source")
        encoded = self.encode(source_ids, source_valid, dtype, backend)
        current, caches, generated = mx.array([[BOS]]), None, []
        for _ in range(min(max_tokens, self.config.max_context)):
            hidden, caches = self.decode(current, encoded, source_valid, caches=caches,
                                         dtype=dtype, backend=backend)
            token = int(mx.argmax(self.logits(hidden[:, -1:], dtype)[0, -1]).item())
            if token == eos_id:
                return {"token_ids": generated, "status": "completed"}
            generated.append(token)
            current = mx.array([[token]])
        return {"token_ids": generated, "status": "capped"}


def boundary_features(encoded, encoder_positions):
    """Position 0 is trusted source-start; later positions precede boundaries.

    The caller provides the complete content-token map including terminal.
    Legal UTF-8 boundary masking is separate, with no added boundary weights.
    """
    if encoded.shape[0] != 1 or not encoder_positions:
        raise ValueError("single source and source-start position required")
    if any(not 0 <= p < encoded.shape[1] for p in encoder_positions):
        raise ValueError("boundary encoder position outside source")
    return encoded[:, mx.array(encoder_positions, dtype=mx.int32), :]


def pointer_mask(legal, *, minimum_index=0):
    if legal.ndim != 1 or legal.dtype != mx.bool_:
        raise ValueError("legal pointer mask must be bool [boundaries]")
    result = legal & (mx.arange(legal.size) >= minimum_index)
    if not bool(mx.any(result).item()):
        raise EditContractError("no legal pointer target")
    return result


def validate_source_binding(source, source_token_ids, encoder_positions, byte_offsets, legal, token_to_bytes):
    """Bind original bytes, all content tokens and the complete pointer map.

    Pure Python validation precedes encoding. Only trusted reserved framing can
    lie before source-start; after content, only EOS/PAD framing is permitted.
    """
    raw = source.encode("utf-8", errors="strict")
    if not encoder_positions or len(byte_offsets) != len(encoder_positions) or len(legal) != len(byte_offsets):
        raise EditContractError("incomplete source boundary map")
    if any(type(p) is not int for p in encoder_positions) or any(type(p) is not int for p in byte_offsets):
        raise EditContractError("source boundary map is not integer-valued")
    start = encoder_positions[0]
    if not 0 <= start < len(source_token_ids) or source_token_ids[start] != 259:
        raise EditContractError("missing designated source-start separator")
    expected_positions = tuple(range(start,start+len(encoder_positions)))
    if tuple(encoder_positions) != expected_positions or encoder_positions[-1] >= len(source_token_ids):
        raise EditContractError("source content positions are not complete and ordered")
    if tuple(source_token_ids[:start]) not in ((308,), (257,308)):
        raise EditContractError("untrusted restore-reference framing before source-start")
    if any(token not in (256,258) for token in source_token_ids[encoder_positions[-1]+1:]):
        raise EditContractError("unmapped literal after source content")
    segments = []
    try:
        for position in encoder_positions[1:]:
            segment = token_to_bytes(source_token_ids[position])
            if not isinstance(segment,bytes) or not segment:
                raise EditContractError("content token has no literal byte map")
            segments.append(segment)
    except (KeyError,ValueError) as error:
        raise EditContractError("content token has invalid literal byte map") from error
    cumulative = [0]
    for segment in segments:
        cumulative.append(cumulative[-1]+len(segment))
    if b"".join(segments) != raw or tuple(cumulative) != tuple(byte_offsets):
        raise EditContractError("encoded source bytes or cumulative offsets mismatch")
    codepoints = set(codepoint_boundaries(source))
    expected_legal = tuple(offset in codepoints for offset in cumulative)
    if any(type(flag) is not bool for flag in legal) or tuple(legal) != expected_legal:
        raise EditContractError("source UTF-8 legal pointer flags mismatch")


class C101(EncoderDecoder):
    def __init__(self, config=B100_CONFIG, seed=42, pointer_width=128):
        super().__init__(config, seed)
        self._pointer_width = pointer_width
        rng = MLXRNG(seed + 100001)
        self.start_query = Linear(config.width, pointer_width, rng)
        self.start_key = Linear(config.width, pointer_width, rng)
        self.end_query = Linear(config.width, pointer_width, rng)
        self.end_key = Linear(config.width, pointer_width, rng)
        self.action = Linear(config.width, 3, rng)
        self.action_bias = mx.zeros((3,), dtype=mx.float32)

    def action_logits(self, hidden, dtype=mx.float32):
        return self.action(hidden, dtype) + self.action_bias.astype(dtype)

    def pointer_logits(self, hidden, boundaries, *, end=False, legal=None, minimum_index=0,
                       dtype=mx.float32):
        query = (self.end_query if end else self.start_query)(hidden, dtype)
        keys = (self.end_key if end else self.start_key)(boundaries, dtype)
        scores = (query.astype(mx.float32) @ keys.astype(mx.float32).swapaxes(-1, -2))/math.sqrt(self._pointer_width)
        if legal is not None:
            scores = mx.where(pointer_mask(legal, minimum_index=minimum_index), scores, -mx.inf)
        return scores

    def teacher_inputs(self, labels, boundaries, dtype=mx.float32):
        vectors = []
        for event in labels.inputs:
            if event.kind == "token":
                vector = self.embedding[event.value].astype(dtype)
            else:
                token = EDIT if event.kind == "start_feedback" else END_EDIT
                vector = self.embedding[token].astype(dtype) + boundaries[0, event.value].astype(dtype)
            vectors.append(vector)
        return mx.stack(vectors)[None, :, :]

    def component_sums(self, source_ids, labels, encoder_positions, legal,
                       *, source_valid=None, dtype=mx.float32, backend="reference"):
        """One example loss sums; denominator comes from the queued update."""
        encoded = self.encode(source_ids, source_valid, dtype, backend)
        boundaries = boundary_features(encoded, encoder_positions)
        inputs = self.teacher_inputs(labels, boundaries, dtype)
        hidden, _ = self.decode(None, encoded, source_valid, inputs=inputs,
                                dtype=dtype, backend=backend)
        zero = mx.array(0., dtype=mx.float32)
        sums = {key: zero for key in labels.denominators}
        if labels.action:
            positions, targets = zip(*labels.action)
            logits = self.action_logits(hidden[:, mx.array(positions)], dtype)
            target = mx.array([targets], dtype=mx.int32)
            sums["action"] = masked_cross_entropy(logits, target, mx.ones(target.shape, dtype=mx.bool_))
        previous_end = 0
        for (start_position, a), (end_position, b) in zip(labels.start, labels.end):
            for key, position, target, is_end, minimum in (
                    ("start", start_position, a, False, previous_end),
                    ("end", end_position, b, True, a)):
                logits = self.pointer_logits(hidden[:, position:position+1], boundaries, end=is_end,
                                             legal=legal, minimum_index=minimum, dtype=dtype)
                if not bool(pointer_mask(legal, minimum_index=minimum)[target].item()):
                    raise EditContractError("illegal teacher-forced pointer")
                sums[key] = sums[key] + masked_cross_entropy(logits, mx.array([[target]]), mx.array([[True]]))
            previous_end = b
        if labels.vocabulary:
            positions, targets = zip(*labels.vocabulary)
            logits = self.logits(hidden[:, mx.array(positions)], dtype)
            target = mx.array([targets], dtype=mx.int32)
            sums["vocabulary"] = masked_cross_entropy(logits, target, mx.ones(target.shape, dtype=mx.bool_))
        return sums

    def greedy_edits(self, source, source_ids, encoder_positions, byte_offsets, legal,
                     token_to_bytes, *, source_valid=None, max_edits=64, max_decoder_positions=None,
                     dtype=mx.float32, backend="reference"):
        """Bounded deterministic greedy state machine with strict final rendering."""
        if source_ids.ndim != 2 or source_ids.shape[0] != 1:
            raise EditContractError("one encoded source is required")
        validate_source_binding(source, source_ids.tolist()[0], encoder_positions, byte_offsets,
                                legal.tolist(), token_to_bytes)
        if source_valid is not None:
            if source_valid.shape != source_ids.shape or source_valid.dtype != mx.bool_:
                raise EditContractError("invalid source validity mask")
            flags = source_valid.tolist()[0]
            if any(not flags[p] for p in encoder_positions):
                raise EditContractError("source content or source-start is masked out")
        encoded = self.encode(source_ids, source_valid, dtype, backend)
        boundaries = boundary_features(encoded, encoder_positions)
        position_cap = self.config.max_context if max_decoder_positions is None else min(max_decoder_positions, self.config.max_context)
        if position_cap < 1:
            raise EditContractError("positive decoder position cap required")
        cache, positions, edits, previous_end = None, 0, [], 0
        def advance(vector):
            nonlocal cache, positions
            if positions >= position_cap:
                raise EditContractError("decoder context exhausted")
            hidden, cache = self.decode(None, encoded, source_valid, caches=cache,
                inputs=vector[None, None, :], dtype=dtype, backend=backend)
            positions += 1
            return hidden
        try:
            hidden = advance(self.embedding[BOS].astype(dtype))
            while True:
                action = int(mx.argmax(self.action_logits(hidden, dtype)[0, -1]).item())
                if action in (1, 2):
                    terminal = "END" if action == 1 else "ABSTAIN"
                    program = EditProgram(*source_identity(source), tuple(edits), terminal)
                    if terminal == "ABSTAIN":
                        return {"program": program, "status": "abstained", "output": None, "decoder_positions": positions}
                    output = render(source, program, pointer_boundaries=[p for p, ok in zip(byte_offsets, legal.tolist()) if ok])
                    return {"program": program, "status": "completed", "output": output, "decoder_positions": positions}
                if len(edits) >= max_edits:
                    raise EditContractError("edit count exhausted")
                a = int(mx.argmax(self.pointer_logits(hidden, boundaries, legal=legal,
                    minimum_index=previous_end, dtype=dtype)[0, -1]).item())
                hidden = advance(self.embedding[EDIT].astype(dtype) + boundaries[0, a])
                b = int(mx.argmax(self.pointer_logits(hidden, boundaries, end=True, legal=legal,
                    minimum_index=a, dtype=dtype)[0, -1]).item())
                hidden = advance(self.embedding[END_EDIT].astype(dtype) + boundaries[0, b])
                replacement = []
                while True:
                    logits = self.logits(hidden, dtype)[0, -1].astype(mx.float32)
                    allowed = (mx.arange(logits.size) < 256) | (mx.arange(logits.size) >= 320) | (mx.arange(logits.size) == END_EDIT)
                    token = int(mx.argmax(mx.where(allowed, logits, -mx.inf)).item())
                    hidden = advance(self.embedding[token].astype(dtype))
                    if token == END_EDIT:
                        break
                    replacement.append(token_to_bytes(token))
                value = b"".join(replacement).decode("utf-8", errors="strict")
                edits.append(Edit(byte_offsets[a], byte_offsets[b], value)); previous_end = b
        except (ValueError, KeyError) as error:
            return {"program": None, "status": "invalid_or_capped", "output": None,
                    "reason": str(error), "decoder_positions": positions}


def c_microbatch_loss(model, examples, denominators, *, dtype=mx.float32):
    sums = {key: mx.array(0., dtype=mx.float32) for key in denominators}
    for example in examples:
        component = model.component_sums(**example, dtype=dtype)
        sums = {key: sums[key] + component[key] for key in sums}
    return normalized_component_loss(sums, denominators)
