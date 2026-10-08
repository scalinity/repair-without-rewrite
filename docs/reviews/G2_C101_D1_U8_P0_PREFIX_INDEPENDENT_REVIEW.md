# Independent Generation-2 C101-D1-U8 P0 prefix review

Date: 2026-10-08T13:40:36.015287+00:00

Reviewed base: `d979782f2540de68b22de33b2a6824281f3942b8`. Evidence: `experiments/manifests/generation_2/scientific-progress-independent.attempt09.json`, retained failed attempt10, and passing attempt11. The separate CPU checker sources, logs and immutable update snapshots are hash-bound in those receipts. The active serial job remains undisturbed.

MEASURED RESULT: The retained 6M check reconstructs 1,464 completed U8 updates, 183 masters, 82,998 presentations and 6,003,105 actual canonical exposures against 6M nominal in 6.371055 measured CPU seconds. The subsequent P0 check reconstructs all 1,632 completed updates against the frozen D1 native presentation ledger and geometry. Ordered presentation IDs, source/target/anchor hashes, channels/phases, native consumption identities, cumulative charges, actual-update denominators, master/subqueue identities, optimizer steps and LRs reproduce. The verified P0 prefix contains 92,507 presentations and 204 completed masters, with 6,692,124 actual canonical exposures against 6,666,667 nominal. The immutable update-1,632 checkpoint reproduces both payload hashes and zero-pending queue/charge/accumulation metadata.

| Completed observation | Completed update | Nominal exposure | Actual exposure |
|---|---:|---:|---:|
| Initialization | 0 | 0 | 0 |
| 1M | 248 | 1,000,000 | 1,016,836 |
| 3M | 736 | 3,000,000 | 3,017,745 |
| P0 | 1,632 | 6,666,667 | 6,692,124 |

MEASURED RESULT: Each of the four completed observations contains 2,984 heldout cases with unique IDs. All payload inventories and observation-to-checkpoint state identities reproduce. Initialization retains separate 304-case TRAIN greedy and forced diagnostics. Calibration receipts reproduce 7,600 evaluations without training use, sealed-reference use or recipe/checkpoint selection. Completed campaign observations at this cutoff record 64,600 calibration evaluations.

FACT: Independent attempt10 failed before executing scientific checks because its invocation omitted the repository root from the Python import path. Its source, failed log and failure receipt remain preserved. Attempt11 supplies that path and passes without any scientific source, artifact or process change.

MEASURED RESULT: All 47 frozen scientific sources, three scientific inputs, three frontier decision/amendment identities, 21 qualification receipts, 12 external artifact identities, seven original recipe hashes and the separate ByT5 binding remain unchanged. Bound-volume identity/access/free-space checks pass before and after the 6.766403-second measured P0 CPU check.

FACT: Five prescribed outcomes are complete; recipe 6 continues and ByT5 remains AUTHORIZED_UNSTARTED. This check verifies the immutable prefix and observations; recipe 6 completion remains UNRUN. Full scientific metric/gate, factorial and campaign accounting analyses remain UNRUN until all seven outcomes exist. A new complete suite remains UNRUN during active scientific acceleration; the last complete suite is 505 passed, zero failures/skips, and nine later targeted CPU analysis tests pass. No quality selection, scientific treatment change, final run or sealed inference occurs.

PASS_INDEPENDENT_SCIENTIFIC_PREFIX_AND_COMPLETED_OBSERVATIONS
