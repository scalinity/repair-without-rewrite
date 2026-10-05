"""Owned v1.2 Transformer math. FP32 leaves, differentiable working casts.

Weights are stored [output,input]; this is the transpose of the specification's
notation. Masks are boolean with True meaning allowed. No learned cache/position
objects exist. Tiny configs qualify math, not the exact MODEL-0 architecture.
"""
from dataclasses import dataclass
import math

import mlx.core as mx
import mlx.nn as nn
from mlx.utils import tree_flatten


class MLXRNG:
    """Explicit keyed MLX RNG, so continuation never relies on opaque global state."""

    def __init__(self, seed=42, key=None):
        self.key = mx.random.key(seed) if key is None else key

    def next(self):
        keys = mx.random.split(self.key, 2)
        self.key = keys[0]
        return keys[1]


@dataclass(frozen=True)
class ModelConfig:
    vocab_size: int = 16384
    width: int = 256
    num_layers: int = 6
    q_heads: int = 4
    kv_heads: int = 2
    ffn_width: int = 704
    max_context: int = 1024

    def __post_init__(self):
        if min(self.vocab_size, self.width, self.num_layers, self.q_heads,
               self.kv_heads, self.ffn_width, self.max_context) <= 0:
            raise ValueError("all model dimensions must be positive")
        if self.width % self.q_heads or self.q_heads % self.kv_heads:
            raise ValueError("width/head or query/KV grouping mismatch")
        if (self.width // self.q_heads) % 2:
            raise ValueError("adjacent RoPE needs an even head dimension")

    def parameter_count(self):
        d, k, f = self.width, self.kv_heads * (self.width // self.q_heads), self.ffn_width
        return self.vocab_size*d + self.num_layers*(2*d*d+2*d*k+3*d*f+2*d)+d


@dataclass(frozen=True)
class EncoderDecoderConfig:
    vocab_size: int = 16384
    width: int = 768
    encoder_layers: int = 8
    decoder_layers: int = 4
    q_heads: int = 12
    kv_heads: int = 4
    ffn_width: int = 2048
    max_context: int = 1024

    def __post_init__(self):
        ModelConfig(self.vocab_size, self.width, self.decoder_layers,
                    self.q_heads, self.kv_heads, self.ffn_width, self.max_context)
        if self.encoder_layers <= 0:
            raise ValueError("encoder_layers must be positive")

    def parameter_count(self):
        d, k, f = self.width, self.kv_heads*(self.width//self.q_heads), self.ffn_width
        return (self.vocab_size*d + self.encoder_layers*(4*d*d+3*d*f+2*d)
                + self.decoder_layers*(4*d*d+4*d*k+3*d*f+3*d)+2*d)


def parameter_inventory(model):
    seen, inventory = set(), []
    for name, value in tree_flatten(model.trainable_parameters()):
        if id(value) in seen:
            raise ValueError("aliased trainable leaves: keep one tied embedding owner")
        seen.add(id(value))
        inventory.append({"name": name, "shape": list(value.shape),
                          "dtype": str(value.dtype), "count": value.size})
    return inventory


class Linear(nn.Module):
    def __init__(self, input_dim, output_dim, rng, std=.02):
        super().__init__()
        self.weight = mx.random.normal((output_dim, input_dim), key=rng.next()) * std

    def __call__(self, x, dtype=mx.float32):
        return x.astype(dtype) @ self.weight.astype(dtype).T


class RMSNorm(nn.Module):
    def __init__(self, width, eps=1e-6):
        super().__init__()
        self.weight = mx.ones((width,), dtype=mx.float32)
        self._eps = eps

    def __call__(self, x, dtype=mx.float32):
        xf = x.astype(mx.float32)
        return (xf * mx.rsqrt(mx.mean(xf*xf, axis=-1, keepdims=True)+self._eps)
                * self.weight).astype(dtype)


def rope(x, offset=0, base=10000.):
    """Adjacent real pairs; Q/K only. Input [B,H,T,D]."""
    d = x.shape[-1]
    if d % 2 or offset < 0:
        raise ValueError("even head dimension and nonnegative offset required")
    angles = mx.arange(offset, offset+x.shape[-2], dtype=mx.float32)[:, None] * (
        base ** (-mx.arange(0, d, 2, dtype=mx.float32)/d))[None, :]
    pairs = x.astype(mx.float32).reshape(*x.shape[:-1], d//2, 2)
    even, odd = pairs[..., 0], pairs[..., 1]
    rotated = mx.stack((even*mx.cos(angles)-odd*mx.sin(angles),
                        even*mx.sin(angles)+odd*mx.cos(angles)), axis=-1)
    return rotated.reshape(x.shape).astype(x.dtype)


def attention_reference(q, k, v, mask=None):
    """Transparent explicit head repetition, FP32 scores/softmax."""
    if q.shape[1] % k.shape[1]:
        raise ValueError("query heads must group evenly over KV heads")
    repetitions = q.shape[1]//k.shape[1]
    k = mx.repeat(k, repetitions, axis=1).astype(mx.float32)
    v = mx.repeat(v, repetitions, axis=1).astype(mx.float32)
    scores = (q.astype(mx.float32) @ k.swapaxes(-1, -2))/math.sqrt(q.shape[-1])
    if mask is not None:
        scores = mx.where(mask, scores, -mx.inf)
    probabilities = mx.softmax(scores, axis=-1)
    return (probabilities @ v).astype(q.dtype)


def attention_native(q, k, v, mask=None):
    """Pinned MLX GQA; no forced fused path or mask removal."""
    return mx.fast.scaled_dot_product_attention(q, k, v,
                                               scale=q.shape[-1]**-.5, mask=mask)


def attention_mask(query_length, key_length, *, causal=False, offset=0, valid=None):
    mask = None
    if causal:
        mask = (mx.arange(key_length)[None, :] <=
                mx.arange(offset, offset+query_length)[:, None])[None, None, :, :]
    if valid is not None:
        if valid.ndim != 2 or valid.shape[-1] != key_length or valid.dtype != mx.bool_:
            raise ValueError("valid key mask must be bool [B,key_length]")
        if not bool(mx.all(mx.any(valid, axis=-1)).item()):
            raise ValueError("all-masked source/example is invalid")
        padding = valid[:, None, None, :]
        mask = padding if mask is None else mask & padding
    if mask is not None and not bool(mx.all(mx.any(mask, axis=-1)).item()):
        raise ValueError("all-masked attention row is invalid")
    return mask


class Attention(nn.Module):
    def __init__(self, width, q_heads, kv_heads, rng, output_std=.02, rotary=True):
        super().__init__()
        self.q = Linear(width, width, rng)
        self.k = Linear(width, kv_heads*(width//q_heads), rng)
        self.v = Linear(width, kv_heads*(width//q_heads), rng)
        self.o = Linear(width, width, rng, output_std)
        self._q_heads, self._kv_heads, self._head_dim = q_heads, kv_heads, width//q_heads
        self._rotary = rotary

    def _heads(self, x, n):
        return x.reshape(x.shape[0], x.shape[1], n, self._head_dim).transpose(0, 2, 1, 3)

    def __call__(self, x, *, context=None, causal=False, valid=None, cache=None,
                 dtype=mx.float32, backend="reference"):
        cross = context is not None
        offset = 0 if cache is None or cross else cache[0].shape[-2]
        q = self._heads(self.q(x, dtype), self._q_heads)
        if cross and cache is not None:
            k, v = cache
        else:
            keys = x if context is None else context
            k = self._heads(self.k(keys, dtype), self._kv_heads)
            v = self._heads(self.v(keys, dtype), self._kv_heads)
            if self._rotary:
                k = rope(k, offset)
            if cache is not None:
                k, v = mx.concatenate((cache[0], k), axis=-2), mx.concatenate((cache[1], v), axis=-2)
        if self._rotary:
            q = rope(q, offset)
        mask = attention_mask(q.shape[-2], k.shape[-2], causal=causal, offset=offset, valid=valid)
        if backend not in ("reference", "native"):
            raise ValueError("unknown attention backend")
        fn = attention_reference if backend == "reference" else attention_native
        out = fn(q, k, v, mask).transpose(0, 2, 1, 3).reshape(x.shape)
        return self.o(out, dtype), (k, v)


class SwiGLU(nn.Module):
    def __init__(self, width, hidden, rng, output_std=.02):
        super().__init__()
        self.gate, self.up = Linear(width, hidden, rng), Linear(width, hidden, rng)
        self.down = Linear(hidden, width, rng, output_std)

    def __call__(self, x, dtype=mx.float32):
        gate = self.gate(x, dtype)
        return self.down((gate * mx.sigmoid(gate))*self.up(x, dtype), dtype)


class Block(nn.Module):
    def __init__(self, width, q_heads, kv_heads, ffn_width, rng, std, cross=False):
        super().__init__()
        self.attention_norm = RMSNorm(width)
        self.attention = Attention(width, q_heads, kv_heads, rng, std)
        self.ffn_norm = RMSNorm(width)
        self.ffn = SwiGLU(width, ffn_width, rng, std)
        if cross:
            self.cross_norm = RMSNorm(width)
            self.cross_attention = Attention(width, q_heads, kv_heads, rng, std, rotary=False)

    def __call__(self, x, *, causal=False, valid=None, context=None, source_valid=None,
                 cache=None, dtype=mx.float32, backend="reference"):
        self_cache = None if cache is None else cache.get("self")
        branch, self_cache = self.attention(self.attention_norm(x, dtype), causal=causal,
                                             valid=valid, cache=self_cache, dtype=dtype, backend=backend)
        x = x + branch
        result_cache = {"self": self_cache}
        if context is not None:
            cross_cache = None if cache is None else cache.get("cross")
            branch, cross_cache = self.cross_attention(self.cross_norm(x, dtype), context=context,
                valid=source_valid, cache=cross_cache, dtype=dtype, backend=backend)
            x = x + branch
            result_cache["cross"] = cross_cache
        return x + self.ffn(self.ffn_norm(x, dtype), dtype), result_cache


class DecoderLM(nn.Module):
    def __init__(self, config=ModelConfig(), seed=42):
        super().__init__()
        self._config = config
        rng = MLXRNG(seed)
        self.embedding = mx.random.normal((config.vocab_size, config.width), key=rng.next())*.02
        std = .02/math.sqrt(2*config.num_layers)
        self.layers = [Block(config.width, config.q_heads, config.kv_heads, config.ffn_width, rng, std)
                       for _ in range(config.num_layers)]
        self.final_norm = RMSNorm(config.width)

    @property
    def config(self):
        return self._config

    def __call__(self, ids, *, valid=None, caches=None, dtype=mx.float32,
                 backend="reference", return_cache=False):
        offset = 0 if caches is None else caches[0]["self"][0].shape[-2]
        if ids.ndim != 2 or ids.shape[1] == 0 or ids.shape[1]+offset > self._config.max_context:
            raise ValueError("invalid decoder context")
        x, new_caches = self.embedding[ids].astype(dtype), []
        for i, layer in enumerate(self.layers):
            x, cache = layer(x, causal=True, valid=valid,
                cache=None if caches is None else caches[i], dtype=dtype, backend=backend)
            new_caches.append(cache)
        logits = self.final_norm(x, dtype) @ self.embedding.astype(dtype).T
        return (logits, new_caches) if return_cache else logits

    def greedy(self, prompt, max_new_tokens, eos_id=258, dtype=mx.float32, backend="reference"):
        if prompt.ndim != 2 or prompt.shape[0] != 1 or max_new_tokens < 0:
            raise ValueError("greedy accepts one prompt and a nonnegative token cap")
        generated, caches, current = [], None, prompt
        status = "capped"
        for _ in range(max_new_tokens):
            logits, caches = self(current, caches=caches, dtype=dtype, backend=backend, return_cache=True)
            token = int(mx.argmax(logits[0, -1]).item())
            generated.append(token)
            if token == eos_id:
                status = "completed"
                break
            current = mx.array([[token]], dtype=mx.int32)
            if caches[0]["self"][0].shape[-2] >= self._config.max_context:
                break
        return {"token_ids": generated, "status": status}


class EncoderDecoder(nn.Module):
    def __init__(self, config=EncoderDecoderConfig(), seed=42):
        super().__init__()
        self._config = config
        rng = MLXRNG(seed)
        self.embedding = mx.random.normal((config.vocab_size, config.width), key=rng.next())*.02
        self.encoder = [Block(config.width, config.q_heads, config.q_heads, config.ffn_width,
                             rng, .02/math.sqrt(2*config.encoder_layers))
                        for _ in range(config.encoder_layers)]
        self.decoder = [Block(config.width, config.q_heads, config.kv_heads, config.ffn_width,
                             rng, .02/math.sqrt(3*config.decoder_layers), cross=True)
                        for _ in range(config.decoder_layers)]
        self.encoder_norm, self.decoder_norm = RMSNorm(config.width), RMSNorm(config.width)

    @property
    def config(self):
        return self._config

    def encode(self, source_ids, source_valid=None, dtype=mx.float32, backend="reference"):
        if source_ids.ndim != 2 or not 0 < source_ids.shape[1] <= self._config.max_context:
            raise ValueError("invalid encoder context")
        x = self.embedding[source_ids].astype(dtype)
        for layer in self.encoder:
            x, _ = layer(x, valid=source_valid, dtype=dtype, backend=backend)
        return self.encoder_norm(x, dtype)

    def decode(self, decoder_ids, encoder_states, source_valid=None, decoder_valid=None,
               caches=None, dtype=mx.float32, backend="reference", inputs=None):
        x = self.embedding[decoder_ids].astype(dtype) if inputs is None else inputs.astype(dtype)
        offset = 0 if caches is None else caches[0]["self"][0].shape[-2]
        if x.ndim != 3 or not 0 < x.shape[1]+offset <= self._config.max_context:
            raise ValueError("invalid decoder context")
        new_caches = []
        for i, layer in enumerate(self.decoder):
            x, cache = layer(x, causal=True, valid=decoder_valid, context=encoder_states,
                             source_valid=source_valid, cache=None if caches is None else caches[i],
                             dtype=dtype, backend=backend)
            new_caches.append(cache)
        return self.decoder_norm(x, dtype), new_caches

    def logits(self, hidden, dtype=mx.float32):
        return hidden.astype(dtype) @ self.embedding.astype(dtype).T

    def __call__(self, source_ids, decoder_ids, source_valid=None, decoder_valid=None,
                 dtype=mx.float32, backend="reference"):
        encoded = self.encode(source_ids, source_valid, dtype, backend)
        hidden, _ = self.decode(decoder_ids, encoded, source_valid, decoder_valid,
                                dtype=dtype, backend=backend)
        return self.logits(hidden, dtype)


def masked_cross_entropy(logits, targets, valid):
    """Return FP32 loss sum; caller owns whole-update denominator and shifting."""
    if targets.shape != logits.shape[:-1] or valid.shape != targets.shape:
        raise ValueError("loss shape mismatch")
    z = logits.astype(mx.float32)
    selected = mx.take_along_axis(z, targets[..., None], axis=-1)[..., 0]
    return mx.sum(mx.where(valid, mx.logsumexp(z, axis=-1)-selected, 0))


def causal_loss(model, ids, target_valid=None, dtype=mx.float32, backend="reference"):
    if ids.shape[-1] < 2:
        raise ValueError("shifted loss requires at least two tokens")
    valid = mx.ones(ids[:, 1:].shape, dtype=mx.bool_) if target_valid is None else target_valid
    logits = model(ids[:, :-1], dtype=dtype, backend=backend)
    return masked_cross_entropy(logits, ids[:, 1:], valid)
