"""NONSCIENTIFIC complete artificial SELECT labels; no EVAL implementation."""
from .records import SelectRecord, Selection, ThresholdEvidence, THRESHOLDS, width


def select_threshold(records: tuple[SelectRecord, ...], form):
    width(form)
    for row in records: row.__post_init__()
    if len({r.case_id for r in records}) != len(records): raise ValueError("duplicate SELECT case")
    raw = sum(r.raw_errors for r in records)
    zero = sum(r.raw_errors == 0 for r in records)
    evidence = []
    for threshold in (*THRESHOLDS, None):
        accepted = [r for r in records if threshold is not None and r.eligible_proposal and r.predicted_utility > threshold]
        ids = {r.case_id for r in accepted}
        output = sum(r.proposal_errors if r.case_id in ids else r.raw_errors for r in records)
        repairs = sum(r.completed_repair_lower for r in accepted)
        introductions = sum(r.introduced_error_upper for r in accepted)
        groups = len({r.group for r in accepted if r.completed_repair_lower > 0})
        damaged = sum(r.raw_errors == 0 and r.proposal_errors > 0 for r in accepted)
        reasons = []
        if threshold is None: reasons.append("reject_all")
        if output >= raw: reasons.append("output_errors_not_below_RAW")
        if repairs < 10: reasons.append("insufficient_repairs")
        if groups < 5: reasons.append("insufficient_repair_groups")
        if 4*introductions > repairs: reasons.append("introduced_bound")
        if zero == 0: reasons.append("undefined_lexical_zero_denominator")
        elif 200*damaged > zero: reasons.append("lexical_zero_preservation")
        evidence.append(ThresholdEvidence(threshold, tuple(r.case_id for r in accepted), len(records), raw, output, repairs, introductions, groups, zero, damaged, repairs-4*introductions, not reasons, tuple(reasons)))
    eligible = [e for e in evidence if e.eligible]
    if eligible:
        best = max(eligible, key=lambda e: (e.conservative_utility, e.threshold))
        return Selection(form, best.threshold, "SELECTED", tuple(evidence))
    return Selection(form, None, "UNRESOLVED" if not zero else "SELECTION_FAILURE", tuple(evidence))
