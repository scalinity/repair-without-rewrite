"""Descriptive paired source-group bootstrap; never an eligibility rule."""
import hashlib


def paired_group_intervals(group_ids, numerator_denominator_by_arm):
    import numpy as np
    groups = sorted(group_ids)
    if len(groups) != 52 or len(set(groups)) != 52:
        raise ValueError("all 52 frozen natural DEVELOPMENT groups required")
    if not numerator_denominator_by_arm:
        raise ValueError("nonempty paired comparison required")
    draws = np.random.Generator(np.random.PCG64(42)).integers(0, 52, size=(10000, 52))
    intervals = {}
    samples = {}
    for name, by_group in numerator_denominator_by_arm.items():
        if set(by_group) != set(groups):
            raise ValueError("paired arms must include the same complete groups")
        values = np.asarray([by_group[group] for group in groups], dtype=np.float64)
        if (values.shape != (52, 2) or not np.isfinite(values).all() or (values < 0).any()
                or values[:, 1].sum() <= 0):
            raise ValueError("finite nonnegative group totals with a positive population denominator required")
        totals = values[draws].sum(axis=1)
        if (totals[:, 1] <= 0).any():
            raise ValueError("fixed bootstrap draw has an undefined denominator; no redraw or exclusion")
        samples[name] = totals[:, 0] / totals[:, 1]
        intervals[name] = np.percentile(samples[name], [2.5, 97.5]).tolist()
    names = list(samples)
    paired_differences = {a + " minus " + b: np.percentile(samples[a] - samples[b],
        [2.5, 97.5]).tolist() for index, a in enumerate(names) for b in names[index + 1:]}
    return {"draws": 10000, "groups": 52, "seed": 42, "generator": "PCG64",
        "draw_indices_int64_sha256": hashlib.sha256(draws.astype("<i8").tobytes()).hexdigest(),
        "percentiles": [2.5, 97.5], "group_order": groups, "intervals": intervals,
        "paired_difference_intervals": paired_differences,
        "all_cases_in_each_selected_group": True, "eligibility_affected": False,
        "scorer_alignment_bounds_are_separate": True}
