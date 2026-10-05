"""Sealed R/S denominators, failure mapping, and integer aggregate ledgers."""
from dataclasses import dataclass, asdict
import hashlib
from .text import strict_text, normalize_tokens, lexical, POLICY_HASH
from .triple import Limits, distance, lattice, source_masks, score_tokens, seal


@dataclass(frozen=True)
class Source:
    reference: bytes
    source: bytes
    r: tuple
    s: tuple
    masks: dict
    mask_hash: str
    source_hash: str
    reference_hash: str
    eS: int
    rs_lattice: dict | None
    offsets: dict


def prepare_source(reference,source,limits=Limits()):
    rtext,stext=strict_text(reference),strict_text(source)
    rb,sb=rtext.encode('utf-8'),stext.encode('utf-8')
    _,rt=normalize_tokens(rb);_,st=normalize_tokens(sb)
    r,s=tuple(t.value for t in rt),tuple(t.value for t in st)
    rs=lattice(r,s,limits.pair_cells)
    masks=source_masks(r,s,rs)
    return Source(rb,sb,r,s,masks,seal(masks),hashlib.sha256(sb).hexdigest(),
                  hashlib.sha256(rb).hexdigest(),distance(r,s),rs,
                  {'reference':[asdict(t) for t in rt],'source':[asdict(t) for t in st]})


@dataclass(frozen=True)
class Output:
    text: bytes | str | None
    status: str = 'complete'


STATUSES={'complete','capped','timeout_prefix','missing','invalid_utf8','invalid_c',
          'abstain','timeout_no_prefix'}


def score_output(prepared,output,limits=Limits()):
    if seal(prepared.masks)!=prepared.mask_hash:
        raise ValueError('sealed source mask was altered')
    if output.status not in STATUSES:
        raise ValueError('unknown output status')
    failure=None
    if output.status in {'missing','invalid_utf8','invalid_c','abstain','timeout_no_prefix'}:
        observed='';complete=False;failure=output.status
    elif output.text is None:
        observed='';complete=False;failure='missing'
    else:
        try:
            observed=strict_text(output.text)
            complete=output.status=='complete'
            failure=None if complete else output.status
        except (UnicodeError,ValueError):
            observed='';complete=False;failure='invalid_utf8'
    tokens=lexical(observed)
    result=score_tokens(prepared.r,prepared.s,tokens,limits,prepared.rs_lattice)
    # R/S masks are sealed before any O; local data computed later cannot narrow them.
    result['source_masks']=prepared.masks
    result.update(schema_version='score_record_v1',scorer_algorithm='reference_triple_v1',
                  normalization_id='lexical_eval_v1',normalization_tables_hash=POLICY_HASH,
                  complete_valid=complete,failure_reason=failure,
                  observed_text_policy='emitted' if failure in {None,'capped','timeout_prefix'} else 'empty_failure',
                  completed_repair=result['repair'] if complete else (0,0),
                  unresolved=(prepared.eS-result['repair'][1],prepared.eS-result['repair'][0]),
                  source_hash=prepared.source_hash,reference_hash=prepared.reference_hash,
                  source_mask_hash=prepared.mask_hash,output_hash=None if output.text is None else
                    hashlib.sha256(output.text if isinstance(output.text,bytes) else output.text.encode('utf-8',errors='surrogatepass')).hexdigest(),
                  observed_output_hash=hashlib.sha256(observed.encode()).hexdigest(),
                  raw_byte_exact=complete and observed.encode()==prepared.reference,
                  lexical_exact=complete and tokens==prepared.r,
                  surface_character_errors=distance(tuple(prepared.reference.decode()),tuple(observed)),
                  reference_scalar_count=len(prepared.reference.decode()),
                  source_consensus_eligible_counts=None if prepared.masks['status']!='available' else {
                    'correct':prepared.masks['reference_labels'].count('certain_correct'),
                    'error':prepared.masks['reference_labels'].count('certain_error'),
                    'ambiguous':prepared.masks['reference_labels'].count('ambiguous')},
                  normalization_offsets=prepared.offsets)
    assert seal(prepared.masks)==prepared.mask_hash
    return result


def aggregate(records):
    records=list(records)
    totals={'reference_words':sum(r['reference_words'] for r in records),
            'source_errors':sum(r['eS'] for r in records),
            'output_errors':sum(r['eO'] for r in records),
            'invalid_or_incomplete':sum(not r['complete_valid'] for r in records)}
    for key in ('repair','introduced','completed_repair'):
        totals[key]=tuple(sum(r[key][i] for r in records) for i in (0,1))
    n,e=totals['reference_words'],totals['source_errors']
    totals['wer']=totals['output_errors']/n if n else None
    totals['introduced_rate']=tuple(x/n for x in totals['introduced']) if n else None
    totals['completed_repair_rate']=tuple(x/e for x in totals['completed_repair']) if e else None
    return totals
