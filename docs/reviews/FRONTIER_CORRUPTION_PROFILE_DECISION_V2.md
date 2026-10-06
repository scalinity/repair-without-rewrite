<!-- Decision provenance: date 2026-10-05; reviewed checkpoint 1b114ff485a2a59051bf7a2e39acec5774fd35a1; disposition CORRUPTION_PROFILE_REVISION_AUTHORIZED; six_10M_recipes_started=false; final_training_started=false; affected_final_outcomes_seen=false; sealed_candidate_inference=none; paper_protocol_v2_frozen=false. The complete approved Astra response below is preserved verbatim. -->

# Frontier Corruption-Profile Decision v2

## A. Final disposition

**CORRUPTION_PROFILE_REVISION_AUTHORIZED**

Choose **Option B: a lexical-first empirical profile**, implemented as supported character edits in the representation defined below.

Authorize a prospective revision of the DEVELOPMENT corruption treatment only. This does **not** admit the six probes.

I reviewed the ten requested documents and associated implementation evidence at [checkpoint `1b114ff485a2a59051bf7a2e39acec5774fd35a1`](https://github.com/scalinity/repair-without-rewrite/tree/1b114ff485a2a59051bf7a2e39acec5774fd35a1). Local HEAD and published `main` match that checkpoint; the working tree is clean. The raw-table hash matches the reported value. No repository modification, training, probe, or new model-output inspection occurred during this review.

The evidence identifies a corruption-treatment problem. It does not demonstrate a fatal contradiction in B100, C101, or the fixed core protocol.

## B. Scientific diagnosis

**REPOSITORY EVIDENCE**

The **92.0492%** figure describes retained elementary-edit **sampling weight**: 1,945 of 2,113 occurrences are tagged punctuation, case, or whitespace/boundary. It does **not** establish that 92.0492% of generated examples—or 36.8197% of total canonical exposure—would be surface-only. Applicability, rejection, composition, inversion, and example lengths could change the realized distribution. That distribution remains unmeasured.

Nevertheless, the concern is substantial:

- Punctuation and case alone supply **89.7776%** of retained weight.
- Double-quote deletion alone supplies **20.4922%**.
- **690/1,024** natural pairs have identical lexical sequences.
- The independent review attributes **56.8386%** of retained raw edit weight to records with no lexical discrepancy.

These findings show that the raw estimator captures considerable reference/recognizer surface-policy disagreement. They do not show an estimator defect, identify every edit’s semantic importance, or prove that the remaining “other-character” weight represents meaningful recognition errors. [Measured profile](https://github.com/scalinity/repair-without-rewrite/blob/1b114ff485a2a59051bf7a2e39acec5774fd35a1/docs/reports/EMPIRICAL_CORRUPTION_PROFILE_QUALIFICATION.md), [independent review](https://github.com/scalinity/repair-without-rewrite/blob/1b114ff485a2a59051bf7a2e39acec5774fd35a1/docs/reviews/EMPIRICAL_CORRUPTION_PROFILE_INDEPENDENT_REVIEW.md).

**LITERATURE**

LibriSpeech-PC explicitly distinguishes word error without punctuation/capitalization from capitalization-inclusive, punctuation-inclusive, and punctuation-specific measures. This supports separating those quantities while recognizing that surface restoration remains useful. It does not prescribe this study’s training allocation. [Meister et al., *LibriSpeech-PC*](https://arxiv.org/pdf/2310.02943).

Alignment-derived ASR simulation also has precedent, but transfer depends on the source corpus and vocabulary. That supports retaining empirical lineage while qualifying transfer into this deliberately different technical domain. [Wang, Lu, and Chen, *Data Augmentation for Training Dialog Models Robust to Speech Recognition Errors*](https://aclanthology.org/2020.nlp4convai-1.8.pdf).

**SCIENTIFIC JUDGMENT**

The intervention should emphasize discrepancies observable under the already-frozen lexical definition, without replacing exact model targets with normalized text.

| Candidate family | Decision and consequence |
|---|---|
| A — Keep raw profile | Reject. A surface-inclusive study could be defensible, but the present evidence does not establish sufficient lexical repair pressure after generated-domain qualification. Accepting it would require a different justification for the largest channel. |
| B — Lexical-first estimation | **Choose.** Remove scorer-invariant surface differences before estimating corruption; retain transferable, supported character operations. |
| C — Raw edits conditioned on lexical effect | Reject as the primary method. Selecting lexical-error records still retains unrelated surface edits within those records. Precise raw-span attribution would add complexity that projection avoids. |
| D — Two strata | Reject. The evidence supplies no defensible internal exposure ratio. Natural surface prevalence is not automatically the appropriate training allocation. |
| E — Empirical severity with rule realization | Reject as the primary method. It discards useful character-level evidence and moves the 40% channel closer to the existing rule curriculum. |

This is a controlled lexical-restoration intervention, not an attempt to reproduce Parakeet’s complete output distribution.

## C. Chosen empirical estimand

Introduce the DEVELOPMENT profile:

**`development_lexical_corruption_v2`**

Let \(L(x)\) be the ordered token-value sequence returned by the unchanged `lexical_eval_v1`, including its pinned Unicode 15.1 normalization, case folding, mappings, and scanner.

Define:

\[
\Phi(x)=\operatorname{join}_{\text{ASCII space}} L(x).
\]

An empty token sequence maps to the empty string. Token values contain no separator spaces, so this serialization preserves token-sequence identity.

For every frozen TRAIN reference/hypothesis pair \((A_i,H_i)\), estimate edits from:

\[
\Phi(A_i)\longrightarrow\Phi(H_i).
\]

Use all **1,024 TRAIN records exactly once**. The 690 lexically equal records contribute zero projected edits; they remain in prevalence and coverage accounting.

The estimand consists of:

1. Supported, unanimous elementary codepoint-edit frequencies in these projected strings.
2. Conditional projected-codepoint severity among lexically discrepant records.
3. Broad operation-class co-occurrence, defined in Section E.

This is a **character corruption profile over lexical projections**. It is neither a whole-word confusion model nor a phonetic simulator.

Projection is used for estimation and qualification only. **Model sources, clean spoken anchors, written targets, objectives, and canonical accounting remain unnormalized.**

## D. Surface-policy treatment

Apply the following policy to the **empirical perturbation component**, not to all training behavior:

| Effect | Operational treatment |
|---|---|
| Case differences collapsed by `lexical_eval_v1` | No empirical sampling weight. They remain visible in raw diagnostics and exact targets. |
| Punctuation differences leaving \(L(x)\) unchanged | No empirical sampling weight. |
| Punctuation affecting the lexical sequence | Eligible through the projected edit estimator, support rules, and generated qualification. No global punctuation ban. |
| Whitespace amount/style leaving token boundaries unchanged | No empirical sampling weight. |
| Boundary changes altering the lexical sequence | Eligible as projected separator changes, subject to the same support and inversion requirements. |

For example, scorer-recognized differences between `can't` and `cant`, or between `a b` and `ab`, are not discarded merely because punctuation or spacing is involved.

Conversely, scorer invariance is **not** a declaration of semantic harmlessness. Case distinctions can matter outside this lexical estimand.

Legitimate surface behavior remains in:

- All unchanged raw public-real pairs in the 10% channel.
- Exact identity targets.
- Existing minimal and verified-rule examples.
- Exact spoken-to-written transduction and full written targets in the 40% channel.
- Raw-byte, raw-CER, and surface diagnostics.

There is **no additional surface-only sampling quota** inside the revised 40%.

Preserve the old table unchanged, under its existing hash:

`5df3800d7a29e370abdce36bd489989482d5d878765612b5a14a4b2cab1fc310`

Continue describing it as **“raw TRAIN reference-to-recognizer surface differences under the repaired Parakeet development runtime.”**

## E. Lexical/content treatment

**Elementary estimation**

- Unit: one Unicode codepoint in \(\Phi(x)\), including its explicit ASCII token separators.
- Alignment: unit-cost Levenshtein.
- Direction: projected reference → projected hypothesis.
- Ambiguity: retain an edit only if operation, both projected coordinates, and literal payload agree across **every** optimal alignment.
- Entry key: `(operation, reference_payload, hypothesis_payload)`.
- Operations: substitution, deletion, insertion.
- Support: **at least five distinct TRAIN records AND three source groups**.
- Weight: retained consensus occurrence count.
- Unsupported entries: zero sampling weight.

No arbitrary traceback, word-confusion label, external confusion list, or lowered support threshold is permitted.

Report ambiguity omission and support rejection separately, using the **new projected-distance denominator**. The old raw rejection percentages do not transfer to this profile.

**Two-operation dependence**

Use a deliberately coarser abstraction than the old literal-pair table:

- Estimate the six unordered S/D/I class pairs: SS, SD, SI, DD, DI, II.
- A record supports a class pair only when it contains two retained observations belonging to individually supported entries at distinct, nonoverlapping original positions.
- Two insertions at the same original gap do not qualify.
- A class pair requires **five distinct records AND three groups**.
- Its weight is the number of supporting records, counted once per record.

Within an admitted class pair, literal entries are sampled from their supported marginal occurrence weights.

This explicitly assumes conditional independence of literal payloads for generated composition. It does **not** claim that every resulting literal pair was jointly observed. The small corpus supports this broader composition abstraction more credibly than a large literal-pair model.

The previous **67 entries and 85 joint entries are not qualifications of the revised profile**.

## F. Zero-mass policy

For the revised 40% channel:

\[
\boxed{P(K=0)=0}
\]

Neither raw-zero prevalence nor lexical-zero prevalence is copied into its exposure weights.

The intervention is conditional on a lexical discrepancy. Every accepted empirical variant must change the lexical sequence of its clean spoken anchor and must remain lexically different from its written target.

Continue reporting separately:

- Raw zero: \(182/1024\).
- Lexical zero: \(690/1024\).
- Realized source-equals-target exposure.
- Realized lexical source-equals-target exposure.

This intentionally concentrates the corruption channel on repair. Preservation remains explicitly allocated through the unchanged 15% identity component, rule-clean views, and unchanged natural pairs. No natural record is removed because it has zero lexical error.

Zero-operation spoken renderings remain part of the **inverse ambiguity check**, even though they receive no empirical-channel sampling weight.

## G. Severity policy

Use distance in the **same representation and units as the revised elementary operations**:

\[
z_i=d_{\mathrm{cp}}\!\left(\Phi(A_i),\Phi(H_i)\right).
\]

Let \(I_+=\{i:z_i>0\}\). Correct reproduction should yield \(|I_+|=334\).

Define:

| Phase | Empirical operation count |
|---|---|
| P0 | \(K=1\) with probability 1 |
| P1/P2 | \(P(K=1)=\#\{i:z_i=1\}/334\) |
| P1/P2 | \(P(K=2)=\#\{i:z_i\ge2\}/334\) |

These are canonical-exposure subweights. They are estimated **before** support rejection; unsupported examples do not silently redefine severity.

The new numeric weights remain **unmeasured**. Sol must calculate and independently reproduce them.

Do not substitute the 521 word-edit units, raw codepoint distance, or retained-edit count for \(z_i\). Those answer different questions.

Report the full uncapped \(z_i\) distribution. The generated intervention remains capped at two operations and conditional on error; it does not reproduce natural error prevalence, utterance-length dependence, WER, or the severity tail.

Also report separately:

- Applied operation count.
- Actual lexical distance \(L(S)\) to \(L(R)\).
- Actual lexical distance \(L(S)\) to \(L(Y)\).
- Raw distance and native model lengths.

The fixed spoken-to-written transformation can require substantially more work than the one or two added empirical operations.

## H. Generated realization

Retain the existing eight categories, TRAIN value domain, deduplication, template cells, and `technical_spoken_renderer_v1`.

Keep P0/P1 cells 0–2 and P2’s 50% replay / 50% previously withheld cell-3 allocation within each category.

**Where edits apply**

Apply supported literal codepoint operations only inside rendered field values. Preserve scaffold bytes.

For this renderer’s current field vocabulary, verify:

\[
\Phi(r_{\text{field}})=r_{\text{field}}.
\]

This supplies a direct literal realization of projected character edits. If that equality fails, stop qualification for the affected construction; do not silently normalize or change the renderer.

**Proposal law**

- **K=1:** choose uniformly among fields with applicable supported entries; choose an entry by its retained occurrence weight conditional on applicability; choose uniformly among its matching positions or insertion gaps.
- **K=2:** apply one operation to each of the two distinct fields. Choose an admitted class pair by its record-support weight conditional on a feasible field assignment. Choose uniformly among feasible assignments, then sample each field’s literal entry and position as above.

Each changed field must individually change under \(L\). The complete candidate must satisfy:

\[
L(S)\ne L(R),\qquad L(S)\ne L(Y).
\]

These checks prevent surface-only proposals, cancellation into a lexical no-op, and accidental arrival at the target.

Use the existing corruption seed and deterministic, version-separated sampling convention. After **50 proposals per base/severity**, mark the variant unavailable. Do not substitute a rule variant, identity example, unsupported noise, or another category.

Keep at most one accepted variant per positive severity per base, reused across phases.

**Recoverability**

Qualify the complete source against the union of:

- Existing permitted clean/minimal/rule relations.
- The unchanged spoken renderer.
- Revised one- and two-operation empirical relations across all phases.
- Zero-operation spoken preimages.

The old raw empirical table becomes diagnostic, not an additional active corruption relation.

The inverse receives the source and public grammar/profile only. It must not receive the selected family, channel, phase, clean anchor, target, operation trace, or a lookup table restricted to generated TRAIN targets.

Enumerate all compatible targets permitted by that public relation. Require one unique complete written target, then compare it with the intended target. Preserve the **500-state bound**; capped or incomplete search fails qualification.

A remembered target, a small edit distance, or an individually recoverable operation is insufficient.

Apply common capacity rules and preserve exact \(S,R,Y\) lineage. Never filter examples separately for B and C.

## I. Distinction from the 20% rule channel

The channels retain different roles:

| 20% verified rules | Revised 40% empirical corruption |
|---|---|
| Starts from exact written forms under prescribed rule views. | Starts from deterministic clean spoken renderings. |
| Teaches selected technical transformations and their controlled compositions. | Adds TRAIN-supported stochastic character corruption before spoken-to-written restoration. |
| Uses the existing fixed rule-view proportions. | Uses conditional empirical severity, character weights, and broad co-occurrence weights. |
| Rule identity determines perturbation. | Supported empirical entries and generated applicability determine perturbation. |

Exact collisions can still occur, particularly in the restricted negation domain. Deduplicate physical variants and report shared lineage and cross-channel exposure. Do not claim independent support for duplicated examples.

No rule-generated fallback is allowed to fill missing empirical strata.

## J. Support adequacy

**The measured corpus is sufficient to attempt this bounded DEVELOPMENT estimator, but it does not yet establish a qualified generated treatment.**

The **334 lexical-error records and 521 word-edit units** do not justify:

- A broad word-confusion lexicon.
- Context-dependent confusion probabilities.
- A reliable long-tail error model.
- Detailed literal-pair dependence.
- Claims about recognizers or domains beyond these frozen pairs.

They can support modest descriptive severity estimates, broad operation-class co-occurrence, and a limited set of character entries that independently meet the existing support floor.

The **48 groups describe the complete 1,024-record pool**. Sol must report how many groups actually contain lexical errors and support each surviving estimate; do not assume all 48 contribute equally.

Report group concentration and leave-one-group-out changes in severity and retained mass. These are sensitivity diagnostics, not additional tuning data.

If the resulting supported table cannot populate the required generated strata, the treatment remains blocked. Do not lower thresholds, invent substitutions, or claim that corpus size alone proves adequacy.

Nothing here establishes statistical power or training diversity for the final 150M campaign.

## K. What remains unchanged

| Element | Binding |
|---|---|
| Top-level allocation | **30/20/10/40** |
| Identity/minimal | **15% identity + 15% minimal** |
| Other channels | Existing 20% rule and 10% public-real policies |
| Models | B100 and C101 architectures and parameterizations |
| C representation | Pointer/events and deterministic edit-renderer semantics |
| Inference | Source-only boundary |
| Tokenizer | Existing DEVELOPMENT tokenizer and reserved IDs |
| Objectives | B loss; C’s four components and weights; whole-update normalization |
| Optimization | AdamW, clipping, precision, accumulation policies |
| Accounting | `paper_canonical_v2`: \(|BPE(R)|+|BPE(Y)|+5\); corrupted source excluded |
| Scheduler | Existing deterministic hierarchical canonical-exposure deficit scheduler and deviation bounds |
| Update target | **32,768 anchors**, completing the last whole presentation |
| Pilot phases | **6,666,667 / 2,666,667 / 666,666** nominal exposures |
| LR slots | B and C × **1e-4, 3e-4, 6e-4**, all seed **42** |
| LR schedule | 200k warmup; continuous cosine decay to 10% of peak at 10M |
| Selection | Existing endpoint eligibility and LR-selection rules |
| Final seeds | **1729, 2718, 31415** |
| Attribution | H1 remains **representation-plus-renderer** |

Checkpoint policy also remains unchanged: scheduled complete-update saves, qualified interruption saves at completed microbatch boundaries, exact pending-state preservation, atomic publication/readback, and cold-resume comparison through the next 20 complete updates.

Only the corruption profile, its zero/severity policy, and its specified realization/qualification rules change.

## L. New qualification gates

Sol must produce the following evidence before reader admission:

1. **Input and projection binding.** Rejoin every frozen TRAIN ID and group; verify reference/hypothesis hashes and normalization identities. Reproduce 690 lexical-zero and 334 lexical-positive records. Exclude CALIBRATION, HPO, final data, and model outputs.

2. **Independent estimation.** Independently reproduce projected distances, unanimous observations, ambiguity omissions, support counts, weights, class-pair support, and severity. Compare complete serialized outputs, including rejected entries.

3. **Preserved provenance.** Verify the old raw-table hash remains unchanged. Assign new hashes to the revised table and, separately, the eventual complete construction/reader bundle.

4. **Generated qualification.** Report every category/cell/positive-severity pool, accepted and rejected counts, reasons, attempts, unique targets/bundles, duplicates, and inverse search coverage. Every required stratum must be nonempty.

5. **Lexical-effect checks.** Every accepted variant must pass the field-level and complete-source lexical-change requirements. Report the remaining spoken-to-written transformation separately from added empirical damage.

6. **Transfer and concentration audit.** Report supported-table weights, applicable proposal weights, accepted-variant frequencies, and realized canonical-exposure distributions separately. Include character entries, S/D/I, boundary edits, source groups, severity, and cross-channel collisions.

7. **Fresh fairness and operational qualification.** Complete the common presentation ledger, accounting/scheduler checks, actual paired consumption audit, capacity checks, update qualification, boundary/mid-update resume, sustained BENCH, and cost projection.

**Prospective stop rules**

Stop with scientific review required if:

- No supported revised profile survives.
- A required positive-weight stratum is empty.
- Unique inversion cannot be proved within the bound.
- Hidden metadata or an invented fallback is needed.
- Accepted “corruption” is lexically neutral.
- B/C require different accepted examples.
- The revised treatment becomes dominated by one elementary entry or by boundary-only edits.

For the last condition, bind a reproducible **strict-majority alarm: greater than 50%**, checked both in retained table occurrence weight and realized corruption-channel edit weight. For realized weight, weight each applied edit by its presentation’s canonical charge. Boundary-only means insertion/deletion of the projected ASCII separator without another character payload.

This majority threshold is a **review trigger**, not a statistical validity test or a quota to achieve by reweighting. It asks for explicit scientific reconsideration when most corruption again collapses into one narrow mechanism.

No failed gate permits automatic redistribution, threshold relaxation, another noise generator, or model redesign.

## M. Prospective amendment text

:::writing{variant="document" id="68412"}
### DEVELOPMENT corruption-profile revision v2

At reviewed checkpoint `1b114ff485a2a59051bf7a2e39acec5774fd35a1`, before any result from the six seed-42 10M probes, the frontier scientific review authorizes `development_lexical_corruption_v2`.

The raw estimator was correctly implemented. Its table, SHA-256 `5df3800d7a29e370abdce36bd489989482d5d878765612b5a14a4b2cab1fc310`, remains unchanged as a diagnostic of raw TRAIN reference-to-recognizer surface differences under the repaired Parakeet development runtime.

The revised profile estimates unit-cost codepoint edits after serializing the unchanged `lexical_eval_v1` token sequence with single ASCII spaces. All 1,024 frozen TRAIN pairs contribute once. Retain only edits unanimous across every optimal alignment, with at least five distinct records and three source groups; weight supported entries by consensus occurrences. Two-operation dependence is estimated at the six unordered S/D/I class pairs, with the same support floor and supporting-record weights.

The 40% channel is conditional on lexical error: no zero-operation sampling. P0 applies one operation. P1/P2 use the empirical distribution of projected codepoint distance capped at two, conditional on positive distance. Two-operation variants affect distinct fields. Exact unnormalized sources, spoken anchors, written targets, and objectives remain unchanged.

Generated candidates require lexical effect and unique complete source-only inversion under the full permitted relation. The existing 50-proposal and 500-state bounds remain. Empty required strata or the concentration alarms in Frontier Corruption-Profile Decision v2 block admission.

The 30/20/10/40 allocation, other channels, models, representation/renderer, tokenizer, optimization, accounting, scheduler, update target, probe schedule, LR grid, checkpoints, final seeds, and H1 attribution remain fixed.

New profile and construction hashes await measurement and independent reproduction. No final result has been seen or used; no probe slot has been consumed. Reader admission and owner authorization remain pending. `paper_protocol_v2` is not frozen.
:::

## N. Sol implementation handoff

Implement the following sequence:

1. Preserve this decision and append the prospective amendment without rewriting the supplied canonical specification or old evidence.
2. Implement and re-estimate `development_lexical_corruption_v2` exactly as defined above.
3. Obtain independent reproduction of the complete estimator output and new hashes.
4. Implement the unchanged spoken renderer and revised empirical realization; finish generated-pool and source-only union-inverse qualification.
5. Finish the common reader, full dry-run ledger, support/reuse reporting, scheduler, and canonical accounting.
6. Finish actual B/C fairness, complete-update qualification, boundary and mid-update resume, sustained BENCH, and cost projection.
7. Issue **`BC_10M_PROBE_ADMISSION_DECISION_V4`**, identifying every gate as passed, failed, or unverified, with exact artifact hashes.
8. Stop for owner authorization. Technical qualification does not itself authorize consuming a probe slot.

If a scientific stop rule fires, preserve the failed evidence and return it for review. Do not repair the result through undeclared changes.

DO NOT RUN THE SIX 10M PROBES YET.
