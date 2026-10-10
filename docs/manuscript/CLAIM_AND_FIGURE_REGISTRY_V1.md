# Claim and figure registry v1

FACT — Prepared 2026-10-10 from documentation checkpoint `abfd0d595e80b1cca544bb9e91e238b094e2a604` and frozen G2 scientific checkpoint `609f97f31979d469ad8551d06b2c07c3513181ec`. This registry is manuscript preparation, not a scientific scope change, selected model list or publication-readiness verdict. Candidate claims below retain their original populations, denominators and evidence classifications.

The [development draft](DEVELOPMENT_EVIDENCE_DRAFT_V1.md) supplies the complete A–R narrative and E01–E14 [evidence map](DEVELOPMENT_EVIDENCE_DRAFT_V1.md#evidence-map-and-reading-conventions). The [evidence inventory](../../experiments/manifests/manuscript_development_evidence/evidence-inventory.attempt01.json) binds source bytes and histories. The G1 primary receipt is [descriptive-tables.attempt01.json](../../experiments/manifests/six_10m_probes/descriptive-tables.attempt01.json); G2 primary is [scientific-results.attempt01.json](../../experiments/manifests/generation_2/scientific-results.attempt01.json). The retrospective [feasibility report](../reports/POST_G2_READ_ONLY_TASK_FEASIBILITY_V1.md) supplies its complete aggregate tables and appendices; it is not itself a new independent-review receipt.

FACT — “Independent” below describes recorded historical reconstruction, not verification rerun in this writing session. “Supported” means the exact narrow claim is supported, not that an expanded causal/capability claim is. Alignment bounds (A), descriptive source-group sampling (G), unmeasured training-seed variability (S) and unmeasured domain/pretraining/generalization uncertainty (D) are separate. Fixed configuration/accounting claims have exact identity/count uncertainty rather than a sampling interval. No new protected-source processing is permitted to complete a figure.

## Candidate manuscript claims

### C01 — Original controlled question and its boundary

- Exact claim, FACT: The B100/C101 comparison concerns representation, supervision, decoding and constitutive copying together under matched presentations and canonical charge; it does not isolate output format alone or establish final H1.
- Supporting evidence/source: E01 §§2, 9–10, 23, 25; E02 draft registry; E12 v1 §§R–T and v2 §L.
- Numerical denominator: two architecture definitions, not an outcome ratio; final H1 population is unexecuted.
- Independently reconstructed: configuration/presentation identities historically verified in E04/E09/E10; hypothesis boundaries are accepted design statements.
- Uncertainty: A/G/S/D constrain possible results; no final-population estimate exists.
- Already supported: YES as the declared question and attribution limit.
- Additional evidence required: useful paired models, qualified final populations and prospective final design/authorization before a final H1 claim.

### C02 — Architecture and scientific input lineage

- Exact claim, FACT: B100 has 100,686,336 parameters; C101 has 101,081,859, with the shared width-768 eight-encoder/four-decoder backbone, random scratch initialization and unchanged qualified input/loss contracts.
- Supporting evidence/source: E01 §§9, 18; E03 campaign freeze `models`; E05 execution freeze `recipes[].config.model`; E04 provenance.
- Numerical denominator: full trainable parameter inventory per architecture; six G1 and six new G2 scratch recipes.
- Independently reconstructed: YES, historical parameter/state and execution-source identities; no arrays loaded here.
- Uncertainty: exact accounting, S/D for behavioral extrapolation.
- Already supported: YES.
- Additional evidence required: none for identities; size/architecture superiority would require a separately designed treatment.

### C03 — Within-condition exposure matching

- Exact claim, MEASURED RESULT: G1 and G2 D0 each use 134,591 presentations and 10,007,223 actual canonical exposures; G2 D1 uses 136,755 and 10,006,223. Within each D, B/C and U1/U8 match ordered presentations and exposure exactly; cross-D equality is not claimed.
- Supporting evidence/source: E03 freeze/descriptive receipts; E04 full-projection provenance; E05 `data_conditions`; E10 accounting `recipes[]` and within-D checks.
- Numerical denominator: one complete per-recipe ledger, 305 master queues; U8 2,440 versus U1 305 optimizer updates.
- Independently reconstructed: YES historically, through separate ledger/accounting paths.
- Uncertainty: exact identity/counts; native work is not equalized.
- Already supported: YES.
- Additional evidence required: complete equal-compute/equal-time comparisons would need a prospective design; do not infer them from this match.

### C04 — Dataset roles and inference boundary

- Exact claim, FACT: G2 uses 14,113 TRAIN records in 314 groups and 2,696 natural DEVELOPMENT cases in 52 groups (1,900 CAL/40, 796 HPO/12); references and latent labels are absent from correction inference.
- Supporting evidence/source: E05 corpus/execution freezes; E13 metadata census `counts`, `groups`; E09 observation/role checks; E01 §9.1; E08 source recipe.
- Numerical denominator: complete admitted census and all 2,696 natural cases, rather than publisher totals.
- Independently reconstructed: YES historically for role/population/input bindings; unknown upstream pretraining overlap is not verified absent.
- Uncertainty: exact role identities; D and reference-conditional truth limits.
- Already supported: YES for this project lineage.
- Additional evidence required: independent future data qualification and permitted overlap checks before a new policy evaluation.

### C05 — G1 failed natural adequacy

- Exact claim, MEASURED RESULT: G1 B100 natural error counts are 2,208/2,584/2,664 and C101 counts 121/128/109 at LRs 1e-4/3e-4/6e-4, respectively; all exceed RAW's 64 errors. Neither arm has an eligible endpoint or selected LR.
- Supporting evidence/source: E03 `outcomes[].learning_curve` at nominal 10M and endpoint-selection `arms`; E04 independent metrics and selection.
- Numerical denominator: 108 cases, 2,270 reference words, 64 source errors; six fixed endpoint recipes.
- Independently reconstructed: YES; all 36 evaluations rescored, separate distance checks, dense oracle only within its budget.
- Uncertainty: A for repair/introduction; S/D unmeasured; no final equal-domain H1 inference.
- Already supported: YES for those development screens.
- Additional evidence required: different regimes/architectures cannot be ruled out; any new treatment needs a prospective decision and authorization.

### C06 — G1 generated repair differs from natural repair

- Exact claim, MEASURED RESULT: C101 completes 49/79/54 genuine repair-bearing generated cases at the three LRs, but zero completed natural endpoint repairs at all three. B100 has zero genuine generated repairs at all three endpoints.
- Supporting evidence/source: E03 `generated.required_repair_cases_completed` and `natural.completed_repair`; E04 metrics.
- Numerical denominator: 192 generated repair-bearing cases, 288 required fields, 288 all generated cases; natural repair denominator 64 source errors in 108 cases. These are not interchangeable.
- Independently reconstructed: YES historically.
- Uncertainty: structural qualification and A; S/D unmeasured; no natural transfer inferred.
- Already supported: YES.
- Additional evidence required: useful heldout natural repair; generated successes alone cannot admit a restorer.

### C07 — Complete G2 factorial endpoints

- Exact claim, MEASURED RESULT: Expanded-panel B100 WERs for D0-U1/D0-U8/D1-U1/D1-U8 are 114.858815/124.384401/111.086675/33.375879%; C101 WERs are 4.832502/6.230609/10.768566/8.041079%; RAW is 2.774614%.
- Supporting evidence/source: E07 fixed-cell tables; E06 `tables` archived controls and prescribed endpoints; E09 independent result receipt.
- Numerical denominator: 50,926 reference words, 1,413 RAW errors, 2,696 natural cases and 52 groups for every cell. D0-U1 is archived and rescored, not retrained.
- Independently reconstructed: YES historically for all eight cells and descriptive group intervals.
- Uncertainty: G; S/D unmeasured. A affects decomposition, not integer WER distances.
- Already supported: YES descriptively; no winning-cell claim.
- Additional evidence required: useful paired systems/final evidence before representation-superiority or capability claims.

### C08 — Data/update interaction

- Exact claim, CALCULATION: The within-arm WER interaction `(D1U8-D1U1)-(D0U8-D0U1)` is −87.236382 pp for B100 and −4.125594 pp for C101. U8 improves D1 relative to U1 but worsens D0 for both arms.
- Supporting evidence/source: E07 exact fractions `-22213/25463` and `-2101/50926`; E06 `factorial_analysis.<arm>.effects.WER`; E09 exact-fraction/bootstrap checks.
- Numerical denominator: fixed 50,926 reference words per cell; shared 52-group paired bootstrap, 10,000 draws.
- Independently reconstructed: YES historically.
- Uncertainty: G intervals B [−90.379734, −84.259554], C [−5.050752, −3.203511] pp; S unmeasured. D changes composition; U bundles multiple optimizer effects.
- Already supported: YES as the registered intervention contrast.
- Additional evidence required: unbundled controls and new prospective authority to identify diversity or step count as a unique cause.

### C09 — Prescribed G2 candidates remained inadequate

- Exact claim, MEASURED RESULT: B100-D1-U8 and C101-D1-U8 fail WER strictly below RAW. B also fails genuine generated required repair. D1-U8 remains predeclared; no alternative cell or intermediate is admitted.
- Supporting evidence/source: E10 post-G2 decision; E06 `endpoint_viability`, `D1_U8_remains_predeclared_candidate`, `model_or_cell_selection_performed`; E09 endpoint-only gates.
- Numerical denominator: two prescribed scratch candidates, natural population 2,696/50,926/1,413; generated 288 cases/192 repair-bearing cases.
- Independently reconstructed: YES historically.
- Uncertainty: gate outcome exact under frozen rules; S/D limit generalization.
- Already supported: YES.
- Additional evidence required: separately accepted scientific treatment; a bootstrap interval or relative improvement cannot reverse eligibility.

### C10 — ByT5 descriptive trajectory and endpoint failure

- Exact claim, MEASURED RESULT: At actual presentations 28,228/70,568/141,130, ByT5 WER is 3.012214/3.073086/3.239995%, completed repairs 84/105/120 and introductions 205/257/357. Exact ten-pass adequacy fails against RAW 2.774614%.
- Supporting evidence/source: E08; E06 ByT5 `tables` updates 7057/17642/35283; E09 and recorded milestone/checkpoint reviews; E10.
- Numerical denominator: 2,696 natural cases, 50,926 words, 1,413 source errors; one seed 42 adaptation of 14,113 records for ten passes.
- Independently reconstructed: YES historically; nominal offsets +2/+3/0 and state bindings also verified.
- Uncertainty: A, G endpoint interval [2.782617, 3.756010]%; S/D unknown; pretraining/distribution/budget not matched to scratch.
- Already supported: YES as trajectory and frozen endpoint outcome, not a chosen best checkpoint.
- Additional evidence required: new prospective authority for a different recipe; intermediate selection cannot be performed retrospectively.

### C11 — Repair counts do not offset introduced damage

- Exact claim, MEASURED RESULT/CALCULATION: G2 B/C/ByT5 endpoints complete 44–45/18/120 repairs while introducing 15,628–15,629/2,702/357 errors. C has 20 raw repairs; raw conservation uses 20, not 18. ByT5 has 237 net additional errors versus RAW.
- Supporting evidence/source: E06 `natural.repair`, `completed_repair`, `introduced`, `output_errors`; E08; E11 §§D–E; E09.
- Numerical denominator: repair rates /1,413, introduction rates /50,926; all 2,696 cases, failures included.
- Independently reconstructed: YES historically for endpoint scores/conservation; aggregate conservation also checked during documentation preparation.
- Uncertainty: A and G separately; S/D unknown. Introductions are not merely correct-token damage.
- Already supported: YES.
- Additional evidence required: none for these counts; utility requires a separately qualified source-only system.

### C12 — Originally lexical-zero material was damaged

- Exact claim, CALCULATION: B/C/ByT5 damage 1,600/288/183 of the 1,818 originally lexical-zero natural cases; ByT5 contributes 239 errors on that stratum.
- Supporting evidence/source: E11 §D lexical-zero stratum table and its frozen endpoint score bindings; E12 v2 §I. E06 binds the original endpoint aggregates but does not expose this stratum as a named `natural_subsets` entry.
- Numerical denominator: fixed 1,818 lexical-zero cases; word-error totals are counts, not case rates.
- Independently reconstructed: historical G2 subgroup scores YES; detailed retrospective decomposition not fully requalified by v3.
- Uncertainty: reference-conditional zero status, G/S/D; no semantic-harm prevalence estimate.
- Already supported: YES narrowly.
- Additional evidence required: independent replication/generalization evidence for a broader preservation claim.

### C13 — Narrow TRAIN fit without heldout usefulness

- Exact claim, MEASURED RESULT: B100 D0-U8 is lexically target-exact on all 64 selected TRAIN error diagnostics (113 errors repaired, zero introduced), while expanded DEVELOPMENT WER is 124.384401%. B100 D1-U8 has zero target-lexically exact outputs on its separate 64 TRAIN error diagnostics.
- Supporting evidence/source: E06 TRAIN diagnostics and endpoint table; E09's 12-state reconstruction; E11 §J.
- Numerical denominator: 64 selected TRAIN error cases per condition, not all TRAIN; heldout 2,696 cases/50,926 words. Selections differ across D.
- Independently reconstructed: YES historically for greedy/teacher-forced diagnostic aggregates.
- Uncertainty: selected-sample scope; S/D; no matched-example causal contrast.
- Already supported: YES as fitting/transfer evidence.
- Additional evidence required: causal memorization/conditioning claims or repetition remedies require new controls.

### C14 — C has multiple edit-decision bottlenecks

- Exact claim, CALCULATION/INFERENCE: C D0-U8 has exact spans on 63/64 selected TRAIN errors, with 39 exact-span/wrong-replacement cases; D1-U8 gives no-edit on 52/64. Heldout D1-U8 returns no-edit on 661/878 error-bearing cases and has zero target-lexically exact outputs there.
- Supporting evidence/source: E11 §F; E12 v2 §H and v3 §§B, F; E06 TRAIN/heldout exactness aggregates.
- Numerical denominator: 64 selected TRAIN error cases in each D; 878 heldout lexical-error cases, separately 1,818 lexical-zero cases.
- Independently reconstructed: PARTIAL. G2 greedy aggregates yes; v3 explicitly did not repeat complete C decomposition/omission calculations.
- Uncertainty: diagnostic program definition, canonical versus alternate-program equivalence, S/D; mechanisms inferred rather than causally isolated.
- Already supported: counts YES as recorded calculations; unique causal explanation NO.
- Additional evidence required: a separate reconstruction of detailed program diagnostics before making them a central publication result; new controlled treatments for remedies.

### C15 — Natural repetition dilution

- Exact claim, CALCULATION: D0 has 18,693 repair presentations with 763 records repeated 18 times and 261 repeated 19; D1 has 19,538 with 8,688 records presented once and 5,425 twice. Means are 18.254883 versus 1.384397.
- Supporting evidence/source: E11 §B/Appendix1; E12 v3 §B independently reaggregated these distributions; E05 ledger identities.
- Numerical denominator: 1,024 versus 14,113 distinct natural repair records; not all channel presentations.
- Independently reconstructed: YES historically for these repetition distributions; exact weighted sums and means checked from public aggregate numbers here.
- Uncertainty: exact ledger counts; interpretation/generalization S/D unmeasured.
- Already supported: YES.
- Additional evidence required: more repetition improving transfer remains an unexecuted scientific question, not a conclusion.

### C16 — Charge and first-pass accounting

- Exact claim, CALCULATION: Natural repair charge is 1,000,665 (D0) and 1,000,628 (D1); first full passes end at 547,635 and 7,218,011 total canonical exposure. Identity presentations are separate: 28,040/29,365, charges 1,501,032/1,501,003.
- Supporting evidence/source: E11 §§B–C and Appendices1/3; E12 v2 §G.
- Numerical denominator: repair/identity ledgers separately; charge-based pass equivalents divide by full-pass charges 54,812/721,825; no optimizer or word-count substitution.
- Independently reconstructed: PARTIAL. Aggregate G2 charge identities yes; v3 independently checked repair repetition, not all detailed phase/first-pass/identity tables.
- Uncertainty: exact calculation conditioned on retained ledgers; S/D for interpretation.
- Already supported: YES as recorded calculations with qualified reconstruction limits.
- Additional evidence required: separate detailed ledger reconstruction if elevated to a central paper finding; new training for causal exposure claims.

### C17 — Fixed whole-output benefit and oracle ceiling

- Exact claim, CALCULATION: B/C/ByT5 prescribed endpoints have better/equal/worse counts 2/297/2,397; 3/2,197/496; 67/2,360/269. Whole-output oracle gains are 2/3/109 errors across 2/3/36 groups, giving oracle WER 2.770687/2.768723/2.560578%.
- Supporting evidence/source: E11 §§D–E; E12 v2 §I and v3 §B independently reaggregated point ceilings from retained scores by two equations.
- Numerical denominator: all 2,696 natural cases, 50,926 words and 1,413 RAW errors. Only complete cached proposals may replace RAW.
- Independently reconstructed: YES historically for point proposal/oracle aggregates; no private rows reprocessed here.
- Uncertainty: oracle reference dependence; G intervals in C18; S/D unknown.
- Already supported: YES as an oracle diagnostic only.
- Additional evidence required: independently evaluated source-only policy for achievable benefit; arbitrary edit mixtures are a different experiment.

### C18 — Oracle gain uncertainty and its limit

- Exact claim, CALCULATION: ByT5 oracle headroom is 0.214036 WER pp, approximately 7.714% of RAW errors; its recorded descriptive 95% group interval is [.154027, .288196] pp. B/C intervals are [0, .010418]/[0, .013181] pp.
- Supporting evidence/source: E11 §§E, I; E12 v3 §B point-gain verification; E09 establishes the historical shared-draw contract, not independent reproduction of all new feasibility intervals.
- Numerical denominator: 50,926 reference words for pp, 1,413 RAW errors for relative gain, 52 groups/10,000 shared draws.
- Independently reconstructed: PARTIAL. Point gain yes; detailed feasibility oracle intervals not fully repeated in v3.
- Uncertainty: G, not A or S; oracle does not predict transfer or selectable gain.
- Already supported: YES as recorded calculation, with limited independent scope.
- Additional evidence required: separate interval reconstruction if central to publication; fresh independent data and authorized source-only policy test for capability.

### C19 — Existing features establish no deployable policy

- Exact claim, INFERENCE: Descriptive edit-burden, completion, event-count and TRAIN-support summaries do not demonstrate an effective acceptance rule; no detector, threshold or calibrator was fitted in the feasibility study and probability traces were unavailable.
- Supporting evidence/source: E11 §G; E12 v2 §R, v3 §§D, M–O.
- Numerical denominator: three fixed endpoints over 2,696 natural/288 generated cases; populated bins retain their actual counts, empty bins are zero observations.
- Independently reconstructed: no full new independent feature reconstruction; accepted frontier interpretation preserves this absence-of-capability boundary.
- Uncertainty: S/D, unspecified separability, probability information unmeasured.
- Already supported: YES as a limit of completed work; “no policy can work” is unsupported.
- Additional evidence required: accepted prospective FIT/SELECT/EVAL design, qualified fresh groups and separate execution authority.

### C20 — No exact collision witness proves little about recoverability

- Exact claim, CALCULATION/INFERENCE: D1 TRAIN plus natural DEVELOPMENT contains 16,809 records, one duplicate raw-source key with two rows and no conflicting byte/lexical targets; absence of conflicts does not prove source-only recoverability.
- Supporting evidence/source: E11 §H; E12 v3 §J.
- Numerical denominator: 14,113 TRAIN + 2,696 DEVELOPMENT records; local-mapping denominators are different and must remain separate.
- Independently reconstructed: NO full fresh reconstruction recorded by v3; this is the retrospective calculation and accepted limited interpretation.
- Uncertainty: mostly unique sources, reference policy, unknown acoustic/semantic truth, D.
- Already supported: YES as recorded calculation/absence of a witness; universal inferability NO.
- Additional evidence required: appropriate independent support/ambiguity evidence before broader claims; no invented acoustic labels or model-judged gold.

### C21 — Evaluation and independent reconstruction scope

- Exact claim, FACT: Historical G1 review rescored 36 panels / 14,256 instances and independently dense-checked 11,783 within its budget; G2 reconstructed 42 heldout panels of 2,984 cases and 12 separate 304-case TRAIN states. G2 uses 10,000 paired draws over 52 groups, distinct from alignment bounds and unmeasured seed uncertainty.
- Supporting evidence/source: E04; E09 independent receipt `panels_reconstructed`, `cases_per_panel`, draw hash and separate checker identities; E01 §23.
- Numerical denominator: G1 dense coverage 11,783/14,256, leaving 2,473 outside budget; G2 heldout 125,328 instance rows, not 125,328 independent cases; TRAIN 3,648 instance rows separate.
- Independently reconstructed: YES historically; public bindings checked here, no full rerun.
- Uncertainty: A/G/S/D remain distinct; verification scope is finite.
- Already supported: YES.
- Additional evidence required: nothing to describe historical checks; new data/results require new verification.

### C22 — Native recipe and evaluation cost

- Exact claim, MEASURED RESULT/CALCULATION: G1's six recipe intervals total 23,128.912421s (6.424698h); G2's seven total 132,122.121229s (36.700589h). G2 ByT5 consumes 79,862.099614s, including training, saves and four observations; components must not be added again.
- Supporting evidence/source: E03 `sum_serial_recipe_wall_seconds`, `outcomes[].recipe_wall_seconds`; E08 observation table; E10 accounting `recipes[].attempt_elapsed_seconds_MEASURED` and physical observations.
- Numerical denominator: six/seven physical recipe attempts, zero scientific replay, one ByT5 trajectory; G2 archived controls incur no new training.
- Independently reconstructed: YES historically, source ledger/resource scopes separately verified.
- Uncertainty: MEASURED host wall versus unmeasured exact device kernel time; G2 all-in operational span unmeasured; electricity/depreciation/price UNPRICED.
- Already supported: YES for this native implementation/budget; universal efficiency NO.
- Additional evidence required: complete matched useful-system request comparison, multiple hardware/quality settings or final training for expanded cost claims.

### C23 — Related work forecloses broad novelty claims

- Exact claim, FACT/INFERENCE: Full-versus-compact ASR comparison, scratch specialization, selective correction, source copying and conservative correction all have direct precedents; none alone is this project's novelty.
- Supporting evidence/source: E01 §3; E02 F01; E14; the nine primary sources linked in draft §Q, accessed 2026-10-10; E12 v1 §S and v2 §P.
- Numerical denominator: nine named prior works reviewed, not a systematic exhaustive literature population; no cross-paper score denominator.
- Independently reconstructed: existing F01 qualification plus current primary-page verification; external experiments were not reproduced.
- Uncertainty: literature completeness and version/input/cost differences; prospective empirical distinctiveness remains a review question.
- Already supported: YES for exclusions and overlap; publishable novelty NO.
- Additional evidence required: later frontier paper-scope/positioning review; a distinct informative result beyond implemented machinery.

### C24 — Current prerequisites remain blocked/held

- Exact claim, FACT: Mozilla Common Voice 26.0 British English remains NOT QUALIFIED, fresh independent data are unavailable, acceptance execution and Generation 3 are NOT AUTHORIZED, and final seeds/populations/protocol remain untouched/held.
- Supporting evidence/source: E12 v3/v4 and unchanged amendments; metadata-access blocker supplied with this task, consistent with v4 retained403 evidence; E10 final-work boundary.
- Numerical denominator: zero qualified new acceptance populations, zero acceptance/G3 executions; historical G2 data cannot become untouched validation.
- Independently reconstructed: identity/status documents verified; no new Mozilla access audit or qualification performed here.
- Uncertainty: exact payload/eligibility/component sufficiency and current access resolution unverified by this task.
- Already supported: YES at this documentation checkpoint and supplied current state.
- Additional evidence required: successful bounded metadata/source qualification, reviewed independent population bindings and separate owner execution authorization.

### C25 — Result most relevant to capability-based viability

- Exact claim, OPEN SCIENTIFIC QUESTION: Whether the fixed ten-pass ByT5 proposer plus source-only whole-output acceptance meets prospective benefit/preservation requirements on independent groups, and whether conditional scores improve upon the otherwise identical structural policy.
- Supporting evidence/source: E12 v3 §§M–O and v4 unchanged prerequisites; E11 oracle/feature limitations.
- Numerical denominator: no observed future outcome; prospective FIT 4,000 / SELECT 2,000 / EVAL 6,000 and minimum 80/40/100 components are requirements, not available populations or passed gates.
- Independently reconstructed: NOT APPLICABLE; no experiment exists.
- Uncertainty: future capability/mechanism/transfer, all unmeasured.
- Already supported: NO as a result; YES as the already accepted prospective question.
- Additional evidence required: qualify fresh data, record missing scientific bindings, obtain separate execution permission, execute the fixed design and independently verify it. Documentation does not authorize any step.

## Figure and table blueprints

FACT — These eight specifications are complete blueprints, not generated charts or an additional analysis campaign. Plot data must come from existing public aggregates. If an item needs private rows, missing grouping, new probability extraction or protected material, leave it a blueprint and request the required scientific review/authorization; do not open that material here. No smooth curve, fabricated zero, fitted trend or model-selection symbol is authorized.

### F01 — Generation-1 scratch outcomes

- Purpose/claims: C05–C06; show failed natural adequacy beside generated learning without merging populations.
- Exact sources: E03 primary G1 receipt `outcomes[]`, choose `learning_curve[]` where `nominal_endpoint=10000000`; fields `natural.output_errors`, `reference_words`, `source_errors`, `completed_repair`, `introduced`, `wer`; generated `whole_case_conformance`, `required_repair_cases_completed`, `required_repair_fields_completed`. Cross-check E03 endpoint selection and E04.
- Data roster: all six recipes, grouped by B/C and LR 1e-4/3e-4/6e-4. Errors B 2,208/2,584/2,664; C 121/128/109; RAW 64. Exact values already appear in draft §G.
- Layout/axes: table or two natural WER panels with shared LR categories, RAW horizontal line 64/2,270; generated panel reports successes with explicit /288, /192 or /288-fields labels. Full B scale retained; a C detail panel must show its own scale.
- Denominators/uncertainty: natural 108 cases, 2,270 words, 64 source errors; no invented sampling bars. Alignment bounds shown only for decomposition. Failures/structural qualification retained.
- Caption requirement: DEVELOPMENT, single seed 42, all endpoints ineligible, selected LRs null. Generated counts are not natural repair.
- Status: public aggregate values AVAILABLE; no new row processing needed. Unsupported source processing stops at this blueprint.

### F02 — Generation-2 B100/C101 factorial WER

- Purpose/claims: C07–C09; show all four prespecified cells within each arm and the treatment interaction.
- Exact sources: E06 `tables` keys `archived-B100-D0-U1`, `archived-C101-D0-U1`; for each arm, `G2-<arm>-D0-U8-seed42-lr3e-4/update2440`, D1-U1/update305, D1-U8/update2440. Fields `natural.output_errors`, `reference_words`, `wer`. E06 `paired_group_bootstrap.WER.intervals` supplies 95% intervals; E07 table checks and `factorial_analysis.<arm>.effects.WER` supply exact contrasts.
- Data roster: eight endpoints exactly as draft §I, with RAW 1,413/50,926. WER B 114.858815/124.384401/111.086675/33.375879%; C 4.832502/6.230609/10.768566/8.041079% in D0U1/D0U8/D1U1/D1U8 order.
- Layout/axes: two arm panels, x=data condition, separate U1/U8 series, y=WER%; preserve full B values above 100%. Identify archived controls and predeclared D1-U8 candidates in labels; no “winner” badge. Effects table in percentage points with exact fractions.
- Denominators/uncertainty: 2,696 cases, 50,926 words, 52 groups; 95% paired group intervals, 10,000 draws. Exact distances do not have alignment-bound WER bars. S remains unmeasured.
- Caption requirement: D changes composition; U bundles optimizer behavior; actual cross-D exposure differs. Intervals do not establish H1 or candidate eligibility.
- Status: public aggregate values/intervals AVAILABLE; no private rescore or bootstrap rerun.

### F03 — Repair versus introduced-error tradeoffs

- Purpose/claims: C10–C12; distinguish repaired source errors from damage rather than ranking WER alone.
- Exact sources: E06 endpoint keys for B/C D1-U8 and ByT5/update35283; `natural.completed_repair`, `repair`, `introduced`, `reference_words`, `source_errors`, `invalid_or_incomplete`; E08/E11 reconciliation.
- Data roster: B completed 44–45 / raw 44–45, introduced 15,628–15,629; C completed 18 / raw 20, introduced 2,702; ByT5 completed / raw 120, introduced 357. RAW has zero repair/introduction by identity. Optionally show ByT5 nominal 2/5 states 84/205 and 105/257 separately as descriptive trajectory points, never selected alternatives.
- Layout/axes: counts table with two denominator columns, or x=completed repair/source errors%, y=introduced/reference words%; include a count companion. A display-bound segment represents alignment endpoints, not confidence. Avoid stacking unlike rates.
- Denominators/uncertainty: repair / 1,413, introduction / 50,926; 2,696 cases. G intervals, if displayed, use corresponding lower and upper estimands in E06 `paired_group_bootstrap`; never combine them into one unexplained error bar.
- Caption requirement: raw conservation uses C 20; completion-qualified repair is a separate utility metric; failures included, no bare-model fallback credit.
- Status: public aggregates AVAILABLE; additional fine-grained damage extraction remains outside this task.

### F04 — C101 adaptation trajectories

- Purpose/claims: C07, C09, C14; copying-to-editing trajectory without retrospective checkpoint selection.
- Exact sources: E06 `tables` for new C101 D0-U8, D1-U1, D1-U8, updates 0/248/736/1632/2280/2440 (U8) or 0/31/92/204/285/305 (U1); `state.actual_exposure`, `optimizer_updates`; `natural.wer`, `completed_repair`, `introduced`, `source_lexical_identity`, `invalid_or_incomplete`. E06/E07 fixed-panel observations cross-check.
- Exact actual exposure vectors: D0 `[0,1017149,3018478,6693230,9350642,10007223]`; D1 `[0,1016836,3017745,6692124,9349783,10006223]`. WER vectors: D0U8 `[86.857401,2.792287,3.161450,4.318030,4.999411,6.230609]`; D1U1 `[86.857401,2.774614,2.774614,2.774614,10.872639,10.768566]`; D1U8 `[86.857401,2.774614,2.774614,3.481522,6.267918,8.041079]` percent.
- Layout/axes: x=actual canonical exposure; y=WER%, separate companion rows for completed repairs/1413, introductions/50926 and invalid counts/2696. Retain initialization and endpoint; a full-scale plot plus explicitly labelled zoom can preserve early failures. Straight connections merely join observations; no interpolation claim.
- Denominators/uncertainty: same 2,696/50,926/1,413/52-group population at each state. A ranges and recorded G intervals distinct. No new checkpoint inspection.
- Caption requirement: early RAW equality has zero completed repair and is descriptive, not eligibility. Endpoint-only candidate gates remain failed.
- Status: public observations AVAILABLE. Missing finer event trajectories stay unplotted; no model scoring.

### F05 — ByT5 2/5/10-pass descriptive trajectory

- Purpose/claims: C10–C11; correction increases while introduced damage rises faster.
- Exact sources: E06 ByT5 `tables` updates 0/7057/17642/35283 and E08 schedule/observation tables; exact labels retained from `byt5-execution-schedule.attempt01.json`.
- Data roster: actual presentations 0/28228/70568/141130; nominal 0/28226/70565/141130; offsets 0/+2/+3/0. WER 100/3.012214/3.073086/3.239995%; repairs 0/84/105/120; introductions initialization 49,648–49,652, then 205/257/357. Natural invalid 2,696/1/1/0; generated invalid/capped 288/69/171/63.
- Layout/axes: x=actual presentations or actual/14113 pass-equivalent; label nominal milestones separately. WER panel with full initialization scale and clearly separate post-adaptation detail; companion count/rate table. No best-checkpoint marker.
- Denominators/uncertainty: natural 2,696/50,926/1,413; generated 288 separate. G intervals only from recorded E06 fields, A bounds separate.
- Caption requirement: milestone offsets are inside fixed extent; exact ten-pass endpoint alone supplies adequacy and fails. Pretraining/data/budget differ from scratch.
- Status: public data AVAILABLE; no probability extraction or renewed inference.

### F06 — D0-versus-D1 natural repetition

- Purpose/claims: C15–C16; show diversity/repetition tradeoff without calling repeated presentations independent data.
- Exact sources: E11 §B for repetition, charge, first-pass and identity values; §C for phases; Appendix1 complete group counts; Appendix3 diagnostic exposure. E12 v3 §B independently confirms repair distributions, while detailed accounting has narrower independent coverage.
- Data roster: record-balanced repair frequency mass: D0 (18 → 763, 19 → 261); D1 (1 → 8,688, 2 → 5,425); zero → 0 for both. Companion values: 18,693/19,538 repair presentations, means 18.254883/1.384397, repair charge 1,000,665/1,000,628, first full pass 547,635/7,218,011. Identity counts 28,040/29,365 and identity repetition/charges appear in draft §M, separated from repair.
- Layout/axes: frequency table or x=presentations per distinct repair record, y=number or explicitly normalized fraction of records within D. Phase charge and first-full-pass table separate from frequency distribution. Do not use equal-size bars that hide denominators 1,024/14,113.
- Denominators/uncertainty: 1,024/14,113 records; exact finite ledger counts, no fabricated sampling bars. Charge-based pass equivalents use 54,812/721,825 full-pass charges, not record counts.
- Caption requirement: increased diversity under approximately fixed charge, not a pure sample-count intervention or test of sustained D1 training. More exposure helping is unproved.
- Status: aggregate blueprint AVAILABLE. Independent detailed reprocessing is outstanding if these calculations become central; no private ledger access here.

### F07 — Whole-output proposal benefit and oracle headroom

- Purpose/claims: C17–C19; contrast actual damage with a reference-aware ceiling.
- Exact sources: E11 §§D–E, I; E12 v3 §B point-gain reaggregation; E06 endpoints bind original scores. Do not reconstruct per-case chart points from private outputs.
- Data roster: all 2,696 cases: B better/equal/worse 2/297/2,397; C 3/2,197/496; ByT5 67/2,360/269. Actual errors 16,997/4,095/1,650, RAW 1,413; oracle errors 1,411/1,410/1,304; gains 2/3/109, groups 2/3/36. ByT5 headroom 0.214036pp/7.714% RAW; recorded gain interval [.154027,.288196]pp.
- Layout/axes: outcome-category counts beside RAW/actual/oracle error table or WER panel. Explicit “reference-aware oracle” label on every oracle series; actual and oracle status visually distinct. Descriptive group intervals labelled separately with partial independent verification disclosed.
- Denominators/uncertainty: outcomes / 2,696, WER / 50,926, relative removable errors / 1,413; groups / 52. No raw-repair summation substituted for whole-output gain.
- Caption requirement: complete fixed proposals or RAW only; no edit mixing, new text or checkpoint change. No deployable policy demonstrated; oracle benefit does not predict new-population gain.
- Status: aggregate data AVAILABLE; uncertainty is recorded, not freshly requalified; remains a blueprint.

### F08 — Training and evaluation runtime

- Purpose/claims: C22; expose complete native cost and component nesting.
- Exact sources: E03 `outcomes[].recipe_wall_seconds`, `training_resources` and `learning_curve[].resources`; E10 accounting `recipes[]` fields `recipe_id`, `attempt_elapsed_seconds_MEASURED`, `unique_logged_optimizer_updates`, `unique_scientific_presentations`; each `attempts[].logged_training_seconds_MEASURED`; E08 four observation intervals and decode/scorer components; E10 `physical_evaluations` inventory.
- Data roster: all six G1 and seven new G2 intervals as draft §P. ByT5 observations at actual 0/28228/70568/141130: 8525.970953/7214.049868/10059.125263/7074.588477s. Training 21,143.834539s is nested in 79,862.099614s recipe time. Archived D0U1 adds zero new G2 training.
- Layout/axes: recipe wall seconds/hours table or bars, all 13 attempts. Separate component table for training/observation/decode/scorer with “included in” relationships, rather than adding overlapping components. G1 endpoint decode comparisons retain complete panel 396 versus G2 panel 2,984 labels; do not compare them as equal-work latency.
- Denominators/uncertainty: physical attempts, updates/presentations separately; timing scope defined per field, no sampling interval invented. Kernel time and G2 operational span UNMEASURED; electricity/depreciation/price UNPRICED. Pretraining is not assigned zero cost.
- Caption requirement: one local native implementation, failed models and unequal comparator training; compact decoding does not prove overall efficiency. Failed CPU verification attempts remain separate from scientific replay.
- Status: public aggregate timing fields AVAILABLE. Missing kernel/all-in/cost fields remain unavailable rather than estimated without authority.

## Manuscript readiness boundary

INFERENCE — Methods, configuration/provenance, G1/G2 negative development results, treatment interactions, repair/introduction accounting, repetition and oracle diagnostics, uncertainty and local runtime can be drafted now. The record does not support useful restoration, H1 confirmation/rejection in the final population, universal architecture failure, generic compact-edit novelty, a deployable acceptance policy or broad efficiency claims.

FACT — Fresh independent data remain unavailable; Mozilla is NOT QUALIFIED and metadata-blocked at the supplied current state. Acceptance and Generation 3 remain NOT AUTHORIZED. Final/sealed work is HELD. Detailed retrospective calculations keep their incomplete independent reconstruction status. The draft does not select a new paper direction.

OPEN SCIENTIFIC QUESTION — The accepted v3 source-only acceptance capability/mechanism experiment, after its data prerequisites and separate authorization, is the future result most relevant to capability-based publication viability. Its outcome is unknown. No model, protected data, scientific evidence or automation is changed by this preparation.

MANUSCRIPT_DEVELOPMENT_EVIDENCE_PREPARED
