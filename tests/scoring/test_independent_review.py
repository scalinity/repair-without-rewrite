"""Independent review: complete path lists, occurrence sets and frozen subsets.

No production distance, lattice, traceback, or existing oracle is used to derive
expected values. The small domain is deliberately separate from natural data.
"""
import itertools
import pytest

from src.scoring.triple import Limits, lattice, score_tokens, source_masks
from src.scoring.records import Output, aggregate, equal_domain_aggregate, prepare_source, score_output


def pair_paths(x, y):
    paths = []
    def visit(i, j, cols):
        if i == len(x) and j == len(y):
            paths.append(cols); return
        if i < len(x): visit(i + 1, j, cols + [(i, None, j)])
        if j < len(y): visit(i, j + 1, cols + [(None, j, i)])
        if i < len(x) and j < len(y): visit(i + 1, j + 1, cols + [(i, j, i)])
    visit(0, 0, [])
    costs = [sum((None if a is None else x[a]) != (None if b is None else y[b])
                 for a, b, _ in p) for p in paths]
    best = min(costs)
    return best, [p for p, c in zip(paths, costs) if c == best]


def independent_masks(r, s):
    _, paths = pair_paths(r, s)
    ref, src = [set() for _ in r], [set() for _ in s]
    gap_lists = [set() for _ in range(len(r) + 1)]
    for path in paths:
        gaps = [[] for _ in gap_lists]
        for i, j, gap in path:
            if i is not None: ref[i].add(j)
            if j is not None:
                src[j].add(('reference', i) if i is not None else ('gap', gap))
                if i is None: gaps[gap].append(j)
        for index, values in enumerate(gaps): gap_lists[index].add(tuple(values))
    labels = []
    for i, values in enumerate(ref):
        correctness = [j is not None and r[i] == s[j] for j in values]
        labels.append('certain_correct' if len(values) == 1 and all(correctness)
                      else 'certain_error' if not any(correctness) else 'ambiguous')
    return ref, src, labels, [next(iter(v)) if len(v) == 1 else None for v in gap_lists], paths


def independent_triple(r, s, o):
    es, _ = pair_paths(r, s); eo, _ = pair_paths(r, o)
    _, src, labels, _, _ = independent_masks(r, s)
    all_paths = []
    def visit(i, j, k, columns):
        if (i, j, k) == (len(r), len(s), len(o)):
            all_paths.append(columns); return
        available = [tuple(range(i, len(r)))[:1], tuple(range(j, len(s)))[:1],
                     tuple(range(k, len(o)))[:1]]
        for flags in itertools.product((False, True), repeat=3):
            if not any(flags) or any(f and not v for f, v in zip(flags, available)): continue
            indices = tuple(p if f else None for p, f in zip((i, j, k), flags))
            visit(i + flags[0], j + flags[1], k + flags[2], columns + [(indices, i)])
    visit(0, 0, 0, [])
    summaries = []
    for columns in all_paths:
        rs = ro = so = repair = introduced = damage = fixed_repair = 0
        events = [set() for _ in s]
        for (i, j, k), gap in columns:
            rv = None if i is None else r[i]
            sv = None if j is None else s[j]
            ov = None if k is None else o[k]
            se, oe = rv != sv, rv != ov
            rs += se; ro += oe; so += sv != ov
            rep, intro = se and not oe, oe and not se
            repair += rep; introduced += intro
            if i is not None and labels[i] == 'certain_correct': damage += intro
            if rep and ((i is not None and labels[i] == 'certain_error') or
                        (i is None and j is not None and len(src[j]) == 1 and next(iter(src[j]))[0] == 'gap')):
                fixed_repair += 1
            label = 'repair' if rep else 'introduced' if intro else 'unresolved' if se else 'preserved'
            if j is not None: events[j].add((label, 'gap' if i is None else 'reference', gap, k))
        if rs == es and ro == eo:
            summaries.append((so, repair, introduced, damage, fixed_repair, events))
    h = min(p[0] for p in summaries)
    optimal = [p for p in summaries if p[0] == h]
    return {key: (min(p[col] for p in optimal), max(p[col] for p in optimal))
            for key, col in [('repair', 1), ('introduced', 2), ('fixed_correct_damage', 3), ('fixed_error_repair', 4)]} | {
        'h': h, 'source_events': [set().union(*(p[5][j] for p in optimal)) for j in range(len(s))]}


def test_independent_225_source_occurrence_and_gap_consensus_sets():
    seqs = [p for n in range(4) for p in itertools.product('ab', repeat=n)]
    for r, s in itertools.product(seqs, repeat=2):
        ref, src, labels, gaps, paths = independent_masks(r, s)
        actual = source_masks(r, s, lattice(r, s))
        assert [set(v) for v in actual['reference']] == ref
        assert [set(v) for v in actual['source']] == src
        assert list(actual['reference_labels']) == labels
        assert list(actual['gap_sequences']) == gaps
        assert actual['pair_unique'] == (len(paths) == 1)


def test_independent_343_conditional_source_events_and_fixed_subset_extrema():
    seqs = [p for n in range(3) for p in itertools.product('ab', repeat=n)]
    for r, s, o in itertools.product(seqs, repeat=3):
        expected = independent_triple(r, s, o)
        actual = score_tokens(r, s, o)
        for key, value in expected.items(): assert actual[key] == value, (r, s, o, key)


@pytest.mark.parametrize('r,s,o,repair,introduced', [
    (('a',), ('b',), ('b',), (0, 0), (0, 0)),
    (('a',), ('b',), ('a',), (1, 1), (0, 0)),
    (('a',), ('a',), ('b',), (0, 0), (1, 1)),
])
@pytest.mark.parametrize('limits', [Limits(pair_cells=100, joint_states=0),
                                 Limits(pair_cells=100, joint_moves=0), Limits(pair_cells=1)])
def test_closed_form_totals_survive_local_budget_failure(r, s, o, repair, introduced, limits):
    actual = score_tokens(r, s, o, limits)
    assert actual['repair'] == repair and actual['introduced'] == introduced
    assert actual['fixed_correct_damage'] is None and actual['fixed_error_repair'] is None
    assert actual['reference_events'] is None and actual['source_events'] is None


def test_failed_empty_reference_case_keeps_corpus_insertion_numerator():
    empty = score_output(prepare_source('', 'x'), Output('x y', 'capped'))
    normal = score_output(prepare_source('a', 'a'), Output('a'))
    totals = aggregate([empty, normal])
    assert empty['eO'] == 2 and empty['completed_repair'] == (0, 0)
    assert totals['reference_words'] == 1 and totals['output_errors'] == 2
    assert totals['wer'] == 2 and totals['invalid_or_incomplete'] == 1


def test_equal_domain_primary_uses_fixed_weights_and_exact_rational_counts():
    repaired=score_output(prepare_source('a','x'),Output('a'))
    unchanged=score_output(prepare_source('b c d','x y z'),Output('x y z'))
    result=equal_domain_aggregate({'LibriSpeech_PC':[repaired],'SLUE_VoxCeleb':[unchanged]})
    assert result['rational_endpoints']['wer']==(1,2)
    assert result['rational_endpoints']['completed_repair_rate']==((1,2),(1,2))
    assert result['wer']==0.5 and aggregate([repaired,unchanged])['wer']==0.75
    assert aggregate([repaired,unchanged])['completed_repair_rate']==(0.25,0.25)


def test_undefined_domain_is_retained_without_reweighting():
    row=score_output(prepare_source('a','a'),Output('a'))
    result=equal_domain_aggregate({'LibriSpeech_PC':[row],'SLUE_VoxCeleb':[]})
    assert result['wer'] is None and result['completed_repair_rate'] is None
    assert result['domain_weights']['SLUE_VoxCeleb']==(1,2)
    with pytest.raises(ValueError):equal_domain_aggregate({'LibriSpeech_PC':[row]})


@pytest.mark.parametrize('field',['offset','lattice'])
def test_cached_preflight_provenance_tamper_blocks_before_candidate_score(field):
    prepared=prepare_source('a','b')
    if field=='offset':prepared.offsets['reference'][0]['raw_byte_span']=(0,2)
    else:prepared.rs_lattice['edges'][(0,0)]=()
    with pytest.raises(ValueError,match='preflight'):score_output(prepared,Output('a'))
