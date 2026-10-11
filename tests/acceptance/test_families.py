"""NONSCIENTIFIC all graph edge types, boundaries and transitive bridges."""
from dataclasses import replace
import pytest
from src.acceptance.families import FamilyRecord,close_families,signature,textual_link
from src.acceptance.allocation import allocate
from .fixtures import synthetic_id,synthetic_isolation
from .independent_oracles import graph_components,independent_component


@pytest.mark.parametrize("left,right", [
    ({"speaker":"invented-s"},{"speaker":"invented-s"}),
    ({"recording":"invented-r"},{"recording":"invented-r"}),
    ({"recording":"invented-r"},{"verified_recording_aliases":("invented-r",)}),
    ({"prompt":"invented-p"},{"prompt":"invented-p"}),
    ({"derivations":("invented-work",)},{"derivations":("invented-work",)}),
    ({"duplicate_audio_hash":synthetic_id("audio")},{"duplicate_audio_hash":synthetic_id("audio")}),
    ({"text":"A!"},{"text":"a"}),
    ({"text":"abcdefghij"},{"text":"abcdefghiX"}),
])
def test_every_edge_type(left,right):
    a=FamilyRecord(synthetic_id(1),**({"text":""}|left))
    b=FamilyRecord(synthetic_id(2),**({"text":""}|right))
    groups=close_families((a,b))
    expected=tuple(sorted((a.stable_id,b.stable_id)))
    assert len(groups)==1 and groups[0].members==expected
    assert groups[0].component_id==independent_component(expected)


def test_transitive_ineligible_bridge_and_input_order():
    a=FamilyRecord(synthetic_id(1),"",speaker="invented-s")
    bridge=FamilyRecord(synthetic_id(2),"",speaker="invented-s",prompt="invented-p")
    b=FamilyRecord(synthetic_id(3),"",prompt="invented-p")
    unrelated=FamilyRecord(synthetic_id(4),"")
    rows=(a,bridge,b,unrelated)
    expected=graph_components([r.stable_id for r in rows],[(a.stable_id,bridge.stable_id),(bridge.stable_id,b.stable_id)])
    actual=close_families(rows)
    assert sorted(f.members for f in actual)==expected
    assert actual==close_families(tuple(reversed(rows)))
    allocated=allocate(actual,eligible_ids=(a.stable_id,b.stable_id,unrelated.stable_id),
        excluded_ids=(bridge.stable_id,))
    assert sum(r.available_cases for r in allocated)==1


def test_explicit_known_lineage_links_and_unknown_endpoints():
    rows=tuple(FamilyRecord(synthetic_id(i),"") for i in range(3))
    links=((rows[0].stable_id,rows[1].stable_id),(rows[1].stable_id,rows[2].stable_id))
    assert len(close_families(rows,links))==1
    with pytest.raises(ValueError):
        close_families(rows,((rows[0].stable_id,synthetic_id("absent")),))


def test_text_signature_is_not_lexical_normalization():
    assert signature("A_B café")==("a_b","café")
    assert signature("cafe\u0301")==("café",)
    assert not textual_link((),())
    assert textual_link(("x",),("x",))
    assert not textual_link(signature("abcdefghi"),signature("abcdefghX"))
    assert textual_link(signature("abcdefghij"),signature("abcdefghiX"))


@pytest.mark.parametrize("count,linked",[(19,False),(22,False),(23,True)])
def test_minimum_words_and_exact_point_nine_jaccard(count,linked):
    words=["invented"+str(i) for i in range(count)]
    changed=words[:-1]+["z"*500]
    # Large replacement defeats the independent character-distance rule.
    assert textual_link(tuple(words),tuple(changed))==linked


def test_long_exact_and_character_unicode_boundary():
    words=tuple("x"+str(i) for i in range(100))
    assert textual_link(words,words)
    assert textual_link(signature("éabcdefghi"),signature("xabcdefghi"))
    assert not textual_link(signature("éabcdefgh"),signature("xabcdefgh"))


def test_giant_component_stays_whole():
    rows=tuple(FamilyRecord(synthetic_id(i),"",speaker="invented-one") for i in range(125))
    families=close_families(rows)
    assert len(families)==1 and len(families[0].members)==125
    allocation=allocate(families,eligible_ids=tuple(r.stable_id for r in rows))
    assert sum(r.available_cases for r in allocation)==60


def test_conflicting_stable_identity_is_rejected():
    row=FamilyRecord(synthetic_id(1),"")
    with pytest.raises(ValueError): close_families((row,replace(row,text="invented")))
