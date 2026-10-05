"""Development-only technical_latent_v1 constructor and source-only inverse.

Public grammar is a finite catalog. Core operators are typed 1/l, 0/O
confusion, field-specific separator verbalization, finite unit aliases and
polarity-preserving negation spelling. Arbitrary deletion/replacement is not
part of qualified_core_v1. All compatible catalog entries are considered.
"""
from dataclasses import dataclass, asdict
import hashlib
import json
import re
from pathlib import Path

PROTOCOL = "paper_protocol_v2_DEVELOPMENT_NOT_FROZEN"
CATEGORIES = ("signs_numerical", "negation", "versions", "paths", "identifiers",
              "units_quantities", "repeated_literals", "multiple_bindings")
SEEDS = {"manifest": 120012, "partition": 120101, "train": 120201, "dev": 120202,
         "corruption": 120301, "panel": 120501}
VIEWS = ("clean_preservation", "uniquely_recoverable_repair", "mixed_repair_preservation")
TYPE = {"signs_numerical": "signed_decimal", "negation": "negation",
        "versions": "version", "paths": "path", "identifiers": "identifier",
        "units_quantities": "quantity", "repeated_literals": "integer",
        "multiple_bindings": "quantity"}


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(text):
    return hashlib.sha256(text.encode("utf-8", errors="strict")).hexdigest()


def derived_bytes(purpose, seed, partition, family, group, view="", ordinal=0, counter=0):
    # JSON array, UTF-8 without normalization; big-endian digest integers.
    payload = [PROTOCOL, purpose, seed, partition, family, group, view, ordinal, counter]
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).digest()


def bounded_integer(bound, *, purpose, seed, partition, family, group, view="", ordinal=0):
    if bound <= 0:
        raise ValueError("positive bound required")
    limit = (1 << 256) - (1 << 256) % bound
    counter = 0
    while True:
        value = int.from_bytes(derived_bytes(purpose, seed, partition, family, group, view, ordinal, counter), "big")
        if value < limit:
            return value % bound
        counter += 1


@dataclass(frozen=True)
class Grammar:
    family_id: str
    partition: str
    category: str
    cell: int
    field_type: str
    scaffold: tuple[str, str, str]

    def render(self, values):
        return self.scaffold[0] + values[0] + self.scaffold[1] + values[1] + self.scaffold[2]

    def parse(self, text):
        # Captures can contain wrong or empty values. Delimiters cannot occur in
        # slots; complete consumption is required, and no preferred substring.
        pattern = re.escape(self.scaffold[0]) + r"([^;\n]*)" + re.escape(self.scaffold[1]) + r"([^;\n]*)" + re.escape(self.scaffold[2])
        match = re.fullmatch(pattern, text)
        if not match:
            return None
        return match.group(1), match.group(2)


def catalog():
    entries = []
    # Packs are assigned before values/views. Test entries are grammar only:
    # this module deliberately offers no final-test value-generation seed.
    for partition, prefix in (("train", "Exercise"), ("dev", "Calibration"), ("test", "Reserved")):
        for category in CATEGORIES:
            for cell in range(4):
                field_type = TYPE[category]
                label = field_type.replace("_", " ")
                leading = (f"{prefix} {category}: ", f"{prefix} {category} record. ",
                           f"{prefix} {category} context with two bound fields. ",
                           f"{prefix} {category} context. " + "Stable scaffold. "*8)[cell]
                # Four different complete scaffold forms and explicit bindings.
                first, second = (("Primary", "Backup"), ("Left", "Right"),
                                 ("Earlier", "Later"), ("Input", "Output"))[cell]
                entries.append(Grammar(f"{partition}/{category}/cell{cell}", partition, category, cell,
                                       field_type, (leading + f"{first} {label}: ",
                                                    f"; {second} {label}: ", ".")))
    return tuple(entries)


GRAMMARS = catalog()


def valid_surface(value, field_type, partition=None):
    patterns = {"signed_decimal": r"[+-][0-9]+\.[0-9]{2}", "negation": r"(?:not|never|no|)",
                "version": r"[0-9]+\.[0-9]+\.[0-9]+(?:-rc[0-9]+)?", "integer": r"[0-9]+",
                "quantity": r"[0-9]+ (?:ms|s|kg)",
                "path": r"/(?:trainstem|devstem|teststem)/[a-z0-9_]+\.bin",
                "identifier": r"(?:trainstem|devstem|teststem)_[0-9]+"}
    return re.fullmatch(patterns[field_type], value) is not None


def inverse_field(value, field_type):
    """Symbolically enumerate all inverse core operations, including identity.

    Each core operator's noncanonical alphabet is disjoint from canonical
    surfaces for its type. Compositions commute on disjoint character classes,
    so exhaustive operator subset closure proves the unique inverse here.
    """
    operators = []
    if field_type in ("signed_decimal", "version", "integer", "quantity"):
        operators.append(lambda x: x.replace("l", "1").replace("O", "0"))
    if field_type == "path":
        operators.append(lambda x: x.replace(" slash ", "/").replace(" dot ", "."))
    if field_type == "identifier":
        operators.append(lambda x: x.replace(" underscore ", "_"))
    if field_type == "quantity":
        operators.append(lambda x: x.replace(" milliseconds", " ms").replace(" seconds", " s").replace(" kilograms", " kg"))
    if field_type == "negation":
        operators.append(lambda x: {"n ot": "not", "ne ver": "never", "n o": "no"}.get(x, x))
    seen, frontier = {value}, [value]
    while frontier:
        current = frontier.pop(0)
        for operator in operators:
            candidate = operator(current)
            if candidate not in seen:
                seen.add(candidate); frontier.append(candidate)
    return tuple(sorted(x for x in seen if valid_surface(x, field_type)))


@dataclass(frozen=True)
class InverseResult:
    status: str
    candidates: tuple[str, ...]
    compatible_families: tuple[str, ...]
    examined_states: int

    @property
    def unique_target(self):
        return self.candidates[0] if self.status == "unique" else None


def inverse(source, *, state_cap=500, policy="qualified_core_v1"):
    """Accepts only source + public catalog, never latent metadata."""
    source.encode("utf-8", errors="strict")
    if policy not in ("qualified_core_v1", "underdetermined_diagnostic_v1"):
        raise ValueError("unknown public corruption policy")
    candidates, compatible, states = set(), [], 0
    for grammar in GRAMMARS:
        parsed = grammar.parse(source)
        if parsed is None:
            continue
        compatible.append(grammar.family_id)
        alternatives = [inverse_field(value, grammar.field_type) for value in parsed]
        if policy == "underdetermined_diagnostic_v1":
            for i,value in enumerate(parsed):
                if grammar.field_type == "signed_decimal" and re.fullmatch(r"[0-9]+\.[0-9]{2}",value):
                    alternatives[i] = ("+"+value,"-"+value)
                elif grammar.field_type == "negation" and value == "":
                    alternatives[i] = ("","not","never","no")
        left,right = alternatives
        states += 1 + len(left)*len(right)
        if states > state_cap:
            return InverseResult("capped", (), tuple(compatible), states)
        for a in left:
            for b in right:
                # Repetition is public structural relation, not latent hint.
                if grammar.category == "repeated_literals" and a != b:
                    continue
                candidates.add(grammar.render((a, b)))
    ordered = tuple(sorted(candidates))
    status = "unique" if len(ordered) == 1 else "ambiguous" if ordered else "no_inverse"
    return InverseResult(status, ordered, tuple(compatible), states)


def inverse_baseline(source):
    answer = inverse(source)
    return answer.unique_target if answer.status == "unique" else source


def corrupt(value, field_type):
    if field_type in ("signed_decimal", "version", "integer"):
        return value.replace("1", "l").replace("0", "O")
    if field_type == "path":
        return value.replace("/", " slash ").replace(".", " dot ")
    if field_type == "identifier":
        return value.replace("_", " underscore ")
    if field_type == "quantity":
        return value.replace("1", "l").replace("0", "O").replace(" ms", " milliseconds")
    return {"not": "n ot", "never": "ne ver", "no": "n o"}.get(value, value)


def _values(grammar, group):
    # Content domains are assigned with packs before values, not rescued by
    # partition-specific textual prefixes. Canonical typed bundles are disjoint.
    number = (100 if grammar.partition == "train" else 400) + bounded_integer(300, purpose="values", seed=SEEDS[grammar.partition],
                                  partition=grammar.partition, family=grammar.family_id, group=group)
    # The leading 1 guarantees a nonempty uniquely repairable transformation.
    a, b = "1" + str(number), "1" + str(number + 1)
    field_type = grammar.field_type
    if field_type == "signed_decimal": return (f"-{a}.05", f"+{b}.10")
    if field_type == "negation":
        return ("never", "never") if grammar.partition == "train" else ("not", "never" if number % 2 else "no")
    if field_type == "version": return (f"1.{a}.0", f"1.{b}.0-rc1")
    if field_type == "path": return (f"/{grammar.partition}stem/run_{a}.bin", f"/{grammar.partition}stem/run_{b}.bin")
    if field_type == "identifier": return (f"{grammar.partition}stem_{a}", f"{grammar.partition}stem_{b}")
    if field_type == "quantity": return (f"{a} ms", f"{b} ms")
    return (a, a)


def _canonical_value(value, field_type):
    if field_type == "signed_decimal":
        sign, magnitude = value[0], value[1:]
        integer, fraction = magnitude.split(".")
        return {"sign": sign, "coefficient": integer+fraction, "scale": len(fraction)}
    if field_type == "quantity":
        coefficient, unit = value.split(" ")
        return {"coefficient": coefficient, "scale": 0, "unit": unit}
    if field_type == "version":
        numeric, _, suffix = value.partition("-")
        return {"components": numeric.split("."), "prerelease": suffix or None}
    if field_type == "negation":
        return {"polarity": "affirmative" if not value else "negative", "surface": value}
    return value


def _spans(grammar, values):
    first_start = len(grammar.scaffold[0])
    second_start = first_start + len(values[0]) + len(grammar.scaffold[1])
    # ASCII owned grammar now; explicit conversion preserves interface for Unicode.
    text = grammar.render(values)
    codepoints = ((first_start, first_start + len(values[0])),
                  (second_start, second_start + len(values[1])))
    byte_spans = tuple((len(text[:a].encode("utf-8")), len(text[:b].encode("utf-8"))) for a, b in codepoints)
    return byte_spans, codepoints


def generate_group(category, cell, group_ordinal, *, partition="dev"):
    if partition not in ("dev", "train"):
        raise ValueError("final-test generation is not authorized by development tooling")
    grammar = next(g for g in GRAMMARS if (g.partition, g.category, g.cell) == (partition, category, cell))
    group = f"{grammar.family_id}/group{group_ordinal:04d}"
    values = _values(grammar, group)
    reference = grammar.render(values)
    reference_spans, reference_cp = _spans(grammar, values)
    records = []
    for view in VIEWS:
        changed = () if view == VIEWS[0] else (0, 1) if view == VIEWS[1] else (0,)
        source_values = tuple(corrupt(v, grammar.field_type) if i in changed else v for i, v in enumerate(values))
        source = grammar.render(source_values)
        qualification = inverse(source)
        if qualification.unique_target != reference:
            raise ValueError(f"unqualified proposal: {qualification.status}")
        source_spans, source_cp = _spans(grammar, source_values)
        operations, intermediate = [], list(values)
        for ordinal, i in enumerate(changed):
            before_text = grammar.render(intermediate)
            before_spans, _ = _spans(grammar, intermediate)
            intermediate[i] = source_values[i]
            after_text = grammar.render(intermediate)
            after_spans, _ = _spans(grammar, intermediate)
            operations.append({"operator_id": "qualified_core_v1", "field_id": f"slot{i+1}",
                               "before": values[i], "after": source_values[i],
                               "before_text": before_text, "after_text": after_text,
                               "before_byte_span": before_spans[i], "after_byte_span": after_spans[i],
                               "all_after_byte_spans": after_spans,
                               "parameters": {"field_type": grammar.field_type},
                               "seed_sha256": derived_bytes("corruption", SEEDS["corruption"], partition,
                                    grammar.family_id, group, view, ordinal).hex()})
        fields = [{"field_id": f"slot{i+1}", "occurrence_id": f"{group}/slot{i+1}",
                   "field_name": f"slot{i+1}", "field_type": grammar.field_type, "role": "payload",
                   "canonical_value": _canonical_value(value, grammar.field_type), "reference_surface": value, "surface_rendering": value,
                   "allowed_target_surfaces": [value], "source_span": source_spans[i],
                   "reference_span": reference_spans[i], "source_codepoint_span": source_cp[i],
                   "reference_codepoint_span": reference_cp[i], "coordinate_status": "present",
                   "initial_field_match": i not in changed, "preserve_required": i not in changed,
                   "repair_required": i in changed, "binding_id": f"slot{i+1}", "order": i,
                   "multiplicity": 1, "recoverability_class": "unique_public_inverse",
                   "recoverability_witness": "visible typed labels and qualified_core_v1",
                   "inverse_candidate_count": len(qualification.candidates)} for i, value in enumerate(values)]
        records.append({"schema_version": "technical_latent_v1", "population_id": "development_only",
                        "case_id": f"{group}/{view}", "base_group_id": group, "paired_view_id": group,
                        "partition": partition, "view_kind": view, "primary_category": category,
                        "secondary_categories": [], "template_id": grammar.family_id,
                        "template_family_id": grammar.family_id, "constructor_family_id": "typed_two_slot_v1",
                        "semantic_family_id": "equal_two_slots" if category == "repeated_literals" else "labeled_two_slots",
                        "lexical_family_ids": [f"{partition}stem"], "parent_ids": [],
                        "reference_utf8": reference, "source_utf8": source,
                        "reference_sha256": digest(reference), "source_sha256": digest(source),
                        "reference_byte_length": len(reference.encode("utf-8")), "source_byte_length": len(source.encode("utf-8")),
                        "scaffold": grammar.scaffold, "structural_grammar_version": "technical_structure_parser_v1_dev",
                        "target_language_version": "technical_target_language_v1_dev", "full_input_consumption": True,
                        "escaping_policy": "forbid_semicolon_newline_in_fields_v1", "fields": fields,
                        "relations": {"required_equal": category == "repeated_literals", "order": ["slot1", "slot2"]},
                        "operations": operations, "generation_seed": SEEDS[partition], "proposal_ordinal": 0,
                        "qualification_status": "unique_source_inverse", "rejection_reason": None,
                        "evaluation_membership": "development_conformance_only", "frozen": False,
                        "panel_selection_key": derived_bytes("panel", SEEDS["panel"], partition, grammar.family_id, group).hex(),
                        "configuration_id": PROTOCOL})
    return records


def score(record, output, *, complete=True):
    grammar = next(g for g in GRAMMARS if g.family_id == record["template_id"])
    parsed = None
    if isinstance(output, str):
        try:
            output.encode("utf-8", errors="strict")
            parsed = grammar.parse(output)
        except UnicodeError:
            pass
    success = [bool(parsed is not None and complete and parsed[i] in field["allowed_target_surfaces"])
               for i, field in enumerate(record["fields"])]
    preserve = [i for i, f in enumerate(record["fields"]) if f["preserve_required"]]
    repairs = [i for i, f in enumerate(record["fields"]) if f["repair_required"]]
    return {"structure_valid": parsed is not None, "complete": complete,
            "field_success": success, "preserved": sum(success[i] for i in preserve),
            "preserve_denominator": len(preserve), "repaired": sum(success[i] for i in repairs),
            "repair_denominator": len(repairs), "introduced_field_failures": sum(not success[i] for i in preserve),
            "whole_case_conformance": bool(complete and parsed is not None and all(success)),
            "all_source_correct_retained": all(success[i] for i in preserve) if preserve else None,
            "mixed_success": bool(complete and preserve and repairs and all(success))}


def select_development_panel(records, groups_per_cell):
    """Hash selection includes all views, row-order independent, never freeze."""
    cells = {}
    for record in records:
        if record["partition"] != "dev":
            raise ValueError("development panel accepts dev only")
        cell = (record["primary_category"], record["template_family_id"])
        cells.setdefault(cell, {})[record["base_group_id"]] = record["panel_selection_key"]
    selected = set()
    for groups in cells.values():
        if len(groups) < groups_per_cell:
            raise ValueError("cell quota exhausted")
        selected.update(sorted(groups, key=lambda g: (groups[g], g))[:groups_per_cell])
    return sorted((r for r in records if r["base_group_id"] in selected), key=lambda r: r["case_id"])


def typed_bundle_signature(record):
    # IDs and scaffold/partition prefixes cannot make repeated payloads unique.
    fields = [{key:field[key] for key in ("field_type","role","canonical_value","binding_id","order","multiplicity")}
              for field in record["fields"]]
    return digest(canonical_json({"fields":fields,"relations":record["relations"]}))


def validate_split_leakage(records):
    seen = {}
    for record in records:
        for kind, value in (("source", record["source_sha256"]), ("reference", record["reference_sha256"]),
                            ("family", record["template_family_id"]), ("latent", record["base_group_id"]),
                            ("typed_bundle",typed_bundle_signature(record)),
                            *( ("lexical_family",value) for value in record["lexical_family_ids"] ),
                            *( ("parent_lineage",value) for value in [record["case_id"],record["base_group_id"],*record["parent_ids"]] )):
            previous = seen.setdefault((kind, value), record["partition"])
            if previous != record["partition"]:
                raise ValueError(f"cross-partition {kind} leakage")


def generate_development_manifest(*, groups_per_cell=3, maximum_proposals=50):
    """Bounded slot construction with a retained rejection ledger."""
    if not 1 <= maximum_proposals <= 50 or groups_per_cell <= 0:
        raise ValueError("development construction bound is invalid")
    records, rejections = [], []
    for category in CATEGORIES:
        for cell in range(4):
            for slot in range(groups_per_cell):
                for proposal in range(maximum_proposals):
                    try:
                        group = generate_group(category,cell,slot*maximum_proposals+proposal)
                    except ValueError as error:
                        rejections.append({"category":category,"cell":cell,"slot":slot,
                                           "proposal":proposal,"reason":str(error)})
                        continue
                    generator_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
                    grammar_sha = digest(canonical_json([asdict(g) for g in GRAMMARS]))
                    configuration_sha = digest(canonical_json({"groups_per_cell":groups_per_cell,
                        "maximum_proposals":maximum_proposals,"protocol":PROTOCOL,"seeds":SEEDS}))
                    for record in group:
                        record["proposal_ordinal"] = proposal
                        record["generator_code_sha256"] = generator_sha
                        record["grammar_catalog_sha256"] = grammar_sha
                        record["configuration_sha256"] = configuration_sha
                        record["manifest_seed"] = SEEDS["manifest"]
                        record["partition_seed"] = SEEDS["partition"]
                        record["corruption_seed"] = SEEDS["corruption"]
                    records.extend(group)
                    break
                else:
                    return {"status":"quota_blocked","records":records,"rejections":rejections,
                            "blocked_cell":[category,cell],"blocked_slot":slot}
    return {"status":"development_complete_not_frozen","records":records,"rejections":rejections}
