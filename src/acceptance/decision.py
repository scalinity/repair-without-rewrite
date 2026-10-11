"""NONSCIENTIFIC pure delivery; source/proposal bytes and scalar inputs only."""
import math
from src.scoring.text import lexical
from .features import raw_bytes, digest
from .records import DecisionRecord, THRESHOLDS


def decide(source, proposal, *, proposal_status, predicted_utility, threshold, score_ok=True):
    sb = raw_bytes(source)
    if proposal_status not in {"complete", "missing", "invalid", "incomplete", "capped"}:
        raise ValueError("unknown proposer status")
    if type(score_ok) is not bool: raise ValueError("score status required")
    if threshold is not None and (type(threshold) not in (int, float) or not math.isfinite(threshold) or threshold not in THRESHOLDS):
        raise ValueError("unregistered threshold; reject-all is None")
    ob = None; reason = None
    try:
        finite_utility = type(predicted_utility) in (int, float) and math.isfinite(predicted_utility)
    except OverflowError:
        finite_utility = False
    valid_utility = float(predicted_utility) if finite_utility else None
    try:
        if proposal is not None: ob = raw_bytes(proposal)
    except (ValueError, UnicodeError):
        reason = "invalid_proposal"
    if len(sb)+1 > 512: reason = "source_capacity_overflow"
    elif reason is not None: pass
    elif proposal_status != "complete" or ob is None: reason = "proposal_" + ("missing" if ob is None else proposal_status)
    elif len(ob)+1 > 512: reason = "proposal_capacity_overflow"
    elif not score_ok: reason = "score_failure"
    elif lexical(sb) == lexical(ob): reason = "lexical_identity"
    elif threshold is None: reason = "reject_all"
    elif not finite_utility: reason = "score_failure"
    else:
        valid_utility = float(predicted_utility)
        if not predicted_utility > threshold: reason = "below_or_equal_threshold"
    delivered = sb if reason else ob
    record = DecisionRecord(digest(sb), None if ob is None else digest(ob),
        digest(delivered), "RAW" if reason else "PROPOSAL", proposal_status,
        reason, valid_utility, threshold)
    return delivered, record
