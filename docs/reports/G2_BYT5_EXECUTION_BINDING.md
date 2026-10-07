# Generation-2 ByT5 execution observation binding

FACT: Recorded 2026-10-07; reviewed source `b1c565e341c1571fec15d4f918049c584246517b`. The complete frontier milestone decision was published alone at that source before affected implementation. `docs/reviews/PROSPECTIVE_AMENDMENTS.md` appends the owner-supplied normative wording unchanged. This step qualifies observation binding, not a scientific outcome or campaign freeze.

MEASURED RESULT: The pre-binding full suite passes 465 tests, zero failures/skips, in 42.591054583 seconds process wall. The post-binding full suite passes 477 tests, zero failures/skips, in 42.347051375 seconds. Receipts are `execution-binding-baseline-tests.attempt01.json` and `execution-binding-final-tests.attempt01.json` under `experiments/manifests/generation_2/`; their complete external logs are hash-bound. No baseline test file changes.

CALCULATION: `experiments/manifests/generation_2/byt5-execution-schedule.attempt01.json` binds exactly four observations:

| Nominal passes | Nominal presentations | Completed update | Actual presentations | Actual minus nominal | Exact label |
|---:|---:|---:|---:|---:|---|
| 0 | 0 | 0 | 0 | 0 | initialization |
| 2 | 28,226 | 7,057 | 28,228 | +2 | 2-pass nominal milestone — first completed update at/after boundary |
| 5 | 70,565 | 17,642 | 70,568 | +3 | 5-pass nominal milestone — first completed update at/after boundary |
| 10 | 141,130 | 35,283 | 141,130 | 0 | 10-pass exact endpoint |

FACT: Every state binds the published frontier decision identity/hash and original qualified recipe SHA-256 `cd74653ce9af7a155560884e1b34d1e936392ed9fce61558345b1d8ac442b5df`. The original recipe, training iterator and qualified model/training/scoring code remain unchanged. The new observation module does not initialize a model or modify training.

MEASURED RESULT: Twelve new regression cases check the exact counts/updates/offsets/labels, rejection of altered observations, and all 141,130 presentations in the unchanged one-shuffle ten-pass order. Both crossing batches retain pass indices `[1,1,2,2]` and `[4,5,5,5]`; all nonfinal batches remain four, the final batch remains two, and the stream retains 35,283 updates. The independent retained integer-enumeration path agrees and proves the preceding states are below each intermediate boundary; `execution-schedule-independent.attempt01.json` and `docs/reviews/G2_BYT5_EXECUTION_BINDING_INDEPENDENT_REVIEW.md` carry that separate check.

FACT: The intermediate observations are descriptive only. Endpoint-only adequacy remains at the exact ten-pass state. Progress axes use actual presentations, or actual presentations divided by 14,113; reporting preserves nominal counts separately. Save/evaluation charges attach to actual states. The +2/+3 offsets are already within the fixed stream and add no training charge.

FACT: All seven scientific recipes remain AUTHORIZED_UNSTARTED with zero slots consumed. Scientific execution orchestration and campaign-freeze publication remain pending. No final training, sealed inference, protocol freeze, teacher/TTS calls, cloud spending, production change or protected snapshot operation occurred.

G2_BYT5_EXECUTION_BINDING_QUALIFIED
