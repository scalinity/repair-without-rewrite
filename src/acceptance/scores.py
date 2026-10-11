"""NONSCIENTIFIC aggregation of supplied traces only; no score provider."""
import math
from .features import raw_bytes, digest, structural_features
from .records import ScoreAggregate, ScoreTrace


def aggregate_trace(source, target, trace: ScoreTrace):
    trace.__post_init__()
    sb, tb = raw_bytes(source), raw_bytes(target)
    expected = tuple(b + 3 for b in tb) + (1,)
    if trace.source_hash != digest(sb) or trace.target_hash != digest(tb):
        raise ValueError("source/target identity mismatch")
    if trace.token_ids != expected:
        raise ValueError("target token identity/count/EOS mismatch; PAD/start excluded")
    try: total = math.fsum(trace.log_probabilities)
    except OverflowError as exc: raise ValueError("nonfinite aggregate") from exc
    if not math.isfinite(total): raise ValueError("nonfinite aggregate")
    return ScoreAggregate(trace, len(tb), total)


def score_contrasts(source, proposal, proposal_trace: ScoreTrace, identity_trace: ScoreTrace):
    proposed = aggregate_trace(source, proposal, proposal_trace)
    identity = aggregate_trace(source, source, identity_trace)
    contrasts = ((proposed.total - identity.total)/max(1, identity.target_bytes),
                 proposed.total/(proposed.target_bytes+1) - identity.total/(identity.target_bytes+1))
    if not all(math.isfinite(v) for v in contrasts): raise ValueError("nonfinite contrast")
    return contrasts


def primary_features(source, proposal, proposal_trace: ScoreTrace, identity_trace: ScoreTrace):
    """Exactly eight structural values followed by the two bound score contrasts."""
    return structural_features(source, proposal).values + score_contrasts(
        source, proposal, proposal_trace, identity_trace)
