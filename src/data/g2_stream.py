"""Versioned actual-update cursor over frozen whole-presentation master queues."""
from collections import Counter, defaultdict
import json

from src.data.g2_geometry import scientific_projection, split_master


class G2BenchStream:
    """The accepted G1 phase-deficit BENCH selector, with explicit U8 cursors."""
    def __init__(self, rows, ledger, updates, data_condition, update_condition):
        if data_condition not in {"D0", "D1"} or update_condition not in {"U1", "U8"}:
            raise ValueError("approved D/U condition required")
        self.rows, self.ledger, self.updates = rows, ledger, updates
        self.data_condition, self.update_condition = data_condition, update_condition
        self.pools = defaultdict(list)
        for index, update in enumerate(updates):
            dominant = max(("P0", "P1", "P2"), key=lambda phase: update["phase_segments"].get(phase, 0))
            self.pools[dominant].append(index)
        if any(not self.pools[phase] for phase in ("P0", "P1", "P2")):
            raise ValueError("all phase populations required for BENCH")
        self.cursor, self.phase_charges, self.selector_exposure = Counter(), Counter(), 0
        self.master_completed, self.master_committed_exposure, self.subqueue_index = 0, 0, 0
        self.master_queue_index, self.master = None, []
        self.weights = {"P0": 6666667, "P1": 2666667, "P2": 666666}

    def _queue(self, index):
        if type(index) is not int or not 0 <= index < len(self.updates):
            raise ValueError("G2 frozen master index outside the ledger")
        update = self.updates[index]
        master = [{**item, "row": self.rows[item["variant_id"]]}
            for item in self.ledger[update["first_ordinal"]:update["last_ordinal"] + 1]]
        charge = sum(item["canonical_charge"] for item in master)
        if (charge != update["canonical_charge"] or charge < 32768
                or charge - master[-1]["canonical_charge"] >= 32768):
            raise ValueError("immutable U1 whole-presentation master geometry mismatch")
        return master

    def actual_queue(self):
        if not self.master:
            phase = max(("P0", "P1", "P2"), key=lambda name: (
                self.weights[name] * self.selector_exposure - 10000000 * self.phase_charges[name],
                -("P0", "P1", "P2").index(name)))
            index = self.pools[phase][self.cursor[phase] % len(self.pools[phase])]
            self.master = self._queue(index)
            self.master_queue_index = index
            self.cursor[phase] += 1
            self.selector_exposure += self.updates[index]["canonical_charge"]
            self.phase_charges.update(self.updates[index]["phase_segments"])
        return split_master(self.master, self.update_condition)[self.subqueue_index]

    def finish_actual(self):
        if not self.master:
            raise ValueError("no active master update")
        self.subqueue_index += 1
        factor = 8 if self.update_condition == "U8" else 1
        if self.subqueue_index == factor:
            self.master_completed += 1
            self.master_committed_exposure += sum(item["canonical_charge"] for item in self.master)
            self.master_queue_index, self.master, self.subqueue_index = None, [], 0

    def state(self):
        return {"schema": "g2_bench_whole_master_cursor_v1", "scope": "QUALIFICATION_ONLY_NOT_SCIENTIFIC",
            "data_condition": self.data_condition, "update_condition": self.update_condition,
            "phase_pool_cursor": dict(self.cursor), "phase_charges": dict(self.phase_charges),
            "selector_exposure": self.selector_exposure, "master_completed": self.master_completed,
            "master_committed_exposure": self.master_committed_exposure,
            "master_queue_index": self.master_queue_index, "subqueue_index": self.subqueue_index,
            "master_presentations": scientific_projection(self.master)}

    def restore(self, state):
        if (state["schema"] != "g2_bench_whole_master_cursor_v1"
                or state["scope"] != "QUALIFICATION_ONLY_NOT_SCIENTIFIC"
                or state["data_condition"] != self.data_condition
                or state["update_condition"] != self.update_condition):
            raise ValueError("G2 reader condition/scope mismatch")
        self.cursor = Counter(state["phase_pool_cursor"])
        self.phase_charges = Counter(state["phase_charges"])
        for key in ("selector_exposure", "master_completed", "master_committed_exposure", "subqueue_index"):
            if type(state[key]) is not int or state[key] < 0:
                raise ValueError("G2 reader integer clock required")
            setattr(self, key, state[key])
        if set(self.cursor) - set(self.weights) or set(self.phase_charges) - set(self.weights):
            raise ValueError("G2 reader phase inventory mismatch")
        if any(type(value) is not int or value < 0 for value in [*self.cursor.values(), *self.phase_charges.values()]):
            raise ValueError("G2 reader phase clock required")
        self.master_queue_index = state["master_queue_index"]
        self.master = [] if self.master_queue_index is None else self._queue(self.master_queue_index)
        if scientific_projection(self.master) != state["master_presentations"]:
            raise ValueError("G2 reader pending master differs from immutable ledger")
        if self.master:
            if self.subqueue_index >= (8 if self.update_condition == "U8" else 1):
                raise ValueError("G2 reader subqueue cursor overflow")
        elif self.subqueue_index:
            raise ValueError("G2 reader has subqueue without a pending master")
        expected_selector = self.master_committed_exposure + sum(item["canonical_charge"] for item in self.master)
        if self.selector_exposure != expected_selector or sum(self.phase_charges.values()) != expected_selector:
            raise ValueError("G2 reader selector/exposure accounting mismatch")
        if sum(self.cursor.values()) != self.master_completed + bool(self.master):
            raise ValueError("G2 reader completed/pending master count mismatch")

    def completed_actual_clock(self):
        factor = 8 if self.update_condition == "U8" else 1
        exposure = self.master_committed_exposure
        if self.master:
            exposure += sum(item["canonical_charge"] for part in split_master(
                self.master, self.update_condition)[:self.subqueue_index] for item in part)
        return self.master_completed * factor + self.subqueue_index, exposure


def canonical_cursor(state):
    return json.dumps(state, sort_keys=True, separators=(",", ":"), allow_nan=False)


class G2ScientificStream(G2BenchStream):
    """Sequential frozen master cursor; qualification snapshots cannot initialize it."""
    def actual_queue(self):
        if not self.master:
            if self.master_completed == len(self.updates):
                raise StopIteration("all frozen scientific masters completed")
            self.master_queue_index = self.master_completed
            self.master = self._queue(self.master_queue_index)
        return split_master(self.master, self.update_condition)[self.subqueue_index]

    def state(self):
        return {"schema": "g2_scientific_whole_master_cursor_v1",
            "scope": "FROZEN_SEQUENTIAL_SCIENTIFIC_STREAM", "data_condition": self.data_condition,
            "update_condition": self.update_condition, "master_completed": self.master_completed,
            "master_committed_exposure": self.master_committed_exposure,
            "master_queue_index": self.master_queue_index, "subqueue_index": self.subqueue_index,
            "master_presentations": scientific_projection(self.master)}

    def restore(self, state):
        if (state["schema"] != "g2_scientific_whole_master_cursor_v1"
                or state["scope"] != "FROZEN_SEQUENTIAL_SCIENTIFIC_STREAM"
                or state["data_condition"] != self.data_condition
                or state["update_condition"] != self.update_condition):
            raise ValueError("scientific cursor requires its own frozen scope; BENCH initializers forbidden")
        for key in ("master_completed", "master_committed_exposure", "subqueue_index"):
            value = state[key]
            if type(value) is not int or value < 0:
                raise ValueError("scientific integer cursor required")
            setattr(self, key, value)
        if self.master_completed > len(self.updates):
            raise ValueError("scientific master cursor exceeds frozen endpoint")
        expected = sum(item["canonical_charge"] for item in self.updates[:self.master_completed])
        if expected != self.master_committed_exposure:
            raise ValueError("scientific exposure differs from frozen completed masters")
        self.master_queue_index = state["master_queue_index"]
        self.master = [] if self.master_queue_index is None else self._queue(self.master_queue_index)
        if self.master and self.master_queue_index != self.master_completed:
            raise ValueError("scientific pending master is not the next frozen master")
        if scientific_projection(self.master) != state["master_presentations"]:
            raise ValueError("scientific pending master projection changed")
        if (self.master and self.subqueue_index >= (8 if self.update_condition == "U8" else 1)
                or not self.master and self.subqueue_index):
            raise ValueError("scientific subqueue cursor outside pending master")
