# Post-G2 Frontier Scientific Decision v2

Date: October 9, 2026  
Reviewed branch: `codex/g2-execution`  
Reviewed checkpoint: `609f97f31979d469ad8551d06b2c07c3513181ec`  
Qualified Generation-2 source: `2c27cff28a31ae64220df9b06094a914e94dd0f3`

## A. Final disposition

**AUTHORIZE_READ_ONLY_TASK_FEASIBILITY_STUDY**

The next investment should be a bounded analysis of retained proposals, natural supervision, and preservation decisions. **A third neural campaign is not yet justified.**

Three findings determine this decision:

1. **The scratch models lack useful proposal quality, not merely a conservative acceptance threshold.** Even a reference-aware selector choosing between RAW and each complete D1-U8 output could remove only **2 errors for B100 and 3 for C101** from the 1,413-error natural panel.
2. **ByT5 provides a stronger feasibility instrument.** The corresponding reference-aware whole-output selector could remove **109 errors**, across 36 source groups. This establishes headroom within its cached proposals, not an achievable source-only policy.
3. **Generation 2 diluted repetition substantially.** D1 repair pairs received only one or two presentations each, versus 18–19 under D0. This prevents interpreting the failed D1 endpoints as evidence against larger natural corpora generally.

The preservation-action hypothesis deserves priority, but it must distinguish **proposal generation**, **local edit quality**, and **acceptance**. “Add a gate” is inadequate as a diagnosis of the scratch results.

This decision defines the next analytical stage. It does not authorize implementation, training, new inference, spending, or automatic execution.

**FACT — repository verification.** Local HEAD and the live published review branch both equal the reviewed checkpoint. The working tree is clean. Qualified source → campaign freeze → launch → completed checkpoint ancestry holds. Published `main` is an ancestor, not a superseding result. All 47 frozen scientific-source hashes match. All seven terminal receipts record one completed scientific attempt. The continuation automation is paused.

**Verification limits.** The 514 passing tests, 82 checkpoints, 40 observations, 42 reconstructed heldout panels, and 12 TRAIN diagnostic states are supported by the retained reports and independent receipts; this review did not rerun the suite or rehash every checkpoint. Selected ledger, corpus, and output payload hashes were checked directly. No files, models, datasets, or automation settings were changed.

## B. What the two generations definitively established

**MEASURED RESULT — neither generation produced an eligible scratch restorer.** Generation 1 completed its six prescribed recipes. Generation 2 completed six new scratch treatments and the pretrained comparator. These are completed negative adequacy results, not incomplete execution.

The expanded natural panel contains 2,696 cases, 50,926 reference words, and 1,413 RAW errors: **2.774614% WER**.

| Prescribed G2 candidate | Natural WER | Completed repairs | Introduced errors | Scientific adequacy |
|---|---:|---:|---:|---|
| B100-D1-U8 | 33.375879% | 44–45 | 15,628–15,629 | Failed |
| C101-D1-U8 | 8.041079% | 18 | 2,702 | Failed |
| ByT5, exact ten-pass endpoint | 3.239995% | 120 | 357 | Failed |

Evidence: [G2 campaign](https://github.com/scalinity/repair-without-rewrite/blob/609f97f31979d469ad8551d06b2c07c3513181ec/docs/reports/G2_BC_SCIENTIFIC_CAMPAIGN.md), [ByT5 adaptation](https://github.com/scalinity/repair-without-rewrite/blob/609f97f31979d469ad8551d06b2c07c3513181ec/docs/reports/G2_BYT5_SCIENTIFIC_ADAPTATION.md), and [G1 campaign](https://github.com/scalinity/repair-without-rewrite/blob/609f97f31979d469ad8551d06b2c07c3513181ec/docs/reports/SIX_10M_PROBE_CAMPAIGN.md).

Further established findings:

- B100 can fit a narrow, repeatedly presented TRAIN sample. Its D0-U8 failure is therefore not universal inability to express the required mapping.
- D1 and U8 interact strongly for B100. The WER interaction is **−87.236382 percentage points**, but the improvement primarily reduces destructive output; it does not establish useful repair.
- C101 can produce genuine generated repairs and some natural repairs. Deterministic copying does not guarantee safe edit decisions.
- ByT5’s failure persists after complete, independently verified adaptation.
- More completed repairs can coexist with worse WER.
- The observed outcomes do not establish architectural impossibility, natural-task impossibility, final-population superiority, or H1.
- Engineering verification supports interpreting the experiments. It does not establish scientific adequacy.

The new arithmetic below is labelled **CALCULATION** and tied to retained inputs. It is not a newly published independent-review receipt.

## C. B100 root-cause ranking

Confidence concerns the explanation, not the existence of the reported observations.

| Rank | Mechanism and supporting evidence | Contrary evidence / unresolved issue | Confidence | Cheapest discriminating diagnostic and implication |
|---|---|---|---|---|
| 1 | **Failure to generalize source-faithful transduction.** D0-U8 fits all 64 selected TRAIN error cases lexically, yet reaches 124.38% heldout WER. D1-U8 still damages 1,600 originally lexical-zero cases. | Selected TRAIN fit does not identify whether the model memorizes outputs, learns narrow conditional mappings, or fails under unfamiliar contexts. | High for the generalization gap; medium for its internal mechanism. | Join cached errors to TRAIN support, repetition, length, and source overlap. Concentration in unfamiliar material supports a support/generalization account; uniformly poor behavior also implicates basic transduction learning. |
| 2 | **Insufficient natural learning exposure and training horizon under D1.** One or two repair presentations per case; no lexical-exact corrections in the selected D1 TRAIN error sample. | D0’s much greater repetition still fails transfer. Longer training is not sufficient evidence of eventual usefulness. | High for limited exposure; medium-high as a contributor. | Reconstruct exact record/group/phase exposure and diagnostic-case repetition. This determines whether a future intervention should increase natural learning opportunity before acquiring more data. |
| 3 | **Full-target objective and weak copying bias.** Every output token must be regenerated; D1-U8 preserves only 288/2,696 sources lexically. | D0 TRAIN copying succeeds, and full-text correction works in other settings. Absence of a copy mechanism is not proof of architectural incapacity. | Medium-high. | Decompose cached errors into omissions, substitutions, insertions, and changes in originally correct regions. A causal copy-mechanism test would require a later new treatment. |
| 4 | **Curriculum and synthetic-to-natural mismatch.** Generated channels receive 75% of canonical exposure; real pairs receive 10%. | B also fails generated heldout required repair, so natural-domain mismatch alone cannot explain the failure. | Medium. | Compare TRAIN/generated versus heldout/generated fit and natural transfer by error pattern. Broad heldout failure argues against merely adding more natural vocabulary. |
| 5 | **Optimizer geometry interacts with learning.** D1-U8 greatly improves on D1-U1; D0-U8 worsens on D0-U1. | U8 changes normalization granularity, clipping, moment evolution, weight decay applications, and LR sampling together. It does not isolate step count. | High for interaction; low for a unique optimizer cause. | Retained update logs can describe phase-local behavior. Choosing a new optimizer or LR still requires a prospective causal design. |
| 6 | **Scale and encoder/decoder allocation poorly matched to resources.** Approximately 100M random parameters receive little independent natural supervision. | No smaller-model or depth-allocation comparison exists. Narrow TRAIN fit argues against a simple capacity shortage. | Low-medium. | Cost and supervision accounting can justify a smaller pilot economically, but cannot establish that a smaller architecture will generalize better. |

Reference ambiguity cannot plausibly explain B’s catastrophic damage to originally correct material. It may limit achievable repair, but it is not the leading explanation for this failure.

## D. C101 root-cause ranking

| Rank | Mechanism and supporting evidence | Contrary evidence / unresolved issue | Confidence | Cheapest discriminating diagnostic and implication |
|---|---|---|---|---|
| 1 | **Poor discrimination between useful and harmful action.** D1-U8 introduces 2,702 errors while completing 18 repairs. Its learning curve moves from identity to harmful editing. | Confidence calibration itself is unmeasured; activity and confidence are different quantities. Whole-output gating has almost no scratch headroom. | High for harmful decisions; unestablished for probabilistic miscalibration. | Separate missed opportunities, damaging edits, and mixed beneficial/harmful outputs using cached programs. This identifies whether acceptance or proposal quality dominates. |
| 2 | **Insufficiently learned natural repair under D1.** Immediate END occurs on 52/64 selected TRAIN error cases; none is target-lexically exact. | D1 contains many more error-bearing examples; some generated learning succeeds. | High on the diagnostic sample; medium-high as a training explanation. | Join these cases to their actual presentation histories and gold-program complexity. Do not infer a global END-class imbalance from this sample. |
| 3 | **Replacement generation is a distinct bottleneck.** D0-U8 matches every gold span on 63/64 TRAIN error cases, but 39 of these use wrong replacement text. | This is TRAIN behavior under one condition; alternate valid programs need not match the canonical program. | High for this specific failure mode. | Tabulate exact-span/wrong-replacement programs separately from localization failures. A generic END penalty cannot fix this category. |
| 4 | **Surface supervision and generated-task transfer compete with lexical preservation.** Many lexical-zero natural examples still require surface edits; generated repairs do not transfer reliably. | No objective or curriculum ablation isolates the effect. Surface restoration remains part of the declared task. | Medium-high. | Measure gold surface-edit burden, replacement-token supervision, and lexical damage without changing targets or excluding cases. |
| 5 | **Localization and autoregressive error propagation.** D1-U8 matches all gold spans on only 1/64 selected TRAIN error cases. | Fifty-two cases produce no edit, so most span mismatches do not independently establish a pointer failure. | Medium. | Condition localization diagnostics on actual activation; retain the unconditional denominator. Distinguish missing edits from incorrectly localized edits. |
| 6 | **Optimizer regime, scale, and horizon.** U8 helps D1 relative to U1 but worsens D0; the expanded corpus remains poorly fitted. | No evidence uniquely supports changing model size, loss coefficients, or optimizer. | Medium for interaction; low for a specific remedy. | Complete exposure and component-loss analysis before choosing one later intervention. |

The strongest diagnosis is **multiple bottlenecks**, not “C needs encouragement to edit.”

## E. ByT5 root-cause ranking

| Rank | Mechanism and supporting evidence | Contrary evidence / unresolved issue | Confidence | Cheapest discriminating diagnostic and implication |
|---|---|---|---|---|
| 1 | **Overcorrection overwhelms useful proposals.** Repairs rise 84→105→120; introductions rise 205→257→357. At the endpoint, all natural outputs complete. | Whether retained source/output features can distinguish beneficial proposals is unknown. | High behaviorally. | Whole-output benefit/harm accounting and fixed-feature diagnostics on cached proposals. A separable subset would motivate a later acceptance-policy experiment. |
| 2 | **Likelihood-trained rewriting does not optimize improvement over RAW.** Full-target decoding exposes correct material to change; 183 lexical-zero cases are damaged. | There is no objective or decoding ablation, and ByT5 preserves most sources lexically. | Medium-high. | Separate surface-only changes, lexical changes, and mixed repair/damage within utterances. |
| 3 | **Ambiguous or distribution-specific supervision.** Short read-speech excerpts can contain names, omissions, and reference-specific distinctions not determined by text alone. | The model does complete 120 repairs across 37 groups; universal unlearnability is contradicted. | Medium as a limitation; unknown prevalence. | Source-collision and TRAIN-supported local-mapping analysis, with ambiguous cases explicitly unresolved. |
| 4 | **Adaptation recipe or horizon is suboptimal.** Net error worsens over the retained trajectory. | Ten passes and 35,283 updates were completed. This is not the scratch models’ one-to-two-presentation regime. No alternative LR or duration was tested. | Medium for recipe limitation; low for any proposed replacement. | Analyse where additional repairs and damage occur between fixed observations. Do not select the two-pass checkpoint. |
| 5 | **Evaluation/domain effects.** The panel covers one recognizer and short literary speech. | Failure occurs in both CAL and HPO, and in clean and other subsets; it is not explained by a single displayed subset. | High limitation; low as an explanation that invalidates the result. | Preserve subgroup reporting and group-aware uncertainty. Broader generalization requires separate prospective evidence. |

ByT5 establishes that **this adaptation failed**, despite having some useful repair proposals. It does not establish that pretrained correction, full-text generation, or the natural task cannot work.

## F. B100 TRAIN-versus-DEV generalization interpretation

**MEASURED RESULT.** B100-D0-U8 obtains 64/64 target-lexical exactness on the frozen TRAIN error stratum, completes 113 repairs, and introduces zero errors. Its reference-as-source identity diagnostics are also lexically preserved.

**INFERENCE.** Eighteen or nineteen repeated real-pair presentations, together with repeated identity views and shared training context, allowed this narrow sample to be fitted. The evidence supports sample memorization or narrow transduction learning. It does not distinguish them causally.

The heldout result—124.384401% WER—shows that this success did not transfer.

For D1-U8:

- Each natural repair pair appears only once or twice.
- The first complete real-pair pass finishes at canonical exposure **7,218,011**, already in P1.
- The selected TRAIN error cases have target loss approximately **3.529**, versus **0.000216** for the D0-U8 error sample.
- The equivalent D1 diagnostic has zero target-lexically exact error cases.

These are separately hash-selected D0 and D1 samples, not identical examples exposed under two treatments. Therefore their difference is not a clean within-example estimate of corpus expansion.

D1-U8 can improve heldout WER while failing to fit its TRAIN corrections because it learns broader copying/transduction behavior without learning reliable corrections. Its heldout repair count remains small while introduced damage falls substantially.

**Verdict:** D0 demonstrates narrow fitting without generalization; D1 demonstrates partial broader learning without useful repair. Neither justifies extrapolating the existing learning curve to success at 150M.

## G. Actual natural-corpus exposure / repetition interpretation

**CALCULATION — directly reconstructed from the hash-verified frozen natural files and presentation ledgers.** These counts are shared across arms and U regimes within each D condition.

| Quantity | D0 | D1 |
|---|---:|---:|
| Distinct natural repair pairs seen | 1,024 | 14,113 |
| Real-pair presentations | 18,693 | 19,538 |
| Real-pair canonical exposure | 1,000,665 | 1,000,628 |
| Repetition distribution | 763 cases ×18; 261 ×19 | 8,688 cases ×1; 5,425 ×2 |
| Mean presentations per pair | 18.254883 | 1.384397 |
| Distinct lexical-error pairs | 334 | 5,373 |
| Lexical-error presentations | 6,102 | 7,390 |
| Canonical exposure on lexical-error pairs | 366,186 | 421,428 |
| Natural source groups seen | 48 | 314 |
| Error-bearing source groups seen | 47 | 309 |
| Real-pair exposure per group, minimum–maximum | 5,253–59,609 | 184–16,212 |
| Error presentations per supported group, minimum–maximum | 18–401 | 1–277 |
| Separate natural-identity presentations | 28,040 | 29,365 |
| Identity canonical exposure | 1,501,032 | 1,501,003 |
| Identity repetition distribution | 632 cases ×27; 392 ×28 | 12,974 cases ×2; 1,139 ×3 |

The charge-based pass equivalents are **18.256312 for D0** and **1.386247 for D1**. These differ slightly from presentation-based averages because example charges differ.

Actual phase allocation:

| Condition / phase | Real presentations | Error-bearing presentations | Real canonical exposure | Identity presentations | Identity canonical exposure |
|---|---:|---:|---:|---:|---:|
| D0 P0 | 12,456 | 4,070 | 666,666 | 18,681 | 1,000,061 |
| D0 P1 | 4,979 | 1,614 | 266,669 | 7,481 | 399,991 |
| D0 P2 | 1,258 | 418 | 67,330 | 1,878 | 100,980 |
| D1 P0 | 13,026 | 4,968 | 666,666 | 19,526 | 1,000,060 |
| D1 P1 | 5,221 | 1,937 | 266,651 | 7,853 | 400,043 |
| D1 P2 | 1,291 | 485 | 67,311 | 1,986 | 100,900 |

Evidence bindings: [corpus freeze](https://github.com/scalinity/repair-without-rewrite/blob/609f97f31979d469ad8551d06b2c07c3513181ec/experiments/manifests/generation_2/corpus-freeze.attempt01.json) and [execution freeze](https://github.com/scalinity/repair-without-rewrite/blob/609f97f31979d469ad8551d06b2c07c3513181ec/experiments/manifests/generation_2/execution-campaign-freeze.attempt01.json). The next study must retain the complete per-group table, not only these ranges.

**Verdict:** D1 meaningfully increased independent support but barely increased total real-pair presentations. It tested diversity under fixed exposure, not adequate learning from a larger corpus.

The 10% allocation is therefore a major interpretive constraint. It does not make the experiment invalid; it limits the conclusion. “Larger natural corpora do not help” is unsupported.

## H. C101 overcorrection and edit-decision analysis

**CALCULATION — cached native programs provide a more precise diagnosis than aggregate WER.**

| Frozen TRAIN error stratum, 64 cases | D0-U8 | D1-U8 |
|---|---:|---:|
| Immediate END with no edits | 0 | 52 |
| Nonempty predicted programs | 64 | 12 |
| Exact complete gold-span sequence | 63 | 1 |
| Exact gold edits including replacement text | 24 | 0 |
| Exact spans but wrong replacement text | 39 | 1 |

Exact-program matching is diagnostic only: a different program can render the same valid target. It is not a replacement for the output scorer.

The retained teacher-forced losses reinforce the separation:

- D0-U8: action ≈0.000309; start pointer ≈0.0134; end pointer ≈0.000362; replacement vocabulary ≈0.815.
- D1-U8: action ≈0.484; start ≈2.086; end ≈0.872; replacement vocabulary ≈4.623.

These losses have different denominators and prediction spaces. They must not be ranked as directly comparable error rates. Nevertheless, D0’s exact-span failures with wrong replacement text are concrete evidence of a generation bottleneck.

Heldout D1-U8 also combines misses and damage:

- 661/878 lexical-error cases return immediate no-edit.
- 207 produce nonempty valid programs; 10 have no complete program.
- Among 1,818 lexical-zero cases, 284 produce nonempty valid programs and 16 have no complete program.
- 288 lexical-zero cases acquire word errors.

Furthermore, D1-U8 has **fewer** valid nonempty natural programs than D0-U8—491 versus 659—while producing worse WER. Edit severity and replacement quality matter alongside activation frequency.

**Accounting qualification:** C101-D1-U8 has 20 raw repairs but only 18 completed repairs. The error conservation identity is:

`1,413 − 20 + 2,702 = 4,095`

Using completion-gated repair in that identity would be incorrect.

**Verdict:** no generic END penalty, focal loss, or editing bonus is justified. A stronger END preference can suppress remaining repairs; a weaker one can amplify damage. The next analysis must separate activation, localization, replacement, completion, and acceptance.

## I. ByT5 adaptation trajectory interpretation

The completed trajectory is:

| State | Repairs | Introductions | Net additional errors versus RAW |
|---|---:|---:|---:|
| Two-pass nominal observation | 84 | 205 | 121 |
| Five-pass nominal observation | 105 | 257 | 152 |
| Exact ten-pass endpoint | 120 | 357 | 237 |

The model learns additional corrections, but damage rises faster. This supports a preservation problem under the frozen adaptation. It does not prove that confidence increases, because the retained outputs do not contain the probability traces needed to measure confidence calibration.

**CALCULATION.** At the endpoint, 183/1,818 lexical-zero utterances are damaged, contributing **239 errors**. That is a substantial component of the 357 introduced errors.

For a fixed endpoint proposal \(O_i\), define the reference-aware whole-output headroom:

\[
G_{\mathrm{whole}}
=\sum_i \mathbf{1}[\text{complete}_i]\max(0,e_{S,i}-e_{O,i}).
\]

This selector may choose only the complete cached proposal or RAW. It cannot repair a proposal or use a different checkpoint.

| Fixed endpoint | Beneficial complete utterances | Maximum removable errors | Supporting groups | Oracle WER |
|---|---:|---:|---:|---:|
| B100-D1-U8 | 2 | 2 | 2 | 2.770687% |
| C101-D1-U8 | 3 | 3 | 3 | 2.768723% |
| ByT5 exact ten-pass | 67 | 109 | 36 | 2.560578% |

These calculations were checked both by summing positive gains and by summing per-case minimum errors. Their inputs are the immutable endpoint payloads bound by the observation receipts.

The ByT5 headroom is **0.214036 WER percentage points**, or **7.714% relative to RAW**. It is an unattainable reference-aware ceiling for this particular whole-output choice, not demonstrated system performance or a general recoverability bound.

**Verdict:** analyse the exact ten-pass ByT5 proposals first. Do not retrospectively substitute its two-pass checkpoint.

## J. Source-only recoverability verdict

**Some reference distinctions cannot be determined uniquely from a short ASR 1-best string. The prevalence of those distinctions here is unmeasured.**

The analysis must distinguish:

| Category | What can be established without new human annotation |
|---|---|
| Normalization under an explicit deterministic rule | Rule applicability and lexical/surface effect; not universal semantic correctness. |
| Locally supported textual correction | Repeated TRAIN evidence across independent groups; support does not prove correctness on every occurrence. |
| Context-dependent uncertain correction | Statistical support or conflict, labelled as such. |
| Reference-specific ambiguity | Exact identical-input/different-target collisions provide direct empirical witnesses. |
| Errors requiring acoustic evidence | Generally cannot be certified from these retained text triples alone. Mark unresolved rather than assigning an acoustic-necessity label by intuition. |

An exact source collision with different targets establishes that a deterministic source-only model cannot satisfy both references simultaneously. Absence of collisions does not establish recoverability: most full sentences are unique.

A language model’s preference or a fluent replacement is not a recoverability certificate. No model judge should supply primary labels.

The existing task is already explicitly **reference-conditional**, not recovery of acoustic truth. That contract remains coherent. The scientific problem is whether a useful subset can be repaired with sufficiently little damage—not whether every reference error is inferable.

## K. Current 100M model-size verdict

**Another investment in the existing 100M scratch pair has not earned default status. No replacement size is scientifically selected.**

- **20M–40M:** plausible for a cheaper transduction pilot, but weaker capacity may also hurt rare corrections.
- **40M–70M:** plausible compromise, but no project evidence establishes its advantage.
- **Approximately 100M:** demonstrated capacity to fit a small D0 sample; no demonstrated useful heldout restoration.

Parameter count alone does not resolve the dominant uncertainty. Reducing size while changing curriculum and objectives would create another bundled intervention.

Because no resizing treatment is authorized here, layer counts, widths, heads, FFN dimensions, and parameter arithmetic remain deliberately unbound. A later decision recommending resizing must supply them exactly.

## L. Representation versus preservation-decision verdict

The current comparison concerns **representation, supervision, decoding, and constitutive rendering together**. It does not isolate a purely symbolic output-format effect.

| Matching concept | What it controls—and what it does not |
|---|---|
| Parameter matching | Approximate model capacity; not equal optimization difficulty. |
| Canonical exposure matching | Declared source/target accounting; not equal native supervised positions. |
| Presentation matching | Identical examples and order within D; not identical loss weighting. |
| Optimizer-step matching | Update count; not equivalent gradients or moment dynamics. |
| Initialization lineage | Scratch versus pretrained information; not equivalent task knowledge. |
| Deterministic copying | Preserves untouched bytes; does not establish that touched spans should change. |
| Inference cost | Requires complete request accounting; output length alone is insufficient. |

**Verdict:** preservation-aware selective correction should become the next primary development hypothesis. It is not yet an established explanation of all three systems or a proven novel contribution.

A whole-transcript acceptance gate cannot meaningfully rescue the scratch endpoints. A local edit policy might recover useful pieces from otherwise harmful outputs, but that requires separate analysis of interactions and localization. It must not be credited retrospectively to the bare model.

## M. Curriculum and data-supply verdict

**Do not retain 15/15/20/10/40 as an unquestioned default for another natural-restoration campaign. Do not replace it with invented percentages in this review.**

The current allocation was useful for identifying D/U interactions. It has not demonstrated that it serves natural restoration well.

A further complication is that **natural identity examples use reference text as source**. They are not equivalent to preserving a lexical-zero ASR hypothesis with different casing, punctuation, or surface form.

**CALCULATION:**

- D0: 508/690 lexical-zero natural pairs still contain gold surface edits.
- D1: 6,470/8,740 lexical-zero natural pairs still contain gold surface edits.

Thus a large part of “correct lexical input” training still asks the model to act. That is a legitimate surface-restoration objective, but it can conflict with conservative lexical behavior.

Priority order for a later curriculum decision:

1. Measure effective natural correction and preservation supervision already available.
2. Separate copying competence from repair competence.
3. Determine whether surface restoration and lexical repair need separate controls or stages.
4. Set training extent in complete natural passes as well as canonical exposure.
5. Add technical generated specialization only if it serves the revised scientific question.

No channel share, oversampling ratio, phase schedule, or loss coefficient is authorized here. Those are consequential scientific choices, not implementation details.

## N. Luna/teacher augmentation verdict

**Do not introduce teacher data next.**

| Option | Scientific value | Decision |
|---|---|---|
| Existing qualified LS-PC/Parakeet pairs | Strongest available source/target lineage; existing error distribution. | First analyse and use more effectively before expanding supply. |
| More exposure to the existing 14,113 pairs | Directly addresses the measured repetition deficit. | Plausible later intervention; not automatically sufficient or authorized. |
| Teacher clean seeds + deterministic corruption | Cheap linguistic diversity; target precedes corruption. | Deferred: current corruption realism and natural invertibility are inadequate assumptions. |
| Teacher clean seeds + TTS + Parakeet | Recognizer generates errors; stronger lineage than invented correction pairs. | Deferred: adds teacher, synthesis, acoustic realization, and domain factors. |
| Direct teacher noisy/clean pairs | Easy to generate. | Weakest primary supervision: teacher defines both the error and its answer. |

The current bottleneck is not proven to be lack of clean text. New synthetic data would add another domain before resolving natural exposure and proposal quality.

If teacher augmentation is reconsidered, it needs a separate generation definition, immutable teacher identity and prompts, target-before-corruption lineage, source-family grouping, deduplication, protected-data exclusion, and a prospective real-data comparison. A randomly initialized student would still receive pretrained-model information through its data.

No teacher/API call or price-dependent spending recommendation is part of this decision.

## O. Best future architecture or task framing

The strongest next question is:

> **For low-error ASR 1-best transcripts, how much useful correction is present in fixed proposals, and how much of that benefit can be retained using only source-available acceptance signals?**

Assessment of the requested alternatives:

| Alternative | Judgment |
|---|---|
| A. Retain B100/C101 with a new curriculum | Possible later, but two-arm retraining is premature. |
| B. Resize the scratch pair | Economically plausible; causally unresolved. |
| C. Add source copying to B | Strong mechanistic candidate if copying failure remains central; changes the comparison. |
| D. Redesign C around detection and acceptance | Relevant, but must also address missed edits and replacement generation. |
| E. Shared scratch denoising/transduction foundation | Could reduce basic transduction failure; expensive and changes the training intervention. |
| F. Pretrained/shared-initialization comparison | Most direct later route to capability, with explicit lineage and head-initialization accounting. |
| G. Preservation-aware correction framing | Best hypothesis to investigate now; existing work prevents claiming invention. |
| H. Stop the current scratch representation experiment | Suspend further execution now; preserve its controlled negative evidence. |

If feasibility supports another model experiment, begin with **one narrowly defined proposer or acceptance mechanism**, not another six-cell matrix. A full representation comparison becomes worthwhile only after useful restoration is established.

## P. Nearest-work and novelty verdict

| Work | Consequence for this project |
|---|---|
| [Zhang, Stahlberg and Kumar](https://arxiv.org/html/2501.13831v1) | Already compares full transcripts and compact ASR rewrite representations with deterministic expansion. No first-comparison claim. |
| [FastCorrect](https://proceedings.neurips.cc/paper/2021/hash/b597460c506e8e35fb0cc1c1905dd3bc-Abstract.html) | Establishes edit-aligned nonautoregressive correction and accuracy/latency tradeoffs. Efficient structured correction is established territory. |
| [PATCorrect](https://arxiv.org/html/2302.05040v2) | Includes scratch training, source-derived phonemes, and detection/correction measurements. Scratch initialization is not itself novel. |
| [SoftCorrect](https://arxiv.org/abs/2212.01039) | Explicitly addresses detection and selective correction. Its information and training setup cannot be silently imported into a 1-best-only comparison. |
| [ConstDecoder](https://www.isca-archive.org/interspeech_2022/yang22g_interspeech.pdf) | Uses operation prediction and constrained selective decoding. Keep/change mechanisms are not new here. |
| [ECLM](https://arxiv.org/html/2405.15216v2) | Directly challenges novelty based on compact specialists, realistic synthetic errors, or low-error correction. Its correction-first results use acoustic rescoring and cannot be treated as source-only drop-in results. |
| [DARAG](https://aclanthology.org/2025.findings-acl.125/) | Already combines generated data and retrieval augmentation. Teacher/TTS augmentation alone is not a contribution. |
| [Conservative Data Filtering](https://aclanthology.org/2024.emnlp-industry.20/) | Explicitly addresses overcorrection and whether corrections are inferable from available context. The preservation hypothesis must offer a distinct experiment. |
| [RED-ACE](https://aclanthology.org/2022.emnlp-main.180/) | Demonstrates the value of ASR confidence information for detection; that information is absent from this project’s inference contract. |

Potential contributions, with present status:

- **Capability:** not demonstrated.
- **Representation comparison:** controlled development evidence exists; useful matched systems do not.
- **Measurement:** explicit repair/damage, ambiguity, completion, and accounting are valuable, but implementation alone is not novelty.
- **Efficiency/precision tradeoff:** promising only after a useful system and complete cost comparison exist.
- **Controlled negative finding:** supportable narrowly for these recipes and budgets.
- **Curriculum insight:** substantial repetition dilution is established; a causal remedy remains untested.

The manuscript must explain something beyond “small scratch models failed” or “gating reduces editing.”

## Q. Paper viability verdict

**A compelling manuscript remains possible within roughly a month, but the original confirmatory H1 paper is not currently on an evidence-backed schedule.**

The project has strong reproducibility and interpretable negative development evidence. It lacks useful paired scratch systems, a successful comparator under the frozen gate, final-population results, and completed publication prerequisites.

The retained source-qualification record also leaves SLUE access/qualification unresolved. Nothing in the completed G2 record establishes that the original equal-domain endpoint is ready. Dropping that domain would require an explicit prospective scope change.

A reasonable calendar allocation is:

- Up to two working days for the bounded feasibility study.
- A new frontier decision immediately afterward.
- At most one focused capability intervention before considering a paired comparison.
- Reserve substantial time for independent validation, remaining data access, final design, and writing.

This is a planning allocation, not a completion forecast. A narrow negative-results or diagnostic manuscript may be more realistic than the original H1 claim, but its publication value depends on the resulting insight and comparison quality.

## R. Exact next research stage

**Stage identifier:** `POST_G2_READ_ONLY_FEASIBILITY_V1`

**Primary question:** Does retained evidence support a useful source-only selective-correction treatment, or does proposal quality/information support require a more fundamental change?

### Frozen inputs

Use checkpoint `609f97f31979d469ad8551d06b2c07c3513181ec` and these repository-relative bindings:

| Input | SHA-256 |
|---|---|
| `execution-campaign-freeze.attempt01.json` | `084be260a7f6797d9e138839fe56660c3ce47cb6d92d813c4c3a518b3344cb14` |
| `scientific-results.attempt01.json` | `510e0efceec1127f38d524f8ca71a224cbaea59cd8206f5dc138889d9be74edd` |
| `scientific-results-independent.attempt01.json` | `8f952fc01a96e2e8468c4ac65234de5922bc3aad1984155f1803aecc8d8b5cf7` |
| `scientific-accounting-independent.attempt01.json` | `3dfdad614f2b16bda60e97a454f9dc08b6eb8a132e710ebaf18dc0d271bb8334` |

All four are under `experiments/manifests/generation_2/`.

Resolve private payloads only through these frozen identities and their observation receipts:

- D0/D1 natural records, presentation ledgers, masters, actual updates, and diagnostic selections.
- The frozen 2,984-case DEVELOPMENT panel.
- All 42 retained heldout panels and 12 TRAIN diagnostic states.
- Exact endpoint C programs and ByT5 generated IDs/text.
- Existing corruption-profile and source-group records.

Verify the declared file hashes before use. No checkpoint-array loading is needed.

### Analysis 1: Exposure and supervision

Reproduce Section G independently. Produce record-, group-, channel-, and phase-level counts, including:

- Zero-, one-, and repeated-presentation support.
- Lexical-error and surface-only supervision.
- Gold action/pointer/replacement denominators.
- First-presentation and first-complete-pass exposure.
- Exact repetition of each frozen TRAIN diagnostic case.

Do not treat canonical charge, native target tokens, event labels, and optimizer steps as interchangeable.

### Analysis 2: Proposal benefit and damage

For each prescribed endpoint, report:

- Better/equal/worse output error counts per utterance.
- Completed repair, raw repair, introduction, and failure counts.
- Originally lexical-zero damage.
- Whole-output oracle headroom using the fixed equation in Section I.
- Group support and concentration of gains and damage.

The three predeclared candidates remain the primary endpoints. Other cells and intermediate states remain descriptive. Do not select a checkpoint, arm, or cell.

### Analysis 3: C program failure decomposition

Use cached programs and frozen gold programs:

- Immediate no-edit, nonempty valid, invalid/capped, and abstained states.
- Missing edits versus wrong spans versus wrong replacement text.
- Canonical-program exactness separately from rendered-output exactness.
- Surface-only gold edits that cause lexical damage.
- Per-event omission diagnostics on the fixed D1-U8 endpoint, if needed.

Any event omission is an **analytical counterfactual constructed from a cached program**, not new model inference or an evaluated deployable system. Do not sum isolated event gains as an achievable total: edits can interact. Do not search arbitrary subsets of edits.

### Analysis 4: Acceptance-signal feasibility

Use only existing, inference-available source/output quantities:

- Source and output lengths.
- Lexical source-output edit distance.
- Relative edit burden.
- Insertion/deletion/substitution composition.
- Validity/completion.
- Native event count for within-C analysis.
- TRAIN-only support for local source-to-replacement patterns.

Use fixed descriptive edit-count bins: `0`, `1`, `2`, `3–4`, `≥5`. Report continuous burden plots or complete descriptive curves without selecting a threshold.

**Do not fit a calibrator, optimize a guard, tune thresholds, or train a detector in this stage.**

The retained decoder records do not expose the token/action probability traces required for probabilistic calibration. Gold teacher-forced TRAIN losses are not deployment confidence. Missing confidence remains unavailable; do not obtain it through new forward passes.

### Analysis 5: Recoverability and information support

On existing TRAIN and DEVELOPMENT data only:

- Identify exact raw-source/different-target collisions.
- Separate byte-target conflicts from lexical-target conflicts.
- Count repeated local correction mappings with one-word and three-word source contexts, using TRAIN support only.
- Report support by distinct records and groups; a supported mapping requires at least five TRAIN records and three groups for this diagnostic.
- Retain unsupported and conflicting patterns as unresolved.
- Separate deterministic normalization from lexical substitution, insertion, deletion, and surface-only restoration.

These are operational support measures. They do not certify semantic inferability or acoustic necessity.

### Aggregation and uncertainty

Use all cases. Preserve existing roles, source groups, failures, and caps.

Report corpus ratios with fixed denominators. For descriptive intervals, reuse the registered **10,000 paired source-group bootstrap draws, PCG64 seed 42, over 52 groups**. Keep alignment bounds separate from sampling intervals.

Do not bootstrap utterances as independent observations. Do not interpret these intervals as training-seed uncertainty or confirmatory inference.

All 2,696 natural DEVELOPMENT cases have already informed research decisions. Neither CAL nor HPO may be relabelled as untouched validation. A later fitted acceptance policy needs a separately authorized fitting/evaluation design.

### Deliverables

Return:

1. Input-identity and coverage table.
2. Complete exposure/repetition summary, including per-group support.
3. Endpoint proposal-benefit and damage tables.
4. C failure decomposition.
5. Source-only support/ambiguity assessment.
6. Acceptance-feature analysis with unavailable confidence explicitly identified.
7. Independent arithmetic reconciliation.
8. One recommendation for the next scientific decision.

Provide the report in chat under read-only authority. Any later archival files, amendment recording, commits, or publication require separately authorized evidence-writing scope.

## S. Bounded compute and storage budget

| Item | Bound |
|---|---|
| New neural training recipes | **0** |
| New neural inference / teacher-forced forward passes | **0** |
| Teacher, TTS, ASR, paid API requests | **0** |
| Dataset or model downloads | **0** |
| CPU analysis | **At most four elapsed compute hours**, including independent reconciliation |
| Working memory target | **At most 8 GiB**, using streamed records and compact aggregates |
| Analyst horizon | **At most two working days** |
| New persistent storage under read-only authority | **0 bytes** |
| Evidence deletion, pruning, relocation | **None** |

These are prospective operational caps, not measured runtime forecasts.

**FACT:** current literal free space was read as approximately **321.294 GiB**. The full post-disconnect 539-file integrity result remains supplied prior evidence; it was not repeated across all 143.35 GB in this review.

Generation 2’s measured scientific recipe wall time remains **36.700589 hours**. Training, saving, decoding, and scoring are already included. Reusing cached outputs avoids another neural evaluation campaign.

Any later neural proposal must separately budget retained failed attempts, checkpoints, qualification, evaluation, and archive growth. Available free space is not authorization to consume it.

## T. Acceptance and stop criteria

The feasibility study is complete only when:

- Frozen identities and membership reconcile.
- All required populations and failures remain present.
- Exposure accounting reproduces independently.
- Whole-output headroom reproduces by two arithmetic formulations.
- C program diagnostics distinguish canonical-program equality from output correctness.
- Support and uncertainty denominators are explicit.
- Missing confidence and unresolved semantic recoverability remain labelled unavailable.
- No parameter, threshold, checkpoint, or subgroup has been selected for a success claim.

Scientific branching rules:

- **Negligible whole-output headroom:** reject acceptance-only rescue of that fixed proposer. The present scratch endpoints already meet this concern.
- **Headroom but no demonstrated usable signal:** retain uncertainty; request a separate, narrowly scoped scoring/calibration design if justified.
- **Useful local edits embedded in harmful outputs:** consider an edit-level policy or proposal redesign, not a whole-output gate.
- **Sparse natural learning support plus learnable repeated patterns:** consider one natural-focused learning treatment.
- **Predominantly unresolved target ambiguity:** narrow claims or explicitly reconsider the information boundary; do not remove difficult evaluation cases.

Stop immediately for identity contradictions, protected-data access, required new inference, required human annotation, or budget exhaustion. Return partial coverage honestly. A stopped analysis is not a passed study.

No outcome automatically releases Generation 3.

## U. Prospective scientific amendment

```text
Post-G2 Frontier Scientific Decision v2 — 2026-10-09

Reviewed branch: codex/g2-execution
Reviewed checkpoint: 609f97f31979d469ad8551d06b2c07c3513181ec
Qualified Generation-2 source:
2c27cff28a31ae64220df9b06094a914e94dd0f3

Disposition: AUTHORIZE_READ_ONLY_TASK_FEASIBILITY_STUDY

Preserve all completed Generation-1 and Generation-2 treatments, outputs,
failures, accounting, adequacy gates, and dispositions unchanged. All seven
Generation-2 scientific slots remain consumed. No historical checkpoint,
learning rate, cell, or subgroup becomes a selected successful model.

Adopt POST_G2_READ_ONLY_FEASIBILITY_V1, Sections R–T of this decision, as the
next bounded analytical design. Its purpose is to distinguish inadequate
proposal quality, harmful edit acceptance, limited natural supervision, and
unresolved source-only information support using retained evidence.

The study permits no new neural training, inference, teacher-forced model
scoring, detector fitting, calibration fitting, threshold optimization,
teacher generation, TTS, ASR calls, data acquisition, or paid API use.

Use the exact frozen Generation-2 corpus, ledgers, DEVELOPMENT panel,
prescribed outputs, TRAIN diagnostics, and source-group identities. Preserve
all cases and failure treatments. Existing DEVELOPMENT observations remain
development-consumed; no partition is relabelled untouched validation.

Reference-aware whole-output selection is an oracle diagnostic restricted
to RAW versus the fixed complete cached output. It is not a deployable
source-only policy or a general task-recoverability bound. Local edit
counterfactuals are analytical diagnostics and cannot be credited to the
bare model or combined without accounting for edit interactions.

Keep scorer alignment bounds, group-bootstrap uncertainty, and training-seed
uncertainty distinct. Missing probability traces remain unavailable.
Automatic support and collision analyses do not establish semantic truth,
acoustic truth, or universal text recoverability.

No model size, architecture, copying mechanism, event representation,
curriculum share, loss coefficient, optimizer, learning rate, training
horizon, teacher corpus, final population, or paper claim is changed here.

Execution and any persistent evidence-writing scope require separate owner
authorization. Record this decision and amendment before the subsequent
analytical stage in an authorized documentation session. Do not modify
immutable design inputs or historical reports.

After the bounded study, return for a new frontier scientific decision.
No result automatically authorizes implementation, Generation 3, final
seeds 1729/2718/31415, final 150M training, sealed inference,
paper_protocol_v2 freeze, publication, cloud spending, or production changes.
```

## V. Sol read-only analysis handoff

```text
Perform POST_G2_READ_ONLY_FEASIBILITY_V1 in
/Users/danny/Documents/Tools/LocalFlowResearch.

Project: Repair Without Rewrite: A Controlled Comparison of Full-Transcript
Generation and Compact Editing Under Matched Source Exposure.

Review codex/g2-execution at exactly
609f97f31979d469ad8551d06b2c07c3513181ec.
Remote: https://github.com/scalinity/repair-without-rewrite
Qualified source: 2c27cff28a31ae64220df9b06094a914e94dd0f3.

Treat this as a read-only analytical session only when the owner explicitly
authorizes its execution. Do not infer execution permission from the
scientific decision alone.

Own no repository-writing paths. Do not branch, edit files, commit, push,
resume automation, or dispatch another workflow. Other sessions may exist;
do not disturb their work. Do not start Generation 3.

Read in order:
1. AGENTS.md and the complete Post-G2 Frontier Scientific Decision v2.
2. docs/design-inputs/KICKOFF_PROMPT.txt and PACKAGE_README.md.
3. The accepted review, canonical specification, registry, and
   docs/reviews/PROSPECTIVE_AMENDMENTS.md.
4. docs/reviews/FRONTIER_POST_10M_SCIENTIFIC_DECISION_V1.md and
   docs/reviews/FRONTIER_G2_BYT5_MILESTONE_DECISION_V1.md.
5. The four G2 scientific reports and all three required independent reviews.
6. The campaign freeze, scientific results, independent results, independent
   accounting, corpus freeze, and observation receipts under
   experiments/manifests/generation_2/.

Verify the branch, HEAD, live remote branch, clean/dirty state, ancestry,
and frozen identities before analysis. If HEAD differs, identify the
difference and stop dependent analysis; do not silently review main.

Bind these SHA-256 identities:
execution-campaign-freeze.attempt01.json:
084be260a7f6797d9e138839fe56660c3ce47cb6d92d813c4c3a518b3344cb14
scientific-results.attempt01.json:
510e0efceec1127f38d524f8ca71a224cbaea59cd8206f5dc138889d9be74edd
scientific-results-independent.attempt01.json:
8f952fc01a96e2e8468c4ac65234de5922bc3aad1984155f1803aecc8d8b5cf7
scientific-accounting-independent.attempt01.json:
3dfdad614f2b16bda60e97a454f9dc08b6eb8a132e710ebaf18dc0d271bb8334

Resolve retained private artifacts under
/Volumes/Research Archive/LocalFlowResearch-G2-artifacts
through the frozen manifest and observation receipts. Verify each consumed
payload hash. Do not load checkpoint arrays or model runtimes.

If this study is partly completed, inspect the supplied prior analytical
output and its input identities. Reuse verified mechanical results without
rerunning neural work or inventing missing evidence.

Settle these questions:
- Reconstruct D0/D1 presentations, repetitions, error-bearing support,
  per-group exposure, identity/repair exposure, and phase allocation.
- Analyse fixed endpoint benefit, harm, failures, and lexical-zero damage.
- Reproduce whole-output oracle gain as both positive-error-reduction sums
  and per-case minimum-error sums, accepting only complete cached outputs.
- Separate C immediate END, missing edits, incorrect spans, incorrect
  replacement text, surface-only supervision, and invalid/capped programs.
- Analyse source/output edit burden and TRAIN-only local correction support.
- Identify exact source/target conflicts without claiming semantic or
  acoustic recoverability from their absence.

Expected review calculations, to verify rather than assume:
D0 real presentations: 18,693; repetition 763x18 and 261x19.
D1 real presentations: 19,538; repetition 8,688x1 and 5,425x2.
Error-bearing presentations: D0 6,102; D1 7,390.
Whole-output oracle gains at prescribed candidate endpoints:
B100-D1-U8 2; C101-D1-U8 3; exact ten-pass ByT5 109.

Use all 2,696 natural and 288 generated DEVELOPMENT cases. Keep the
12 TRAIN diagnostic states separate. Other cells and intermediate
checkpoints remain descriptive, never candidates for retrospective selection.

For descriptive acceptance analysis, use source/output length, lexical edit
distance, relative edit burden, edit composition, validity/completion, and
TRAIN-only local support. Use fixed edit-count bins 0, 1, 2, 3–4, and >=5.
Do not fit a model, calibrator, threshold, or guard. Do not select a favorable
point from a curve. Probability traces absent from retained records are
unavailable; do not generate them with new forward passes.

Use existing source groups and the registered 10,000 paired PCG64 seed-42
bootstrap draws over 52 groups. Preserve fixed denominators, alignment
bounds, failures, and coverage. Existing CAL/HPO data are already consumed
development evidence, not fresh validation.

Any local edit omission is a labelled analytical counterfactual, not model
inference or system performance. Do not search arbitrary edit subsets or
sum isolated gains as jointly achievable.

Use no final or sealed references, audio, N-best, acoustic confidence,
teacher hints, human annotation, new downloads, paid APIs, training,
inference, benchmarks, builds, or test-suite execution. Do not modify,
delete, prune, relocate, or persist files. Use read-only in-memory
calculations and return results in chat.

Bound work to four elapsed CPU-compute hours, 8 GiB working memory, and
two working days. Stop on identity conflict, protected-data access,
required inference, or exhausted budget. Report partial work explicitly.

Close out:
1. Report exact identities and input coverage.
2. Return exposure, proposal, C-program, support, and uncertainty tables.
3. Separate FACT, MEASURED RESULT from retained receipts, CALCULATION,
   INFERENCE, and PROPOSED NEXT ACTION.
4. Identify independent arithmetic checks and all unrun/unavailable checks.
5. Recommend one next scientific decision without selecting a model or
   authorizing a neural experiment.
6. State that repository files, historical results, automation, and
   ORCHESTRATION.html were unchanged under read-only scope.
7. End with exactly:
FRONTIER_MODEL_REVIEW_REQUIRED
```

## W. Unresolved scientific uncertainties

The following remain consequential:

- Whether source conditioning is weak in B, versus learned but unable to generalize; cached outputs cannot establish the causal distinction.
- Whether additional natural exposure would produce useful transfer rather than stronger memorization or overcorrection.
- How much C’s local useful content can be separated from harmful replacements without reference access.
- Whether any available acceptance signal can approach a meaningful fraction of ByT5’s oracle headroom.
- The prevalence of genuinely reference-ambiguous natural errors.
- The causal effect of surface-target pressure on lexical damage.
- The appropriate scratch model size, depth allocation, and training horizon.
- Robustness across training seeds, recognizers, domains, and longer recordings.
- Whether a sufficiently distinct positive or negative result can support a compelling manuscript within the resource horizon.

None is resolved by 514 engineering tests, a narrow TRAIN fit, or a descriptive group-bootstrap interval.

## X. Explicit prohibitions and next authorization boundary

No seventh scratch G2 recipe, replacement G1 slot, retrospective checkpoint selection, weakened RAW gate, removed failed sample, teacher corpus, changed inference input, final seed, final 150M run, sealed inference, or protocol freeze is authorized.

This review changed no repository files. `ORCHESTRATION.html` and `docs/LOG.md` remain unchanged because the session is read-only; a later authorized recording session should register this decision and realign the page to the feasibility-study recommendation.

The next boundary is **explicit owner authorization for the bounded read-only analytical stage**. Its completion returns to frontier review. Implementation and any new neural execution remain separate decisions.

AUTHORIZE_READ_ONLY_TASK_FEASIBILITY_STUDY
