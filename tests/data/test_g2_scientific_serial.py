from types import SimpleNamespace

import pytest

from benchmarks import g2_scientific_serial as serial


def test_serial_campaign_never_launches_a_successor_after_defect(monkeypatch, tmp_path):
    launches = []
    outcomes = {}
    monkeypatch.setattr(serial, "ArtifactRoot", lambda _: SimpleNamespace(preflight=lambda: {}, path=lambda name: tmp_path / name.split("/")[-1]))
    monkeypatch.setattr(serial, "execution_outcomes", lambda name: outcomes.get(name, []))
    monkeypatch.setattr(serial.signal, "signal", lambda *args: None)
    def child(args, **kwargs):
        name = args[args.index("--recipe") + 1]; launches.append(name)
        outcomes[name] = [{"attempt": 1, "status": "STOPPED_DEFECT"}]
        return SimpleNamespace(poll=lambda: 1, returncode=1)
    monkeypatch.setattr(serial.subprocess, "Popen", child)
    with pytest.raises(RuntimeError): serial.run("synthetic-binding")
    assert launches == [serial.ORDER[0]]


def test_serial_numerical_replay_uses_exact_checkpoint_before_successor(monkeypatch, tmp_path):
    launches = []; outcomes = {}
    monkeypatch.setattr(serial, "ArtifactRoot", lambda _: SimpleNamespace(preflight=lambda: {}, path=lambda name: tmp_path / name.split("/")[-1]))
    monkeypatch.setattr(serial, "execution_outcomes", lambda name: outcomes.get(name, []))
    monkeypatch.setattr(serial.signal, "signal", lambda *args: None)
    def child(args, **kwargs):
        name = args[args.index("--recipe") + 1]; attempt = int(args[args.index("--attempt") + 1]); launches.append((name, attempt, args))
        status = "NUMERICAL_FAILURE" if name == serial.ORDER[0] and attempt == 1 else "FAILED_NUMERICAL" if name == serial.ORDER[0] else "COMPLETED"
        outcomes.setdefault(name, []).append({"attempt": attempt, "status": status, "latest_verified_checkpoint": "exact-state"})
        return SimpleNamespace(poll=lambda: 0 if status == "COMPLETED" else 1, returncode=0 if status == "COMPLETED" else 1)
    monkeypatch.setattr(serial.subprocess, "Popen", child)
    serial.run("synthetic-binding")
    assert [(name, attempt) for name, attempt, _ in launches] == [(serial.ORDER[0], 1), (serial.ORDER[0], 2), *[(name, 1) for name in serial.ORDER[1:]]]
    replay = launches[1][2]
    assert replay[replay.index("--resume") + 1] == "exact-state"
