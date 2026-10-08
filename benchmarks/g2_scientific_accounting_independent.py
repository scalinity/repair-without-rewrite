"""Independent CPU ledger and failure-inclusive measured resource accounting."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import time

from src.data.g2_artifacts import ArtifactRoot, read_complete, sha256

BASE = Path("experiments/manifests/generation_2")


def require(condition, message):
    if not condition: raise ValueError(message)


def stable_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def incorporate(unique, step, identity):
    """Repeated replay work is charged physically but never added to recipe extent."""
    if step in unique: require(unique[step] == identity, "replayed completed-update identity differs")
    else: unique[step] = identity


def native_update(row, expected, ledger, arm):
    require(row["update"] == expected["optimizer_step_index"], "optimizer sequence differs")
    for observed, qualified in (("canonical_charge", "canonical_charge"), ("examples", "examples"),
        ("committed_canonical_exposure", "completed_actual_exposure"), ("master_queue_index", "master_index"),
        ("subqueue_index", "subqueue_index"), ("lr", "lr")):
        require(row[observed] == expected[qualified], "qualified optimizer geometry differs: "+observed)
    require(row["denominators"] == expected["denominators"], "qualified update denominator differs")
    require(row["presentation_ids"] == [item["presentation_id"] for item in ledger], "presentation sequence differs")
    require(len(row["actual_consumption"]) == len(ledger), "native receipt cardinality differs")
    consumed = []
    for actual, planned in zip(row["actual_consumption"], ledger):
        for key in ("presentation_id", "variant_id", "source_sha256", "target_sha256", "anchor_sha256", "canonical_charge", "phase", "channel"):
            require(actual[key] == planned[key], "native presentation identity differs: "+key)
        require(actual["cumulative_canonical_exposure"] == planned["end_exposure"], "canonical clock includes a different presentation")
        consumed.append({key: actual[key] for key in ("presentation_id", "variant_id", "source_sha256", "target_sha256", "canonical_charge", "phase", "channel")})
    return stable_hash({"update": row["update"], "loss": row["loss"], "gradient_norm": row["gradient_norm"], "denominators": row["denominators"], "consumed": consumed})


def byt5_update(row, ordering):
    step = row["update"]; end = min(step*4, 141130); start = (step-1)*4
    require(1 <= step <= 35283 and row["actual_presentations"] == end and row["lr"] == 3e-4, "ByT5 optimizer extent or LR differs")
    require(row["ids"] == [ordering[i % 14113] for i in range(start, end)], "ByT5 shuffled record sequence differs")
    require(row["presentations"] == [{"presentation": i, "pass_index": i//14113, "pass_offset": i%14113} for i in range(start, end)], "ByT5 continuous batching differs")
    return stable_hash({key: row[key] for key in ("update", "actual_presentations", "ids", "presentations", "native_source", "native_targets", "loss", "gradient_norm", "lr")})


def run(binding, attempt):
    root = ArtifactRoot(binding); before = root.preflight(); started = time.perf_counter()
    output = BASE/f"scientific-accounting-independent.attempt{attempt:02d}.json"
    if output.exists(): raise FileExistsError(output)
    freeze_path = BASE/"execution-campaign-freeze.attempt01.json"; campaign = json.loads(freeze_path.read_text())
    receipts = {}
    for recipe in campaign["recipes"]:
        name = recipe["recipe_id"]
        paths = sorted(BASE.glob(f"scientific-outcome-{name}.attempt*.json"))
        require(bool(paths), "all seven prescribed outcomes required")
        receipts[name] = [(path, json.loads(path.read_text())) for path in paths]
        require(receipts[name][-1][1]["status"] in ("COMPLETED", "FAILED_NUMERICAL"), "unresolved scientific outcome")
    rows = []; by_data = {}; checkpoints = {}; observations = {}
    for recipe in campaign["recipes"]:
        name = recipe["recipe_id"]; cfg = recipe["config"]; byt5 = name.startswith("G2-ByT5")
        unique = {}; cost = []; ordering = None
        if byt5:
            corpus = json.loads(Path(campaign["corpus_freeze_path"]).read_text())
            pairs = root.path("asr-hypotheses-v1/construction.attempt01/pairs.jsonl")
            require(sha256(pairs) == corpus["pairs_sha256"], "ByT5 TRAIN census bytes differ")
            ordering = [row["id"] for row in (json.loads(line) for line in pairs.open()) if row["role"] == "train"]
            require(len(ordering) == len(set(ordering)) == 14113, "ByT5 TRAIN census differs")
            random.Random(42).shuffle(ordering)
        else:
            directory = root.path(cfg["corpus_geometry"]["artifact_relative"]); read_complete(directory)
            expected_updates = json.loads((directory/"actual-updates.json").read_text())[cfg["update_condition"]]
            require(sha256(directory/"presentations.jsonl") == cfg["corpus_geometry"]["ledger_sha256"], "frozen presentation ledger differs")
        for path, outcome in receipts[name]:
            relative = outcome["output_relative"] if outcome["status"] == "COMPLETED" else outcome["retained_partial_relative"]
            directory = root.path(relative)
            if outcome["status"] == "COMPLETED":
                read_complete(directory); require(sha256(directory/"COMPLETE.json") == outcome["artifact_complete_sha256"], "completed artifact differs")
            require(sha256(BASE/f"scientific-start-{name}.attempt{outcome['attempt']:02d}.json") is not None, "attempt launch receipt missing")
            updates_file = directory/("steps.jsonl" if byt5 else "updates.jsonl")
            physical_updates = presentations = canonical = 0; train_seconds = 0.
            ledger_cursor = 0
            ledger_stream = None if byt5 else (root.path(cfg["corpus_geometry"]["artifact_relative"])/"presentations.jsonl").open()
            if updates_file.exists():
                with updates_file.open() as stream:
                    for line in stream:
                        row = json.loads(line); step = row["update"]
                        if byt5: identity = byt5_update(row, ordering)
                        else:
                            expected = expected_updates[step-1]; selected = []
                            while ledger_cursor <= expected["last_ordinal"]:
                                planned = json.loads(next(ledger_stream))
                                require(planned["ordinal"] == ledger_cursor, "ledger ordinal is discontinuous")
                                if ledger_cursor >= expected["first_ordinal"]: selected.append(planned)
                                ledger_cursor += 1
                            identity = native_update(row, expected, selected, cfg["arm"])
                            canonical += row["canonical_charge"]
                        incorporate(unique, step, identity); physical_updates += 1
                        presentations += len(row["ids"]) if byt5 else row["examples"]
                        train_seconds += row["wall_seconds"] if byt5 else row["update_wall_seconds"]
            if ledger_stream: ledger_stream.close()
            cost.append({"attempt": outcome["attempt"], "status": outcome["status"], "receipt": str(path), "receipt_sha256": sha256(path),
                "elapsed_seconds_MEASURED": outcome["elapsed_seconds"], "logged_training_seconds_MEASURED": train_seconds,
                "logged_physical_updates_MEASURED": physical_updates, "logged_physical_presentations_MEASURED": presentations,
                "logged_physical_canonical_charge_MEASURED": canonical if not byt5 else None,
                "updates_sha256": sha256(updates_file) if updates_file.exists() else None,
                "failed_or_interrupted_work_retained_and_charged": True,
                "unlogged_failed_microbatch_extent": "UNMEASURED" if outcome["status"] != "COMPLETED" else "not applicable"})
            for checkpoint in outcome.get("checkpoints", []):
                point = checkpoint["relative"]; read_complete(root.path(point))
                checkpoints[point] = {"COMPLETE_sha256": sha256(root.path(point)/"COMPLETE.json"),
                    "seconds_MEASURED": checkpoint["seconds"], "optimizer_update": checkpoint["optimizer_update"]}
        terminal = receipts[name][-1][1]
        last = max(unique, default=0)
        require(set(unique) == set(range(1, last+1)), "a completed scientific update is missing from retained attempts")
        if terminal["status"] == "COMPLETED": require(last == (35283 if byt5 else cfg["stop_endpoint"]["optimizer_updates"]), "resolved completion differs from fixed extent")
        for path in sorted(BASE.glob(f"scientific-observation-{name}.update*.attempt*.json")):
            observation = json.loads(path.read_text())
            directories = {str(Path(p).parent) for p in observation["payload_hashes"]}
            require(len(directories) == 1, "one atomic observation directory required")
            point = directories.pop()
            require(point not in observations, "one physical evaluation charged twice")
            read_complete(root.path(point))
            observations[point] = {"receipt": str(path), "receipt_sha256": sha256(path), "seconds_MEASURED": observation["seconds"],
                "state": observation.get("milestone", observation.get("endpoint")),
                "payload_hashes": observation["payload_hashes"]}
        actual_presentations = min(last*4, 141130) if byt5 else (expected_updates[last-1]["last_ordinal"]+1 if last else 0)
        actual_exposure = None if byt5 else (expected_updates[last-1]["completed_actual_exposure"] if last else 0)
        digest = stable_hash(unique)
        rows.append({"recipe_id": name, "status": terminal["status"], "unique_logged_optimizer_updates": last,
            "unique_scientific_presentations": actual_presentations, "unique_scientific_canonical_exposure": actual_exposure,
            "completed_update_identities_sha256": digest, "attempts": cost,
            "attempt_elapsed_seconds_MEASURED": sum(row["elapsed_seconds_MEASURED"] for row in cost),
            "checkpoint_and_evaluation_time_is_already_in_attempt_elapsed": True,
            "ByT5_offsets_are_in_fixed_extent_not_added": byt5})
        if not byt5 and terminal["status"] == "COMPLETED":
            ledger_identity = (cfg["corpus_geometry"]["ledger_sha256"], actual_presentations, actual_exposure)
            if cfg["data_condition"] in by_data: require(by_data[cfg["data_condition"]] == ledger_identity, "within-D matched exposure differs")
            by_data[cfg["data_condition"]] = ledger_identity
    # Failed/interrupted attempts may have completed saves before their failure.
    # Inventory those immutable directories even when the outcome lacks a timer.
    names = tuple(recipe["recipe_id"]+"." for recipe in campaign["recipes"])
    for directory in root.path("scientific-checkpoints-v1").iterdir():
        if not directory.is_dir() or not directory.name.startswith(names) or ".partial-" in directory.name: continue
        read_complete(directory); point = str(directory.relative_to(root.root))
        complete = json.loads((directory/"COMPLETE.json").read_text())
        record = checkpoints.setdefault(point, {"COMPLETE_sha256": sha256(directory/"COMPLETE.json"), "seconds_MEASURED": None,
                                               "save_time_status": "UNMEASURED_SEPARATELY_INCLUDED_IN_ATTEMPT_ELAPSED"})
        record["retained_file_hashes"] = complete
        record["logical_payload_bytes_MEASURED"] = sum(p.stat().st_size for p in directory.iterdir() if p.is_file())
    result = {"schema": "g2_scientific_accounting_independent_v1", "status": "PASS_INDEPENDENT_SCIENTIFIC_TRAJECTORY_ACCOUNTING",
        "campaign_sha256": sha256(freeze_path), "recipes": rows, "checkpoint_inventory": checkpoints,
        "physical_evaluations": observations, "within_D_exact_matching": by_data,
        "cross_D_exposure_is_not_claimed_equal": True, "failed_attempts_included": True,
        "cost_UNPRICED": ["electricity", "hardware depreciation", "local monetary price"],
        "no_cloud_spending": True, "before": before, "after": root.preflight(),
        "code_sha256": sha256(__file__), "elapsed_seconds": time.perf_counter()-started}
    with output.open("x") as stream: json.dump(result, stream, sort_keys=True, allow_nan=False); stream.write("\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--artifact-binding", required=True); parser.add_argument("--attempt", type=int, required=True)
    args = parser.parse_args(); print(json.dumps({"status": run(args.artifact_binding, args.attempt)["status"]}))
