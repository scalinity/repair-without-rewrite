# Independent paired-reader contract review — 2026-10-05

**Disposition: FRONTIER_MODEL_REVIEW_REQUIRED for the affected mixed-reader/BENCH branch.** The supplied documents fix the objective, four mixture shares, canonical accounting components and B/C mathematical contracts. They do not yet fix enough of the generated training population, empirical corruption treatment or pilot presentation policy to construct the requested registered mixed ledger without consequential scientific choices. Existing natural pairs are independently valid; this is not a source-pool failure, an architecture verdict or a measured failure of a repetition threshold. No threshold is invented here.

This review reads the canonical source, registry, prospective amendments, existing reader/generator/tokenizer/edit interfaces, foundation/admission reports and actual development metadata. It independently recomputes counts, hashes and native label quantities rather than accepting the root audit's summary. Work is CPU-only. It creates no examples, presentation schedule, model job, optimizer update or final-data exposure. Existing reports/evidence are preserved.

## Contract evidence and the remaining choices

Line references below identify the supplied files at the hashes recorded at the end of this review. `canonical` denotes `docs/design-inputs/EXTRACTED_CANONICAL_SOURCE.md`; `registry` denotes `docs/design-inputs/LocalFlow_Publication_Experiment_Registry_v2.txt`.

| Contract | Exact evidence | Consequence for this continuation |
|---|---|---|
| Four shares are **canonical exposure**, not example counts | canonical §10.2, lines 1065–1065; §14.4, lines 1482–1486; registry lines 344–356 | A repeating 3/2/1/4 row schedule does not establish 30/20/10/40 when anchors differ. A dry-run must reproduce anchor-weighted totals and its prospectively defined discrepancy policy. |
| Same example schedule and complete common update boundary | canonical §10.4, lines 1110–1110 | B/C consume one predeclared ordered ledger. Native C event length, microbatch padding and valid-loss counts cannot change that schedule or its charge. Whole common-update overshoot is reported. |
| Model sees corrupted source; accounting sees clean anchor and target | canonical §§10.4/12.3/17.2, lines 1087–1089, 1317–1323, 1710–1710 | Do not replace the clean accounting anchor with the actual corrupted source, use C event counts as paper exposure, or feed accounting metadata to the model. |
| Accounting serialization must be frozen | canonical lines 1087–1087 and 1317–1323 | The component invariant is supplied; a versioned integer-producing serializer still needs its exact trusted framing/EOS/delimiter specification. The old natural-probe formula is not that specification. Resolve this under the separate canonical review without changing the invariant. |
| Required-repair programmatic cases need a unique public source inverse | canonical §14.2, lines 1453–1459 | A remembered hidden clean seed does not alone justify repair supervision. Natural reference-anchored pairs and unique-inverse stress fixtures have distinct validity scopes. |
| Empirical text corruption needs training-observed characterization | canonical §14.3, lines 1463–1478; registry lines 403–405 | Characterization source, aligner ambiguity treatment/coverage, confusion tables, lexicons, severity and compositions are not supplied as a frozen reader configuration. Designing these quantities changes the corruption treatment. |
| Text corruption starts from the deterministic spoken rendering | canonical lines 1484–1486 and 1553–1557; registry lines 405–412 | Direct corruption of a formatted target is not an interchangeable implementation. The renderer implementation hash is still pending; no general qualified renderer artifact appears in the current reader/generator. |
| No-op cases remain valid; no forced edit quota | canonical lines 1473–1473 and 1615–1615; registry lines 424–425 | The natural pool's byte or lexical identity yield cannot be edited away. The 30% identity/minimal share does not determine the identity/minimal subdivision or the generated channel's no-op rule. |
| Generated support and reuse need explicit policy | canonical lines 1488–1488, 1592–1592, 1611–1615; registry lines 429–431 | These require reporting and a frozen seed/view weighting, repetition cap and reserve/exhaustion policy. They supply no numerical minimum support or cap. The illustrative 75-repeat arithmetic is not an acceptance limit. |
| Real-pair source allocation/order is a development decision | canonical §12.6, lines 1383–1393 and §17.2, lines 1722–1722 | Hash-bound eligible rows exist. A uniform-row versus uniform-group policy, reuse order and exposure balance are not determined by eligibility alone. No claim that the present pool is too small follows without a declared gate. |
| Phase difficulty is conceptually fixed, but pilot mapping is not | canonical lines 1075–1075, 1714–1724; registry lines 353–356 | Final P0/P1/P2 budgets are 100M/40M/10M; phase difficulty and P2 replay/generation policy await freeze. A 10M pilot uses a predeclared pilot schedule. Neither a scaled phase schedule nor an all-P0 pilot is specified here. Final P2 choices are not independently imposed as a new current pilot requirement; the current pilot schedule still needs an explicit resolution. |
| Common context admission includes C's actual serialization | canonical lines 1114–1118 | Check source/control, full-target/EOS and `1+R+3K` before the common schedule. Do not drop only C's difficult examples. Raising the cap or windowing changes the qualified population and requires the appropriate declared extension. |

The prospective amendments, lines 21–37, settle development reference bytes, model naming, bounded comparator recipes and earlier natural calibration panels. They do not add a mixed-reader pool, empirical corruption profile, share scheduler, repeat cap or pilot phase policy. Earlier admission already identifies those dependencies (`docs/reports/BC_10M_PROBE_ADMISSION_DECISION.md`, lines 3–5, 17, 41 and 47). That report is corroborating historical evidence; the normative findings above come from the actual canonical sections, not the report's conclusions.

## Existing interfaces do not resolve the scientific gaps

`src/data/development_reader.py`, lines 8–47, is a hash-bound released-target join. It enforces allowed development roles, stable audio identity, `text_raw`, both reference hashes and official archive identity. It returns sorted admitted targets. It supplies neither the four-channel population nor sampling/augmentation/presentation semantics.

`src/generation/stress.py`, lines 1–6 and 181–194, defines `qualified_core_v1`: typed `1/l` and `0/O` confusions, separator verbalization, unit aliases and polarity-preserving spelling. Lines 244–303 construct three typed two-slot views and require agreement with the public source inverse; lines 330–341 choose the development panel by cell/group hash. This is useful exact conformance infrastructure. It is not an empirical natural confusion/severity model, general spoken renderer or canonical mixed curriculum. `configs/stress_development.json`, lines 2–15, explicitly marks development-only status, eight categories, 288 cases, bounded proposals and no final generation. A stress-slot proposal bound is not a TRAIN pool repetition/exhaustion rule.

Some qualified primitives may be reused in a subsequently approved rule-composition channel. Assigning all these fixtures to a 20% curriculum without approved category/composition/support weights, or rebranding them as the 40% empirical corruption treatment, would add a treatment choice. The current TRAIN fixture membership says `development_conformance_only`; its presence in a TRAIN partition is not proof of a registered training presentation population.

`benchmarks/bc_real_calibration.py`, lines 39–51, uses `[RESTORE_REFERENCE, SEP, source, EOS]` and the earlier `2 * target_BPE + 3` anchor convention. `src/models/tokenizer.py`, lines 164–170, separately offers a four-control source frame explicitly named `dev_source_frame_v1_not_frozen`. Neither supplies a frozen clean-anchor-plus-full-target paper accounting serialization. Different source layouts are not by themselves proof of a violated canonical invariant; they do make silent promotion of the old arithmetic into the registered counter unjustified.

## Independent metadata and label reproduction

I parsed the committed role manifest and raw frozen pairs directly, loaded the qualified project tokenizer, recomputed strict UTF-8 source/reference hashes, rejoined each pair to its role/group/reference metadata, rebuilt source-relative edit programs and checked exact rendered targets. C totals below were recomputed from each program's edit count `K` and replacement BPE count `R`: decoder `1+R+3K`, action `K+1`, start/end `K`, vocabulary `R+K`. These are native/loss quantities, not the canonical accounting definition. All 1,120 root inventory entries agree on every reproduced numerical field. No model weights or neural runtime were loaded or executed.

| Released role metadata | Rows / unique stable IDs | Closed groups | Unique raw target hashes | Raw target bytes | Lexical target tokens |
|---|---:|---:|---:|---:|---:|
| TRAIN | 45,729 / 45,729 | 314 | 45,716 | 8,423,028 | 1,547,339 |
| CALIBRATION | 6,271 / 6,271 | 40 | 6,264 | 1,136,880 | 209,366 |
| HPO DEVELOPMENT | 898 / 898 | 12 | 898 | 85,970 | 16,000 |

| Actual frozen natural pairs | TRAIN | CALIBRATION |
|---|---:|---:|
| Rows / groups | 1,024 / 48 | 96 / 5 |
| Rows per group, minimum–maximum | 6–61 | 13–28 |
| Unique source / target hashes | 1,024 / 1,024 | 96 / 96 |
| Byte-identical source/target | 182 | 19 |
| Source / target BPE total | 24,456 / 24,846 | 2,318 / 2,377 |
| Edit count K / replacement BPE R | 1,987 / 3,094 | 192 / 297 |
| C decoder positions | 10,079 | 969 |
| C action / start / end / vocabulary denominators | 3,011 / 1,987 / 1,987 / 5,081 | 288 / 192 / 192 / 489 |
| B target + EOS denominator | 25,870 | 2,473 |
| Native source with prior three controls | 27,528 | 2,606 |
| Prior `2 * target_BPE + 3` total, **not registered paper charge** | 52,764 | 5,042 |
| Rejections under the prior source/full-target/C 1,024 envelope | 0 | 0 |

There are zero pair role/hash/render failures and zero TRAIN/CALIBRATION group intersections. CALIBRATION is not admitted to fitting by this audit. TRAIN group sizes vary substantially; row-uniform and group-uniform replay would give different group weights. These counts describe available support, not independent random draws, a new repetition cap or sufficient support for an unchosen schedule.

The root inventory is `exports/paired-reader-bench/admitted-pool-audit-attempt01/inventory.jsonl`. Every one of its 1,120 `presentation_index` values is null. It is correctly an inventory, not a repeated presentation ledger or a successful mixed-reader dry-run. No new mixture/update balance, accumulation cursor, resumed exposure sequence or full-update rate can be reproduced from it.

Independently counted technical fixture artifacts:

| Artifact | Rows | Base groups | Template families | Unique target / source hashes | Views |
|---|---:|---:|---:|---:|---|
| `stress_split_repair_20261005T054436Z/split_audit_train_fixtures.jsonl` | 96 | 32 | 32 | 32 / 96 | 32 per each of the three views |
| Same directory, `latents.jsonl` (DEV) | 288 | 96 | 32 | 89 / 267 | 96 per each of the three views |

Both have eight categories with 12/36 rows per category respectively, correct literal payload hashes, and explicit TRAIN/DEV partition membership. Repeated content in DEV means base-group IDs are not interchangeable with unique target/source content. None of these counts is evidence of a natural mixed training population or the final stress population.

## Routine implementation versus frontier review

The following remain ordinary contract-preserving work once the population/presentation choices are supplied: immutable row/index/hash ledgers; exact source-only inputs; common context checks; deterministic cursors/RNG capture; padding masks; FP32 accumulation/master/moments; B global target+EOS denominator; C's four global component denominators; complete AdamW cadence; atomic verified checkpoint publication; update-boundary resume; and separate native/padding/canonical accounting. Canonical §17.1, lines 1701–1705 fixes the loss normalization. Registry lines 367–375 fixes optimizer/precision and leaves actual microbatch/bucketing to qualification. Choosing a microbatch size that preserves those mathematics is not itself a research redesign.

Canonical §19.7, lines 2074–2087, fixes actual full-update timing, five warmups, 100 timed updates, 20 measured thermal minutes, real-reader work and a cold 20-update resumed-versus-uninterrupted comparison. Nominal 32,768 is conditional on qualification, not permission to silently label the earlier four-request workload the selected regime. Canonical line 2262 explicitly permits optimizer-boundary checkpoints without gradient buffers; a boundary-only implementation with an enforced prohibition on partial-accumulation saves need not invent a new mid-update resume policy. An allowed mid-update path must preserve accumulator/denominator and exact cursor semantics.

The smallest frontier decisions needed are a written, prospectively approved specification of: (1) the actual generated TRAIN seed/target/rendering pool and rule/identity-minimal distributions; (2) the empirical corruption characterization/ambiguity/severity policy and its approved development construction procedure; (3) group/seed/view weighting, order, reuse, no-op allowance and reserve/exhaustion behavior, with any repetition/support acceptance gate explicitly supplied or explicitly designated reporting-only; and (4) the 10M pilot difficulty/phase schedule and canonical-share scheduling/discrepancy rule. These are choices for review, not implementations or recommended numeric values in this artifact. The final H2 acoustic acceptance policy and P2 final pool remain separately gated; this review does not expand the current task into their construction.

Identical B/C ledgers would control relative architecture exposure under a chosen population. They would not make an arbitrary newly selected corruption population equivalent to the approved scientific treatment. Substituting stress grammar for empirical corruption, changing clean rendering to formatted target, removing no-error cases, or using row percentages would confound the curriculum/channel or change the canonical exposure estimand. Changing the native cap or short filtering would change population admission. Changing loss weights/objectives or optimizer is outside routine reader work.

Accordingly, the pool audit may be reported as reproduced metadata. The requested registered mixed-reader qualification, paired complete-update BENCH, presentation-level fairness audit and resulting six-probe cost/admission decision cannot receive PASS from these artifacts. No long mixed schedule, model BENCH or six-slot probe should start by filling the missing scientific choices automatically. This is a request to resolve those exact choices under the user's frontier rule, not a conclusion that the paper path is unjustified.

## Audited identities

| File | SHA-256 |
|---|---|
| `docs/design-inputs/EXTRACTED_CANONICAL_SOURCE.md` | `94746ef2c223f9f461d5dc92378961813e8f9377fe89fd5166dd9d6097ced746` |
| `docs/design-inputs/LocalFlow_Publication_Experiment_Registry_v2.txt` | `596932dd91e0b108936c3a7a80245f4f44df5cfeac4f13d6fda8cfb30412cfe0` |
| `docs/reviews/PROSPECTIVE_AMENDMENTS.md` | `74c4d40bd47badda6d09948a37183217fc567edcab738963b5cdf876a6bbdf22` |
| `src/data/development_reader.py` | `24f61cb4a8245831b112fd2a25aa26e332e1cea6526d1e6ddd69f25d7a2ad3f5` |
| `src/generation/stress.py` | `0d83fdc4a2a54720d7269041d2698582cea9fc8b14a75605e5c547af14ca28ec` |
| `src/models/tokenizer.py` | `c6b7452659ae1654ca36d868f33367d17b03df0ad3325b58e993ccaf454d7372` |
| `src/models/edits.py` | `9a2b752fb50328e1f857a33fd011dee7e91681dfd5916938be0f1d706513e461` |
| `configs/stress_development.json` | `13e43073d75972ae14985934fde02eb38e9481674dc67bd983bfd3ed0b12c24c` |
| `configs/tokenizer_development/tokenizer.json` | `b125551f3c3627edc9cb8d325bc70bfd8340df1518f03d0fd16d140ff7ace6ca` |
| `experiments/manifests/public_lspc_training_roles.development.jsonl` | `56c5889d952c83120267ea92b4aaf8bcec63dff61a34e83ce531c9be97b3eb98` |
| `exports/foundation-repair/development-asr-pairs-attempt01/pairs.jsonl` | `ce4a170a086afee430085c4e6f665e8af58b8c68091afc27f10ee403c81951d8` |
| `exports/paired-reader-bench/admitted-pool-audit-attempt01/inventory.jsonl` | `0f09c51308928db215aed1aa7a50e6da52affba915d9025ea9a7e3e14633ed8b` |
| Same audit directory, `summary.json` | `3fea973e215f0f09a26e87f1702cf629b61d069a0f9f2fef5839352dfbd0a224` |
| TRAIN stress fixtures above | `f5bed5a71ac0c9ec39c83a1a6fd8a7c588bb869be5ddee5a942788435cecfbe2` |
| DEV stress latents above | `fc8dad695c28f2f1be326546e1e528d5bdff7f548c23aea6ee7d74957c701cb1` |

The root audit's recorded starting revision is `f24712ed3b33e2396efbf4de89cf7409051ace4a`. The reproduction above is tied to actual listed artifact bytes; it makes no clean-tree or complete benchmark claim.

FRONTIER_MODEL_REVIEW_REQUIRED

## Integration clarification — interrupted partial accumulation

The original review bytes are preserved unchanged at `exports/paired-reader-bench/review-integration/original-reader-contract-review.md` (17,486 bytes, SHA-256 `876a9d4a42813725ba723785c408f2b042e91ea2b48fb590723041587ea064af`), with a separate identity receipt in that ignored directory. This appendix leaves those original observations intact and corrects the interpretation of the future partial-update obligation.

The latest user request, §10E, lines 605–607, explicitly says: “If the training contract allows checkpointing mid-update, test it.” It permits a prohibition proof instead only if that contract **explicitly forbids** mid-update checkpoint publication. Canonical line 2262 allows a mid-accumulation save when the complete accumulator and denominator are serialized. Default optimizer-boundary publication in canonical lines 2056/2083 is not an explicit contractual prohibition on the allowed mid-update case.

My earlier suggestion that a future boundary-only implementation could enforce rejection of partial saves does **not** by itself authorize replacing this user-required allowed-case test. Under the presently supplied permissive contract, the future B/C BENCH must exercise an interrupted partial-accumulation save/cold load/resume against an uninterrupted control, preserving accumulators, all applicable component denominators, model/master/moment state, RNG, scheduler, reader cursor, canonical charges and next presentation identity. A wrapper's choice to reject an allowed operation, or a rejection test alone, is not this qualification. Substitution of a prohibition proof requires an explicit applicable approved contract prohibition; none is established by this review. No partial-case test or prohibition proof has run for the new mixed reader.

The five integration reports retain the correct current scope: final H2 acoustic acceptance, SLUE access and the final P2 pool are not automatic current reader/BENCH prerequisites. The missing current pilot mapping and text-channel generation/sampling bindings remain the reasons for the frontier disposition. Broken evidence-link spellings and conditional LR wording observed in the first report read were separately reported to the root for correction; I did not edit its reports. The corrected reports were rechecked: all local Markdown targets exist, BENCH line 11 and V2 answer 20 require the allowed partial-state test, and BENCH line 13 preserves the user's conditional LR requirement without selecting a new clock or unconditional LR gate. No remaining unsupported gate/scope claim was identified in that read; new reader/BENCH qualification remains outstanding.

FRONTIER_MODEL_REVIEW_REQUIRED
