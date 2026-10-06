"""CPU-only reconstruction of six-probe provenance; imports no campaign code."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

import numpy as np


SAFE = Path("experiments/manifests/six_10m_probes")
PRIVATE = Path("exports/six-10m-probes")
FREEZE = SAFE / "campaign-freeze.attempt01.json"
CAMPAIGN_SHA = "43a97ef40acbb2efebaf4941931934969c093e23f77b69bfd132f236755b1dd3"
AUTHORIZED = "7868302afc43e3cbd475464452f57912a9c2cf97"
LEDGER = Path("exports/lexical-reader-v2/mixed-reader-attempt02/presentations.jsonl")
INDEX = Path("experiments/manifests/lexical_reader_v2/mixed-reader-update-index.attempt02.json")
POOLS = [Path("exports/lexical-reader-v2/generated-pool-attempt02/accepted.jsonl"),
         Path("exports/lexical-reader-v2/mixed-reader-attempt02/natural-accepted.jsonl")]
LATENTS = Path("experiments/manifests/stress_split_repair_20261005T054436Z/latents.jsonl")
COMPONENTS = ("action", "start", "end", "vocabulary")


def check(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def lines(path):
    with Path(path).open() as stream:
        for line in stream:
            yield json.loads(line)


def canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2,
                      allow_nan=False).encode() + b"\n"


def ordered_ids(rows):
    return hashlib.sha256(canonical([r["id"] for r in rows])).hexdigest()


def pool_key(row):
    if row["channel"] == "natural":
        return "real/natural"
    path = row["subpath"]
    if row["channel"] == "identity_minimal":
        if path[0] == "identity":
            return "identity/natural"
        channel, path = "minimal", path[1:]
    else:
        channel = row["channel"]
    category, _, cell, view = path
    return f"{channel}/{category}/{cell}/{view}"


def reconstruct_ledger(freeze):
    accepted = {}
    for path in POOLS:
        for row in lines(path):
            check(row["variant_id"] not in accepted, "duplicate accepted variant")
            for key in ("source", "target", "anchor"):
                check(hashlib.sha256(row[key].encode()).hexdigest() == row[key + "_sha256"],
                      "accepted literal hash mismatch")
            check(len(row["canonical_sequence"]) == row["canonical_charge"], "canonical length mismatch")
            check({k: len(row["gold_labels"][k]) for k in COMPONENTS} == row["C_denominators"],
                  "accepted event denominator mismatch")
            accepted[row["variant_id"]] = row
    ledger = list(lines(LEDGER))
    supplied = read(INDEX)
    queues, current, exposure = [], [], 0
    for ordinal, row in enumerate(ledger):
        check(row["ordinal"] == ordinal and row["presentation_id"] == f"seed42/{ordinal:09d}",
              "ledger ordinal mismatch")
        item = accepted[row["variant_id"]]
        check(row["accepted_row_sha256"] == hashlib.sha256(canonical(item)).hexdigest(),
              "accepted row binding mismatch")
        check(all(row[k + "_sha256"] == item[k + "_sha256"] for k in ("source", "target", "anchor")),
              "presentation literal binding mismatch")
        phase = "P0" if exposure < 6666667 else "P1" if exposure < 9333334 else "P2"
        check(row["phase"] == phase and row["start_exposure"] == exposure, "ledger phase/start mismatch")
        check(row["canonical_charge"] == item["canonical_charge"], "presentation charge mismatch")
        exposure += row["canonical_charge"]
        check(row["end_exposure"] == exposure, "ledger endpoint mismatch")
        current.append(row)
        if sum(r["canonical_charge"] for r in current) >= 32768:
            queues.append(current)
            current = []
    check(not current and len(queues) == 305 and len(ledger) == 134591 and exposure == 10007223,
          "frozen complete endpoint mismatch")
    check(len(supplied) == len(queues), "index length mismatch")
    for number, (queue, item) in enumerate(zip(queues, supplied)):
        denoms = {"B": sum(len(accepted[r["variant_id"]]["target_ids"]) + 1 for r in queue),
                  "C": {k: sum(len(accepted[r["variant_id"]]["gold_labels"][k]) for r in queue)
                        for k in COMPONENTS}}
        check(item["update"] == number and item["first_ordinal"] == queue[0]["ordinal"]
              and item["last_ordinal"] == queue[-1]["ordinal"] and item["examples"] == len(queue)
              and item["canonical_charge"] == sum(r["canonical_charge"] for r in queue)
              and item["start_exposure"] == queue[0]["start_exposure"]
              and item["end_exposure"] == queue[-1]["end_exposure"]
              and item["B_denominator"] == denoms["B"] and item["C_denominators"] == denoms["C"],
              "independently reconstructed queue/index mismatch")
        for key, field in (("channel", "channel_charges"), ("phase", "phase_segments")):
            charges = Counter()
            for row in queue:
                charges[row[key]] += row["canonical_charge"]
            check(dict(charges) == item[field], "queue allocation mismatch")
    for endpoint in freeze["save_endpoints"] + freeze["evaluation_endpoints"]:
        nominal, update = endpoint["nominal"], endpoint["update"]
        expected_update = 0 if nominal == 0 else next(i + 1 for i, q in enumerate(queues)
                                                    if q[-1]["end_exposure"] >= nominal)
        check(update == expected_update, "endpoint was not first completed update")
        check(endpoint["canonical_exposure"] == (queues[update - 1][-1]["end_exposure"] if update else 0)
              and endpoint["last_ordinal"] == (queues[update - 1][-1]["ordinal"] if update else -1),
              "endpoint clock mismatch")
    return accepted, ledger, queues, supplied


def audit_reader(state, prefix, accepted):
    check(state["exposure"] == (prefix[-1]["end_exposure"] if prefix else 0)
          and state["presentation"] == len(prefix)
          and state["phase"] == (prefix[-1]["phase"] if prefix else None), "reader cursor mismatch")
    uses = defaultdict(Counter)
    nodes = defaultdict(Counter)
    for row in prefix:
        uses[pool_key(row)][row["variant_id"]] += 1
        if row["phase"] == state["phase"]:
            path = [row["channel"], *row["subpath"]]
            for i, child in enumerate(path):
                nodes[tuple(path[:i])][child] += row["canonical_charge"]
    for key, leaf in state["pools"].items():
        check(leaf["pool"] == key and leaf["uses"] == dict(uses[key]), "reader leaf uses mismatch")
        if key in ("identity/natural", "real/natural"):
            view = "identity" if key.startswith("identity") else "natural"
            count = sum(row.get("view") == view and "source_group_id" in row for row in accepted.values())
        else:
            _, category, cell, view = key.split("/")
            count = sum(row.get("category") == category and str(row.get("cell")) == cell
                        and row.get("view") == view for row in accepted.values())
        check(count > 0, "empty reader pool")
        total = sum(uses[key].values())
        expected = (0, 0) if total == 0 else ((total - 1) // count, (total - 1) % count + 1)
        check((leaf["pass"], leaf["offset"]) == expected, "reader leaf pass/offset mismatch")
    check(set(uses) <= set(state["pools"]), "used pool missing in checkpoint")

    def walk(value, path=()):
        if "children" not in value:
            check(value == state["pools"][value["pool"]], "tree/pool cursor mismatch")
            return
        check(value["charges"] == dict(nodes[path]) and value["total"] == sum(nodes[path].values()),
              "reader deficit charges mismatch")
        for name, child in value["children"].items():
            walk(child, (*path, name))

    if prefix:
        walk(state["deficits"])
    else:
        check(state["deficits"] is None and not state["pools"], "initial reader state mismatch")


def parameter_hashes(path, metadata):
    digests = {p: hashlib.sha256() for p in ("model", "m", "v", "acc")}
    count, arrays, zero_acc = 0, 0, True
    with np.load(path, allow_pickle=False) as data:
        check(set(data.files) == set(metadata["shapes"]) == set(metadata["dtypes"]), "tensor inventory mismatch")
        for key in sorted(data.files):
            value = data[key]
            check(list(value.shape) == metadata["shapes"][key] and str(value.dtype) == metadata["dtypes"][key],
                  "tensor shape/dtype mismatch")
            check(np.isfinite(value).all(), "nonfinite verified checkpoint tensor")
            prefix = key.split("::", 1)[0]
            check(value.dtype == (np.uint32 if prefix == "rng" else np.float32), "checkpoint precision mismatch")
            if prefix in digests:
                digests[prefix].update(json.dumps([key, list(value.shape), str(value.dtype)],
                                                 separators=(",", ":")).encode())
                digests[prefix].update(value.tobytes(order="C"))
            if prefix == "model":
                count += value.size
            if prefix == "acc":
                zero_acc = zero_acc and not np.any(value)
            arrays += 1
    return {p: d.hexdigest() for p, d in digests.items()}, int(count), arrays, bool(zero_acc)


def audit_checkpoint(path, receipt, recipe, freeze, accepted, ledger, queues):
    complete = read(path / "COMPLETE.json")
    check(set(complete) == {"arrays.npz", "metadata.json"}, "native publication inventory mismatch")
    for name, digest in complete.items():
        check(sha(path / name) == digest, "native checkpoint byte identity mismatch")
    meta = read(path / "metadata.json")
    step = meta["optimizer_step"]
    exposure = queues[step - 1][-1]["end_exposure"] if step else 0
    ordinal = queues[step - 1][-1]["ordinal"] if step else -1
    expected_identities = {**freeze["runtime_identities"], "campaign_sha256": CAMPAIGN_SHA,
                           "recipe_config_sha256": recipe["config_sha256"]}
    model = freeze["models"][recipe["config"]["arm"]]
    check(meta["identities"] == expected_identities and meta["config"] == model["config"]
          and meta["optimizer_policy"] == model["optimizer"]
          and meta["arm"] == recipe["config"]["arm"] and meta["microbatch_size"] == model["microbatch_examples"]
          and meta["working_dtype"] == "mlx.core.bfloat16" and meta["enforce_complete_target"], "checkpoint treatment mismatch")
    check(meta["clock"] == {"peak": recipe["config"]["peak_lr"], "planned_exposure": 10000000,
                            "warmup": 200000, "floor_fraction": 0.1}, "checkpoint LR clock mismatch")
    check(meta["committed_exposure"] == exposure and not meta["queue"] and meta["pending_charge"] == 0
          and meta["accumulator_microbatches"] == meta["completed_microbatches"] == 0,
          "checkpoint is not a complete common update boundary")
    audit_reader(meta["reader_state"], ledger[:ordinal + 1], accepted)
    hashes, count, arrays, zero_acc = parameter_hashes(path / "arrays.npz", meta)
    check(count == model["parameter_count"] and zero_acc, "complete checkpoint parameter/accumulator mismatch")
    check(receipt["recipe_id"] == recipe["recipe_id"] and receipt["update"] == step
          and receipt["canonical_exposure"] == exposure and receipt["parameter_sha256"] == hashes["model"],
          "checkpoint receipt/state mismatch")
    if "optimizer_sha256" in receipt:
        check(receipt["optimizer_sha256"] == {k: hashes[k] for k in ("m", "v")}
              and receipt["checkpoint_complete_sha256"] == sha(path / "COMPLETE.json")
              and receipt["last_ordinal"] == ordinal and receipt["runtime_identities"] == expected_identities,
              "checkpoint receipt identities mismatch")
    if step == 0:
        check(hashes["model"] == model["initial_parameter_sha256"]
              and hashes["m"] + ":" + hashes["v"] == model["initial_optimizer_sha256"], "initial state mismatch")
    check("python_rng" in meta and "numpy_rng" in meta and "rng" in meta["shapes"], "checkpoint RNG absent")
    return {"path": str(path), "update": step, "canonical_exposure": exposure, "last_ordinal": ordinal,
            "arrays_sha256": complete["arrays.npz"], "metadata_sha256": complete["metadata.json"],
            "complete_sha256": sha(path / "COMPLETE.json"), "parameter_sha256": hashes["model"],
            "optimizer_sha256": {k: hashes[k] for k in ("m", "v")}, "parameter_count": count,
            "array_count": arrays, "reader_state_sha256": hashlib.sha256(canonical(meta["reader_state"])).hexdigest()}


def audit_updates(path, recipe, queues, accepted, max_update=None):
    observed = []
    structure = hashlib.sha256()
    if max_update == 0:
        return observed, structure.hexdigest()
    for result in lines(path):
        number = result["update"]
        queue = queues[number - 1]
        check(result["presentation_ids"] == [r["presentation_id"] for r in queue]
              and result["examples"] == len(queue)
              and result["canonical_charge"] == sum(r["canonical_charge"] for r in queue)
              and result["committed_canonical_exposure"] == queue[-1]["end_exposure"], "actual common queue mismatch")
        check(result["denominators"] == {"B": sum(len(accepted[r["variant_id"]]["target_ids"]) + 1 for r in queue),
                                        "C": {k: sum(accepted[r["variant_id"]]["C_denominators"][k] for r in queue)
                                              for k in COMPONENTS}}, "actual whole-queue denominator mismatch")
        exposure = min(result["committed_canonical_exposure"], 10000000)
        peak = recipe["config"]["peak_lr"]
        lr = peak * exposure / 200000 if exposure < 200000 else peak * (
            0.1 + 0.9 * (1 + math.cos(math.pi * (exposure - 200000) / 9800000)) / 2)
        check(math.isclose(result["lr"], lr, rel_tol=1e-14, abs_tol=1e-18), "actual LR mismatch")
        check(result["phase"] == queue[-1]["phase"] and math.isfinite(result["loss"])
              and math.isfinite(result["gradient_norm"]), "update phase/numerical accounting mismatch")
        check(len(result["actual_consumption"]) == len(queue), "native consumption count mismatch")
        size = 16 if recipe["config"]["arm"] == "B100" else 4
        for index, (actual, frozen) in enumerate(zip(result["actual_consumption"], queue)):
            row = accepted[frozen["variant_id"]]
            check(all(actual[k] == frozen[k] for k in ("presentation_id", "variant_id", "canonical_charge",
                                                       "channel", "phase", "source_sha256", "target_sha256", "anchor_sha256"))
                  and actual["cumulative_canonical_exposure"] == frozen["end_exposure"], "native trace identity mismatch")
            batch = queue[index // size * size:index // size * size + size]
            width = max(len(accepted[r["variant_id"]]["source_ids"]) for r in batch)
            check(actual["native_source_ids"] == row["source_ids"] + [256] * (width - len(row["source_ids"])),
                  "native source input differs from accepted row")
            if recipe["config"]["arm"] == "B100":
                width = max(len(accepted[r["variant_id"]]["target_ids"]) + 1 for r in batch)
                check(actual["native_target_ids_with_EOS"] == row["target_ids"] + [258]
                      + [256] * (width - len(row["target_ids"]) - 1), "native target input mismatch")
            else:
                check(actual["native_event_labels"] == row["gold_labels"]
                      and actual["native_encoder_positions"] == row["encoder_positions"]
                      and actual["native_legal_pointer_mask"] == row["legal"], "native event input mismatch")
        check(not observed or number == observed[-1] + 1, "attempt update sequence gap")
        observed.append(number)
        structure.update(canonical(result))
        if number == max_update:
            break
    return observed, structure.hexdigest()


def audit():
    check(sha(FREEZE) == CAMPAIGN_SHA, "campaign freeze hash mismatch")
    freeze = read(FREEZE)
    check(freeze["authorized_checkpoint"] == AUTHORIZED and freeze["seed"] == 42
          and freeze["scientific_recipe_slots_consumed"] == 0, "pre-run authority mismatch")
    for path, digest in {**freeze["source_hashes"], **freeze["data_identities"]}.items():
        check(sha(path) == digest, "frozen source/data hash mismatch: " + path)
    check(sha(LATENTS) == freeze["generated_evaluation_latents_sha256"], "generated latent identity mismatch")
    order = freeze["execution_order"]
    check(len(order) == len(set(order)) == len(freeze["recipes"]) == 6, "six-slot freeze mismatch")
    check(order == [f"{arm}-seed42-lr{lr}" for lr in ("1e-04", "3e-04", "6e-04")
                    for arm in ("B100", "C101")], "frozen recipe order mismatch")
    for recipe in freeze["recipes"]:
        check(recipe["recipe_id"] in order and recipe["status"] == "AUTHORIZED_UNSTARTED"
              and sha(recipe["config_path"]) == recipe["config_sha256"]
              and read(recipe["config_path"]) == recipe["config"], "frozen recipe/config mismatch")
    check(not freeze["final_training_started"] and not freeze["sealed_inference_performed"]
          and not freeze["paper_protocol_v2_frozen"], "forbidden campaign state in freeze")
    accepted, ledger, queues, _ = reconstruct_ledger(freeze)
    panel = read(freeze["evaluation_panel_path"])
    check(sha(freeze["evaluation_panel_path"]) == freeze["evaluation_panel_sha256"]
          and len(panel) == len({r["id"] for r in panel}) == 396
          and Counter(r["population"] for r in panel) == {"natural": 108, "generated": 288}, "panel identity mismatch")
    starts = sorted(SAFE.glob("start-*.attempt*.json"))
    terminals = sorted(SAFE.glob("recipe-*.attempt*.json"))
    check(all(read(p)["recipe_id"] in order for p in starts + terminals), "unregistered recipe slot")
    check(all(p.name in order for p in PRIVATE.iterdir() if p.is_dir()), "unregistered private recipe directory")
    recipes, timelines, reader_hashes = [], [], defaultdict(set)
    for recipe in sorted(freeze["recipes"], key=lambda r: order.index(r["recipe_id"])):
        identifier = recipe["recipe_id"]
        start_files = sorted(SAFE.glob(f"start-{identifier}.attempt*.json"))
        complete_files = sorted(SAFE.glob(f"recipe-{identifier}.attempt*.json"))
        check(len(complete_files) <= 1, "recipe has multiple terminal outcomes")
        observations = {"recipe_id": identifier, "status": "UNSTARTED", "starts": [], "checkpoints": [],
                        "evaluations": [], "failures": [], "interruption_receipts": [], "updates": []}
        check([read(p)["attempt"] for p in start_files] == list(range(1, len(start_files) + 1)),
              "attempt number gap")
        for path in start_files:
            start = read(path)
            expected_identities = {**freeze["runtime_identities"], "campaign_sha256": CAMPAIGN_SHA,
                                   "recipe_config_sha256": recipe["config_sha256"]}
            check(start["campaign_sha256"] == CAMPAIGN_SHA and start["config_sha256"] == recipe["config_sha256"]
                  and start["runtime_identities"] == expected_identities and start["seed"] == 42
                  and start["dirty_status"] == "" and start["no_concurrent_accelerator"]
                  and start["hardware"] == freeze["hardware"]
                  and start["initial_parameter_sha256"] == freeze["models"][recipe["config"]["arm"]]["initial_parameter_sha256"],
                  "recorded recipe start mismatch")
            check(subprocess.run(["git", "merge-base", "--is-ancestor", AUTHORIZED, start["head"]],
                                 capture_output=True).returncode == 0, "recipe source ancestry mismatch")
            frozen_at_start = subprocess.check_output(["git", "show", f"{start['head']}:{FREEZE}"])
            check(hashlib.sha256(frozen_at_start).hexdigest() == CAMPAIGN_SHA,
                  "campaign was not committed at the recorded start")
            for source_path, expected_sha in freeze["source_hashes"].items():
                source_at_start = subprocess.check_output(["git", "show", f"{start['head']}:{source_path}"])
                check(hashlib.sha256(source_at_start).hexdigest() == expected_sha,
                      "recorded source commit differs from frozen runtime")
            directory = Path(start["output_directory"])
            check(directory == PRIVATE / identifier / f"attempt{start['attempt']:02d}" and read(directory / "preflight.json")
                  == {k: v for k, v in start.items() if k != "status"}, "private/public start mismatch")
            if start["resume_path"] is not None:
                resume = Path(start["resume_path"])
                check(resume.parent.parent == PRIVATE / identifier and (resume / "COMPLETE.json").exists(),
                      "cross-recipe or missing resume checkpoint")
                prior_attempt = start["attempt"] - 1
                failure_path = SAFE / f"failure-{identifier}.attempt{prior_attempt:02d}.json"
                interruption_path = SAFE / f"interruption-{identifier}.attempt{prior_attempt:02d}.json"
                check(prior_attempt >= 1 and (failure_path.exists() or interruption_path.exists()),
                      "resume lacks a preserved preceding attempt")
                preceding = read(failure_path if failure_path.exists() else interruption_path)
                check(start["resume_path"] == preceding.get("last_verified_checkpoint", preceding.get("verified_resume_path")),
                      "resume did not restore the last registered verified state")
            else:
                check(start["attempt"] == 1, "later attempt restarted from scratch")
            observations["starts"].append({"path": str(path), "sha256": sha(path), "attempt": start["attempt"],
                                           "head": start["head"], "resume_path": start["resume_path"]})
            timelines.append((start["start_unix"], identifier))
        if start_files:
            observations["status"] = "ACTIVE_OR_PARTIAL"
        for path in sorted((PRIVATE / identifier).glob("attempt*/checkpoint-update*-receipt.json")):
            receipt = read(path)
            observed = audit_checkpoint(Path(receipt["checkpoint_path"]), receipt, recipe, freeze, accepted, ledger, queues)
            observations["checkpoints"].append(observed)
            reader_hashes[observed["update"]].add(observed["reader_state_sha256"])
        for path in sorted(SAFE.glob(f"failure-{identifier}.attempt*.json")):
            failure = read(path)
            directory = PRIVATE / identifier / f"attempt{failure['attempt']:02d}"
            check(read(directory / "failure.json") == failure
                  and sha(directory / "failed-state-arrays.npz") == failure["failed_arrays_sha256"]
                  and sha(directory / "failed-state-metadata.json") == failure["failed_metadata_sha256"],
                  "failure state preservation mismatch")
            observations["failures"].append({"path": str(path), "sha256": sha(path), "attempt": failure["attempt"],
                                             "disposition": failure["disposition"], "completed_update": failure["completed_update"],
                                             "committed_exposure": failure["committed_exposure"]})
        numeric = [f for f in observations["failures"] if f["disposition"] == "NUMERICAL_FAILURE"]
        check(len(numeric) <= 2, "more than one registered numerical replay")
        for path in sorted(SAFE.glob(f"interruption-{identifier}.attempt*.json")):
            interruption = read(path)
            resume = Path(interruption["verified_resume_path"])
            check(resume.parent.parent == PRIVATE / identifier,
                  "interruption resume scope mismatch")
            if resume.name.startswith("interruption-"):
                receipt = read(resume.with_name(resume.name + "-receipt.json"))
                audit_checkpoint(resume, receipt, recipe, freeze, accepted, ledger, queues)
            observations["interruption_receipts"].append({"path": str(path), "sha256": sha(path)})
        for path in sorted(SAFE.glob(f"evaluation-{identifier}-update*.attempt*.json")):
            evaluation = read(path)
            endpoint = evaluation["actual_endpoint"]
            check(endpoint in freeze["evaluation_endpoints"] and evaluation["panel_sha256"] == freeze["evaluation_panel_sha256"]
                  and evaluation["recipe_id"] == identifier, "evaluation endpoint/population mismatch")
            attempt = int(path.name.split(".attempt")[1].split(".")[0])
            output = PRIVATE / identifier / f"attempt{attempt:02d}" / f"evaluation-update{endpoint['update']:03d}.jsonl"
            check(sha(output) == evaluation["output_sha256"], "evaluation output binding mismatch")
            rows = list(lines(output))
            check([r["id"] for r in rows] == [r["id"] for r in panel], "evaluation ID/order mismatch")
            for actual, frozen in zip(rows, panel):
                check(all(actual[k] == frozen[k] for k in ("population", "source_sha256", "target_sha256"))
                      and actual["arm"] == recipe["config"]["arm"]
                      and actual["checkpoint_label"] == f"update{endpoint['update']:03d}", "evaluation case binding mismatch")
            observations["evaluations"].append({"path": str(path), "sha256": sha(path), "endpoint": endpoint,
                                                "output_sha256": sha(output), "ordered_ids_sha256": ordered_ids(rows),
                                                "case_count": len(rows)})
        if complete_files:
            terminal = read(complete_files[0])
            check(terminal["campaign_sha256"] == CAMPAIGN_SHA, "terminal campaign identity mismatch")
            observations["status"] = terminal["status"]
            observations["terminal_path"] = str(complete_files[0])
            observations["terminal_sha256"] = sha(complete_files[0])
            if terminal["status"] == "COMPLETED":
                directory = Path(terminal["private_output_directory"])
                check(read(directory / "recipe-complete.json") == terminal
                      and sha(directory / "updates.jsonl") == terminal["updates_sha256"]
                      and terminal["endpoint"] == recipe["config"]["actual_stop_endpoint"]
                      and terminal["numerical_replays"] == len(numeric), "completed recipe receipt mismatch")
                check({r["update"] for r in observations["checkpoints"]} == {r["update"] for r in freeze["save_endpoints"]}
                      and {r["endpoint"]["update"] for r in observations["evaluations"]}
                      == {r["update"] for r in freeze["evaluation_endpoints"]}, "completed save/evaluation schedule missing")
                final = next(r for r in observations["checkpoints"] if r["update"] == 305
                             and r["parameter_sha256"] == terminal["final_parameter_sha256"])
                check(final["complete_sha256"] == terminal["final_checkpoint_complete_sha256"], "final checkpoint identity mismatch")
            else:
                check(terminal["status"] == "FAILED" and len(numeric) == 2, "unregistered terminal failure")
            covered = set()
            for start_path in start_files:
                start = read(start_path)
                update_path = Path(start["output_directory"]) / "updates.jsonl"
                updates, structure = audit_updates(update_path, recipe, queues, accepted)
                if updates:
                    resume_step = read(Path(start["resume_path"]) / "metadata.json")["optimizer_step"] if start["resume_path"] else 0
                    check(updates[0] == resume_step + 1, "resume starts from wrong update")
                covered.update(updates)
                observations["updates"].append({"path": str(update_path), "sha256": sha(update_path),
                                                "observed_structure_sha256": structure,
                                                "count": len(updates), "first": updates[0] if updates else None,
                                                "last": updates[-1] if updates else None})
            if terminal["status"] == "COMPLETED":
                check(covered == set(range(1, 306)), "completed recipe update coverage incomplete")
        elif start_files:
            # The live file can continue growing; audit only its published-checkpoint prefix.
            start = read(start_files[-1])
            directory = Path(start["output_directory"])
            resume_step = read(Path(start["resume_path"]) / "metadata.json")["optimizer_step"] if start["resume_path"] else 0
            published = [r["update"] for r in observations["checkpoints"] if Path(r["path"]).parent == directory]
            last = max(published, default=resume_step)
            updates, structure = audit_updates(directory / "updates.jsonl", recipe, queues, accepted,
                                               max_update=last if last > resume_step else 0)
            check(updates == list(range(resume_step + 1, last + 1)), "published prefix update coverage mismatch")
            observations["updates"].append({"path": str(directory / "updates.jsonl"),
                                            "scope": "published-checkpoint prefix; live suffix not audited",
                                            "observed_structure_sha256": structure, "count": len(updates),
                                            "first": updates[0] if updates else None,
                                            "last": updates[-1] if updates else None})
        recipes.append(observations)
    check(all(len(values) == 1 for values in reader_hashes.values()), "reader state differs across recipes at common endpoint")
    observed_order = []
    for _, identifier in sorted(timelines):
        if not observed_order or identifier != observed_order[-1]:
            observed_order.append(identifier)
    check(observed_order == order[:len(observed_order)], "actual recipe execution order mismatch")
    terminal_count = sum(r["status"] in ("COMPLETED", "FAILED") for r in recipes)
    completed_count = sum(r["status"] == "COMPLETED" for r in recipes)
    return {"campaign_sha256": CAMPAIGN_SHA, "frozen_recipe_order": order, "recipes": recipes,
            "ledger_sha256": sha(LEDGER), "ledger_presentations_reconstructed": len(ledger),
            "common_updates_reconstructed": len(queues), "common_endpoint_exposures": 10007223,
            "panel_sha256": freeze["evaluation_panel_sha256"], "panel_ordered_ids_sha256": ordered_ids(panel),
            "panel_population_counts": dict(Counter(r["population"] for r in panel)),
            "slots_started": sum(bool(r["starts"]) for r in recipes), "terminal_outcomes": terminal_count,
            "completed_10M_recipes": completed_count, "all_six_terminal_outcomes_available": terminal_count == 6,
            "all_six_10M_endpoints_available": completed_count == 6,
            "disposition": "SIX_RECIPE_PROVENANCE_RECONSTRUCTED" if terminal_count == 6
                           else "PARTIAL_PROVENANCE_RECONSTRUCTED_CAMPAIGN_PENDING"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    receipt = Path(args.receipt)
    check(not receipt.is_absolute() and receipt.parent == SAFE
          and receipt.name.startswith("independent-provenance") and not receipt.exists(), "new public relative receipt required")
    result = {"schema": "six10m_independent_provenance_v1", "utc": datetime.now(timezone.utc).isoformat(),
              "checker_path": "benchmarks/six_10m_provenance_independent.py", "checker_sha256": sha(__file__),
              "accelerator_used": False, "MLX_imported": False, "Torch_imported": False,
              "metric_selection_reproduction": "SEPARATE_REVIEW_NOT_PERFORMED_HERE"}
    exit_code = 0
    try:
        result.update(audit())
        if args.require_complete and not result["all_six_terminal_outcomes_available"]:
            exit_code = 2
    except Exception as error:
        result.update(disposition="PROVENANCE_RECONSTRUCTION_FAILED", error_type=type(error).__name__, error=str(error))
        exit_code = 1
    with receipt.open("x") as stream:
        stream.write(canonical(result).decode())
    print(json.dumps({k: result[k] for k in ("disposition", "slots_started", "terminal_outcomes", "error") if k in result}))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
