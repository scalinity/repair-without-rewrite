import json
import pytest
from benchmarks import g2_historical_compatibility as historical
from benchmarks import g2_parakeet_sources as source
from benchmarks import g2_source_audio as audio


@pytest.mark.parametrize("module,invoke", [
    (historical, lambda p: historical.run(p, "B100", 1)),
    (source, lambda p: source.run(p, 1)),
    (audio, lambda p: audio.extract(p, "dev-clean", 1))])
def test_unavailable_external_root_precedes_native_libraries_and_output(tmp_path, monkeypatch, module, invoke):
    def missing(_):
        raise FileNotFoundError("missing external root")
    monkeypatch.setattr(module, "ArtifactRoot", missing)
    with pytest.raises(FileNotFoundError):
        invoke(tmp_path / "missing")
    assert list(tmp_path.iterdir()) == []


def test_checkpoint_update_comparison_uses_exact_persisted_labels_without_numeric_tolerance():
    observed = {name: 1 for name in historical.DETERMINISTIC_UPDATE_FIELDS}
    observed["actual_consumption"] = [{"native_event_labels": {"action": (0, 1, 2)}}]
    expected = json.loads(json.dumps(observed))
    assert historical.differing_update_fields(observed, expected) == []
    expected["actual_consumption"][0]["native_event_labels"]["action"][1] = 9
    assert historical.differing_update_fields(observed, expected) == ["actual_consumption"]
    expected = json.loads(json.dumps(observed))
    observed["loss"] = 1.0000000000000002
    assert historical.differing_update_fields(observed, expected) == ["loss"]
