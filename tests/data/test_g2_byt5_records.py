import json

import pytest

from benchmarks.g2_byt5_qualification import serialize
from src.scoring.records import Output, aggregate, prepare_source, score_output


@pytest.mark.parametrize("text,status", [("a b", "complete"), ("a", "capped"),
    (None, "invalid_utf8"), ("", "complete")])
def test_actual_scored_byt5_record_retains_sets_bounds_and_aggregate(text, status):
    score = score_output(prepare_source("a b", "a x"), Output(text, status))
    record = dict(id="synthetic-case", score=score, status=status,
        decoded=dict(text=text, status=status), generated_ids=[0, 1])
    with pytest.raises(TypeError, match="set"):
        json.dumps(record)
    loaded = json.loads(serialize(record))
    assert loaded["id"] == record["id"] and loaded["decoded"] == record["decoded"]
    assert loaded["generated_ids"] == [0, 1] and loaded["status"] == status
    assert set(loaded["score"]) == set(score)
    for name in ("repair", "completed_repair", "introduced", "unresolved"):
        assert loaded["score"][name] == list(score[name])
    assert aggregate([loaded["score"]]) == aggregate([score])
    assert serialize(json.loads(serialize(record))) == serialize(record)
