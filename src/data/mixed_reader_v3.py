"""Common raw-source native admission and approved canonical accounting."""
from dataclasses import asdict
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import math

from src.generation.stress import CATEGORIES, SEEDS, canonical_json

from src.models.edits import EditContractError, canonical_labels, events, render
from src.models.tokenizer import BOS, EOS, RESTORE_REFERENCE, SEP


def canonical_serialization(tokenizer, anchor, target):
    return [BOS, RESTORE_REFERENCE, SEP, *tokenizer.encode(anchor), SEP,
            *tokenizer.encode(target), EOS]


def native_shape(tokenizer, source, anchor, target):
    """One common admission; no arm-specific replacement or target truncation."""
    tokenized = tokenizer.source(source)
    source_ids = [BOS, RESTORE_REFERENCE, SEP, *tokenized.ids, EOS]
    target_ids = tokenizer.encode(target)
    anchor_ids = tokenizer.encode(anchor)
    if len(source_ids) > 1024 or len(anchor_ids) + 4 > 1024 or len(target_ids) + 1 > 1024:
        return None
    program = canonical_labels(source, target, tuple(tokenizer.byte_map[token] for token in tokenized.ids))
    if render(source, program) != target:
        raise ValueError("canonical C labels do not render the exact target")
    try:
        labels = events(program, tokenizer.encode, {offset: index for index, offset in enumerate(tokenized.byte_offsets)})
    except EditContractError as error:
        if str(error).startswith("decoder context overflow:"):
            return None
        raise
    canonical = [BOS, RESTORE_REFERENCE, SEP, *anchor_ids, SEP, *target_ids, EOS]
    if len(canonical) != len(anchor_ids) + len(target_ids) + 5:
        raise ValueError("canonical serialization charge mismatch")
    return {"source_ids": source_ids, "target_ids": target_ids,
        "encoder_positions": list(range(2, len(tokenized.ids) + 3)),
        "byte_offsets": list(tokenized.byte_offsets), "legal": list(tokenized.legal_pointer_mask),
        "gold_program": asdict(program), "gold_labels": asdict(labels),
        "canonical_charge": len(canonical), "canonical_sequence": canonical,
        "native_source_positions": len(source_ids), "native_target_positions": len(target_ids) + 1,
        "native_C_positions": len(labels.inputs), "C_denominators": labels.denominators,
        "anchor_bpe": len(anchor_ids), "target_bpe": len(target_ids)}


READER_VERSION = "frontier_reader_v1_lexical_corruption_v2"
PHASE_ENDS = (6_666_667, 9_333_334, 10_000_000)
UPDATE_TARGET = 32_768


def phase_at(exposure):
    return "P0" if exposure < PHASE_ENDS[0] else "P1" if exposure < PHASE_ENDS[1] else "P2"


def pilot_lr(endpoint, peak):
    if endpoint < 0 or peak not in (1e-4, 3e-4, 6e-4):
        raise ValueError("invalid approved pilot exposure or peak LR")
    endpoint = min(endpoint, PHASE_ENDS[-1])
    if endpoint <= 200_000:
        return peak * endpoint / 200_000
    return peak * (.1 + .45 * (1 + math.cos(math.pi * (endpoint - 200_000) / 9_800_000)))


def order_key(purpose, pool, pass_number, identifier):
    payload = [READER_VERSION, purpose, SEEDS["manifest"], 42, "train", pool,
               pass_number, identifier]
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).digest()


class CompletePass:
    def __init__(self, rows, pool, *, coverage_first=False):
        if not rows:
            raise ValueError(f"empty required pool: {pool}")
        self.rows = {row["variant_id"]: row for row in rows}
        if len(self.rows) != len(rows):
            raise ValueError("duplicate pool variant ID")
        self.pool, self.coverage_first = pool, coverage_first
        self.pass_number, self.offset, self.uses = 0, 0, Counter()
        self.order = self._order()

    def _order(self):
        key = lambda identifier: (order_key("record-pass", self.pool, self.pass_number, identifier), identifier)
        if not self.coverage_first:
            return sorted(self.rows, key=key)
        groups = defaultdict(list)
        for identifier, row in self.rows.items():
            groups[row["source_group_id"]].append(identifier)
        first, remaining = [], []
        for group in sorted(groups, key=lambda group: (
                order_key("group-pass", self.pool, self.pass_number, group), group)):
            ordered = sorted(groups[group], key=key)
            first.append(ordered[0])
            remaining.extend(ordered[1:])
        return first + sorted(remaining, key=key)

    def next(self):
        if self.offset == len(self.order):
            self.pass_number += 1
            self.offset = 0
            self.order = self._order()
        identifier = self.order[self.offset]
        self.offset += 1
        self.uses[identifier] += 1
        return self.rows[identifier]

    def state(self):
        return {"pool": self.pool, "pass": self.pass_number, "offset": self.offset,
                "uses": dict(self.uses)}

    def restore(self, state):
        if state["pool"] != self.pool or state["pass"] < 0 or not 0 <= state["offset"] <= len(self.rows):
            raise ValueError("complete-pass state mismatch")
        if set(state["uses"]) - self.rows.keys() or any(count < 0 for count in state["uses"].values()):
            raise ValueError("invalid complete-pass use counter")
        self.pass_number, self.offset = state["pass"], state["offset"]
        self.uses = Counter(state["uses"])
        self.order = self._order()


class DeficitNode:
    def __init__(self, children):
        self.children = tuple((name, Fraction(weight), child) for name, weight, child in children)
        if not self.children or any(weight <= 0 for _, weight, _ in self.children):
            raise ValueError("positive required child weights")
        self.weight_sum = sum(weight for _, weight, _ in self.children)
        self.total, self.charges = 0, Counter()

    def next(self):
        index = max(range(len(self.children)), key=lambda index: (
            self.children[index][1] * self.total / self.weight_sum
            - self.charges[self.children[index][0]], -index))
        name, _, child = self.children[index]
        row, path = (child.next(), []) if isinstance(child, CompletePass) else child.next()
        charge = row["canonical_charge"]
        self.total += charge
        self.charges[name] += charge
        return row, [name, *path]

    def state(self):
        return {"total": self.total, "charges": dict(self.charges), "children": {
            name: child.state() for name, _, child in self.children}}

    def restore(self, state):
        names = {name for name, _, _ in self.children}
        if set(state["children"]) != names or set(state["charges"]) - names:
            raise ValueError("deficit scheduler child mismatch")
        if any(charge < 0 for charge in state["charges"].values()) or sum(state["charges"].values()) != state["total"]:
            raise ValueError("deficit scheduler charge mismatch")
        self.total, self.charges = state["total"], Counter(state["charges"])
        for name, _, child in self.children:
            child.restore(state["children"][name])


class MixedReader:
    """Frozen shared examples; only phase counters reset, never leaf cursors."""
    def __init__(self, generated, identity, natural, severity_weights):
        self.generated = defaultdict(list)
        for row in generated:
            self.generated[(row["category"], row["cell"], row["view"])].append(row)
        self.identity, self.natural, self.severity_weights = identity, natural, severity_weights
        self.pools = {}
        self.phase, self.root = None, None
        self.exposure, self.presentation = 0, 0

    def _leaf(self, key, rows, *, natural=False):
        if key not in self.pools:
            self.pools[key] = CompletePass(rows, key, coverage_first=natural)
        return self.pools[key]

    def _generated(self, channel, phase):
        def cell_node(category, cell):
            views = (("mixed", 1),) if channel == "minimal" else (
                (("clean", 1), ("mixed", 4)) if phase == "P0" else
                (("clean", 1), ("mixed", 2), ("two", 2))) if channel == "rules" else (
                (("empirical1", 1),) if phase == "P0" else
                (("empirical1", self.severity_weights[1]), ("empirical2", self.severity_weights[2])))
            return DeficitNode([(view, weight, self._leaf(
                f"{channel}/{category}/{cell}/{view}", self.generated[(category, cell, view)]))
                for view, weight in views])
        categories = []
        for category in CATEGORIES:
            replay = DeficitNode([(str(cell), 1, cell_node(category, cell)) for cell in (0, 1, 2)])
            component = DeficitNode([("replay", 1, replay)]) if phase != "P2" else DeficitNode([
                ("replay", 1, replay), ("fresh", 1, DeficitNode([("3", 1, cell_node(category, 3))]))])
            categories.append((category, 1, component))
        return DeficitNode(categories)

    def _tree(self, phase):
        return DeficitNode([
            ("identity_minimal", 3, DeficitNode([
                ("identity", 1, self._leaf("identity/natural", self.identity, natural=True)),
                ("minimal", 1, self._generated("minimal", phase))])),
            ("rules", 2, self._generated("rules", phase)),
            ("natural", 1, self._leaf("real/natural", self.natural, natural=True)),
            ("empirical", 4, self._generated("empirical", phase))])

    def next(self):
        phase = phase_at(self.exposure)
        if phase != self.phase:
            self.phase, self.root = phase, self._tree(phase)
        row, path = self.root.next()
        presentation = {"presentation_id": f"seed42/{self.presentation:09d}", "ordinal": self.presentation,
            "phase": phase, "channel": path[0], "subpath": path[1:],
            "start_exposure": self.exposure, "end_exposure": self.exposure + row["canonical_charge"],
            "variant_id": row["variant_id"], "canonical_charge": row["canonical_charge"], "row": row}
        self.exposure = presentation["end_exposure"]
        self.presentation += 1
        return presentation

    def queue(self):
        queued, charge = [], 0
        while charge < UPDATE_TARGET:
            row = self.next()
            queued.append(row)
            charge += row["canonical_charge"]
        return queued

    def state(self):
        return {"phase": self.phase, "exposure": self.exposure, "presentation": self.presentation,
                "deficits": self.root.state() if self.root else None,
                "pools": {key: value.state() for key, value in self.pools.items()}}

    def restore(self, state):
        if state["exposure"] < 0 or state["presentation"] < 0 or state["phase"] not in (None, "P0", "P1", "P2"):
            raise ValueError("invalid reader resume cursor")
        self.exposure, self.presentation, self.phase = state["exposure"], state["presentation"], state["phase"]
        if self.phase is None:
            if self.exposure or self.presentation or state["pools"] or state["deficits"]:
                raise ValueError("invalid initial reader state")
            self.root, self.pools = None, {}
            return
        self.root = self._tree(self.phase)
        if set(self.pools) != set(state["pools"]):
            raise ValueError("reader resume pool inventory mismatch")
        self.root.restore(state["deficits"])
        if any(pool.state() != state["pools"][key] for key, pool in self.pools.items()):
            raise ValueError("reader leaf counter mismatch")
