# Independent Generation-2 B100-D0-U8 P1 prefix review

Date: 2026-10-08T02:14:40.647388+00:00

Reviewed base: `3eba9115d1c9890c6ec95cbb2a831dbf6b43cfee`. Evidence: `experiments/manifests/generation_2/scientific-progress-independent.attempt03.json` and the hash-bound private update snapshot.

MEASURED RESULT: A CPU-only path reconstructs all 2,280 completed optimizer updates against the frozen D0/U8 update geometry and ordered presentation ledger. Every update's charge, cumulative exposure, master/subqueue index, LR, denominators, presentation order and native consumption identities agree. This covers 127,235 presentations and 9,350,642 actual canonical exposures after 285 completed master queues. The frozen P1 nominal boundary is 9,333,334; its prescribed completed state is update 2,280. The complete checkpoint's payload hashes reproduce, and metadata records step 2,280, committed exposure 9,350,642, no pending queue, zero pending charge and zero accumulated microbatches.

MEASURED RESULT: Four completed observations reproduce their immutable payload hashes and separate calibration-use receipts:

| Observation | Completed update | Nominal exposure | Actual exposure | Heldout cases |
|---|---:|---:|---:|---:|
| Initialization | 0 | 0 | 0 | 2,984 |
| 1M | 248 | 1,000,000 | 1,017,149 | 2,984 |
| 3M | 736 | 3,000,000 | 3,018,478 | 2,984 |
| P0 end | 1,632 | 6,666,667 | 6,693,230 | 2,984 |

MEASURED RESULT: Initialization retains separate 304-case TRAIN greedy and teacher-forced diagnostics. The four heldout observations record 7,600 calibration evaluations, with no training use or checkpoint selection. All 47 frozen scientific source identities, scientific-input identities and frontier decision/amendment hashes reproduce. Bound volume identity, writable access and the free-space policy pass.

FACT: Independent progress attempt02 correctly reconstructed the updates but mislabeled zero-based last master index 284 as the completed-master count. Attempt03 preserves that original, records the correction and binds the correct count of 285 to the frozen endpoint. No scientific result, treatment, launcher or model state changes.

FACT: Recipe 1 remains RUNNING in the prescribed P1 evaluation; six recipes remain AUTHORIZED_UNSTARTED. No quality-based selection, stop or extension occurs. Recipe completion, the remaining outcomes, complete scientific analysis and post-campaign interpretation are UNRUN. The full test suite is UNRUN during the active accelerator job; the last complete suite remains 505 passed, zero skipped/failed. No final/sealed work occurs.

PASS_INDEPENDENT_SCIENTIFIC_PREFIX_AND_COMPLETED_OBSERVATIONS
