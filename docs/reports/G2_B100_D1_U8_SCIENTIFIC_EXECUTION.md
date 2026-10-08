# Generation-2 B100-D1-U8 scientific execution

Date: 2026-10-08T12:38:04.308780+00:00

Reviewed execution evidence base: `17cb443d264584312f147c6e79e83db8f78b4240`. Scientific launch source: `38c1a4f6d6ce1664207f1ffb165f739cb44fc928`. The published campaign freeze is `experiments/manifests/generation_2/execution-campaign-freeze.attempt01.json`.

MEASURED RESULT: `G2-B100-D1-U8-seed42-lr3e-4` completed attempt01 at the fixed endpoint without numerical replay or manual resume. Its outcome is `experiments/manifests/generation_2/scientific-outcome-G2-B100-D1-U8-seed42-lr3e-4.attempt01.json`. Independent completed trajectory/artifact reconstruction passes in `experiments/manifests/generation_2/scientific-recipe-independent-G2-B100-D1-U8-seed42-lr3e-4.attempt01.json`; paired review is `docs/reviews/G2_B100_D1_U8_EXECUTION_INDEPENDENT_REVIEW.md`.

| Training extent | Count |
|---|---:|
| Nominal canonical exposure | 10,000,000 |
| Actual canonical exposure | 10,006,223 |
| Completed optimizer updates | 2,440 |
| Completed master queues | 305 |
| Presentations | 136,755 |
| Complete prescribed saves | 13 |
| Complete heldout observations | 6 |

MEASURED RESULT: All native update identities, ordered D1 presentations, channels/phases, cumulative charges, actual-update denominators, master/subqueue geometry and LRs match the frozen D1/U8 ledger. The fresh initialization fingerprint agrees with the qualified seed42 fingerprint. The complete output and all 13 checkpoint inventories reproduce their hashes, with no pending queue, charge or accumulated microbatch at any checkpoint. All six observation state identities match their complete checkpoints. Each heldout observation contains 2,984 cases; initialization and endpoint each retain separate 304-case TRAIN greedy and teacher-forced diagnostics. Six calibration receipts record 11,400 evaluations without training or checkpoint-selection use. B100 D1/U1 and D1/U8 retain the shared master geometry, presentation order and extent; U8 retains its eight qualified updates per master. The next C101 D1/U8 recipe binds the same geometry and save/evaluation endpoints. This does not assert equal exposure or presentations across D0 and D1.

| Observation | Completed update | Nominal exposure | Actual exposure |
|---|---:|---:|---:|
| Initialization | 0 | 0 | 0 |
| 1M | 248 | 1,000,000 | 1,016,836 |
| 3M | 736 | 3,000,000 | 3,017,745 |
| P0 end | 1,632 | 6,666,667 | 6,692,124 |
| P1 end | 2,280 | 9,333,334 | 9,349,783 |
| 10M endpoint | 2,440 | 10,000,000 | 10,006,223 |

| Measured time component | Seconds |
|---|---:|
| Complete attempt wall interval | 8631.517741 |
| Logged completed-update training intervals | 1897.213684 |
| Observation intervals | 6450.914888 |
| Checkpoint intervals | 54.485050 |

CALCULATION: The complete attempt interval is 2.397644 hours. Training, save and observation intervals are already included in that interval and are not added again. Scientific extent counts the fixed trajectory once. Exact device kernel time, electricity, depreciation and monetary price remain UNMEASURED or UNPRICED.

MEASURED RESULT: The original serial launcher advanced to `G2-C101-D1-U8-seed42-lr3e-4` after B100-D1-U8's completed attempt interval. The sixth start and complete update-zero checkpoint reproduce frozen recipe/campaign/ledger identities and payload hashes. Recipe 6's initialization observation is complete and training is active; five prescribed outcomes are complete, six slots are consumed, and ByT5 remains AUTHORIZED_UNSTARTED. The separate check `experiments/manifests/generation_2/scientific-observation-independent-G2-C101-D1-U8-seed42-lr3e-4.update00000.attempt01.json` verifies its 2,984 unique heldout cases, checkpoint state and payload inventories, separate 304-case TRAIN greedy/forced diagnostics, and 1,900 calibration evaluations without training or selection use. All 47 frozen scientific source identities, scientific inputs, frontier hashes, qualification receipts, external artifact identities, seven original recipe hashes and the separate ByT5 schedule reproduce. External bound-volume identity, writable access and free-space policy pass.

FACT: Full scientific metric/gate reconstruction, factorial effects, full campaign accounting and the four post-campaign reports are UNRUN until all seven prescribed outcomes exist. D1-U8 remains the predeclared adequacy candidate in each scratch arm. This bounded execution report makes no viability, H1, final-population or paper-success claim. The full suite is UNRUN during active scientific acceleration; the last verified complete suite remains 505 passed with zero failures/skips, and nine later targeted CPU analysis tests pass. No final/sealed work or scientific treatment change occurs.

GENERATION_2_SCIENTIFIC_EXECUTION_IN_PROGRESS
