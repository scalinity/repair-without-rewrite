# Independent Generation-2 B100-D1-U1 4M prefix review

Date: 2026-10-08T06:27:42.437415+00:00

Reviewed base: `ae3a0ef09e61a5c7d870cd3e09a236a4cb37625a`. Evidence: `experiments/manifests/generation_2/scientific-progress-independent.attempt05.json`, its hash-bound immutable update snapshot and separate CPU audit code.

MEASURED RESULT: All 122 completed optimizer updates independently match the frozen D1 presentation ledger and U1 geometry. Native presentation IDs, source/target/anchor identities, channels/phases, cumulative charges, denominators, optimizer/master indices, presentation order and LR agree. The prefix contains 55,355 presentations and 4,001,964 actual canonical exposures after 122 completed master queues, against the nominal 4M save boundary. Its complete update-122 checkpoint reproduces all payload hashes; metadata records step 122, committed exposure 4,001,964, an empty pending queue, zero pending charge and zero accumulated microbatches. This bounded check does not assert recipe completion or add an evaluation endpoint.

MEASURED RESULT: Three completed observations reproduce their immutable payload hashes, separate calibration receipts and state identities against the corresponding complete checkpoints:

| Observation | Completed update | Nominal exposure | Actual exposure | Heldout cases |
|---|---:|---:|---:|---:|
| Initialization | 0 | 0 | 0 | 2,984 |
| 1M | 31 | 1,000,000 | 1,016,836 | 2,984 |
| 3M | 92 | 3,000,000 | 3,017,745 | 2,984 |

MEASURED RESULT: Initialization preserves separate 304-case TRAIN greedy and teacher-forced diagnostics, outside heldout gates. The three observations record 5,700 calibration evaluations without training, sealed-reference or checkpoint-selection use. All 47 frozen scientific sources, three scientific inputs, three frontier decision/amendment identities, 21 qualification receipts, 12 external artifact identities, seven original recipe hashes and the versioned ByT5 binding reproduce. Bound-volume identity, writable access and qualified free-space policy pass. The independent path reads complete checkpoints and an immutable first-122-update snapshot while leaving the active scientific process undisturbed.

FACT: Two prescribed outcomes are complete; B100-D1-U1 remains RUNNING, three slots are consumed and four recipes remain AUTHORIZED_UNSTARTED. No quality-based selection, stop or extension occurs. The five remaining outcomes, full scientific metric/gate and factorial/accounting reconstruction, post-campaign reports and new complete suite are UNRUN. The last full suite remains 505 passed with zero failures/skips; it is not rerun during active acceleration. No final/sealed work or scientific treatment change occurs. D0 and D1 retain their separately frozen actual extents.

PASS_INDEPENDENT_SCIENTIFIC_PREFIX_AND_COMPLETED_OBSERVATIONS
