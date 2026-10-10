# Post-Feasibility Frontier Scientific Decision v3

**Date:** October 10, 2026  
**Scientific checkpoint:** `609f97f31979d469ad8551d06b2c07c3513181ec`  
**Recorded authority checkpoint:** `f7dda7bbeddfcb21d9ac7c7441bf8158afbcd06a`  
**Scope:** Scientific design only. No execution permission.

## A. Final disposition

**AUTHORIZE_PROSPECTIVE_ACCEPTANCE_DESIGN**

**INFERENCE — The strongest next investment is one bounded experiment testing whole-output acceptance around the fixed ten-pass ByT5 proposer, using candidate-versus-identity conditional scores.**

The experiment must first establish fresh, independent data. **No eligible fresh population has yet been qualified.** That prerequisite currently blocks implementation, fitting and inference.

This choice is justified by three observations:

- The fixed scratch proposals have effectively exhausted their whole-output usefulness.
- ByT5 contains useful corrections, with a measurable but limited ceiling.
- Testing whether additional source-only scoring information can identify those corrections is cheaper and more causally interpretable than changing the proposer, curriculum and acceptance mechanism together.

This is a feasibility investment, not an assertion that a gate will succeed or that the resulting method is already manuscript-worthy.

## B. Verified study evidence

**FACT — I read the complete preceding chat report, including its group and diagnostic-exposure appendices, the complete v2 decision, all four requested scientific reports and all three requested independent reviews.** The feasibility study remains a chat report; it has not become a committed scientific report or a separately published independent review.

The working tree remains clean at the authority checkpoint. The scientific and authority local branches resolve to the supplied commits. Their difference consists of decision-recording and accompanying documentation/receipts; the seven requested G2 reports and reviews are byte-identical to their frozen scientific versions.

**FACT — Fresh checks in this review verified:**

| Input | Verification |
|---|---|
| Four principal scientific receipts | Exact hashes match the study and historical Git objects |
| Decision v2 | SHA-256 `874957b90a0dd33cffbde3b9a60980be88d06b3733b74b0b4de3e28180f3f88b` |
| Frozen scientific sources | 47/47 current hashes match |
| D0/D1 natural files and presentation ledgers | Exact private payload hashes match |
| Frozen evaluation panel | Exact private payload hash matches |
| Three prescribed endpoint output files | Exact private payload hashes match |
| ByT5 endpoint `state.pt` | 3,595,841,611 bytes; SHA-256 `d6b319df934d7be5c2c3f9d6b7294e8df4cc3e4d92120a09cec78b497f315373` |
| ByT5 checkpoint state identity | Receipt binds `37544640d727edba53e2e927d43f227440025e44ecd83e7c20385558341eb3ca` |

The checkpoint was hashed as bytes; no model arrays were loaded.

**CALCULATION — I independently reaggregated the retained endpoint scores:**

| Endpoint | Better / equal / worse | Output errors | Whole-output oracle gain |
|---|---:|---:|---:|
| B100-D1-U8 | 2 / 297 / 2,397 | 16,997 | 2 |
| C101-D1-U8 | 3 / 2,197 / 496 | 4,095 | 3 |
| ByT5 ten-pass | 67 / 2,360 / 269 | 1,650 | 109 |

Both positive-gain summation and RAW-minus-oracle-error summation reproduce these ceilings.

**CALCULATION — Independent ledger aggregation also reproduces:**

- D0: 18,693 natural presentations; 763 records presented 18 times and 261 presented 19 times.
- D1: 19,538 natural presentations; 8,688 records presented once and 5,425 presented twice.

Evidence status remains distinct:

| Evidence class | Status |
|---|---|
| G2 execution, endpoint scores, accounting and failure dispositions | Previously independently qualified, committed evidence |
| Feasibility-study C decomposition, local support and detailed exposure analyses | New calculations in the preceding chat report |
| Endpoint and repetition reconciliation above | Fresh calculations in this review |
| Scientific prioritization and proposed protocol below | Inference and prospective design |

I did not repeat the complete scorer reconstruction, C omission analysis, local-mapping analysis, all checkpoint inventories or historical tests. Their prior verification is not represented as newly executed verification.

## C. What the feasibility study actually resolves

**INFERENCE — It resolves the immediate investment question more strongly than it resolves the underlying learning mechanisms.**

1. **Whole-output acceptance cannot materially rescue the fixed scratch endpoints.** Their oracle gains are two and three errors.
2. **D1 supplied diversity with little repetition.** It did not test sustained learning over many passes of the enlarged natural corpus.
3. **C101 has several distinct failures.** Missed activation, wrong localization, wrong replacement and harmful action coexist.
4. **ByT5 has useful proposals.** Its poor aggregate result does not mean every proposal is useless.
5. **The examined simple features do not establish an effective acceptance rule.**
6. **The text records do not establish general source-only recoverability or impossibility.**
7. **The existing DEVELOPMENT panel cannot provide fresh validation for a new policy.**

These findings justify a focused decision experiment. They do not justify another broad neural campaign.

## D. What remains scientifically unknown

The following remain unresolved:

- Whether conditional model scores distinguish useful corrections from confident overcorrection.
- Whether the fixed proposer retains useful headroom on a genuinely independent population.
- Whether additional natural exposure would improve scratch generalization.
- Whether surface-target pressure causally contributes to lexical damage.
- Whether a substantially better proposer would deliver enough additional benefit to justify its cost.
- How results transfer across source families, recognizers, domains and longer inputs.
- How much ambiguity is inherent in the available 1-best text.
- Whether a successful acceptance policy would constitute more than an incremental application of established methods.

No observation here estimates training-seed uncertainty.

## E. Scratch proposal quality verdict

**INFERENCE — Suspend further B100/C101 execution. Do not pursue acceptance-only rescue of these endpoints.**

B100’s selected D0 TRAIN success establishes representational capacity for those examples. Its heldout damage establishes failed transfer under the tested recipe. Neither result proves that scratch correction is fundamentally impossible.

D1’s sparse repetition is a credible contributor, but it is not an identified sufficient cause. A future scratch intervention would need to demonstrate improved **proposal generation**, including substantial heldout beneficial coverage and preservation. Merely reducing catastrophic damage would be inadequate.

The present evidence does not select a replacement architecture, copying mechanism, model size, objective or training horizon.

## F. C101 edit-level salvage verdict

**INFERENCE — The current C101 proposal population does not justify an edit-level acceptance research program as the next investment. Better local proposals are the prerequisite.**

The decisive combination is:

- Immediate no-edit on 661/878 error-bearing cases.
- Only 207 valid active programs in that stratum.
- No lexical-exact output among those 878 cases.
- Only eight individually helpful events in the omission diagnostic, distributed across seven active programs.
- Extensive harmful localization/replacement behavior.

The 1,452 harmful-event findings identify damage in the surrounding predicted programs. They do not establish 1,452 recoverable errors, independent decisions or a jointly valid partial-edit policy.

There could be useful combinations that this diagnostic does not expose. Searching arbitrary reference-aware subsets would answer a different question and would not establish deployability. The evidence presently offers too little positive content to justify that added complexity.

## G. ByT5 oracle headroom verdict

**INFERENCE — The ceiling is sufficient for one inexpensive feasibility intervention, but insufficient to justify an open-ended acceptance project.**

The 109-error ceiling corresponds to:

- 0.214036 WER percentage points.
- 7.714% of RAW errors.
- Beneficial proposals across 36 groups.

That is neither trivial nor a large capability reserve. A deployable policy would need to capture a substantial fraction while avoiding damage.

**CALCULATION — A particularly relevant decomposition is:**

| ByT5 whole-output outcome | Repairs | Introductions |
|---|---:|---:|
| Beneficial | 115 | 6 |
| Equal | 5 | 5 |
| Harmful | 0 | 346 |

Under the registered scoring, harmful complete proposals contain no credited repairs. Therefore, the retained ByT5 evidence gives little positive reason to prioritize extracting useful edits from harmful outputs.

The difference between 120 gross repairs and 109 whole-output net gain is **not** an edit-level oracle bound. Recombining edits changes outputs and can change alignments and interactions. Nevertheless, the observed distribution favors testing complete-proposal selection first.

## H. Inference-available acceptance signal verdict

**INFERENCE — Test conditional preference for the candidate against copying the source, rather than interpreting proposal likelihood alone as confidence.**

The proposed additional information is:

\[
L(O\mid S),\qquad L(S\mid S),
\]

where the same frozen correction model scores both the complete proposal and the identity output, conditioned only on the ASR source.

The hypothesis is that their contrast contains contextual information missing from edit counts and lengths. This is plausible because those probabilities depend on the source and complete preceding output context.

It may still fail:

- The model may confidently prefer incorrect corrections.
- Surface restoration may dominate the score difference.
- Sequence length affects likelihood.
- Adaptation may favor familiar target styles.
- Pretrained linguistic preference is not reference truth.

**These quantities are currently unavailable.** Extracting them requires new model passes under separate authorization. They are not calibrated probabilities of correctness.

Do not add ensembles, disagreement sampling, a second language model, a neural judge or a separate detector to this initial intervention.

## I. Natural-exposure dilution verdict

**INFERENCE — The exposure deficit is established; an exposure-focused pilot is scientifically plausible but is not the strongest next investment.**

The enlarged corpus received only 1.384397 repair presentations per record on average, versus 18.254883 for D0. Its first full natural pass finished around 7,218,011 canonical exposure.

This rules out the interpretation that G2 adequately tested sustained learning from D1. It does not establish that more passes would solve generalization, copying or replacement quality.

ByT5 already supplies a cheaper way to test whether useful correction can be made selective. A scratch exposure pilot would require additional training and would still need fresh evaluation data.

No future pilot should inherit the 10M budget or 15/15/20/10/40 mixture automatically. Such a pilot would require a separate decision binding natural passes, presentations, canonical charge, native supervision and optimizer geometry.

## J. Source-only information/recoverability verdict

**INFERENCE — Useful source-only correction is empirically possible for some examples; its reliable selectable extent remains unknown.**

The collision analysis supplies no identical-source/conflicting-reference witness in these populations. Because most full sources are unique, that absence is weak evidence about general recoverability.

The local support counts establish recurring patterns under specified context keys. They do not show that unsupported corrections are impossible, or that supported corrections are appropriate in a new sentence.

The next study may claim only reference-conditional correction performance under a strict 1-best-text boundary. It must not claim recovery of acoustic truth or use fluent model output as a correctness label.

## K. Lexical versus surface-target verdict

**PROPOSED NEXT ACTION — Separate the scientific claims and acceptance behavior, while retaining the frozen proposer and historical scoring targets.**

For the proposed policy:

- Primary utility concerns lexical correction and lexical preservation.
- If source and proposal are lexically identical under `lexical_eval_v1`, return RAW.
- If a lexical change is accepted, return the entire original proposal, including its surface form.
- Report surface correctness separately wherever valid surface references exist.
- Do not train a formatting stage or alter ByT5’s adaptation targets.

This deliberately defers surface-only restoration. It does not declare normalization-equivalent text to be raw-reference correct.

The proposed capability question is consequently narrower than full transcript surface restoration. That scope must be recorded prospectively. Historical G2 targets and outcomes remain unchanged.

## L. Prospective fresh-data feasibility

**FACT — No fresh independent population is established in the qualified local supply.**

I compared the complete group sets, not just their counts:

| Role | Larger qualified metadata pool | G2 population | Groups outside G2 |
|---|---:|---:|---:|
| TRAIN | 45,729 rows / 314 groups | 14,113 / 314 | 0 |
| CAL | 6,271 / 40 | 1,900 / 40 | 0 |
| HPO DEVELOPMENT | 898 / 12 | 796 / 12 | 0 |

The 36,089 additional metadata rows do not supply new independent groups. They cannot satisfy the proposed separation contract merely because their individual utterances were unused.

Therefore:

- D1 TRAIN cannot serve as independent policy-fitting evidence under this design.
- CAL/HPO cannot become untouched evaluation.
- Cross-validation cannot erase their historical use.
- Protected final populations remain unavailable.
- New independent source families must be qualified.

**PROPOSED NEXT ACTION — Limit the first external availability assessment to TED-LIUM release 3’s legacy training partition.** Its published description establishes a substantial English transcribed-speech corpus, making it a reasonable candidate for a bounded provenance assessment. It does not establish project eligibility. [TED-LIUM 3 paper](https://arxiv.org/abs/1805.04699)

Current availability remains unresolved: the inspected OpenSLR landing page returned “Resource not found,” and the author-linked landing page timed out. No corpus was downloaded.

The prerequisite must establish official release identity, lawful access, usable reference conventions, source-family identities, overlap exclusions and sufficient eligible groups. It must also acknowledge that this introduces a talk-speech domain; it would not provide an untouched replication on the original literary-speech population.

If this single candidate cannot satisfy the contract within the qualification budget, stop. Do not silently substitute another dataset.

## M. Chosen next scientific direction

**PROPOSED NEXT ACTION — Test this single falsifiable hypothesis:**

> For a fixed pretrained correction proposer, candidate-versus-identity conditional scores provide incremental information beyond source/output edit features, enabling whole-output acceptance that improves lexical accuracy over RAW while meeting explicit preservation requirements on independent source groups.

There are two separate tests:

1. **Capability:** Does the accepted-output system meet the benefit and preservation criteria?
2. **Mechanism:** Does adding the conditional scores improve on an otherwise identical policy using only text-edit features?

A successful capability result without the second result would not establish the proposed scoring mechanism.

## N. Rejected alternatives

| Alternative | Why it is not next |
|---|---|
| Whole-output gating of B100/C101 | Their fixed oracle ceilings are negligible. |
| C101 edit-level acceptance | Insufficient demonstrated useful local content; substantial interaction and rendering complexity. |
| ByT5 edit-level acceptance | Little demonstrated repair content in harmful complete outputs; additional complexity lacks an immediate evidence-based payoff. |
| Better proposer | Potentially valuable, but combines greater cost with unresolved selection and data questions. |
| Natural-exposure pilot | Addresses a real limitation, but its causal payoff is uncertain and it needs the same fresh-data solution. |
| Immediate manuscript pivot as the main investment | Writing around failed recipes would not meet the capability objective. First test one bounded, credible route to utility. |
| Termination now | ByT5’s useful proposals justify one focused attempt, subject to strict data and cost limits. |

## O. Exact implementation-ready protocol

**PROPOSED NEXT ACTION — The prerequisite below is fully specified. The main experiment is conditional and must not run until its missing data identities are supplied and approved.**

### O1. First gate: `POST_FEASIBILITY_FRESH_DATA_QUALIFICATION_V1`

Scope: candidate-blind provenance and availability qualification only.

1. Inspect the official TED-LIUM release 3 legacy-training documentation and existing local inventories.
2. Establish authoritative release locations, checksums, licensing/access terms, segment/reference conventions, speaker identities and talk/source identifiers.
3. Establish whether metadata sufficient for qualification is already available. If obtaining it requires a download, report the exact acquisition request and stop before acquisition.
4. Exclude official development/test partitions, all project-protected populations, and known relatives of G1/G2 training or consumed development sources.
5. Construct the proposed grouping rule from connected speaker, talk, recording and derivation-family identities. Exact/near-duplicate transcript families must not cross roles.
6. Use existing permitted exclusion metadata and fingerprints for protected populations. Do not open protected reference text. If the exclusion check cannot be completed from permitted material, stop.
7. Verify that existing released transcripts can supply automatic reference labels without new listening, annotation, adjudication or model-generated “gold.”
8. Produce a candidate population-binding table: release/hash, reference field/parser, grouping rule, exclusions, counts, acquisition size, recognizer identity and complete projected cost.
9. Return to frontier review before source construction, correction inference or fitting.

**Caps:** one working day, two CPU hours, 8 GiB working memory; zero neural calls, corpus downloads, persistent writes or protected-reference access under the read-only prerequisite.

The reference parser and actual population identities are unresolved scientific bindings. Sol may document them, but may not invent missing conventions or approve a substitute population.

### O2. Frozen proposer

Use only:

- `google/byt5-small`
- Revision `68377bdc18a2ffec8a0533fef03b1c513a4dd49d`
- 299,637,760 parameters
- G2 exact ten-pass endpoint: update 35,283; 141,130 presentations
- Checkpoint directory relative to the private root:  
  `scientific-checkpoints-v1/G2-ByT5-D1-10pass-seed42-lr3e-4.attempt01.update35283`
- `state.pt` SHA-256:  
  `d6b319df934d7be5c2c3f9d6b7294e8df4cc3e4d92120a09cec78b497f315373`

Load the saved model weights without advancing optimizer state. No fine-tuning, checkpoint substitution, quantization change or decoding search.

### O3. Candidate and inference boundary

For each source \(S\):

- Input is raw ASR 1-best text, without a prefix.
- Generate one greedy proposal \(O\).
- Preserve the G2 FP32 MPS/eager implementation and disabled CPU fallback.
- Use source capacity 512 including EOS and maximum 512 emitted output positions.
- Use the frozen byte encoding and strict completion/UTF-8 validation.
- No audio, N-best, acoustic scores, references, error masks, speaker identity or corpus role enters the correction system.

Return RAW for source overflow, incomplete/invalid generation, scoring failure or lexical identity. Do not truncate, regenerate, repair an invalid output or construct partial edits.

The evaluated policy chooses exactly \(S\) or the complete \(O\).

### O4. Conditional scores

For valid lexically changed proposals, make two teacher-forced sequence evaluations:

\[
L(Y\mid S)=\sum_{t=1}^{|Y_{\mathrm{bytes}}|+1}
\log p_\theta(y_t\mid y_{<t},S),
\]

for \(Y=O\) and \(Y=S\).

Include EOS; exclude decoder-start and PAD. Use raw byte strings, natural logarithms, dropout disabled and unmodified vocabulary logits.

Reference text never enters these scoring passes. Retain target-token log probabilities and aggregate scores; full vocabulary-logit archives are unnecessary.

These are conditional scores, not correctness probabilities.

### O5. Prospective populations

The conditional design targets **12,000 cases**:

| Population | Cases | Minimum independent groups | Permitted use |
|---|---:|---:|---|
| FIT | 4,000 | 80 | Fit the two fixed linear policies |
| SELECT | 2,000 | 40 | Choose one threshold per policy |
| EVAL | 6,000 | 100 | One untouched assessment |

These are prospective requirements, not established available counts or a power guarantee.

After complete source-family closure, assign components using SHA-256 of `POST_FEASIBILITY_ACCEPTANCE_V1|<component_id>`, interpreted as an unsigned integer modulo six:

- 0–1: FIT.
- 2: SELECT.
- 3–5: EVAL.

Within each role, rank eligible records by SHA-256 of `POST_FEASIBILITY_CASE_V1|<stable_id>`. Admit at most 60 records per component, then take the first required number. Do not reshuffle or rebalance after inspecting outcomes. Insufficient cases/groups fails qualification.

Use published segment boundaries, English speech and a prospective 2–12-second duration range. Reference-validity and annotation-marker rules must be frozen before source construction. Do not select by recognizer error rate, proposal quality or reference inferability.

No role may overlap the proposer’s project adaptation data, previous consumed development groups or protected final families. Undocumented upstream pretraining overlap remains a disclosed limitation.

### O6. Automatic supervision and reference use

After separately authorized source construction:

- Source: one output from the frozen, hash-bound G2 Parakeet recognizer implementation.
- Reference: the qualified official transcript, parsed by the frozen automatic rule.
- FIT labels: registered scorer repair/introduction counts for \(S,O,R\).
- SELECT labels: the same quantities, used only for the prescribed threshold decision.
- EVAL references: unavailable to fitting, threshold selection and inference; scored once after both policies are frozen.

An upstream ASR failure must remain a construction failure. It cannot be silently replaced. Unresolved source/reference construction failures block the main experiment.

Once the case population is fixed, correction failures remain in every evaluation denominator and return RAW.

### O7. Exact policy features

Let \(n_S,n_O\) be lexical word counts; \(b_S,b_O\) be UTF-8 byte counts.

The **structural baseline** uses eight features:

1. \(\log(1+n_S)\)
2. \(\log(1+n_O)\)
3. \(\log(1+b_S)\)
4. \(\log(1+b_O)\)
5. Lexical insertions divided by \(\max(1,n_S)\)
6. Lexical deletions divided by \(\max(1,n_S)\)
7. Lexical substitutions divided by \(\max(1,n_S)\)
8. Byte Levenshtein distance divided by \(\max(1,b_S)\)

Use one fixed minimum-distance traceback with match, substitution, deletion, insertion priority. These counts are features only; no local edits are applied.

The **primary policy** adds exactly two features:

\[
\frac{L(O\mid S)-L(S\mid S)}{\max(1,b_S)}
\]

and

\[
\frac{L(O\mid S)}{b_O+1}-\frac{L(S\mid S)}{b_S+1}.
\]

No lexical lookup tables, pretrained embeddings, reference-derived features, group IDs or additional confidence signals.

### O8. Fitting objective and regularization

Fit only on valid, lexically changed FIT proposals.

For case \(i\), define conservative utility:

\[
u_i=R_i^{\mathrm{lower}}-4I_i^{\mathrm{upper}},
\]

where \(R\) is completed genuine repair and \(I\) is introduced error.

The factor four is a prospective preservation preference: introducing one error costs four credited repairs. It is not estimated from the current DEVELOPMENT panel.

For each of the two feature sets, fit one ridge regression:

\[
\min_{a,w}\frac1N\sum_i(u_i-a-w^\top z_i)^2
+0.01\lVert w\rVert_2^2.
\]

Standardize using FIT means and population standard deviations only. Set constant standardized columns to zero. Leave the intercept unpenalized. Use deterministic float64 linear algebra.

Exactly two fits are permitted. No regularization search, neural detector, calibration model, cross-validation or post-selection refit.

### O9. Policy-selection rule

For each fitted policy, evaluate only:

\[
\tau\in\{0,\;0.25,\;0.5,\;1,\;2,\;4,\;+\infty\}.
\]

Accept when predicted utility is strictly greater than \(\tau\), subject to mandatory RAW fallback.

On SELECT, a finite threshold is eligible only if:

- Corpus errors are below RAW.
- Completed repair lower bound is at least 10, across at least five groups.
- Introduced-error upper bound is at most one quarter of completed-repair lower bound.
- At most 0.5% of originally lexical-zero cases acquire errors.

Among eligible thresholds, maximize total conservative utility; break ties toward the largest threshold. If none qualifies, select \(+\infty\), declare selection failure and stop before EVAL.

Apply the same rule independently to the structural baseline. Freeze both policy files before EVAL. The primary policy remains primary regardless of which policy later performs better.

### O10. Baselines and causal comparison

Report:

- RAW.
- Accept every complete valid ByT5 proposal.
- Structural policy.
- Primary policy with conditional scores.
- Reference-aware whole-output oracle, explicitly diagnostic.

The structural policy is the single necessary control for the scoring hypothesis. Both learned policies share proposals, fitting labels, regularization, selection procedure and evaluation cases.

The causal contrast concerns **adding these two score features within this fixed procedure**. It does not isolate pretraining, architecture or the original adaptation objective.

## P. Acceptance and failure criteria

All numerical requirements below are **prospective design choices**, not measured achievements.

### Capability success

On EVAL, require all of:

| Requirement | Bound |
|---|---|
| Absolute WER improvement over RAW | At least **0.10 percentage points** |
| Relative RAW error reduction | At least **3%** |
| Paired group-bootstrap interval for WER gain | Two-sided 95% lower endpoint strictly above zero |
| Completed genuine repair lower bound | At least **50 errors** |
| Independent repair support | At least **20 groups** |
| Introduced errors | Upper bound ≤25% of completed-repair lower bound |
| Lexical-zero preservation | At least **99.5%** of originally lexical-zero cases remain lexical-zero |
| Evaluation information | At least 100 groups, 100,000 reference words and 1,000 RAW errors |

The information requirements are checked automatically without exposing case-level evaluation outcomes during fitting. If unmet, report insufficient evaluation information; do not add cases after seeing policy results.

The point preservation requirement must be accompanied by its group-bootstrap interval. It is not a distribution-free safety guarantee.

### Mechanism success

In addition to capability success, require a positive lower endpoint of the paired 95% group-bootstrap interval for primary-policy WER improvement over the structural policy.

Use hierarchical interpretation: assess the mechanism claim only after capability success. Report both policies even if the primary policy loses.

### Uncertainty

Use 10,000 paired source-group draws with PCG64 seed 42, resampling complete evaluation components and sharing draws across policies.

The new evaluation has a different group population, so it receives a new draw identity. Preserve the historical 52-group draw identity for historical results; do not pretend those draws apply unchanged to new groups.

Keep separate:

- Scorer alignment bounds.
- Evaluation-group sampling intervals.
- Unmeasured training-seed and policy-fitting-sample uncertainty.

### Failure and stopping

- Failed data qualification: no inference or fitting.
- Missing or ambiguous reference convention: no implementer-chosen substitute.
- FIT has fewer than 40 beneficial proposals across 20 groups, or fewer than 200 valid lexical-change proposals: stop as insufficient fitting support.
- No SELECT threshold qualifies: stop before EVAL.
- EVAL fails capability criteria: abandon this exact acceptance treatment; do not retune on EVAL.
- Capability passes but mechanism fails: no claim that the added score information helped.
- New population lacks oracle headroom: report proposer limitation on that population, not acceptance impossibility.
- Budget, identity or protected-data contradiction: stop with `FRONTIER_MODEL_REVIEW_REQUIRED`.

A negative result applies to the specified signals and policy class. It does not establish that all source-only selection is impossible.

## Q. Budget and resource estimate

**MEASURED RESULT — Historical reference:** G2 consumed 36.700589 recipe wall hours. ByT5’s endpoint observation took 7,074.588477 seconds for 2,984 cases, including 4,916.474747 decode seconds.

**CALCULATION — Linear scaling to 12,000 cases gives approximately:**

- 5.49 decode hours.
- 7.90 observation hours.

This is a planning extrapolation from a different population, not a forecast validated on the proposed data.

| Work | Estimate/status | Prospective cap |
|---|---|---:|
| Read-only availability/provenance qualification | Up to one analyst day | 2 CPU hours |
| Authorized acquisition and reference/source preparation | **UNMEASURED**; requires exact release and byte inventory | 2 analyst days; stop if unresolved |
| New recognizer source construction | **ASSUMED** 1–3 model hours | 12,000 unique calls, no quality-based retries |
| ByT5 proposal generation | **CALCULATED** historical scaling: 5.49 hours | 12,000 greedy sequences |
| Conditional score extraction | **ASSUMED** 1–3 model hours | Two sequence-scoring passes per valid changed proposal; maximum 24,000 |
| Runtime/scoring qualification | **ASSUMED** up to 2 hours | FIT-only qualification, charged within total |
| Total new model work | **ASSUMED** approximately 8–14 hours | **16 elapsed model hours**, all stages included |
| Two policy fits | Expected small; **UNMEASURED** | 15 CPU minutes |
| Selection, scoring, uncertainty | **ASSUMED** 0.5–2 CPU hours | 2 CPU hours |
| Independent result/code review | **ASSUMED** one analyst day | 4 CPU hours |
| New evidence and acquisition storage | **UNESTABLISHED** until release inventory | **80 GiB maximum**, including temporary copies and failed attempts |

Additional limits:

- New neural training: **zero**.
- New proposer checkpoints: **zero**.
- Policy artifacts: two small fits plus frozen threshold records.
- Maximum unified-memory use: **32 GiB**, leaving operating headroom on the 48 GiB machine.
- One accelerator workload at a time.
- No cloud spending, paid API calls, teacher generation or evidence deletion.

**FACT — Current free space was approximately 321.294 GiB.** That does not establish acquisition feasibility. An archive plus extracted audio, temporary data and retained failures must fit the 80 GiB allowance and the existing storage policy.

Measure proposal-generation and score-extraction latency separately, including warm median, p95 and cold load. The gate adds computation after generation; it cannot recover the generation cost. Require mean scoring overhead no greater than 25% of mean proposer latency for an efficiency claim. Missing or failed timing is not PASS.

Electricity and depreciation remain **UNPRICED**.

## R. Paper contribution and novelty

**INFERENCE — Selective correction itself is established. The possible contribution is a controlled account of useful-proposal headroom versus attainable source-only selection in a low-error regime.**

| Nearest work | What it already establishes; consequence here |
|---|---|
| [Zhang, Stahlberg and Kumar](https://arxiv.org/html/2501.13831v1) | Compact phrasal ASR rewriting and accuracy/efficiency comparisons. No first compact-representation claim. |
| [FastCorrect](https://proceedings.neurips.cc/paper/2021/hash/b597460c506e8e35fb0cc1c1905dd3bc-Abstract.html) | Edit-aligned nonautoregressive correction. Efficient structured correction is established. |
| [PATCorrect](https://arxiv.org/html/2302.05040v2) | Phoneme-augmented correction and latency/accuracy evaluation. A compact correction model alone is insufficient novelty. |
| [SoftCorrect](https://arxiv.org/abs/2212.01039) | Explicit soft error detection and constrained correction. Detection before editing is not new. |
| [ConstDecoder](https://www.isca-archive.org/interspeech_2022/yang22g_interspeech.html) | Keep/delete/change prediction and selective decoding. Preservation operations are not new. |
| [ECLM](https://arxiv.org/abs/2405.15216) | Specialized correction, realistic synthetic errors and correction-first acoustic rescoring. Its acoustic scoring falls outside this source-only boundary. |
| [DARAG](https://aclanthology.org/2025.findings-acl.125/) | Synthetic augmentation and retrieval for correction/generalization. Data augmentation or retrieval alone would not distinguish this project. |
| [Conservative Data Filtering](https://aclanthology.org/2024.emnlp-industry.20/) | Explicit treatment of overcorrection and contextual inferability in supervision. Preservation and inferability are prior concerns. |
| [RED-ACE](https://aclanthology.org/2022.emnlp-main.180/) | Benefits of recognizer confidence for error detection. Those signals are excluded here; correction-model scores must not be described as ASR confidence. |

The distinguishing experiment would hold proposals fixed and measure whether conditional scores add usable selection information beyond structural features, while reporting:

- Available oracle headroom.
- Realized repairs and introduced errors.
- Preservation of initially correct cases.
- Independent group support.
- Failure-inclusive performance.
- Additional inference cost.
- Strict data-consumption boundaries.

Assessment of the three possible contributions:

| Contribution | Judgment |
|---|---|
| Useful selective system | Best immediate capability route, but likely modest effect; requires the prospective success criteria. |
| Controlled negative selection result | Valuable only when adequate fresh headroom exists and the failed signal/policy class is precisely bounded. |
| New scratch learning mechanism | Potentially stronger methodological contribution, but currently less attributable and more expensive. |

A simple ridge gate with a small WER gain is not automatically a serious manuscript. A positive result would justify a later independent replication and fuller positioning. A negative result might support a focused diagnostic contribution, but the existing failures alone do not guarantee publication value.

## S. Timeline and dependencies

**PROPOSED NEXT ACTION:**

1. **Decision recording — separate authorization.** Preserve this decision and the preceding study; realign the project record.
2. **Availability/provenance qualification — one working day.** Return exact bindings or an explicit failure.
3. **Frontier acceptance of the population binding and owner execution authorization.**
4. **Source construction and runtime qualification — up to two working days.**
5. **FIT and SELECT — bounded model/CPU work.** Stop here if selection fails.
6. **One untouched EVAL and independent review — approximately two working days.**
7. **Return for the capability/manuscript decision.**

Allow roughly one to two working weeks after successful data qualification. Acquisition remains the principal scheduling uncertainty. No calendar commitment overrides the data gate.

## T. Prospective scientific amendment

Post-Feasibility Frontier Scientific Decision v3  
Date: 2026-10-10

Reviewed scientific checkpoint:
609f97f31979d469ad8551d06b2c07c3513181ec

Recorded preceding authority checkpoint:
f7dda7bbeddfcb21d9ac7c7441bf8158afbcd06a

Disposition: AUTHORIZE_PROSPECTIVE_ACCEPTANCE_DESIGN

Preserve all Generation-1 and Generation-2 treatments, results, failures,
accounting, targets and adequacy dispositions. All Generation-2 scientific
slots remain consumed. No historical checkpoint becomes a retrospectively
selected successful model.

Adopt one dominant development direction: whole-output acceptance around
the fixed Generation-2 ByT5 exact ten-pass endpoint. The scientific
hypothesis is that candidate-versus-identity conditional model scores add
usable information beyond source/output edit features.

This decision authorizes design only. It does not authorize repository
writes, implementation, acquisition, source construction, inference,
probability extraction, fitting, testing, benchmarking, spending or
automation resumption.

The completed POST_G2_READ_ONLY_FEASIBILITY_V1 remains a chat-delivered
analytical study until separately authorized recording. Its calculations
must remain distinguished from previously independently qualified G2
evidence and from this decision's scientific inferences.

No qualified fresh independent population has been established. The
existing larger LS-PC metadata pool supplies no additional independent
TRAIN, CAL or HPO groups beyond those represented in G2. Unused utterances
from those groups do not satisfy the new independence contract. Existing
CAL/HPO data remain consumed. D1 TRAIN cannot supply independent policy
fitting under this design. Protected final populations remain sealed.

Define POST_FEASIBILITY_FRESH_DATA_QUALIFICATION_V1 as the first prerequisite.
Assess only TED-LIUM release 3 legacy-training availability and provenance,
using the exact bounded procedure in Section O1 of this decision. Establish
official release identity, access terms, reference conventions, source-family
grouping, project-overlap exclusions, eligible counts and complete costs.
Do not substitute a dataset, invent reference rules or infer execution
permission. Return unresolved bindings for frontier review.

The conditional main design is Sections O2–O10, P and Q of this decision.
Those sections are normative and must accompany this amendment when
recorded or handed off.

Freeze the proposer to google/byt5-small revision
68377bdc18a2ffec8a0533fef03b1c513a4dd49d at G2 update 35283,
141130 presentations. Bind state.pt SHA-256
d6b319df934d7be5c2c3f9d6b7294e8df4cc3e4d92120a09cec78b497f315373.

Permit no model updates or checkpoint substitution. The conditional
candidate is one complete greedy proposal under the inherited byte,
capacity, precision and decoding contracts. A policy returns either RAW
or the entire proposal. Invalid, incomplete, over-capacity, score-failed
and lexically unchanged proposals return RAW.

The inference input remains ASR 1-best text. References, audio, N-best,
acoustic scores, error masks and source-family identities cannot enter
correction inference. Any later authorized source construction is a
separate data-preparation stage.

Prospective primary utility is lexical correction and preservation.
Surface-only restoration is deferred. Historical raw-reference targets
remain unchanged, and normalization equivalence is never described as
raw-reference correctness.

The conditional study uses independent FIT, SELECT and untouched EVAL
populations, with 4000, 2000 and 6000 cases respectively and the grouping,
assignment and inclusion rules in Section O5. Qualification must establish
the actual source and reference identities before any affected policy
outcome is observed.

Compare exactly two ridge policies: the eight-feature structural control
and the primary policy adding the two specified conditional score
contrasts. Use FIT-only standardization, conservative utility
repair_lower minus four times introduced_upper, fixed regularization
0.01 and the exact SELECT threshold rule. Do not conduct additional
feature, model, regularization or threshold searches.

Evaluate once using all frozen cases and RAW fallback for correction
failures. Capability success requires every criterion in Section P,
including at least 0.10 percentage-point and 3% relative WER improvement,
positive paired group-bootstrap support, at least 50 repaired errors
across 20 groups, introduced errors no greater than one quarter of
repairs, and at least 99.5% lexical-zero preservation.

The score-information mechanism requires incremental improvement over
the structural control. Capability without that contrast does not
establish the mechanism. Negative results apply only to this proposer,
population, signal set and policy class.

Keep scoring-alignment bounds, group-sampling intervals and unmeasured
training-seed uncertainty distinct. New evaluation groups require their
own shared 10000-draw PCG64 seed42 bootstrap identity.

Respect all Section Q caps, including zero neural training, at most
16000 model-wall seconds times 3.6 (16 model hours), two CPU policy fits,
80 GiB incremental storage and no evidence deletion. Acquisition,
temporary files and retained failed attempts count against storage.

Stop at any unmet prerequisite, identity contradiction, protected-data
requirement or exhausted bound. Do not retune on EVAL or relabel historical
data as fresh. No result automatically authorizes a new proposer,
scratch pilot, edit-level search, Generation 3, final seeds, final 150M
training, sealed inference, protocol freeze, publication or production
changes.

## U. Sol implementation handoff

**PROPOSED NEXT ACTION — A handoff is justified for the prerequisite only. It is not a main-experiment implementation authorization.**

```text
FRONTIER_MODEL_REVIEW_REQUIRED escalation rule:
Stop if this task requires an unbound scientific choice, new inference,
model fitting, training, protected-reference access, acquisition, or writes
outside separately explicit owner authorization. Report the exact blocker.
Do not invent a substitute population, reference convention or policy.

Perform POST_FEASIBILITY_FRESH_DATA_QUALIFICATION_V1 in:
/Users/danny/Documents/Tools/LocalFlowResearch

Project:
Repair Without Rewrite: A Controlled Comparison of Full-Transcript
Generation and Compact Editing Under Matched Source Exposure.

Scope:
Qualify the availability and provenance of a fresh independent population
for the design-only Post-Feasibility Frontier Scientific Decision v3.
Do not implement or execute its acceptance experiment.

Other work and ownership:
Own no writing paths under read-only authorization. Do not branch, switch
worktrees, edit the orchestration page, commit, push or resume automation.
Respect other sessions. Do not start Generation 3.

Startup:
1. Read AGENTS.md.
2. Verify the scientific checkpoint:
   609f97f31979d469ad8551d06b2c07c3513181ec
   and the recorded authority checkpoint:
   f7dda7bbeddfcb21d9ac7c7441bf8158afbcd06a.
3. Read the complete supplied v3 decision, especially O1 and Sections L–Q.
   If the decision is neither supplied nor recorded, stop; do not
   reconstruct it from this handoff.
4. Read docs/reviews/FRONTIER_POST_G2_SCIENTIFIC_DECISION_V2.md.
5. Inspect these qualified metadata records:
   experiments/manifests/public_lspc_training_roles.development.jsonl
   experiments/manifests/public_lspc_training_supply_qualification.json
   experiments/manifests/generation_2/metadata-census.attempt01.jsonl
   experiments/manifests/generation_2/metadata-census-summary.attempt01.json.
6. Inspect any existing prerequisite result before repeating work.

Evidence to preserve:
The larger qualified local metadata pool contains 45729 TRAIN rows in
314 groups, 6271 CAL rows in 40 groups and 898 HPO rows in 12 groups.
Every one of those groups is represented in the consumed G2 population.
Unused utterances are not new independent groups.

Settle:
Assess only TED-LIUM release 3 legacy-training availability and provenance.
Start from the author paper:
https://arxiv.org/abs/1805.04699

Establish authoritative release identities, access terms, official
reference conventions, speaker/talk/recording/derivation grouping,
project-overlap exclusions, eligible population counts and complete
acquisition/storage cost.

Do not assume availability: the preceding review received “Resource not
found” from the OpenSLR 51 landing page and a timeout from the author-linked
TED-LIUM 3 page.

Constraints:
Use public documentation and already permitted local metadata.
Do not download corpus/model payloads, construct ASR sources, load model
arrays, run forward passes, fit policies, execute tests or benchmarks,
or open protected final references.

Use existing permitted protected-population exclusion metadata only.
If adequate exclusion requires unavailable identities or protected text,
stop and report that exact requirement.

Do not substitute another corpus or decide an ambiguous transcript parser.
The full source/reference binding must return to frontier review before
policy outcomes exist.

Bounds:
One working day; two CPU hours; 8 GiB working memory.
Zero persistent writes under read-only execution authority.

Verification:
Separate FACT, retained MEASURED RESULT, new CALCULATION, INFERENCE and
PROPOSED NEXT ACTION. An unrun check is UNVERIFIED.
Do not describe metadata availability as qualified audio, references,
independent evaluation or statistical power.

Close out:
1. Return the exact candidate source/reference/provenance binding table.
2. Give eligible and unresolved group/case counts with their evidence.
3. Report acquisition, inference, storage and review requirements.
4. State whether all O1 prerequisites were established; list every gap.
5. State that scientific evidence, Git, automation and orchestration
   remain unchanged under read-only scope.
6. Stop before acquisition, implementation, inference or fitting.
7. Print last:
FRONTIER_MODEL_REVIEW_REQUIRED
```

## V. Unresolved risks

**INFERENCE — The largest risk is that the new score information will be confidently wrong in the same places as the proposer.** The proposed control makes that failure interpretable.

Other material risks are:

- Fresh-data acquisition may fail within the budget.
- Talk-speech transfer may reduce the proposer’s headroom.
- Reference conventions may not support the intended lexical target without a new scientific decision.
- Surface preferences may dominate raw-sequence scores.
- Sparse beneficial examples may limit fitting and evaluation precision.
- Source-family closure may leave too few independent groups.
- Upstream pretrained-model contamination may remain unknowable.
- Added scoring may cost too much relative to its small benefit.
- A positive result may be useful but insufficiently novel for the intended manuscript.

None justifies weakening the evaluation, adding favorable cases or broadening the intervention after observing outcomes.

## W. Next authorization boundary

**FACT — This review performed read-only inspection, hashing, bounded retained-data aggregation and primary-source literature reading.** It performed no training, inference, fitting, tests, benchmarks, corpus downloads, repository writes, commits, pushes or automation changes.

Final checks show:

- HEAD remains `f7dda7bbeddfcb21d9ac7c7441bf8158afbcd06a`.
- Working tree remains clean.
- Git index, `ORCHESTRATION.html` and `docs/LOG.md` hashes remain unchanged.
- The continuation automation remains byte-unchanged and **PAUSED**.

**PROPOSED NEXT ACTION — Separately authorize recording this decision and executing only the bounded fresh-data prerequisite.** Main implementation, acquisition, recognizer calls, probability extraction, policy fitting and untouched evaluation remain held until the population binding is complete and explicit execution permission is granted.

AUTHORIZE_PROSPECTIVE_ACCEPTANCE_DESIGN
