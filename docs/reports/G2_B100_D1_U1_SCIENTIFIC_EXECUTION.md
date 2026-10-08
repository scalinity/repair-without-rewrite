# Generation-2 B100-D1-U1 scientific execution

Date: 2026-10-08T07:27:17.808627+00:00

Reviewed execution evidence base: `6ca92b9810f05ad88bb2a0a79462600ff698485c`. Scientific launch source: `b867d2430fb577c714e152d2f6ccad91d6095e49`. The published campaign freeze is `experiments/manifests/generation_2/execution-campaign-freeze.attempt01.json`.

MEASURED RESULT: `G2-B100-D1-U1-seed42-lr3e-4` completed attempt01 at the fixed endpoint without numerical replay or manual resume. Its outcome is `experiments/manifests/generation_2/scientific-outcome-G2-B100-D1-U1-seed42-lr3e-4.attempt01.json`. Independent completed trajectory/artifact reconstruction passes in `experiments/manifests/generation_2/scientific-recipe-independent-G2-B100-D1-U1-seed42-lr3e-4.attempt01.json`; paired review is `docs/reviews/G2_B100_D1_U1_EXECUTION_INDEPENDENT_REVIEW.md`.

| Training extent | Count |
|---|---:|
| Nominal canonical exposure | 10,000,000 |
| Actual canonical exposure | 10,006,223 |
| Completed optimizer updates | 305 |
| Completed master queues | 305 |
| Presentations | 136,755 |
| Complete prescribed saves | 13 |
| Complete heldout observations | 6 |

MEASURED RESULT: All native update identities, ordered D1 presentations, channels/phases, cumulative charges, actual-update denominators, master geometry and LRs match the frozen D1/U1 ledger. The fresh initialization fingerprint agrees with the qualified seed42 fingerprint. The complete output and all 13 checkpoint inventories reproduce their hashes, with no pending queue, charge or accumulated microbatch at any checkpoint. All six observation state identities match their complete checkpoints. Each heldout observation contains 2,984 cases; initialization and endpoint each retain separate 304-case TRAIN greedy and teacher-forced diagnostics. Six calibration receipts record 11,400 evaluations without training or checkpoint-selection use. Frozen D1/U1 geometry and evaluation/save endpoints agree across the B100 and C101 recipes; this does not assert equal exposure or presentations across D0 and D1.

| Observation | Completed update | Nominal exposure | Actual exposure |
|---|---:|---:|---:|
| Initialization | 0 | 0 | 0 |
| 1M | 31 | 1,000,000 | 1,016,836 |
| 3M | 92 | 3,000,000 | 3,017,745 |
| P0 end | 204 | 6,666,667 | 6,692,124 |
| P1 end | 285 | 9,333,334 | 9,349,783 |
| 10M endpoint | 305 | 10,000,000 | 10,006,223 |

| Measured time component | Seconds |
|---|---:|
| Complete attempt wall interval | 7276.738185 |
| Logged completed-update training intervals | 1551.013264 |
| Observation intervals | 5617.406249 |
| Checkpoint intervals | 56.308546 |

CALCULATION: The complete attempt interval is 2.021316 hours. Training, save and observation intervals are already included in that interval and are not added again. Scientific extent counts the fixed trajectory once. Exact device kernel time, electricity, depreciation and monetary price remain UNMEASURED or UNPRICED.

MEASURED RESULT: The original serial launcher advanced to `G2-C101-D1-U1-seed42-lr3e-4` after B100-D1-U1's completed attempt interval. The fourth start and complete update-zero checkpoint reproduce frozen recipe/campaign/ledger identities and payload hashes. Recipe 4's initialization evaluation is active; three prescribed outcomes are complete, four slots are consumed, and three recipes remain AUTHORIZED_UNSTARTED. All 47 frozen scientific source identities, scientific inputs, frontier hashes, qualification receipts, external artifact identities, seven original recipe hashes and the separate ByT5 schedule reproduce. External bound-volume identity, writable access and free-space policy pass.

FACT: Full scientific metric/gate reconstruction, factorial effects, full campaign accounting and the four post-campaign reports are UNRUN until all seven prescribed outcomes exist. D1-U8 remains the predeclared adequacy candidate in each scratch arm. This bounded execution report makes no viability, H1, final-population or paper-success claim. The full suite is UNRUN during active scientific acceleration; the last verified complete suite remains 505 passed with zero failures/skips. No final/sealed work or scientific treatment change occurs.

GENERATION_2_SCIENTIFIC_EXECUTION_IN_PROGRESS
