# Generation-2 B100-D0-U8 scientific execution

Date: 2026-10-08T03:19:34.642721+00:00

Reviewed execution evidence base: `568eeaf39a082ba9e82fd7117ff83a62faec2475`. Scientific launch source: `c3d6724b7838be62881f87f6505bd3e474b72849`. The published campaign freeze is `experiments/manifests/generation_2/execution-campaign-freeze.attempt01.json`.

MEASURED RESULT: `G2-B100-D0-U8-seed42-lr3e-4` completed attempt01 at the fixed endpoint, with no numerical replay or manual resume. The outcome is `experiments/manifests/generation_2/scientific-outcome-G2-B100-D0-U8-seed42-lr3e-4.attempt01.json`. Independent trajectory/artifact reconstruction passes in `scientific-recipe-independent-G2-B100-D0-U8-seed42-lr3e-4.attempt02.json` in the same directory; its paired review is `docs/reviews/G2_B100_D0_U8_EXECUTION_INDEPENDENT_REVIEW.md`.

| Training extent | Count |
|---|---:|
| Nominal canonical exposure | 10,000,000 |
| Actual canonical exposure | 10,007,223 |
| Completed optimizer updates | 2,440 |
| Completed master queues | 305 |
| Presentations | 134,591 |
| Complete prescribed saves | 13 |
| Complete heldout observations | 6 |

MEASURED RESULT: All logged native update identities, presentation order, cumulative charges, update denominators, subqueue geometry and LRs match the frozen D0/U8 ledger. The fresh initialization fingerprint matches the qualified seed42 fingerprint. The final artifact and all 13 checkpoint inventories reproduce their hashes; checkpoint metadata has no pending optimizer queue. Each scheduled heldout observation has 2,984 cases. The initialization and endpoint each retain separate 304-case TRAIN greedy and teacher-forced diagnostics. Six observations record 11,400 calibration evaluations, with no training use or checkpoint selection.

| Observation | Completed update | Nominal exposure | Actual exposure |
|---|---:|---:|---:|
| Initialization | 0 | 0 | 0 |
| 1M | 248 | 1,000,000 | 1,017,149 |
| 3M | 736 | 3,000,000 | 3,018,478 |
| P0 end | 1,632 | 6,666,667 | 6,693,230 |
| P1 end | 2,280 | 9,333,334 | 9,350,642 |
| 10M endpoint | 2,440 | 10,000,000 | 10,007,223 |

| Measured time component | Seconds |
|---|---:|
| Complete attempt wall interval | 10286.654194 |
| Logged completed-update training intervals | 2361.968268 |
| Observation intervals | 7590.863871 |
| Checkpoint intervals | 60.027967 |

CALCULATION: The complete attempt interval is 2.857404 hours. Training, save and observation intervals are components already included in that interval; do not add them again. Scientific extent counts the fixed trajectory once. Exact device kernel time, electricity, depreciation and local monetary price are UNMEASURED or UNPRICED.

FACT: The first bounded review attempt used an incorrect receipt-envelope equality check: save receipts include `io_timing`, while immutable COMPLETE inventories contain schema and file identities. Attempt01 is retained as a failed check. Attempt02 compares the immutable schema/files, independently reads all payload hashes, and keeps timing separate. No scientific artifact, source or treatment was repaired or changed.

FACT: The original serial launcher advanced to `G2-C101-D0-U8-seed42-lr3e-4` only after recipe 1 completed. Its start receipt and verified update-zero checkpoint are retained. Two slots are consumed, one outcome is complete, recipe 2 is running and five recipes remain AUTHORIZED_UNSTARTED. All 47 frozen scientific source identities, scientific inputs and frontier hashes reproduce. External volume identity, writable access and the free-space policy pass. No concurrent scientific accelerator job or final/sealed work is started.

FACT: Scientific gate reconstruction, factorial effects, full campaign accounting and the four post-campaign reports are UNRUN until all seven prescribed outcomes exist. D1-U8 remains the predeclared adequacy candidate in each scratch arm. This execution report makes no viability, H1, final-population or paper-success claim. The full suite is UNRUN during the active accelerator job; its last verified complete result remains 505 passed, zero failed/skipped.

MEASURED RESULT: Recipe 2 has now completed its initialization observation. Independent receipt `experiments/manifests/generation_2/scientific-observation-independent-G2-C101-D0-U8-seed42-lr3e-4.update00000.attempt01.json` reproduces all six payload hashes, 2,984 heldout cases and separate 304-case TRAIN greedy/forced diagnostics. The observation state matches its verified update-zero checkpoint; its 1,900 calibration evaluations are recorded without training or selection use. Scientific training continues in recipe 2.

GENERATION_2_SCIENTIFIC_EXECUTION_IN_PROGRESS
