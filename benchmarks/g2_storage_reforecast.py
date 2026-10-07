"""Reprice retained qualification and all future saves on the bound volume."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import time

from src.data.g2_artifacts import ArtifactRoot, read_complete, sha256


def retained_census(root, versioned_areas):
    files = defaultdict(lambda: dict(files=0, symlinks=0, logical_bytes=0, allocated_bytes=0))
    physical_root = root.resolve(strict=True)
    device = root.stat().st_dev
    for path in root.rglob("*"):
        area = path.relative_to(root).parts[0]
        if area not in versioned_areas:
            raise ValueError("retained artifact outside approved versioned areas")
        if path.is_symlink():
            target = path.resolve(strict=True)
            if not target.is_relative_to(physical_root) or target.stat().st_dev != device:
                raise ValueError("retained G2 artifact redirects outside physical accounting")
            # rglob does not descend directory aliases. Count the link payload
            # itself; the real target is already inventoried at its own path.
            stat = path.lstat()
            files[area]["symlinks"] += 1
        elif path.is_file():
            stat = path.stat()
            if stat.st_dev != device:
                raise ValueError("retained G2 artifact outside bound physical volume")
            files[area]["files"] += 1
        else:
            continue
        files[area]["logical_bytes"] += stat.st_size
        files[area]["allocated_bytes"] += stat.st_blocks * 512
    return dict(files)


def run(binding, attempt):
    root = ArtifactRoot(binding)
    before = root.preflight()
    started = time.perf_counter()
    receipt = Path(f"experiments/manifests/generation_2/storage-reforecast.attempt{attempt:02d}.json")
    if receipt.exists():
        raise FileExistsError(receipt)
    files = retained_census(root.root, root.policy["versioned_areas"])
    native = {}
    for arm in ("B100", "C101"):
        sizes = []
        metadata = []
        for data, condition in (("D0","U8"),("D1","U1"),("D1","U8")):
            name = f"{arm}-{data}-{condition}.attempt01"
            report = json.loads(Path(f"experiments/manifests/generation_2/bench-{name}.json").read_text())
            if report["status"] != "PASS_G2_NATIVE_BENCH_COLD_PENDING":
                raise ValueError("complete native checkpoint layout required")
            for relative in report["checkpoint_relatives"].values():
                path = root.path(relative)
                complete = read_complete(path)
                sizes.append(complete["files"]["arrays.npz"]["bytes"])
                metadata.append(complete["files"]["metadata.json"]["bytes"])
        native[arm] = dict(measured_max_array_bytes=max(sizes),
            measured_max_metadata_bytes=max(metadata),future_checkpoints=39,
            metadata_allowance_per_checkpoint=max(16*1024**2,max(metadata)))
        native[arm]["calculated_future_bytes"] = 39 * (max(sizes) + native[arm]["metadata_allowance_per_checkpoint"])
    by = json.loads(Path("experiments/manifests/generation_2/byt5-qualification.attempt02.json").read_text())
    if by["status"] != "PASS_G2_BYT5_RUNNER_100_UPDATES":
        raise ValueError("native ByT5 storage layout required")
    by_sizes = {}
    for label, key in (("initial","initial_checkpoint"),("trained","final_checkpoint")):
        path = root.path(by[key]["relative"])
        by_sizes[label] = read_complete(path)["files"]["state.pt"]["bytes"]
    by_sizes["calculated_future_bytes"] = by_sizes["initial"] + 3 * by_sizes["trained"] + 4 * 16 * 1024**2
    # Existing failures are already included in current free space and retained
    # census. This is an additional future failure reserve, not a subtraction.
    allowances = dict(additional_failed_attempt_reserve=32*1024**3,
        one_writer_atomic_transient=8*1024**3,future_evaluation_and_diagnostic_outputs=4*1024**3,
        future_presentation_and_consumption_logs=4*1024**3,future_private_logs_and_receipts=8*1024**3)
    remaining = sum(row["calculated_future_bytes"] for row in native.values()) + by_sizes["calculated_future_bytes"] + sum(allowances.values())
    after = root.preflight()
    free = min(before["literal_free_bytes"],after["literal_free_bytes"])
    high_water_free = free - remaining
    status = "PASS_G2_RETAINED_STORAGE_FORECAST" if high_water_free >= 250*1024**3 else "GENERATION_2_STORAGE_BLOCKED"
    result = dict(schema="g2_retained_storage_reforecast_v1",status=status,
        retained_by_area=dict(files),retained_logical_bytes=sum(x["logical_bytes"] for x in files.values()),
        retained_allocated_bytes=sum(x["allocated_bytes"] for x in files.values()),
        allocation_caveat="file allocation sums are not unique APFS physical blocks; actual statvfs free space is the capacity gate",
        measured_native_checkpoint_sizes=native,measured_byt5_checkpoint_sizes=by_sizes,
        assumed_future_allowances_bytes=allowances,calculated_remaining_conservative_bytes=remaining,
        literal_free_bytes_for_forecast=free,calculated_high_water_literal_free_bytes=high_water_free,
        minimum_literal_free_bytes=250*1024**3,all_current_failures_and_partials_retained=True,
        no_sparse_saving_assumed=True,scientific_recipes_started=0,before=before,after=after,
        code_sha256=sha256(__file__),elapsed_seconds=time.perf_counter()-started)
    receipt.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-binding",required=True)
    parser.add_argument("--attempt",type=int,required=True)
    args = parser.parse_args()
    result = run(args.artifact_binding,args.attempt)
    print(json.dumps({"status":result["status"],"high_water_free_GiB":result["calculated_high_water_literal_free_bytes"]/1024**3}),flush=True)
