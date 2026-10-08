# Independent Generation-2 B100-D1-U8 P0 prefix review

Date: 2026-10-08T11:30:14.632493+00:00

Reviewed base: `75f78e89ba186e0a9019e15077d6db086612de3d`. Evidence: `experiments/manifests/generation_2/scientific-progress-independent.attempt08.json`; its separate CPU checker and immutable first-1,632-update snapshot are hash-bound in that receipt. The earlier 736-update 3M check is retained in `experiments/manifests/generation_2/scientific-progress-independent.attempt07.json`. The active serial job remains undisturbed.

MEASURED RESULT: All 1,632 completed U8 updates independently match the frozen D1 native presentation ledger and geometry. Ordered presentation IDs, source/target/anchor hashes, channels/phases, native consumption identities, cumulative charges, actual-update denominators, master/subqueue indices, optimizer steps and LRs reproduce. The verified prefix contains 92,507 presentations and 204 completed masters, with 6,692,124 actual canonical exposures against 6,666,667 nominal at P0 end. The immutable update-1,632 checkpoint reproduces both payload hashes and zero-pending queue/charge/accumulation metadata.

| Completed observation | Completed update | Nominal exposure | Actual exposure |
|---|---:|---:|---:|
| Initialization | 0 | 0 | 0 |
| 1M | 248 | 1,000,000 | 1,016,836 |
| 3M | 736 | 3,000,000 | 3,017,745 |
| P0 end | 1,632 | 6,666,667 | 6,692,124 |

MEASURED RESULT: Each of the four completed observations contains 2,984 heldout cases with unique IDs. All payload inventories and observation-to-checkpoint state identities reproduce. Initialization retains separate 304-case TRAIN greedy and forced diagnostics. Calibration receipts reproduce 7,600 evaluations without training use, sealed-reference use or recipe/checkpoint selection. Completed campaign observations at this cutoff record 53,200 calibration evaluations.

MEASURED RESULT: All 47 frozen scientific sources, three scientific inputs, three frontier decision/amendment identities, 21 qualification receipts, 12 external artifact identities, seven original recipe hashes and the separate ByT5 binding remain unchanged. Bound-volume identity/access/free-space checks pass before and after the 8.196414-second measured CPU check. The retained independent 3M check took 5.730288 measured seconds and passed.

FACT: Four prescribed outcomes are complete; recipe 5 continues and two recipes remain AUTHORIZED_UNSTARTED. This check verifies the immutable prefix and observations; recipe 5 remains incomplete. Full scientific metric/gate, factorial and campaign accounting analyses remain UNRUN until all seven prescribed outcomes exist. A new complete suite remains UNRUN during active scientific acceleration; the last complete suite is 505 passed, zero failures/skips, and nine later targeted CPU analysis tests pass. No quality selection, scientific treatment change, final run or sealed inference occurs.

PASS_INDEPENDENT_SCIENTIFIC_PREFIX_AND_COMPLETED_OBSERVATIONS
