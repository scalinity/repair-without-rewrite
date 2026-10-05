import itertools
import pytest
from src.models.edits import (Edit, EditProgram, EditContractError, source_identity,
    render, canonical_labels, codepoint_boundaries, legal_token_boundaries, events,
    update_denominators, normalized_component_loss)


def program(source, *edits, terminal="END"):
    return EditProgram(*source_identity(source), tuple(edits), terminal)


@pytest.mark.parametrize("source,edits,expected", [
    ("", (), ""), ("α🙂e\u0301\r\n", (), "α🙂e\u0301\r\n"),
    ("abc", (Edit(0,0,"X"), Edit(3,3,"Y")), "XabcY"),
    ("abc", (Edit(1,2,""),), "ac"),
    ("same same", (Edit(5,9,"other"),), "same other"),
    ("abc", (Edit(0,1,"q"), Edit(1,2,"r")), "qrc"),
    ("abc", (Edit(1,1,"X"),Edit(1,1,"Y")), "aXYbc"),
])
def test_renderer_exact_gaps(source, edits, expected):
    assert render(source, program(source,*edits)) == expected
    assert render(source, program(source,*edits)) == expected


@pytest.mark.parametrize("source,edits,terminal", [
    ("abc", (Edit(0,2,"x"),Edit(1,3,"y")), "END"),
    ("🙂", (Edit(1,2,"x"),), "END"),
    ("abc", (Edit(2,1,"x"),), "END"),
    ("abc", (), ""), ("abc", (), "EOS"), ("abc", (), "ABSTAIN"),
])
def test_renderer_rejects_complete_invalid(source, edits, terminal):
    with pytest.raises(EditContractError): render(source, program(source,*edits,terminal=terminal))


def test_source_identity_validation():
    with pytest.raises(EditContractError): render("abd", program("abc"))
    with pytest.raises(EditContractError): render("abc", EditProgram(source_identity("abc")[0], 4, ()))
    with pytest.raises(UnicodeError): render("abc", program("abc",Edit(0,1,"\ud800")))


def test_bpe_utf8_legality():
    assert legal_token_boundaries("é", (b"\xc3",b"\xa9")) == (0,2)
    with pytest.raises(EditContractError): legal_token_boundaries("é", (b"e",))
    with pytest.raises(EditContractError): render("abc",program("abc",Edit(1,2,"d")),pointer_boundaries=(0,3))


def test_canonical_leftmost_expansion_and_merge():
    label = canonical_labels("aaaa", "aaa", (b"a",)*4)
    assert label.edits == (Edit(0,1,""),)
    label = canonical_labels("abc", "axc", (b"abc",))
    assert label.edits == (Edit(0,3,"axc"),)
    label = canonical_labels("abcde", "aXcYe", (b"abcde",))
    assert label.edits == (Edit(0,5,"aXcYe"),)
    label = canonical_labels("🙂e\u0301", "🙂a\u0301", (b"\xf0",b"\x9f\x99\x82e",b"\xcc",b"\x81"))
    assert render("🙂e\u0301",label) == "🙂a\u0301"


def test_exhaustive_canonical_renderer_small_states():
    strings = ["".join(chars) for n in range(4) for chars in itertools.product("ab",repeat=n)]
    for source in strings:
        for target in strings:
            for tokens in ((tuple(bytes([x]) for x in source.encode())), ((source.encode(),) if source else ())):
                labels = canonical_labels(source,target,tokens)
                assert render(source,labels) == target
                assert canonical_labels(source,target,tokens) == labels


@pytest.mark.parametrize("edit_list", [(), (Edit(0,0,"x"),), (Edit(0,1,""),),
    (Edit(0,1,"xy"),), (Edit(0,1,"x"),Edit(2,3,"yz"))])
def test_event_counts_and_shift(edit_list):
    labels = events(program("abc",*edit_list), lambda x:list(x.encode()), {i:i for i in range(4)})
    k, r = len(edit_list), sum(len(e.replacement.encode()) for e in edit_list)
    assert len(labels.inputs) == 1+r+3*k
    assert labels.denominators == dict(action=k+1,start=k,end=k,vocabulary=r+k)
    assert labels.action[-1] == (len(labels.inputs)-1,1)
    for position, target in labels.vocabulary:
        assert labels.inputs[position+1].value == target


def test_abstain_and_context_overflow():
    assert events(program("abc",terminal="ABSTAIN"),lambda x:list(x.encode()),{0:0,3:1}).action == ((0,2),)
    with pytest.raises(EditContractError,match="1027"):
        events(program("x",Edit(0,1,"a"*1023)),lambda x:list(x.encode()),{0:0,1:1})
    with pytest.raises(EditContractError): events(program("abc",Edit(1,2,"d")),lambda x:[256],{1:0,2:1})


def test_whole_update_component_counts_and_zero():
    identity = events(program("abc"),lambda x:list(x.encode()),{i:i for i in range(4)})
    deletion = events(program("abc",Edit(0,1,"")),lambda x:list(x.encode()),{i:i for i in range(4)})
    replacement = events(program("abc",Edit(1,2,"xyz")),lambda x:list(x.encode()),{i:i for i in range(4)})
    counts = update_denominators(((identity,), (deletion,replacement)))
    assert counts == dict(action=5,start=2,end=2,vocabulary=5)
    assert normalized_component_loss(dict(action=2.,start=3.,end=5.,vocabulary=7.),counts) == pytest.approx(5.8)
    only = identity.denominators
    assert normalized_component_loss(dict(action=2.,start=99.,end=99.,vocabulary=99.),only) == 2


def test_seeded_unicode_property_token_expansion_roundtrips():
    import random
    rng = random.Random(20261004)
    alphabet = ["a","b","é","🙂","\u0301","\r","\n"," "]
    for _ in range(500):
        source = "".join(rng.choices(alphabet,k=rng.randrange(9)))
        target = "".join(rng.choices(alphabet,k=rng.randrange(9)))
        raw = source.encode("utf-8")
        cuts = [0]+[i for i in range(1,len(raw)) if rng.randrange(2)]+([len(raw)] if raw else [])
        tokens = tuple(raw[a:b] for a,b in zip(cuts,cuts[1:]))
        labels = canonical_labels(source,target,tokens)
        assert render(source,labels,pointer_boundaries=legal_token_boundaries(source,tokens)) == target
