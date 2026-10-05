import itertools
import json
import random
import pytest
from src.scoring.oracle import enumerate_triple, dense_triple, pair_oracle
from src.scoring.triple import score_tokens, lattice, source_masks, Limits, serialize
from src.scoring.records import prepare_source, score_output, Output, aggregate
from src.scoring.text import lexical, normalize_tokens, strict_text, _nfc_with_origins, TABLE_ROOT
import unicodedata2 as ud

SEQUENCES=[tuple(v) for length in range(4) for v in itertools.product('ab',repeat=length)]


def test_exhaustive_3375_triples():
    count=0
    for r,s,o in itertools.product(SEQUENCES,repeat=3):
        actual=score_tokens(r,s,o);expected=enumerate_triple(r,s,o)
        for key in ('eS','eO','h','repair','introduced','reference_events'):
            assert actual[key]==expected[key],(r,s,o,key,actual,expected)
        assert serialize(actual)==serialize(score_tokens(r,s,o))
        assert json.loads(serialize(actual))==json.loads(serialize(json.loads(serialize(actual))))
        count+=1
    assert count==3375


def test_exhaustive_225_pair_lattices_and_masks():
    count=0
    for r,s in itertools.product(SEQUENCES,repeat=2):
        actual=lattice(r,s);expected=pair_oracle(r,s)
        edges={(u,v) for u,vs in actual['edges'].items() for v in vs}
        assert edges==expected['edges']
        masks=source_masks(r,s,actual)
        assert [set(v) for v in masks['reference']]==expected['reference_mappings']
        assert masks['pair_unique']==(expected['paths']==1)
        count+=1
    assert count==225


def assert_invariants(result):
    r0,r1=result['repair'];i0,i1=result['introduced'];es,eo=result['eS'],result['eO']
    assert 0<=r0<=r1<=es and 0<=i0<=i1<=eo
    assert r0-i0==r1-i1==es-eo
    assert max(0,es-eo)<=r0 and max(0,eo-es)<=i0


def test_10000_fixed_seed_properties():
    rng=random.Random(20261004)
    for trial in range(10000):
        r,s,o=[tuple(rng.choice(('a','b','c','ε','😀','-')) for _ in range(rng.randrange(7))) for _ in range(3)]
        result=score_tokens(r,s,o);assert_invariants(result)
        independent=dense_triple(r,s,o)
        for key in ('eS','eO','h','repair','introduced'):
            assert result[key]==independent[key],(trial,r,s,o,key)
        assert score_tokens(r,s,s)['repair']==(0,0)
        assert score_tokens(r,s,r)['repair']==(result['eS'],)*2
        assert score_tokens(r,r,o)['introduced']==(result['eO'],)*2


def test_500_preselected_development_parity():
    manifest=json.loads(open('experiments/manifests/scorer_development_parity.json').read())
    assert manifest['kind']=='SYNTHETIC_DEVELOPMENT_ONLY'
    assert len(manifest['triples'])==500
    for row in manifest['triples']:
        r,s,o=map(tuple,(row['r'],row['s'],row['o']))
        assert max(map(len,(r,s,o)))<=64
        actual=score_tokens(r,s,o);independent=dense_triple(r,s,o)
        for key in ('eS','eO','h','repair','introduced'):
            assert actual[key]==independent[key],(row['id'],key)


def test_metamorphic_relations():
    rows=[score_output(prepare_source('red blue','red wrong'),Output('red blue')),
          score_output(prepare_source('one two','one two'),Output('one bad'))]
    a,b=aggregate(rows),aggregate(rows*2)
    for key in ('wer','introduced_rate','completed_repair_rate'):
        assert a[key]==b[key]==aggregate(reversed(rows))[key]
    rng=random.Random(20261004)
    for _ in range(100):
        triple=[tuple(rng.choice('abc') for _ in range(5)) for _ in range(3)]
        actual=score_tokens(*triple)
        renamed=score_tokens(*(tuple({'a':'xx','b':'yy','c':'zz'}[v] for v in seq) for seq in triple))
        reverse=score_tokens(*(seq[::-1] for seq in triple))
        for key in ('repair','introduced','eS','eO','h'):
            assert actual[key]==renamed[key]==reverse[key]
    assert score_tokens(('L','x','R'),('L','x','R'),('L','bad','R'))['introduced']==(1,1)
    assert score_tokens(('L','x','R'),('L','bad','R'),('L','x','R'))['repair']==(1,1)


@pytest.mark.parametrize('status',['missing','invalid_utf8','invalid_c','abstain','timeout_no_prefix','capped','timeout_prefix'])
def test_failure_credit_and_source_immutability(status):
    prepared=prepare_source('a','a x')
    before=serialize(prepared.masks)
    record=score_output(prepared,Output('a',status))
    assert record['completed_repair']==(0,0)
    assert not record['complete_valid']
    assert before==serialize(prepared.masks)
    assert record['source_mask_hash']==prepared.mask_hash
    assert record['reference_words']==1 and record['eS']==1


def test_empty_and_invalid_distinctions():
    p=prepare_source('','x')
    empty=score_output(p,Output(''));missing=score_output(p,Output(None,'missing'))
    assert empty['completed_repair']==(1,1) and missing['completed_repair']==(0,0)
    assert empty['lexical_exact'] and not missing['lexical_exact']
    assert aggregate([empty])['wer'] is None
    with pytest.raises(ValueError):prepare_source(None,'x')
    with pytest.raises(UnicodeError):prepare_source(b'\xff','x')
    assert score_output(prepare_source('a','a'),Output(b'\xff'))['failure_reason']=='invalid_utf8'


def test_budget_fallback_contains_exact():
    triple=(('a','b','c'),('b','c','a'),('c','a','b'))
    exact=score_tokens(*triple)
    for limits in (Limits(joint_states=1),Limits(joint_moves=4),Limits(pair_cells=1)):
        fallback=score_tokens(*triple,limits=limits)
        for key in ('repair','introduced'):
            assert fallback[key][0]<=exact[key][0]<=exact[key][1]<=fallback[key][1]
        assert fallback['status']=='resource_envelope'
        assert fallback['eO']==exact['eO'] and fallback['eS']==exact['eS']


def test_output_cannot_recompute_unavailable_source_eligibility():
    prepared=prepare_source('a a','a',limits=Limits(pair_cells=1))
    assert prepared.masks['status']=='computationally_unavailable'
    record=score_output(prepared,Output('a a'))
    assert record['source_masks']==prepared.masks
    assert record['source_consensus_eligible_counts'] is None
    assert record['fixed_correct_damage'] is None


def test_surface_scanner_and_origins():
    assert lexical("DON’T mother‐in‑law")==("don't",'mother-in-law')
    assert lexical("'a-' -5 −5 +5 10%")==( 'a','-','-','5','−','5','+','5','10','%')
    assert lexical('file_name 2.1')==lexical('file name 2 1')
    assert lexical('café')==lexical('cafe\u0301')
    assert lexical('İ')==('i\u0307',)
    assert lexical('Straße')==('strasse',)
    assert lexical('\ufeff\x00😀\u0301')==('\ufeff','\x00','😀','\u0301')
    assert lexical('ε')==('ε',)
    assert lexical('a a')==('a','a')
    normalized,tokens=normalize_tokens('cafe\u0301 Straße')
    assert normalized=='café strasse'
    assert tokens[0].raw_byte_span==(0,6) and tokens[1].raw_byte_span==(7,14)
    record=score_output(prepare_source('café','café'),Output('cafe\u0301'))
    assert record['eO']==0 and record['surface_character_errors']==2
    assert not record['raw_byte_exact'] and record['lexical_exact']
    assert lexical('a\r\nb')==lexical('a\nb')
    with pytest.raises(UnicodeError):strict_text('\ud800')


def test_unicode_151_normalization_conformance():
    count=0
    for line in (TABLE_ROOT/'NormalizationTest.txt').read_text().splitlines():
        data=line.split('#',1)[0].strip()
        if not data or data.startswith('@'):continue
        columns=[''.join(chr(int(v,16)) for v in column.split()) for column in data.split(';')[:5]]
        c1,c2,c3,c4,c5=columns
        for value in (c1,c2,c3):
            mapped=''.join(c for c,_ in _nfc_with_origins([(c,frozenset({i})) for i,c in enumerate(value)]))
            assert mapped==c2==ud.normalize('NFC',value)
        for value in (c4,c5):
            mapped=''.join(c for c,_ in _nfc_with_origins([(c,frozenset({i})) for i,c in enumerate(value)]))
            assert mapped==c4==ud.normalize('NFC',value)
        count+=1
    assert count==19074
