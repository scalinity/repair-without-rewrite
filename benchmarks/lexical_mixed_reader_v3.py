"""CPU-only full-pilot presentation/accounting dry run; no model execution."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import subprocess
import time

from benchmarks.lexical_corruption_profile_v2 import admitted_rows, sha
from src.data.lexical_corruption_v2 import concentration_alarms, serialized
from src.data.mixed_reader_v3 import MixedReader, PHASE_ENDS, READER_VERSION, native_shape
from src.generation.lexical_v2 import digest
from src.models.tokenizer import ByteBPE
from src.scoring.text import lexical


SAFE = Path("experiments/manifests/lexical_reader_v2")
POOL = Path("exports/lexical-reader-v2/generated-pool-attempt02/accepted.jsonl")


def row_hash(row):
    return hashlib.sha256(serialized(row)).hexdigest()


def write(path, value):
    path.write_bytes(serialized(value))


def prepare():
    qualification = json.loads((SAFE / "generated-pool-qualification.attempt02.json").read_text())
    if qualification["scientific_stop_triggered"] or qualification["empty_required_strata"]:
        raise ValueError("generated-pool scientific stop blocks reader")
    if sha(POOL) != qualification["accepted_pool_sha256"]:
        raise ValueError("accepted pool bytes changed")
    generated = [json.loads(line) for line in POOL.read_text().splitlines()]
    for row in generated:
        for field in ("source", "anchor", "target"):
            if digest(row[field]) != row[field + "_sha256"]:
                raise ValueError("changed accepted generated row")
    tokenizer = ByteBPE.load("configs/tokenizer_development")
    identity, natural = [], []
    for row in admitted_rows():
        for channel, destination in (("identity", identity), ("natural", natural)):
            source = row["target"] if channel == "identity" else row["source"]
            shape = native_shape(tokenizer, source, row["target"], row["target"])
            if shape is None:
                raise ValueError("one of the 1,024 required natural TRAIN rows exceeds common capacity")
            destination.append({"variant_id": channel + "/" + row["id"], "record_id": row["id"],
                "source_group_id": row["source_group_id"], "view": channel,
                "source": source, "anchor": row["target"], "target": row["target"],
                "source_sha256": digest(source), "anchor_sha256": digest(row["target"]),
                "target_sha256": digest(row["target"]), "source_equals_target": source == row["target"],
                "lexical_source_equals_target": lexical(source) == lexical(row["target"]),
                "operations": [], **shape})
    table = json.loads((SAFE / "lexical-profile-table.attempt01.json").read_text())
    reader = MixedReader(generated, identity, natural, {
        1: table["severity_P1_P2"]["1"], 2: table["severity_P1_P2"]["2"]})
    return generated, identity, natural, reader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempt", type=int, required=True)
    args = parser.parse_args()
    if args.attempt < 1:
        raise ValueError("attempt must be positive")
    tag = f"attempt{args.attempt:02d}"
    OUT = Path("exports/lexical-reader-v2/mixed-reader-" + tag)
    OUT.mkdir(parents=True, exist_ok=False)
    identities = {path: sha(path) for path in (
        "src/data/mixed_reader_v3.py", "src/generation/lexical_v2.py", "benchmarks/lexical_mixed_reader_v3.py",
        "configs/tokenizer_development/tokenizer.json", "experiments/manifests/lexical_reader_v2/lexical-profile-table.attempt01.json",
        "experiments/manifests/lexical_reader_v2/generated-pool-qualification.attempt02.json")}
    start = time.perf_counter()
    generated, identity, natural, reader = prepare()
    with (OUT / "natural-accepted.jsonl").open("w") as stream:
        for row in [*identity, *natural]:
            stream.write(json.dumps(row, sort_keys=True) + "\n")
    lookup = {row["variant_id"]: row for row in [*generated, *identity, *natural]}
    fingerprints = {key: row_hash(value) for key, value in lookup.items()}
    write(OUT / "preflight.json", {"head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "code_data_identities": identities, "accepted_generated_sha256": sha(POOL),
        "accepted_natural_sha256": sha(OUT / "natural-accepted.jsonl"), "reader_version": READER_VERSION,
        "seed": 42, "phase_absolute_ends": PHASE_ENDS, "update_target": 32768,
        "scope": "FULL_10M_ACCOUNTING_DRY_RUN_NO_NEURAL_EXECUTION", "six_probe_slots_consumed": 0})
    counts, exposure, phase_channels, phase_exposure = Counter(), Counter(), Counter(), Counter()
    phase_max = {phase: max(row["canonical_charge"] for row in [*identity, *natural, *generated]
        if "cell" not in row or phase == "P2" or row["cell"] != 3) for phase in ("P0", "P1", "P2")}
    sources, source_channels, variants, bases, bundles = Counter(), defaultdict(set), Counter(), Counter(), Counter()
    record_counts, group_counts, edits = defaultdict(Counter), defaultdict(Counter), Counter()
    repairs = Counter()
    updates, windows = [], []
    window_start, window_counts, window_segments = 0, Counter(), Counter()
    max_window_discrepancy, max_update_discrepancy = 0, 0
    with (OUT / "presentations.jsonl").open("w") as ledger:
        while reader.exposure < PHASE_ENDS[-1]:
            queued = reader.queue()
            update_channels, update_segments = Counter(), Counter()
            for presentation in queued:
                row = presentation["row"]
                phase, channel, charge = presentation["phase"], presentation["channel"], presentation["canonical_charge"]
                frozen = {key: value for key, value in presentation.items() if key != "row"}
                frozen.update({key: row[key] for key in ("source_sha256", "target_sha256", "anchor_sha256")})
                frozen["accepted_row_sha256"] = fingerprints[row["variant_id"]]
                ledger.write(json.dumps(frozen, sort_keys=True) + "\n")
                labels = [f"channel/{channel}", f"phase/{phase}", f"view/{row['view']}"]
                if "category" in row:
                    labels.extend(("category/" + row["category"], f"cell/{row['cell']}",
                        f"stratum/{phase}/{channel}/{row['category']}/{row['cell']}/{row['view']}"))
                    bases[row["base_id"]] += 1
                    bundles[row["typed_bundle_id"]] += 1
                for label in labels:
                    counts[label] += 1
                    exposure[label] += charge
                phase_channels[(phase, channel)] += charge
                phase_exposure[phase] += charge
                update_channels[channel] += charge
                update_segments[phase] += charge
                window_counts[channel] += charge
                window_segments[phase] += charge
                sources[row["source_sha256"]] += 1
                source_channels[row["source_sha256"]].add(channel)
                variants[row["variant_id"]] += 1
                for equal, label in ((row["source_equals_target"], "source_equals_target"),
                                      (row["lexical_source_equals_target"], "lexical_source_equals_target")):
                    if equal:
                        repairs[label + "_presentations"] += 1
                        repairs[label + "_exposure"] += charge
                if not row["source_equals_target"]:
                    repairs["byte_repair_required_presentations"] += 1
                    repairs["byte_repair_required_exposure"] += charge
                if not row["lexical_source_equals_target"]:
                    repairs["lexical_repair_required_presentations"] += 1
                    repairs["lexical_repair_required_exposure"] += charge
                if "record_id" in row:
                    record_counts[channel][row["record_id"]] += 1
                    group_counts[channel][row["source_group_id"]] += 1
                if channel == "empirical":
                    if row["lexical_source_equals_target"] or lexical(row["source"]) == lexical(row["anchor"]):
                        raise ValueError("accepted empirical lexical-neutral row: scientific stop")
                    for operation in row["operations"]:
                        edits[tuple(operation["key"])] += charge
                if presentation["end_exposure"] - window_start >= 1_000_000:
                    span = presentation["end_exposure"] - window_start
                    bound = 3 * sum(phase_max[segment] for segment in window_segments)
                    discrepancy = {name: window_counts[name] - weight * span
                        for name, weight in (("identity_minimal", .3), ("rules", .2), ("natural", .1), ("empirical", .4))}
                    if any(abs(value) > bound + 1e-8 for value in discrepancy.values()):
                        raise ValueError("scheduler 1M-window bound failed")
                    max_window_discrepancy = max(max_window_discrepancy, *map(abs, discrepancy.values()))
                    windows.append({"start": window_start, "end": presentation["end_exposure"],
                        "phase_segments": dict(window_segments), "charges": dict(window_counts),
                        "discrepancies": discrepancy, "bound": bound})
                    window_start, window_counts, window_segments = presentation["end_exposure"], Counter(), Counter()
            total = sum(presentation["canonical_charge"] for presentation in queued)
            discrepancy = {name: update_channels[name] - weight * total for name, weight in (
                ("identity_minimal", .3), ("rules", .2), ("natural", .1), ("empirical", .4))}
            bound = 3 * sum(phase_max[segment] for segment in update_segments)
            if any(abs(value) > bound + 1e-8 for value in discrepancy.values()):
                raise ValueError("scheduler complete-update window bound failed")
            max_update_discrepancy = max(max_update_discrepancy, *map(abs, discrepancy.values()))
            updates.append({"update": len(updates), "first_ordinal": queued[0]["ordinal"], "last_ordinal": queued[-1]["ordinal"],
                "start_exposure": queued[0]["start_exposure"], "end_exposure": reader.exposure,
                "canonical_charge": total, "overshoot": total - 32768, "examples": len(queued),
                "phase_segments": dict(update_segments), "channel_charges": dict(update_channels),
                "discrepancies": discrepancy, "bound": bound,
                "B_denominator": sum(presentation["row"]["native_target_positions"] for presentation in queued),
                "C_denominators": {name: sum(presentation["row"]["C_denominators"][name] for presentation in queued)
                    for name in ("action", "start", "end", "vocabulary")}})
            if len(updates) % 50 == 0:
                print(json.dumps({"updates": len(updates), "presentations": reader.presentation,
                    "canonical_exposure": reader.exposure, "elapsed_seconds": time.perf_counter() - start}), flush=True)
    phase_discrepancies = {}
    for phase, total in phase_exposure.items():
        phase_discrepancies[phase] = {}
        for channel, weight in (("identity_minimal", .3), ("rules", .2), ("natural", .1), ("empirical", .4)):
            value = phase_channels[(phase, channel)] - weight * total
            if not -(2 + weight) * phase_max[phase] - 1e-8 <= value <= (1 - weight) * phase_max[phase] + 1e-8:
                raise ValueError("scheduler phase discrepancy bound failed")
            phase_discrepancies[phase][channel] = value
    alarm = concentration_alarms(edits.items())
    stop = alarm["entry_strict_majority"] or alarm["separator_strict_majority"]
    if max(record_counts["natural"].values()) > 19:
        raise ValueError("approved natural-channel 19-use bound failed")
    write(OUT / "reader-final-state.json", reader.state())
    update_index = SAFE / f"mixed-reader-update-index.{tag}.json"
    write(update_index, updates)
    write(OUT / "one-million-windows.json", windows)
    summary = {"status": "FRONTIER_MODEL_REVIEW_REQUIRED" if stop else "READER_DRY_RUN_QUALIFIED_NATIVE_CONSUMPTION_PENDING",
        "scientific_stop_triggered": stop, "presentations": reader.presentation, "canonical_exposure": reader.exposure,
        "nominal_exposure": 10_000_000, "final_complete_update_overshoot": reader.exposure - 10_000_000,
        "complete_updates": len(updates), "counts": dict(counts), "canonical_charges": dict(exposure),
        "whole_reader_equality_repair": dict(repairs), "phase_exposure": dict(phase_exposure),
        "phase_max_admitted_charge": phase_max, "phase_discrepancies": phase_discrepancies,
        "max_complete_update_window_discrepancy": max_update_discrepancy,
        "max_1M_window_discrepancy": max_window_discrepancy, "realized_edit_concentration": alarm,
        "realized_edit_weights": [{"key": list(key), "canonical_charge_weight": weight} for key, weight in sorted(edits.items())],
        "unique_generated_bases": len(bases), "unique_variants": len(variants), "unique_typed_bundles": len(bundles),
        "variant_use_distribution": dict(Counter(variants.values())), "base_use_distribution": dict(Counter(bases.values())),
        "duplicate_source_presentations": sum(count - 1 for count in sources.values()),
        "duplicate_source_use_distribution": dict(Counter(sources.values())),
        "cross_channel_source_count": sum(len(channels) > 1 for channels in source_channels.values()),
        "cross_channel_source_channel_sets": dict(Counter("/".join(sorted(channels)) for channels in source_channels.values() if len(channels) > 1)),
        "natural_record_use_distribution": {channel: dict(Counter(values.values())) for channel, values in record_counts.items()},
        "natural_group_uses": {channel: dict(values) for channel, values in group_counts.items()},
        "ledger_sha256": sha(OUT / "presentations.jsonl"), "reader_state_sha256": sha(OUT / "reader-final-state.json"),
        "update_index_sha256": sha(update_index),
        "accepted_pool_sha256": sha(POOL), "accepted_natural_sha256": sha(OUT / "natural-accepted.jsonl"),
        "code_data_identities": identities, "wall_seconds": time.perf_counter() - start,
        "neural_execution": "NONE", "six_probe_slots_consumed": 0}
    write(SAFE / f"mixed-reader-dry-run.{tag}.json", summary)
    print(json.dumps({key: summary[key] for key in ("status", "presentations", "canonical_exposure", "complete_updates", "realized_edit_concentration", "wall_seconds")}), flush=True)


if __name__ == "__main__":
    main()
