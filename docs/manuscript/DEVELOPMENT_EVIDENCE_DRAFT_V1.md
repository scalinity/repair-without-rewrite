# Development evidence draft v1

FACT — Documentation preparation, 2026-10-10. This is material for a possible manuscript, not an accepted paper scope, final experiment, or demonstrated useful transcript restorer. Documentation base: `abfd0d595e80b1cca544bb9e91e238b094e2a604`. G1/G2 experimental evidence is retained at scientific checkpoint `609f97f31979d469ad8551d06b2c07c3513181ec`; the retrospective feasibility record and frontier v3/v4 are retained at the documentation base. Existing scientific files are immutable.

MEASURED RESULT — Neither scratch arm produced an eligible G1 endpoint. The prescribed G2 B100, C101 and adapted ByT5 candidates all failed WER strictly below RAW. CALCULATION — The fixed ten-pass ByT5 proposals contain reference-aware whole-output oracle headroom. INFERENCE — These records support bounded negative development findings and diagnostics, with publication value and scientific manuscript scope still subject to frontier review. OPEN SCIENTIFIC QUESTION — Whether a source-only system can retain useful correction while limiting introduced errors on an independent population remains unanswered.

## Evidence map and reading conventions

All local links are relative to this document. E identifiers are stable within these two preparation documents. Original bytes and SHA-256 identities are recorded in [the evidence inventory](../../experiments/manifests/manuscript_development_evidence/evidence-inventory.attempt01.json). That inventory distinguishes frozen experimental sources from later retrospective records. No private transcript, reference, audio or checkpoint payload was opened for this preparation.

| ID | Primary record and corresponding verification |
|---|---|
| E01 | [Canonical extracted v1.2 specification](../design-inputs/EXTRACTED_CANONICAL_SOURCE.md), especially §§2, 9–12, 17–18, 23, 25; [canonical PDF](../design-inputs/LocalFlow_From_Scratch_Master_Spec_v1_2.pdf); [input hashes](../design-inputs/SHA256SUMS) |
| E02 | [Draft experiment registry](../design-inputs/LocalFlow_Publication_Experiment_Registry_v2.txt), [accepted review](../reviews/Independent_Pre_Implementation_Review_v1_2_Accepted_Findings.md), [prospective amendments](../reviews/PROSPECTIVE_AMENDMENTS.md) |
| E03 | [G1 campaign](../reports/SIX_10M_PROBE_CAMPAIGN.md), [campaign freeze](../../experiments/manifests/six_10m_probes/campaign-freeze.attempt01.json), [descriptive tables](../../experiments/manifests/six_10m_probes/descriptive-tables.attempt01.json), [endpoint selection](../../experiments/manifests/six_10m_probes/endpoint-selection.attempt01.json) |
| E04 | [G1 independent metrics](../reviews/SIX_10M_METRICS_INDEPENDENT_REVIEW.md), [provenance](../reviews/SIX_10M_PROVENANCE_INDEPENDENT_REVIEW.md), [report consistency](../reviews/SIX_10M_REPORT_CONSISTENCY_INDEPENDENT_REVIEW.md), [campaign review](../reports/SIX_10M_PROBE_INDEPENDENT_REVIEW.md) |
| E05 | [G2 campaign freeze](../../experiments/manifests/generation_2/execution-campaign-freeze.attempt01.json), [corpus freeze](../../experiments/manifests/generation_2/corpus-freeze.attempt01.json), [historical compatibility](../reviews/G2_HISTORICAL_INDEPENDENT_REVIEW.md), [admission](../reports/G2_INDEPENDENT_ADMISSION_REVIEW.md) |
| E06 | [G2 B/C campaign](../reports/G2_BC_SCIENTIFIC_CAMPAIGN.md), [primary aggregate result receipt](../../experiments/manifests/generation_2/scientific-results.attempt01.json) |
| E07 | [G2 factorial analysis](../reports/G2_FACTORIAL_ANALYSIS.md), using the same primary aggregate receipt |
| E08 | [G2 ByT5 adaptation](../reports/G2_BYT5_SCIENTIFIC_ADAPTATION.md), [four-state schedule](../../experiments/manifests/generation_2/byt5-execution-schedule.attempt01.json) |
| E09 | [Independent G2 results](../reviews/G2_SCIENTIFIC_RESULTS_INDEPENDENT_REVIEW.md), [independent result receipt](../../experiments/manifests/generation_2/scientific-results-independent.attempt01.json), [independent ten-pass observation](../reviews/G2_BYT5_10PASS_OBSERVATION_INDEPENDENT_REVIEW.md) |
| E10 | [Independent G2 accounting](../reviews/G2_SCIENTIFIC_ACCOUNTING_INDEPENDENT_REVIEW.md), [accounting receipt](../../experiments/manifests/generation_2/scientific-accounting-independent.attempt01.json), [post-G2 decision](../reports/POST_G2_DEVELOPMENT_DECISION.md) |
| E11 | [Complete retrospective feasibility study](../reports/POST_G2_READ_ONLY_TASK_FEASIBILITY_V1.md), including all three appendices |
| E12 | [Frontier v1](../reviews/FRONTIER_POST_10M_SCIENTIFIC_DECISION_V1.md), [v2](../reviews/FRONTIER_POST_G2_SCIENTIFIC_DECISION_V2.md), [v3](../reviews/FRONTIER_POST_FEASIBILITY_SCIENTIFIC_DECISION_V3.md), [v4](../reviews/FRONTIER_POST_FEASIBILITY_FRESH_DATA_SOURCE_DECISION_V4.md) |
| E13 | [Public source qualification](../reports/PUBLIC_SOURCE_QUALIFICATION.md), [public source identities](../../experiments/manifests/public_sources.json), [G2 metadata census](../../experiments/manifests/generation_2/metadata-census-summary.attempt01.json), [source preparation](../reports/G2_SOURCE_PREPARATION.md) |
| E14 | [Prior-work qualification](../reports/COMPARATOR_AND_PRIOR_WORK_QUALIFICATION.md), [tokenizer attribution](../../configs/tokenizer_development/ATTRIBUTION.md) |

FACT — MEASURED RESULT refers to completed recorded experiments. CALCULATION refers to arithmetic or analysis of retained artifacts. INFERENCE is interpretation with its limitations. OPEN SCIENTIFIC QUESTION is unresolved. Scorer lower/upper bounds concern alignment identification; they are not confidence intervals. Historical independent reconstruction is identified explicitly; this writing task did not repeat private-payload reconstruction or scientific tests.

## A. Research motivation

INFERENCE — A corrector acts on mostly correct recognizer text. Aggregate accuracy therefore depends on both repairing existing errors and avoiding new ones. Full-output generation exposes unchanged content to generation; sparse editing can copy untouched bytes mechanically, while still damaging a source through wrong edit decisions. A controlled comparison can make this tradeoff visible without treating fluent output, copying or low training loss as evidence of correct restoration. The evaluated task is restoration relative to a designated reference, not a guarantee of intended meaning or acoustic truth. [E01, E12]

## B. Original controlled representation-comparison question

FACT — The original question asks how full-transcript generation and compact editing with deterministic copying differ in useful repair, introduced errors, preservation and complete native cost under matched downstream presentations and source exposure. B100 and C101 share a nearly matched scratch backbone; their supervision, decoding and constitutive renderer differ. This is not a pure output-format or neural-architecture contrast. [E01 §§2, 9–10; E12 v1 §§R–T, v2 §L]

FACT — The draft final H1 requires introduced-error superiority while retaining useful repair and WER, with explicit noninferiority and utility conditions. Its prospective final equal-domain LS-PC/SLUE population, final seeds and 150M training are not the development populations or adequacy screens below. The immutable v1.2 specification and draft registry are design inputs; neither is evidence of protocol freeze or achieved final gates. No claim confirms or rejects H1 in the protected final population. [E01 §§2.3, 25; E02]

## C. B100 and C101 architecture and training configuration

FACT — Both scratch systems use fresh seed-42 random initialization, vocabulary 16,384, width 768, eight bidirectional MHA encoder layers and four causal GQA decoder layers with cross-attention. They have 12 query heads, four decoder KV heads, head width 64, SwiGLU width 2,048, pre-RMSNorm, RoPE self-attention and a shared tied vocabulary matrix. B100 has 100,686,336 trainable parameters. C101 adds 128-wide start/end pointer projections and an EDIT/END/ABSTAIN action head, totaling 101,081,859 parameters. [E01 §9; E03 models; E05 recipes]

FACT — B predicts full target text with target/EOS cross-entropy, excluding PAD from its whole-update denominator. C predicts monotonic source-relative byte-span edits and replacement text, restricted to legal UTF-8 boundaries. Its deterministic renderer copies untouched source gaps. Action, start-pointer, end-pointer and vocabulary losses each use their own whole-update valid-decision denominator, with four coefficients equal to one and zero-count components omitted. END-EDIT is included in vocabulary supervision. For K edits and R ordinary replacement tokens, C uses `1 + R + 3K` decoder positions and `R + K` vocabulary targets; ordinary word count is not native work. [E01 §9.4; E12 v1 §T]

FACT — Scratch AdamW uses β₁=.9, β₂=.95, ε=1e-8, matrix decay=.1, no norm decay, tied embedding counted once and global norm clip=1. Master parameters, moments and gradient accumulation are FP32; working computation is BF16; TF32 is disabled. Microbatches are B16/C4. The LR schedule warms up through 200,000 canonical exposures, then continuously decays by cosine to 10% of peak at nominal 10M, without phase reset. The source context cap is 1,024; greedy output/event cap is 256 and C edit cap is 64. [E03, E05; E12 v1]

FACT — The nominal phase endpoints are 6,666,667, 9,333,334 and 10,000,000 exposures. Allocation decomposes as 15% natural reference-as-source identity, 15% generated minimal, 20% generated rules, 10% natural repair pairs and 40% frozen empirical generated corruption. These are exposure shares, not distinct-record shares. No teacher or TTS augmentation entered G1/G2 scratch training. [E03, E05; E11 §§B–C; E12 v1 §M]

## D. Canonical exposure matching and its limitations

FACT — The paper-canonical charge counts trusted framing, the clean spoken/reference anchor and the full written target under the common project tokenizer, excluding PAD. The anchor is accounting metadata and does not enter inference. B decoder length and C event length do not determine that common charge. Whole presentations are retained; stopping uses the first completed master queue reaching nominal 10M. [E01 §10.4; E03, E05]

MEASURED RESULT — G1's six runs share 134,591 ordered presentations and 10,007,223 actual exposures at 305 updates. Ledger SHA-256: `21c3f5838f5c7e85f258e8eef25b2b38884a2023199afc5d1852d68155b04f2f`. G2 D0 preserves that extent. G2 D1 has 136,755 presentations and 10,006,223 actual exposures; ledger SHA-256: `4927980826095d6e2f5d74f37c17d43e233acf3356ccb99d16a1930b29b3a60f`. Matching is exact across arms and U conditions within D. Cross-D actual exposure differs by 1,000; no cross-D ledger equality is claimed. [E03–E05, E10]

INFERENCE — This controls presented examples and declared charge within D. It does not equalize FLOPs, padded computation, native supervision, optimization difficulty or elapsed time. C's loss and renderer are part of the treatment. ByT5's pretrained information, native byte interface, natural-only adaptation and budget differ; its comparison is descriptive task feasibility, not a matched scratch-versus-pretrained experiment. [E08, E12 v1 §§P–Q, v2 §L]

## E. Dataset provenance and source-only inference contract

FACT — Natural examples join LibriSpeech audio to LibriSpeech-PC restored reference material and frozen Parakeet 1-best hypotheses. The LS-PC manifest archive is content-pinned by SHA-256 `96d4eae2222b29b66437a21959252419bcd4762e5042e71e023790171054d1c0`; the source record distinguishes `text_raw` from normalized `text`. LS-PC and parent LibriSpeech declare CC BY 4.0, with attribution retained in the source records. The recognizer is `mlx-community/parakeet-tdt-0.6b-v3`, revision `ed2b7e8c15f9aaa0b5772e2efb986255eaef7e15`, qualified runtime `parakeet-mlx-0.5.2-frame-bound-v1-single-fp32-wave-bf16-weights`. Upstream pretraining overlap remains unknown. [E13; E12 v4 §H]

FACT — The predeclared G2 census contains 14,113 TRAIN records in 314 source groups, 1,900 CAL in 40 groups and 796 HPO DEVELOPMENT in 12 groups. Admission includes 2–12-second source runtime eligibility, source-family closure and role separation. D0's 1,024 pairs are a source/target-hash subset of D1. The fixed generated pool, latent identities and corruption profile remain unchanged. Public receipts retain hashes and aggregate counts; they do not redistribute transcript/reference payloads. [E05, E11 §A, E13]

FACT — Inference receives raw one-best recognizer text plus only the registered trusted task framing; ByT5 receives raw text without a prefix. No reference, gold edit, latent annotation, audio, recognizer confidence, N-best list, corpus role or speaker identity enters correction inference. TRAIN reference-as-source identity examples are explicitly a training view, not extra inference information. CAL/HPO references have been consumed for development evaluation and research decisions; neither population can become untouched validation. [E01 §9.1; E08; E11 §I; E12]

## F. Generation-1 experimental design

FACT — Six registered seed-42 recipes cross B100/C101 with peak LRs {1e-4, 3e-4, 6e-4}. Architecture-specific initial parameter and optimizer identities match across LRs; no inherited trained weights are used. Each run completes the same 305 queues at 10,007,223 exposures. Evaluations are fixed at initialization and first completed queues reaching 1M, 3M, P0 end, P1 end and 10M. All six slots completed attempt01; no recorded scientific numerical replay or interruption occurred. [E03–E04]

FACT — The fixed panel contains 108 LS-PC natural DEVELOPMENT cases, 2,270 reference words and 64 RAW source errors, plus 288 generated cases. Generated views each have 96 cases; genuine repair-bearing cases number 192 and required repair fields number 288. The five endpoint-only gates require completion, natural WER below RAW, positive completed natural repair, repair supported in at least two groups and genuine generated required repair. Only eligible endpoints may enter the within-arm LR ranking. DET was unmeasured on this panel. [E03–E04]

## G. Generation-1 measured results

MEASURED RESULT — Natural RAW is 64/2,270 = 2.819383% WER. Repair and introduction columns are alignment-bound counts on the same 108 cases; completed repair is divided by 64 source errors when reporting rates, introductions by 2,270 reference words. [E03 descriptive tables; E04]

| Arm / peak LR | Natural errors / 2,270 | WER % | Completed repair | Introduced errors | Generated conformance / 288 | Genuine repaired cases / 192 |
|---|---:|---:|---:|---:|---:|---:|
| B100 / 1e-4 | 2,208 | 97.268722 | 6–6 | 2,150–2,150 | 0 | 0 |
| B100 / 3e-4 | 2,584 | 113.832599 | 2–2 | 2,522–2,522 | 0 | 0 |
| B100 / 6e-4 | 2,664 | 117.356828 | 2–2 | 2,602–2,602 | 0 | 0 |
| C101 / 1e-4 | 121 | 5.330396 | 0–0 | 57–57 | 131 | 49 |
| C101 / 3e-4 | 128 | 5.638767 | 0–0 | 64–64 | 149 | 79 |
| C101 / 6e-4 | 109 | 4.801762 | 0–0 | 45–45 | 132 | 54 |

MEASURED RESULT — Both eligible rankings are empty and both selected LRs are null. All B endpoints fail natural WER and generated repair; all C endpoints fail natural WER, completed natural repair and repair-support gates. C generated learning cannot substitute for natural restoration. The original disposition is `CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE`. [E03–E04]

INFERENCE — B's 1e-4 output undergenerates; the larger LRs rewrite destructively. C's natural behavior is predominantly copying, with zero completed natural endpoint repairs. This is not literal all-case identity collapse or architecture impossibility. G1 lacked TRAIN greedy diagnostics, so reduced teacher-forced loss alone cannot distinguish memorization from free-generation failure. [E03; E12 v1 §§B–D]

## H. Generation-2 factorial experimental design

FACT — Frontier v1 prospectively bound two factors within each arm: D0 original 1,024 natural pairs versus D1 qualified 14,113-pair census; U1 one optimizer update per 32,768-anchor whole-presentation master queue versus U8 eight contiguous complete subupdates of that same queue. U8 cuts at the first whole-presentation boundary satisfying `8C >= jQ`, j=1…7, and ends at the same master endpoint. It is not an exact 4,096-anchor threshold. Each actual update uses its own denominators, clipping and optimizer step. [E05; E12 v1]

FACT — The archived G1 3e-4 D0-U1 runs are compatibility-qualified controls, rescored on the expanded panel without retraining. Six new B/C cells use fixed peak LR3e-4, chosen as the central qualified setting rather than a G1 winner. D1-U8 is the predeclared joint-intervention adequacy candidate; other cells and intermediate states are descriptive. U1 has 305 updates and U8 2,440, within each D. [E05–E07]

FACT — All 2,984 cases are retained: 2,696 natural, with 50,926 reference words, 1,413 RAW errors and 52 groups; 288 generated. Natural cases include 878 lexical-error and 1,818 lexical-zero cases; all 1,900 CAL and 796 HPO cases. Legacy108/new2588 and clean/other subsets are reported separately and overlap other subsets. Split names beginning with `train` describe heldout source provenance, not student TRAIN diagnostic reuse. [E06–E09]

FACT — D1 changes diversity, error prevalence and composition together. U8 bundles update frequency, normalization, clipping, moment evolution, weight-decay applications, gradient noise and LR sampling. The factorial contrast therefore does not isolate sample count or optimizer-step count alone. Six registered observations per new scratch run and separate 304-case TRAIN diagnostic panels are frozen in advance. [E05, E12 v1]

## I. Generation-2 measured results

MEASURED RESULT — RAW is 1,413/50,926 = 2.774614% WER. All eight cells use that same expanded natural denominator; archived controls retain their historical G1 outcomes separately. Bracketed WER intervals are descriptive 95% source-group sampling intervals in percent. Repair/introduction ranges are alignment bounds. [E06–E09]

| Arm / D-U cell | Output errors | WER % | 95% WER interval % | Completed repair / 1,413 | Introduced errors / 50,926 |
|---|---:|---:|---|---:|---:|
| B100 D0-U1, archived | 58,493 | 114.858815 | [112.965125, 116.940350] | 76–77 | 57,156–57,157 |
| B100 D0-U8 | 63,344 | 124.384401 | [120.576000, 128.539106] | 66–69 | 61,997–62,000 |
| B100 D1-U1 | 56,572 | 111.086675 | [109.312852, 112.930836] | 85–88 | 55,244–55,247 |
| B100 D1-U8 | 16,997 | 33.375879 | [32.279222, 34.370571] | 44–45 | 15,628–15,629 |
| C101 D0-U1, archived | 2,461 | 4.832502 | [4.346289, 5.371956] | 5–6 | 1,053–1,054 |
| C101 D0-U8 | 3,173 | 6.230609 | [5.597195, 6.886230] | 9–9 | 1,769–1,769 |
| C101 D1-U1 | 5,484 | 10.768566 | [9.207387, 12.313305] | 14–14 | 4,098–4,098 |
| C101 D1-U8 | 4,095 | 8.041079 | [6.906683, 9.170769] | 18–18 | 2,702–2,702 |

CALCULATION — For a=D0-U1, b=D0-U8, c=D1-U1, d=D1-U8, interaction is `(d-c)-(b-a)`. B100's WER interaction is `-22213/25463` = −87.236382 percentage points, descriptive interval [−90.379734, −84.259554]. C101's is `-2101/50926` = −4.125594 pp, interval [−5.050752, −3.203511]. E07 also reports all data/update effects and both alignment endpoints of repair/introduction contrasts. [E07–E09]

INFERENCE — U8 helps D1 relative to U1 while worsening D0 for both arms. B's large interaction mainly reduces severe damage; it does not establish useful repair. MEASURED RESULT — Both prescribed D1-U8 candidates fail WER below RAW; B additionally fails generated genuine required repair. C completes 23 genuine generated repairs among 192 repair-bearing cases, but remains inadequate naturally. No cell becomes a winner. [E06, E10]

## J. Pretrained ByT5 comparison

FACT — `google/byt5-small`, revision `68377bdc18a2ffec8a0533fef03b1c513a4dd49d`, has 299,637,760 parameters and imported mC4 pretraining; its model card declares Apache 2.0. Its one qualified G2 recipe uses raw-source natural-only D1 adaptation, seed42, continuous batch four, ten complete passes (141,130 presentations), 35,283 updates and final batch two. AdamW β₁=.9/β₂=.999/ε1e-8/decay.01/clip1; constant LR3e-4; FP32 MPS, eager attention and disabled CPU fallback; source/target capacity and greedy output limit 512 including the registered EOS handling. No truncation, dropped row, extra pass or pass-boundary batch flush occurred. [E08, E14]

MEASURED RESULT — Nominal milestones map to the first completed update at or after each boundary. Quantitative axes must use actual presentations; the +2/+3 offsets are inside the fixed trajectory. All observations are descriptive, with only the exact ten-pass endpoint supplying adequacy. [E08–E10]

| Reporting state | Nominal / actual presentations | Update | Offset | Natural errors / 50,926 | WER % | Completed repair / 1,413 | Introduced errors / 50,926 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Initialization | 0 / 0 | 0 | 0 | 50,926 | 100.000000 | 0–0 | 49,648–49,652 |
| 2-pass nominal, first completed update at/after boundary | 28,226 / 28,228 | 7,057 | +2 | 1,534 | 3.012214 | 84–84 | 205–205 |
| 5-pass nominal, first completed update at/after boundary | 70,565 / 70,568 | 17,642 | +3 | 1,565 | 3.073086 | 105–105 | 257–257 |
| 10-pass exact endpoint | 141,130 / 141,130 | 35,283 | 0 | 1,650 | 3.239995 | 120–120 | 357–357 |

MEASURED RESULT — The endpoint completes all 2,696 natural outputs and supports completed repair in 37 groups, but fails WER below RAW. Its WER sampling interval is [2.782617, 3.756010]%. Generated outputs retain 63 capped sequences among 288, and all 288 fail structural conformance. Generated performance is descriptive for this natural-only comparator, not an added adequacy gate. [E08–E09]

## K. Repair-versus-introduced-error tradeoff

MEASURED RESULT — At the prescribed G2 endpoints, B completes 44–45 repairs while introducing 15,628–15,629 errors; C completes 18 while introducing 2,702; ByT5 completes 120 while introducing 357. These quantities have different rate denominators: 1,413 source errors for repair, 50,926 reference words for introduction. Introduced errors include new insertions as well as damage to source-correct material. [E06, E08]

CALCULATION — Raw count conservation is `eO = eS - raw_repair + introduced`. C's 20 raw repairs differ from its 18 completion-qualified repairs: `1413 - 20 + 2702 = 4095`. ByT5 gives `1413 - 120 + 357 = 1650`, or 237 more errors than RAW. Completion-gated repairs must not be substituted into raw conservation. [E01 §23; E11 §§D–E]

CALCULATION — The feasibility record finds lexical damage in 1,600/1,818 originally lexical-zero cases for B, 288/1,818 for C and 183/1,818 for ByT5. ByT5's better/equal/worse outputs number 67/2,360/269. Its beneficial outputs contain 115 repairs and six introductions; equal outputs contain five/five; worse outputs contain zero/346. Positive repair alone does not establish utility. [E11 §D; partial independent reaggregation in E12 v3 §B]

## L. TRAIN-versus-DEVELOPMENT generalization findings

MEASURED RESULT — Each D condition has 304 preselected TRAIN diagnostics: 64 natural lexical-error, 64 lexical-zero, 128 corresponding reference-as-source identity views and 48 generated TRAIN views. Initialization/endpoint greedy and teacher-forced diagnostics form 12 separately reconstructed states; they never enter heldout gates. [E06, E09]

MEASURED RESULT — B100 D0-U8 is lexically target-exact on all 64 selected TRAIN error cases, repairing all 113 source errors there with zero introductions, yet reaches 124.384401% WER on the 2,696-case DEVELOPMENT population. B100 D1-U8 has zero lexically target-exact outputs among its separate 64 selected TRAIN error cases. [E06, E09]

CALCULATION — C101 D0-U8 has a complete gold-span sequence on 63/64 TRAIN error cases, but 39 exact-span cases have wrong replacements; 25/64 outputs are lexically target-exact. D1-U8 returns immediate no-edit on 52/64 selected TRAIN error cases and has zero lexically target-exact outputs. On heldout D1-U8, 661/878 error-bearing cases return no-edit and none of those 878 outputs is target-lexically exact. [E11 §F; E12 v2 §H]

INFERENCE — These records support narrow fitting without useful transfer for B D0-U8 and distinct activation/localization/replacement problems for C. D0 and D1 diagnostic selections differ: comparing their fit is not a matched-example causal estimate. Canonical-program mismatch does not necessarily imply output mismatch. Detailed feasibility C decomposition was not independently reconstructed in full by v3; that limitation follows the claim into the registry. [E11 §§F, J; E12 v3 §B]

## M. Exact natural repetition/exposure findings

CALCULATION — The retrospective ledger reconstruction separates natural repair from reference-as-source identity. Frontier v3 independently reaggregated the repair repetition distributions; it did not independently repeat every detailed phase, group, supervision or diagnostic-exposure calculation. [E11 §§B–C and Appendices 1, 3; E12 v3 §B]

| Quantity | D0 | D1 |
|---|---:|---:|
| Distinct natural repair records | 1,024 | 14,113 |
| Repair presentations | 18,693 | 19,538 |
| Records with zero repair presentations | 0 | 0 |
| Exact repair repetition | 763 × 18; 261 × 19 | 8,688 × 1; 5,425 × 2 |
| Mean presentations per record | 18.254883 | 1.384397 |
| Natural repair canonical charge | 1,000,665 | 1,000,628 |
| Error-bearing records / presentations | 334 / 6,102 | 5,373 / 7,390 |
| Error-bearing canonical charge | 366,186 | 421,428 |
| Reference-as-source identity presentations | 28,040 | 29,365 |
| Identity repetition | 632 × 27; 392 × 28 | 12,974 × 2; 1,139 × 3 |
| Identity canonical charge | 1,501,032 | 1,501,003 |
| First full natural repair pass, ending exposure | 547,635 | 7,218,011 |
| Charge-based natural pass equivalents | 18.256312 | 1.386247 |

INFERENCE — D1 expands diversity under approximately fixed natural charge, with about 13.2 times less average repetition. Its first full natural pass completes after P0. This is evidence of limited learning opportunity, not evidence that more passes would produce useful transfer or that larger corpora generally fail. Presentation means and charge-based pass equivalents differ because record lengths differ. [E11; E12 v2–v3]

## N. Cached-proposal oracle feasibility calculations

CALCULATION — The accepted oracle chooses only RAW or the fixed complete endpoint proposal, using the reference to compare error counts. For incomplete outputs it chooses RAW. Its gain is `sum_i 1[complete_i] max(0, eS_i-eO_i)`, also reconstructed as RAW total minus the sum of per-case minimum errors. It neither constructs new text nor selects a checkpoint. [E11 §E; E12 v2 §I, v3 §B]

| Fixed endpoint | Better / equal / worse, of 2,696 | Beneficial complete cases | Beneficial groups | Removable errors | Oracle errors / 50,926 | Oracle WER % |
|---|---|---:|---:|---:|---:|---:|
| B100 D1-U8 | 2 / 297 / 2,397 | 2 | 2 | 2 | 1,411 | 2.770687 |
| C101 D1-U8 | 3 / 2,197 / 496 | 3 | 3 | 3 | 1,410 | 2.768723 |
| ByT5 exact ten-pass | 67 / 2,360 / 269 | 67 | 36 | 109 | 1,304 | 2.560578 |

CALCULATION — ByT5's ceiling is 109/50,926 ×100 = 0.214036 WER percentage points, or approximately 7.714% of the 1,413 RAW errors. Descriptive group-bootstrap gain intervals in pp are B [0, .010418], C [0, .013181], ByT5 [.154027, .288196]. The interval calculation was recorded in E11; v3's independent reaggregation covers point gains, not a fresh full requalification of these intervals. [E11 §I; E12 v3 §B]

INFERENCE — Whole-output acceptance has negligible scratch headroom in these proposals. ByT5 has real beneficial outputs but no demonstrated source-only selector. The oracle is reference-aware and is not deployable performance or a general task-recoverability bound. Feasibility feature summaries neither fit nor select a policy; probability traces were unavailable. [E11 §§G–K; E12]

## O. Evaluation methodology and group-aware uncertainty

FACT — `lexical_eval_v1` uses strict UTF-8, Unicode NFC, versioned case folding and a fixed word scanner with declared apostrophe/hyphen handling. It does not silently perform number expansion, spelling correction or general inverse normalization. Pairwise word Levenshtein distances determine WER. The joint source/reference/output scorer retains all conditional-optimum ties and reports repair/introduction extrema. It keeps computational coverage and source-consensus preservation coverage distinct from all-case WER. [E01 §23 and Part IV; E04, E09]

FACT — Natural and generated cases have separate denominators. Invalid/capped outputs remain included; completed repair is zero for failed completion. Valid full-text capped prefixes retain their observed WER text; invalid C programs are not partially rendered. Generated fields receive success only with complete structural qualification. Legitimate empty text differs from a missing or invalid output. No candidate-dependent exclusion or fallback credit is added. [E01 §23.5; E03, E06, E08]

CALCULATION — G2 descriptive intervals use 10,000 paired source-group percentile bootstrap draws, PCG64 seed42, resampling all cases within each of the 52 groups together. Shared int64 draw-index SHA-256 is `ca7289b19fcdde43e36592843d88bc89d9aa3f2361120a120cd3df4c9ec336d0`. Independent result reconstruction reproduces the draws, fixed denominators, exact factorial fractions and intervals. These are group-sampling intervals, not alignment bounds, training-seed uncertainty, final H1 tests or a criterion to admit an otherwise failed candidate. [E07–E09]

FACT — Historical independent review reconstructed all 36 G1 evaluations (14,256 case instances); a separate dense oracle covered 11,783 cases within its fixed budget, not the remaining 2,473. G2 independently reconstructed 42 heldout panels of 2,984 cases (40 campaign observations and two archived controls), plus 12 TRAIN diagnostic states. This manuscript preparation checked public aggregates and byte identities; it did not repeat those private-data checks. [E04, E09]

## P. Native computational cost

MEASURED RESULT — G1 ran serially on Apple M5 Pro with 48 GiB unified memory, macOS 27.2, Python3.12.15, MLX0.32.3 and NumPy2.2.6. G2 costs refer to the retained qualified native scratch/ByT5 implementations. The wall intervals include training, saves and prescribed evaluation; their nested components are not additive charges. [E03, E08, E10]

| Generation / recipe | Physical recipe wall seconds, MEASURED |
|---|---:|
| G1 B100 1e-4 | 2,117.458817 |
| G1 C101 1e-4 | 5,360.392531 |
| G1 B100 3e-4 | 2,255.100029 |
| G1 C101 3e-4 | 5,544.691853 |
| G1 B100 6e-4 | 2,468.490537 |
| G1 C101 6e-4 | 5,382.778655 |
| G2 B100 D0-U8 | 10,286.654194 |
| G2 C101 D0-U8 | 9,010.581726 |
| G2 B100 D1-U1 | 7,276.738185 |
| G2 C101 D1-U1 | 8,864.873318 |
| G2 B100 D1-U8 | 8,631.517741 |
| G2 C101 D1-U8 | 8,189.656452 |
| G2 ByT5 exact ten-pass | 79,862.099614 |

CALCULATION — G1's six physical intervals total 23,128.912421 seconds = 6.424698 hours; G2's seven total 132,122.121229 seconds = 36.700589 hours. Archived controls add no new training to G2. G1's separately measured operational span is 25,879.683465 seconds, including review/publication pauses; G2 all-in operational span is unmeasured. [E03, E10]

MEASURED RESULT — ByT5 logged training totals 21,143.834539 seconds. Its four observation wall intervals are 8,525.970953, 7,214.049868, 10,059.125263 and 7,074.588477 seconds, respectively at actual presentations 0/28,228/70,568/141,130. Decode components are 7,901.264797/5,343.791777/7,636.503629/4,916.474747 seconds; scorer components 5.389383/11.141651/14.241679/10.757864. All are already inside recipe wall time. Their remainder is not newly assigned to a named cost category. [E08, E10]

FACT — G1 synchronized update host intervals, decode positions/times and memory peaks are available in E03; they are not exact device kernel traces. Independent G2 reconstruction cost is separate (results 1,836.888611 CPU seconds, accounting 145.442976 seconds). No cloud expenditure occurred in these campaigns. Electricity, depreciation and local monetary cost are UNPRICED. Upstream pretraining cost and final-campaign cost are not established by these timings. Compact output alone does not imply lower training or complete-request cost. [E03, E09–E10]

## Q. Limitations and literature positioning

FACT — Compact editing, copying untouched content, selective correction, correction detection and synthetic ASR correction data have established precedents. The primary pages below were checked on 2026-10-10. These are related-work descriptions, not reproduced external benchmarks or direct score comparisons.

| Prior work | Established contribution and boundary for this manuscript |
|---|---|
| [Zhang, Stahlberg and Kumar, ICASSP 2025 / arXiv v1](https://arxiv.org/html/2501.13831v1) | Directly compares full ASR rewrites with compact spans and phrasal representations with deterministic expansion. A first full-versus-compact comparison claim is excluded. Output-length evidence does not itself establish this project's complete native cost. |
| [FastCorrect, NeurIPS 2021](https://proceedings.neurips.cc/paper/2021/hash/b597460c506e8e35fb0cc1c1905dd3bc-Abstract.html) | Edit-alignment-based efficient non-autoregressive correction is established; efficient structured ASR correction is not new here. |
| [PATCorrect, inspected v2](https://arxiv.org/html/2302.05040v2) | Phoneme-augmented non-autoregressive correction, detection analysis and explicit scratch training are established. Scratch specialization alone is not novel. |
| [SoftCorrect, AAAI 2023](https://ojs.aaai.org/index.php/AAAI/article/view/26531) | Soft detection and constrained CTC focus correction on detected errors. Selective correction and protection of correct tokens are established. |
| [ConstDecoder, Interspeech 2022](https://www.isca-archive.org/interspeech_2022/yang22g_interspeech.html) | Operation prediction with constrained decoding and unchanged-token copying is established. This project has no qualified reproduction arm or new algorithm claim. |
| [ECLM, inspected arXiv v2](https://arxiv.org/html/2405.15216v2) | Specialized correction models, training-data design and hallucination concerns are established. Model/data lineage and input information differ from the matched scratch pair. |
| [DARAG, Findings ACL 2025](https://aclanthology.org/2025.findings-acl.125/) | Synthetic data and retrieval-augmented correction address generalization and entities. Its extra information and data interventions are not this source-only treatment. |
| [Conservative Data Filtering, EMNLP Industry 2024](https://aclanthology.org/2024.emnlp-industry.20/) | Inferability-aware filtering and overcorrection reduction already motivate conservative correction. Conservatism alone is not a contribution. |
| [RED-ACE, EMNLP 2022](https://aclanthology.org/2022.emnlp-main.180/) | Error detection with ASR confidence embeddings is established. Those recognizer confidence features are absent from this project's correction input. |

INFERENCE — Potential supported material is narrower than capability: (i) controlled negative outcomes for the exact budgets and recipes; (ii) within-arm D/U interactions with their bundled-treatment limits; (iii) source-fidelity evidence separating mechanical copying from learned edit correctness; (iv) activation/localization/replacement diagnostics, with their reconstruction limits; (v) auditable paired presentation, scoring, failure and native-cost records. These are candidate empirical contributions, not proof of novelty, publishability or the first such study. A broad novelty/completeness claim requires a later positioning review. [E01 §3; E12 v1 §S, v2 §§P–Q]

FACT — Single-seed development results do not estimate training-seed variability. The low-error, short literary-speech panel is not a protected final equal-domain population or evidence across recognizers/domains/long inputs. The 10% natural repair share limits independent natural supervision. D1 changes composition as well as sample count; U8 bundles optimizer effects. ByT5 has different pretraining, scale and adaptation data. No eligible paired restorer exists, DET was unmeasured on the G1 panel, and Qwen/ConstDecoder are not completed task-matched scientific comparators in these campaigns. [E03, E05, E08, E12–E14]

FACT — Exact-source collision absence does not prove recoverability: most complete sources are unique. The feasibility study's local support and event-omission calculations are operational diagnostics, not semantic labels or deployable edit policies. Detailed omissions, local support and oracle intervals lack a complete new independent reconstruction in v3. Surface-only restoration and lexical identity differ; copying or normalized equivalence does not establish byte-exact reference recovery. Pretrained test contamination is unknown. [E11 §§F–J; E12 v3]

## R. Outstanding experiments and publication prerequisites

FACT — G1, G2 and the post-G2 read-only feasibility analysis are complete. Frontier v3 authorizes prospective acceptance DESIGN only. Frontier v4 identifies Mozilla Common Voice Scripted Speech 26.0 — British English, dataset ID `cmrt6zrob000zmm07yqwjlpwi`, as an alternative metadata-qualification candidate; it remains NOT QUALIFIED. Required metadata were unavailable with retained HTTP403 findings. Fresh independent data remain unavailable. This task neither updates nor interferes with that access workstream. [E11–E12]

FACT — No deployable acceptance policy has been demonstrated. The fixed reference-aware oracle cannot substitute for it. Acceptance execution and Generation 3 are NOT AUTHORIZED. Final seeds 1729/2718/31415 and protected final/sealed populations remain untouched; final 150M work, sealed inference and protocol freeze remain HELD. Nothing here changes hypotheses, margins, historical outcomes, targets or scientific scope. [E02, E10, E12]

OPEN SCIENTIFIC QUESTION — The already accepted prospective direction asks whether a fixed ByT5 proposer with source-only acceptance can meet benefit and preservation criteria on qualified independent groups, and whether candidate-versus-identity conditional scores add information beyond structural edit features. A separately authorized result resolving those questions would most improve capability-based publication viability. This is the v3 question, not a new manuscript pivot or permission to execute it. [E12 v3 §§M–O]

OPEN SCIENTIFIC QUESTION — Other unresolved mechanisms include the causal effect of more natural exposure, surface-target supervision, architecture/copying choices, training horizon and unknown textual recoverability. They require new prospective scientific decisions and controls; documentation cannot settle them. [E11 §L; E12]

FACT — Before any submission or capability claim: qualify rights/access and independent populations; retain frozen scoring and uncertainty rules; obtain the required prospective scientific scope review and separate execution permissions; complete relevant independent reconstruction, comparator and publication gates; and obtain publication authority for the resulting manuscript. The original H1 path additionally lacks useful paired models, final population readiness (including SLUE), seed evidence and final protocol freeze. This branch publication authorizes these aggregate documentation artifacts, not manuscript submission or redistribution of third-party data. [E01–E02, E12–E14]

FACT — The companion [claim and figure registry](CLAIM_AND_FIGURE_REGISTRY_V1.md) supplies supported claims, unsupported extrapolations and eight figure/table blueprints. No new chart-data extraction, model execution, scientific evidence modification or automation change occurred. Documentation/publication checks are recorded in the new preparation receipts. Historical 514 passing tests remain historical evidence; model tests were not rerun.

MANUSCRIPT_DEVELOPMENT_EVIDENCE_PREPARED
