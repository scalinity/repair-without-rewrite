# Six 10M metric and selection independent review

**MEASURED RESULT — review PASS; campaign disposition CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE.** Independent reconstruction found no scoring, population, complete-update, resource or endpoint-selection discrepancy. Both eligible rankings are empty; both selected LRs are null.

FACT — reviewed HEAD `1f398126de6f869f03f39c368a1bec08759b3013`. The authorized start remains `7868302afc43e3cbd475464452f57912a9c2cf97`. The pre-run campaign hash is `43a97ef40acbb2efebaf4941931934969c093e23f77b69bfd132f236755b1dd3`. The metric checker is [six_10m_metrics_independent.py](../../benchmarks/six_10m_metrics_independent.py), SHA-256 `ed901a5fd0619975edc072351d2cf0ce480237ee16cc0bc4c7ed88bce9a63a8a`. This review changed no scientific source, model, recipe, score or configuration and used no accelerator runtime.

The machine-readable endpoint reconstruction is [independent-metrics-final-selection.attempt01.json](../../experiments/manifests/six_10m_probes/independent-metrics-final-selection.attempt01.json), SHA-256 `e655ac7ddf418a7ba56458156f475232f2369934867134f6f6f9170c29a65316`. The full curve/update/checkpoint reconstruction is [independent-metrics-curve-consistency.attempt07.json](../../experiments/manifests/six_10m_probes/independent-metrics-curve-consistency.attempt07.json), SHA-256 `018e1723a1991ef615a9ea92cd00d2015bb57c54f3db2bb0950b756ffa024f36`. These bind every evaluated recipe/endpoint, independent score receipt, raw output, initial/final identity, native checkpoint marker, update log and metric aggregate.

FACT — all 36 frozen evaluations contain the identical ordered 396 DEVELOPMENT IDs: 108 natural LS-PC cases and 288 generated cases, with 96 cases in each generated view. Panel SHA-256: `5043ed60d6ce8f891ee8e30255fabaa40fcac37b0a043c1a85dd88178832ce4e`; ordered-ID SHA-256: `18fbfdb99442d18719f490999f5cb624c8fc8c9c7293883352c4d2d651e23694`. Every raw source/reference hash and population header was checked against the frozen panel. Natural and generated denominators remain separate.

MEASURED RESULT — all 14,256 retained canonical score records were reproduced through the frozen scorer. Separate integer edit-distance calculations performed 42,768 checks. The independently implemented dense alignment oracle reproduced 11,783 bounded cases; dense coverage is not claimed for the remaining 2,473 cases outside its fixed state-product budget. All invalid, capped, incomplete, missing and empty outputs remain in the records and reported denominators. Scorer bounds and ambiguity coverage were retained.

FACT — the controlling pilot rule is [FRONTIER_READER_CURRICULUM_DECISION_V1.md](FRONTIER_READER_CURRICULUM_DECISION_V1.md), lines 438–479, adopted prospectively in [PROSPECTIVE_AMENDMENTS.md](PROSPECTIVE_AMENDMENTS.md). It binds pooled failure-inclusive natural DEVELOPMENT WER. The final equal-domain LS-PC/SLUE H1 primary is a later endpoint; SLUE is absent from this pilot panel. The five eligibility gates and six-stage lexicographic rule were applied only to the nominal 10M evaluation, mapped to the common completed endpoint.

MEASURED RESULT — all six terminal attempt01 outcomes are COMPLETED at update 305, 10,007,223 canonical exposures and presentation ordinal 134,590. The review joined every presentation across all 1,830 updates (807,546 presentation consumptions) to the frozen scientific ledger. The 305 queue boundaries, complete-update exposures, phases and shared denominators match across all six recipes. B uses 16-example microbatches and the PAD-excluded target/EOS denominator. C uses 4-example microbatches and whole-queue action/start/end/vocabulary denominators. Every logged LR matches the frozen warmup and continuous cosine exposure clock; the final LR is 10% of peak.

Ledger SHA-256: `21c3f5838f5c7e85f258e8eef25b2b38884a2023199afc5d1852d68155b04f2f`. All 78 saved states reproduce the 13 deduplicated approved save endpoints per recipe through their native COMPLETE/metadata hashes, optimizer step, reader cursor, empty queue and zero pending charge. The source-context cap 1,024, decoder-position cap 256 and C edit cap 64 were respected in the stored records and native source accounting. No numerical failure, replay or interruption receipt exists; all terminal receipts record zero replay.

FACT — initial parameter identities agree across the three recipes within each architecture. Each initial identity was reconstructed from the campaign, terminal and native initial-checkpoint receipts; final identities and save metadata were similarly joined. Full tensor/arrays.npz byte and tensor-hash reproduction is the scope of the separate provenance review. This metric review does not claim that heavy verification.

| Architecture and recipes | Initial parameter identity |
| --- | --- |
| B100-seed42-lr1e-04, B100-seed42-lr3e-04, B100-seed42-lr6e-04 | `2739837ff4ad4ff26475dca5a37608d9c46a1c7ff34f8778f24eadb18b8e8044` |
| C101-seed42-lr1e-04, C101-seed42-lr3e-04, C101-seed42-lr6e-04 | `9671ba3aaf0afb9fe22302fe140512db7bdf7e31f4d9e439bc13c75edafc2ff1` |

MEASURED RESULT — the natural reference denominator is 2,270 words and RAW has 64 errors in every endpoint population. Every recipe completes, but every final natural WER exceeds RAW. The B recipes have positive completed repair supported in multiple groups and no genuine generated required repair. The C recipes complete genuine generated required repairs and have zero completed natural repair and zero natural repair-support groups.

| Recipe | Natural errors / 2,270 | Completed repair bounds | Lower-bound support groups | Generated required-repair cases | Eligibility |
| --- | ---: | ---: | ---: | ---: | --- |
| B100-seed42-lr1e-04 | 2208 | [6, 6] | 3 | 0 | FAIL |
| C101-seed42-lr1e-04 | 121 | [0, 0] | 0 | 49 | FAIL |
| B100-seed42-lr3e-04 | 2584 | [2, 2] | 2 | 0 | FAIL |
| C101-seed42-lr3e-04 | 128 | [0, 0] | 0 | 79 | FAIL |
| B100-seed42-lr6e-04 | 2664 | [2, 2] | 2 | 0 | FAIL |
| C101-seed42-lr6e-04 | 109 | [0, 0] | 0 | 54 | FAIL |

Exact eligibility outcomes, in the frozen order (completion, WER below RAW, positive completed repair, at least two support groups, genuine generated required repair): B100 at every LR is `[PASS, FAIL, PASS, PASS, FAIL]`; C101 at every LR is `[PASS, FAIL, FAIL, FAIL, PASS]`.

MEASURED RESULT — exact lexicographic keys are listed below for reproduction. The key order is WER, introduced upper/reference words, negative completed repair lower, natural invalid/incomplete, negative generated mixed success, and peak LR. Only eligible recipes enter selection.

| Recipe | Exact six-stage key |
| --- | --- |
| B100-seed42-lr1e-04 | `(1104/1135, 215/227, -6, 0, 0, 1/10000)` |
| C101-seed42-lr1e-04 | `(121/2270, 57/2270, 0, 0, -32, 1/10000)` |
| B100-seed42-lr3e-04 | `(1292/1135, 1261/1135, -2, 0, 0, 3/10000)` |
| C101-seed42-lr3e-04 | `(64/1135, 32/1135, 0, 0, -42, 3/10000)` |
| B100-seed42-lr6e-04 | `(1332/1135, 1301/1135, -2, 0, 0, 3/5000)` |
| C101-seed42-lr6e-04 | `(109/2270, 9/454, 0, 0, -30, 3/5000)` |

**B100 eligible ranking: `[]`; selected recipe/LR: `null`. C101 eligible ranking: `[]`; selected recipe/LR: `null`.** An ineligible endpoint does not become a selected LR. All six decisions and exact keys match [endpoint-selection.attempt01.json](../../experiments/manifests/six_10m_probes/endpoint-selection.attempt01.json).

MEASURED RESULT — the 0/1M/3M/P0/P1/10M curve values were reconciled with all six raw output files per recipe and the corresponding training-update summaries. Word/output-length distributions, byte/lexical identity, scorer ambiguity, failure/structure counts, C program availability/edit burden, B returned-token burden, decoder positions and decode/scorer timing reproduce [descriptive-tables.attempt01.json](../../experiments/manifests/six_10m_probes/descriptive-tables.attempt01.json). Training host timing sums, phase counts, memory peaks, example/microstep/native-position totals and throughput inputs match all 305 update records per recipe.

The summed serial recipe wall time is 23128.91242146492004 seconds. Exact accelerator kernel time remains UNMEASURED; synchronized native-update host wall intervals are reported separately. This review does not reinterpret host intervals as device-kernel time.

FACT — [campaign-progress.attempt05.json](../../experiments/manifests/six_10m_probes/campaign-progress.attempt05.json) reproduces six consumed/completed slots and zero unstarted slots. [development_calibration_consumption_six_10m_probes.attempt06.json](../../experiments/manifests/development_calibration_consumption_six_10m_probes.attempt06.json) binds 36 evaluation uses of the same 96 previously consumed CAL IDs (3,456 case evaluations) and 12 frozen HPO IDs; no row role, fit or sealed-reference use changed.

FACT — failed preparation diagnostics remain on disk: the initial selection-helper preparation findings, the curve-review command schema error in curve-consistency attempt04, and the final plot-source binding diagnostic in final-review-preparation attempt01. They describe review/reporting preparation, not scientific recipe failures. Corrected preparation checks passed before a final decision used their helpers. B100 1e-4 baseline was reviewed again as independent-metrics attempt40 under the current checker; the earlier attempt02 checker binding remains preserved. No training or neural inference was repeated for this refresh.

The display-only plot change (tick rotation, caption wrapping, margins and additive V2 filenames) is independently rebound in [independent-metrics-reporting-library.attempt02.json](../../experiments/manifests/six_10m_probes/independent-metrics-reporting-library.attempt02.json), SHA-256 `a9cd736f93b29416179dea2623a48c516c20af626c709a9a621b4e1ef41e4ab5`. A blank isolated Agg export fixture passed; metric inputs, axes scales, denominators, bound interpretation and six-recipe membership checks are unchanged. The prior library receipt and original figures remain preserved.

DESCRIPTIVE INFERENCE — the frozen endpoint screens admit neither arm at 10M. That statement does not establish that either architecture can never work and does not confirm H1. No intermediate checkpoint was selected, no eligibility gate was weakened, and no cross-arm LR choice occurred.

FUTURE SCIENTIFIC DECISION — the current prospective 150M campaign cannot proceed under these frozen results. Interpretation or scientific changes require the separately authorized frontier review; this independent metric review proposes no treatment change. No final seed, final 150M run, sealed inference, A100/H2 campaign or protocol freeze was performed by this review.

CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE
