import numpy as np
import pytest
import mlx.core as mx
import mlx.nn as nn
from mlx.utils import tree_flatten
from src.models.core import EncoderDecoderConfig, parameter_inventory, masked_cross_entropy
from src.models.bc import B100, C101, boundary_features, pointer_mask, c_microbatch_loss
from src.models.training import GradientAccumulator, flat_parameters
from src.models.edits import (canonical_labels, events, update_denominators,
                              normalized_component_loss, EditContractError)


def tiny_config():
    return EncoderDecoderConfig(vocab_size=320,width=16,encoder_layers=1,decoder_layers=1,
                                q_heads=2,kv_heads=1,ffn_width=32,max_context=32)


def example(source,target):
    labels = canonical_labels(source,target,tuple(bytes([byte]) for byte in source.encode()))
    event = events(labels,lambda text:list(text.encode()),{i:i for i in range(len(source)+1)},max_context=32)
    return dict(source_ids=mx.array([[308,259,*source.encode()]],dtype=mx.int32),labels=event,
                encoder_positions=tuple(range(1,len(source)+2)),legal=mx.array([True]*(len(source)+1)))


def all_close(a,b,tol=2e-5):
    mx.eval(a,b)
    assert np.max(np.abs(np.array(a)-np.array(b))) <= tol


def test_exact_b100_c101_unique_leaf_inventories():
    b = B100()
    inventory = parameter_inventory(b)
    assert sum(leaf["count"] for leaf in inventory) == 100686336 == b.config.parameter_count()
    assert len([x for x in inventory if x["name"] == "embedding"]) == 1
    assert all("bias" not in leaf["name"] for leaf in inventory)
    del b
    c = C101()
    inventory = parameter_inventory(c)
    assert sum(leaf["count"] for leaf in inventory) == 101081859
    assert len([x for x in inventory if "bias" in x["name"]]) == 1
    assert next(x for x in inventory if x["name"] == "action_bias")["shape"] == [3]
    assert c.start_query.weight is not c.end_query.weight
    assert c.start_key.weight is not c.end_key.weight


def test_b_encoder_bidirectional_decoder_causal_and_source_padding():
    model = B100(tiny_config(),42)
    source = mx.array([[308,259,97,98,99]])
    changed_source = mx.array([[308,259,97,98,100]])
    encoded = model.encode(source); changed = model.encode(changed_source)
    assert float(mx.max(mx.abs(encoded[:,0]-changed[:,0])).item()) > 1e-6
    dec = mx.array([[257,97,98]])
    other = mx.array([[257,97,100]])
    all_close(model(source,dec)[:,:2],model(source,other)[:,:2])
    valid = mx.array([[True,True,True,True,False]])
    all_close(model(source,dec,valid),model(changed_source,dec,valid))
    with pytest.raises(ValueError): model(source,dec,mx.array([[False]*5]))


def test_bc_cache_one_token_and_chunk_cross_mask_parity():
    model = B100(tiny_config(),43)
    source = mx.array([[308,259,97,98,0]])
    valid = mx.array([[True,True,True,True,False]])
    encoded = model.encode(source,valid)
    ids = mx.array([[257,97,98,99]])
    full,_ = model.decode(ids,encoded,valid)
    one,cache = model.decode(ids[:,:1],encoded,valid)
    chunk,cache = model.decode(ids[:,1:3],encoded,valid,caches=cache)
    final,_ = model.decode(ids[:,3:],encoded,valid,caches=cache)
    all_close(full,mx.concatenate((one,chunk,final),axis=1))
    assert all(cache[i]["cross"][0].shape[-2] == source.shape[-1] for i in range(len(cache)))


def test_c_boundary_feedback_and_conditional_masks():
    model = C101(tiny_config(),44,pointer_width=8)
    sample = example("aa","ba")
    encoded = model.encode(sample["source_ids"])
    boundaries = boundary_features(encoded,sample["encoder_positions"])
    all_close(boundaries[:,0],encoded[:,1])
    all_close(boundaries[:,-1],encoded[:,-1])
    inputs = model.teacher_inputs(sample["labels"],boundaries)
    for i,event in enumerate(sample["labels"].inputs):
        if event.kind == "start_feedback":
            all_close(inputs[0,i],model.embedding[266]+boundaries[0,event.value])
        elif event.kind == "end_feedback":
            all_close(inputs[0,i],model.embedding[267]+boundaries[0,event.value])
    assert pointer_mask(mx.array([True,False,True]),minimum_index=1).tolist() == [False,False,True]
    with pytest.raises(EditContractError): pointer_mask(mx.array([False,False]))
    scores = model.pointer_logits(mx.ones((1,1,16)),boundaries,end=True,
                                  legal=sample["legal"],minimum_index=1)
    assert np.isneginf(np.array(scores)[0,0,0])
    assert np.isfinite(np.array(scores)[0,0,1:]).all()


def test_c_component_denominators_gradient_single_accumulator_uneven_microbatches():
    model = C101(tiny_config(),45,pointer_width=8)
    examples = [example("aa","ba"),example("ab","ab"),example("bb","b")]
    denominator = update_denominators([[x["labels"] for x in examples]])
    loss = lambda model,rows:c_microbatch_loss(model,rows,denominator)
    value_and_grad = nn.value_and_grad(model,loss)
    whole,grad = value_and_grad(model,examples)
    first,g1 = value_and_grad(model,examples[:1])
    rest,g2 = value_and_grad(model,examples[1:])
    all_close(whole,first+rest)
    accumulator = GradientAccumulator(flat_parameters(model))
    accumulator.add(g1); accumulator.add(g2)
    accumulated = accumulator.gradients(already_normalized=True)
    assert accumulator.denominator == 0 and accumulator.microbatches == 2
    g1,g2 = dict(tree_flatten(g1)),dict(tree_flatten(g2))
    for name,leaf in tree_flatten(grad):
        all_close(leaf,g1[name].astype(mx.float32)+g2[name].astype(mx.float32),tol=5e-5)
        all_close(leaf,accumulated[name],tol=5e-5)
        assert leaf.dtype == mx.float32 and bool(mx.all(mx.isfinite(leaf)).item())
    # Identity still trains END and no pointer/vocabulary component.
    identity = examples[1]
    sums = model.component_sums(**identity)
    assert all(float(sums[key].item()) == 0 for key in ("start","end","vocabulary"))
    assert float(sums["action"].item()) > 0


def test_c_pointer_and_action_gradient_finite_difference():
    model = C101(tiny_config(),46,pointer_width=8)
    sample = example("aa","ba")
    denominator = sample["labels"].denominators
    def loss(model):
        return normalized_component_loss(model.component_sums(**sample),denominator)
    value,grad = nn.value_and_grad(model,loss)(model)
    for name,index in (("action_bias",(0,)),("start_query.weight",(0,0)),("end_query.weight",(0,0))):
        module,attr = (model,name) if "." not in name else (getattr(model,name.split(".")[0]),"weight")
        original = getattr(module,attr)
        analytic = dict(tree_flatten(grad))[name][index]
        eps = 1e-3
        perturb = mx.zeros_like(original).at[index].add(eps)
        setattr(module,attr,original+perturb); plus = loss(model)
        setattr(module,attr,original-perturb); minus = loss(model)
        setattr(module,attr,original)
        numeric = (plus-minus)/(2*eps)
        assert float(mx.abs(numeric-analytic).item()) < 2e-3


def test_c_greedy_source_binding_rejected_before_encoding():
    from src.models.bc import validate_source_binding
    mapping = lambda token:bytes([token])
    validate_source_binding("a",[308,259,97],(1,2),(0,1),(True,True),mapping)
    validate_source_binding("",[308,259],(1,),(0,),(True,),mapping)
    for args in [
        ("a",[308,259,98],(1,2),(0,1),(True,True)),
        ("a",[308,259,97],(1,2),(0,2),(True,True)),
        ("a",[308,259,97],(1,2),(0,1),(True,False)),
        ("a",[308,259,97,98],(1,2),(0,1),(True,True)),
        ("a",[308,259,97],(1,1),(0,1),(True,True)),
    ]:
        with pytest.raises(EditContractError):validate_source_binding(*args,mapping)
    validate_source_binding("é",[308,259,195,169],(1,2,3),(0,1,2),(True,False,True),mapping)
    with pytest.raises(EditContractError):
        validate_source_binding("é",[308,259,195,169],(1,2,3),(0,1,2),(True,True,True),mapping)
    # Exercise the public method: the mismatch must fail before any encoding.
    class PureArray:
        def __init__(self,value,ndim=1):self.value=value;self.ndim=ndim;self.shape=(1,len(value[0])) if ndim==2 else (len(value),)
        def tolist(self):return self.value
    class NeverEncode:
        def encode(self,*args,**kwargs):raise AssertionError("encoding occurred before validation")
    with pytest.raises(EditContractError,match="encoded source bytes"):
        C101.greedy_edits(NeverEncode(),"a",PureArray([[308,259,98]],ndim=2),(1,2),(0,1),PureArray([True,True]),mapping)
