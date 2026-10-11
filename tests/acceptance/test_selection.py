"""NONSCIENTIFIC threshold grid and complete-population evidence."""
from dataclasses import replace
import pytest
from src.acceptance.selection import select_threshold
from src.acceptance.records import SelectRecord
from .fixtures import selection_rows, synthetic_isolation
from .independent_oracles import independent_select


@pytest.mark.parametrize("form",["STRUCTURAL","PRIMARY"])
@pytest.mark.parametrize("score,threshold", [(5.,4.),(4.,2.),(2.,1.),(1.,.5),(.5,.25),(.25,0.),(0.,None)])
def test_strict_thresholds_largest_tie_and_oracle(form,score,threshold):
    result=select_threshold(selection_rows(score),form)
    assert result.threshold==threshold==independent_select(selection_rows(score))
    assert tuple(e.threshold for e in result.evidence)==(0.,.25,.5,1.,2.,4.,None)


def test_ineligible_failed_cases_remain_in_denominators():
    rows=selection_rows()+ (SelectRecord("invented-failed","invented",100.,7,0,7,0,False),)
    result=select_threshold(rows,"PRIMARY")
    e=result.evidence[-2]
    assert e.population==206 and e.raw_errors==17 and e.output_errors==7
    assert e.repairs==10 and len(e.accepted_cases)==5


@pytest.mark.parametrize("zero_count,passes",[(199,False),(200,True),(201,True)])
def test_point_five_percent_boundary(zero_count,passes):
    rows=selection_rows(zero_count=zero_count)
    rows=tuple(replace(r,predicted_utility=5.,proposal_errors=1,introduced_error_upper=1,
        eligible_proposal=True) if r.case_id=="invented-zero-0" else r for r in rows)
    result=select_threshold(rows,"PRIMARY")
    assert (result.threshold is not None)==passes
    assert result.threshold==independent_select(rows)


def test_support_lower_bound_groups_and_introduction_bound():
    rows=selection_rows()
    assert select_threshold(tuple(replace(r,group="one") for r in rows),"PRIMARY").threshold is None
    assert select_threshold(tuple(replace(r,completed_repair_lower=1) if r.raw_errors else r for r in rows),"PRIMARY").threshold is None
    for intro,eligible in ((2,True),(3,False)):
        altered=(replace(rows[0],introduced_error_upper=intro),)+rows[1:]
        assert (select_threshold(altered,"PRIMARY").threshold is not None)==eligible


def test_output_errors_strictly_less_than_raw():
    rows=tuple(replace(r,proposal_errors=r.raw_errors) for r in selection_rows())
    assert select_threshold(rows,"STRUCTURAL").status=="SELECTION_FAILURE"


def test_zero_and_undefined_denominator_blocks():
    for rows in ((),selection_rows(zero_count=0)):
        result=select_threshold(rows,"PRIMARY")
        assert result.status=="UNRESOLVED" and result.threshold is None
        assert all("undefined_lexical_zero_denominator" in e.failure_reasons for e in result.evidence)


def test_duplicate_cases_rejected():
    rows=selection_rows()
    with pytest.raises(ValueError): select_threshold(rows+(rows[0],),"PRIMARY")

def test_inclusive_one_quarter_boundary_exact():
    # Five groups, 12 conservative repairs and exactly 3 introductions.
    rows=selection_rows()
    changed=(replace(rows[0],completed_repair_lower=4,introduced_error_upper=3),)+rows[1:]
    assert select_threshold(changed,"PRIMARY").threshold==4.
    changed=(replace(changed[0],introduced_error_upper=4),)+changed[1:]
    assert select_threshold(changed,"PRIMARY").threshold is None
