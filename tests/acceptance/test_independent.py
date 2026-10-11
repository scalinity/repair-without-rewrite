"""NONSCIENTIFIC numerical independence and explicit isolation attempts."""
import builtins
from fractions import Fraction
import inspect
import math
import socket
from pathlib import Path
import numpy as np
import pytest
from src.acceptance.features import structural_features
from src.acceptance.scores import score_contrasts
from src.acceptance.policy import fit_policy,predict
from src.acceptance.decision import decide
from src.acceptance.records import FitRecord
from .fixtures import fit_rows,trace,SyntheticLabels,synthetic_isolation
from .independent_oracles import rational_ridge, rational_standard_deviation


@pytest.mark.parametrize("form",["STRUCTURAL","PRIMARY"])
def test_fraction_oracle_nontrivial_matrix(form):
    n=8 if form=="STRUCTURAL" else 10
    rows=tuple(FitRecord(tuple(float((i+j*j)%7) for j in range(n)),
        i*i, i%2, "invented"+str(i)) for i in range(6))
    expected=rational_ridge([r.values for r in rows],
        [r.completed_repair_lower-4*r.introduced_error_upper for r in rows])
    actual=fit_policy(rows,form)
    assert actual.normalizer.means==pytest.approx(expected[0],abs=1e-14)
    assert actual.normalizer.standard_deviations==pytest.approx(expected[1],abs=1e-14)
    assert actual.intercept==pytest.approx(expected[2],abs=1e-12)
    assert actual.coefficients==pytest.approx(expected[3],abs=2e-12)


def test_f1_exact_positive_variance_and_analytic_ridge_expectations():
    q = Fraction(1, 2**600)
    t = math.ldexp(1.0, -600)
    mean = q/2
    variance = sum((v-mean)**2 for v in (Fraction(0), q))/2
    sd = q/2
    assert variance == sd**2 > 0 and float(variance) == 0
    assert float(sd) == t/2 > 0
    assert rational_standard_deviation(Fraction(0)) == 0
    assert rational_standard_deviation(variance) == sd
    with pytest.raises(ArithmeticError, match="positive exact variance"):
        rational_standard_deviation(q*q/2)  # positive, nonsquare, and lost by float conversion
    standardized = tuple((v-mean)/sd for v in (Fraction(0), q))
    assert standardized == (-1, 1)
    # Exact independent normal equations: intercept diagonal 2, coefficient 2+.02.
    intercept = Fraction(1, 2)
    coefficient = Fraction(1, 2)/Fraction(101, 100)
    predictions = tuple(intercept + coefficient*z for z in standardized)
    assert predictions == (Fraction(1, 202), Fraction(201, 202))
    assert tuple(p > Fraction(1, 4) for p in predictions) == (False, True)
    structural = (math.log1p(1),)*3 + (math.log1p(2), 0., 0., 1., 2.)
    matrix = (structural + (0., t), structural + (t, t))
    means, deviations, actual_intercept, coefficients = rational_ridge(matrix, (0, 1))
    assert means == structural + (float(mean), t)
    assert deviations == (0.,)*8 + (float(sd), 0.)
    assert actual_intercept == float(intercept)
    assert coefficients == (0.,)*8 + (float(coefficient), 0.)
    # Reconstruction tolerance is software-only; the threshold comparison above is exact.
    reconstructed = tuple(actual_intercept + coefficients[8]*z for z in standardized)
    assert reconstructed == pytest.approx(tuple(float(p) for p in predictions), abs=1e-15)


def test_reference_group_role_label_access_trap():
    class Poison:
        def __getattribute__(self,name):
            raise AssertionError("forbidden synthetic label access")
    policy=fit_policy(fit_rows(),"STRUCTURAL")
    labels=SyntheticLabels("invented reference never passed",1,0)
    assert labels.provenance=="NONSCIENTIFIC"
    calls=[
        (structural_features,("a","b"),{}),
        (score_contrasts,("a","b",trace("a","b",(-1.,-1.)),trace("a","a",(-1.,-1.))),{}),
        (predict,(policy,[(1.,)*8]),{}),
        (decide,("a","b"),dict(proposal_status="complete",predicted_utility=2.,threshold=1.)),
    ]
    for function,args,kwargs in calls:
        forbidden={"reference","labels","group","speaker","corpus_role","audio"}
        assert not forbidden & set(inspect.signature(function).parameters)
        for name in forbidden:
            with pytest.raises(TypeError): function(*args,**kwargs,**{name:Poison()})
        function(*args,**kwargs)


@pytest.mark.parametrize("operation", [
    lambda: socket.socket(),
    lambda: socket.create_connection(("invented.invalid",443)),
    lambda: builtins.__import__("torch"),
    lambda: builtins.__import__("mlx.core"),
    lambda: builtins.__import__("transformers"),
    lambda: builtins.__import__("src.inference.byt5_probe"),
    lambda: np.load("invented-model.npz"),
    lambda: Path("exports/invented-private.json").read_text(),
    lambda: Path("/Volumes/NONSCIENTIFIC_ISOLATION_TRAP/reference.txt").read_text(),
    lambda: builtins.open("checkpoints/invented.pt","rb"),
])
def test_explicit_isolation_traps(operation):
    with pytest.raises(AssertionError,match="NONSCIENTIFIC forbidden"):
        operation()
