# Post-10M Frontier Scientific Decision v1

Reviewed checkpoint: `abd8bc885ee754cb43b48d6197b8d93b011c24fb`
Date: October 6, 2026

Local HEAD and remote `main` match; the working tree is clean. This review made no repository changes, downloaded no corpus/audio payloads, made no paid API calls, and ran no models.

## A. Final disposition

**AUTHORIZE_DEVELOPMENT_GENERATION_2**

Authorize a **bounded diagnostic design**, retaining B100 and C101 and testing two interventions:

1. Expand the natural training pool from 1,024 pairs to the qualified portion of the **predeclared 14,113-record census**.
2. Replace one optimizer update per large presentation queue with **eight exposure-balanced complete updates**, while preserving that queue’s presentations and final exposure.

Use the two existing `3e-4` runs as historical control cells, subject to exact compatibility checks. This leaves **six new B/C training recipes**, plus **one separately bounded ByT5 adaptation recipe**.

Do not introduce teacher data, resize the models, modify the losses, or increase the 10M B/C exposure budget in this generation.

This is authorization of the scientific design. **Implementation, qualification, and execution occur in a later authorized session.** Launch is currently blocked by insufficient artifact storage.

## B. What generation 1 taught

**MEASURED RESULT — B100 failed as a useful full-transcript restorer under this regime.**

| Peak LR | Natural WER | Completed natural repair | Introduced errors | Generated whole-case success |
|---|---:|---:|---:|---:|
| `1e-4` | 97.269% | 6 | 2,150 | 0/288 |
| `3e-4` | 113.833% | 2 | 2,522 | 0/288 |
| `6e-4` | 117.357% | 2 | 2,602 | 0/288 |

RAW was **2.819%**, or 64 errors in 2,270 reference words. At `1e-4`, B generated only 1,014 natural output words against 2,270 reference words. The higher LRs produced more text without useful preservation.

Falling teacher-forced training loss does not establish successful free generation on TRAIN. The campaign did not contain the TRAIN greedy evaluations needed to distinguish memorization, weak source conditioning, and failure during autoregressive generation.

**MEASURED RESULT — C101 learned some generated editing, but failed natural restoration.**

| Peak LR | Natural WER | Completed natural repair | Introduced errors | Generated whole-case success |
|---|---:|---:|---:|---:|
| `1e-4` | 5.330% | 0 | 57 | 131/288 |
| `3e-4` | 5.639% | 0 | 64 | 149/288 |
| `6e-4` | 4.802% | 0 | 45 | 132/288 |

C’s generated success was incomplete and concentrated. Pure-repair whole-case successes were only **6/96, 11/96, and 6/96**. Identifiers and paths had zero repaired required fields at every final LR.

C predominantly copied natural inputs, but was not universally incapable of editing. The `3e-4` run completed one natural repair at P1, then lost it by the endpoint.

All six completed the registered campaign. None was eligible. These remain permanent results.

## C. Root-cause ranking

Confidence below concerns the **causal explanation**, not whether the supporting measurements occurred.

### B100

| Rank / explanation | Evidence for | Evidence against or missing | Confidence | Discriminating diagnostic / action |
|---|---|---|---|---|
| 1. Insufficient optimization opportunity | Only 305 updates; six warmup updates; full-text generation remains unusable | Training loss falls substantially; more updates could amplify memorization | Medium | Change complete-update granularity at fixed presentations and exposure |
| 2. Insufficient natural quantity/diversity | Only 1,024 pairs, 48 groups, 334 lexical-error cases | Each pair was repeated 18–19 times; quantity alone may not solve copying | Medium | Expanded real-pair pool with architecture and allocation fixed |
| 3. Generated-domain mismatch | 75% of exposure is generated technical material; no generated heldout whole-case success | Failure also affects the deliberately supported generated task | Medium | Compare data-pool effects and TRAIN/DEV greedy behavior |
| 4. Scale excessive for available learning | Approximately 100M random parameters versus little distinct natural supervision | No controlled smaller model; literature supports similarly sized correction models with adequate training | Medium–low | Defer resizing until data/optimization contrasts are available |
| 5. Objective/free-generation mismatch | Low teacher-forced loss coexists with destructive greedy output | No demonstrated shift, mask, denominator, or serialization defect | Medium | Fixed TRAIN greedy and teacher-forced diagnostics |
| 6. Unhelpful encoder/decoder allocation or absent copy mechanism | B must regenerate every token; four decoder layers may constrain learning | C shares the backbone; other successful correction architectures also use shallow decoders | Low–medium | Retain architecture for this diagnostic; do not add a copy mechanism yet |
| 7. Undetected implementation defect | Always possible | Independent native accounting, masks, losses, checkpoints and scoring passed | Low on present evidence | Compatibility and independent reproduction; stop if a defect appears |

### C101

| Rank / explanation | Evidence for | Evidence against or missing | Confidence | Discriminating diagnostic / action |
|---|---|---|---|---|
| 1. Natural-data and domain mismatch | Generated repair appears, while natural endpoint repair is zero; only 334 distinct natural error cases | Expanded real data might still lack source-only recoverable errors | Medium–high | Expanded real-pair pool |
| 2. Insufficient optimization opportunity | 305 updates; generated repair still increases late | Natural WER is not monotonically improving; more updates may strengthen wrong edits | Medium | Same-presentation optimizer-granularity contrast |
| 3. Narrow corruption transfer | Only 20 supported character entries; 229/875 projected codepoint edit mass retained | The profile was deliberately narrow, not a claimed natural ASR simulator | Medium | Hold it fixed while testing real data; do not silently broaden it |
| 4. Learned preservation bias / weak natural edit activation | Immediate END on 88, 87, and 96 of 108 final natural cases | Gold action labels were **61.19% EDIT**, not majority END; C does edit | Medium | Natural TRAIN versus DEV edit/repair diagnostics |
| 5. Objective weighting or surface-label competition | Many lexically correct natural pairs still require byte-level formatting edits | Current four-component objective learns generated tasks; no causal weight trial exists | Low–medium | Retain weights; report lexical versus surface supervision |
| 6. Excess model capacity | Approximately 101M parameters with little distinct natural data | No size comparison; successful generated learning argues against total incapacity | Low–medium | Defer resizing |
| 7. Pointer/event architecture inadequate | Localization errors could obstruct natural corrections | Valid nonempty programs and genuine generated repairs exist | Low on present evidence | Retain representation and renderer; inspect fixed diagnostic outputs |
| 8. Evaluation too small | Only 31 error-bearing natural cases and 64 RAW errors | Small-panel uncertainty cannot explain away observed damage or B’s catastrophic WER | High as a precision limitation; low as the sole failure explanation | Expand DEVELOPMENT prospectively |

The evidence supports **data and optimization as competing explanations**. It does not establish a single dominant cause or justify an architectural rescue.

## D. Was 305 updates / 10M exposure adequate?

**Adequate for the registered viability screen; inadequate for declaring the architectures incapable or converged.**

The actual units were:

| Quantity per recipe | Observed |
|---|---:|
| Canonical exposures | 10,007,223 |
| Whole presentations | 134,591 |
| Optimizer updates | 305 |
| B target/EOS positions | 4,445,162 |
| C event positions | 1,492,422 |
| Natural-pair presentations | 18,693 |
| Distinct natural pairs | 1,024 |
| Distinct natural lexical-error pairs | 334 |

Canonical exposure is `anchor BPE + target BPE + 5`. It is neither unique text nor native decoder supervision.

At the original update scale, 150M would yield approximately **4,578 updates**, not an automatically adequate optimization budget.

Relevant literature provides context, not a universal minimum:

| Work | Relevant training context |
|---|---|
| Original Transformer | 65M base model; 4.5M translation pairs; approximately 25k source and 25k target tokens per batch; 100k updates; 4k-step warmup. Different task, but clearly a different optimization scale. |
| PATCorrect | Scratch training on about 1.17M transcription examples for 30 epochs; 5,000-token maximum batches; six-layer text and phoneme encoders and joint decoder. |
| FastCorrect | Six-layer encoder/decoder, width 512; 400M pseudo-training sentences; 30 pretraining and 20 adaptation epochs; reported 12,000-token batches. |
| ECLM | Includes a 69M encoder–decoder, alongside larger models; tens of millions of synthesized examples, 160k-token batches, and a schedule measured in hundreds of thousands of steps. |
| Zhang–Stahlberg–Kumar | Adapts pretrained PaLM 2 models using frozen USM transcripts. It does not establish scratch learnability from a small natural pool. |

Generation 2 therefore tests a substantial optimization change **without assuming that 2,440 updates will establish convergence**.

## E. Data-supply verdict

**Insufficient natural diversity is a plausible primary bottleneck, especially for C. It is not yet a demonstrated primary cause.**

Natural lexical-error presentations numbered 6,102: approximately **4.53% of all presentations**, repeatedly drawn from 334 cases. Meanwhile, 106,782 presentations repeated already-seen source bytes.

The profile’s **875** denotes projected **codepoint** edit distance, not word errors. Its retained 229 units and 20 entries cannot represent the full natural error distribution.

Expanding real data tests something materially different from replaying the same pairs longer.

## F. Real LS-PC expansion verdict

**Choose real LS-PC expansion as the primary data intervention.**

Independent reconstruction of the existing role manifest gives:

| Role | All eligible-role rows | Within qualified 2–12s duration | Groups | Speakers |
|---|---:|---:|---:|---:|
| TRAIN | 45,729 | **14,113** | 314 | 420 |
| CAL | 6,271 | **1,900** | 40 | 56 |
| HPO | 898 | **796** | 12 | 12 |

These are **candidate counts**, not a newly qualified audio corpus.

The TRAIN census contains 325,630 target BPE tokens and **721,825 canonical exposures per full pass**. Its maximum target length is 56 BPE tokens. This selects the corpus size from actual support, rather than choosing an arbitrary 10k or 50k target.

Use:

- Existing closed source-family roles without reassignment.
- Unchanged released `text_raw` references.
- The pinned, repaired Parakeet runtime, single unchunked 2–12s mono 16kHz PCM16 FLAC.
- Existing hypotheses for the original 1,024 TRAIN and 108 DEVELOPMENT cases, byte-for-byte.
- **13,089 new TRAIN and 2,588 new DEVELOPMENT hypotheses.**

The missing official training archives total **53,642,979,491 bytes**. Only 417 additional TRAIN cases are available from the already-local `train-clean-100` archive; those add no new source groups. Restricting expansion to that archive would not adequately test the diversity hypothesis.

LS-PC supplies read literary speech. Expansion does **not** create conversational, medical, or recognizer-independent coverage. Both releases are CC BY 4.0; retain attribution and archive identities.

Any missing audio, incompatible format, numerical failure, capacity failure, or lineage contradiction blocks census qualification. **No replacement, outcome-based exclusion, or automatic smaller corpus is authorized.**

## G. Luna / Batch augmentation verdict

**Defer teacher generation from generation 2. Authorized teacher candidates: zero.**

Its monetary cost is attractive. Its scientific value is less certain than the available real-data intervention, and introducing it now would add teacher-language and corruption-process factors to the diagnostic.

Current official documentation verifies:

- API identity: **`gpt-6-luna`**.
- Responses API, structured outputs, and Batch support.
- `reasoning.effort: "none"` is supported.
- No separate dated snapshot is documented on the model page.
- Batch pricing: **$0.05/M input tokens and $0.25/M output tokens** under the ordinary short-context tier.

Account-specific access was not tested.

Because teacher generation is excluded, no production prompt, prompt hash, sampling configuration, domain quotas, or generation schema is being falsely presented as frozen. Those fields are **NOT APPLICABLE—ZERO REQUESTS** in the generation-2 manifest.

## H. Four-strategy corpus comparison

| Rank | Strategy | Principal strength | Principal limitation | Decision |
|---|---|---|---|---|
| **1** | Real LS-PC audio → existing Parakeet → released reference | Real speech and actual recognizer errors; established reference and grouping lineage | Read-speech domain; acquisition and source qualification required | **Primary generation-2 intervention** |
| **2** | Luna clean seeds → TTS → Parakeet | Target exists before corruption; recognizer produces the observed hypothesis | TTS realization errors, voice/prosody bias, teacher-language distribution; intended text is not independently verified acoustic truth | Best subsequent synthetic candidate; **deferred** |
| **3** | Luna clean seeds → frozen deterministic corruption | Cheap linguistic diversity and exact construction lineage | Current 20-entry profile is a narrow character treatment; ordinary prose generally lacks the generated grammar’s unique inverse | **Deferred**, requiring a separately defined natural-corruption contract |
| **4** | Direct Luna noisy/clean pairs | Cheap and easy to produce | Teacher defines both the error and its correction; plausibility and recoverability are teacher assertions | **Reject as primary supervision** |

The second strategy has genuine precedent. DARAG already uses LLM/TTS-generated augmentation, so this pipeline would not itself be novel.

Cheap synthetic text is an option, not evidence that it is the right next intervention.

## I. Teacher-lineage claim boundary

For the recommended generation, use this manuscript interpretation:

> Both restoration students are randomly initialized and receive the same downstream presentation ledger within each treatment. Natural hypotheses are produced by a frozen pretrained Parakeet recognizer. Neither restoration student loads pretrained language-model weights. The overall pipeline is therefore not pretrained-model-free.

If teacher text is introduced later, add:

> Part of the downstream training corpus is generated by a pretrained language model. “Trained from scratch” describes student parameter initialization, not the provenance of all training information.

A later teacher extension must prohibit benchmark-conditioned prompts, student-failure-driven regeneration, and access to protected references or identifiers. It must deduplicate against TRAIN, DEVELOPMENT, protected populations through an isolated firewall, stress targets, and other teacher seeds.

Exact and near-duplicate filtering reduces known overlap; it cannot establish that a pretrained teacher never encountered benchmark material.

## J. Model-size verdict

**Retain both existing sizes for generation 2.**

| Candidate | Judgment |
|---|---|
| 20–40M | Potentially cheaper and easier to optimize, but a large capacity intervention without a controlled causal basis |
| 40–70M | Plausible future comparison; successful models in this range do not establish adequacy on this corpus |
| Existing approximately 100M | Retain to isolate the proposed data and optimizer interventions |

No evidence currently distinguishes “too many parameters” from “too few useful updates and too little diverse supervision.”

A smaller model might be the right eventual choice. Adding it now would require another experimental factor or would confound any improvement.

## K. B architecture verdict

**Retain bare B100.**

Exact definition:

- 8 bidirectional MHA encoder layers.
- 4 causal GQA decoder layers with cross-attention.
- Width 768; 12 query heads; 4 decoder KV heads; head width 64.
- SwiGLU width 2,048.
- Vocabulary 16,384; tied embedding/readout.
- Existing pre-RMSNorm, RoPE, masks, initialization and native implementation.
- **100,686,336 parameters.**

Do not rebalance encoder/decoder depth or add a pointer-generator/copy objective.

Adding a copy mechanism could improve B, but it would change the comparison from the current bare full-transcript generator. The immediate missing evidence is whether the existing B can generate correctly on its own training examples under a more useful optimizer regime.

## L. C architecture/objective verdict

**Retain C101 and all four loss coefficients at 1.**

C retains the B backbone, 128-wide start/end pointer projections, three-way action head and three classifier biases: **101,081,859 parameters**.

Keep event serialization, pointer feedback, legal UTF-8 boundaries, monotonic edits, deterministic copying, and invalid-program treatment unchanged.

Do not add focal loss, detection heads, edit bonuses, END penalties, or loss reweighting. Majority-END supervision is not supported by the measured action counts.

## M. Curriculum verdict

**Retain 30/20/10/40 for this diagnostic, deliberately.**

| Channel | Canonical-exposure share | Function |
|---|---:|---|
| Natural identity | 15% | Exact preservation and full-text copying |
| Generated minimal | 15% | One certified repair |
| Generated rules | 20% | Controlled repair/preservation combinations |
| Real Parakeet/reference pairs | 10% | Natural recognition and surface restoration |
| Existing empirical generated corruption | 40% | Frozen supported corruption plus spoken-to-written restoration |

Under the expanded-data condition, replace **both** the natural identity pool and real-pair pool with the census. Leave generated pools, profile, and phase policies unchanged.

This is not an endorsement of 75% generated exposure as the eventual optimum. It prevents a simultaneous allocation change from obscuring the data-pool and optimizer contrasts.

A negative result would not falsify every natural-focused curriculum.

## N. Natural error/no-error sampling verdict

**No oversampling and no balancing intervention.**

Use coverage-first, record-balanced complete passes:

- Every record appears once before any record repeats.
- Preserve existing group-first ordering and deterministic hash conventions.
- Carry cursors across phases.
- Retain every naturally error-free pair.

For the old pool, the lexical-error/no-error ratio is exactly **334:690 per completed pass**.

For the expanded pool, it is exactly **`E : (14,113 − E)`**, where `E` is measured once from frozen TRAIN hypotheses before training. This is a fully specified census policy, not an implementation choice.

Report error prevalence, byte equality, group support and realized exposure separately. The larger pool changes diversity **and potentially error prevalence/domain composition**; do not call it a pure sample-count intervention.

## O. Development evaluation verdict

Freeze a new panel containing:

- **2,696 natural cases:** all 1,900 duration-eligible CAL and 796 HPO records.
- **The unchanged 288 generated DEVELOPMENT cases.**
- Total: **2,984 cases**.

The old 108 natural IDs are included. Their source/reference bytes and lineage must also match exactly.

Report separately:

1. Full natural panel.
2. Legacy 108-case subset.
3. Newly added 2,588 cases.
4. CAL versus HPO and clean versus other source splits.
5. Generated populations and their three views.

Do not balance or select DEVELOPMENT cases by error severity. Preserve all invalid, capped, abstained and incomplete outputs.

Before any student training, require the expanded natural panel to contain at least **200 lexical-error-bearing cases across 20 source groups**, and **200 lexically correct cases**. This is a prospective diagnostic-support floor, **not a power calculation**. If it fails, stop; do not add cases.

Keep greedy decoding, 256-position generation/event caps, C’s 64-edit cap, scorer and failure mapping unchanged.

For descriptive uncertainty, use 10,000 paired source-group bootstrap draws, PCG64 seed 42, shared across contrasts. Resample the 52 groups with replacement and retain all their cases. Report percentile intervals separately from alignment bounds. They do not capture training-seed uncertainty or establish H1.

## P. Training-budget verdict

**Keep nominal 10M canonical exposures per new B/C recipe. Change update granularity as an experimental factor.**

For each data condition, first freeze its ordinary 32,768-anchor whole-presentation master queues.

- **U1:** one optimizer update per master queue.
- **U8:** eight contiguous complete optimizer updates per master queue.

For a master queue of charge `Q`, cut after the first whole presentation satisfying:

`8C >= jQ`, for `j=1,...,7`

where `C` is cumulative charge within that queue. The eighth subqueue ends at the original master endpoint.

On the existing ledger, this gives exactly:

- **305 master queues**.
- **2,440 optimizer updates**.
- Subqueue charges **3,887–4,283**.

This is **not** an exact 4,096-anchor threshold.

Evaluate, save routinely, and stop at master endpoints after all eight updates. Thus U1 and U8 consume exactly the same ordered presentations and exposure within each data condition.

The intervention bundles update frequency, clipping, gradient noise, LR sampling, moment horizon, weight decay, and normalization granularity. Its result cannot identify “step count alone.”

## Q. Comparator verdict

**Reserve one new ByT5 adaptation recipe before any final scratch investment.**

Use:

- `google/byt5-small@68377bdc18a2ffec8a0533fef03b1c513a4dd49d`.
- Existing official native byte interface and 299,637,760-parameter model.
- Raw source, no textual prefix.
- All 14,113 qualified TRAIN pairs.
- Seed 42; batch four; **10 complete record passes**.
- **141,130 presentations; 35,283 updates**, including a final batch of two.
- Constant LR `3e-4`.
- Existing ByT5 AdamW: β₁=.9, β₂=.999, ε=`1e-8`, decay=.01, clip=1.
- FP32 MPS, eager attention, CPU fallback disabled.
- Existing 512-byte source/target capacities and 512-position greedy cap.

All candidate reference targets fit 512 bytes. New ASR-source capacities remain unqualified. An overflow blocks admission; do not silently truncate or exclude.

Save/evaluate at initialization and after 2, 5 and 10 passes; endpoint-only adequacy. The existing runner’s 600-update/900-second limits must be explicitly replaced in a separately qualified generation-2 runner.

Minimum useful comparator evidence: completion without unresolved failure, natural WER below RAW, positive completed-repair lower bound, and repair in at least two source groups. Report preservation and generated results, but do not require generated success from this natural-only adaptation.

This comparator receives a different training distribution from B/C. It tests natural-task feasibility; it is not a matched-training scratch-versus-pretrained headline comparison.

## R. Paper-scope verdict

Choose **Option A: repair the controlled experiment through richer real data and a diagnostic second generation**.

Retain the prospective question:

> Under explicitly matched downstream presentations and source exposure, how do full-transcript generation and compact editing with deterministic copying differ in useful repair, introduced errors, preservation, and complete native cost?

Do not pivot now to “C wins,” compact-preservation superiority, or a publishable negative result. C has not demonstrated endpoint natural repair.

Final populations, H1 margins, SLUE requirements, final seeds and protocol freeze remain unresolved and unchanged. Generation 2 does not authorize narrowing final populations to obtain success.

## S. Novelty verdict

The defensible contribution remains **controlled attribution and measurement**, not the invention of compact rewriting or synthetic correction data.

- **Zhang–Stahlberg–Kumar:** already compares full and compact ASR rewrite representations. No first-comparison claim.
- **PATCorrect/FastCorrect:** already establish efficient structured correction. Their input information, alignment mechanisms and training scales differ from this controlled pair.
- **ConstDecoder/SoftCorrect:** already exploit selective correction and detection. ConstDecoder uses pretrained BERT; SoftCorrect also uses multiple hypotheses and specialized objectives.
- **ECLM/DARAG:** already establish synthetic speech or teacher-assisted correction pipelines.

The remaining opportunity is a reproducible scratch-student comparison with matched presentations, failure-inclusive repaired/introduced-error accounting, and actual native cost. That opportunity is worth one bounded diagnostic generation. It is not yet evidence of a viable paper.

## T. Exact DEVELOPMENT_GENERATION_2 specification

### Experimental cells

Use fixed peak LR **`3e-4`** because it is the original central, BENCH-qualified setting—not because it won generation 1. No LR is selected from the failed campaign.

| Data / optimizer condition | B100 | C101 |
|---|---|---|
| D0: original pool; U1: original update | Existing G1 `3e-4` control | Existing G1 `3e-4` control |
| D0: original pool; U8: eight updates | New recipe | New recipe |
| D1: expanded census; U1 | New recipe | New recipe |
| D1: expanded census; U8 | New recipe | New recipe |

Historical controls require identical scientific behavior and separately labelled generation-2 evaluations. Their generation-1 eligibility remains unchanged.

### Normative bindings

| Item | Binding |
|---|---|
| A. Question | Effects of the natural-pool expansion, complete-update granularity, and their interaction within each arm |
| B. G1 lesson | Neither arm viable; B destructive, C generated learning without natural endpoint repair |
| C. Changes | D1 natural pools; U8 update granularity; expanded DEVELOPMENT; fixed diagnostic panels |
| D. Fixed | Architecture, initialization, tokenizer, source-only boundary, renderer, loss coefficients, optimizer settings, generated data/profile, allocation, phase policy, decoding/scorer |
| E–G. Architectures/counts | Exact B100/C101: 100,686,336 / 101,081,859 |
| H. Initialization | Fresh seed42; zero optimizer state; no inherited trained weights |
| I. Real corpus | Predeclared 14,113 TRAIN census, subject to complete qualification; no substitutions |
| J–N. Teacher corpus/schema/API/QC/grouping | Not applicable; zero teacher requests and zero teacher-derived examples |
| O. TTS share | Zero |
| P. Generated corruption | Existing 40% empirical channel; unchanged profile and generated pool |
| Q. Allocation | Exact 15/15/20/10/40 decomposition |
| R. Natural sampling | Complete record-balanced passes, no error oversampling |
| S. Repetition/grouping | Existing source groups and shared lineage; deterministic pass cursors; no phase restart |
| T. Losses | Existing B target/EOS mean; C component means with coefficients 1; omit zero-count components |
| U. Optimizer | AdamW β₁=.9, β₂=.95, ε=`1e-8`, matrix decay=.1, no norm decay, tied embedding once, global clip=1 |
| V. LR | Single peak `3e-4`; no grid |
| W. Geometry | U1/U8 as defined above; B16/C4 microbatches within each actual complete update |
| X. Steps | D0-U8 exactly 2,440; D1-U1 exactly its frozen master count `N1`; D1-U8 exactly `8N1` |
| Y. Exposure | First completed master queue reaching nominal 10M; no truncated final queue |
| Z. Phases | P0 6,666,667; P1 2,666,667; P2 666,666 nominal exposures; existing whole-presentation phase assignment |
| AA. Evaluation | Fixed 2,984-case panel; six nominal endpoints; master-endpoint mapping |
| AB. Eligibility | Existing five viability conditions applied prospectively to the expanded panel; no intermediate selection |
| AC. New recipe maximum | Six B/C plus one ByT5 |
| AD. Stops | As defined below; no automatic replacement recipes |
| AE. Before final training | Both-arm natural adequacy, credible comparator, independent reproduction, final population/power/scope/cost review and separate authorization |

The expanded ledger’s exact `N1`, exposure, ordinals and hashes must be computed and frozen before training. This is deterministic accounting, not a choice delegated to the implementer.

### Additional exact rules

**LR:** linear warmup through 200,000 canonical exposures, then the original continuous cosine to `3e-5` at nominal 10M. Compute LR at each actual optimizer update’s completed exposure. No resets or batch-size LR scaling.

**Precision:** unchanged FP32 master parameters, moments, accumulation and sensitive accounting; approved BF16 working computation; TF32 disabled.

**Denominators:** compute B or C denominators for the actual optimizer update. U8 therefore uses subqueue denominators. Do not retain large-queue denominators, add a second division, or multiply gradients to imitate U1.

**Matched exposure:** equality is exact across arms and U settings **within D**. Across D, actual endpoint overshoot and scheduler interleaving may differ. Report those differences rather than claiming identical cross-D ledgers.

**Saves:** initial state; first master endpoint reaching every million and both phase boundaries; deduplicate. Preserve full optimizer/resume state and verified atomic publication.

**Evaluations:** nominal `0, 1M, 3M, P0 end, P1 end, 10M`, mapped to master endpoints. The expanded panel must also be used for the archived control checkpoints, in new receipts.

**Diagnostic panels:** freeze before training, separately from heldout metrics:

- 64 natural TRAIN lexical-error records and 64 lexical-zero records, selected by the smallest SHA-256 of canonical JSON `["G2",42,data_condition,stratum,stable_id]`.
- Their 128 reference-as-source identity views.
- One generated TRAIN base per category and cell 0–2, selected by the same hash rule from bases actually present in the frozen training ledger; evaluate its clean and mixed views: 48 cases.
- Total **304 diagnostic cases per data condition**.
- Evaluate at initialization and endpoint. Report greedy fit/copy behavior and teacher-forced component losses separately. Identity-view outputs do not count as natural heldout repair.

**Analysis:** calculate data effects at each U, optimizer-regime effects at each D, and the difference-in-differences interaction. Keep arms separate. Do not select a winning cell by subjective inspection.

D1-U8 is the predeclared joint-intervention adequacy candidate. Success still leads to frontier review, not final training. Other cells explain effects; they are not an unregistered model-selection menu.

## U. New data-generation budget

The later qualification stage may construct:

- **15,677 new unique ASR hypotheses**.
- One deterministic replay of **64 preselected new records**, 32 TRAIN and 32 DEVELOPMENT, selected before recognition by stable-ID hash.
- Maximum **15,741 source-recognizer calls**.
- Zero teacher calls.
- Zero TTS calls.
- Zero quality-driven regeneration.

The original 1,132 hypotheses are reused unchanged.

Freeze request IDs before recognition. Keep failures and stop on qualification failure; do not redraw.

## V. New neural recipe budget

Execution order, once separately released:

1. `G2-B100-D0-U8-seed42-lr3e-4`
2. `G2-C101-D0-U8-seed42-lr3e-4`
3. `G2-B100-D1-U1-seed42-lr3e-4`
4. `G2-C101-D1-U1-seed42-lr3e-4`
5. `G2-B100-D1-U8-seed42-lr3e-4`
6. `G2-C101-D1-U8-seed42-lr3e-4`
7. `G2-ByT5-D1-10pass-seed42-lr3e-4`

Each B/C recipe answers one cell of the factorial comparison. ByT5 tests whether richer natural supervision supports useful correction with pretrained linguistic knowledge.

No alternative seed, additional LR, architecture variant, longer B/C run, or replacement failed recipe exists.

The six generation-1 slots remain spent. Qualification work below is additional, explicitly accounted neural work; it must not be hidden inside the scientific recipe count.

## W. Required BENCH and qualification

Before releasing these recipes:

1. **Baseline reproduction:** reproduce the current 379-test suite in the pinned runtime. The historical authorized baseline remains 372 tests.
2. **Storage:** secure an artifact volume with at least **250 GiB free**. Do not delete or relocate existing evidence without authorization.
3. **Corpus qualification:** verify every role, family, archive/member identity, format, reference, hypothesis, capacity and original-subset byte identity.
4. **Freeze:** new corpus, evaluation, diagnostic panels, two presentation ledgers, master boundaries, subqueue boundaries and all recipe statuses as `AUTHORIZED_UNSTARTED`.
5. **Historical compatibility:** two bounded 31-update controls, one per arm at D0-U1, must reproduce the original `3e-4` first saved state and associated optimizer/consumption identity. No quality-based decisions.
6. **New geometry:** independently verify every cut, denominator, microbatch, phase and exposure. Distinguish master index, subqueue index and optimizer-step index.
7. **Checkpoint repair for the new contract:** do not reuse the G1 assertion `exposure ≥ optimizer_steps × 32768` for U8. Preserve G1 validation; implement a separately versioned G2 contract.
8. **BENCH:** one stream for each of the six new B/C configurations: five complete warmups, 100 timed complete updates, then at least 20 minutes sustained, finishing the last complete update. Cover all phases.
9. **Cold resume:** boundary and mid-update replay for each stream; finish pending work and match the next 20 complete updates exactly.
10. **ByT5 qualification:** one bounded 100-update execution/resource check for the new runner; discard those weights. Verify final short-batch and pass accounting.
11. **Costs:** measure expanded-panel decoding/scoring, source construction, save/load and new update rates; forecast with one 25% reserve.
12. **Independent admission review:** reproduce counts, identities, exposure, resume and costs from artifacts.

This bounds qualification to **six BENCH trajectories, twelve cold-replay trajectories, two compatibility controls and one ByT5 qualification trajectory**. Retain their costs and failures.

If compatibility fails, do not automatically add two replacement scientific controls. Return for review.

## X. Stop conditions

Stop the affected stage for:

- Missing or contradictory source/group/hash identities.
- Failure to qualify the full predeclared census.
- Insufficient expanded DEVELOPMENT support under the approved panel rule.
- Any change needed to ASR semantics, model capacity, renderer, loss coefficients or protected populations.
- Historical-control incompatibility.
- Nonidentical paired consumption, incorrect denominator accounting, or failed exact resume.
- Insufficient storage.
- A measured forecast above the **96-hour serialized generation-2 budget**.
- An implementation/data defect potentially invalidating outcomes.

Retain one exact replay for qualifying numerical failure; a repeated failure marks the recipe failed. An implementation defect is not a numerical replay.

Do not stop weak recipes for quality. Do not extend promising recipes.

After the prescribed outcomes, stop for frontier interpretation regardless of success. Failure of both joint-intervention arms does not authorize a teacher, resizing or objective sweep.

## Y. Cost estimate

### Teacher economics—evaluated, not authorized

Assume **500 input and 200 output tokens per candidate**, one candidate per request, and **80% acceptance**. Acceptance is an assumption, not a measured yield.

| Target accepted clean seeds | Candidate requests | Standard token cost | Batch token cost |
|---|---:|---:|---:|
| 10,000 | 12,500 | $1.875 | **$0.9375** |
| 50,000 | 62,500 | $9.375 | **$4.6875** |
| 100,000 | 125,000 | $18.75 | **$9.375** |

Batch cost is approximately **$0.00009375 per accepted seed** under those assumptions. These estimates exclude retries, longer outputs, tools, taxes and downstream processing.

Batch permits up to 50,000 requests and 200 MB per file, with a 24-hour completion window and explicit expiration handling. Account queue limits may require smaller batches. It is not a guarantee of an accepted corpus within 24 hours.

The text bill is minor. At an assumed eight seconds of audio per accepted seed, 10k/50k/100k seeds imply approximately **22/111/222 audio hours**, or **2.56/12.8/25.6 GB** of 16kHz PCM16 audio before compression. The repository’s two-utterance Kokoro timing does not qualify generation at those scales.

### Recommended real-data generation

At the measured rate of 1,120 calls in 156.586 seconds, 15,677 new calls project to **36.53 minutes of ASR-loop time**. That is an extrapolation; acquisition, extraction, checks, scoring and changed source distributions are excluded.

The missing archives require approximately 50 GiB. At present, the volume has only approximately **40 GiB free**.

### Generation-2 planning envelope

| Work | Provisional serialized allowance | Basis |
|---|---:|---|
| Six B/C training trajectories | 8 h | G1 measured training rates plus allowance; new rates unqualified |
| Expanded B/C evaluation and diagnostics | 33 h | Conservative scaling of existing panel envelopes, including historical controls |
| ByT5 training and evaluation | 15 h | Existing per-update and initial-decode measurements extrapolated |
| Qualification and cold replay | 4 h | Planning allowance |
| Source construction and processing | 2 h | Planning allowance, excluding network acquisition |
| Subtotal | **62 h** | Provisional |
| With one 25% reserve | **77.5 h** | Calculated |

This is not a measured upper bound. BENCH must replace the estimates before launch. The admission ceiling is **96 serialized hours**.

Another 78 B/C checkpoints have approximately **126 GB logical payload** at the existing format, before comparator saves and data. The 250 GiB free-space prerequisite preserves room for the complete evidence set.

The device budget appears compatible with a month **conditionally**. Researcher time, implementation effort and final-paper readiness remain unpriced. No 150M campaign feasibility claim follows.

## Z. Prospective amendment text

Post-10M Frontier Scientific Decision v1 — 2026-10-06

Reviewed checkpoint: abd8bc885ee754cb43b48d6197b8d93b011c24fb.
Disposition: AUTHORIZE_DEVELOPMENT_GENERATION_2.
Status: scientific design authorized; implementation, qualification and
scientific execution remain separate stages. No final outcomes have been seen.

Preserve all six generation-1 seed-42 recipes and their ineligible outcomes.
Do not select a generation-1 LR or relabel any run as an implementation test.

Adopt the complete Post-10M Frontier Scientific Decision v1, sections A–Y,
as the normative generation-2 DEVELOPMENT contract.

Retain exact B100/C101 architectures, initialization, tokenizer, source-only
inference, pointer/event representation, deterministic renderer, loss
coefficients, optimizer settings, precision, generated pool and lexical
corruption profile.

Define D0 as the original 1,024-pair natural pool. Define D1 as the complete
predeclared 14,113-record TRAIN census within the existing 2–12-second source
runtime envelope, subject to full qualification. Replace both natural identity
and public-real pools under D1. Retain 30/20/10/40 allocation, phase policy,
record-balanced passes and natural zero-error cases. No teacher or TTS data.

Define U1 as one complete optimizer update per original 32,768-anchor
whole-presentation master queue. Define U8 as eight contiguous subqueues cut
at the first whole-presentation boundaries satisfying 8*C >= j*Q for j=1..7.
Normalize, clip and update once per actual subqueue. Preserve exact master
endpoints for evaluation, routine saves and stopping.

Use fixed peak LR3e-4, seed42, 200,000-exposure warmup, continuous cosine decay
to 10% at nominal10M and no phase reset. Reuse the two original3e-4 D0-U1
runs only after exact compatibility qualification. Admit at most six new B/C
recipes: D0-U8, D1-U1 and D1-U8 for each arm. No LR sweep or B/C extension.

Freeze all2,696 eligible natural DEVELOPMENT cases and the unchanged288
generated cases. Preserve the original108 natural cases byte-for-byte and
report them separately. Record prospective calibration consumption. Keep
decoding, caps, scorer and failure inclusion unchanged. Do not rewrite
generation-1 evaluations or selection.

Reserve one separate ByT5 raw-source adaptation recipe on D1: official pinned
ByT5-small, seed42, batch4, ten complete record passes, constantLR3e-4 and
existing ByT5 optimizer/native-byte policies. Its35,283-update execution
requires a separately qualified runner.

Require corpus, accounting, native consumption, historical compatibility,
checkpoint/resume, BENCH, cost and independent-review gates. Require250GiB
available artifact storage and a measured forecast within96 serialized hours,
including one25% reserve.

No new scientific recipe may execute before a frozen manifest, successful
independent admission and separate owner execution authorization. No
outcome-driven corpus, LR, loss, architecture, cap or eligibility change is
permitted. Numerical replay remains one exact replay; defects stop the
affected campaign.

This amendment does not freeze paper_protocol_v2, alter final populations,
confirm H1, authorize final seeds, final150M training, sealed inference,
A100, H2, cloud spending or teacher API spending.

## AA. Sol handoff

Implement and qualify DEVELOPMENT_GENERATION_2 for Repair Without Rewrite:
A Controlled Comparison of Full-Transcript Generation and Compact Editing
Under Matched Source Exposure.

Repository: /Users/danny/Documents/Tools/LocalFlowResearch
Remote: https://github.com/scalinity/repair-without-rewrite
Required starting checkpoint:
abd8bc885ee754cb43b48d6197b8d93b011c24fb

Scope: implement the approved Post-10M Frontier Scientific Decision v1,
construct its real-data census, qualify its runtime/accounting/resume paths,
and prepare a frozen campaign for independent admission. Do not execute the
seven scientific training recipes in this session. Stop for separate owner
execution authorization after qualification.

No parallel repository-writing session is authorized by this handoff.
Own the generation-2 implementation, tests, manifests and reports. Preserve
all generation-1 files and raw evidence. Use a codex/ branch. Root makes
commits; no attribution trailers. Do not push without session authorization.

Startup:
1. Read AGENTS.md and the supplied complete Post-10M Frontier Scientific
   Decision v1 before writing.
2. Verify clean local state, remote main and exact starting SHA. If work is
   already partially implemented, inspect its immutable attempts and resume
   only verified mechanical work; never restart or replace evidence blindly.
3. Read the six completed campaign reports, both frontier design decisions,
   prospective amendments, source qualification, model/native trainer and
   checkpoint contracts.
4. Preserve the complete scientific decision verbatim as
   docs/reviews/FRONTIER_POST_10M_SCIENTIFIC_DECISION_V1.md and append its
   amendment prospectively before affected results.
5. Reproduce the379-test baseline using
   MLX_ENABLE_TF32=0 .venv/bin/python -m pytest.
6. Verify an authorized artifact destination has at least250GiB free.
   Current repository storage was insufficient. Do not delete or move
   generation-1 evidence to create space. If no suitable destination exists,
   report the storage blocker before downloading archives or running models.

Implement these fixed choices:
- Exact B100100686336 and C101101081859; seed42 fresh initialization.
- No model, renderer, objective-weight, tokenizer or corruption-profile change.
- D0 original1024TRAIN pairs; D1 all14113 existing TRAIN-role records with
  2–12s durations, preserving original pairs byte-for-byte.
- D1 affects15%natural identity and10%public-real pools. Other shares remain
  15%minimal,20%rules,40%empirical generated corruption.
- All2696 eligible CAL/HPO natural cases plus original288generated cases form
  the new DEVELOPMENT panel; preserve/report original108natural cases.
- Construct15677new ASR hypotheses using the exact narrowed repaired Parakeet
  runtime. Preselect64one-time replay cases. No outcome-based redraw, teacher
  API, TTS, new dataset, sealed payload access or human annotation.
- Retain all census records. Any source/capacity/lineage failure blocks
  qualification rather than authorizing a smaller replacement pool.
- Freeze the304-case TRAIN diagnostic panel per data condition using the
  decision's hash selection, natural/error strata and24generated bases.
- Fixed peakLR3e-4;200k-exposure warmup; original10Mcosine and phase schedule.
- U1 uses the existing32768-anchor whole-presentation master queues.
- U8 cuts each master queue into eight nonempty contiguous subqueues using
  8*cumulative_charge >= j*master_charge,j=1..7.
- Normalize B or C over each actual optimizer update; clip/apply/clear once.
  Use B16/C4 microbatches and the existing FP32/BF16 precision contract.
- Track master queue, subqueue, optimizer step and committed exposure
  separately. Preserve the G1 validator; qualify a versioned G2 contract.
- Map saves, six evaluations and10Mstopping to completed master endpoints.
  D0-U8 must have2440updates at10007223exposures. Compute and freeze D1's
  exact ledger/counts before training.
- Prepare six unstarted B/C recipes in this order:
  B-D0-U8,C-D0-U8,B-D1-U1,C-D1-U1,B-D1-U8,C-D1-U8.
  Reuse original3e-4D0-U1controls only after exact compatibility checks.
- Prepare one unstarted ByT5 recipe: pinned official ByT5-small, raw source,
  seed42,batch4,ten full D1passes,141130presentations,35283updates with final
  batch2,constantLR3e-4,FP32MPS,512native-byte capacities and existing
  ByT5optimizer settings. Qualify its new execution bounds explicitly.

Qualification authorization is bounded to the decision's source construction,
two31-update historical-compatibility controls, six5-warmup/100-timed/
20-minute BENCH trajectories, twelve cold replays, and one100-update ByT5
runner/resource check. Preserve all costs and failed attempts. BENCH weights
must never initialize scientific recipes. Run neural work serially.

Independently verify corpus membership/bytes, full ledgers, native labels,
denominators, subqueue cuts, loss accounting, initialization, atomic checkpoints
and exact cold resume. Reprice all expanded evaluations, diagnostics and
checkpoints. Use one25%reserve; block admission above96serialized hours.
Apply the expanded-panel support floor before student training.

Do not settle new scientific choices in implementation. A contradiction,
required treatment change, invalid historical control or failed census
qualification returns to frontier review. An implementation defect is not
a numerical replay. Never weaken caps, change populations, add an LR or
replace a scientific recipe.

Close out:
1. Save small public-safe manifests and reports; keep raw text/audio/weights
   in ignored artifact storage and hash-bind them.
2. Save independent qualification reviews and before/after test receipts.
   Label every unrun check unrun.
3. Freeze the full prospective campaign, with all seven new scientific
   recipes AUTHORIZED_UNSTARTED and original controls separately identified.
4. Append docs/LOG.md; realign ORCHESTRATION.html from repository evidence.
5. Scan named staged files for credentials and private identifiers; commit
   small verified steps using existing identity and no attribution trailers.
6. Report exact clean checkpoint, qualification status, storage destination,
   measured cost and remaining blockers. Do not claim execution admission
   or publication without evidence and authorization.
7. Stop before scientific recipe1, final seeds, sealed inference, protocol
   freeze, A100 or H2.

DO NOT START ANY FINAL 150M RUN.
