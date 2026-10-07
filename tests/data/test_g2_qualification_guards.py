import json
import pytest
from benchmarks import g2_historical_compatibility as historical
from benchmarks import g2_parakeet_sources as source
from benchmarks import g2_source_audio as audio
from benchmarks import g2_native_qualification as native
from benchmarks import g2_byt5_qualification as byt5
from benchmarks import g2_corpus_qualification as corpus
from benchmarks import g2_corpus_independent as independent
from benchmarks import g2_archived_evaluation as archived
from benchmarks import g2_native_independent as native_independent
from benchmarks import g2_cost_projection as cost
from benchmarks import g2_byt5_independent as byt5_independent
from benchmarks import g2_cost_independent as cost_independent
from benchmarks import g2_storage_reforecast as storage_reforecast
from benchmarks import g2_archive_independent as archive_independent
from benchmarks import g2_admission_independent as admission_independent
from benchmarks import g2_calibration_consumption as calibration_consumption
from benchmarks import g2_evaluation_summary as evaluation_summary


@pytest.mark.parametrize("module,invoke", [
    (historical, lambda p: historical.run(p, "B100", 1)),
    (source, lambda p: source.run(p, 1)),
    (audio, lambda p: audio.extract(p, "dev-clean", 1)),
    (native, lambda p: native.run(p, "B100", "D0", "U8", "bench")),
    (native, lambda p: native.run(p, "C101", "D1", "U1", "cold", kind="mid")),
    (byt5, lambda p: byt5.run(p, 1)),
    (corpus, lambda p: corpus.run(p, 1)),
    (independent, lambda p: independent.run(p, 1)),
    (archived, lambda p: archived.run(p, "B100", 1)),
    (native_independent, lambda p: native_independent.run(p, 1)),
    (byt5_independent, lambda p: byt5_independent.run(p, 1)),
    (cost_independent, lambda p: cost_independent.run(p, 1)),
    (storage_reforecast, lambda p: storage_reforecast.run(p, 1)),
    (archive_independent, lambda p: archive_independent.run(p, 1)),
    (admission_independent, lambda p: admission_independent.run(p, 1)),
    (calibration_consumption, lambda p: calibration_consumption.run(p, 2)),
    (evaluation_summary, lambda p: evaluation_summary.run(p, 1)),
    (cost, lambda p: cost.run(p, 1))])
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
