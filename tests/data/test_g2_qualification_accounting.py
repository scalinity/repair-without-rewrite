import hashlib
import json
import math
import random

import pytest
from benchmarks.g2_corpus_qualification import diagnostics
from benchmarks.g2_cost_projection import reserve_and_gate
from benchmarks.g2_admission_independent import assert_unstarted
from src.generation.stress import CATEGORIES


def test_diagnostics_select_from_train_and_actual_ledger_with_order_independent_hashes():
    natural = [dict(view="natural", record_id=f"{equal}/{i}",
        variant_id=f"natural/{equal}/{i}", lexical_source_equals_target=equal)
        for equal in (False, True) for i in range(100)]
    generated = [dict(base_id=f"{category}/{cell}/{i}", category=category, cell=cell,
        view=view, variant_id=f"{view}/{category}/{cell}/{i}")
        for category in CATEGORIES for cell in range(3) for i in range(3)
        for view in ("clean", "mixed")]
    ledger = [dict(variant_id=row["variant_id"]) for row in generated
        if row["base_id"].endswith(("/1", "/2"))]
    chosen = diagnostics("D1", natural, generated, ledger)
    assert len(chosen) == len({row["id"] for row in chosen}) == 304
    for equal, stratum in ((False, "natural_lexical_error"), (True, "natural_lexical_zero")):
        def digest(row):
            payload = ["G2", 42, "D1", stratum, row["record_id"]]
            return hashlib.sha256(json.dumps(payload, ensure_ascii=False,
                separators=(",", ":")).encode()).hexdigest()
        expected = sorted((row for row in natural if row["lexical_source_equals_target"] == equal), key=digest)[:64]
        assert [row["id"] for row in chosen if row["stratum"] == stratum] == [row["variant_id"] for row in expected]
        assert [row["id"] for row in chosen if row["stratum"] == stratum + "/identity"] == ["identity/" + row["record_id"] for row in expected]
    assert all(not row["base_id"].endswith("/0") for row in chosen if "base_id" in row)
    random.Random(9).shuffle(natural); random.Random(11).shuffle(generated); ledger.reverse()
    assert diagnostics("D1", natural, generated, ledger) == chosen
    with pytest.raises(ValueError, match="no replacement"):
        diagnostics("D1", natural[:20], generated, ledger)


def test_cost_ceiling_charges_exactly_one_reserve_and_blocks_above_boundary():
    subtotal = 96 * 3600 / 1.25
    reserve, total, status = reserve_and_gate(subtotal)
    assert reserve == subtotal / 4 and total == 96 * 3600
    assert status == "PASS_G2_COST_CEILING_ONLY"
    assert reserve_and_gate(math.nextafter(subtotal, math.inf))[2] == "GENERATION_2_COST_BLOCKED"
    for invalid in (-1, math.nan, math.inf):
        with pytest.raises(ValueError):
            reserve_and_gate(invalid)


def test_all_seven_recipes_stay_unstarted_and_never_use_qualification_initializers(tmp_path):
    ids = [f"G2-{arm}-{data}-{condition}-seed42-lr3e-4"
        for data, condition in (("D0","U8"),("D1","U1"),("D1","U8"))
        for arm in ("B100","C101")]
    configs = [dict(recipe_id=recipe, status="AUTHORIZED_UNSTARTED",scientific_slot_consumed=False,
        qualification_initializers_forbidden=True,execution_requires_separate_owner_session=True)
        for recipe in [*ids,"G2-ByT5-D1-10pass-seed42-lr3e-4"]]
    area = tmp_path / "scientific-checkpoints-v1"
    assert assert_unstarted(configs,area)["scientific_slots_consumed"] == 0
    assert not area.exists()
    for field, value in (("status","RUNNING"),("scientific_slot_consumed",True),
                          ("qualification_initializers_forbidden",False)):
        changed = [dict(row) for row in configs]; changed[0][field] = value
        with pytest.raises(ValueError,match="boundary changed"):
            assert_unstarted(changed,area)
    with pytest.raises(ValueError,match="seven unique"):
        assert_unstarted(configs[:-1],area)
    area.mkdir(); (area / "partial-scientific.fixture").write_text("unqualified")
    with pytest.raises(ValueError,match="nonempty"):
        assert_unstarted(configs,area)
