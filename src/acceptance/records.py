"""NONSCIENTIFIC typed records; strict, versioned, deterministic JSON."""
from __future__ import annotations

from dataclasses import dataclass, fields
import json
import math
import types
from typing import Literal, get_args, get_origin, get_type_hints

Form = Literal["STRUCTURAL", "PRIMARY"]
FEATURE_ORDER = ("log_source_words", "log_proposal_words", "log_source_bytes",
                 "log_proposal_bytes", "insertions_per_source_word",
                 "deletions_per_source_word", "substitutions_per_source_word",
                 "byte_distance_per_source_byte", "score_difference_per_source_byte",
                 "mean_target_score_difference")
THRESHOLDS = (0.0, 0.25, 0.5, 1.0, 2.0, 4.0)
SCHEMA = "fixture_only_acceptance_v1"


def width(form: Form) -> int:
    if form not in ("STRUCTURAL", "PRIMARY"):
        raise ValueError("unregistered policy form")
    return 8 if form == "STRUCTURAL" else 10


def _check(value, annotation):
    origin, args = get_origin(annotation), get_args(annotation)
    if origin in (types.UnionType,):
        if not any(_matches(value, a) for a in args):
            raise ValueError("unexpected union value")
    elif origin is Literal:
        if value not in args or (isinstance(value, bool) and value not in (True, False)):
            raise ValueError("unexpected literal")
    elif origin is tuple:
        if type(value) is not tuple:
            raise ValueError("tuple required")
        if len(args) == 2 and args[1] is Ellipsis:
            for item in value: _check(item, args[0])
        else:
            if len(value) != len(args): raise ValueError("tuple length")
            for item, typ in zip(value, args): _check(item, typ)
    elif annotation is float:
        try:
            valid = type(value) in (int, float) and math.isfinite(value)
        except OverflowError:
            valid = False
        if not valid:
            raise ValueError("finite numerical value required")
    elif annotation is int:
        if type(value) is not int: raise ValueError("integer required")
    elif not isinstance(value, annotation):
        raise ValueError("unexpected field type")


def _matches(value, annotation):
    try:
        _check(value, annotation)
        return True
    except (ValueError, TypeError):
        return False


def _hash(value):
    if len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise ValueError("SHA-256 identity required")


@dataclass(frozen=True, kw_only=True)
class Record:
    provenance: Literal["NONSCIENTIFIC"] = "NONSCIENTIFIC"

    def __post_init__(self):
        for name, annotation in get_type_hints(type(self)).items():
            _check(getattr(self, name), annotation)


@dataclass(frozen=True)
class FeatureRecord(Record):
    source_hash: str
    proposal_hash: str
    source_bytes: int
    proposal_bytes: int
    values: tuple[float, ...]
    order: tuple[str, ...] = FEATURE_ORDER[:8]
    normalization: Literal["lexical_eval_v1"] = "lexical_eval_v1"

    def __post_init__(self):
        super().__post_init__()
        _hash(self.source_hash); _hash(self.proposal_hash)
        if min(self.source_bytes, self.proposal_bytes) < 0 or len(self.values) != 8 or self.order != FEATURE_ORDER[:8]:
            raise ValueError("invalid structural feature record")


@dataclass(frozen=True)
class ScoreTrace(Record):
    source_hash: str
    target_hash: str
    token_ids: tuple[int, ...]
    log_probabilities: tuple[float, ...]

    def __post_init__(self):
        super().__post_init__()
        _hash(self.source_hash); _hash(self.target_hash)
        if any(p > 0 for p in self.log_probabilities):
            raise ValueError("log probability exceeds zero")
        if len(self.token_ids) != len(self.log_probabilities):
            raise ValueError("trace lengths differ")


@dataclass(frozen=True)
class ScoreAggregate(Record):
    trace: ScoreTrace
    target_bytes: int
    total: float

    def __post_init__(self):
        super().__post_init__()
        if self.target_bytes < 0 or len(self.trace.token_ids) != self.target_bytes + 1:
            raise ValueError("aggregate target length")
        if self.trace.token_ids[-1:] != (1,) or any(not 3 <= n <= 258 for n in self.trace.token_ids[:-1]):
            raise ValueError("aggregate EOS/byte contract")
        if self.total != math.fsum(self.trace.log_probabilities):
            raise ValueError("aggregate differs from supplied trace")


@dataclass(frozen=True)
class Normalizer(Record):
    form: Form
    means: tuple[float, ...]
    standard_deviations: tuple[float, ...]
    fit_count: int
    order: tuple[str, ...]

    def __post_init__(self):
        super().__post_init__()
        n = width(self.form)
        if len(self.means) != n or len(self.standard_deviations) != n or self.order != FEATURE_ORDER[:n] or self.fit_count < 1 or any(s < 0 for s in self.standard_deviations):
            raise ValueError("invalid FIT normalizer")


@dataclass(frozen=True)
class Policy(Record):
    form: Form
    normalizer: Normalizer
    intercept: float
    coefficients: tuple[float, ...]

    def __post_init__(self):
        super().__post_init__()
        if self.form != self.normalizer.form or len(self.coefficients) != width(self.form):
            raise ValueError("policy feature binding")


@dataclass(frozen=True)
class FitRecord(Record):
    values: tuple[float, ...]
    completed_repair_lower: int
    introduced_error_upper: int
    group: str
    valid: bool = True
    changed: bool = True
    beneficial: bool = False
    role: Literal["FIT"] = "FIT"

    def __post_init__(self):
        super().__post_init__()
        if min(self.completed_repair_lower, self.introduced_error_upper) < 0 or not self.group:
            raise ValueError("invalid artificial FIT labels")


@dataclass(frozen=True)
class SelectRecord(Record):
    case_id: str
    group: str
    predicted_utility: float
    raw_errors: int
    proposal_errors: int
    completed_repair_lower: int
    introduced_error_upper: int
    eligible_proposal: bool
    role: Literal["SELECT"] = "SELECT"

    def __post_init__(self):
        super().__post_init__()
        if not self.case_id or not self.group or min(self.raw_errors, self.proposal_errors, self.completed_repair_lower, self.introduced_error_upper) < 0:
            raise ValueError("invalid SELECT evidence")


@dataclass(frozen=True)
class ThresholdEvidence(Record):
    threshold: float | None
    accepted_cases: tuple[str, ...]
    population: int
    raw_errors: int
    output_errors: int
    repairs: int
    introductions: int
    repair_groups: int
    zero_cases: int
    damaged_zero_cases: int
    conservative_utility: int
    eligible: bool
    failure_reasons: tuple[str, ...]

    def __post_init__(self):
        super().__post_init__()
        if self.threshold is not None and self.threshold not in THRESHOLDS:
            raise ValueError("unregistered evidence threshold")
        if min(self.population, self.raw_errors, self.output_errors, self.repairs,
               self.introductions, self.repair_groups, self.zero_cases,
               self.damaged_zero_cases) < 0:
            raise ValueError("negative evidence count")
        if self.damaged_zero_cases > self.zero_cases or len(set(self.accepted_cases)) != len(self.accepted_cases) or len(self.accepted_cases) > self.population:
            raise ValueError("inconsistent SELECT counts")
        if self.conservative_utility != self.repairs - 4*self.introductions:
            raise ValueError("utility mismatch")


@dataclass(frozen=True)
class Selection(Record):
    form: Form
    threshold: float | None
    status: Literal["SELECTED", "SELECTION_FAILURE", "UNRESOLVED"]
    evidence: tuple[ThresholdEvidence, ...]

    def __post_init__(self):
        super().__post_init__(); width(self.form)
        if self.threshold is not None and self.threshold not in THRESHOLDS:
            raise ValueError("unregistered threshold")
        if (self.status == "SELECTED") != (self.threshold is not None):
            raise ValueError("selection/reject-all binding")


@dataclass(frozen=True)
class DecisionRecord(Record):
    source_hash: str
    proposal_hash: str | None
    delivered_hash: str
    delivered_from: Literal["RAW", "PROPOSAL"]
    proposal_status: Literal["complete", "missing", "invalid", "incomplete", "capped"]
    failure_reason: str | None
    predicted_utility: float | None
    threshold: float | None

    def __post_init__(self):
        super().__post_init__()
        _hash(self.source_hash); _hash(self.delivered_hash)
        if self.proposal_hash is not None: _hash(self.proposal_hash)
        if self.threshold is not None and self.threshold not in THRESHOLDS:
            raise ValueError("decision threshold")


@dataclass(frozen=True)
class Family(Record):
    component_id: str
    members: tuple[str, ...]

    def __post_init__(self):
        super().__post_init__(); _hash(self.component_id)
        if not self.members or self.members != tuple(sorted(set(self.members))):
            raise ValueError("unique sorted component members required")
        for member in self.members: _hash(member)


@dataclass(frozen=True)
class RoleAllocation(Record):
    role: Literal["FIT", "SELECT", "EVAL"]
    selected_ids: tuple[str, ...]
    selected_components: int
    available_cases: int
    sufficient: bool
    failure_reasons: tuple[str, ...]

    def __post_init__(self):
        super().__post_init__()
        for value in self.selected_ids: _hash(value)
        if min(self.selected_components, self.available_cases) < 0 or len(set(self.selected_ids)) != len(self.selected_ids) or len(self.selected_ids) > self.available_cases or self.selected_components > len(self.selected_ids):
            raise ValueError("invalid allocation counts")


@dataclass(frozen=True)
class NumericalReceipt(Record):
    check: str
    status: Literal["PASS", "FAIL", "UNVERIFIED"]
    values: tuple[float, ...]
    failure_reasons: tuple[str, ...]


TYPES = {c.__name__: c for c in (FeatureRecord, ScoreTrace, ScoreAggregate,
    Normalizer, Policy, FitRecord, SelectRecord, ThresholdEvidence, Selection,
    DecisionRecord, Family, RoleAllocation, NumericalReceipt)}


def _pack(value):
    if isinstance(value, Record):
        value.__post_init__()
        return {"schema_version": SCHEMA, "type": type(value).__name__,
                "fields": {f.name: _pack(getattr(value, f.name)) for f in fields(value)}}
    if isinstance(value, tuple): return [_pack(v) for v in value]
    return value


def _unpack(value):
    if isinstance(value, list): return tuple(_unpack(v) for v in value)
    if isinstance(value, dict):
        if set(value) != {"schema_version", "type", "fields"} or value["schema_version"] != SCHEMA or value["type"] not in TYPES:
            raise ValueError("unexpected record schema")
        typ = TYPES[value["type"]]
        if set(value["fields"]) != {f.name for f in fields(typ)}:
            raise ValueError("unexpected or missing record fields")
        return typ(**{k: _unpack(v) for k, v in value["fields"].items()})
    return value


def encode_record(record: Record) -> str:
    if type(record).__name__ not in TYPES: raise ValueError("unknown record")
    return json.dumps(_pack(record), sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False)


def decode_record(text: str) -> Record:
    def pairs(items):
        obj = {}
        for key, value in items:
            if key in obj: raise ValueError("duplicate JSON key")
            obj[key] = value
        return obj
    def constant(value): raise ValueError("nonstandard numerical constant")
    result = _unpack(json.loads(text, object_pairs_hook=pairs, parse_constant=constant))
    if not isinstance(result, Record): raise ValueError("record required")
    return result
