# Lexical corruption profile v2 qualification — 2026-10-05

**PROFILE ESTIMATION QUALIFIED; GENERATED POOL AND READER ADMISSION PENDING.** The approved `development_lexical_corruption_v2` was implemented without a new scientific choice. Neither retained-table strict-majority alarm fires. No generated-pool, complete reader, paired consumption, update/resume or BENCH PASS follows from this result.

The approved [frontier decision](../reviews/FRONTIER_CORRUPTION_PROFILE_DECISION_V2.md) and its exact amendment were separately committed at `ab8fe95` before implementation, on verified clean local/published `1b114ff485a2a59051bf7a2e39acec5774fd35a1`. The required baseline reproduced: **275 passed in 23.34s**, `MLX_ENABLE_TF32=0`; [baseline receipt](../../experiments/manifests/lexical_reader_v2/baseline-validation.attempt01.json).

## Inputs and exact estimation

All **1,024 frozen TRAIN pairs / 48 groups contribute once**. The unchanged `lexical_eval_v1` uses pinned Unicode 15.1 tables. `Phi(x)` joins its ordered token values with single ASCII spaces; token nonemptiness and separator safety are asserted. Projection is an estimation view only; model inputs, targets and anchors are never normalized by this estimator. All 96 CALIBRATION pairs are excluded; there is no HPO/final/student/external contribution.

The reference/hypothesis bytes rejoin admitted TRAIN roles, families, groups, and official `text_raw`/processed-reference hashes. Pair-file SHA-256 remains `ce4a170a086afee430085c4e6f665e8af58b8c68091afc27f10ee403c81951d8`. Exactly **690 lexical-zero / 334 lexical-positive** records reproduce. Lexical errors occur in **47 of the 48 groups**; **38 groups** supply retained edit mass.

Alignment identity is `lexical-projected-codepoint-all-optimal-edge-consensus-v2`. Unit-cost codepoint edits run from projected reference to hypothesis. An observation requires operation, both coordinates and literal payload to agree across every optimal alignment. The production implementation reuses the unchanged exact prefix/suffix path-count mathematics. An independent implementation uses its own lexical scanner and forward intersections/backward unions of optimal edit sets.

An entry requires **five distinct records AND three groups**. Retained occurrence count supplies its weight. Six unordered S/D/I class pairs use individually supported observations at distinct original positions, exclude same-gap insertion pairs, require the same support floor, and count each supporting record once. Generated literal-payload independence is explicitly a controlled assumption, not observed literal-pair dependence.

## Measurement

| Quantity | Result |
|---|---:|
| Projected unit edit mass | 875 |
| Ambiguity-omitted unit mass | 511 / 875 = 58.4000% |
| Consensus occurrences | 364 |
| Support-rejected occurrences | 135 / 364 = 37.0879% |
| Retained weighted occurrences | 229 |
| Supported / unsupported entries | 20 / 221 |
| Retained S / D / I | 49 / 106 / 74 |
| Records with ambiguous edits / multiple optimal paths | 169 / 169 |
| Possible / ambiguous possible edit edges | 1,700 / 1,336 |
| Retained-entry record support | 5–31 |
| Retained-entry group support | 4–21 |
| CPU measurement including input binding | 25.673543 seconds |

The reconciliation is **875 = 511 + 135 + 229**. Combined omission/rejection is **646/875 = 73.8286%**. Possible-edge counts have a different denominator and are not observed unit-edit mass. High ambiguity/support omission limits the profile's coverage; this is disclosed, not repaired by threshold relaxation.

Uncapped projected-distance distribution, numerically ordered:

`{0: 690, 1: 103, 2: 117, 3: 42, 4: 40, 5: 11, 6: 7, 7: 2, 8: 2, 9: 2, 10: 1, 11: 2, 12: 2, 13: 1, 17: 1, 21: 1}`

The 40% channel has **K=0 weight zero**. P0 has K=1 weight 1. P1/P2 have **K=1: 103/334 (30.8383%); K=2: 231/334 (69.1617%)**. These pre-support probabilities are canonical-exposure weights, not natural prevalence or matched WER. Raw-zero prevalence remains 182/1,024; lexical-zero prevalence remains 690/1,024.

Class-pair weights/support (records/groups): **SS 0 (3/3, unsupported), SD 11 (11/9), SI 7 (7/6), DD 16 (16/12), DI 8 (8/7), II 5 (5/5)**. No unsupported SS composition is admitted. The old 85 literal-pair entries are not an active revised relation.

## Concentration and group sensitivity

Largest entry is projected ASCII-space deletion: **33/229 = 14.4105%**. Combined separator-only insertion/deletion is **50/229 = 21.8341%**. Both are below the approved strict-majority threshold; neither table alarm fires. No reweighting was performed.

The complete [table](../../experiments/manifests/lexical_reader_v2/lexical-profile-table.attempt01.json) records each entry's supporting group IDs, group-level positive-record/edit counts and all 48 leave-one-group-out diagnostics. Support is requalified after each group omission using cached unanimous observations; no new alignment or tuning occurs. Retained mass ranges **193–229**, supported entries **17–20**, and conditional K=1 probability **0.300000–0.315951**. Fixed full-table top-ten entry weights are reported in every omission. These are sensitivity diagnostics, not estimates from a large independent corpus.

## Independent reproduction and artifact boundary

The [independent checker/review](../reviews/LEXICAL_CORRUPTION_PROFILE_V2_INDEPENDENT_REVIEW.md) reproduces **all 1,024 projected audits and the complete serialized table byte-for-byte**, including ambiguity, rejected entries, source-group support, severity, class pairs, and leave-one-group-out fields. Its projection/alignment code does not import production estimator logic. Independent table SHA-256 equals **`bc14b7ca5e8299ee8004cefb6deb67151ea93f1d44f48ea48d0b4619a9549b87`**; the private audit SHA-256 equals **`943f3b8041ddfae89b3a3cf2a6aec4db6299e5e2b1d3c6557d59e48732f6e3b0`**.

The old raw table is separately reconstructed by the independent checker and remains byte-identical at **`5df3800d7a29e370abdce36bd489989482d5d878765612b5a14a4b2cab1fc310`**. It remains labeled **raw TRAIN reference-to-recognizer surface differences under the repaired Parakeet development runtime**.

The new table hash identifies an estimator output, not a full renderer/proposal/pool/reader freeze. Realized edit concentration, category/cell/severity availability and exact inversion remain dependent gates. Targeted estimator validation: **22 passed in 2.60s**. No model, BENCH, registered probe slot, final training, sealed candidate inference or protocol freeze occurred during profile estimation.
