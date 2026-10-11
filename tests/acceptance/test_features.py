"""NONSCIENTIFIC feature conformance."""
import itertools
import math
import pytest
from src.acceptance.features import structural_features, edit_counts, distance
from .independent_oracles import tiny_alignments, recursive_distance
from .fixtures import synthetic_isolation


def test_exhaustive_225_lexical_alignments():
    seqs = [p for n in range(4) for p in itertools.product(("a","b"),repeat=n)]
    for source, proposal in itertools.product(seqs,repeat=2):
        expected = tiny_alignments(source,proposal)
        assert edit_counts(source,proposal) == expected[:3]
        assert distance(source,proposal) == expected[3]


@pytest.mark.parametrize("source,proposal,counts", [
    ("","",(0,0,0)), ("","a b",(2,0,0)), ("a b","",(0,2,0)),
    ("a b","b a",(0,0,2)), ("a a","a",(0,1,0)),
    ("Don't café","don’t cafe\u0301",(0,0,0)),
    ("RED, blue!","red blue",(0,0,0)), ("é","e",(0,0,1)),
])
def test_feature_order_lengths_and_edit_orientation(source,proposal,counts):
    actual = structural_features(source,proposal)
    sb,ob = source.encode(),proposal.encode()
    # Invented cases above have manually specified word counts.
    lengths = {"":0,"a b":2,"a":1,"b a":2,"a a":2,"Don't café":2,
               "don’t cafe\u0301":2,"RED, blue!":2,"red blue":2,"é":1,"e":1}
    ns,no = lengths[source],lengths[proposal]
    expected = (math.log1p(ns),math.log1p(no),math.log1p(len(sb)),math.log1p(len(ob)),
        *(v/max(1,ns) for v in counts),recursive_distance(sb,ob)/max(1,len(sb)))
    assert actual.values == expected
    assert actual.provenance == "NONSCIENTIFIC"


def test_multibyte_distance_is_byte_distance():
    actual=structural_features("é","e")
    assert recursive_distance("é","e")==1
    assert actual.values[7]==1.0  # two byte edits / two source bytes
    assert structural_features("","🐢").values[7]==4


@pytest.mark.parametrize("bad", [None,42,b"\xff","\ud800"])
def test_bad_text_is_rejected(bad):
    with pytest.raises((ValueError,UnicodeError)):
        structural_features(bad,"invented")
