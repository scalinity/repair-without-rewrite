"""Score every preselected public DEV ASR row under both unfrozen reference fields.

O=S is the RAW identity control; this is source-denominator qualification, not
candidate evaluation or a natural final result population.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time
import tracemalloc

from src.scoring.records import Output, aggregate, prepare_source, score_output
from src.scoring.text import POLICY_HASH


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--asr', type=Path, required=True)
    parser.add_argument('--audio-manifest', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    panel = json.loads(args.audio_manifest.read_text())
    calls = [json.loads(line) for line in (args.asr / 'calls.jsonl').read_text().splitlines()]
    rows = [row for row in calls if row['segment'] == 'development']
    assert len(rows) == len(panel['cases'])
    assert sorted(row['case_index'] for row in rows) == list(range(len(rows)))
    barrier = json.loads((args.asr / 'source_barrier.json').read_text())
    assert barrier['status'] == 'PASS_BOOK_PROJECT_DEVELOPMENT_CLOSURE'
    assert barrier['audio_manifest']['sha256'] == sha(args.audio_manifest)
    provenance = {'classification': 'PUBLIC_DEV_SOURCE_COUNTS_RAW_IDENTITY_ONLY_NOT_FINAL',
        'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'dirty': subprocess.check_output(['git', 'status', '--short'], text=True),
        'audio_manifest_sha256': sha(args.audio_manifest),
        'asr_calls_sha256': sha(args.asr / 'calls.jsonl'),
        'asr_source_barrier_sha256': sha(args.asr / 'source_barrier.json'),
        'program_sha256': sha(__file__), 'normalization_tables_hash': POLICY_HASH,
        'reference_policies': ['text', 'text_raw'], 'policy_frozen': False,
        'no_candidate_output': True, 'seed': 'preselected audio seed42; scorer deterministic',
        'scorer_code_hashes': {str(path): sha(path) for path in sorted(Path('src/scoring').glob('*.py'))}}
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / 'provenance.json').write_text(json.dumps(provenance, indent=2, sort_keys=True) + '\n')
    start = time.perf_counter()
    tracemalloc.start()
    policies = {}
    with (args.out / 'records.jsonl').open('w') as stream:
        for field in ('text', 'text_raw'):
            scored = []
            failures = []
            for row in rows:
                case = panel['cases'][row['case_index']]
                assert row['audio_sha256'] == case['audio_sha256']
                assert row['reference_text'] == case['text']
                assert row['reference_text_raw'] == case['text_raw']
                if row['status'] != 'COMPLETED':
                    failures.append({'case_index': row['case_index'], 'asr_status': row['status'],
                        'reason': 'source unavailable; denominator unknown; retained in preselected population'})
                    continue
                fixed = prepare_source(case[field], row['hypothesis'])
                record = score_output(fixed, Output(row['hypothesis']))
                assert record['repair'] == (0, 0) and record['introduced'] == (0, 0)
                record.update(case_id=Path(case['audio_filepath']).stem,
                    corpus_id='LibriSpeech_PC', population_id='book_closed_public_dev_attempt03',
                    output_view='RAW_identity', reference_policy_id=field + '_DEVELOPMENT_UNFROZEN',
                    recognizer_view='parakeet_ed2b7e8', cluster_ids=[case['source_group_id']],
                    source_field_policy_frozen=False)
                stream.write(json.dumps(record, sort_keys=True) + '\n')
                scored.append(record)
            policies[field] = {'preselected_cases': len(rows), 'scored_cases': len(scored),
                'source_unavailable_cases': failures, 'population_complete': not failures,
                'aggregate_pooled_dev_only': aggregate(scored),
                'alignment_status_counts': dict(Counter(r['status'] for r in scored)),
                'point_repair_counts': sum(r['repair'][0] == r['repair'][1] for r in scored),
                'max_repair_bound_width': max((r['repair'][1] - r['repair'][0] for r in scored), default=None),
                'source_consensus_counts': dict(sum((Counter(r['source_consensus_eligible_counts'] or {}) for r in scored), Counter())),
                'max_joint_states': max((r['joint_states'] for r in scored), default=None),
                'max_joint_edges': max((r['joint_edges'] for r in scored if r['joint_edges'] is not None), default=None),
                'cap_cases': sum(r['status'] in ('resource_envelope', 'closed_form_point') for r in scored)}
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    summary = {'classification': provenance['classification'], 'policies': policies,
        'elapsed_seconds': elapsed, 'python_traced_peak_bytes': peak,
        'process_peak_rss_bytes_macos': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'selected_cases': len(rows), 'selected_groups': len({c['source_group_id'] for c in panel['cases']}),
        'selected_audio_seconds': panel['selected_audio_seconds'],
        'records_sha256': sha(args.out / 'records.jsonl'),
        'primary_equal_domain_endpoint': None,
        'primary_unavailable_reason': 'SLUE unavailable; do not reweight registered0.5/0.5 domains',
        'literal_extractor_and_cluster_bootstrap': 'NOT_QUALIFIED',
        'joint_scope_limit': 'O=S identity cannot establish candidate-output ambiguity or H1 precision',
        'no_source_error_free_exclusions': True}
    (args.out / 'summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
