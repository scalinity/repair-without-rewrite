"""NONSCIENTIFIC source-byte delivery, separate proposer status."""
import pytest
from src.acceptance.decision import decide
from .fixtures import synthetic_isolation


@pytest.mark.parametrize("kwargs,reason", [
    ({"proposal_status":"missing","proposal":None},"proposal_missing"),
    ({"proposal_status":"invalid"},"proposal_invalid"),
    ({"proposal_status":"incomplete"},"proposal_incomplete"),
    ({"proposal_status":"capped"},"proposal_capped"),
    ({"score_ok":False},"score_failure"),
    ({"proposal":b"\xff"},"invalid_proposal"),
    ({"proposal":"A,  b"},"lexical_identity"),
    ({"threshold":None},"reject_all"),
    ({"predicted_utility":1.0},"below_or_equal_threshold"),
    ({"predicted_utility":float("nan")},"score_failure"),
    ({"proposal":"x"*512},"proposal_capacity_overflow"),
])
def test_every_raw_fallback(kwargs,reason):
    params=dict(proposal_status="complete",predicted_utility=5.,threshold=1.,proposal=b"c")
    params.update(kwargs)
    proposal=params.pop("proposal")
    source=b"  a\r\nb\t"
    delivered,record=decide(source,proposal,**params)
    assert delivered is source or delivered==source
    assert record.delivered_from=="RAW" and record.failure_reason==reason
    assert record.proposal_status==params["proposal_status"]


def test_source_capacity_eos_boundary():
    good=decide("a"*511,"b",proposal_status="complete",predicted_utility=1.,threshold=0.)
    bad=decide("a"*512,"b",proposal_status="complete",predicted_utility=1.,threshold=0.)
    assert good[0]==b"b"
    assert bad[1].failure_reason=="source_capacity_overflow"


def test_complete_empty_is_a_full_proposal():
    delivered,record=decide("a","",proposal_status="complete",predicted_utility=.5,threshold=.25)
    assert delivered==b"" and record.delivered_from=="PROPOSAL"
    assert record.proposal_status=="complete"
    missing=decide("a",None,proposal_status="missing",predicted_utility=.5,threshold=.25)
    assert missing[0]==b"a" and missing[1].proposal_status=="missing"


def test_acceptance_preserves_entire_surface_bytes():
    proposal=b"  New!\r\n"
    assert decide(b"old",proposal,proposal_status="complete",predicted_utility=2.,threshold=1.)[0]==proposal


@pytest.mark.parametrize("threshold",[float("inf"),float("nan"),.1,True])
def test_threshold_cannot_be_nonregistered(threshold):
    with pytest.raises(ValueError):
        decide("a","b",proposal_status="complete",predicted_utility=2.,threshold=threshold)

def test_unicode_raw_fallback_and_unrepresentable_score():
    source=" café\u0301\r\n".encode()
    delivered,record=decide(source,"invented",proposal_status="complete",predicted_utility=10**400,threshold=0.)
    assert delivered==source and record.failure_reason=="score_failure"


def test_complete_output_capacity_boundary():
    assert decide("a","b"*511,proposal_status="complete",predicted_utility=1.,threshold=0.)[1].delivered_from=="PROPOSAL"
    assert decide("a","b"*512,proposal_status="complete",predicted_utility=1.,threshold=0.)[1].failure_reason=="proposal_capacity_overflow"
