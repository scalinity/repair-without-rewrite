from collections import Counter
import inspect
import json
from pathlib import Path

import pytest

from src.generation import stress
from src.generation.lexical_v2 import (
    SourceOnlyUnionInverse, empirical_proposal, generated_bases, grammar_for_base,
    lexical_effect, positions, qualify_empirical_variant, rule_views, spoken_field,
    values_for_number, written_spoken_field,
)


@pytest.fixture(scope="module")
def table():
    root = Path(__file__).resolve().parents[2]
    return json.loads((root / "experiments/manifests/lexical_reader_v2/lexical-profile-table.attempt01.json").read_text())


@pytest.fixture(scope="module")
def bases():
    return generated_bases()


@pytest.mark.parametrize("kind,value,expected", [
    ("signed_decimal", "-1100.05", "minus one one zero zero point zero five"),
    ("version", "1.1100.0-rc1", "one dot one one zero zero dot zero hyphen r c one"),
    ("path", "/trainstem/a_10.bin", "slash t r a i n s t e m slash a underscore one zero dot b i n"),
    ("identifier", "trainstem_10", "t r a i n s t e m underscore one zero"),
    ("quantity", "1100 ms", "one one zero zero milliseconds"),
    ("quantity", "1 kg", "one kilograms"),
    ("integer", "001", "zero zero one"),
    ("negation", "never", "never"),
    ("negation", "", ""),
])
def test_exact_renderer_roundtrip_and_phi_invariant(kind, value, expected):
    from src.data.lexical_corruption_v2 import phi
    assert spoken_field(value, kind) == expected
    assert phi(expected) == expected
    assert written_spoken_field(expected, kind) == value


def test_spoken_inverse_does_not_normalize_or_guess():
    assert written_spoken_field("one  zero", "integer") is None
    assert written_spoken_field("One zero", "integer") is None
    assert written_spoken_field("one zer", "integer") is None
    assert written_spoken_field("one", "negation") is None


def test_manifest_is_exact_finite_constructor_domain_and_deduplicates_negation(bases, monkeypatch):
    assert len(bases) == 8404
    assert len({base["base_id"] for base in bases}) == 8404
    assert Counter(base["category"] for base in bases)["negation"] == 4
    assert len({base["typed_bundle_id"] for base in bases if base["category"] == "negation"}) == 1
    for number in (100, 399):
        monkeypatch.setattr(stress, "bounded_integer", lambda *args, **kwargs: number - 100)
        for grammar in stress.GRAMMARS:
            if grammar.partition == "train":
                assert values_for_number(grammar, number) == stress._values(grammar, "fixture")
    with pytest.raises(ValueError, match="TRAIN"):
        values_for_number(next(grammar for grammar in stress.GRAMMARS if grammar.partition == "dev"), 100)


def test_applicability_and_k1_sampling_are_deterministic(table, bases):
    assert positions("aab", {"key": ["deletion", "a", ""]}) == (0, 1)
    assert positions("ab", {"key": ["insertion", "", "e"]}) == (0, 1, 2)
    base = bases[0]
    first = empirical_proposal(base, 1, table, 0)
    assert first == empirical_proposal(base, 1, table, 0)
    source, operations = first
    assert len(operations) == 1
    grammar = grammar_for_base(base)
    original = grammar.parse(base["anchor"])
    changed = grammar.parse(source)
    assert sum(before != after for before, after in zip(original, changed)) == 1
    with pytest.raises(ValueError, match="severity"):
        empirical_proposal(base, 0, table, 0)


def test_k2_uses_distinct_fields_and_only_supported_class_pairs(table, bases):
    from src.data.lexical_corruption_v2 import OPERATION_CODES
    supported = {pair["class_pair"] for pair in table["class_pairs"] if pair["supported"]}
    for ordinal in range(20):
        _, operations = empirical_proposal(bases[0], 2, table, ordinal)
        assert {operation["field"] for operation in operations} == {0, 1}
        pair = "".join(sorted((OPERATION_CODES[operation["key"][0]] for operation in operations), key="SDI".index))
        assert pair in supported
        assert pair != "SS"


def test_bad_phi_fields_have_no_empirical_applicability(table, bases):
    base = {**bases[0], "spoken_fields": ("One", "Two")}
    assert empirical_proposal(base, 1, table, 0) is None
    assert empirical_proposal(base, 2, table, 0) is None


def test_lexical_effect_rejects_surface_noise_and_arrival_at_target(bases):
    base = next(base for base in bases if base["category"] == "negation")
    assert not lexical_effect(base, base["anchor"] + " ", [{"before": "never", "after": "never "}])
    assert not lexical_effect(base, base["target"], [{"before": "never", "after": "ne ver"}])


def test_fifty_proposal_exhaustion_and_no_rule_fallback(bases):
    empty = {"entries": [], "class_pairs": []}
    accepted, audit = qualify_empirical_variant(bases[0], 1, empty, SourceOnlyUnionInverse(empty))
    assert accepted is None
    assert len(audit) == 50
    assert all(row["reason"] == "no_applicable_supported_operations" for row in audit)


def test_common_capacity_rejection_uses_same_fifty_proposal_bound(table, bases):
    accepted, audit = qualify_empirical_variant(
        bases[0], 1, table, SourceOnlyUnionInverse(table), eligible=lambda source: False)
    assert accepted is None
    assert len(audit) == 50
    assert any(row["reason"] == "common_capacity_failed" for row in audit)
    assert all(row["reason"] != "accepted" for row in audit)


def test_source_only_union_qualifies_every_category_sample(table, bases):
    inverse = SourceOnlyUnionInverse(table)
    seen = set()
    for base in bases:
        if base["category"] in seen:
            continue
        seen.add(base["category"])
        for source, _ in rule_views(base).values():
            assert inverse(source).unique_target == base["target"]
        for severity in (1, 2):
            accepted, audit = qualify_empirical_variant(base, severity, table, inverse)
            assert accepted is not None
            assert len(audit) <= 50
            assert lexical_effect(base, accepted["source"], accepted["operations"])
            assert inverse(accepted["source"]).unique_target == base["target"]
            assert inverse(accepted["source"], state_cap=1).status == "capped"
    assert seen == set(stress.CATEGORIES)
    assert tuple(inspect.signature(inverse).parameters) == ("source", "state_cap")


def test_inverse_considers_public_values_outside_generated_train_manifest(table, bases):
    base = next(base for base in bases if base["category"] == "paths")
    grammar = grammar_for_base(base)
    # Arbitrary alphabetic substitution can remain a valid zero-error spoken
    # preimage. Both alternatives must survive; TRAIN inventory is not an oracle.
    target_a = grammar.render(("/trainstem/a.bin", "/trainstem/a.bin"))
    source = grammar.render((spoken_field("/trainstem/e.bin", "path"), spoken_field("/trainstem/a.bin", "path")))
    result = SourceOnlyUnionInverse(table)(source)
    assert result.status == "ambiguous"
    assert target_a in result.candidates
    assert grammar.render(("/trainstem/e.bin", "/trainstem/a.bin")) in result.candidates


def test_core_union_does_not_invent_two_operations_in_one_field(table, bases):
    base = next(base for base in bases if base["category"] == "signs_numerical")
    grammar = grammar_for_base(base)
    source = grammar.render((base["written_fields"][0].replace("1", "l"), base["written_fields"][1]))
    assert SourceOnlyUnionInverse(table)(source).status == "no_inverse"


def test_repeated_literal_relation_is_checked_after_complete_candidate_count(table, bases):
    base = next(base for base in bases if base["category"] == "repeated_literals")
    grammar = grammar_for_base(base)
    source = grammar.render(("1100", "1101"))
    result = SourceOnlyUnionInverse(table)(source)
    assert result.status == "no_inverse"
    assert result.examined_states >= 2


def test_rejected_class_pair_is_counted_before_state_cap(table, bases):
    base = next(base for base in bases if base["category"] == "repeated_literals")
    grammar = grammar_for_base(base)
    source = grammar.render(("ona", "oni"))
    result = SourceOnlyUnionInverse(table)(source)
    assert result.status == "no_inverse"
    assert result.examined_states == 2
    assert SourceOnlyUnionInverse(table)(source, state_cap=1).status == "capped"


def test_off_manifest_class_rejected_combinations_can_exceed_existing_bound(table, bases):
    base = next(base for base in bases if base["category"] == "paths")
    grammar = grammar_for_base(base)
    field = spoken_field("/trainstem/eeeeeeeeeeeeee.bin", "path")
    result = SourceOnlyUnionInverse(table)(grammar.render((field, field)))
    assert result.status == "capped"
    assert result.examined_states == 842
