"""Operational checkpoint storage and immutable campaign endpoint guards."""
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from benchmarks.six_10m_campaign import sparse_exact, write
import benchmarks.six_10m_campaign as campaign


def test_sparse_checkpoint_keeps_binary_bytes_and_trailing_zeros(tmp_path):
    payload = bytes(range(256)) * 256 + bytes(65536 * 3) + b"npz-footer" + bytes(777)
    path = tmp_path / "arrays.npz"
    path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    result = sparse_exact(path, digest)
    assert path.read_bytes() == payload
    assert result["sha256"] == digest
    assert result["logical_bytes"] == len(payload)


def test_sparse_bad_hash_preserves_original_and_failed_copy(tmp_path):
    path = tmp_path / "arrays.npz"
    path.write_bytes(b"checkpoint" + bytes(65536))
    original = path.read_bytes()
    with pytest.raises(ValueError, match="logical bytes"):
        sparse_exact(path, "0" * 64)
    assert path.read_bytes() == original
    assert path.with_name("arrays.npz.sparse-partial").read_bytes() == original


def test_receipts_cannot_replace_prior_evidence(tmp_path):
    path = tmp_path / "receipt.json"
    write(path, {"status": "FAILED"})
    with pytest.raises(FileExistsError):
        write(path, {"status": "PASS"})
    assert json.loads(path.read_text()) == {"status": "FAILED"}


def test_six_frozen_recipes_share_whole_endpoints():
    configs = [json.loads(path.read_text()) for path in Path(
        "experiments/manifests/lexical_reader_v2").glob("pilot-*-seed42-lr*.json")]
    assert len(configs) == 6
    assert {(c["arm"], c["peak_lr"]) for c in configs} == {
        (arm, peak) for arm in ("B100", "C101") for peak in (1e-4, 3e-4, 6e-4)}
    assert {json.dumps(c["save_endpoints"], sort_keys=True) for c in configs} == {
        json.dumps(configs[0]["save_endpoints"], sort_keys=True)}
    assert {json.dumps(c["evaluation_endpoints"], sort_keys=True) for c in configs} == {
        json.dumps(configs[0]["evaluation_endpoints"], sort_keys=True)}
    assert len(configs[0]["save_endpoints"]) == 13
    assert [p["update"] for p in configs[0]["evaluation_endpoints"]] == [0,31,92,204,285,305]


def test_capped_scorer_correspondence_is_retained_with_unavailable_preservation(tmp_path):
    outputs = Path("exports/lexical-reader-v2/bench-C101-attempt03/evaluation-final.jsonl")
    if not outputs.exists():
        pytest.skip("private qualification outputs unavailable")
    panel=json.loads(campaign.PANEL.read_text())
    records=[json.loads(line) for line in outputs.read_text().splitlines()]
    natural=next(r for r in records if r["population"]=="natural")
    natural["score"]["fixed_correct_damage"]=None
    natural["score"]["fallback_reason"]="synthetic joint-state cap fixture"
    mutated=tmp_path/"capped-fixture.jsonl"
    mutated.write_text("".join(json.dumps(r)+"\n" for r in records))
    metrics=campaign.summarize_evaluation(mutated,panel,0,{},"CAP_FIXTURE_NOT_A_RECIPE")
    assert metrics["natural"]["source_correct_preserved_bounds"] is None
    assert metrics["natural"]["source_correct_preservation_coverage"]["unavailable_cases"]==1
    assert metrics["natural"]["scorer_caps"]>=1
    assert metrics["generated"]["cases"]==288
    assert metrics["natural"]["reference_words"]==sum(r["score"]["reference_words"] for r in records if r["population"]=="natural")


@pytest.mark.parametrize("failure_site", ["final_evaluation", "phase_update"])
def test_numerical_replay_keeps_final_checkpoint_and_uses_fresh_reader(tmp_path, monkeypatch, failure_site):
    """Reproduce two real operational hazards without any neural training."""
    import numpy as np
    import src.models.paired_training_v3 as native
    monkeypatch.chdir(tmp_path)
    safe = tmp_path / "safe"
    private = tmp_path / "private"
    safe.mkdir()
    private.mkdir()
    panel = tmp_path / "panel.json"
    panel.write_text("[]")
    latents = tmp_path / "latents.jsonl"
    latents.write_text("")
    config_path = tmp_path / "recipe.json"
    config_path.write_text("{}")
    points = [{"nominal": i*32768, "update": i, "canonical_exposure":i*32768,"last_ordinal":i-1} for i in range(3)]
    config = {"arm":"B100","peak_lr":1e-4,"save_endpoints":points,"evaluation_endpoints":[points[0],points[-1]],"actual_stop_endpoint":points[-1]}
    recipe_id = "B100-seed42-lr1e-04"
    freeze = safe / "freeze.json"
    freeze.write_text(json.dumps({"recipes":[{"recipe_id":recipe_id,"config":config,"config_path":str(config_path),"config_sha256":campaign.sha(config_path)}],"source_hashes":{},"data_identities":{},"evaluation_panel_sha256":campaign.sha(panel),"generated_evaluation_latents_sha256":campaign.sha(latents),"execution_order":[recipe_id],"runtime_identities":{"runtime":{}},"models":{"B100":{"initial_parameter_sha256":"initial"}},"hardware":{}}))
    for name,value in (("SAFE",safe),("PRIVATE",private),("FREEZE",freeze),("PANEL",panel),("LATENTS",latents)):
        monkeypatch.setattr(campaign,name,value)
    monkeypatch.setattr(campaign.subprocess,"check_output",lambda args,**kw: "" if "--porcelain" in args else "head")
    monkeypatch.setattr(campaign.signal,"signal",lambda *args:None)
    readers = []
    failed = []
    class Reader:
        def __init__(self): self.exposure=0; self.phase=None
        def state(self): return {"phase":self.phase,"exposure":self.exposure}
        def restore(self,state):
            assert self.phase is None, "cold restoration must have a fresh reader"
            self.phase=state["phase"]; self.exposure=state["exposure"]
    def common():
        reader=Reader(); readers.append(reader)
        return {"v":{}},[{"variant_id":"v"}],[{"end_exposure":32768},{"end_exposure":65536}],reader,{}
    monkeypatch.setattr(campaign,"common",common)
    monkeypatch.setattr(campaign,"runtime_identities",lambda _: {"runtime":{}})
    def queue(rows,ledger,item,reader):
        reader.phase="P1" if item["end_exposure"]==65536 else "P0"
        reader.exposure=item["end_exposure"]
        return [{"presentation_id":"p"}]
    monkeypatch.setattr(campaign,"exact_queue",queue)
    class Trainer:
        def __init__(self):
            self.optimizer=SimpleNamespace(step=0,policy=lambda:{})
            self.committed_exposure=0; self.queue=[]; self.pending_charge=0; self.completed_microbatches=0
            self.partition=[]; self.denominators=None; self.loss=0.; self.consumption=[]; self.clock={}
        def arrays(self): return {"model::x":np.zeros(1,dtype=np.float32)}
        def update(self,queue,state):
            self.reader_state=state
            if failure_site=="phase_update" and state["phase"]=="P1" and not failed:
                failed.append(True); raise FloatingPointError("injected numerical failure")
            self.optimizer.step+=1; self.committed_exposure=state["exposure"]
            return {"loss":1.,"committed_canonical_exposure":self.committed_exposure,"update":self.optimizer.step}
    monkeypatch.setattr(campaign,"trainer_for",lambda *args:Trainer())
    monkeypatch.setattr(campaign,"tensor_hash",lambda *args:"initial")
    def save(trainer,path,row):
        path.mkdir(); (path/"arrays.npz").write_bytes(b"checkpoint")
        (path/"COMPLETE.json").write_text(json.dumps({"step":trainer.optimizer.step,"exposure":trainer.committed_exposure,"reader":trainer.reader_state}))
        return {"arrays.npz":campaign.sha(path/"arrays.npz")}
    def load(trainer,path,rows):
        meta=json.loads((path/"COMPLETE.json").read_text())
        trainer.optimizer.step=meta["step"]; trainer.committed_exposure=meta["exposure"]
        return {"reader_state":meta["reader"]}
    monkeypatch.setattr(native,"save_paired_checkpoint",save)
    monkeypatch.setattr(native,"load_paired_checkpoint",load)
    def evaluate(trainer,panel,out,label):
        if failure_site=="final_evaluation" and label=="update002" and not failed:
            failed.append(True); raise FloatingPointError("injected evaluation failure")
        (out/f"evaluation-{label}.jsonl").write_text("")
    monkeypatch.setattr(campaign,"evaluation_timing",evaluate)
    monkeypatch.setattr(campaign,"summarize_evaluation",lambda *args:{"natural":{"wer":1.,"completed_repair":[0,0]},"generated":{"whole_case_conformance":0}})
    monkeypatch.setattr(campaign,"system_snapshot",lambda:{})
    campaign.run(recipe_id)
    receipt=json.loads((safe/f"recipe-{recipe_id}.attempt02.json").read_text())
    assert receipt["status"]=="COMPLETED"
    assert receipt["numerical_replays"]==1
    assert receipt["endpoint"]["update"]==2
    assert receipt["final_checkpoint_complete_sha256"]
    assert len(readers)==3
    assert (safe/f"failure-{recipe_id}.attempt01.json").exists()
