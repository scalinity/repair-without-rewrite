import pytest
from benchmarks.bc_real_calibration import shape,select_buckets,check_anchor_bound,decode_literal
from src.models.tokenizer import ByteBPE


def test_real_shapes_bind_utf8_content_and_complete_event_cost():
    t=ByteBPE.train(["é🙂 foo","é🙂 bar"],3)
    row=shape({"id":"x","source":"é🙂 foo","target":"é🙂 bar"},t)
    assert row["source_ids"][:2]==[308,259]
    assert row["source_ids"][-1]==258
    assert t.decode(row["source_ids"][2:-1])==row["source"]
    assert row["byte_offsets"][-1]==len(row["source"].encode())
    assert row["c_positions"]==1+row["R"]+3*row["K"]
    assert row["anchors"]==2*len(t.encode(row["target"]))+3
    assert 256 not in row["target_ids"]


def test_preselection_spans_three_densities_and_source_lengths():
    rows=[{"id":str(i),"density":i//20,"source_bpe":i%20} for i in range(60)]
    selected=select_buckets(rows)
    assert len({r["id"] for r in selected})==12
    assert {r["bucket"] for r in selected}=={"low","median","high"}
    for density in range(3):
        lengths=[r["source_bpe"] for r in selected if r["density"]==density]
        assert min(lengths)<5 and max(lengths)>15


def test_complete_batch_cap_and_decode_failure_provenance():
    check_anchor_bound(7999786,214,8000000)
    with pytest.raises(RuntimeError):check_anchor_bound(7999786,238,8000000)
    t=ByteBPE()
    for ids,kind in (([258],"ValueError"),([195],"UnicodeDecodeError")):
        text,status,raw=decode_literal(t,{"token_ids":ids,"status":"completed"})
        assert text is None and status=="invalid_byte_decoding"
        assert raw["underlying_model_status"]=="completed"
        assert raw["decode_failure"]["type"]==kind
    assert decode_literal(t,{"token_ids":[97],"status":"capped"})[:2]==("a","capped")
