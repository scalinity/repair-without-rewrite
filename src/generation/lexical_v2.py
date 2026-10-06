"""Frozen v1 generated domain and approved v2 field corruption/inverse.

The inverse sees the source and public grammar/profile only. It never consumes
the finite TRAIN base manifest, a chosen target, or a forward operation trace.
"""
from dataclasses import dataclass
from itertools import product
import hashlib
import re

from src.data.lexical_corruption_v2 import OPERATION_CODES, PROFILE_VERSION, phi
from src.generation.stress import CATEGORIES, GRAMMARS, SEEDS, canonical_json, valid_surface
from src.scoring.text import lexical


RENDERER_VERSION = "technical_spoken_renderer_v1"
DIGITS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
READ_DIGIT = dict(zip("0123456789", DIGITS))
WRITE_DIGIT = dict(zip(DIGITS, "0123456789"))
SYMBOLS = {"/": "slash", ".": "dot", "_": "underscore", "-": "hyphen"}
WRITE_SYMBOL = {value: key for key, value in SYMBOLS.items()}
UNITS = {"ms": "milliseconds", "s": "seconds", "kg": "kilograms"}
WRITE_UNIT = {value: key for key, value in UNITS.items()}
NEGATION_RULES = {"not": "n ot", "never": "ne ver", "no": "n o"}


def digest(text):
    return hashlib.sha256(text.encode("utf-8", "strict")).hexdigest()


def draw(bound, purpose, *context):
    if bound <= 0:
        raise ValueError("positive sampling bound required")
    limit = (1 << 256) - (1 << 256) % bound
    counter = 0
    while True:
        payload = [PROFILE_VERSION, purpose, SEEDS["corruption"], "train", *context, counter]
        number = int.from_bytes(hashlib.sha256(canonical_json(payload).encode()).digest(), "big")
        if number < limit:
            return number % bound
        counter += 1


def weighted(items, weights, purpose, *context):
    if len(items) != len(weights) or not items or any(weight <= 0 for weight in weights):
        raise ValueError("positive applicable weights required")
    selected = draw(sum(weights), purpose, *context)
    for item, weight in zip(items, weights):
        if selected < weight:
            return item
        selected -= weight
    raise AssertionError("weighted draw exhausted")


def spoken_field(value, field_type):
    if not valid_surface(value, field_type):
        raise ValueError("invalid public written field")
    digits = lambda text: [READ_DIGIT[char] for char in text]
    if field_type == "signed_decimal":
        integer, fraction = value[1:].split(".")
        words = [{"+": "plus", "-": "minus"}[value[0]], *digits(integer), "point", *digits(fraction)]
    elif field_type == "version":
        number, separator, suffix = value.partition("-")
        words = []
        for index, component in enumerate(number.split(".")):
            if index:
                words.append("dot")
            words.extend(digits(component))
        if separator:
            words.append("hyphen")
            words.extend(READ_DIGIT.get(char, char) for char in suffix)
    elif field_type in ("path", "identifier"):
        words = [READ_DIGIT.get(char, SYMBOLS.get(char, char)) for char in value]
    elif field_type == "quantity":
        coefficient, unit = value.split(" ")
        words = [*digits(coefficient), UNITS[unit]]
    elif field_type == "integer":
        words = digits(value)
    elif field_type == "negation":
        return value
    else:
        raise ValueError("unknown field type")
    return " ".join(words)


def written_spoken_field(text, field_type):
    """Exact public spoken grammar, with roundtrip enforcement; no normalization."""
    words = text.split(" ")
    try:
        if field_type == "negation":
            value = text
        elif field_type == "signed_decimal":
            point = words.index("point")
            sign = {"plus": "+", "minus": "-"}[words[0]]
            value = sign + "".join(WRITE_DIGIT[word] for word in words[1:point]) + "."
            value += "".join(WRITE_DIGIT[word] for word in words[point + 1:])
        elif field_type == "version":
            if "hyphen" in words:
                split = words.index("hyphen")
                numeric, suffix = words[:split], words[split + 1:]
            else:
                numeric, suffix = words, []
            value = "".join("." if word == "dot" else WRITE_DIGIT[word] for word in numeric)
            if suffix:
                value += "-" + "".join(WRITE_DIGIT[word] if word in WRITE_DIGIT else word for word in suffix)
        elif field_type in ("path", "identifier"):
            value = "".join(WRITE_DIGIT[word] if word in WRITE_DIGIT else
                            WRITE_SYMBOL[word] if word in WRITE_SYMBOL else
                            word if len(word) == 1 and "a" <= word <= "z" else
                            "\x00" for word in words)
        elif field_type == "quantity":
            value = "".join(WRITE_DIGIT[word] for word in words[:-1]) + " " + WRITE_UNIT[words[-1]]
        elif field_type == "integer":
            value = "".join(WRITE_DIGIT[word] for word in words)
        else:
            raise ValueError("unknown field type")
        if valid_surface(value, field_type) and spoken_field(value, field_type) == text:
            return value
    except (KeyError, ValueError, IndexError):
        pass
    return None


def values_for_number(grammar, number):
    """Exact existing TRAIN constructor formulas with its finite number draw exposed."""
    if grammar.partition != "train" or not 100 <= number <= 399:
        raise ValueError("only approved TRAIN number domain may be materialized")
    a, b = "1" + str(number), "1" + str(number + 1)
    kind = grammar.field_type
    if kind == "signed_decimal":
        return (f"-{a}.05", f"+{b}.10")
    if kind == "negation":
        return ("never", "never")
    if kind == "version":
        return (f"1.{a}.0", f"1.{b}.0-rc1")
    if kind == "path":
        return (f"/trainstem/run_{a}.bin", f"/trainstem/run_{b}.bin")
    if kind == "identifier":
        return (f"trainstem_{a}", f"trainstem_{b}")
    if kind == "quantity":
        return (f"{a} ms", f"{b} ms")
    return (a, a)


def generated_bases():
    bases = []
    for grammar in GRAMMARS:
        if grammar.partition != "train":
            continue
        distinct = {}
        for number in range(100, 400):
            values = values_for_number(grammar, number)
            target = grammar.render(values)
            distinct.setdefault(target, values)
        for target, values in sorted(distinct.items()):
            rendered = tuple(spoken_field(value, grammar.field_type) for value in values)
            if any(phi(field) != field for field in rendered):
                raise ValueError("rendered field violates Phi equality; construction ineligible")
            bases.append({"base_id": grammar.family_id + "/target/" + digest(target),
                "family_id": grammar.family_id, "category": grammar.category, "cell": grammar.cell,
                "field_type": grammar.field_type, "written_fields": values,
                "spoken_fields": rendered, "target": target, "anchor": grammar.render(rendered),
                "typed_bundle_id": digest(canonical_json([grammar.field_type, values]))})
    return bases


def grammar_for_base(base):
    return next(grammar for grammar in GRAMMARS if grammar.family_id == base["family_id"])


def positions(field, entry):
    operation, reference, _ = entry["key"]
    if operation == "insertion":
        return tuple(range(len(field) + 1))
    if operation not in ("substitution", "deletion") or len(reference) != 1:
        raise ValueError("invalid supported elementary entry")
    return tuple(index for index, char in enumerate(field) if char == reference)


def apply_entry(field, entry, position):
    operation, reference, hypothesis = entry["key"]
    if position not in positions(field, entry):
        raise ValueError("entry is not applicable at position")
    if operation == "insertion":
        if reference != "" or len(hypothesis) != 1:
            raise ValueError("invalid insertion")
        return field[:position] + hypothesis + field[position:]
    if operation == "deletion":
        if hypothesis != "":
            raise ValueError("invalid deletion")
        return field[:position] + field[position + 1:]
    if len(hypothesis) != 1 or reference == hypothesis:
        raise ValueError("invalid substitution")
    return field[:position] + hypothesis + field[position + 1:]


def rule_operations(field, field_type):
    proposals = []
    mappings = []
    if field_type in ("signed_decimal", "version", "integer", "quantity"):
        mappings.extend((("1", "l"), ("0", "O")))
    if field_type == "path":
        mappings.extend((("/", " slash "), (".", " dot ")))
    if field_type == "identifier":
        mappings.append(("_", " underscore "))
    for before, after in mappings:
        for index, char in enumerate(field):
            if char == before:
                proposals.append({"before": field, "after": field[:index] + after + field[index + 1:],
                                  "position": index, "reference": before, "hypothesis": after})
    if field_type == "quantity":
        coefficient, unit = field.split(" ")
        proposals.append({"before": field, "after": coefficient + " " + UNITS[unit],
                          "position": len(coefficient) + 1, "reference": unit, "hypothesis": UNITS[unit]})
    if field_type == "negation" and field in NEGATION_RULES:
        proposals.append({"before": field, "after": NEGATION_RULES[field], "position": 0,
                          "reference": field, "hypothesis": NEGATION_RULES[field]})
    return proposals


def rule_views(base):
    grammar = grammar_for_base(base)
    fields = base["written_fields"]
    choices = [(index, operation) for index, field in enumerate(fields)
               for operation in rule_operations(field, grammar.field_type)]
    if not choices:
        raise ValueError("required minimal rule variant unavailable")
    field, operation = choices[draw(len(choices), "minimal-operation", base["family_id"], base["base_id"])]
    changed = list(fields)
    changed[field] = operation["after"]
    mixed = grammar.render(changed)
    other = 1 - field
    candidates = rule_operations(fields[other], grammar.field_type)
    if not candidates:
        raise ValueError("required two-field rule variant unavailable")
    second = candidates[draw(len(candidates), "two-rule-operation", base["family_id"], base["base_id"])]
    changed[other] = second["after"]
    return {"clean": (base["target"], ()),
            "mixed": (mixed, ({**operation, "field": field},)),
            "two": (grammar.render(changed), ({**operation, "field": field}, {**second, "field": other}))}


def empirical_proposal(base, severity, table, ordinal):
    fields = base["spoken_fields"]
    entries = [entry for entry in table["entries"] if entry["supported"] and entry["weight"] > 0]
    applicable = [[entry for entry in entries if positions(field, entry)] if phi(field) == field else []
                  for field in fields]
    context = (base["family_id"], base["base_id"], severity, ordinal)
    if severity == 1:
        eligible = [index for index, choices in enumerate(applicable) if choices]
        if not eligible:
            return None
        assignments = [(eligible[draw(len(eligible), "empirical-field", *context)], None)]
    elif severity == 2:
        feasible = []
        for pair in table["class_pairs"]:
            if not pair["supported"] or not pair["weight"]:
                continue
            classes = pair["class_pair"]
            orientations = sorted(set((classes, classes[::-1])))
            orientations = [orientation for orientation in orientations if all(any(
                OPERATION_CODES[entry["key"][0]] == orientation[index] for entry in applicable[index])
                for index in (0, 1))]
            if orientations:
                feasible.append((pair, orientations))
        if not feasible:
            return None
        pair, orientations = weighted(feasible, [item[0]["weight"] for item in feasible], "empirical-class-pair", *context)
        orientation = orientations[draw(len(orientations), "empirical-field-assignment", *context)]
        assignments = [(index, orientation[index]) for index in (0, 1)]
    else:
        raise ValueError("v2 empirical channel permits severity 1 or 2 only")
    changed, operations = list(fields), []
    for operation_ordinal, (field, operation_class) in enumerate(assignments):
        choices = [entry for entry in applicable[field] if operation_class is None or
                   OPERATION_CODES[entry["key"][0]] == operation_class]
        entry = weighted(choices, [entry["weight"] for entry in choices], "empirical-entry", *context, operation_ordinal)
        locations = positions(fields[field], entry)
        position = locations[draw(len(locations), "empirical-position", *context, operation_ordinal)]
        changed[field] = apply_entry(fields[field], entry, position)
        operations.append({"field": field, "position": position, "key": entry["key"],
                           "before": fields[field], "after": changed[field]})
    return grammar_for_base(base).render(changed), tuple(operations)


def lexical_effect(base, source, operations):
    return (all(lexical(operation["before"]) != lexical(operation["after"]) for operation in operations)
            and lexical(source) != lexical(base["anchor"])
            and lexical(source) != lexical(base["target"]))


def _core_field_preimages(source, field_type):
    zero = {source} if valid_surface(source, field_type) else set()
    one = set()
    reverse = []
    if field_type in ("signed_decimal", "version", "integer", "quantity"):
        reverse.extend((("l", "1"), ("O", "0")))
    if field_type == "path":
        reverse.extend(((" slash ", "/"), (" dot ", ".")))
    if field_type == "identifier":
        reverse.append((" underscore ", "_"))
    if field_type == "quantity":
        reverse.extend((" " + spoken, " " + written) for written, spoken in UNITS.items())
    if field_type == "negation":
        reverse.extend((after, before) for before, after in NEGATION_RULES.items())
    for before, after in reverse:
        for match in re.finditer(re.escape(before), source):
            candidate = source[:match.start()] + after + source[match.end():]
            if not valid_surface(candidate, field_type):
                continue
            if any(operation["after"] == source for operation in rule_operations(candidate, field_type)):
                one.add(candidate)
    return zero, one


class SourceOnlyUnionInverse:
    def __init__(self, table):
        self.entries = tuple(tuple(entry["key"]) for entry in table["entries"]
                             if entry["supported"] and entry["weight"] > 0)
        self.class_pairs = {pair["class_pair"] for pair in table["class_pairs"]
                            if pair["supported"] and pair["weight"] > 0}
        self._field_cache = {}

    def _spoken_preimages(self, source, field_type):
        cache_key = (source, field_type)
        if cache_key in self._field_cache:
            return self._field_cache[cache_key]
        value = written_spoken_field(source, field_type)
        zero = {value} if value is not None and phi(source) == source else set()
        one = {}
        source_lexical = lexical(source)
        for operation, reference, hypothesis in self.entries:
            if operation == "deletion":
                candidates = (source[:index] + reference + source[index:] for index in range(len(source) + 1))
            else:
                candidates = (source[:index] + reference + source[index + 1:]
                              for index, char in enumerate(source) if char == hypothesis)
            for candidate in candidates:
                value = written_spoken_field(candidate, field_type)
                if value is None or phi(candidate) != candidate or lexical(candidate) == source_lexical:
                    continue
                one.setdefault(value, set()).add(OPERATION_CODES[operation])
        result = (zero, one)
        self._field_cache[cache_key] = result
        return result

    def __call__(self, source, *, state_cap=500):
        source.encode("utf-8", "strict")
        candidates, compatible, states = set(), [], 0
        for grammar in GRAMMARS:
            fields = grammar.parse(source)
            if fields is None:
                continue
            compatible.append(grammar.family_id)
            core = [_core_field_preimages(field, grammar.field_type) for field in fields]
            spoken = [self._spoken_preimages(field, grammar.field_type) for field in fields]
            pairs = []
            for left_severity, right_severity in ((0, 0), (1, 0), (0, 1), (1, 1)):
                pairs.extend(product(core[0][left_severity], core[1][right_severity]))
            pairs.extend(product(spoken[0][0], spoken[1][0]))
            pairs.extend(product(spoken[0][1], spoken[1][0]))
            pairs.extend(product(spoken[0][0], spoken[1][1]))
            rejected_class_pairs = 0
            for left, right in product(spoken[0][1], spoken[1][1]):
                if any("".join(sorted((a, b), key="SDI".index)) in self.class_pairs
                       for a in spoken[0][1][left] for b in spoken[1][1][right]):
                    pairs.append((left, right))
                else:
                    rejected_class_pairs += 1
            # Preserve the existing inverse's state convention: a compatible
            # grammar plus every complete candidate field tuple examined.
            states += 1 + len(pairs) + rejected_class_pairs
            if states > state_cap:
                return UnionInverseResult("capped", (), tuple(compatible), states)
            for left, right in sorted(pairs):
                if grammar.category == "repeated_literals" and left != right:
                    continue
                candidates.add(grammar.render((left, right)))
        ordered = tuple(sorted(candidates))
        status = "unique" if len(ordered) == 1 else "ambiguous" if ordered else "no_inverse"
        return UnionInverseResult(status, ordered, tuple(compatible), states)


@dataclass(frozen=True)
class UnionInverseResult:
    status: str
    candidates: tuple
    compatible_families: tuple
    examined_states: int

    @property
    def unique_target(self):
        return self.candidates[0] if self.status == "unique" else None


def qualify_empirical_variant(base, severity, table, inverse, *, state_cap=500, eligible=None):
    if severity not in (1, 2):
        raise ValueError("no zero empirical severity in v2")
    audit = []
    for ordinal in range(50):
        proposal = empirical_proposal(base, severity, table, ordinal)
        if proposal is None:
            audit.append({"proposal": ordinal, "reason": "no_applicable_supported_operations"})
            continue
        source, operations = proposal
        record = {"proposal": ordinal, "source": source, "operations": operations}
        if not lexical_effect(base, source, operations):
            audit.append({**record, "reason": "lexical_effect_failed"})
            continue
        result = inverse(source, state_cap=state_cap)
        record.update(inverse_status=result.status, examined_states=result.examined_states,
                      inverse_candidates=result.candidates)
        if result.unique_target != base["target"]:
            audit.append({**record, "reason": result.status if result.status != "unique" else "target_disagreement"})
            continue
        if eligible is not None and not eligible(source):
            audit.append({**record, "reason": "common_capacity_failed"})
            continue
        audit.append({**record, "reason": "accepted"})
        return {"source": source, "operations": operations, "severity": severity,
                "examined_states": result.examined_states}, audit
    return None, audit
