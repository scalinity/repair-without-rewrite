"""NONSCIENTIFIC invented log probabilities; no extraction."""
from dataclasses import replace
import pytest
from src.acceptance.scores import aggregate_trace, score_contrasts
from .fixtures import trace, synthetic_isolation


def test_manual_contrasts_and_terminal_eos():
    source,proposal="a","é"
    identity=trace(source,source,(-.25,-.5))
    proposed=trace(source,proposal,(-1.0,-2.0,-.5))
    assert aggregate_trace(source,proposal,proposed).total == -3.5
    assert score_contrasts(source,proposal,proposed,identity)==(-2.75,-3.5/3+.75/2)
    empty=trace("","",(-.125,))
    assert aggregate_trace("","",empty).total==-.125
    assert score_contrasts("","",empty,empty)==(0.0,0.0)


@pytest.mark.parametrize("ids,probabilities", [
    ((100,),(-1.,)), ((0,100,1),(-1.,-1.,-1.)), ((100,1,0),(-1.,-1.,-1.)),
    ((1,100),(-1.,-1.)), ((101,1),(-1.,-1.)), ((100,1),(-1.,)),
    ((100,1),(float("nan"),-1.)), ((100,1),(float("-inf"),-1.)),
    ((100,1),(.01,-1.)), ((100.0,1),(-1.,-1.)),
])
def test_trace_boundaries_fail(ids,probabilities):
    from src.acceptance.records import ScoreTrace
    with pytest.raises(ValueError):
        base=trace("a","a",(-1.,-1.))
        record=ScoreTrace(base.source_hash,base.target_hash,ids,probabilities)
        aggregate_trace("a","a",record)


def test_source_and_proposal_bindings():
    t=trace("a","a",(-1.,-1.))
    for source,target in (("b","a"),("a","b")):
        with pytest.raises(ValueError,match="identity"):
            aggregate_trace(source,target,t)


def test_empty_source_and_nonempty_target():
    proposed=trace("","a",(-1.,-.5))
    identity=trace("","",(-.5,))
    assert score_contrasts("","a",proposed,identity)==(-1.,-.25)


def test_aggregation_overflow_is_explicit():
    with pytest.raises(ValueError):
        aggregate_trace("a","a",trace("a","a",(-1e308,-1e308)))

def test_primary_exact_order_binding_and_end_to_end_prediction():
    import math
    from src.acceptance.scores import primary_features
    from src.acceptance.policy import fit_policy,predict
    from src.acceptance.decision import decide
    from .fixtures import fit_rows
    values=primary_features("a","b",trace("a","b",(-.25,-.25)),trace("a","a",(-1.,-1.)))
    assert values==(math.log(2),)*4+(0.,0.,1.,1.,1.5,.75)
    predicted=predict(fit_policy(fit_rows("PRIMARY"),"PRIMARY"),[values])[0]
    delivered,record=decide("a","b",proposal_status="complete",predicted_utility=predicted,threshold=0.)
    assert delivered==b"b" and record.delivered_from=="PROPOSAL"
    with pytest.raises(ValueError):
        primary_features("a","b",trace("x","b",(-1.,-1.)),trace("a","a",(-1.,-1.)))
