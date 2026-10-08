# Independent Generation-2 C101-D0-U8 5M prefix review

Date: 2026-10-08T04:23:05.499619+00:00

Reviewed base: `95d47128e763c6924da1aa51d5c2b078c83336c2`. Evidence: `experiments/manifests/generation_2/scientific-progress-independent.attempt04.json`, its hash-bound private update snapshot and separate CPU audit code.

MEASURED RESULT: A CPU-only path reconstructs all 1,224 completed optimizer updates against the frozen D0/U8 geometry and ordered presentation ledger. Every update's charge, cumulative exposure, master/subqueue index, LR, denominators, presentation order and native consumption identities agree. This prefix contains 68,331 presentations and 5,019,821 actual canonical exposures after 153 completed master queues. The nominal 5M save boundary is 5,000,000. The saved checkpoint's complete payload inventory reproduces, with metadata recording step 1,224, committed exposure 5,019,821, an empty pending queue, zero pending charge and zero accumulated microbatches. This checkpoint verification does not assert a completed recipe or a new evaluation endpoint.

MEASURED RESULT: Three completed observations reproduce their immutable payload hashes and separate calibration-use receipts:

| Observation | Completed update | Nominal exposure | Actual exposure | Heldout cases |
|---|---:|---:|---:|---:|
| Initialization | 0 | 0 | 0 | 2,984 |
| 1M | 248 | 1,000,000 | 1,017,149 | 2,984 |
| 3M | 736 | 3,000,000 | 3,018,478 | 2,984 |

MEASURED RESULT: The initialization's six payloads, including separate 304-case TRAIN greedy and teacher-forced diagnostics, retain their independently verified identities. The three heldout observations record 5,700 calibration evaluations without training use or checkpoint selection. All 47 frozen scientific source identities, three scientific inputs, three frontier decision/amendment identities, 21 qualification receipts and 12 external artifact identities reproduce. Bound volume identity, writable access and the qualified free-space policy pass. The independent check reads completed data and does not run a model or alter the active process.

FACT: B100-D0-U8 is complete; C101-D0-U8 remains RUNNING; five recipes remain AUTHORIZED_UNSTARTED. There are two consumed scientific slots. No quality-based selection, stop or extension occurs. The other six prescribed outcomes, full scientific metric/gate analysis, factorial reconstruction and post-campaign reports are UNRUN. The complete test suite is UNRUN during active scientific acceleration; its last verified result remains 505 passed with zero failures/skips. No final/sealed work or scientific treatment change occurs.

PASS_INDEPENDENT_SCIENTIFIC_PREFIX_AND_COMPLETED_OBSERVATIONS
