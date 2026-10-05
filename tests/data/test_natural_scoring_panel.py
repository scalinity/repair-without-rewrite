import pytest
from benchmarks.natural_output_scoring import validate_panels


def test_repeated_panels_retain_every_request_and_fixed_source():
    rows=[{"id":str(i),"step":s,"reference":"gold","raw_source":"source"} for s in (0,200,600) for i in range(24)]
    assert len(validate_panels(rows))==24
    for bad in (rows[:-1],rows+[rows[0]],[{**r,"raw_source":"changed"} if j==25 else r for j,r in enumerate(rows)]):
        with pytest.raises(ValueError):validate_panels(bad)
