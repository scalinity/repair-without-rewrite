# Frontier reader implementation session — 2026-10-05

**Outcome: FRONTIER_MODEL_REVIEW_REQUIRED. Faithful implementation reached a measured empirical-profile stop; the six 10M probes remain unstarted.** This is a scientific qualification issue, not an architecture failure, a measured 32k memory failure or rejection of the paper.

## Handoff and prospective evidence

Before modifications, local HEAD and remote main were equal at `928fd0305206ad6d6130d0667d1b206baa521a64`; working tree was clean and ancestry check passed. The integrated baseline reproduced **259 tests in 23.56 seconds** with `MLX_ENABLE_TF32=0`. [Baseline receipt](../../experiments/manifests/frontier_reader/baseline-validation.attempt01.json) pins preserved stdout; invocation wall was not separately measured.

The preceding Astra decision is preserved verbatim in [FRONTIER_READER_CURRICULUM_DECISION_V1.md](../reviews/FRONTIER_READER_CURRICULUM_DECISION_V1.md), with requested authorization metadata. Its exact approved amendment was appended to [PROSPECTIVE_AMENDMENTS.md](../reviews/PROSPECTIVE_AMENDMENTS.md). Separate commit: **`bd882ceea205c2f9e0547fa49337e94e1b042fad`**. It precedes implementation. Supplied v1.2 documents and registry were not modified.

## Work actually completed

- Implemented the TRAIN-only raw-codepoint all-optimal consensus estimator and support/co-occurrence/severity tables.
- Added hash-bound CPU input qualification against the frozen pair file and current admitted TRAIN roles/targets.
- Used all 1,024 TRAIN rows / 48 groups once; excluded all 96 CALIBRATION rows from fitting/profile estimation.
- Added 16 regression tests, including an independent exhaustive optimal-path oracle over 225 string pairs.
- Measured and preserved the complete aggregate table, unsupported entries, ambiguity, input hashes and private per-record alignment audit.
- Ran a separate descriptive existing-lexical-policy audit; it did not filter or alter the table.
- Obtained separate independent reconstruction of every raw alignment and exact aggregate table bytes.
- Wrote all requested V2/V3 gate reports with explicit blocked/unmeasured dispositions.

The table retains 67 elementary entries with 2,113 occurrence weight: **1,372 punctuation, 525 case, 48 whitespace, 168 other**. Surface effects comprise **92.0492%**. The largest entry is double-quote deletion (433 occurrences). **508 of 842** raw-different records are lexically equal. Full mass/support/severity and the precise frontier request are in [profile qualification](EMPIRICAL_CORRUPTION_PROFILE_QUALIFICATION.md).

The owner explicitly required escalation for a surface-policy-dominated profile. Reader admission and dependent generation/trainer/checkpoint/BENCH/probe work stopped. No profile filtering, substitute corruption or weight redistribution occurred.

## Scope remaining blocked

Common generated-base/variant manifests, spoken renderer, full union inverse, generated support availability, accounting serializer/worked examples, deficit scheduler/pass persistence, long dry run, actual B/C ledgers, compressed executable pilot configuration, machine-readable future-panel freeze, 32,768-update integration, actual boundary/mid-update cold replay, BENCH and cost forecast remain unqualified. Approved scientific requirements remain recorded; absence of implementation is not PASS.

No fairness equality is claimed over absent ledgers. No old fixture timing is promoted into complete-update cost. Future one-B, one-C and all-six wall estimates remain UNPRICED.

## Validation and preserved evidence

[Final integrated receipt](../../experiments/manifests/frontier_reader/final-validation.attempt01.json): **275 passed in 23.43 seconds**, invocation wall **23.932327 seconds**, `MLX_ENABLE_TF32=0`. It binds current estimator/test/runner and unchanged tokenizer/canonical/registry hashes. The baseline/final suites perform bounded numerical model operations; neither consumes a registered recipe slot or new mixed-reader BENCH update.

Root measured profile input binding/estimation wall **24.300607 CPU seconds**; separate descriptive lexical audit **0.672664 CPU seconds**. Whole-session active/elapsed/device time was not comprehensively instrumented, so no total is fabricated. Independent review timing is recorded separately and should not be added as serialized training cost.

Ignored evidence stays under `exports/frontier-reader/`: original private preflight and run-source snapshot, exact input inventory, full alignment audit, measurement stdout, baseline/final stdout and test preflights. Independent review preserves its own diagnostic checker attempts, including its initial serialization-only checker failure; the estimator/table did not fail that audit.

The measurement runner originally exported one real nonfunctional absolute local code path via `__file__`. The exact original receipt was preserved outside Git before creating a separately labeled [public export](../../experiments/manifests/frontier_reader/empirical-profile-preflight.public.attempt01.json) containing the repository-relative key; source/result hashes were unchanged. The runner is fixed for future exports. Original measured runner code/hash remains preserved; this path-only correction did not rerun or revise the empirical result.

## Evidence and next action

- [Empirical profile qualification](EMPIRICAL_CORRUPTION_PROFILE_QUALIFICATION.md)
- [Mixed-reader V2](PAIRED_MIXED_READER_QUALIFICATION_V2.md)
- [Complete-update BENCH V2](PAIRED_COMPLETE_UPDATE_BENCH_V2.md)
- [Independent profile review](../reviews/EMPIRICAL_CORRUPTION_PROFILE_INDEPENDENT_REVIEW.md)
- [Fairness V2](PAIRED_READER_FAIRNESS_AUDIT_V2.md)
- [Cost projection](BC_10M_PROBE_COST_PROJECTION.md)
- [Admission V3, all 39 questions](BC_10M_PROBE_ADMISSION_DECISION_V3.md)

Commits after the prospective decision and exact published implementation checkpoint are identified by Git and the final response; no report embeds its own future commit hash. The [publication audit](../../experiments/manifests/frontier_reader/publication-safety.attempt01.json) checks additive working-tree files and each introduced commit snapshot, excluded private assets/state, local links and unchanged tested source hashes. Publication includes only named source/tests, aggregate evidence and reports. Raw text/audio/model assets, private alignment records, environment/cache and agent state remain excluded.

**Next action:** owner frontier review of the measured profile and explicit authorization of retaining or revising its scientific treatment. Fixed B100/C101, objectives, tokenizer, canonical/pilot design, six LR slots and H1 attribution remain unchanged.

No six 10M probe, final seed, final/sealed candidate inference, protocol freeze, cloud spending or production LocalFlow modification occurred.

FRONTIER_MODEL_REVIEW_REQUIRED
