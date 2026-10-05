import math

import mlx.core as mx
import mlx.nn as nn
from mlx.utils import tree_flatten
import numpy as np
import pytest

from src.models.core import (
    Attention, Block, DecoderLM, EncoderDecoder, EncoderDecoderConfig, Linear,
    MLXRNG, ModelConfig, RMSNorm, SwiGLU, attention_mask, attention_native,
    attention_reference, causal_loss, masked_cross_entropy, parameter_inventory, rope,
)


def tiny():
    return ModelConfig(32, 16, 2, 4, 2, 24, 64)


def array(x):
    mx.eval(x)
    return np.asarray(x.astype(mx.float32))


def test_exact_model0_count_and_shapes():
    model = DecoderLM()
    inventory = parameter_inventory(model)
    assert sum(x["count"] for x in inventory) == 8621312 == ModelConfig().parameter_count()
    assert len(inventory) == 56
    assert sum(x["name"] == "embedding" for x in inventory) == 1
    assert all(x["dtype"] == "mlx.core.float32" for x in inventory)
    assert model.embedding.shape == (16384, 256)
    assert model.layers[0].attention.k.weight.shape == (128, 256)
    assert model.layers[0].ffn.gate.weight.shape == (704, 256)
    logits = model(mx.array([[0, 1, 2, 3]], dtype=mx.int32))
    assert logits.shape == (1, 4, 16384)
    assert np.isfinite(array(logits)).all()


def test_seq2seq_analytic_counts_and_tiny_enumeration():
    assert EncoderDecoderConfig().parameter_count() == 100686336
    config = EncoderDecoderConfig(32, 16, 2, 1, 4, 2, 24, 64)
    model = EncoderDecoder(config)
    assert sum(x["count"] for x in parameter_inventory(model)) == config.parameter_count()
    assert model.encoder[0].attention.k.weight.shape == (16, 16)
    assert model.decoder[0].cross_attention.k.weight.shape == (8, 16)
    assert not model.decoder[0].cross_attention._rotary


def test_rms_scalar_reference_and_zero():
    x = np.array([[[1., 2., 3., 4.], [0, 0, 0, 0]]], dtype=np.float32)
    norm = RMSNorm(4)
    norm.weight = mx.array([1., 2., 3., 4.])
    expected = x/np.sqrt(np.mean(x*x, -1, keepdims=True)+1e-6)*np.array([1, 2, 3, 4])
    np.testing.assert_allclose(array(norm(mx.array(x))), expected, atol=1e-6, rtol=1e-6)


def numpy_decoder_forward(weights, config, ids):
    """Independent whole-model NumPy FP64 arrangement; no core math calls."""
    def norm(x, weight):
        return x/np.sqrt(np.mean(x*x, axis=-1, keepdims=True)+1e-6)*weight

    def rotate(x):
        out = x.copy()
        for t in range(x.shape[-2]):
            for j in range(x.shape[-1]//2):
                angle = t*10000**(-2*j/x.shape[-1])
                a, b = x[..., t, 2*j], x[..., t, 2*j+1]
                out[..., t, 2*j] = a*math.cos(angle)-b*math.sin(angle)
                out[..., t, 2*j+1] = a*math.sin(angle)+b*math.cos(angle)
        return out

    d, h, hk = config.width, config.q_heads, config.kv_heads
    x = weights["embedding"][ids]
    for layer in range(config.num_layers):
        prefix = f"layers.{layer}."
        normalized = norm(x, weights[prefix+"attention_norm.weight"])
        q, k, v = [normalized@weights[prefix+f"attention.{part}.weight"].T for part in ("q", "k", "v")]
        q = rotate(q.reshape(*q.shape[:-1], h, d//h).transpose(0, 2, 1, 3))
        k = rotate(k.reshape(*k.shape[:-1], hk, d//h).transpose(0, 2, 1, 3))
        v = v.reshape(*v.shape[:-1], hk, d//h).transpose(0, 2, 1, 3)
        scores = q@np.repeat(k, h//hk, axis=1).swapaxes(-1, -2)/math.sqrt(d//h)
        scores = np.where(np.tril(np.ones((ids.shape[1], ids.shape[1]), dtype=bool)), scores, -np.inf)
        exp = np.exp(scores-np.max(scores, axis=-1, keepdims=True))
        attended = (exp/exp.sum(axis=-1, keepdims=True))@np.repeat(v, h//hk, axis=1)
        branch = attended.transpose(0, 2, 1, 3).reshape(x.shape)@weights[prefix+"attention.o.weight"].T
        x = x+branch
        normalized = norm(x, weights[prefix+"ffn_norm.weight"])
        gate, up = [normalized@weights[prefix+f"ffn.{part}.weight"].T for part in ("gate", "up")]
        x = x+(gate/(1+np.exp(-gate))*up)@weights[prefix+"ffn.down.weight"].T
    return norm(x, weights["final_norm.weight"])@weights["embedding"].T


def test_tiny_explicit_full_forward_independent_numpy_oracle():
    from mlx.utils import tree_unflatten
    config = ModelConfig(8, 4, 2, 2, 1, 6, 16)
    model = DecoderLM(config)
    weights = {}
    for number, (name, value) in enumerate(tree_flatten(model.parameters())):
        explicit = (np.sin(np.arange(value.size).reshape(value.shape)+number)*.04).astype(np.float32)
        if value.ndim == 1:
            explicit += 1
        weights[name] = explicit.astype(np.float64)
    model.update(tree_unflatten([(name, mx.array(value.astype(np.float32))) for name, value in weights.items()]))
    ids = np.array([[1, 2, 3, 4], [4, 3, 2, 1]], dtype=np.int32)
    expected = numpy_decoder_forward(weights, config, ids)
    for backend in ("reference", "native"):
        np.testing.assert_allclose(array(model(mx.array(ids), backend=backend)), expected, atol=1e-5, rtol=1e-4)


def test_rope_adjacent_zero_norm_relative_dot():
    x = mx.array(np.arange(1, 25, dtype=np.float32).reshape(1, 1, 3, 8)/10)
    np.testing.assert_array_equal(array(rope(x))[..., 0, :], array(x)[..., 0, :])
    np.testing.assert_allclose(np.linalg.norm(array(rope(x)), axis=-1),
                               np.linalg.norm(array(x), axis=-1), atol=1e-6)
    # Independent scalar rotation calculation at nonzero cache offset.
    expected = array(x).copy()
    for t in range(3):
        for j in range(4):
            angle = (t+7)*10000**(-2*j/8)
            a, b = array(x)[0, 0, t, 2*j:2*j+2]
            expected[0, 0, t, 2*j] = a*math.cos(angle)-b*math.sin(angle)
            expected[0, 0, t, 2*j+1] = a*math.sin(angle)+b*math.cos(angle)
    np.testing.assert_allclose(array(rope(x, 7)), expected, atol=1e-6)
    one, other = x[..., :1, :], x[..., 1:2, :]
    same_shift = np.sum(array(rope(one, 9))*array(rope(other, 12)))
    relative = np.sum(array(one)*array(rope(other, 3)))
    np.testing.assert_allclose(same_shift, relative, atol=1e-5)


@pytest.mark.parametrize("dtype", [mx.float32, mx.bfloat16])
@pytest.mark.parametrize("causal", [False, True])
def test_native_gqa_independent_numpy_and_gradient_parity(dtype, causal):
    rng = np.random.default_rng(42)
    q, k, v = [mx.array(rng.normal(0, .3, s).astype(np.float32)).astype(dtype)
               for s in ((2, 4, 3, 8), (2, 2, 3, 8), (2, 2, 3, 8))]
    valid = mx.array([[True, True, False], [True, True, True]])
    mask = attention_mask(3, 3, causal=causal, valid=valid)
    # NumPy oracle owns head repeat, matrix multiplication, masking and softmax.
    qn, kn, vn = array(q), np.repeat(array(k), 2, axis=1), np.repeat(array(v), 2, axis=1)
    scores = qn@kn.swapaxes(-1, -2)/np.sqrt(8)
    scores = np.where(np.asarray(mask), scores, -np.inf)
    exp = np.exp(scores-np.max(scores, -1, keepdims=True))
    expected = (exp/exp.sum(-1, keepdims=True))@vn
    native, reference = attention_native(q, k, v, mask), attention_reference(q, k, v, mask)
    atol, rtol = (1e-5, 1e-4) if dtype == mx.float32 else (.02, .02)
    np.testing.assert_allclose(array(native), expected, atol=atol, rtol=rtol)
    np.testing.assert_allclose(array(native), array(reference), atol=atol, rtol=rtol)
    fn_ref = lambda q, k, v: mx.sum(attention_reference(q, k, v, mask).astype(mx.float32)**2)
    fn_nat = lambda q, k, v: mx.sum(attention_native(q, k, v, mask).astype(mx.float32)**2)
    gr, gn = mx.grad(fn_ref, argnums=(0, 1, 2))(q, k, v), mx.grad(fn_nat, argnums=(0, 1, 2))(q, k, v)
    for a, b in zip(gr, gn):
        np.testing.assert_allclose(array(a), array(b), atol=atol, rtol=rtol)
        assert float(np.sum(array(a)*array(b))) > 0


@pytest.mark.parametrize("backend", ["reference", "native"])
def test_causal_no_future_leakage_and_cache_chunks(backend):
    model = DecoderLM(tiny())
    ids = mx.array([[1, 4, 2, 3, 7, 9, 10, 11]])
    changed = mx.array([[1, 4, 2, 3, 18, 19, 20, 21]])
    full = model(ids, backend=backend)
    np.testing.assert_array_equal(array(full[:, :4]), array(model(changed, backend=backend)[:, :4]))
    for chunks in ([1]*8, [3, 1, 4]):
        outputs, caches, cursor = [], None, 0
        for length in chunks:
            result, caches = model(ids[:, cursor:cursor+length], backend=backend,
                                   caches=caches, return_cache=True)
            outputs.append(result)
            cursor += length
        np.testing.assert_allclose(array(mx.concatenate(outputs, axis=1)), array(full), atol=1e-5, rtol=1e-4)


def test_encoder_bidirectional_and_cross_padding_cache():
    model = EncoderDecoder(EncoderDecoderConfig(32, 16, 1, 1, 4, 2, 24, 64))
    valid = mx.array([[True, True, False]])
    ids = mx.array([[1, 2, 3]])
    changed_padding = mx.array([[1, 2, 29]])
    encoded = model.encode(ids, valid)
    changed_encoded = model.encode(changed_padding, valid)
    np.testing.assert_array_equal(array(encoded[:, :2]), array(changed_encoded[:, :2]))
    assert not np.allclose(array(encoded[:, 0]), array(model.encode(mx.array([[1, 9, 3]]), valid)[:, 0]), atol=1e-6)
    decoder_ids = mx.array([[4, 5, 6, 7, 8]])
    hidden, _ = model.decode(decoder_ids, encoded, valid)
    hidden_padded, _ = model.decode(decoder_ids, changed_encoded, valid)
    np.testing.assert_array_equal(array(hidden), array(hidden_padded))
    first, caches = model.decode(decoder_ids[:, :1], encoded, valid)
    later, new_caches = model.decode(decoder_ids[:, 1:], encoded, valid, caches=caches)
    assert new_caches[0]["cross"][0] is caches[0]["cross"][0]
    np.testing.assert_allclose(array(mx.concatenate((first, later), axis=1)), array(hidden), atol=1e-5, rtol=1e-4)
    with pytest.raises(ValueError, match="all-masked"):
        model.encode(ids, mx.array([[False, False, False]]))


def test_linear_swiglu_and_residual_scalar_oracle():
    rng = MLXRNG(42)
    swiglu = SwiGLU(2, 3, rng)
    swiglu.gate.weight = mx.array([[.1, .2], [-.3, .4], [.5, -.6]])
    swiglu.up.weight = mx.array([[.7, .8], [.9, -.1], [.2, -.3]])
    swiglu.down.weight = mx.array([[.2, .4, .6], [.1, -.3, -.5]])
    x = np.array([[1., 2.], [3., 4.]], dtype=np.float32)
    gate, up = x@array(swiglu.gate.weight).T, x@array(swiglu.up.weight).T
    expected = ((gate/(1+np.exp(-gate)))*up)@array(swiglu.down.weight).T
    np.testing.assert_allclose(array(swiglu(mx.array(x))), expected, atol=1e-6)
    block = Block(4, 2, 1, 6, rng, .01)
    block.attention.o.weight = mx.zeros_like(block.attention.o.weight)
    block.ffn.down.weight = mx.zeros_like(block.ffn.down.weight)
    x = mx.array([[[1., 2., 3., 4.], [2., 3., 4., 5.]]])
    out, _ = block(x, causal=True)
    np.testing.assert_array_equal(array(out), array(x))


def test_loss_shift_padding_and_uniform():
    logits = mx.zeros((1, 3, 8))
    targets, valid = mx.array([[1, 2, 3]]), mx.array([[True, False, True]])
    assert float(masked_cross_entropy(logits, targets, valid).item()) == pytest.approx(2*math.log(8))
    z = np.array([[[1., 2., -1.], [3., -2., 1.], [0., 1., 2.]]], np.float32)
    expected = sum(math.log(sum(math.exp(float(y)) for y in z[0, t]))-z[0, t, target]
                   for t, target in ((0, 1), (2, 2)))
    assert masked_cross_entropy(mx.array(z), mx.array([[1, 0, 2]]), valid).item() == pytest.approx(expected, abs=1e-6)
    model = DecoderLM(tiny())
    ids = mx.array([[1, 2, 3, 4]])
    expected = masked_cross_entropy(model(ids[:, :-1]), ids[:, 1:], mx.ones((1, 3), dtype=mx.bool_))
    assert causal_loss(model, ids).item() == expected.item()


def test_repeatable_forward_fp32_bf16_and_all_gradients_finite():
    model, ids = DecoderLM(tiny()), mx.array([[1, 2, 3, 4], [4, 3, 2, 1]])
    for dtype in (mx.float32, mx.bfloat16):
        one, two = model(ids, dtype=dtype), model(ids, dtype=dtype)
        np.testing.assert_array_equal(array(one), array(two))
        loss, grads = nn.value_and_grad(model, lambda m: causal_loss(m, ids, dtype=dtype))(model)
        assert math.isfinite(loss.item())
        assert all(v.dtype == mx.float32 and np.isfinite(array(v)).all()
                   and np.linalg.norm(array(v)) > 0 for _, v in tree_flatten(grads))
    np.testing.assert_allclose(array(model(ids, dtype=mx.bfloat16)), array(model(ids)), atol=.02, rtol=.02)


def test_finite_difference_independent_linear_and_model_leaves():
    # Scalar loss with well-conditioned nonzero gradients; independent central differences.
    layer = Linear(2, 2, MLXRNG(42))
    layer.weight = mx.array([[.2, -.4], [.5, .3]])
    x = mx.array([[.7, -.8], [.2, .6]])
    fn = lambda m: mx.sum(m(x)**2)
    _, grads = nn.value_and_grad(layer, fn)(layer)
    analytic = array(grads["weight"])
    initial = array(layer.weight)
    for index in np.ndindex(initial.shape):
        losses = []
        for sign in (-1, 1):
            value = initial.copy()
            value[index] += sign*.001
            layer.weight = mx.array(value)
            losses.append(fn(layer).item())
        numerical = (losses[1]-losses[0])/.002
        assert abs(numerical-analytic[index])/abs(analytic[index]) < 1e-3
    model, ids = DecoderLM(ModelConfig(8, 4, 1, 2, 1, 6, 16)), mx.array([[1, 2, 3, 4]])
    _, grads = nn.value_and_grad(model, lambda m: causal_loss(m, ids))(model)
    # Embedding + residual-down leaves: pick the largest derivative to avoid ill conditioning.
    for path in ("embedding", "layers.0.ffn.down.weight"):
        leaves = dict(tree_flatten(model.parameters()))
        original, analytic = array(leaves[path]), array(dict(tree_flatten(grads))[path])
        index = np.unravel_index(np.argmax(np.abs(analytic)), analytic.shape)
        # Independently recompute numerical derivatives in NumPy FP64; FP32
        # loss subtraction is ill-conditioned for the small down projection.
        weights = {k: array(v).astype(np.float64) for k, v in leaves.items()}
        step = .0001
        losses = []
        for sign in (-1, 1):
            value = original.astype(np.float64).copy()
            value[index] += sign*step
            weights[path] = value
            logits = numpy_decoder_forward(weights, model.config, np.asarray(ids[:, :-1]))
            exp = np.exp(logits-np.max(logits, axis=-1, keepdims=True))
            lognormalizer = np.log(exp.sum(-1))+np.max(logits, axis=-1)
            selected = np.take_along_axis(logits, np.asarray(ids[:, 1:])[..., None], axis=-1)[..., 0]
            losses.append(float(np.sum(lognormalizer-selected)))
        numerical = (losses[1]-losses[0])/(2*step)
        assert abs(numerical-analytic[index])/abs(analytic[index]) < 1e-3


def test_greedy_deterministic_completed_and_cap():
    model = DecoderLM(tiny())
    model.embedding = mx.zeros_like(model.embedding)
    prompt = mx.array([[1, 2]])
    assert model.greedy(prompt, 3, eos_id=0) == {"token_ids": [0], "status": "completed"}
    assert model.greedy(prompt, 3, eos_id=31) == {"token_ids": [0, 0, 0], "status": "capped"}
