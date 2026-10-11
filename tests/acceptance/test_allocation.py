"""NONSCIENTIFIC independent byte/hash reconstruction and fixed allocation."""
import hashlib
import pytest
from src.acceptance.allocation import case_identity_bytes,case_id,component_id,role_for,case_rank,allocate
from src.acceptance.records import Family,encode_record,decode_record
from .fixtures import synthetic_id,synthetic_isolation
from .independent_oracles import identity_bytes,independent_component,independent_allocation


@pytest.mark.parametrize("path",["clips/invented.mp3","clips/invented-é.mp3","clips/space here.mp3"])
def test_exact_canonical_json_and_case_hash(path):
    expected=identity_bytes(path)
    assert case_identity_bytes(path)==expected
    assert case_id(path)==hashlib.sha256(expected).hexdigest()


@pytest.mark.parametrize("path",["","/absolute","../x","clips/../x","clips/./x","clips//x","clips/","x\\y","https://invented.invalid/x","x\n",None])
def test_malformed_paths_are_rejected_not_normalized(path):
    with pytest.raises(ValueError): case_id(path)


def test_component_hash_member_order_salts_and_duplicate_conflicts():
    members=(synthetic_id(2),synthetic_id(1))
    expected=independent_component(members)
    assert component_id(members)==expected==component_id(tuple(reversed(members)))
    remainder=int(hashlib.sha256(("POST_FEASIBILITY_ACCEPTANCE_V1|"+expected).encode()).hexdigest(),16)%6
    assert role_for(expected)==("FIT" if remainder<2 else "SELECT" if remainder==2 else "EVAL")
    assert case_rank(members[0])==hashlib.sha256(("POST_FEASIBILITY_CASE_V1|"+members[0]).encode()).digest()
    with pytest.raises(ValueError): component_id((members[0],members[0]))


def test_cap_before_quota_insufficiency_and_exclusion():
    members=tuple(sorted(synthetic_id(i) for i in range(100)))
    family=Family(independent_component(members),members)
    actual=allocate((family,),eligible_ids=members)
    expected=independent_allocation((members,),members,())
    for result in actual:
        assert (result.selected_ids,result.selected_components,result.available_cases,result.sufficient)==expected[result.role]
        assert not result.sufficient
        assert decode_record(encode_record(result))==result
    assert sum(r.available_cases for r in actual)==60
    assert sum(r.available_cases for r in allocate((family,),eligible_ids=members,excluded_ids=(members[99],)))==0
    with pytest.raises(ValueError): allocate((family,family),eligible_ids=members)
    with pytest.raises(ValueError): allocate((family,),eligible_ids=(synthetic_id("unknown"),))


def test_fixed_full_synthetic_quota_allocation():
    groups=tuple(tuple(sorted(synthetic_id(("invented-component",i,j)) for j in range(60))) for i in range(600))
    families=tuple(Family(independent_component(g),g) for g in groups)
    eligible=tuple(m for g in groups for m in g)
    actual=allocate(families,eligible_ids=eligible)
    expected=independent_allocation(groups,eligible,())
    assert [len(r.selected_ids) for r in actual]==[4000,2000,6000]
    for result in actual:
        assert (result.selected_ids,result.selected_components,result.available_cases,result.sufficient)==expected[result.role]
        assert result.sufficient
    assert actual==allocate(tuple(reversed(families)),eligible_ids=tuple(reversed(eligible)))


def test_selected_component_minimum_is_independent_of_cases():
    # Enough FIT cases from only 67 components cannot meet its 80-component minimum.
    groups=[]; i=0
    while len(groups)<67:
        members=tuple(sorted(synthetic_id(("invented-fit",i,j)) for j in range(60)))
        c=independent_component(members)
        remainder=int(hashlib.sha256(("POST_FEASIBILITY_ACCEPTANCE_V1|"+c).encode()).hexdigest(),16)%6
        if remainder<2: groups.append(members)
        i+=1
    families=tuple(Family(independent_component(g),g) for g in groups)
    fit=allocate(families,eligible_ids=tuple(m for g in groups for m in g))[0]
    assert len(fit.selected_ids)==4000
    assert fit.selected_components==67 and not fit.sufficient
    assert fit.failure_reasons==("insufficient_selected_components",)

def test_component_records_roundtrip_and_iterable_order():
    members=tuple(sorted(synthetic_id(i) for i in range(3)))
    family=Family(independent_component(members),members)
    assert decode_record(encode_record(family))==family
    assert allocate(iter((family,)),eligible_ids=members)==allocate((family,),eligible_ids=members)
