"""NONSCIENTIFIC exact Fraction ridge oracle and analytic fixtures."""
from dataclasses import replace
from fractions import Fraction
import math
import numpy as np
import pytest
from src.acceptance.policy import fit_policy, predict, transform, fit_support, NumericalFailure
from src.acceptance.records import FitRecord, FEATURE_ORDER
from src.acceptance.scores import aggregate_trace, primary_features
from src.acceptance.decision import decide
from .fixtures import fit_rows, trace, synthetic_isolation
from .independent_oracles import rational_ridge


@pytest.mark.parametrize("form",["STRUCTURAL","PRIMARY"])
def test_exact_oracle_collinear_constant_and_intercept(form):
    rows=fit_rows(form)
    means,sd,intercept,coef=rational_ridge([r.values for r in rows],
        [r.completed_repair_lower-4*r.introduced_error_upper for r in rows])
    policy=fit_policy(rows,form)
    assert policy.normalizer.means==means
    assert policy.normalizer.standard_deviations==sd
    assert policy.intercept==pytest.approx(intercept,abs=1e-12)
    assert policy.coefficients==pytest.approx(coef,abs=1e-12)
    assert policy.intercept==pytest.approx(4.0)
    assert all(v==0 for v in policy.coefficients[2:])
    # Two duplicate standardized columns: each coefficient = sqrt(5)/2.01.
    assert policy.coefficients[0]==pytest.approx(math.sqrt(5)/2.01)
    assert policy.coefficients[1]==pytest.approx(math.sqrt(5)/2.01)


def test_single_case_all_constant_unpenalized_intercept():
    row=FitRecord((1e30,)*8,7,2,"invented")
    policy=fit_policy((row,),"STRUCTURAL")
    assert policy.intercept==-1.
    assert policy.coefficients==(0.,)*8
    assert predict(policy,[(0.,)*8])==(-1.,)


def test_fit_only_state_invariance_and_constant_future_columns():
    policy=fit_policy(fit_rows(),"STRUCTURAL")
    before=policy.normalizer
    predict(policy,[(1.,2.,99.,100.,1000.,10.,0.,-10.)])
    predict(policy,[(-100.,200.,1.,2.,3.,4.,5.,6.)])
    assert policy.normalizer==before
    assert tuple(transform(before,[(0.,)*8])[0,2:])==(0.,)*6


def test_n_scaled_regularization():
    rows=tuple(FitRecord((float(i),)+(0.,)*7,i+1,0,"invented") for i in range(4))
    policy=fit_policy(rows,"STRUCTURAL")
    assert policy.intercept==pytest.approx(2.5)
    assert policy.coefficients[0]==pytest.approx(math.sqrt(1.25)/1.01)
    duplicate=fit_policy(rows*2,"STRUCTURAL")
    assert duplicate.coefficients==pytest.approx(policy.coefficients,abs=1e-12)


@pytest.mark.parametrize("change", [{"valid":False},{"changed":False},{"role":"SELECT"}])
def test_non_fit_or_invalid_changed_cases_rejected(change):
    with pytest.raises(ValueError):
        fit_policy((replace(fit_rows()[0],**change),),"STRUCTURAL")


def test_numerical_failure_does_not_rescue(monkeypatch):
    def failure(*args,**kwargs): raise np.linalg.LinAlgError("invented failure")
    monkeypatch.setattr(np.linalg,"solve",failure)
    with pytest.raises(NumericalFailure,match="no rescue"):
        fit_policy(fit_rows(),"STRUCTURAL")


def test_nonfinite_inputs_and_wrong_forms_rejected():
    for values in ([tuple([float("nan")]*8)],[(0.,)*7]):
        policy=fit_policy(fit_rows(),"STRUCTURAL")
        with pytest.raises(NumericalFailure): predict(policy,values)
    with pytest.raises(ValueError): fit_policy(fit_rows(),"NEW")


def test_artificial_support_gate_and_separate_benefit_label():
    rows=tuple(FitRecord((float(i),)+(0.,)*7,1,0,"invented-group-"+str(i%20),
                        beneficial=i<40) for i in range(200))
    assert fit_support(rows)
    assert not fit_support(rows[:199])
    assert not fit_support(tuple(replace(r,beneficial=i<39) for i,r in enumerate(rows)))
    assert not fit_support(tuple(replace(r,group="invented-one") for r in rows))

@pytest.mark.parametrize("bad", [(True,)*8,("1.0",)*8])
def test_prediction_rejects_coerced_numeric_inputs(bad):
    with pytest.raises(NumericalFailure):
        predict(fit_policy(fit_rows(),"STRUCTURAL"),[bad])


def test_f1_nonconstant_primary_variance_underflow_fails_before_policy(monkeypatch):
    t = math.ldexp(1.0, -600)
    q = Fraction(1, 2**600)
    traces = ((trace("a", "a", (-3*t,)*2), trace("a", "bc", (-2*t,)*3)),
              (trace("a", "a", (-2*t,)*2), trace("a", "bc", (-t,)*3)))
    expected_structural = (math.log1p(1),)*3 + (math.log1p(2), 0., 0., 1., 2.)
    values = []
    for i, (identity, proposal) in enumerate(traces):
        assert identity.token_ids == (100, 1)
        assert proposal.token_ids == (101, 102, 1)
        assert aggregate_trace("a", "a", identity).total == (-6*t if i == 0 else -4*t)
        assert aggregate_trace("a", "bc", proposal).total == (-6*t if i == 0 else -3*t)
        values.append(primary_features("a", "bc", proposal, identity))
    assert values == [expected_structural + (0., t), expected_structural + (t, t)]
    rows = tuple(FitRecord(v, i, 0, "invented-f1-"+str(i)) for i, v in enumerate(values))
    for row in rows:
        row.__post_init__()
        assert row.valid and row.changed and row.role == "FIT"
        assert row.provenance == "NONSCIENTIFIC" and len(row.values) == len(FEATURE_ORDER) == 10
    column = np.asarray([r.values[8] for r in rows], dtype=np.float64)
    assert column[0] != column[1] and Fraction(float(column[1])) == q
    exact_mean = q/2
    exact_variance = sum((v-exact_mean)**2 for v in (Fraction(0), q))/2
    exact_sd = q/2
    assert exact_variance == exact_sd**2 > 0
    assert float(exact_sd) == t/2 > 0
    assert float(np.mean(column)) == t/2
    assert float(np.mean((column-np.mean(column))**2)) == 0

    def forbidden(*args, **kwargs):
        pytest.fail("collapsed nonconstant variance must fail before solving or emitting a policy")
    monkeypatch.setattr(np.linalg, "solve", forbidden)
    monkeypatch.setattr("src.acceptance.policy.Policy", forbidden)
    fitted = None
    with pytest.raises(NumericalFailure, match="fixed ridge arithmetic failed; no rescue") as failed:
        fitted = fit_policy(rows, "PRIMARY")
    assert str(failed.value.__cause__) == "nonconstant FIT standard deviation collapsed to zero"
    assert fitted is None
    # No prediction from the failed fit: the existing absent-score path delivers RAW.
    delivered, decision = decide("a", "bc", proposal_status="complete",
                                 predicted_utility=None, threshold=.25)
    assert delivered == b"a" and decision.delivered_from == "RAW"
    assert decision.failure_reason == "score_failure" and decision.predicted_utility is None
