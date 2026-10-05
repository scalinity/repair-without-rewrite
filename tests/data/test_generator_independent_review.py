"""Hand-authored visible sources; no constructor traces select inverse answers."""
import copy
import hashlib
import json
from pathlib import Path
import pytest

from src.generation.stress import GRAMMARS, generate_group, inverse, inverse_baseline, score, validate_split_leakage


@pytest.mark.parametrize('category,source_values,target_values', [
    ('signs_numerical',('-l0.05','+20.l0'),('-10.05','+20.10')),
    ('negation',('n ot','ne ver'),('not','never')),
    ('versions',('l.O.l','l.20.O-rcl'),('1.0.1','1.20.0-rc1')),
    ('paths',(' slash devstem slash run_10 dot bin','/devstem/run_20.bin'),('/devstem/run_10.bin','/devstem/run_20.bin')),
    ('identifiers',('devstem underscore 10','devstem_20'),('devstem_10','devstem_20')),
    ('units_quantities',('lO milliseconds','2 kilograms'),('10 ms','2 kg')),
    ('repeated_literals',('l0','10'),('10','10')),
    ('multiple_bindings',('l0 milliseconds','2 seconds'),('10 ms','2 s')),
])
def test_source_only_inverse_from_hand_derived_typed_values(category,source_values,target_values):
    grammar=next(g for g in GRAMMARS if g.family_id==f'dev/{category}/cell0')
    source=grammar.scaffold[0]+source_values[0]+grammar.scaffold[1]+source_values[1]+grammar.scaffold[2]
    expected=grammar.scaffold[0]+target_values[0]+grammar.scaffold[1]+target_values[1]+grammar.scaffold[2]
    answer=inverse(source)
    assert answer.status=='unique' and answer.candidates==(expected,)
    assert inverse_baseline(source)==expected
    assert inverse(source,state_cap=1).status=='capped'


def test_confusable_scope_and_hidden_replacement_do_not_invent_target():
    # An integer inverse cannot consume unrestricted prose or a Unicode look-alike.
    assert inverse('unrestricted retry l0').status=='no_inverse'
    grammar=next(g for g in GRAMMARS if g.family_id=='dev/repeated_literals/cell0')
    invalid=grammar.render(('Ⅰ0','10'))
    assert inverse(invalid).status=='no_inverse'
    valid=grammar.render(('11','11'))
    assert inverse(valid).unique_target==valid  # A sampled hidden 10 cannot select this answer.


def test_polarity_erasure_is_not_hidden_target_restoration():
    grammar=next(g for g in GRAMMARS if g.family_id=='dev/negation/cell0')
    source=grammar.render(('','never'))
    assert inverse(source).unique_target==source
    diagnostic=inverse(source,policy='underdetermined_diagnostic_v1')
    assert diagnostic.status=='ambiguous' and len(diagnostic.candidates)==4
    assert inverse_baseline(source)==source


def test_model_input_export_contains_no_latent_answer_or_corruption_fields():
    folder=Path('experiments/manifests/stress_foundation_20261005T051039Z')
    inputs=[json.loads(line) for line in (folder/'model_inputs.jsonl').read_text().splitlines()]
    latents={r['case_id']:r for r in map(json.loads,(folder/'latents.jsonl').read_text().splitlines())}
    assert len(inputs)==288 and len(latents)==288
    for row in inputs:
        assert set(row)=={'case_id','source_utf8','task_id'}
        assert row['task_id']=='restore_reference'
        assert row['source_utf8']==latents[row['case_id']]['source_utf8']
    # case_id is a join key containing view/category; it must never enter model tokens.


def test_complete_parser_keeps_wrong_field_and_rejects_extra_content():
    record=generate_group('multiple_bindings',0,0)[2]
    grammar=next(g for g in GRAMMARS if g.family_id==record['template_id'])
    first,second=(f['reference_surface'] for f in record['fields'])
    result=score(record,grammar.render((first,'wrong')))
    assert result['field_success']==[True,False] and result['structure_valid']
    for candidate in [grammar.render((first,second))+' suffix',
                      'prefix '+grammar.render((first,second)),
                      grammar.render((first,second))+grammar.render((first,second)),
                      grammar.render((first,second))[:-1]]:
        outcome=score(record,candidate)
        assert not outcome['whole_case_conformance'] and outcome['field_success']==[False,False]
    assert score(record,grammar.render((first,second)),complete=False)['field_success']==[False,False]


def test_cross_partition_duplicate_bundle_is_blocked():
    # Inject the previously possible bundle reuse despite different split labels.
    # Values are independently read from visible clean source text.
    train=generate_group('negation',0,0,partition='train')[0]
    dev=copy.deepcopy(generate_group('negation',0,0)[0])
    def visible_values(record):
        grammar=next(g for g in GRAMMARS if g.family_id==record['template_id'])
        prefix,middle,suffix=grammar.scaffold
        body=record['source_utf8'][len(prefix):-len(suffix)]
        return tuple(body.split(middle))
    values=visible_values(train)
    grammar=next(g for g in GRAMMARS if g.family_id==dev['template_id'])
    dev['source_utf8']=dev['reference_utf8']=grammar.render(values)
    dev['source_sha256']=dev['reference_sha256']=hashlib.sha256(dev['source_utf8'].encode()).hexdigest()
    for field,value in zip(dev['fields'],values):
        field.update(canonical_value={'polarity':'negative','surface':value},reference_surface=value,
                     surface_rendering=value,allowed_target_surfaces=[value])
    pair=(train,dev)
    assert visible_values(pair[0])==visible_values(pair[1])
    assert pair[0]['source_sha256']!=pair[1]['source_sha256']
    with pytest.raises(ValueError,match='bundle'):
        validate_split_leakage(pair)
