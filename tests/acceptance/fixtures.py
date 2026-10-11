"""NONSCIENTIFIC invented data; no historical distribution or reference reader."""
from dataclasses import dataclass
import hashlib
from src.acceptance.records import ScoreTrace, FitRecord, SelectRecord


def synthetic_id(number):
    return hashlib.sha256(("NONSCIENTIFIC invented identifier " + str(number)).encode()).hexdigest()


def trace(source, target, probabilities):
    return ScoreTrace(hashlib.sha256(source.encode()).hexdigest(),
        hashlib.sha256(target.encode()).hexdigest(),
        tuple(b+3 for b in target.encode())+(1,), tuple(probabilities))


def fit_rows(form="STRUCTURAL"):
    n = 8 if form == "STRUCTURAL" else 10
    return tuple(FitRecord((float(i),)*2 + (7.0,)*(n-2), 2*i+1, 0, "invented-"+str(i)) for i in range(4))


def selection_rows(score=5.0, zero_count=200):
    return tuple(SelectRecord("invented-repair-"+str(i), "invented-group-"+str(i), score,
        2, 0, 2, 0, True) for i in range(5)) + tuple(
        SelectRecord("invented-zero-"+str(i), "invented-zero-group", -1.0, 0, 0, 0, 0, False) for i in range(zero_count))


@dataclass(frozen=True)
class SyntheticLabels:
    """NONSCIENTIFIC label path; never supplied to inference-facing functions."""
    reference: str
    raw_errors: int
    proposal_errors: int
    provenance: str = "NONSCIENTIFIC"

import builtins
import io
import socket
import subprocess
from pathlib import Path
import numpy as np
import pytest


@pytest.fixture(autouse=True)
def synthetic_isolation(monkeypatch):
    """NONSCIENTIFIC tripwires stay active for every acceptance test body."""
    def forbidden(*args, **kwargs):
        raise AssertionError("NONSCIENTIFIC forbidden external/model/payload operation")
    original_import = builtins.__import__
    def guarded_import(name, *args, **kwargs):
        if name.split(".")[0] in {"torch","mlx","transformers","tensorflow","jax"} or name.startswith(("src.models", "src.inference", "benchmarks.g2")):
            return forbidden()
        return original_import(name, *args, **kwargs)
    monkeypatch.setattr(builtins, "__import__", guarded_import)
    monkeypatch.setattr(builtins, "open", forbidden)
    monkeypatch.setattr(io, "open", forbidden)
    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    monkeypatch.setattr(np, "load", forbidden)
