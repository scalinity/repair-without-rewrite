# Lexical corruption profile v2 independent review — 2026-10-05

**INDEPENDENT PROFILE ESTIMATION AND COMPLETE ACCEPTED-POOL INVERSION REPRODUCED.** The independently reconstructed complete revised table and all 1,024 private per-record projected audits match production **byte for byte**. The new table hash is `bc14b7ca5e8299ee8004cefb6deb67151ea93f1d44f48ea48d0b4619a9549b87`. After one identified state-count defect was corrected, independent source-only inversion and edit-lineage checks pass for all **42,020 accepted generated views**. No supported-table stop or empty required generated stratum occurs. Realized edit concentration, reader admission, actual B/C fairness, BENCH, resume, cost, and the six probes remain separate gates.

Authorization is [Frontier Corruption-Profile Decision v2](FRONTIER_CORRUPTION_PROFILE_DECISION_V2.md), preserved at `ab8fe9578ec335d7abb20fd2b39dbe3e162e1868` on reviewed checkpoint `1b114ff485a2a59051bf7a2e39acec5774fd35a1`. I read the decision and latest owner implementation request in full. No thresholds, estimands, zero/severity policies, generated rules, objectives, or architecture were revised by this reviewer.

## Independent implementation and input binding

The [independent CPU checker](../../benchmarks/lexical_corruption_profile_v2_independent.py) imports no production projection, alignment, or estimator logic. It uses its own scanner, loading the pinned Unicode 15.1 `CaseFolding.txt` and `PropList.txt` tables. It applies NFC, explicit pinned full/common case folding, NFC again, declared lookalike mappings, and the lexical scanner. Every emitted token is nonempty and contains no ASCII separator space. `Phi` is exactly their single-ASCII-space join; the empty sequence projects to the empty string. The original natural inputs, spoken anchors, and written model targets are not modified.

The independent aligner propagates intersections of edit sets through all optimal predecessor paths, rather than using production's forward/reverse path-count product test. A separate backward walk of the optimal predecessor graph recovers the union of possible edit edges. It counts optimal paths exactly and identifies every unanimous operation, both projected coordinates, and payload. The checker also reconstructs support by its own record/group sets and computes leave-one-group-out support by subtracting cached per-group contributions. Production instead rebuilds reduced entry tables from cached observations.

The public table schema and serialization were coordinated after the initial independent measurements. Sharing a schema does not share projection or alignment calculations. All distance/severity map keys in the revised schema are strings, so a parsed JSON round trip cannot recreate the earlier raw review's numeric-key serialization error.

The checker independently verifies the frozen pair-file hash, role-manifest hash against the supply receipt, and official source-archive hash. It directly rejoins all selected TRAIN IDs to official `text_raw` references, processed-text hashes, source groups, role/family metadata, and frozen hypothesis hashes. It does not call production's source-admission join. It checks 1,024 distinct completed TRAIN records / 48 groups, excludes all 96 CALIBRATION records, and verifies no TRAIN/CALIBRATION ID or source-group overlap. HPO, final, student outputs, and external confusion lists do not contribute.

The unchanged lexical policy identity reproduces as `e1dc5baa5f5098a7e0f39d3b3e3d612439886715dac5924e2be6b8cd1eed39b0`. Exact private audit parity proves projection and alignment agreement on **every frozen pair**, not only an aggregate count. All supported, rejected, and possible-only table entries, source-group support lists, six class pairs, group diagnostics, and all 48 leave-one-group-out rows reproduce exactly.

## Measured profile and rejection denominators

Raw-zero prevalence remains **182/1,024**. Lexical-zero prevalence reproduces as **690/1,024**, and lexical-positive support as **334/1,024**. These prevalence quantities are reported separately from the conditional corruption-channel exposure weights.

The uncapped projected-codepoint distance distribution is:

`{0:690, 1:103, 2:117, 3:42, 4:40, 5:11, 6:7, 7:2, 8:2, 9:2, 10:1, 11:2, 12:2, 13:1, 17:1, 21:1}`.

| Quantity | Independently reproduced result |
|---|---:|
| Projected unit edit mass | 875 |
| Omitted because observations are not unanimous | 511; 58.4000% of projected mass |
| Consensus occurrences | 364 |
| Rejected by record/group support | 135; 37.0879% of consensus mass, 15.4286% of projected mass |
| Retained occurrence weight | 229; 26.1714% of projected mass |
| Combined ambiguity/support omission | 646; 73.8286% of projected mass |
| Supported / unsupported elementary keys | 20 / 221 |
| Possible / ambiguous optimal edit edges | 1,700 / 1,336 |
| Records with ambiguous edits / multiple optimal paths | 169 / 169 |

Both identities hold exactly: **875 = 511 + 135 + 229** and **364 = 135 + 229**. Possible-edge ambiguity is a different denominator: **1,336/1,700 = 78.5882%**. Multiple incompatible possible edges can represent one uncertain edit unit. Neither old raw percentages nor word-edit counts are substituted for the projected denominator.

| Operation | Retained occurrence weight | Share |
|---|---:|---:|
| Substitution | 49 | 21.3974% |
| Deletion | 106 | 46.2882% |
| Insertion | 74 | 32.3144% |

Every supported entry satisfies **five distinct records AND three groups**. Actual support ranges are **5–31 records / 4–21 groups**. Unsupported and ambiguous-only entries retain zero sampling weight. Training repetitions have not supplied or re-estimated any support.

## Conditional severity and class-pair dependence

| Phase | K=0 | K=1 | K=2 |
|---|---:|---:|---:|
| P0 | 0 | 1 | 0 |
| P1/P2 | 0 | 103/334 = 30.8383% | 231/334 = 69.1617% |

The severity denominator is all **334 positive projected distances before support rejection**. It is not 229 retained occurrences, 521 prior word-edit units, or the 875 projected edit units. Lexical-zero records remain in the full profile's prevalence/coverage denominator but contribute no zero-operation empirical sampling weight. This is the authorized conditional intervention, rather than a reproduction of natural zero prevalence or the severity tail.

For class pairs, the independent checker first restricts to unanimous observations belonging to individually supported entries, then requires distinct original codepoint slots or insertion gaps. Two insertions at the same original gap do not qualify. Each record is counted at most once for each class pair.

| Class pair | Distinct records | Groups | Sampling weight |
|---|---:|---:|---:|
| SS | 3 | 3 | 0; record support fails |
| SD | 11 | 9 | 11 |
| SI | 7 | 6 | 7 |
| DD | 16 | 12 | 16 |
| DI | 8 | 7 | 8 |
| II | 5 | 5 | 5 |

A record may support more than one class pair, so pair weights must not be interpreted as a count of disjoint records. This table qualifies only the approved broad operation-class dependence. Conditional independence of sampled literal payloads within an admitted class pair remains an explicitly controlled generated-domain assumption. No literal-pair joint-observation claim is made, and the old 85 literal-pair entries do not qualify this revision.

## Group concentration and leave-one-group-out diagnostics

**47 of 48 groups** contain a lexical-positive record. **38 groups** contribute at least one retained elementary occurrence. Positive-record counts range from 0 to 22 per group; retained mass ranges from 0 to 23. The largest group's contribution is **23/229 retained occurrences (10.0437%)** and **22/334 positive records (6.5868%)**. These counts describe clustered support; they are not independent sample-size or final-campaign power claims.

Each leave-one-group-out diagnostic removes one entire group, retains its independently computed alignments, requalifies the same 5-record/3-group entry thresholds, and recomputes conditional severity. All 48 diagnostics agree exactly with production. They yield:

- Remaining positive records: **312–334**.
- K=1 conditional probability: **30.0000%–31.5951%**; K=2 is its exact complement.
- Retained occurrence mass after support requalification: **193–229**.
- Supported entry count: **17–20**.

The ten reported entry identities are selected once from the full table, ordered by descending full-table weight and then key. They are never reselected after omitting a group.

| Fixed full-table entry | Full weight | Leave-one-group-out weight range |
|---|---:|---:|
| Delete ASCII separator | 33 | 30–33 |
| Delete `e` | 31 | 25–31 |
| Insert `e` | 18 | 16–18 |
| Insert ASCII separator | 17 | 14–17 |
| Delete `d` | 16 | 12–16 |
| Insert `d` | 13 | 10–13 |
| Insert `u` | 10 | 7–10 |
| Insert `a` | 9 | 7–9 |
| Substitute `a` → `e` | 9 | 7–9 |
| Substitute `e` → `i` | 8 | 6–8 |

These are sensitivity diagnostics. No entry weights, thresholds, severity, or generation policy were tuned from them.

## Scientific stops and scope boundary

The supported table is nonempty. Its largest single entry has **33/229 = 14.4105%** of occurrence weight. Pure projected ASCII-separator insertion/deletion has **50/229 = 21.8341%**. Neither is strictly greater than 50%; both retained-table concentration alarms are false. No table-level scientific stop fires.

Punctuation or boundaries are not globally banned: projected apostrophe deletion survives with seven occurrences across six records/five groups, and projected separator operations remain eligible. These are lexical-sequence discrepancies under the fixed scanner. Their retention does not assign homophone, numeric, or other unobserved semantic classes, and scorer invariance outside this projection does not establish semantic harmlessness.

**Profile estimation alone does not qualify generated corruption.** Applicable field weights, accepted variants, all required category/cell/severity pools, field `Phi` equality, lexical-effect gates, complete source-only union inversion, the 50-proposal/500-state limits, and realized canonical-charge-weighted concentration require separate evidence. The complete accepted-pool checks below establish inversion and edit lineage; realized presentation concentration still needs the reader ledger. The old raw table is diagnostic and cannot be included as an active generated inverse relation. A supported natural entry is not automatically applicable or uniquely recoverable on a technical spoken field.

The two realized concentration alarms remain unverified by this report, because it has no corruption-channel presentation ledger. Complete reader shares, raw/lexical source==target exposure, reuse, paired consumption, 32,768-anchor updates, resume, and BENCH likewise receive no PASS here. This reviewer executed no model, accelerator workload, training update, 10M recipe, final/sealed candidate inference, or protocol freeze.

## Independent source-only generated inverse review

The revised [generated inverse](../../src/generation/lexical_v2.py) receives only the source, public grammar/profile and state cap. It imports no finite generated-target manifest, selected target, operation trace, channel or phase. Target comparison occurs after the inverse returns one unique complete target. Its relation includes written clean/one-elementary-operation-per-field rule views, exact spoken rendering including zero-operation preimages, supported empirical K=1 on either spoken field, and empirical K=2 with one operation on each field and an admitted unordered class pair. Higher-order same-field rule composition and the diagnostic old raw table do not enter this relation.

I implemented a separate CPU oracle in ignored `exports/lexical-reader-v2/independent-review/inverse_check.attempt02.py`. It uses the public catalog as grammar data, its own complete scaffold parser and typed written-field regexes, its own spoken encoder/decoder, its own core and empirical reverse-neighbor enumeration, the independently pinned scanner, and its own union assembly. Production inversion is called only as the comparison subject; its preimage helpers are not reused. Oracle target enumeration has no finite TRAIN-target lookup or intended-target input.

The first 280-fixture comparison identified an actual state-count defect. Complete K=2 field tuples rejected by class-pair support were examined but omitted from the budget. For fields `ona` / `oni`, the unsupported SS pair required two states, including its compatible grammar, while production counted one. At cap one this changed failure status. A public off-manifest path fixture with 14 repeated `e` characters in each basename required **842 states**, but production reported 58 and returned ambiguity instead of a capped search. Duplicate relation-path tuples and repeated-literal rejects were already retained by this point; the missing class-pair rejects were the remaining issue.

The implementation now counts class-pair rejects before admission and preserves every complete examined tuple before target deduplication. This maintains the existing public inverse convention of compatible grammar plus complete field combinations; individual symbolic field-parser neighbors are not optimizer or search states. The initial failed checker output, receipt, cases and production-source snapshot are preserved. The interrupted complete-pool attempt made with the deficient counter cannot supply admission evidence.

After the correction, **all original 280 fixtures plus 72 additional typed two-field class/orientation fixtures pass**. The 352 cases compare complete candidate sets, status, compatible families and exact examined-state counts. Repeated calls with populated field caches and reduced-cap comparisons also agree. They cover every TRAIN/DEV template scaffold, all eight categories, public values outside the generated TRAIN inventory, every supported elementary entry when applicable, admitted and unsupported two-field classes, zero spoken preimages with an empty empirical table, duplicate clean/spoken paths, repeated-literal rejection, malformed spacing/case, and the 500-state overflow. Expected outcomes are **334 unique, 16 no-inverse, one ambiguous and one capped**. No final-test values, model inference or accelerator work were used.

The deliberately ambiguous off-manifest spoken path retains both zero-operation and empirical-preimage targets; the inverse cannot use the generated inventory to resolve it. The unsupported SS example contributes no target, and supported II is retained. The 842-state example now fails closed with no targets. These checks and the source inspection identify no remaining inverse defect in the reviewed revision, but this bounded comparison does not by itself qualify every accepted generated variant or required pool.

The successful inverse comparison completed in **0.731764 seconds**, loaded no MLX or Torch, and binds the revised source SHA-256 `bc5fef652aa73b90f659be83d39d3a16ad4099c037e962463ad96924f5f04f4d`. Independent checker hash is `54c87817e7c8d3f1962f08f5f907336dec36625348c2bb471db1d3b78965b22e`; complete cases hash is `274a8343c8e6da6845842099762207523611cfe88c434eac753ba356fbaa5723`; successful receipt hash is `5ead4cd36f73f653e760f15b0aa4f9f6fefabf41e865da2d5b9a655f63162c64`; actual stdout hash is `b42cb4950c53cedb13a4570e2fda8f208433546acc2d5f9f5e8767ec95a7ce16`. The failed first receipt remains `f833efac6fa3d4444b9b664bb8307943932bf342c5cf8292898bd3a1156cb1cc`.

The replacement complete pool is bound to [attempt02 qualification](../../experiments/manifests/lexical_reader_v2/generated-pool-qualification.attempt02.json), summary SHA-256 `a969c68805edac1be61023e43551b677ac96564369a8e0dbe32c02a7f7f46a1b`, and accepted-file SHA-256 `dc9caac46145eee1e8d9ebea34ff486b3b08afffaee447d0bb22e12bef3fe8dc`. Its preflight SHA-256 is `4f9cdc7fea9aae495198159f18ac0df1b82760b4dc7c21831d8ab6b20d1bf8b4`. The independently checked inverse source matches the executed preflight hash before and after review.

The separate streaming checker calls the independent oracle on each source before comparing its result with the stored target. **42,020 of 42,020 accepted views** have one unique entire target, exact stored examined-state counts, and valid independently checked field/edit lineage. It rechecks raw source/anchor/target hashes, exact spoken rendering, field `Phi` equality, preserved scaffold bytes, permitted rule operations, supported empirical literal keys and class pairs, one operation per changed field, and both field-level and complete-source lexical-effect gates. All accepted empirical variants pass; no old raw entry is used as an active relation.

The accepted file contains **8,404 distinct base IDs, 8,404 target hashes and 42,020 variant IDs**. Each of clean, mixed, two-repair, empirical K=1 and empirical K=2 contributes 8,404 views. Independent row counts reproduce all **160 required category/cell/view strata**, each nonempty. A distinct variant ID does not imply distinct physical source/target support: shared lineage and cross-channel collisions remain reader reporting obligations. Maximum examined states among accepted views is **3**. Production's maximum **11** includes rejected proposals and has a different denominator.

The complete accepted-pool review passes in **29.208477 seconds**, with no MLX or Torch modules loaded. Its checker SHA-256 is `2e2ade806892931cc5b1a8f65449b6214984352a0b1334c9f3877547e85bde44`; complete per-variant check-stream hash is `32335a9c083edfda615f1a8295bf8a852d13f5e095c06f15e157aa95ccfa1565`; receipt hash is `3f9c05a16af693255a8ec54a5e149c2a382415900bfaa4250a217e546d9b6d2a`; stdout hash is `7048e87110912f7b151857125a20cc7e171d18379577e56c3745d67ac563bb17`. Exact scripts, stdout/stderr and per-variant evidence remain ignored under `exports/lexical-reader-v2/independent-review/`.

This full-pool PASS establishes accepted inversion, lineage and nonempty coverage. It does not reproduce the deterministic proposal draw sequence, independently qualify native capacity, or establish any realized reader allocation. Required realized presentation concentration and reader/actual paired-consumption gates remain pending. The corrected counting defect is an implementation qualification issue, not evidence of an architecture failure or a newly adopted scientific policy.

## Preserved raw evidence and durable independent artifacts

The checker recomputed the **complete old raw table from all 1,024 raw pairs using its own aligner**, including raw consensus/ambiguity, support, severity, and literal co-occurrence. Its serialized reconstruction has the unchanged SHA-256 `5df3800d7a29e370abdce36bd489989482d5d878765612b5a14a4b2cab1fc310`, identical to the original bytes. Its label remains **raw TRAIN reference-to-recognizer surface differences under the repaired Parakeet development runtime**. It was neither overwritten nor reinterpreted as the revised estimator.

The initial independent run saved its own projected observations and diagnostic profile before production-schema coordination; it completed successfully in 13.403328 seconds. The final schema/parity run completed in **12.984134 seconds**, including independent raw-table reconstruction, and loaded no MLX or Torch modules. Eleven independent projection fixtures and 49 exhaustive tiny alignment pairs pass within the checker. Actual stdout/stderr, per-record audits, both diagnostic and canonical reconstructions, raw-table reconstruction, a source snapshot, and receipts remain in ignored `exports/lexical-reader-v2/independent-review/`. The first diagnostic output is preserved as an earlier schema, rather than rewritten into the later canonical output.

The [production measurement](../../experiments/manifests/lexical_reader_v2/lexical-profile-measurement.attempt01.json) and [preflight](../../experiments/manifests/lexical_reader_v2/lexical-profile-preflight.attempt01.json) record its separate 25.673543-second CPU estimation/input-binding measurement and code/input identities. The revised estimator's hash is separate from both the old raw table and any future generated reader bundle.

| Identity | SHA-256 |
|---|---|
| Approved v2 decision | `267fc5e4aae08b54cfe879395aef47e1e61c128ea1fc8c6ba27ccc310b685339` |
| Latest owner implementation request | `49af098c27c0eba54e26de2343bc411eb69ebc9e468956579e726195b89330a5` |
| Frozen TRAIN/CAL pair file | `ce4a170a086afee430085c4e6f665e8af58b8c68091afc27f10ee403c81951d8` |
| Role manifest | `56c5889d952c83120267ea92b4aaf8bcec63dff61a34e83ce531c9be97b3eb98` |
| Pinned production lexical scanner | `4db62c3238c830ec25faf979beb656dcc7b882f0843b318d973934b4f340111d` |
| Production revised estimator | `99636542963ea16a3cf81ef4978833b4eb1fe8651cef52c6e194c2eaa1e3f7ce` |
| Production runner | `1a56224abf4477b4b8b9392396058e3a2d0d12995c044c429aa636b632243980` |
| Production revised tests | `bf989a5674b123c2d2cc87b48b8b94230adad463cbb7e145dd6cdebd9d206771` |
| Independent checker | `2069aeb848133ed5218e8c97035fac563078a9b0d4f42db79d41f8f348b0f370` |
| Revised complete table, independently reproduced | `bc14b7ca5e8299ee8004cefb6deb67151ea93f1d44f48ea48d0b4619a9549b87` |
| Complete private projected audit, independently reproduced | `943f3b8041ddfae89b3a3cf2a6aec4db6299e5e2b1d3c6557d59e48732f6e3b0` |
| Independent final parity receipt | `a6873b4736836798c739ab17860377ee85cd708674f02d4d1cb266a214a6df4b` |
| Independent final stdout | `85930354c0c376681fe3b7c19ed3dde16c9c72e5d7568d7a36e79552ae1e9614` |
| Preserved/reconstructed raw table | `5df3800d7a29e370abdce36bd489989482d5d878765612b5a14a4b2cab1fc310` |

No production files, amendments, immutable inputs, dependency lock, Git index, or Git refs were modified by this reviewer. Public checker/report bytes contain no restricted utterances, private absolute paths, or session metadata.

PROFILE_AND_ACCEPTED_GENERATED_INVERSION_REPRODUCED_READER_ADMISSION_PENDING
