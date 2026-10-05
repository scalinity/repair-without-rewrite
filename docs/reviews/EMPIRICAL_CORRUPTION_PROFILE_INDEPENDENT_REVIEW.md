# Empirical corruption profile independent review — 2026-10-05

**FRONTIER_MODEL_REVIEW_REQUIRED.** The TRAIN-only estimator and measured table reproduce independently. The retained profile is dominated by punctuation, case, and whitespace effects: **1,945/2,113 retained occurrences (92.0492%)**. Punctuation and case alone account for **1,897/2,113 (89.7776%)**. Under the owner's explicit surface-artifact stop rule, dependent reader construction and admission must stop for a frontier scientific decision. This finding concerns the proposed corruption treatment; it is **not an architecture failure, failed training result, or demonstrated empty generated pool**.

Reviewed authorization: [Frontier Reader/Curriculum Decision v1](FRONTIER_READER_CURRICULUM_DECISION_V1.md), recorded at `bd882ceea205c2f9e0547fa49337e94e1b042fad` on reviewed base `928fd0305206ad6d6130d0667d1b206baa521a64`. The latest owner implementation request adds an explicit stop if this measured table is obviously dominated by a surface-policy artifact. No new filtering policy, normalization, allocation, architecture, objective, or generated replacement treatment was introduced by this reviewer.

## Independent method and actual scope

I read the owner request in full, the approved decision, repository instructions, canonical §§14.2–14.4, registry construction sections, source admission code, the complete new estimator/runner/tests, and actual measurement artifacts. Checks were bounded CPU work. The independent checker imports standard-library modules and `unicodedata2`; it neither calls the reviewed estimator nor imports a model, MLX, or Torch.

The reviewed implementation proves unanimous edges by multiplying exact prefix/suffix optimal-path counts. My independent implementation instead propagates the **intersection of edit sets over all optimal predecessor paths** through the forward dynamic program, with rolling sets/counts. It separately walks the optimal predecessor graph backward from the terminal state to recover the union of possible edit edges. For every TRAIN record I compared:

- Exact raw Unicode-codepoint distance and number of optimal paths.
- Every unanimous edit's operation, both coordinates, and literal payload.
- Every possible and ambiguous edit edge, omitted unit-edit mass, and source group.
- Independently aggregated elementary record/group support, occurrence counts, rejected weights, severity frequencies, and joint support.

All **1,024 per-record comparisons agree**. The reconstructed aggregate table agrees in every field and reproduces its exact serialized SHA-256, `5df3800d7a29e370abdce36bd489989482d5d878765612b5a14a4b2cab1fc310`. This reproduction includes all unsupported entries and rejected ambiguity diagnostics, not only the surviving entries.

The first reviewer-checker attempt completed all per-record and aggregate-object comparisons, then failed its own byte-serialization assertion: reloaded JSON distance keys were strings, so reviewer serialization sorted them lexically rather than in the original numeric order. Correcting only that reviewer serializer reproduced the original bytes. This was **a reviewer-checker serialization error, not an estimator discrepancy**. Both checker versions are preserved in the ignored `exports/frontier-reader/empirical-profile-attempt01/independent-review/` directory. The first failed process did not write standalone stdout/stderr files; its displayed combined tool output was copied into an explicitly labeled `checker.attempt01.tool-output.txt`. The corrected checker first succeeded interactively, then ran with the same code to save actual stdout/stderr and a hash-bound receipt. This durable evidence run records **9.663388 seconds** for its alignment/aggregate checks and imports no neural runtime. The corrected checker identity is `6822a082a40842dbadef741a31b79c97121d035b50a0e6a795434c3023cbb55c`.

The targeted estimator regression suite independently reran with **16 passed in 0.03s**. The root's [integrated receipt](../../experiments/manifests/frontier_reader/final-validation.attempt01.json) records **275 passed in 23.43s**; I inspected its current file hashes but did not rerun neural correctness tests. Test success does not qualify the reader, generated inverse relation, complete-update BENCH, or probes.

## Input binding

The checker independently parsed the frozen pair file and admitted TRAIN role manifest, checked the role-manifest digest against the supply receipt, and verified the official archive digest. It rejoined all 1,024 selected IDs to the official released records and checked `text_raw`, processed-text hashes, group, role, family metadata, and frozen hypothesis hashes. It did not use the production `load_targets` join to establish these checks.

| Input property | Independent result |
|---|---|
| Frozen selected records / unique IDs | 1,024 / 1,024; each contributes once |
| Source groups | 48 |
| Selected status / role | All `COMPLETED` / `train` |
| Official reference | Exact `text_raw`; strict UTF-8 |
| Alignment direction | Official reference → frozen repaired Parakeet hypothesis |
| Alignment normalization | None; case, punctuation, spacing, and decomposed scalars remain observable |
| CALIBRATION | 96 records excluded; no selected-ID or source-group intersection |
| HPO, final, students, external confusion lists | No profile contribution |
| Re-estimation through replay | None; there is no training replay |

The measured pair file contains TRAIN and CALIBRATION records, but only TRAIN records supply the profile. Metadata exclusion is distinct from future DEVELOPMENT evaluation consumption; this review performs no model evaluation and freezes no evaluation panel.

## Exact retained profile and rejection denominators

| Operation | Retained occurrences | Share of retained mass |
|---|---:|---:|
| Substitution | 938 | 44.3919% |
| Deletion | 879 | 41.5996% |
| Insertion | 296 | 14.0085% |
| Total | 2,113 | 100% |

| Diagnostic effect | Retained occurrences | Share of retained mass |
|---|---:|---:|
| Punctuation | 1,372 | 64.9314% |
| Case only | 525 | 24.8462% |
| Whitespace / boundary | 48 | 2.2717% |
| Other character | 168 | 7.9508% |

There are **465 literal elementary keys**, of which **67 survive** the required **five distinct records AND three groups** rule; 398 have zero sampling weight. Among actual supported entries, record support ranges from **5 to 212** and group support from **4 to 45**. Occurrence weights count unanimous observed edits, not training repetitions. Unsupported possible-only edits cannot supply record or group support.

The largest entry is deletion of a quotation mark: **433 occurrences, 212 distinct records, 40 groups**. Comma deletion has 246 occurrences/187 records/45 groups; comma insertion has 204/175/44. These three entries supply 883/2,113 retained occurrences (41.7889%). Their broad support does not remove the scientific concern that they principally transfer a reference/recognizer surface policy into the generated treatment.

| Quantity | Count | Explicit denominator / calculation |
|---|---:|---|
| Full raw edit mass | 3,089 | Sum of uncapped per-record distances |
| Omitted by alignment ambiguity | 759 | 24.5711% of raw edit mass |
| Unanimous observed edits | 2,330 | Raw mass minus omitted ambiguity |
| Rejected by record/group support | 217 | 9.3133% of unanimous edit mass; 7.0249% of raw mass |
| Retained weighted edits | 2,113 | 68.4040% of raw mass |
| Total omitted/rejected unit mass | 976 | 31.5960% of raw mass |
| Possible optimal edit edges | 4,254 | Union of optimal-path edit edges, not unit edit mass |
| Ambiguous possible edges | 1,924 | 45.2280% of possible edges |
| Records with ambiguous edits / multiple optimal paths | 229 | 22.3633% of TRAIN records |

The reconciliation is exact: **3,089 = 759 + 217 + 2,113**. The 1,924 ambiguous possible-edge count cannot be divided by 3,089 and presented as a rejected-observation fraction: multiple incompatible edges can describe one uncertain unit edit. Entry-key rejection fractions and weighted occurrence rejection fractions likewise have different denominators.

## Severity, zero mass, and co-occurrence

The independently reproduced uncapped distance distribution is:

`{0:182, 1:218, 2:163, 3:141, 4:103, 5:68, 6:41, 7:29, 8:18, 9:15, 10:8, 11:13, 12:3, 13:4, 14:6, 15:1, 17:3, 18:3, 19:1, 20:1, 23:2, 42:1}`.

| Phase distribution | Severity 0 | Severity 1 | Severity 2 |
|---|---:|---:|---:|
| P0: `min(d,1)` | 182/1,024 (17.7734%) | 842/1,024 (82.2266%) | 0 |
| P1/P2: `min(d,2)` | 182/1,024 (17.7734%) | 218/1,024 (21.2891%) | 624/1,024 (60.9375%) |

No-error mass is preserved exactly. Severity depends on full raw distance, not only retained edits. Capping this distribution does not establish that sufficient supported, uniquely invertible variants exist for each prescribed category/cell/severity.

**85 co-occurrence keys** satisfy joint support and individual-entry support. Independent reconstruction reproduced all joint occurrence, distinct-record, and distinct-group counts. In the measured natural records, the only pairs of unanimous edits sharing one reference coordinate were **27 insertion/insertion pairs**; the estimator excluded all of them as operations at the same original insertion gap. It represents original codepoint slots separately from insertion gaps. This is a diagnostic of observed natural edit geometry. No same-coordinate insertion/codepoint pair occurs in this data, so the data do not qualify that boundary case for generated composition.

Supported natural co-occurrence is not proof of nonoverlap, unique inversion, or recoverability after transfer to a generated spoken rendering. Those proposed positions must be checked in the original clean rendering and the complete source-only union qualifier. That machinery has not been implemented or admitted.

## Scientific stop evidence and limits

The aggregate effect labels are descriptive. Punctuation and whitespace can alter lexical content or meaning, and an `other` codepoint change does not identify a homophone, numeric, or proper-name class. I did not equate every punctuation-tagged edit with harmless formatting.

As a separate diagnostic, an independently implemented scanner using the pinned NFC/case-fold/lexical rules found **690/1,024 lexical-equal pairs (67.3828%)**, including **508 of the 842 raw-changed pairs (60.3325%)**. These agree with the root's [descriptive lexical audit](../../experiments/manifests/frontier_reader/raw-surface-descriptive-audit.attempt01.json). The lexical-equal records contribute **1,377 raw edit units**, and **1,201 supported retained occurrences: 314 case + 887 punctuation**. Thus **56.8386% of all retained mass** comes from records with no lexical token change under the already approved evaluation policy. This diagnostic never enters alignment, support, weighting, severity, or a filtering rule.

**Inference:** the retained table is dominated by reference/recognizer surface differences strongly enough to trigger the owner's scientific adequacy stop. Exact faithful raw estimation exposed the issue; estimator correctness cannot decide whether the resulting 40% treatment is scientifically appropriate. The evidence does not isolate which upstream surface convention caused every observation, establish a general Parakeet error distribution, or measure B/C learnability.

Dependent generation, scheduler/accounting integration, inverse qualification, dry runs, complete updates, checkpoint/resume, and BENCH remain **unqualified**. Required pools are **not constructed or assessed**, rather than measured empty. The table hash is a frozen estimator-output identity, **not a qualified full reader/profile freeze**: renderer, proposal/rejection ledger, accepted variants, and resulting pool hashes are absent. Zero registered mixed presentations or B/C complete updates occurred, and no 10M recipe slot was consumed. Final/sealed inference and protocol freeze remain unperformed.

The next action is the owner's frontier scientific review of how to handle this measured surface dominance before dependent implementation resumes. No table cleanup, re-estimation, new threshold, renormalization, or alternative treatment is authorized by this report.

## Provenance and publication hygiene

The runner's original measurement receipt contained one real absolute local code path in its `__file__` hash key. I reported it before publication. The root preserved the exact original outside Git and in ignored evidence, exported a separately identified [public receipt](../../experiments/manifests/frontier_reader/empirical-profile-preflight.public.attempt01.json), and changed future runner path recording to a repository-relative key. The original measurement source hash remains distinct from the corrected runner hash. The estimator, tests, raw input, table, and measurement-summary hashes did not change. Public reports contain no raw natural utterances or private machine/session paths.

| Identity | SHA-256 |
|---|---|
| Approved decision | `7089ef96c847623b01c3d3d54f179e3e2477b8239bdad9cc4a79998d6418043b` |
| Owner implementation/escalation request | `e404d6455189897c3a42b2728283de07dede5ecf6a827cda56badf98a0223473` |
| Canonical source | `94746ef2c223f9f461d5dc92378961813e8f9377fe89fd5166dd9d6097ced746` |
| Registry | `596932dd91e0b108936c3a7a80245f4f44df5cfeac4f13d6fda8cfb30412cfe0` |
| TRAIN role manifest | `56c5889d952c83120267ea92b4aaf8bcec63dff61a34e83ce531c9be97b3eb98` |
| Supply qualification | `d0b1de70c2d2a7c7bbc7ad711a4d771fa91a22ef399651b0482aaeeee7616842` |
| Official archive | `96d4eae2222b29b66437a21959252419bcd4762e5042e71e023790171054d1c0` |
| Frozen TRAIN/CAL pair file | `ce4a170a086afee430085c4e6f665e8af58b8c68091afc27f10ee403c81951d8` |
| Selected TRAIN hash list | `96ad9bee197bb1710175c426dda396f8cfa5abdf3d2d9de91b07fd3421f99240` |
| Estimator | `df4caf02e33aa529e4018f73b1bd72d916f81df475063029790ade83485ec2f3` |
| Measured runner source | `0889518d4992982dee3d14af6dfc5197079e55d951610e18d58894d5b4a8222c` |
| Corrected future runner | `ddde92f2b9899dbf6bc23106b002164b8ea1d8524122501b9fae847ecae742ef` |
| Estimator regression tests | `5e55a4044c32e846d1623d414590ab3162c4022e5df27a414c92a56a12781378` |
| Full private alignment audit | `a6e05d10011e58fc3568a48c4d40eb70bf54affb4d29752fe380fb9a56629d94` |
| Exact empirical table | `5df3800d7a29e370abdce36bd489989482d5d878765612b5a14a4b2cab1fc310` |
| Measurement summary | `04c393164363ca333c580cfd9ce5b6601cfba135ecd0790d605c5c6ab372462c` |
| Original completed preflight | `030dc548bea3be773590f75c7b385bf82cc0e390b5e1f106d65c8781ea266195` |
| Corrected independent checker | `6822a082a40842dbadef741a31b79c97121d035b50a0e6a795434c3023cbb55c` |
| Saved corrected-checker stdout | `bcb939b5eb2cfe81080cb03d7bbc869e54313d92b9276966af9ac778ac2e7ff3` |
| Independent evidence receipt | `c5263f10e5fb670a3a33c2fd6b514b4594e2354bb1e0584ed31fef44123dff86` |

Estimator/input/table checks: **REPRODUCED**. Full empirical channel and reader admission: **NOT QUALIFIED**.

FRONTIER_MODEL_REVIEW_REQUIRED
