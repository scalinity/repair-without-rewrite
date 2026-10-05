import copy
import itertools
import pytest
from src.generation.stress import (CATEGORIES, VIEWS, GRAMMARS, generate_group, inverse,
    inverse_baseline, score, select_development_panel, validate_split_leakage,
    bounded_integer, inverse_field, canonical_json)


def development():
    return [r for category in CATEGORIES for cell in range(4) for group in range(3)
            for r in generate_group(category,cell,group)]


def test_all_eight_categories_three_views_deterministic():
    records = development()
    assert len(records) == 288
    assert canonical_json(records) == canonical_json(development())
    for record in records:
        reference,source = record["reference_utf8"],record["source_utf8"]
        assert inverse(source).unique_target == reference
        assert inverse_baseline(source) == reference
        assert score(record,reference)["whole_case_conformance"]
        for field in record["fields"]:
            a,b = field["reference_span"]; c,d = field["source_span"]
            assert reference.encode()[a:b].decode() == field["reference_surface"]
            assert source.encode()[c:d].decode() == (record["operations"][int(field["order"])] ["after"] if record["view_kind"] == VIEWS[1] else field["reference_surface"] if not field["repair_required"] else record["operations"][0]["after"])
        if record["view_kind"] == VIEWS[2]:
            assert score(record,source)["repaired"] == 0
            assert score(record,source)["preserved"] == 1


def test_parser_distinguishes_wrong_field_from_invalid_structure():
    record = generate_group("multiple_bindings",0,0)[2]
    reference = record["reference_utf8"]
    wrong = reference.replace(record["fields"][1]["reference_surface"], "500 kg")
    result = score(record,wrong)
    assert result["structure_valid"] and result["field_success"] == [True,False]
    assert not result["mixed_success"] and result["introduced_field_failures"] == 1
    for invalid in ("Preface " + reference, reference + " Extra",reference[:-1],reference + reference,
                    reference.replace("Primary", "Backup",1), None,"\ud800"):
        result = score(record,invalid)
        assert not result["whole_case_conformance"] and result["field_success"] == [False,False]
    assert not score(record,reference,complete=False)["whole_case_conformance"]


def test_repeated_equal_occurrences_denominators():
    record = generate_group("repeated_literals",0,0)[0]
    text = record["reference_utf8"]
    assert record["fields"][0]["reference_surface"] == record["fields"][1]["reference_surface"]
    assert record["fields"][0]["occurrence_id"] != record["fields"][1]["occurrence_id"]
    assert score(record,text)["preserve_denominator"] == 2
    relabeled = copy.deepcopy(record)
    for i,field in enumerate(relabeled["fields"]): field["field_id"] = f"new{i}"
    assert score(record,text) == score(relabeled,text)
    assert not score(record,text.replace("; Backup integer: " + record["fields"][1]["reference_surface"],""))["whole_case_conformance"]


def test_split_leakage_and_panel_row_order():
    records = development()
    train = [r for c in CATEGORIES for r in generate_group(c,0,0,partition="train")]
    validate_split_leakage(records+train)
    panel = select_development_panel(records,1)
    assert len(panel) == 96 and panel == select_development_panel(list(reversed(records)),1)
    with pytest.raises(ValueError): select_development_panel(records,4)
    leak = copy.deepcopy(records[0]); leak["partition"] = "train"
    with pytest.raises(ValueError): validate_split_leakage([records[0],leak])
    with pytest.raises(ValueError): generate_group("negation",0,0,partition="test")


def test_source_only_inverse_rejects_uncued_damage_and_cap():
    record = generate_group("signs_numerical",0,0)[1]
    source = record["source_utf8"]
    assert inverse(source).status == "unique"
    assert inverse(source,state_cap=1).status == "capped"
    assert inverse(source.replace("-", "",1)).status == "no_inverse"
    negation = generate_group("negation",0,0)[1]
    # In the restricted core, an empty slot is a true affirmative. No lost-not
    # operator is allowed; a hidden negative target fails source-only agreement.
    erased = negation["source_utf8"].replace("n ot", "")
    assert inverse(erased).unique_target != negation["reference_utf8"]
    assert inverse("some unrestricted l8").status == "no_inverse"


def test_exhaustive_small_typed_confusion_and_compositions():
    for length in (1,2,3):
        for digits in itertools.product("01",repeat=length):
            clean = "".join(digits)
            for mask in itertools.product((False,True),repeat=length):
                source = "".join(("O" if x == "0" else "l") if changed else x for x,changed in zip(digits,mask))
                assert inverse_field(source,"integer") == (clean,)
                assert inverse_field(source+" milliseconds","quantity") == (clean+" ms",)
    values = [bounded_integer(7,purpose="values",seed=120202,partition="dev",family="x",group=str(i)) for i in range(1000)]
    assert set(values) == set(range(7))


def test_independent_exhaustive_full_parser_checker():
    grammar = next(g for g in GRAMMARS if g.family_id == "dev/identifiers/cell0")
    # Independent decomposition enumerates separator positions; regex code is
    # neither called nor duplicated by the reference checker.
    def reference_parse(text):
        prefix,middle,suffix = grammar.scaffold
        if not text.startswith(prefix) or not text.endswith(suffix): return None
        inner = text[len(prefix):len(text)-len(suffix)]
        choices = []
        for index in range(len(inner)+1):
            if inner[index:index+len(middle)] == middle:
                values = (inner[:index],inner[index+len(middle):])
                if not any(";" in x or "\n" in x for x in values): choices.append(values)
        return choices[0] if len(choices) == 1 else None
    for left,right in itertools.product(("","1","l","wrong",";","\n","é"),repeat=2):
        text = grammar.render((left,right))
        for candidate in (text,"extra"+text,text+"extra",text[:-1]):
            assert grammar.parse(candidate) == reference_parse(candidate)


def test_underdetermined_public_policy_rejects_lost_polarity():
    signed = generate_group("signs_numerical",0,0)[0]
    source = signed["reference_utf8"].replace("-", "",1)
    answer = inverse(source,policy="underdetermined_diagnostic_v1")
    assert answer.status == "ambiguous" and len(answer.candidates) == 2
    assert answer.unique_target is None
    assert signed["reference_utf8"] in answer.candidates
    negation = generate_group("negation",0,0)[0]
    source = negation["reference_utf8"].replace("not", "",1)
    answer = inverse(source,policy="underdetermined_diagnostic_v1")
    assert answer.status == "ambiguous" and len(answer.candidates) == 4


def test_exact_typed_values_near_confusables_bindings_and_empty_polarity():
    signed = generate_group("signs_numerical",0,0)[0]
    value = signed["fields"][0]["canonical_value"]
    assert value["sign"] == "-" and value["scale"] == 2
    assert value["coefficient"].isdigit()
    quantity = generate_group("units_quantities",0,0)[0]
    assert quantity["fields"][0]["canonical_value"]["unit"] == "ms"
    bindings = generate_group("multiple_bindings",0,0)[0]
    first,second = (f["reference_surface"] for f in bindings["fields"])
    grammar = next(g for g in GRAMMARS if g.family_id == bindings["template_id"])
    swapped = grammar.render((second,first))
    assert score(bindings,swapped)["field_success"] == [False,False]
    assert not score(bindings,grammar.render((first,second.replace("ms","s"))))["whole_case_conformance"]
    # A public empty negation slot is measurable; inserted polarity fails its
    # own empty finite form and the fixed preservation denominator.
    negation = generate_group("negation",0,0)[0]
    negation = copy.deepcopy(negation)
    grammar = next(g for g in GRAMMARS if g.family_id == negation["template_id"])
    second = negation["fields"][1]["reference_surface"]
    affirmative = grammar.render(("",second))
    negation["reference_utf8"] = negation["source_utf8"] = affirmative
    first_start = len(grammar.scaffold[0])
    second_start = first_start+len(grammar.scaffold[1])
    negation["fields"][0].update(canonical_value={"polarity":"affirmative","surface":""},
        reference_surface="",surface_rendering="",allowed_target_surfaces=[""],
        reference_span=(first_start,first_start),source_span=(first_start,first_start))
    negation["fields"][1].update(reference_span=(second_start,second_start+len(second)),
        source_span=(second_start,second_start+len(second)))
    assert score(negation,affirmative)["whole_case_conformance"]
    assert not score(negation,grammar.render(("not",second)))["whole_case_conformance"]


def test_bounded_proposals_retain_exhaustion(monkeypatch):
    from src.generation import stress
    def rejected(*args,**kwargs): raise ValueError("fixture source inverse nonunique")
    monkeypatch.setattr(stress,"generate_group",rejected)
    result = stress.generate_development_manifest(groups_per_cell=1,maximum_proposals=3)
    assert result["status"] == "quota_blocked" and len(result["rejections"]) == 3
    assert [r["proposal"] for r in result["rejections"]] == [0,1,2]
    with pytest.raises(ValueError):stress.generate_development_manifest(maximum_proposals=51)


def test_complete_typed_latent_bundle_cannot_cross_partitions():
    left = generate_group("negation",0,0,partition="dev")[0]
    right = copy.deepcopy(left)
    right.update(partition="train",template_family_id="train/other-pack",base_group_id="train/other-group",
                 source_sha256="different-source",reference_sha256="different-reference",lexical_family_ids=["trainstem"])
    with pytest.raises(ValueError,match="typed_bundle"):
        validate_split_leakage([left,right])


def test_lexical_and_parent_acoustic_lineage_cannot_cross_partitions():
    left = generate_group("paths",0,0,partition="dev")[0]
    right = generate_group("paths",0,0,partition="train")[0]
    validate_split_leakage([left,right])
    right["lexical_family_ids"] = left["lexical_family_ids"]
    with pytest.raises(ValueError,match="lexical_family"):validate_split_leakage([left,right])
    right["lexical_family_ids"] = ["trainstem"]
    right["parent_ids"] = [left["case_id"]]
    with pytest.raises(ValueError,match="parent_lineage"):validate_split_leakage([left,right])
