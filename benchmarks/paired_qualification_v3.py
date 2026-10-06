"""Bounded paired update/resume/BENCH qualification; never a probe launcher."""
import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
import gc
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import time

from src.data.development_reader import load_targets
from src.data.lexical_corruption_v2 import serialized
from src.data.mixed_reader_v3 import DeficitNode, MixedReader, PHASE_ENDS, native_shape
from src.generation.lexical_v2 import digest
from src.models.tokenizer import ByteBPE


SAFE = Path("experiments/manifests/lexical_reader_v2")
ROOT = Path("exports/lexical-reader-v2")
DRY = SAFE / "mixed-reader-dry-run.attempt02.json"
GENERATED = ROOT / "generated-pool-attempt02/accepted.jsonl"
NATURAL = ROOT / "mixed-reader-attempt02/natural-accepted.jsonl"
LEDGER = ROOT / "mixed-reader-attempt02/presentations.jsonl"
UPDATE_INDEX = SAFE / "mixed-reader-update-index.attempt02.json"


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write(path, value):
    Path(path).write_bytes(serialized(value))


def common():
    dry = json.loads(DRY.read_text())
    if dry["scientific_stop_triggered"]:
        raise ValueError("scientific stop blocks all neural qualification")
    bindings = {GENERATED: "accepted_pool_sha256", NATURAL: "accepted_natural_sha256",
        LEDGER: "ledger_sha256", UPDATE_INDEX: "update_index_sha256"}
    if any(sha(path) != dry[key] for path, key in bindings.items()):
        raise ValueError("qualified common data changed")
    generated = [json.loads(line) for line in GENERATED.read_text().splitlines()]
    natural_rows = [json.loads(line) for line in NATURAL.read_text().splitlines()]
    rows = {row["variant_id"]: row for row in [*generated, *natural_rows]}
    ledger = [json.loads(line) for line in LEDGER.read_text().splitlines()]
    updates = json.loads(UPDATE_INDEX.read_text())
    table = json.loads((SAFE / "lexical-profile-table.attempt01.json").read_text())
    reader = MixedReader(generated, [row for row in natural_rows if row["view"] == "identity"],
        [row for row in natural_rows if row["view"] == "natural"],
        {1: table["severity_P1_P2"]["1"], 2: table["severity_P1_P2"]["2"]})
    identities = {str(path): sha(path) for path in (*bindings, DRY,
        Path("configs/tokenizer_development/tokenizer.json"),
        SAFE / "lexical-profile-table.attempt01.json")}
    return rows, ledger, updates, reader, identities


def frozen_queue(rows, ledger, item):
    queued = [{**presentation, "row": rows[presentation["variant_id"]]}
        for presentation in ledger[item["first_ordinal"]:item["last_ordinal"] + 1]]
    if sum(presentation["canonical_charge"] for presentation in queued) != item["canonical_charge"]:
        raise ValueError("frozen common update charge mismatch")
    return queued


def exact_queue(rows, ledger, item, reader):
    queued = frozen_queue(rows, ledger, item)
    reconstructed = reader.queue()
    if len(reconstructed) != len(queued) or any(
        (a["presentation_id"], a["variant_id"], a["start_exposure"], a["end_exposure"])
        != (b["presentation_id"], b["variant_id"], b["start_exposure"], b["end_exposure"])
        for a, b in zip(reconstructed, queued)):
        raise ValueError("live reader differs from immutable complete queue")
    return queued


def prepare_panel():
    pairs = [json.loads(line) for line in Path(
        "exports/foundation-repair/development-asr-pairs-attempt01/pairs.jsonl").read_text().splitlines()]
    calibration = [row for row in pairs if row["role"] == "calibration"]
    hpo_records = [json.loads(line) for line in Path(
        "exports/foundation-repair/parakeet-frame-repair-attempt01/records.jsonl").read_text().splitlines()]
    hpo_by_id = {}
    for row in hpo_records:
        if row["id"] in hpo_by_id and row["hypothesis"] != hpo_by_id[row["id"]]["hypothesis"]:
            raise ValueError("existing repaired HPO repeat differs")
        hpo_by_id[row["id"]] = row
    official = {row["id"]: row for row in load_targets(
        "experiments/manifests/public_lspc_training_roles.development.jsonl",
        "experiments/manifests/public_lspc_training_supply_qualification.json",
        allowed_roles={"hpo_development", "calibration"})}
    generated = [json.loads(line) for line in Path(
        "experiments/manifests/stress_split_repair_20261005T054436Z/latents.jsonl").read_text().splitlines()]
    if len(calibration) != 96 or len(hpo_by_id) != 12 or len(generated) != 288:
        raise ValueError("approved DEVELOPMENT panel size changed")
    natural = [{"id": row["id"], "role": "calibration_development_consumed", "source_group_id": row["source_group_id"],
        "source": row["source"], "target": row["target"], "source_sha256": row["source_sha256"]} for row in calibration]
    natural.extend({"id": identifier, "role": "hpo_development", "source_group_id": official[identifier]["source_group_id"],
        "source": row["hypothesis"], "target": official[identifier]["target"], "source_sha256": digest(row["hypothesis"])}
        for identifier, row in sorted(hpo_by_id.items()))
    tokenizer = ByteBPE.load("configs/tokenizer_development")
    panel = []
    for row in natural:
        if (row["target"] != official[row["id"]]["target"] or digest(row["source"]) != row["source_sha256"]):
            raise ValueError("existing natural DEVELOPMENT source/target changed")
        shape = native_shape(tokenizer, row["source"], row["target"], row["target"])
        panel.append({**row, "population": "natural", "native_admitted": shape is not None,
            "shape": shape, "target_sha256": digest(row["target"])})
    for row in generated:
        source, target = row["source_utf8"], row["reference_utf8"]
        if digest(source) != row["source_sha256"] or digest(target) != row["reference_sha256"]:
            raise ValueError("existing generated DEV bytes changed")
        panel.append({"id": row["case_id"], "population": "generated", "source": source, "target": target,
            "base_group_id": row["base_group_id"], "view": row["view_kind"], "category": row["primary_category"],
            "source_sha256": digest(source), "target_sha256": digest(target), "native_admitted": True,
            "shape": native_shape(tokenizer, source, target, target)})
        panel[-1]["native_admitted"] = panel[-1]["shape"] is not None
    return panel, [row["id"] for row in calibration]


def prepare():
    destination = ROOT / "pilot-preparation-attempt01"
    destination.mkdir(parents=True, exist_ok=False)
    _, _, updates, _, identities = common()
    panel, consumed = prepare_panel()
    write(destination / "development-panel.json", panel)
    panel_meta = {"scope": "DEVELOPMENT_EVALUATION_ONLY_NOT_FITTING", "natural_calibration": 96, "natural_hpo": 12,
        "generated_dev": 288, "total_cases": len(panel), "native_admitted": sum(row["native_admitted"] for row in panel),
        "native_rejections_frozen": [row["id"] for row in panel if not row["native_admitted"]],
        "decode_positions_cap": 256, "C_edit_cap": 64, "post_decode_exclusions": False,
        "panel_sha256": sha(destination / "development-panel.json"), "model_candidate_outputs_seen": False,
        "calibration_consumed_ids": sorted(consumed), "fit_forbidden": True,
        "panel_sources": {path: sha(path) for path in (
            "exports/foundation-repair/development-asr-pairs-attempt01/pairs.jsonl",
            "exports/foundation-repair/parakeet-frame-repair-attempt01/records.jsonl",
            "experiments/manifests/stress_split_repair_20261005T054436Z/latents.jsonl")}}
    write(SAFE / "development-panel-freeze.attempt01.json", panel_meta)
    prior = json.loads(Path("experiments/manifests/development_calibration_consumption.attempt01.json").read_text())
    union = sorted(set(prior["union_ids"]) | set(consumed))
    write(SAFE / "development-calibration-consumption.attempt02.json", {
        "schema": "development_consumption_overlay_v2", "prior_overlay_sha256": sha(
            "experiments/manifests/development_calibration_consumption.attempt01.json"),
        "prospective_frontier_panel_consumption": sorted(consumed), "union_ids": union, "union_rows": len(union),
        "calibration_role_total": prior["calibration_role_total"],
        "remaining_untouched_calibration_role_rows": prior["calibration_role_total"] - len(union),
        "fit_forbidden": True, "reason": "all96 frozen CALIBRATION pairs bound to DEVELOPMENT evaluation",
        "new_candidate_inference_started": False})
    def endpoint(nominal):
        if nominal == 0:
            return {"nominal": 0, "update": 0, "canonical_exposure": 0, "last_ordinal": -1}
        item = next(item for item in updates if item["end_exposure"] >= nominal)
        return {"nominal": nominal, "update": item["update"] + 1,
            "canonical_exposure": item["end_exposure"], "last_ordinal": item["last_ordinal"]}
    saves = sorted({0, *range(1_000_000, 10_000_001, 1_000_000), *PHASE_ENDS})
    evaluation = (0, 1_000_000, 3_000_000, *PHASE_ENDS)
    shared = {"seed": 42, "nominal_exposure": 10_000_000, "actual_stop_endpoint": endpoint(10_000_000),
        "phase_absolute_ends": PHASE_ENDS, "phase_nominal_exposures": (6_666_667, 2_666_667, 666_666),
        "phase_assignment": "starting cumulative presentation exposure; whole presentation; no update flush",
        "update_target": 32768, "LR_clock": {"warmup": 200000, "decay": "continuous cosine", "floor_fraction": .1,
            "clock": "completed update canonical endpoint clamped at10M", "phase_resets": False},
        "save_endpoints": [endpoint(nominal) for nominal in saves],
        "evaluation_endpoints": [endpoint(nominal) for nominal in evaluation],
        "data_identities": identities, "development_panel_sha256": panel_meta["panel_sha256"],
        "working_dtype": "bfloat16", "master_moments_accumulation": "float32", "clip_update_clear": "once per complete queue",
        "checkpoint_policy": "routine complete optimizer boundaries; interruption after completed microbatch",
        "recipe_status": "CONFIGURED_UNSTARTED_UNAUTHORIZED", "probe_slot_consumed": False}
    recipes = []
    for arm in ("B100", "C101"):
        for peak in (1e-4, 3e-4, 6e-4):
            config = {**shared, "arm": arm, "peak_lr": peak}
            path = SAFE / f"pilot-{arm}-seed42-lr{peak:.0e}.json"
            write(path, config)
            recipes.append({"arm": arm, "peak_lr": peak, "config_path": str(path), "config_sha256": sha(path)})
    write(SAFE / "pilot-preparation.attempt01.json", {"recipes": recipes, "shared_actual_endpoint": shared["actual_stop_endpoint"],
        "panel": panel_meta, "six_probe_slots_consumed": 0, "final_training_started": False, "paper_protocol_v2_frozen": False})
    print(json.dumps({"recipes_configured": 6, "recipes_started": 0, "development_panel_cases": len(panel),
        "native_panel_admitted": panel_meta["native_admitted"], "stop_endpoint": shared["actual_stop_endpoint"]}), flush=True)


def runtime_identities(data):
    if os.environ.get("MLX_ENABLE_TF32") != "0":
        raise ValueError("explicit MLX_ENABLE_TF32=0 required")
    paths = ("src/models/paired_training_v3.py", "src/models/bc.py", "src/models/core.py", "src/models/training.py",
        "src/models/edits.py", "src/models/tokenizer.py", "src/data/mixed_reader_v3.py", "benchmarks/paired_qualification_v3.py")
    return {"data": data, "code": {path: sha(path) for path in paths},
        "runtime": {"python": platform.python_version(), "mlx": importlib.metadata.version("mlx"),
            "numpy": importlib.metadata.version("numpy"), "platform": platform.platform(), "TF32": "0"}}


def create_trainer(arm, identities):
    import mlx.core as mx
    from src.models.bc import B100, C101
    from src.models.core import parameter_inventory
    from src.models.paired_training_v3 import PairedTrainer
    model = B100(seed=42) if arm == "B100" else C101(seed=42)
    count = sum(item["count"] for item in parameter_inventory(model))
    if count != (100686336 if arm == "B100" else 101081859):
        raise ValueError("fixed model geometry changed")
    trainer = PairedTrainer(model, arm, identities, microbatch_size=16 if arm == "B100" else 4)
    mx.eval(model.parameters(), trainer.optimizer.m, trainer.optimizer.v, trainer.accumulator.values)
    return trainer


def preflight(destination, arm, mode, identities):
    destination.mkdir(parents=True, exist_ok=False)
    value = {"scope": mode, "arm": arm, "head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "identities": identities, "no_concurrent_accelerator": True, "six_probe_slots_consumed": 0,
        "final_training_started": False, "paper_protocol_v2_frozen": False}
    write(destination / "preflight.json", value)
    return value


def resume_control(arm):
    import mlx.core as mx
    from src.models.paired_training_v3 import save_paired_checkpoint
    rows, ledger, updates, reader, data_ids = common()
    identities = runtime_identities(data_ids)
    out = ROOT / f"resume-{arm}-control-attempt01"
    preflight(out, arm, "EXACT_32768_UPDATE_RESUME_CONTROL_NOT_PROBE", identities)
    trainer = create_trainer(arm, identities)
    q0 = exact_queue(rows, ledger, updates[0], reader)
    begin = time.perf_counter()
    result = trainer.update(q0, reader.state())
    write(out / "first-complete-update.json", {**result, "wall_seconds": time.perf_counter() - begin})
    print(json.dumps({"arm": arm, "first_complete_update_seconds": time.perf_counter() - begin,
        "canonical_charge": result["canonical_charge"], "microsteps": result["microsteps"], "finite_loss": result["loss"]}), flush=True)
    probe = q0[0]["row"]
    begin = time.perf_counter()
    save_paired_checkpoint(trainer, out / "boundary", probe)
    boundary_seconds = time.perf_counter() - begin
    queued = exact_queue(rows, ledger, updates[1], reader)
    trainer.begin(queued, reader.state())
    trainer.microstep()
    begin = time.perf_counter()
    save_paired_checkpoint(trainer, out / "mid", probe)
    mid_seconds = time.perf_counter() - begin
    controls = []
    for index in range(1, 22):
        begin = time.perf_counter()
        if index == 1:
            while trainer.completed_microbatches < len(trainer.partition):
                trainer.microstep()
            result = trainer.finish()
        else:
            queued = exact_queue(rows, ledger, updates[index], reader)
            result = trainer.update(queued, reader.state())
        record = {**result, "state_sha256": trainer.state_hash(), "reader_state_sha256": digest(
            json.dumps(reader.state(), sort_keys=True)), "wall_seconds": time.perf_counter() - begin}
        controls.append(record)
        with (out / "controls.jsonl").open("a") as stream:
            stream.write(json.dumps(record, sort_keys=True) + "\n")
        print(json.dumps({"arm": arm, "control_update": index + 1, "seconds": record["wall_seconds"],
            "exposure": trainer.committed_exposure}), flush=True)
    write(out / "control-complete.json", {"status": "CONTROL_COMPLETE_COLD_REPLAY_PENDING", "arm": arm,
        "control_updates_after_initial": len(controls), "boundary_save_seconds": boundary_seconds,
        "mid_save_seconds": mid_seconds, "controls_sha256": sha(out / "controls.jsonl"),
        "first_complete_update_sha256": sha(out / "first-complete-update.json"), "probe_slots": 0})


def resume_replay(arm, kind):
    from src.models.paired_training_v3 import load_paired_checkpoint
    rows, ledger, updates, reader, data_ids = common()
    identities = runtime_identities(data_ids)
    control = ROOT / f"resume-{arm}-control-attempt01"
    expected = [json.loads(line) for line in (control / "controls.jsonl").read_text().splitlines()]
    if len(expected) != 21 or not (control / "control-complete.json").exists():
        raise ValueError("complete uninterrupted reference missing")
    out = ROOT / f"resume-{arm}-{kind}-cold-attempt01"
    preflight(out, arm, "COLD_BOUNDARY_OR_MID_REPLAY_NOT_PROBE", identities)
    trainer = create_trainer(arm, identities)
    begin = time.perf_counter()
    load_paired_checkpoint(trainer, control / kind, rows)
    reader.restore(trainer.reader_state)
    load_seconds = time.perf_counter() - begin
    matches = []
    for index, target in enumerate(expected, 1):
        begin = time.perf_counter()
        if kind == "mid" and index == 1:
            while trainer.completed_microbatches < len(trainer.partition):
                trainer.microstep()
            result = trainer.finish()
        else:
            result = trainer.update(exact_queue(rows, ledger, updates[index], reader), reader.state())
        actual_hash = trainer.state_hash()
        reader_hash = digest(json.dumps(reader.state(), sort_keys=True))
        keys = ("presentation_ids", "denominators", "committed_canonical_exposure", "canonical_charge", "lr", "loss")
        if actual_hash != target["state_sha256"] or reader_hash != target["reader_state_sha256"] or any(result[key] != target[key] for key in keys):
            raise ValueError(f"cold resume differs from uninterrupted control at update {index + 1}")
        record = {"update": index + 1, "state_sha256": actual_hash, "reader_state_sha256": reader_hash,
            "canonical_charge": result["canonical_charge"], "committed_canonical_exposure": result["committed_canonical_exposure"],
            "presentation_ids": result["presentation_ids"], "status": "EXACT_MATCH", "wall_seconds": time.perf_counter() - begin}
        matches.append(record)
        with (out / "matches.jsonl").open("a") as stream:
            stream.write(json.dumps(record, sort_keys=True) + "\n")
        print(json.dumps({"arm": arm, "kind": kind, "exact_match_update": index + 1,
            "seconds": record["wall_seconds"]}), flush=True)
    write(out / "summary.json", {"status": "PASS_EXACT_COLD_RESUME", "arm": arm, "kind": kind,
        "matched_complete_updates": len(matches), "pending_completion_plus_next_twenty": kind == "mid",
        "boundary_next_twenty_plus_one": kind == "boundary", "load_seconds": load_seconds,
        "matches_sha256": sha(out / "matches.jsonl"), "controls_sha256": sha(control / "controls.jsonl"),
        "checkpoint_manifest_sha256": sha(control / kind / "COMPLETE.json"), "probe_slots": 0})


class BenchStream:
    """Exposure-balanced draws of unchanged frozen queues from all pilot phases."""
    def __init__(self, updates):
        self.updates = updates
        self.pools = defaultdict(list)
        for index, update in enumerate(updates):
            dominant = max(("P0", "P1", "P2"), key=lambda phase: update["phase_segments"].get(phase, 0))
            self.pools[dominant].append(index)
        if any(not self.pools[phase] for phase in ("P0", "P1", "P2")):
            raise ValueError("BENCH pilot phase population missing")
        self.cursor, self.charges, self.total = Counter(), Counter(), 0
        self.weights = {"P0": 6_666_667, "P1": 2_666_667, "P2": 666_666}

    def next(self):
        phase = max(("P0", "P1", "P2"), key=lambda phase: (
            self.weights[phase] * self.total - 10_000_000 * self.charges[phase],
            -("P0", "P1", "P2").index(phase)))
        index = self.pools[phase][self.cursor[phase] % len(self.pools[phase])]
        self.cursor[phase] += 1
        item = self.updates[index]
        self.total += item["canonical_charge"]
        self.charges.update(item["phase_segments"])
        return index, item


def system_snapshot():
    commands = {"virtual_memory": ("vm_stat",), "swap": ("sysctl", "vm.swapusage"),
        "thermal": ("pmset", "-g", "therm"), "power_source": ("pmset", "-g", "batt"),
        "memory_pressure": ("memory_pressure", "-Q")}
    result = {"monotonic": time.perf_counter(), "rss_peak_bytes_macos": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    for key, command in commands.items():
        try:
            done = subprocess.run(command, text=True, capture_output=True, timeout=10)
            result[key] = {"exit_code": done.returncode, "stdout": done.stdout, "stderr": done.stderr}
        except (OSError, subprocess.TimeoutExpired) as error:
            result[key] = {"status": "UNAVAILABLE", "reason": str(error)}
    return result


def evaluation_timing(trainer, panel, out, label):
    import mlx.core as mx
    from src.scoring.records import Output, prepare_source, score_output
    from src.scoring.triple import serialize
    tokenizer = ByteBPE.load("configs/tokenizer_development")
    total_decode, total_score, records = 0., 0., []
    begin_panel = time.perf_counter()
    with (out / f"evaluation-{label}.jsonl").open("w") as stream:
        for index, row in enumerate(panel):
            if not row["native_admitted"]:
                raise ValueError("frozen panel native rejection needs explicit retained failure handling")
            shape = row["shape"]
            source = mx.array([shape["source_ids"]])
            valid = source != 256
            mx.synchronize()
            begin = time.perf_counter()
            if trainer.arm == "B100":
                answer = trainer.model.greedy_text(source, source_valid=valid, max_tokens=256,
                    dtype=mx.bfloat16, backend="native")
                status = answer["status"]
                try:
                    output = tokenizer.decode(answer["token_ids"])
                except (ValueError, UnicodeError):
                    output, status = None, "invalid_byte_decoding"
                positions = len(answer["token_ids"]) + (answer["status"] == "completed")
                raw = answer
            else:
                answer = trainer.model.greedy_edits(row["source"], source, tuple(shape["encoder_positions"]),
                    tuple(shape["byte_offsets"]), mx.array(shape["legal"], dtype=mx.bool_),
                    lambda token: tokenizer.byte_map[token], source_valid=valid, max_edits=64,
                    max_decoder_positions=256, dtype=mx.bfloat16, backend="native")
                output, status, positions = answer["output"], answer["status"], answer["decoder_positions"]
                raw = {**answer, "program": None if answer["program"] is None else asdict(answer["program"])}
            mx.synchronize()
            decode_seconds = time.perf_counter() - begin
            begin = time.perf_counter()
            prepared = prepare_source(row["target"], row["source"])
            scorer_status = {"completed": "complete", "invalid_byte_decoding": "invalid_utf8",
                "abstained": "abstain", "invalid_or_capped": "invalid_c", "capped": "capped"}[status]
            scored = score_output(prepared, Output(output, scorer_status))
            score_seconds = time.perf_counter() - begin
            total_decode += decode_seconds
            total_score += score_seconds
            record = {"id": row["id"], "population": row["population"], "arm": trainer.arm,
                "checkpoint_label": label, "source_sha256": row["source_sha256"], "target_sha256": row["target_sha256"],
                "status": status, "output": output, "raw_decoder": raw, "decoder_positions": positions,
                "decode_seconds": decode_seconds, "scorer_seconds": score_seconds, "score": scored}
            stream.write(serialize(record) + "\n")
            records.append({key: record[key] for key in ("id", "population", "status", "decode_seconds", "scorer_seconds", "decoder_positions")})
            if (index + 1) % 48 == 0:
                print(json.dumps({"arm": trainer.arm, "evaluation_checkpoint": label, "cases_completed": index + 1,
                    "elapsed_seconds": time.perf_counter() - begin_panel}), flush=True)
    summary = {"checkpoint_label": label, "cases": len(records), "decode_seconds": total_decode,
        "scorer_seconds": total_score, "complete_panel_wall_seconds": time.perf_counter() - begin_panel,
        "status_counts": dict(Counter(row["status"] for row in records)), "per_case": records,
        "records_sha256": sha(out / f"evaluation-{label}.jsonl"),
        "scope": "DEVELOPMENT_RUNTIME_PRICING_NOT_LR_SELECTION_OR_MODEL_QUALITY_ADMISSION"}
    write(out / f"evaluation-{label}-summary.json", summary)
    return summary


def bench(arm):
    import mlx.core as mx
    import numpy as np
    from src.models.paired_training_v3 import save_paired_checkpoint
    for kind in ("boundary", "mid"):
        summary = json.loads((ROOT / f"resume-{arm}-{kind}-cold-attempt01/summary.json").read_text())
        if summary["status"] != "PASS_EXACT_COLD_RESUME" or summary["matched_complete_updates"] != 21:
            raise ValueError("exact-model cold resume gate blocks BENCH")
    begin_startup = time.perf_counter()
    rows, ledger, updates, _, data_ids = common()
    identities = runtime_identities(data_ids)
    out = ROOT / f"bench-{arm}-attempt01"
    preflight(out, arm, "BENCH_00_EXACT_MODEL_APPROVED_READER_NONZERO_PILOT_CLOCK_NOT_PROBE", identities)
    trainer = create_trainer(arm, identities)
    startup_seconds = time.perf_counter() - begin_startup
    panel_meta = json.loads((SAFE / "development-panel-freeze.attempt01.json").read_text())
    panel_path = ROOT / "pilot-preparation-attempt01/development-panel.json"
    if sha(panel_path) != panel_meta["panel_sha256"]:
        raise ValueError("frozen DEVELOPMENT panel changed")
    panel = json.loads(panel_path.read_text())
    selector = BenchStream(updates)
    probe = rows[ledger[0]["variant_id"]]
    write(out / "bench-config.json", {"warmup_complete_updates": 5, "timed_complete_updates": 100,
        "separate_sustained_minimum_seconds": 1200, "peak_lr": 3e-4, "clock": trainer.clock,
        "microbatch_size": trainer.microbatch_size, "optimizer": trainer.optimizer.policy(),
        "parameter_count": sum(value.size for value in trainer.optimizer.m.values()),
        "geometry": asdict(trainer.model.config), "startup_seconds": startup_seconds,
        "stream": "largest canonical-exposure phase deficit; complete frozen queue draws in each phase; persistent queue cursors",
        "phase_weights": selector.weights, "LR_scope": "actual BENCH consumed canonical exposure; no phase or segment LR resets",
        "future_probe_ledger_unchanged": True, "new_six_probe_slots": 0, "discard_bench_weights_for_probes": True})
    save_start = time.perf_counter()
    save_paired_checkpoint(trainer, out / "initial", probe)
    initial_save_seconds = time.perf_counter() - save_start
    initial_evaluation = evaluation_timing(trainer, panel, out, "initial")
    mx.reset_peak_memory()
    snapshots = [system_snapshot()]
    all_updates, segment_phase_charges = [], defaultdict(Counter)
    last_snapshot = time.perf_counter()
    def one_update(segment):
        nonlocal last_snapshot
        begin = time.perf_counter()
        common_index, item = selector.next()
        queued = frozen_queue(rows, ledger, item)
        result = trainer.update(queued, {"immutable_benchmark_queue_selector": {
            "queue_cursors": dict(selector.cursor), "phase_charges": dict(selector.charges), "next_benchmark_step": len(all_updates) + 1},
            "source_ledger_sha256": data_ids[str(LEDGER)], "common_update_index": common_index})
        wall = time.perf_counter() - begin
        result.update(segment=segment, benchmark_step=len(all_updates), common_update_index=common_index,
            phase_segments=item["phase_segments"], wall_seconds=wall, peak_mlx_allocation_bytes=mx.get_peak_memory(),
            active_mlx_allocation_bytes=mx.get_active_memory(), peak_process_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        with (out / "updates.jsonl").open("a") as stream:
            stream.write(json.dumps(result, sort_keys=True) + "\n")
        compact = {key: value for key, value in result.items() if key not in ("actual_consumption", "presentation_ids")}
        all_updates.append(compact)
        segment_phase_charges[segment].update(item["phase_segments"])
        if time.perf_counter() - last_snapshot >= 60:
            snapshots.append(system_snapshot())
            write(out / "system-snapshots.json", snapshots)
            last_snapshot = time.perf_counter()
        print(json.dumps({"arm": arm, "segment": segment, "step": result["benchmark_step"],
            "seconds": wall, "canonical_charge": result["canonical_charge"], "microsteps": result["microsteps"],
            "committed_bench_exposure": result["committed_canonical_exposure"]}), flush=True)
        return compact
    warmups = [one_update("warmup") for _ in range(5)]
    timed_start = time.perf_counter()
    timed = [one_update("timed") for _ in range(100)]
    timed_wall = time.perf_counter() - timed_start
    sustained_start, sustained = time.perf_counter(), []
    while time.perf_counter() - sustained_start < 1200:
        sustained.append(one_update("sustained"))
    sustained_wall = time.perf_counter() - sustained_start
    snapshots.append(system_snapshot())
    write(out / "system-snapshots.json", snapshots)
    def metrics(items, wall):
        durations = [item["wall_seconds"] for item in items]
        canonical = sum(item["canonical_charge"] for item in items)
        native = sum(item["source_positions"] + item["decoder_event_positions"] for item in items)
        return {"complete_updates": len(items), "wall_seconds": wall,
            "mean_update_seconds": float(np.mean(durations)), "median_update_seconds": float(np.median(durations)),
            "p95_update_seconds": float(np.quantile(durations, .95)), "canonical_charge": canonical,
            "canonical_anchors_per_second": canonical / wall, "native_positions_per_second": native / wall,
            "examples_per_second": sum(item["examples"] for item in items) / wall,
            "reader_seconds": sum(item["reader_seconds"] for item in items),
            "forward_backward_seconds": sum(item["forward_backward_seconds"] for item in items),
            "synchronization_seconds": sum(item["synchronization_seconds"] for item in items),
            "optimizer_seconds": sum(item["optimizer_seconds"] for item in items),
            "accumulation_seconds": sum(item["accumulation_seconds"] for item in items),
            "source_positions": sum(item["source_positions"] for item in items),
            "decoder_event_positions": sum(item["decoder_event_positions"] for item in items),
            "source_padding": sum(item["source_padding"] for item in items),
            "decoder_padding": sum(item["decoder_padding"] for item in items)}
    timed_metrics, sustained_metrics = metrics(timed, timed_wall), metrics(sustained, sustained_wall)
    chunk = max(1, len(sustained) // 4)
    first, last = sustained[:chunk], sustained[-chunk:]
    first_rate = sum(item["canonical_charge"] for item in first) / sum(item["wall_seconds"] for item in first)
    last_rate = sum(item["canonical_charge"] for item in last) / sum(item["wall_seconds"] for item in last)
    conservative = min(sustained_metrics["canonical_anchors_per_second"], last_rate)
    begin = time.perf_counter()
    save_paired_checkpoint(trainer, out / "final", probe)
    final_save_seconds = time.perf_counter() - begin
    final_evaluation = evaluation_timing(trainer, panel, out, "final")
    summary = {"status": "BENCH_00_COMPLETE_FAIRNESS_REVIEW_PENDING", "arm": arm,
        "warmups": len(warmups), "timed": timed_metrics, "sustained": sustained_metrics,
        "phase_charges_by_segment": {key: dict(value) for key, value in segment_phase_charges.items()},
        "first_sustained_quartile_anchors_per_second": first_rate, "last_sustained_quartile_anchors_per_second": last_rate,
        "throughput_drift_ratio": last_rate / first_rate, "conservative_sustained_anchors_per_second": conservative,
        "peak_mlx_allocation_bytes": max(item["peak_mlx_allocation_bytes"] for item in all_updates),
        "peak_process_rss_bytes_macos": max(item["peak_process_rss_bytes_macos"] for item in all_updates),
        "system_snapshot_sha256": sha(out / "system-snapshots.json"),
        "startup_seconds": startup_seconds, "initial_save_seconds": initial_save_seconds, "final_save_seconds": final_save_seconds,
        "initial_evaluation": initial_evaluation, "final_evaluation": final_evaluation,
        "complete_bench_updates": len(all_updates), "bench_consumed_canonical_exposure": trainer.committed_exposure,
        "updates_sha256": sha(out / "updates.jsonl"), "no_failures": True, "probe_slots": 0,
        "scope": "performance/update qualification only; no probe LR selection or viability inference"}
    write(out / "summary.json", summary)
    write(SAFE / f"bench-{arm}.attempt01.json", {key: value for key, value in summary.items()
        if key not in ("initial_evaluation", "final_evaluation")})
    print(json.dumps({"arm": arm, "status": summary["status"], "timed_updates": 100,
        "sustained_seconds": sustained_wall, "conservative_anchors_per_second": conservative}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "resume-control", "resume-cold", "bench"))
    parser.add_argument("--arm", choices=("B100", "C101"))
    parser.add_argument("--kind", choices=("boundary", "mid"))
    args = parser.parse_args()
    if args.mode == "prepare":
        prepare()
    elif args.mode == "resume-control" and args.arm:
        resume_control(args.arm)
    elif args.mode == "resume-cold" and args.arm and args.kind:
        resume_replay(args.arm, args.kind)
    elif args.mode == "bench" and args.arm:
        bench(args.arm)
    else:
        parser.error("arm and cold-resume kind required")


if __name__ == "__main__":
    main()
