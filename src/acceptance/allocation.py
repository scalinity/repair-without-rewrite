"""NONSCIENTIFIC frozen Mozilla namespace and v3 allocation; no corpus adapter."""
import hashlib
import json
from .records import RoleAllocation, _hash

CASE_NAMESPACE = ("RWR_CV26_BRITISH_CASE_V1", "cmrt6zrob000zmm07yqwjlpwi",
                  "cv-corpus-26.0-2026-06-12", "en")
ROLE_QUOTAS = {"FIT": (4000, 80), "SELECT": (2000, 40), "EVAL": (6000, 100)}
ROLE_SALT = "POST_FEASIBILITY_ACCEPTANCE_V1|"
CASE_SALT = "POST_FEASIBILITY_CASE_V1|"


def case_identity_bytes(publisher_path: str):
    if type(publisher_path) is not str or not publisher_path or publisher_path.startswith("/") or "\\" in publisher_path or "://" in publisher_path or any(ord(c) < 32 or ord(c) == 127 for c in publisher_path):
        raise ValueError("exact publisher relative path required")
    if any(p in ("", ".", "..") for p in publisher_path.split("/")):
        raise ValueError("ambiguous path; do not normalize")
    publisher_path.encode("utf-8", "strict")
    return json.dumps([*CASE_NAMESPACE, publisher_path], ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")


def case_id(publisher_path):
    return hashlib.sha256(case_identity_bytes(publisher_path)).hexdigest()


def component_id(members):
    members = tuple(members)
    if not members or len(set(members)) != len(members): raise ValueError("unique nonempty members required")
    for member in members: _hash(member)
    payload = "RWR_CV26_BRITISH_COMPONENT_V1\n" + "\n".join(sorted(members))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def role_for(component):
    _hash(component)
    remainder = int.from_bytes(hashlib.sha256((ROLE_SALT+component).encode()).digest(), "big") % 6
    return "FIT" if remainder < 2 else "SELECT" if remainder == 2 else "EVAL"


def case_rank(stable_id):
    _hash(stable_id)
    return hashlib.sha256((CASE_SALT+stable_id).encode()).digest()


def allocate(families, *, eligible_ids, excluded_ids=()):
    """Closure is supplied in full; exclusions veto whole components before cap."""
    families = tuple(families)
    eligible, excluded = set(eligible_ids), set(excluded_ids)
    all_ids = set(); component_ids = set()
    for family in families:
        family.__post_init__()
        if component_id(family.members) != family.component_id:
            raise ValueError("component identity mismatch")
        if all_ids & set(family.members) or family.component_id in component_ids:
            raise ValueError("conflicting component membership")
        all_ids.update(family.members); component_ids.add(family.component_id)
    if not (eligible | excluded) <= all_ids: raise ValueError("unknown eligibility/exclusion identity")
    pools = {r: [] for r in ROLE_QUOTAS}
    owners = {}
    for family in families:
        if excluded & set(family.members): continue
        role = role_for(family.component_id)
        ranked = sorted((m for m in family.members if m in eligible), key=case_rank)[:60]
        pools[role].extend(ranked)
        for m in ranked: owners[m] = family.component_id
    results = []
    for role, (quota, minimum) in ROLE_QUOTAS.items():
        candidates = sorted(pools[role], key=case_rank)
        selected = tuple(candidates[:quota])
        count = len({owners[m] for m in selected})
        reasons = []
        if len(selected) < quota: reasons.append("insufficient_cases")
        if count < minimum: reasons.append("insufficient_selected_components")
        results.append(RoleAllocation(role, selected, count, len(candidates), not reasons, tuple(reasons)))
    return tuple(results)
