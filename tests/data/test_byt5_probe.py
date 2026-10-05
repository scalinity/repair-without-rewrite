import pytest
from src.inference.byt5_probe import decode_ids, native_batch, validate_config


def config():
    return dict(scope='SYNTHETIC_DEVELOPMENT_PATH_ONLY',updates=10,batch_size=2,
                source_capacity=64,target_capacity=64,decode_max_new_tokens=64,device='cpu',training_wall_seconds_cap=180)


def test_probe_native_terminal_and_prefix_failure_contract():
    assert decode_ids([0,1])=={'text':'','status':'complete','reason':None}
    assert decode_ids([0,198,172,1,0])['text']=='é'
    assert decode_ids([0,100])['status']=='capped'
    for ids in [[1],[0,259,1],[0,258,1],[0,198],[0,1,100]]:
        assert decode_ids(ids)['status']=='invalid_utf8'


def test_probe_bos_attention_and_supervised_eos_with_variable_targets():
    rows=[dict(source='x',reference=''),dict(source='é',reference='ab')]
    batch,count=native_batch(rows,config(),'cpu')
    assert count==4
    assert batch['decoder_input_ids'].tolist()==[[0,1,0],[0,100,101]]
    assert batch['decoder_attention_mask'].tolist()==[[1,0,0],[1,1,1]]
    assert batch['labels'].tolist()==[[1,-100,-100],[100,101,1]]


def test_probe_role_capacity_and_workload_barriers():
    rows=[dict(id='x',role='train',source='a',reference='a')]
    validate_config(config(),rows)
    with pytest.raises(ValueError,match='role'):validate_config(config(),[{**rows[0],'role':'sealed_final'}])
    with pytest.raises(ValueError,match='limit'):validate_config({**config(),'updates':51},rows)
    with pytest.raises(ValueError,match='truncate'):validate_config(config(),[{**rows[0],'source':'x'*64}])
