import math
import random

import mlx.core as mx
import mlx.nn as nn
from mlx.utils import tree_flatten
import numpy as np
import pytest

from src.models.core import DecoderLM, ModelConfig, causal_loss
from src.models.training import AdamW, TokenSchedule, Trainer, flat_parameters, load_checkpoint, save_checkpoint


def tiny_model(seed=42):
    return DecoderLM(ModelConfig(16, 8, 1, 2, 1, 12, 32), seed=seed)


def train_one(trainer, ids):
    trainer.accumulate(ids)
    return trainer.update()


def test_adamw_two_scalar_updates_and_matrix_only_decay():
    p = {"matrix": mx.array([[1.]], dtype=mx.float32), "norm": mx.array([1.], dtype=mx.float32)}
    opt = AdamW(p, clip_norm=100.)
    expected, m, v = 1., 0., 0.
    expected_norm = 1.
    for step, gradient in enumerate((.25, -.5), 1):
        p, norm = opt.apply(p, {k: mx.full(x.shape, gradient) for k, x in p.items()}, .01)
        m, v = .9*m+.1*gradient, .95*v+.05*gradient**2
        change = .01*(m/(1-.9**step))/(math.sqrt(v/(1-.95**step))+1e-8)
        expected = expected*(1-.01*.1)-change
        expected_norm -= change
        assert p["matrix"].item() == pytest.approx(expected, abs=1e-6)
        assert p["norm"].item() == pytest.approx(expected_norm, abs=1e-6)
        assert opt.step == step
        assert all(x.dtype == mx.float32 for x in [*opt.m.values(), *opt.v.values()])


def test_global_clip_and_nonfinite_stop():
    p = {"x": mx.array([1., 2.])}
    opt = AdamW(p)
    updated, norm = opt.apply(p, {"x": mx.array([3., 4.])}, .01)
    assert norm == 5.
    np.testing.assert_allclose(np.asarray(opt.m["x"]), [.06, .08], atol=1e-7)
    with pytest.raises(FloatingPointError):
        opt.apply(updated, {"x": mx.array([mx.nan, 0.])}, .01)
    assert opt.step == 1


def test_token_schedule_exact_positions_and_boundaries():
    s = TokenSchedule(10000)
    assert s(0) == 0
    assert s(200) == 3e-4
    assert s(5100) == pytest.approx(.000165)
    assert s(10000) == pytest.approx(3e-5)
    assert s(20000) == pytest.approx(3e-5)


def test_uneven_accumulation_and_tied_update_once():
    ids = mx.array([[1, 2, 3, 4], [2, 3, 4, 5], [4, 5, 6, 7]])
    valid = mx.array([[True, True, True], [True, False, False], [True, True, False]])
    full = Trainer(tiny_model(), TokenSchedule(10000))
    split = Trainer(tiny_model(), TokenSchedule(10000))
    full.accumulate(ids, valid)
    split.accumulate(ids[:1], valid[:1])
    split.accumulate(ids[1:], valid[1:])
    # Normwise relative tolerance avoids treating near-zero elements as meaningful ratios.
    for k, value in full.accumulator.gradients().items():
        a, b = np.asarray(value), np.asarray(split.accumulator.gradients()[k])
        assert np.linalg.norm(a-b)/max(np.linalg.norm(a), 1e-12) < 1e-5
    initial = np.asarray(full.model.embedding).copy()
    gradient = full.accumulator.gradients()["embedding"]
    lr = full.schedule(ids.size)
    # Independently execute one AdamW first update for the tied matrix.
    g = np.asarray(gradient)
    factor = min(1., 1./math.sqrt(sum(float(mx.sum(v*v).item()) for v in full.accumulator.gradients().values())))
    g = g*factor
    expected = initial*(1-lr*.1)-lr*g/(np.abs(g)+1e-8)
    f, s = full.update(), split.update()
    np.testing.assert_allclose(np.asarray(full.model.embedding), expected, atol=1e-7, rtol=1e-5)
    assert full.optimizer.step == split.optimizer.step == 1
    assert len([k for k in full.optimizer.m if k == "embedding"]) == 1
    for k, value in flat_parameters(full.model).items():
        np.testing.assert_allclose(np.asarray(value), np.asarray(flat_parameters(split.model)[k]), atol=1e-7, rtol=1e-5)


def test_bf16_work_fp32_master_gradient_state():
    trainer = Trainer(tiny_model(), TokenSchedule(10000), dtype=mx.bfloat16, backend="native")
    trainer.accumulate(mx.array([[1, 2, 3, 4]]))
    assert all(v.dtype == mx.float32 for v in trainer.accumulator.values.values())
    trainer.update()
    assert trainer.dtype_inventory() == {"master": ["mlx.core.float32"], "moment_m": ["mlx.core.float32"],
        "moment_v": ["mlx.core.float32"], "accumulator": ["mlx.core.float32"], "working": "mlx.core.bfloat16"}


@pytest.mark.parametrize("mid_accumulation", [False, True])
def test_checkpoint_twenty_updates_mid_accumulation_rng_and_identities(tmp_path, mid_accumulation):
    ids = mx.array([[1, 2, 3, 4], [4, 5, 6, 7]])
    options = {"identities": {"model": "tiny_dev", "tokenizer": "fixture_v1", "dataset": "fixture_v1"}}
    control = Trainer(tiny_model(), TokenSchedule(10000), **options)
    for _ in range(3):
        train_one(control, ids)
    control.data_order = [2, 0, 1]
    if mid_accumulation:
        control.accumulate(ids[:1])
    save_checkpoint(control, tmp_path/"checkpoint")
    draws = (random.random(), np.random.random(), np.asarray(control.rng.next()).copy(),
             control.augmentation_rng.integers(0, 10000))
    baseline = []
    if mid_accumulation:
        control.accumulate(ids[1:])
        baseline.append(control.update())
    for _ in range(20):
        baseline.append(train_one(control, ids))
    resumed = Trainer(tiny_model(seed=43), TokenSchedule(10000), **options)
    meta = load_checkpoint(resumed, tmp_path/"checkpoint")
    assert resumed.data_order == [2, 0, 1]
    assert (random.random(), np.random.random()) == draws[:2]
    np.testing.assert_array_equal(np.asarray(resumed.rng.next()), draws[2])
    assert resumed.augmentation_rng.integers(0, 10000) == draws[3]
    trajectory = []
    if mid_accumulation:
        resumed.accumulate(ids[1:])
        trajectory.append(resumed.update())
    for _ in range(20):
        trajectory.append(train_one(resumed, ids))
    assert baseline == trajectory
    assert resumed.processed_tokens == control.processed_tokens
    assert resumed.data_cursor == control.data_cursor
    for k, value in flat_parameters(control.model).items():
        np.testing.assert_array_equal(np.asarray(value), np.asarray(flat_parameters(resumed.model)[k]))
    (tmp_path/"checkpoint"/"metadata.json").write_text("corruption")
    with pytest.raises(ValueError, match="checksum"):
        load_checkpoint(resumed, tmp_path/"checkpoint")


def test_reproducibility_same_seed_and_data():
    ids = mx.array([[1, 2, 3, 4], [4, 5, 6, 7]])
    trajectories = []
    for _ in range(2):
        trainer = Trainer(tiny_model(), TokenSchedule(10000))
        trajectories.append([train_one(trainer, ids) for _ in range(4)])
    assert trajectories[0] == trajectories[1]
