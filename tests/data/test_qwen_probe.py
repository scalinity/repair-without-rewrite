import pytest
from src.inference.qwen_probe import strict_bytelevel_text,validate_config


def test_qwen_strict_bytelevel_prefix_cannot_invent_replacement_unicode():
    decoder={'x':120,'C3':195,'A9':169}
    assert strict_bytelevel_text(['x'],decoder,set())=='x'
    assert strict_bytelevel_text(['C','A'],{'C':195,'A':169},set())=='é'
    assert strict_bytelevel_text(['<|im_start|>'],{}, {'<|im_start|>'})=='<|im_start|>'
    with pytest.raises(UnicodeDecodeError):strict_bytelevel_text(['C'],{'C':195},set())


def test_qwen_identity_precision_greedy_and_dev_barriers():
    cfg=dict(repository='Qwen/Qwen3-4B-Instruct-2507',revision='cdbee75f17c01a7cc42f958dc650907174af0554',
        scope='SYNTHETIC_DEVELOPMENT_PATH_ONLY',precision='BF16',device='mps',max_new_tokens=64,
        input_token_cap=512,do_sample=False,num_beams=1)
    rows=[dict(role='hpo_development')];validate_config(cfg,rows)
    for changed in [dict(repository='Qwen/Qwen3-4B'),dict(precision='Q4'),dict(do_sample=True),dict(max_new_tokens=65)]:
        with pytest.raises(ValueError):validate_config({**cfg,**changed},rows)
    with pytest.raises(ValueError):validate_config(cfg,[dict(role='sealed_final')])
