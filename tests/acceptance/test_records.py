"""NONSCIENTIFIC round trips and JSON validation."""
import json
import pytest
from dataclasses import replace
from src.acceptance.records import encode_record,decode_record,NumericalReceipt
from src.acceptance.features import structural_features
from src.acceptance.scores import aggregate_trace
from src.acceptance.policy import fit_policy
from src.acceptance.selection import select_threshold
from src.acceptance.decision import decide
from .fixtures import fit_rows,selection_rows,trace,synthetic_isolation


def test_versioned_typed_round_trips_preserve_binary64():
    records=[structural_features("é","e"),
        aggregate_trace("a","a",trace("a","a",(-.12345678901234567,-.5))),
        fit_policy(fit_rows(),"STRUCTURAL"),
        select_threshold(selection_rows(),"PRIMARY"),
        decide("a","b",proposal_status="complete",predicted_utility=2.,threshold=1.)[1],
        NumericalReceipt("invented","PASS",(1.2345678901234567,),())]
    for record in records:
        encoded=encode_record(record)
        assert "NONSCIENTIFIC" in encoded
        restored=decode_record(encoded)
        assert restored==record and encode_record(restored)==encoded
        assert encoded==json.dumps(json.loads(encoded),ensure_ascii=False,sort_keys=True,separators=(",",":"))
    encoded=encode_record(select_threshold((),"PRIMARY"))
    assert '"threshold":null' in encoded and "Infinity" not in encoded


@pytest.mark.parametrize("bad", [
    '{"schema_version":"other","type":"Policy","fields":{}}',
    'NaN','Infinity','{"x":1,"x":2}','[]',
])
def test_bad_record_schemas_and_nonstandard_values(bad):
    with pytest.raises(ValueError): decode_record(bad)


def test_numerical_overflow_unknown_fields_and_provenance_rejected():
    record=structural_features("a","b")
    obj=json.loads(encode_record(record))
    for field,value in (("values",[1e309]*8),("provenance","SCIENTIFIC"),("reference","forbidden")):
        changed=json.loads(encode_record(record)); changed["fields"][field]=value
        with pytest.raises(ValueError): decode_record(json.dumps(changed))
    for v in (float("nan"),float("inf"),True):
        with pytest.raises(ValueError): NumericalReceipt("invented","PASS",(v,),())
