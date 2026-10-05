"""Sealed R/S denominators, failure mapping, and integer aggregate ledgers."""
from dataclasses import dataclass, asdict
from fractions import Fraction
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
    preflight_hash: str


def _preflight_hash(reference,source,r,s,masks,rs,offsets):
    frozen_lattice=None if rs is None else {
        'distance':rs['distance'],'cells':rs['cells'],
        'path_count_saturated':rs['path_count_saturated'],
        'edges':[(u,destinations) for u,destinations in sorted(rs['edges'].items())]}
    return seal({'reference_hash':hashlib.sha256(reference).hexdigest(),
                 'source_hash':hashlib.sha256(source).hexdigest(),'r':r,'s':s,
                 'masks':masks,'lattice':frozen_lattice,'offsets':offsets})


def prepare_source(reference,source,limits=Limits()):
    rtext,stext=strict_text(reference),strict_text(source)
    rb,sb=rtext.encode('utf-8'),stext.encode('utf-8')
    _,rt=normalize_tokens(rb);_,st=normalize_tokens(sb)
    r,s=tuple(t.value for t in rt),tuple(t.value for t in st)
    rs=lattice(r,s,limits.pair_cells)
    masks=source_masks(r,s,rs)
    offsets={'reference':[asdict(t) for t in rt],'source':[asdict(t) for t in st]}
    return Source(rb,sb,r,s,masks,seal(masks),hashlib.sha256(sb).hexdigest(),
                  hashlib.sha256(rb).hexdigest(),distance(r,s),rs,
                  offsets,_preflight_hash(rb,sb,r,s,masks,rs,offsets))


@dataclass(frozen=True)
class Output:
    text: bytes | str | None
    status: str = 'complete'


STATUSES={'complete','capped','timeout_prefix','missing','invalid_utf8','invalid_c',
          'abstain','timeout_no_prefix'}


def score_output(prepared,output,limits=Limits()):
    if (seal(prepared.masks)!=prepared.mask_hash or
        _preflight_hash(prepared.reference,prepared.source,prepared.r,prepared.s,
                        prepared.masks,prepared.rs_lattice,prepared.offsets)!=prepared.preflight_hash):
        raise ValueError('sealed source preflight was altered')
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
    # Canonical score_record_v1 names are populated independently of model family.
    # Population/join and optional literal/generator fields require upstream
    # sealed manifests and remain explicitly null in this development interface.
    for field in ('scorer_spec_hash','scorer_implementation_hash','case_id','population_id',
                  'corpus_id','recognizer_view','system_seed_id','output_view','reference_policy_id',
                  'literal_extractor_hash','literal_fixed_denominators','literal_success_bounds',
                  'literal_exclusion_reason_counts','latent_schema_hash','structural_parser_hash',
                  'structural_parse_status','structure_qualified_field_matches','complete_target_conformance'):
        result[field]=None
    result.update(cluster_ids=[],source_preflight_hash=prepared.preflight_hash,
                  source_word_errors=result['eS'],output_word_errors=result['eO'],
                  source_output_word_distance=result['eSO'],conditional_source_output_cost=result['h'],
                  raw_repair_lower=result['repair'][0],raw_repair_upper=result['repair'][1],
                  introduced_lower=result['introduced'][0],introduced_upper=result['introduced'][1],
                  completed_repair_lower=result['completed_repair'][0],completed_repair_upper=result['completed_repair'][1],
                  introduced_reference_word_bounds=result['reference_damage'],
                  introduced_insertion_bounds=result['insertion_damage'],unresolved_bounds=result['unresolved'],
                  edited_unresolved_bounds=result['edited_unresolved'],
                  source_ambiguous_counts=None if prepared.masks['status']!='available' else
                    {'reference':prepared.masks['reference_labels'].count('ambiguous')},
                  output_consensus_counts=None if result['reference_events'] is None else
                    {'reference_available':sum(len(v)==1 for v in result['reference_events']),
                     'reference_unavailable':sum(len(v)!=1 for v in result['reference_events'])},
                  alignment_status=result['status'],joint_states_examined=result['joint_states'],
                  joint_moves_examined=result['joint_moves'],scoring_status='completed',MEASURED_RESULT=None,
                  optional_field_status='requires sealed population/literal/generated manifests')
    assert seal(prepared.masks)==prepared.mask_hash
    return result


def aggregate(records):
    """Pooled secondary ratio ledger. Do not call this the equal-domain primary."""
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


def equal_domain_aggregate(records_by_domain):
    """Fixed 0.5/0.5 primary endpoints; exact rational ledgers plus display values.

    An undefined domain remains undefined. No renormalization, dropping, or
    pooling can replace its registered half-weight.
    """
    names=('LibriSpeech_PC','SLUE_VoxCeleb')
    if set(records_by_domain)!=set(names):
        raise ValueError('both exact registered natural domains are required')
    domains={name:aggregate(records_by_domain[name]) for name in names}
    result={'domain_weights':{name:(1,2) for name in names},'domains':domains,
            'rational_endpoints':{}}
    for key,count,denominator,interval in (
            ('wer','output_errors','reference_words',False),
            ('introduced_rate','introduced','reference_words',True),
            ('completed_repair_rate','completed_repair','source_errors',True)):
        if any(not d[denominator] for d in domains.values()):
            result[key]=None;result['rational_endpoints'][key]=None
            continue
        values=[]
        for endpoint in range(2 if interval else 1):
            value=sum(Fraction(d[count][endpoint] if interval else d[count],d[denominator])
                      for d in domains.values())/2
            values.append(value)
        result[key]=tuple(float(v) for v in values) if interval else float(values[0])
        result['rational_endpoints'][key]=tuple((v.numerator,v.denominator) for v in values) if interval else (values[0].numerator,values[0].denominator)
    return result
