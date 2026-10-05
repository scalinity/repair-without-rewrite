"""Explicit FP32 AdamW, token scheduling, accumulation and atomic resume state."""
from dataclasses import asdict, dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import random
import tempfile

import mlx.core as mx
import mlx.nn as nn
from mlx.utils import tree_flatten, tree_unflatten
import numpy as np

from .core import DecoderLM, MLXRNG, causal_loss


def flat_parameters(model):
    return dict(tree_flatten(model.trainable_parameters()))


@dataclass(frozen=True)
class TokenSchedule:
    planned_tokens: int
    peak_lr: float = 3e-4
    warmup_fraction: float = .02
    floor_fraction: float = .1

    def __post_init__(self):
        if self.planned_tokens <= 0 or self.peak_lr <= 0 or not 0 < self.warmup_fraction < 1:
            raise ValueError("invalid token schedule")
        if not 0 <= self.floor_fraction <= 1:
            raise ValueError("invalid LR floor")

    def __call__(self, tokens):
        if tokens < 0:
            raise ValueError("negative scheduler position")
        warmup = self.planned_tokens*self.warmup_fraction
        if tokens < warmup:
            return self.peak_lr*tokens/warmup
        fraction = min((tokens-warmup)/(self.planned_tokens-warmup), 1.)
        return self.peak_lr*(self.floor_fraction+(1-self.floor_fraction)*.5*(1+math.cos(math.pi*fraction)))


class GradientAccumulator:
    def __init__(self, parameters):
        self.values = {k: mx.zeros(v.shape, dtype=mx.float32) for k, v in parameters.items()}
        self.denominator = 0
        self.microbatches = 0

    def add(self, gradients, denominator=0):
        gradients = dict(tree_flatten(gradients))
        if gradients.keys() != self.values.keys() or denominator < 0:
            raise ValueError("gradient tree/denominator mismatch")
        for k, v in gradients.items():
            if v.shape != self.values[k].shape:
                raise ValueError("gradient shape mismatch")
            self.values[k] = self.values[k] + v.astype(mx.float32)
        self.denominator += denominator
        self.microbatches += 1
        mx.eval(self.values)

    def gradients(self, already_normalized=False):
        if self.microbatches == 0 or (not already_normalized and self.denominator <= 0):
            raise ValueError("no valid update")
        if already_normalized:
            return self.values
        return {k: v/self.denominator for k, v in self.values.items()}

    def clear(self):
        self.values = {k: mx.zeros(v.shape, dtype=mx.float32) for k, v in self.values.items()}
        self.denominator = self.microbatches = 0


class AdamW:
    """Bias corrected, decoupled decay once for each uniquely owned matrix."""
    def __init__(self, parameters, beta1=.9, beta2=.95, epsilon=1e-8, weight_decay=.1, clip_norm=1.):
        if any(v.dtype != mx.float32 for v in parameters.values()):
            raise ValueError("master parameters must be FP32")
        if not 0 <= beta1 < 1 or not 0 <= beta2 < 1 or epsilon <= 0 or weight_decay < 0 or clip_norm <= 0:
            raise ValueError("invalid AdamW policy")
        self.beta1, self.beta2, self.epsilon = beta1, beta2, epsilon
        self.weight_decay, self.clip_norm, self.step = weight_decay, clip_norm, 0
        self.m = {k: mx.zeros(v.shape, dtype=mx.float32) for k, v in parameters.items()}
        self.v = {k: mx.zeros(v.shape, dtype=mx.float32) for k, v in parameters.items()}

    def policy(self):
        return {"beta1": self.beta1, "beta2": self.beta2, "epsilon": self.epsilon,
                "weight_decay": self.weight_decay, "clip_norm": self.clip_norm}

    def apply(self, parameters, gradients, lr):
        if parameters.keys() != gradients.keys() or parameters.keys() != self.m.keys() or lr < 0:
            raise ValueError("optimizer tree/LR mismatch")
        if any(v.dtype != mx.float32 for v in parameters.values()):
            raise ValueError("optimizer requires FP32 master leaves")
        norm = mx.sqrt(sum(mx.sum(g.astype(mx.float32)**2) for g in gradients.values()))
        mx.eval(norm)
        norm_value = float(norm.item())
        if not math.isfinite(norm_value):
            raise FloatingPointError("nonfinite accumulated gradients; optimizer not advanced")
        factor = min(1., self.clip_norm/max(norm_value, 1e-30))
        self.step += 1
        updated = {}
        for k, parameter in parameters.items():
            g = gradients[k].astype(mx.float32)*factor
            self.m[k] = self.beta1*self.m[k]+(1-self.beta1)*g
            self.v[k] = self.beta2*self.v[k]+(1-self.beta2)*g*g
            mhat, vhat = self.m[k]/(1-self.beta1**self.step), self.v[k]/(1-self.beta2**self.step)
            decay = self.weight_decay if parameter.ndim >= 2 else 0.
            updated[k] = parameter*(1-lr*decay)-lr*mhat/(mx.sqrt(vhat)+self.epsilon)
        mx.eval(updated, self.m, self.v)
        if not all(bool(mx.all(mx.isfinite(v)).item()) for v in updated.values()):
            raise FloatingPointError("nonfinite optimizer state; run must stop")
        return updated, norm_value


class Trainer:
    def __init__(self, model, schedule, *, dtype=mx.float32, backend="reference", seed=42,
                 identities=None, optimizer_options=None):
        self.model, self.schedule, self.dtype, self.backend = model, schedule, dtype, backend
        parameters = flat_parameters(model)
        self.optimizer = AdamW(parameters, **(optimizer_options or {}))
        self.accumulator = GradientAccumulator(parameters)
        self.processed_tokens = 0
        self.pending_tokens = 0
        self.loss_sum = 0.
        self.data_cursor = 0
        self.data_order = []
        self.phase = "bounded_correctness"
        self.rng = MLXRNG(seed)
        self.augmentation_rng = np.random.default_rng(seed)
        self.identities = identities or {}
        self._loss_and_grad = nn.value_and_grad(model, lambda model, ids, valid:
            causal_loss(model, ids, valid, dtype=self.dtype, backend=self.backend))

    def accumulate(self, ids, target_valid=None, processed_tokens=None):
        valid = mx.ones(ids[:, 1:].shape, dtype=mx.bool_) if target_valid is None else target_valid
        count = int(mx.sum(valid).item())
        if count == 0:
            raise ValueError("microbatch has no valid targets")
        loss, gradients = self._loss_and_grad(self.model, ids, valid)
        mx.eval(loss, gradients)
        value = float(loss.item())
        if not math.isfinite(value):
            raise FloatingPointError("nonfinite microbatch loss")
        self.accumulator.add(gradients, count)
        tokens = ids.size if processed_tokens is None else processed_tokens
        if tokens < 0:
            raise ValueError("negative processed exposure")
        self.pending_tokens += tokens
        self.loss_sum += value
        self.data_cursor += ids.shape[0]
        return value/count

    def update(self, already_normalized=False):
        token_position = self.processed_tokens+self.pending_tokens
        lr = self.schedule(token_position)
        gradients = self.accumulator.gradients(already_normalized)
        parameters, norm = self.optimizer.apply(flat_parameters(self.model), gradients, lr)
        self.model.update(tree_unflatten(list(parameters.items())))
        result = {"step": self.optimizer.step, "lr": lr, "processed_tokens": token_position,
                  "valid_targets": self.accumulator.denominator,
                  "microbatches": self.accumulator.microbatches, "gradient_norm": norm,
                  "loss": self.loss_sum/max(self.accumulator.denominator, 1)}
        self.processed_tokens = token_position
        self.pending_tokens, self.loss_sum = 0, 0.
        self.accumulator.clear()
        mx.eval(self.model.parameters(), self.optimizer.m, self.optimizer.v, self.accumulator.values)
        return result

    def dtype_inventory(self):
        return {"master": sorted({str(v.dtype) for v in flat_parameters(self.model).values()}),
                "moment_m": sorted({str(v.dtype) for v in self.optimizer.m.values()}),
                "moment_v": sorted({str(v.dtype) for v in self.optimizer.v.values()}),
                "accumulator": sorted({str(v.dtype) for v in self.accumulator.values.values()}),
                "working": str(self.dtype)}


def _hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _tuples(value):
    return tuple(_tuples(x) for x in value) if isinstance(value, list) else value


def save_checkpoint(trainer, destination):
    """New directory only. Manifest, readback and forward check precede atomic rename."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError("checkpoint destination already exists")
    temporary = Path(tempfile.mkdtemp(prefix=destination.name+".partial-", dir=destination.parent))
    try:
        arrays = {}
        for prefix, values in (("model", flat_parameters(trainer.model)), ("m", trainer.optimizer.m),
                               ("v", trainer.optimizer.v), ("acc", trainer.accumulator.values)):
            arrays.update({prefix+"::"+k: np.asarray(v) for k, v in values.items()})
        arrays["mlx_rng"] = np.asarray(trainer.rng.key)
        np.savez(temporary/"arrays.npz", **arrays)
        numpy_state = np.random.get_state()
        meta = {"schema": "localflow_resume_v1", "config": asdict(trainer.model.config),
                "model_type": type(trainer.model).__name__, "identities": trainer.identities,
                "optimizer_policy": trainer.optimizer.policy(), "optimizer_step": trainer.optimizer.step,
                "schedule": asdict(trainer.schedule), "processed_tokens": trainer.processed_tokens,
                "pending_tokens": trainer.pending_tokens, "loss_sum": trainer.loss_sum,
                "acc_denominator": trainer.accumulator.denominator,
                "acc_microbatches": trainer.accumulator.microbatches,
                "data_cursor": trainer.data_cursor, "data_order": trainer.data_order, "phase": trainer.phase,
                "python_rng": random.getstate(),
                "numpy_rng": [numpy_state[0], numpy_state[1].tolist(), *numpy_state[2:]],
                "augmentation_rng": trainer.augmentation_rng.bit_generator.state,
                "working_dtype": str(trainer.dtype), "backend": trainer.backend,
                "mlx_rng_policy": "explicit_key_only; no global MLX RNG consumed",
                "shapes": {k: list(v.shape) for k, v in arrays.items()},
                "dtypes": {k: str(v.dtype) for k, v in arrays.items()}}
        if isinstance(trainer.model, DecoderLM):
            probe = trainer.model(mx.array([[0, 1]], dtype=mx.int32), dtype=trainer.dtype, backend=trainer.backend)
            mx.eval(probe)
            if not bool(mx.all(mx.isfinite(probe)).item()):
                raise FloatingPointError("checkpoint forward probe nonfinite")
            meta["forward_probe_sha256"] = hashlib.sha256(np.asarray(probe.astype(mx.float32)).tobytes()).hexdigest()
        (temporary/"metadata.json").write_text(json.dumps(meta, sort_keys=True, indent=2)+"\n")
        with np.load(temporary/"arrays.npz", allow_pickle=False) as readback:
            if set(readback.files) != set(arrays):
                raise ValueError("checkpoint array inventory readback failed")
            for k in arrays:
                if not np.array_equal(readback[k], arrays[k]):
                    raise ValueError("checkpoint array readback failed")
        manifest = {name: _hash(temporary/name) for name in ("arrays.npz", "metadata.json")}
        (temporary/"COMPLETE.json").write_text(json.dumps(manifest, sort_keys=True)+"\n")
        os.rename(temporary, destination)
        return manifest
    except Exception:
        # Keep failed partials for diagnosis; never publish them as complete.
        raise


def load_checkpoint(trainer, source):
    source = Path(source)
    manifest = json.loads((source/"COMPLETE.json").read_text())
    for name in ("arrays.npz", "metadata.json"):
        if manifest.get(name) != _hash(source/name):
            raise ValueError("checkpoint checksum mismatch")
    meta = json.loads((source/"metadata.json").read_text())
    if (meta["schema"] != "localflow_resume_v1" or meta["config"] != asdict(trainer.model.config)
            or meta["model_type"] != type(trainer.model).__name__ or meta["identities"] != trainer.identities
            or meta["schedule"] != asdict(trainer.schedule) or meta["optimizer_policy"] != trainer.optimizer.policy()
            or meta["working_dtype"] != str(trainer.dtype) or meta["backend"] != trainer.backend):
        raise ValueError("checkpoint configuration or identity mismatch")
    with np.load(source/"arrays.npz", allow_pickle=False) as saved:
        expected = {prefix+"::"+name for prefix in ("model", "m", "v", "acc")
                    for name in flat_parameters(trainer.model)} | {"mlx_rng"}
        if set(saved.files) != expected:
            raise ValueError("checkpoint array inventory mismatch")
        arrays = {}
        for name in saved.files:
            if list(saved[name].shape) != meta["shapes"][name] or str(saved[name].dtype) != meta["dtypes"][name]:
                raise ValueError("checkpoint shape/dtype mismatch")
            arrays[name] = mx.array(saved[name])
    parameters = {k.removeprefix("model::"): v for k, v in arrays.items() if k.startswith("model::")}
    for k, value in flat_parameters(trainer.model).items():
        if parameters[k].shape != value.shape or parameters[k].dtype != mx.float32:
            raise ValueError("checkpoint parameter shape/dtype invalid")
    trainer.model.update(tree_unflatten(list(parameters.items())))
    for prefix, target in (("m", trainer.optimizer.m), ("v", trainer.optimizer.v), ("acc", trainer.accumulator.values)):
        for k in target:
            value = arrays[prefix+"::"+k]
            if value.shape != parameters[k].shape or value.dtype != mx.float32:
                raise ValueError("checkpoint optimizer/accumulator shape/dtype invalid")
            target[k] = value
    trainer.optimizer.step = meta["optimizer_step"]
    for name in ("processed_tokens", "pending_tokens", "loss_sum", "data_cursor", "data_order", "phase"):
        setattr(trainer, name, meta[name])
    trainer.accumulator.denominator = meta["acc_denominator"]
    trainer.accumulator.microbatches = meta["acc_microbatches"]
    trainer.rng.key = arrays["mlx_rng"]
    trainer.augmentation_rng.bit_generator.state = meta["augmentation_rng"]
    random.setstate(_tuples(meta["python_rng"]))
    nr = meta["numpy_rng"]
    np.random.set_state((nr[0], np.array(nr[1], dtype=np.uint32), *nr[2:]))
    mx.eval(trainer.model.parameters(), trainer.optimizer.m, trainer.optimizer.v,
            trainer.accumulator.values, trainer.rng.key)
    if "forward_probe_sha256" in meta:
        probe = trainer.model(mx.array([[0, 1]], dtype=mx.int32), dtype=trainer.dtype, backend=trainer.backend)
        observed = hashlib.sha256(np.asarray(probe.astype(mx.float32)).tobytes()).hexdigest()
        if observed != meta["forward_probe_sha256"]:
            raise ValueError("checkpoint forward probe changed")
    return meta
