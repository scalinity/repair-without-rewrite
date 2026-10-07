"""Frozen ten-pass accounting for G2; no model execution in this module."""
import random
from src.data.comparator_interfaces import byt5_ids

TRAIN_ROWS = 14113
PASSES = 10
BATCH = 4
PRESENTATIONS = 141130
UPDATES = 35283


def validate_pairs(rows):
    if len(rows) != TRAIN_ROWS or len({row["id"] for row in rows}) != TRAIN_ROWS:
        raise ValueError("ByT5 requires every unique D1 TRAIN pair")
    for row in rows:
        if row["role"] != "train" or row["status"] != "COMPLETED":
            raise ValueError("failed or non-TRAIN row cannot enter ByT5 fitting")
        # The inherited interface's 512 native positions include terminal EOS.
        byt5_ids(row["source"], qualified_capacity=512)
        byt5_ids(row["target"], qualified_capacity=512)


def training_batches(rows):
    validate_pairs(rows)
    order = list(range(TRAIN_ROWS))
    # Preserve the original comparator's one seed-42 shuffle and repeat its
    # complete order; only the approved corpus and ten-pass extent change.
    random.Random(42).shuffle(order)
    for start in range(0, PRESENTATIONS, BATCH):
        positions = range(start, min(start + BATCH, PRESENTATIONS))
        yield [{"row": rows[order[position % TRAIN_ROWS]], "pass_index": position // TRAIN_ROWS,
                "pass_offset": position % TRAIN_ROWS, "presentation": position} for position in positions]


def accounting_plan(rows):
    batches = list(training_batches(rows))
    per_pass = [0] * PASSES
    for batch in batches:
        for item in batch:
            per_pass[item["pass_index"]] += 1
    if len(batches) != UPDATES or per_pass != [TRAIN_ROWS] * PASSES or len(batches[-1]) != 2:
        raise ValueError("ten-pass whole-stream accounting mismatch")
    return {"training_rows": TRAIN_ROWS, "passes": PASSES, "presentations": PRESENTATIONS,
        "optimizer_updates": UPDATES, "batch_size": BATCH, "final_batch_size": 2,
        "per_pass_presentations": per_pass, "pass_boundary_flush": False,
        "ordering": "one random.Random(42) shuffle of frozen census order, reused for each complete pass",
        "first_batch_ids": [item["row"]["id"] for item in batches[0]],
        "last_batch_ids": [item["row"]["id"] for item in batches[-1]]}
