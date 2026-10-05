import pytest
from src.scoring.triple import score_tokens
from src.scoring.oracle import dense_triple

FIXTURES = [
    ('identity','red blue','red blue','red blue',(0,0),(0,0)),
    ('repair','red blue','red green','red blue',(1,1),(0,0)),
    ('damage','red blue','red blue','red green',(0,0),(1,1)),
    ('wrong_different_wrong','red blue','red green','red black',(0,0),(0,0)),
    ('collateral','a b c d','a x c d','a b y d',(1,1),(1,1)),
    ('repair_deletion','a b','a','a b',(1,1),(0,0)),
    ('new_deletion','a b','a b','a',(0,0),(1,1)),
    ('repair_insertion','a b','a x b','a b',(1,1),(0,0)),
    ('new_insertion','a b','a b','a x b',(0,0),(1,1)),
    ('repeated_identity','a a','a','a',(0,0),(0,0)),
    ('repeated_repair','a a','a','a a',(1,1),(0,0)),
    ('leading_trailing','a b','a b','z a b q q',(0,0),(3,3)),
    ('gap_tie','START END','START a b END','START b c END',(0,1),(0,1)),
    ('reorder','a b','a b','b a',(0,0),(2,2)),
    ('valid_empty','a b','a b','',(0,0),(2,2)),
    ('empty_reference','','','x y',(0,0),(2,2)),
    ('missing_raw','a','a x','',(1,1),(1,1)),
    ('capped_raw','a b','a x','a b',(1,1),(0,0)),
    ('noncoexisting_optima','a b c','b c a','c a b',(2,2),(2,2)),
    ('all_empty','','','',(0,0),(0,0)),
    ('source_only','','a b','',(2,2),(0,0)),
]

@pytest.mark.parametrize('name,r,s,o,repair,introduced',FIXTURES,ids=[f[0] for f in FIXTURES])
def test_fixture(name,r,s,o,repair,introduced):
    actual=score_tokens(tuple(r.split()),tuple(s.split()),tuple(o.split()))
    independent=dense_triple(tuple(r.split()),tuple(s.split()),tuple(o.split()))
    assert actual['repair']==repair==independent['repair']
    assert actual['introduced']==introduced==independent['introduced']
    assert actual['h']==independent['h']
    for a,b in zip(actual['repair'],actual['introduced']):
        assert a-b==actual['eS']-actual['eO']
