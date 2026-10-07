"""Whole-presentation G2 boundaries; the inherited U1 reader stays unchanged."""
import hashlib
import json

from src.data.mixed_reader_v3 import pilot_lr


def split_master(queue, condition):
    if condition not in {"U1", "U8"} or not queue:
        raise ValueError("nonempty U1/U8 master required")
    charges = [row["canonical_charge"] for row in queue]
    if any(type(value) is not int or value <= 0 for value in charges):
        raise ValueError("whole presentations require positive integer charges")
    if condition == "U1":
        return [queue]
    total = sum(charges)
    cumulative, cuts = 0, []
    for index, charge in enumerate(charges, 1):
        cumulative += charge
        while len(cuts) < 7 and 8 * cumulative >= (len(cuts) + 1) * total:
            cuts.append(index)
    boundaries = [0, *cuts, len(queue)]
    if len(boundaries) != 9 or any(a >= b for a, b in zip(boundaries, boundaries[1:])):
        raise ValueError("approved U8 geometry cannot yield eight nonempty subqueues")
    return [queue[a:b] for a, b in zip(boundaries, boundaries[1:])]


def actual_denominators(queue):
    """Compute each actual update's denominators directly from its labels."""
    if not queue:
        raise ValueError("empty actual update")
    rows = [presentation["row"] for presentation in queue]
    return {"B": sum(len(row["target_ids"]) + 1 for row in rows),
            "C": {name: sum(row["C_denominators"][name] for row in rows)
                  for name in ("action", "start", "end", "vocabulary")}}


def g2_lr(completed_actual_exposure):
    if type(completed_actual_exposure) is not int or completed_actual_exposure <= 0:
        raise ValueError("completed actual-update exposure required")
    return pilot_lr(completed_actual_exposure, 3e-4)


def scientific_projection(queue):
    fields = ("presentation_id", "ordinal", "phase", "channel", "subpath",
              "start_exposure", "end_exposure", "variant_id", "canonical_charge")
    result = []
    for row in queue:
        projected = {name: row[name] for name in fields}
        for name in ("source_sha256", "target_sha256", "anchor_sha256", "accepted_row_sha256"):
            if name in row:
                projected[name] = row[name]
        result.append(projected)
    return result


def projection_hash(queue):
    digest = hashlib.sha256()
    for row in scientific_projection(queue):
        digest.update((json.dumps(row, sort_keys=True, separators=(",", ":"),
                                  ensure_ascii=False) + "\n").encode("utf-8"))
    return digest.hexdigest()
