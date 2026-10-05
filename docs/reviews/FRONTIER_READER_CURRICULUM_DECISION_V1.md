# Prospective DEVELOPMENT authorization record

- Decision date: 2026-10-05
- Reviewed base: `928fd0305206ad6d6130d0667d1b206baa521a64`
- Status: **DEVELOPMENT DESIGN AUTHORIZED**
- Six 10M probes: **NOT STARTED**
- Affected final results seen: **false**
- Final training started: **false**
- `paper_protocol_v2` frozen: **false**
- Final/sealed candidate inference: **none**

The substantive frontier decision below is preserved verbatim from the immediately preceding Astra review. Implementation and admission remain contingent on its qualification gates.

---

# Frontier Reader/Curriculum Decision v1

## A. Decision summary

**READER_DESIGN_AUTHORIZED**

**Date:** 2026-10-05  
**Scope:** DEVELOPMENT mixed reader, complete-update qualification, and the prospective six seed-42 10M probes.  
**Reviewed candidate:** [`928fd0305206ad6d6130d0667d1b206baa521a64`](https://github.com/scalinity/repair-without-rewrite/commit/928fd0305206ad6d6130d0667d1b206baa521a64).

The missing treatment can be bound without changing B100, C101, their objectives, or H1. The evidence establishes underspecification, not an architecture failure.

**This authorizes a design for implementation and qualification. It does not admit the six probes.** In particular, the empirical corruption table and its retained, uniquely recoverable population must still be constructed and measured. Their existence or adequacy is not asserted here.

The published candidate supports the following state:

| Item | Verified disposition |
|---|---|
| Integrated tests | The committed receipt records **259 passing tests**. The two commits after the tested starting revision change reports/reviews/manifests, not model or test implementation. I did not rerun the suite. |
| Six 10M probes, final seeds, final/sealed inference | Recorded as **unstarted/not performed**. |
| `paper_protocol_v2` | **Not frozen**. |
| Parakeet | Qualified only under the documented repaired, narrowed runtime. |
| DEVELOPMENT tokenizer | **16,384 entries**, hash `b125551f…ace6ca`; unchanged. |
| MODEL-0 V6 | **10,002,432 real-shard inputs and labels; PASS**, distinct from restoration convergence. |
| LS-PC supply | Known LS-PC leakage closure completed; **1,024 natural TRAIN pairs / 48 groups** admitted. |
| ByT5 | **REPAIR_REQUIRED**, without independently vetoing these bounded B/C probes. |
| SLUE | Still gated; a later paper dependency, not an automatic LS-PC pilot veto. |

Evidence: [validation receipt](https://github.com/scalinity/repair-without-rewrite/blob/928fd0305206ad6d6130d0667d1b206baa521a64/experiments/manifests/paired_reader_bench/final-validation.attempt01.json), [V2 admission decision](https://github.com/scalinity/repair-without-rewrite/blob/928fd0305206ad6d6130d0667d1b206baa521a64/docs/reports/BC_10M_PROBE_ADMISSION_DECISION_V2.md), [foundation verification](https://github.com/scalinity/repair-without-rewrite/blob/928fd0305206ad6d6130d0667d1b206baa521a64/docs/reports/PAIRED_MIXED_READER_QUALIFICATION.md).

The scientific tradeoff is explicit: **the generated channels use a restricted, source-recoverable construction language.** The 40% channel transfers TRAIN-observed corruption statistics into that language; it does not claim to reproduce unrestricted natural ASR errors. Arbitrary corruption of ordinary prose would not satisfy the canonical requirement merely because its original reference was retained.

The canonical constraints come from the [v1.2 specification](https://github.com/scalinity/repair-without-rewrite/blob/928fd0305206ad6d6130d0667d1b206baa521a64/docs/design-inputs/EXTRACTED_CANONICAL_SOURCE.md) and [registry](https://github.com/scalinity/repair-without-rewrite/blob/928fd0305206ad6d6130d0667d1b206baa521a64/docs/design-inputs/LocalFlow_Publication_Experiment_Registry_v2.txt). The numerical policies below are **prospective scientific judgments**, not measurements or previously approved defaults. Literature supports estimating artificial-error distributions from observed errors, while also showing that synthetic-data choices can change the precision/recall tradeoff; it does not determine our ratios or thresholds. [Felice and Yuan, 2014](https://aclanthology.org/E14-3013/).

## B. Exact channel contract

All percentages below are **canonical-exposure shares**. Channel membership remains metadata and is not supplied to either model.

### Common generated base manifest

Promote the eight existing TRAIN constructor categories, not the existing fixture files as an unquestioned training dataset:

`signs_numerical`, `negation`, `versions`, `paths`, `identifiers`, `units_quantities`, `repeated_literals`, `multiple_bindings`.

Use the existing TRAIN scaffolds, typed-value forms, `trainstem` content domain, and public relations. Materialize the finite distinct targets obtained by enumerating the existing TRAIN constructor’s number parameter over **100–399**, retaining its existing value formulas. Deduplicate identical targets within each template family. Consequently, a constant negation target is one target, not hundreds of independent latents.

No additional category, external lexicon, arbitrary name replacement, or new semantic relation is promoted. In particular, a parser accepting a surface does not itself authorize adding that surface to the training generator. The current implementation and its limits are documented in the [reader review](https://github.com/scalinity/repair-without-rewrite/blob/928fd0305206ad6d6130d0667d1b206baa521a64/docs/reviews/PAIRED_READER_CONTRACT_INDEPENDENT_REVIEW.md) and [generator](https://github.com/scalinity/repair-without-rewrite/blob/928fd0305206ad6d6130d0667d1b206baa521a64/src/generation/stress.py).

For this pilot:

- **P0/P1:** use TRAIN template cells 0, 1 and 2.
- **P2:** generated-channel exposure is **50% replay from those cells, 50% from previously withheld TRAIN cell 3**, within each category.
- Categories have equal exposure weight; eligible cells within each replay/fresh component have equal exposure weight.
- Distinct targets within a cell use complete shuffled passes.
- Cell 3 supplies fresh template contexts, not a claim of fresh semantic mechanisms or entirely novel payload bundles. Report those dependencies.

This is the pilot’s prospective P2 proxy. It does not freeze the final campaign’s development-motivated P2 pool.

### Channel table

| Channel | Base pools and subweights | Construction and eligibility | Sampling and reuse | Phase treatment |
|---|---|---|---|---|
| **30% identity/minimal** | **50% identity / 50% minimal** within channel: 15% total exposure each. Identity uses eligible admitted LS-PC TRAIN `text_raw`; minimal uses the generated manifest above. | Identity has byte-identical source and target. Minimal has exactly one certified elementary perturbation and a unique complete target. | Identity: coverage-first record-balanced passes. Minimal: equal category/cell exposure, then distinct-target passes. | Ratio and elementary operations remain constant. Only the declared P2 fresh/replay allocation changes. |
| **20% verified rules** | Eight categories, **1/8 each** within channel: **2.5% total exposure per category**. | Only the rule views defined below; full source-only inverse agreement required. | Equal cell exposure within category; complete distinct-target passes within a cell/view. | P0 clean/mixed/two-repair = **20/80/0**. P1 and P2 = **20/40/40**. |
| **10% public real** | Exactly the existing **1,024 TRAIN pairs / 48 groups**. | Frozen repaired Parakeet hypotheses; unchanged official `text_raw` targets. Preserve natural identity/no-error cases. | Coverage-first record-balanced passes over all 1,024 records; no replacement within a pass. | Same pool and weighting throughout; pass cursor carries across phases. |
| **40% matched corruption** | Generated manifest above, with its deterministic clean spoken renderings. Eight equal category weights. | Apply only the empirically admitted operations below. Retain zero-operation outcomes and require a unique complete source-visible inverse. | Equal category/cell exposure; separate complete passes through eligible bases for each prescribed severity. Maximum three empirical variants per base. | P0 allows 0/1 empirical operations; P1/P2 allow 0/1/2. Same frozen table throughout; P2 adds the declared fresh/replay split. |

### Identity and minimal-change policy

**Identity means** `source_utf8 == target_utf8`, including whitespace, punctuation, casing and technical bytes. No normalization is allowed. In the identity subchannel, both accounting anchor and target are the unchanged official reference.

**Minimal means exactly one elementary forward perturbation**, selected deterministically from the eligible operations and positions:

| Field type | Permitted elementary perturbation |
|---|---|
| Signed numerical value, version, integer | Replace one `1` with `l`, or one `0` with `O`. Preserve signs and all other characters. |
| Path | Verbalize one `/` as ` slash ` or one `.` as ` dot `. |
| Identifier | Verbalize one `_` as ` underscore `. |
| Quantity | One eligible digit confusion, or one existing finite unit-alias expansion. Current generated quantities retain the existing constructor’s units. |
| Negation | One existing polarity-preserving spelling perturbation: `not→n ot`, `never→ne ver`, or `no→n o`, where the constructor actually supplies that value. |
| Repeated literals / multiple bindings | Apply the corresponding elementary operation to one occurrence/field only. |

Therefore:

- One correction only; **no multiple independent corrections** in this subchannel.
- Technical literals and bounded formatting/spelling expansions are allowed.
- Arbitrary lexical substitutions are forbidden.
- No deletion of semantic content, signs, digits, names or polarity.
- Additional spaces/verbalized separators are allowed only through the listed invertible transformations.
- The qualifier must recover the entire target from the source and public relation. Hidden operation traces cannot select the inverse.

The selected field and operation position are hash-derived; they are not always the first field.

### Verified-rule views

For each generated base, retain at most:

1. **Clean:** source equals written target.
2. **Mixed:** the same one-operation variant used by the minimal channel; the other field remains correct.
3. **Two-repair:** add one elementary operation in the other field and requalify the complete source.

Two-repair means two operations on distinct fields. Higher-order composition is excluded from this pilot. There is no assumption that individually valid operations remain jointly recoverable.

All eight categories enter. Equal category exposure is a controlled training choice, **not natural prevalence weighting**. The small negation support and shared constructor dependencies must remain visible in reporting.

Ambiguous, capped, noninvertible or whole-target-disagreeing candidates are excluded from generated repair supervision. They may be retained as construction diagnostics, with zero training exposure.

The 15% minimal allocation and rule repair views guarantee substantive repair supervision without using an overwhelming identity allocation. C’s cheap END decision and B’s full-target generation remain constitutive differences of the registered comparison; the curriculum does not equalize their decoder work.

### Public-real sampling

Choose **coverage-first, record-balanced passes**, not uniform-group exposure.

For each pass:

1. Hash-permute records independently within each group.
2. Hash-permute the 48 groups.
3. Present one record from every group in that order.
4. Hash-permute and present all remaining records across groups.
5. Begin a newly keyed pass only after every record has appeared once.

Consequences:

- Every group receives support before a second draw from any group **within that pass**.
- Every record appears before any record is reused.
- Across any prefix, record-use counts differ by at most one.
- Group weights over completed passes are proportional to their admitted record counts.
- For group sizes \(N_g\), normalized progress \(n_g/N_g\) differs across groups by at most one pass.
- This intentionally preserves the largest group’s approximately 5.96% record weight, rather than changing it to approximately 2.08%.

A pass is an ordering and reporting unit, not an optimizer epoch or LR-reset event.

The 1,024 references may also appear in the identity pool. Their original IDs/groups remain linked across channels. Their ASR hypotheses are not recycled as clean bases. Natural records are **not** corruption bases under this decision.

### Matched-corruption policy

**D1–D2: base and clean spoken rendering.** Use only the generated TRAIN bases above.

Bind the DEVELOPMENT subset of `technical_spoken_renderer_v1` as follows:

- Preserve scaffold bytes.
- Read digits individually using `zero` through `nine`.
- Signed decimals use `plus`/`minus` and `point`.
- Version separators use `dot`; hyphens use `hyphen`; alphabetic suffix characters are separated literal letters.
- Path/identifier payloads are rendered character by character: literal lowercase letters, digit names, and `slash`, `dot`, `underscore`, `hyphen` as applicable.
- Quantities use digit names plus the finite unit names `milliseconds`, `seconds`, `kilograms`.
- Negation words remain unchanged.
- Join the units within a rendered field with single ASCII spaces. Existing scaffold boundaries remain unchanged.

This is an exact text rendering convention, not a claim of verified audio realization. It deliberately differs from simply corrupting the formatted target.

**D3–D5: estimation source and support.**

Use each of the **1,024 frozen TRAIN pairs once**. Exclude CALIBRATION, HPO, final data, previous student outputs and external confusion lists.

The repaired hypotheses are sufficient to attempt a **bounded DEVELOPMENT profile** under that runtime. They do not establish a general recognizer-error distribution.

Estimate literal corruption from official `text_raw` to frozen hypothesis using unit-cost **Unicode-codepoint Levenshtein alignment**, without normalization:

- Retain an elementary edit observation only when its operation, source/reference coordinates and payload agree across all optimal alignments.
- Preserve exact ambiguity coverage; do not choose an arbitrary optimal path.
- A literal confusion entry enters the table only with support from **at least five distinct TRAIN records and three source groups**.
- Count record/group support separately from total occurrences.
- Table sampling weights are retained occurrence counts. Repeated presentations during training never re-estimate these weights.

These are conservative DEVELOPMENT support thresholds, not claims of statistical consistency.

**D6: operation classes.**

The executable classes are only empirically supported:

- codepoint substitution;
- codepoint deletion;
- codepoint insertion.

Record case, punctuation, whitespace/boundary and other-character tags separately. Do not infer a homophone, function-word, number, proper-name or identifier operator merely from a plausible linguistic label. Such phenomena enter only through retained observed literal edits.

This is a **character-level empirical corruption model**, not a word-confusion model or phonetic simulator. Its limited scope must be named in Methods.

**D7–D9: severity and compositions.**

For each TRAIN record, let \(d_i\) be its exact raw codepoint edit distance.

- P0 severity probabilities are the empirical frequencies of \(\min(d_i,1)\).
- P1/P2 probabilities are the empirical frequencies of \(\min(d_i,2)\).
- These frequencies become canonical-exposure subweights within the corruption channel.
- Thus zero-operation mass is retained. The existing 182 byte-identical records imply a prospective zero-operation weight of **182/1,024**, subject to exact profile reproduction.
- Two-operation class combinations require joint observation in at least **five records / three groups**. Operations must affect distinct, nonoverlapping positions in the original clean rendering.
- No higher-order composition or severity inflation is allowed.

The full uncapped TRAIN distance distribution must also be reported. The pilot distribution is explicitly a capped curriculum, not a claim to reproduce its tail.

**D10–D12: qualification.**

For every candidate:

1. Preserve the clean rendering, target, intermediate strings and exact operations.
2. Check strict UTF-8, declared grammar and common native capacities.
3. Prove a unique complete target from the actual source.
4. Consider the **union of permitted generated relations**—rule views, spoken rendering and empirical operations—across phases. Do not give the qualifier hidden channel, phase, selected template, operation trace or target.
5. Compare the unique result with the intended target only after inversion.
6. Retain the existing **500-state inverse bound**. A capped search is not success.

Zero empirical operations means `source == clean_spoken_rendering`; it does **not** necessarily mean source equals written target.

**D13: backoff.**

Unsupported entries receive zero weight. Within the supported table, sample applicable entries by their retained weights. No invented confusion, generic random noise, teacher corruption, or identity replacement is permitted.

After 50 deterministic proposals for a base/severity variant, mark that variant unavailable. Construct the remaining eligible pool before scheduling. If any required category/cell/severity pool is empty, **reader admission is blocked**. Do not redistribute its weight.

**D14–D20: freeze and reuse.**

- One accepted variant each for severity 0, 1 and 2 per base; at most three empirical variants.
- One table, rendering policy and lexicon identity across all phases and all six arms.
- Rule-generated clean bases may be reused, with shared base/bundle lineage.
- Natural TRAIN records supply the empirical profile but are not synthetic corruption bases.
- TRAIN/DEV/final family and lexical barriers remain intact.
- Before the pilots, freeze source hashes, alignment policy, ambiguity coverage, supported/rejected entries, support counts, weights, severity frequencies, co-occurrence support, renderer identity, proposal/rejection ledger, accepted variants and all resulting pool hashes.

**The actual retained profile is still pending measurement.** Failure to construct it is a data/design qualification failure, not permission to relabel the rule fixtures as the 40% channel.

## C. Exact global scheduler

Use a **deterministic canonical-exposure deficit scheduler**, with complete presentations as indivisible units.

A fixed row cycle is rejected because lengths differ. IID channel sampling is rejected because it introduces avoidable mixture fluctuation and complicates exact matched replay.

Within phase \(p\), after \(n\) accepted presentations:

\[
T_p(n)=\sum_j C_{p,j}(n),\qquad
D_{p,j}(n)=w_jT_p(n)-C_{p,j}(n),
\]

where \(w=(0.30,0.20,0.10,0.40)\).

Select the channel with the largest deficit. Ties use this fixed order:

1. identity/minimal;
2. verified rules;
3. public real;
4. matched corruption.

Obtain its next eligible presentation, append it whole, then add its canonical charge. No truncated example, fractional charge or arm-specific replacement is allowed.

Use the same rule hierarchically for exposure-weighted subdivisions. Ties use the listed category order, ascending cell number, clean/single/two-operation order, and replay before fresh. Record selection within a leaf uses the declared shuffled passes.

**Phase handling:** reset exposure-deficit counters at a phase transition. Carry pool pass cursors and reuse counters forward whenever the pool remains the same. Do not restart the natural pool at phase boundaries.

**Deviation rule.** Let \(L_p\) be the maximum admitted example charge in a phase. For the four-channel scheduler:

\[
-(2+w_j)L_p
\le C_{p,j}-w_jT_p
\le (1-w_j)L_p.
\]

This follows from whole-example charging and largest-deficit selection. It is the acceptance tolerance; no arbitrary percentage tolerance is added.

For a window wholly inside a phase:

\[
\left|\Delta C_j-w_j\Delta T\right|\le 3L_p.
\]

Report phase totals, complete-update windows, and nonoverlapping 1M-exposure windows. For windows crossing phases, sum the corresponding segment bounds. Global deviations follow from summing phase deviations.

**Randomness and ordering:**

- Retain the existing generator seeds: manifest `120012`, partition `120101`, TRAIN values `120201`, corruption `120301`; DEV values/panel seeds remain separate.
- Use domain-separated SHA-256 with canonical JSON arrays, strict UTF-8 without normalization, big-endian integers and unbiased bounded sampling, following the existing generator convention.
- Include decision version, purpose, partition, pool/family/base/view, pass number, operation ordinal and proposal ordinal.
- Presentation-order namespaces include training seed 42.
- **Exclude arm, LR, model outputs, machine timing and worker order** from scientific presentation keys.
- Tie hash collisions by stable ID.

Prefer an immutable, hash-bound full presentation ledger through the final common update. Rejected generation attempts remain in a separate ledger and incur construction cost, but **zero canonical training charge**. At runtime, a missing or invalid accepted row stops the reader; it is not replaced.

Finite pools repeat only through their prescribed complete passes. Empty pools or unsatisfied required strata block admission.

## D. Exact canonical accounting serialization

Bind the DEVELOPMENT realization of `paper_canonical_v2` as:

\[
[\,\mathrm{BOS},\mathrm{restore\_reference},\mathrm{SEP},
\operatorname{BPE}(R),
\mathrm{SEP},
\operatorname{BPE}(Y),
\mathrm{EOS}\,].
\]

Here \(R\) is the clean accounting anchor and \(Y\) the full written target.

| Configured name | Existing ID | Occurrences |
|---|---:|---:|
| `BOS` | 257 | 1 |
| `restore_reference` / `RESTORE_REFERENCE` | 308 | 1 |
| `SEP` | 259 | 2 |
| `EOS` | 258 | 1 |
| `PAD` | 256 | Excluded |

No new reserved ID is allocated. There is no channel token. The first SEP introduces the anchor; the second introduces the target. Encode the two literal segments independently.

\[
\boxed{c_i=|\operatorname{BPE}(R_i)|+|\operatorname{BPE}(Y_i)|+5}
\]

Rules:

- The corrupted source \(S\) is **not charged**.
- No B decoder, C event, pointer, replacement or loss count enters this formula.
- All five framing tokens count, including both SEP occurrences.
- Padding never counts.
- Natural pairs use \(R=Y=\) official reference.
- Generated views use the deterministic spoken rendering \(R\), including clean generated views whose model source equals \(Y\).
- Accounting metadata never enters the encoder.

Separately bind common native source framing to the existing helper’s sequence:

\[
[257,308,259,\operatorname{BPE}(S),258].
\]

This has four native source controls. It is not the accounting serialization.

Common eligibility retains source and native decoder caps of 1,024 positions. Additionally, the generated clean rendering must fit that same source frame, so \(|BPE(R)|\le1020\); full target plus EOS must fit, so \(|BPE(Y)|\le1023\). Therefore \(L_p\le2048\). Do not truncate to satisfy these checks.

The IDs and tokenizer implementation are verified in the candidate’s [reserved map](https://github.com/scalinity/repair-without-rewrite/blob/928fd0305206ad6d6130d0667d1b206baa521a64/configs/tokenizer_development/special_tokens.json) and [tokenizer](https://github.com/scalinity/repair-without-rewrite/blob/928fd0305206ad6d6130d0667d1b206baa521a64/src/models/tokenizer.py).

### Five worked examples

These are accounting illustrations, not newly admitted dataset records. Token lengths below were calculated from the unchanged published tokenizer.

1. **Identity**

   \(S=R=Y=\texttt{"a"}\), with `BPE("a") = [97]`.

   Accounting sequence: `[257,308,259,97,259,97,258]`.  
   **Charge: \(1+1+5=7\).**

2. **One verified-rule repair**

   Written target:

   `Exercise repeated_literals: Primary integer: 1100; Backup integer: 1100.`

   Source changes the first field to `l100`. The spoken anchor is:

   `Exercise repeated_literals: Primary integer: one one zero zero; Backup integer: one one zero zero.`

   Anchor length 36; target length 32.  
   **Charge: \(36+32+5=73\).**

3. **Natural real pair**

   Illustrative source: `The cat sat.`  
   Official-reference anchor and target: `The cat sits.`

   The reference encodes to four tokens.  
   **Charge: \(4+4+5=13\)**, independently of source length.

4. **Matched corruption**

   Use example 2’s target and spoken anchor. Its admitted zero-operation empirical variant has \(S=R\).

   **Charge: \(36+32+5=73\).** Any separately qualified nonzero corruption of this same anchor retains charge 73.

5. **Legitimate empty reference**

   For an explicitly designated legitimate empty natural reference, \(R=Y=""\), even if \(S\) is nonempty:

   Accounting sequence: `[257,308,259,259,258]`.  
   **Charge: 5.**

   Missing/null/sentinel references remain invalid. Do not manufacture empty examples or an empty-example quota. Their lexical reference denominator is zero under F03; an all-zero evaluation denominator remains undefined.

## E. Exact pilot schedule

### Choice

**Choose Option 2: proportionally compressed three-phase curriculum.**

- A 10M P0 prefix would leave LR selection insensitive to later composition and fresh-template behavior.
- Equal thirds would greatly overweight P2 relative to the registered campaign.
- Proportional compression preserves the intended phase balance while exposing every recipe to all three treatments.

| Pilot phase | Nominal exposure | Absolute transition |
|---|---:|---:|
| P0 | 6,666,667 | 6,666,667 |
| P1 | 2,666,667 | 9,333,334 |
| P2 | 666,666 | 10,000,000 |

Assign each next presentation using its **starting cumulative exposure**. A presentation crossing a transition stays whole in its original phase; the next presentation enters the new phase. Keep absolute transition targets fixed.

An optimizer update may contain presentations from both sides of a phase transition. Do not flush a smaller update there.

All six arms stop at the same **first complete common optimizer update reaching 10M**. Report actual exposure and overshoot. Never truncate the last update.

### LR clock

For each unchanged peak \(L_{\max}\in\{10^{-4},3\cdot10^{-4},6\cdot10^{-4}\}\):

- Linear warmup: **200,000 canonical exposures**.
- Then cosine decay to **10% of peak at 10M**.
- No phase reset of LR or optimizer state.
- Evaluate LR at the completed update’s exposure endpoint \(e\), clamped at 10M:

\[
L(e)=
\begin{cases}
L_{\max}e/200000,& e\le200000,\\
L_{\max}\left[0.1+0.45\left(1+\cos\left(\pi
\frac{e-200000}{9800000}\right)\right)\right],& e>200000.
\end{cases}
\]

All recipes start afresh. No BENCH, fixture-fit or MODEL-0 weights are inherited.

### Saves and evaluation

- Save initial state.
- Save at the first common complete update reaching each **1M increment**, and each phase boundary.
- Decode/evaluate at **0, 1M, 3M, 6,666,667, 9,333,334 and 10M**, using the corresponding complete-update endpoint.
- Deduplicate coincident save/evaluation endpoints.
- All six recipes use identical actual presentation endpoints.

Freeze this DEVELOPMENT panel before the first probe:

- All **96 existing frozen CALIBRATION natural pairs**, plus the **12 existing repaired HPO hypotheses**.
- The existing **288-case generated DEV panel**, preserving all views and dependencies.

Using all 96 CALIBRATION pairs is an explicit prospective DEVELOPMENT consumption decision. Record it in the consumption overlay; those IDs cannot later be called untouched calibration. None enters fitting or profile estimation.

Retain the existing qualified greedy decode policy: 256 generated/event positions and C’s 64-edit cap, strict validity and existing failure scoring. Freeze complete panel admission/cap reporting before probes; do not remove cases after decoding.

Report natural and generated results separately. Natural reporting includes failure-inclusive WER, completed-repair bounds, introduced-error bounds, byte/lexical identity, source-correct preservation, failures and group support. Generated reporting includes clean preservation, required repair, mixed success and whole-case conformance. No pooling of their denominators.

### LR selection

Select **one LR independently for B and C**, using only each arm’s three **10M endpoint** results.

A recipe is eligible only if:

1. It completes the prescribed run without unresolved numerical, reader or checkpoint failure.
2. Natural failure-inclusive WER is strictly below RAW.
3. The lower bound on completed natural repair is positive, with completed repair supported in at least two source groups.
4. It completes at least one genuine required repair in the generated DEV panel.

These are DEVELOPMENT viability screens, not H1 significance or final-paper acceptance gates.

Among eligible recipes, rank lexicographically:

1. lowest natural WER;
2. lowest upper bound on natural introduced-error rate;
3. highest lower bound on completed natural repair;
4. fewest incomplete/invalid natural outputs;
5. highest generated mixed-view success;
6. lower peak LR.

Use exact counts/rational comparisons where possible. No “approximately tied” discretion, best intermediate checkpoint, cross-arm loss comparison, or additional LR trial is allowed.

### Outcome disposition

| Outcome | Required action |
|---|---|
| Both arms have an eligible recipe | Record selections; proceed to the remaining pre-freeze adequacy, comparator, scope and cost review. This does not authorize final training. |
| Reader, target, masking, accounting or resume defect | Repair implementation/data handling; preserve failed evidence and require an explicit symmetric rerun decision. Do not treat the defect as architecture evidence. |
| Only one arm has an eligible recipe, or apparent learning remains dominated by unsupported/ambiguous evidence | Request another frontier review before a 150M H1 campaign. Do not rescue the weaker arm through unregistered tuning. |
| Neither arm has an eligible recipe after all prescribed outcomes and failure replays | Abandon launching the **current** 150M campaign. This is a learnability/admission decision, not proof that longer training or either architecture can never work. |
| A fixed architecture/core contract is contradicted by measured evidence | Issue `ARCHITECTURE_OR_CORE_PROTOCOL_REVIEW_REQUIRED` with the required causal analysis. |

The existing one-replay numerical-failure rule remains: replay once from verified state with the same recipe; repeated failure marks that recipe failed.

## F. Exact update target

**Retain 32,768 canonical anchors per complete optimizer update.**

Construct a common ordered queue until its charge first reaches 32,768; finish the last whole presentation. B and C partition that exact queue into their own memory-safe microbatches.

With maximum example charge \(L\):

\[
32768\le Q_{\text{update}}<32768+L.
\]

Compute all whole-update denominators before backpropagation. Clip once, update once, and clear once.

**No smaller optimizer-update target is authorized.** Memory problems may be addressed through faithful microbatch partitioning and materialization. If the exact-model regime remains impractical, return measured evidence for review; changing AdamW cadence is not scientifically equivalent by assertion.

The candidate contains no measured failure of this target. [Complete-update BENCH report](https://github.com/scalinity/repair-without-rewrite/blob/928fd0305206ad6d6130d0667d1b206baa521a64/docs/reports/PAIRED_COMPLETE_UPDATE_BENCH.md).

## G. Exact checkpoint policy

**Mid-update publication is permitted and must be qualified.**

Routine scheduled saves occur at complete optimizer boundaries. A requested interruption save may publish at a completed microbatch boundary after all pending arrays are materialized. Publication during an unfinished forward/backward operation is forbidden.

A mid-update checkpoint must preserve:

- Common queued presentation range, ledger hash and exact queue reconstruction.
- Arm-specific microbatch partition and completed offset.
- FP32 accumulated gradients.
- B’s whole-update denominator or C’s four whole-update denominators.
- Pending canonical charge and completed-update canonical charge separately.
- Model/master weights, working-weight reconstruction policy, optimizer moments and step.
- LR schedule identity and exposure clock.
- All used RNG states.
- Reader phase, deficits, pass cursors, group/record/variant counters and next IDs.
- Model, tokenizer, source, renderer, profile, code/configuration and runtime identities.

Use atomic publication with hashes, shape/dtype/finite-state checks and a real B/C masked-forward readback check. A checksum alone is insufficient.

Cold restoration must finish the **same queued objective**, then match an uninterrupted control for the next 20 complete updates. Preserve the stored microbatch partition on resume. Pending work is committed once when that optimizer update completes; replayed physical work is separately logged.

This retains recoverability during potentially long updates without allowing partial charges or gradients to disappear. The extra complexity is justified only with the exact restoration test. [Independent resume review](https://github.com/scalinity/repair-without-rewrite/blob/928fd0305206ad6d6130d0667d1b206baa521a64/docs/reviews/PAIRED_RESUME_BENCH_INDEPENDENT_REVIEW.md).

## H. Repetition/support safeguards

1. **No artificial uniqueness.** Preserve stable records, source groups, template families, typed-bundle identities and duplicate hashes separately. Repeated numeric draws or renamed IDs do not create independent support.

2. **At most six distinct generated sources per base:** clean written view, one minimal/mixed view, one two-repair view, and empirical severities 0/1/2. Deduplicate coincident source bytes. Replaying a variant does not create another variant.

3. **Within each eligible record/base pool, use-count imbalance is at most one pass.** Exposure differences caused by different example lengths remain reported.

4. **Cross-channel reuse is explicit.** Minimal and rule-mixed may share the same source/target. Rule and empirical views may share a base. Every presentation is charged, but unique support is counted once at each applicable lineage level.

5. **Natural replay has a concrete bound.** Under the new serializer, one complete public-real pass charges:

   \[
   2(24,846)+5(1,024)=54,812.
   \]

   Nominal 1M real exposure therefore corresponds to approximately **18.244 passes**. With the declared scheduler, three phases, \(L\le2048\), common endpoint overshoot and an uninterrupted pass cursor, **no natural record may be presented more than 19 times in a 10M probe**. This is a derived limit, not a claim of 19 independent observations.

6. **No phase-specific natural restart.** Restarting its pass at P1 or P2 would invalidate that reuse policy.

7. **Required generated strata cannot disappear.** Every positive-weight category/cell/view/severity must have a nonempty qualified pool. No automatic renormalization.

8. **Construction rejection precedes accounting.** Preserve rejected candidates, reasons, attempts and cost. An unavailable positive-severity example cannot be replaced with a no-op.

9. **Freeze the complete dry-run support report before probes:** unique groups/targets/bundles, per-channel and joint reuse, support minima, duplicate rates, rejection coverage, realized severity, native lengths and canonical discrepancies.

10. **Do not infer final adequacy from pilot supply.** These safeguards admit a bounded, reproducible pilot population. They do not certify sufficient diversity for 150M or final H1 precision.

## I. What remains fixed

- **B100 architecture unchanged:** 100,686,336 parameters.
- **C101 architecture unchanged:** 101,081,859 parameters.
- C pointer/event representation and deterministic edit renderer unchanged.
- Source-only inference boundary unchanged.
- DEVELOPMENT tokenizer and ID map unchanged.
- B objective and C’s four component objectives/weights unchanged.
- Whole-update normalization, AdamW family/settings, precision policy and clipping unchanged.
- Matched B/C ordered presentations and canonical exposure unchanged.
- **Six LR slots unchanged:** three per arm, seed 42.
- Final seeds **1729, 2718, 31415** unchanged.
- H1 remains a **representation-plus-renderer** comparison, with its repair, damage and anti-identity interpretation.
- Focused H1 scope retained; A100 and H2 remain stretch.
- Final 100M/40M/10M budgets remain unchanged.
- **No final protocol freeze. No final-data use. No final/sealed inference.**

The new spoken-rendering binding concerns data construction. It does not alter C’s edit renderer.

## J. Required implementation tests

Before probe admission, Codex must pass:

| Area | Required evidence |
|---|---|
| Source admission | Exact role/hash joins; all 1,024 real TRAIN records retained; CAL/HPO/final excluded from fitting and corruption-profile estimation; unchanged leakage barriers. |
| Generated population | Correct eight-family manifest; deduplication; TRAIN/DEV/final separation; P2 withholding; all permitted views and variant caps. |
| Recoverability | Source-only qualification across the full permitted relation; hidden metadata unavailable; ambiguous/capped cases rejected; complete-target agreement. |
| Empirical profile | Independent reproduction of alignments, consensus edits, support thresholds, severity/co-occurrence counts, omitted ambiguity and table hashes. |
| Accounting | Five-token framing; strict segment encoding; source independence; PAD exclusion; empty-reference distinction; generated anchor/target differences; worked-example charges. |
| Scheduler | Exact deficits/ties; hierarchical shares; derived discrepancy bounds; phase crossings; whole-example overshoot; deterministic ordering; exhaustion and rejection behavior. |
| Repetition | Coverage-first passes; record/group imbalance rules; cross-channel lineage; no phase restart; natural 19-use maximum. |
| Fairness | Nonempty per-presentation ordered comparison of actual B/C consumption against the common ledger, including phase, channel, source/target/anchor hashes, charge and update range. |
| Native objectives | B pooled target/EOS normalization; C full-queue component denominators and zero-component omission; unequal microbatch partitions; no second division; correct masks and byte pointers. |
| Resume | Atomic boundary save/cold load and actual mid-update save/cold load; same pending queue/gradients/denominators; 20-update uninterrupted equivalence; corruption/nonfinite/inconsistent-state rejection. |
| Complete-update BENCH | Exact models, actual approved reader, 32,768 target, five complete warmups, 100 timed complete updates, separate ≥20-minute thermal segment and required resume checks. |
| Admission costs | Reader, update, checkpoint/load, all registered DEV panels and scoring costs; serialized neural jobs; six-recipe total with 25% reserve and no double counting. |

**Prospective BENCH binding:** use peak LR `3e-4` with the declared nonzero pilot clock, clamped at the endpoint floor if the measurement stream extends beyond 10M. BENCH weights are not probe initializations and BENCH outcomes cannot select an LR.

The timing stream must represent all three approved phase populations. Interleave complete phase-specific queues with an exposure-deficit phase sampler using the pilot’s phase proportions; retain each queue’s actual reader contents and report phase-stratified rates. This is a measurement stream, not an additional curriculum candidate. It must not qualify P1/P2 costs from P0-only timings.

Use the slower sustained measurement window for forecasts. Previous short-fixture or zero-LR rates cannot substitute.

## K. Required prospective amendment text

:::writing{variant="document" id="58143"}
### Frontier Reader/Curriculum Decision v1 — 2026-10-05

Status: DEVELOPMENT DESIGN AUTHORIZED; IMPLEMENTATION AND PROBE ADMISSION PENDING. This decision was made against published candidate `928fd0305206ad6d6130d0667d1b206baa521a64`, before any of the six seed-42 10M B100/C101 recipes. No affected final outcomes were seen. Final training and sealed candidate inference remain unstarted; PUB-GATE 3 and `paper_protocol_v2` freeze remain pending.

Adopt the complete Frontier Reader/Curriculum Decision v1 as the normative DEVELOPMENT reader contract. Preserve 30/20/10/40 by canonical exposure. Split the 30% channel equally between unchanged admitted LS-PC TRAIN identity examples and one-operation, uniquely recoverable generated minimal examples. Promote only the eight named existing TRAIN constructor categories, with equal category exposure. Rule clean/mixed/two-repair shares are 20/80/0 in P0 and 20/40/40 in P1/P2. Public-real training uses all 1,024 admitted TRAIN pairs through coverage-first record-balanced passes without phase restarts.

The 40% channel uses the decision’s deterministic typed spoken renderings and a TRAIN-only empirical Unicode-codepoint corruption table. Admit literal entries only with at least five supporting records and three groups; retain alignment ambiguity and zero-operation mass. P0 uses empirical edit counts capped at one; P1/P2 cap at two, with supported co-occurrence and full source-only inverse qualification. Unsupported or empty required strata block admission; no substitute noise or mixture redistribution is authorized. Freeze actual tables, rendering, populations and rejection/support ledgers before probes.

Use the deterministic canonical-exposure deficit scheduler and whole-example discrepancy bounds specified in the decision. Accounting is `[BOS=257, restore_reference=308, SEP=259, BPE(clean anchor), SEP=259, BPE(full target), EOS=258]`: charge equals anchor tokens plus target tokens plus five, excluding PAD and corrupted-source/native decoder work.

Compress the pilot into 6,666,667 / 2,666,667 / 666,666 nominal exposures. P2 generated content is half replay and half withheld TRAIN template-cell content. Use 200,000-exposure linear warmup and continuous cosine decay to 10% of peak at 10M. Retain the six LR slots and the decision’s common save/decode endpoints, frozen DEVELOPMENT panel, endpoint-only selection rule and failure dispositions. Record the prospective consumption of all 96 existing calibration pairs for DEVELOPMENT evaluation; none enters fitting.

Retain 32,768 canonical anchors per optimizer update and the common final complete-update overshoot. Permit mid-update checkpoints only with complete queued range, offsets, gradients, whole-update denominators, pending charge, model/optimizer, RNG and reader state; qualify actual cold restoration.

B100/C101 architectures, objectives, C event/renderer semantics, tokenizer, optimizer/clipping, final seeds and H1 attribution remain unchanged. This amendment authorizes faithful reader implementation, tests and complete-update BENCH qualification. It does not authorize the six probes, final training, final inference or protocol freeze. After successful qualification, issue a new admission decision and stop for owner authorization.
:::

## L. Codex handoff

Codex: implement the DEVELOPMENT reader, empirical-profile construction, accounting serializer, compressed pilot configuration, immutable presentation ledger and complete checkpoint state exactly as bound above. Perform the reader, fairness, accounting and resume tests, then qualify the **32,768-anchor complete-update BENCH** and price the six recipes.

If a required empirical stratum cannot be qualified, stop with the measured deficiency. Do not invent a replacement treatment or alter a fixed architecture/core contract.

**DO NOT RUN THE SIX 10M PROBES YET.**

After successful qualification, issue a new admission decision with the exact reader/configuration hashes, matched-consumption evidence, resume results and measured cost, then **stop for owner authorization**.

