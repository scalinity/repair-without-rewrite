# G2 ByT5 scientific adaptation

FACT: Recorded 2026-10-09T13:58:35.728134+00:00; reviewed execution source `9e737af0e5168e2b2b7a6d960274e2ded7d724be` on `codex/g2-execution`. This report does not identify its own future commit. Generation 2 remains DEVELOPMENT evidence.

FACT: Published prospective freeze `4fbb852f26b8b8cb6edd4433bf1446b41e1f59b1` precedes clean launch `c3d6724b7838be62881f87f6505bd3e474b72849`. The freeze remains unchanged: `experiments/manifests/generation_2/execution-campaign-freeze.attempt01.json`, SHA-256 `084be260a7f6797d9e138839fe56660c3ce47cb6d92d813c4c3a518b3344cb14`. All seven prescribed recipes completed in frozen serial order, one scientific attempt each, without numerical replay, rescue intervention or quality-based selection.

MEASURED RESULT: Registered result reconstruction `experiments/manifests/generation_2/scientific-results.attempt01.json` (SHA-256 `510e0efceec1127f38d524f8ca71a224cbaea59cd8206f5dc138889d9be74edd`) and separate independent reconstruction `experiments/manifests/generation_2/scientific-results-independent.attempt01.json` (SHA-256 `8f952fc01a96e2e8468c4ac65234de5922bc3aad1984155f1803aecc8d8b5cf7`) agree. The independent path verifies 42 complete heldout panels of 2,984 cases, canonical rescoring, separate edit distances/generated parsing, exact factorial fractions, shared bootstrap draws, endpoint-only gates and separate TRAIN diagnostics.

## Exact frozen recipe

FACT: `google/byt5-small`, pinned revision `68377bdc18a2ffec8a0533fef03b1c513a4dd49d`, 299,637,760 parameters; raw ASR source without a textual prefix. D1 TRAIN has 14,113 records, ten continuous complete passes, 141,130 total presentations and 35,283 optimizer updates. Batch four is continuous across pass boundaries; only the last update has two records. Seed42, constant LR3e-4, AdamW beta1=.9/beta2=.999/epsilon1e-8/decay.01/clip1, FP32 MPS, eager attention and CPU fallback disabled remain unchanged. Source/target byte+EOS capacity and greedy decode limit remain 512. No truncation, dropped record or pass-boundary flush occurred.

FACT: Original qualified recipe SHA-256 `cd74653ce9af7a155560884e1b34d1e936392ed9fce61558345b1d8ac442b5df` remains unchanged. The separately versioned four-state schedule and the verbatim frontier decision bind each observation; the completed training/checkpoint and observation reviews verify both crossing batches and final state.

## Nominal milestones and actual completed states

FACT: Labels and nominal/actual extent are exact. Quantitative axes use actual presentations; pass-equivalent progress is actual / 14,113. Intermediate states are not labelled as exactly 2.000 or 5.000 passes.

| Exact reporting label | Nominal passes | Nominal presentations | Completed update | Actual presentations | Signed offset | Actual pass-equivalent |
| --- | --- | --- | --- | --- | --- | --- |
| initialization | 0 | 0 | 0 | 0 | 0 | 0/14,113 |
| 2-pass nominal milestone — first completed update at/after boundary | 2 | 28,226 | 7,057 | 28,228 | +2 | 28228/14,113 |
| 5-pass nominal milestone — first completed update at/after boundary | 5 | 70,565 | 17,642 | 70,568 | +3 | 70568/14,113 |
| 10-pass exact endpoint | 10 | 141,130 | 35,283 | 141,130 | 0 | 141130/14,113 |

MEASURED RESULT: Update 7,057 retains crossing pass indices [1,1,2,2]; update 17,642 retains [4,5,5,5]. The entire training order, batch membership, gradients, LR/optimizer sequence and final endpoint preserve the qualified treatment. Offsets +2/+3 lie inside the fixed 141,130 presentations and add no unique exposure or optimizer steps.

## Failure-inclusive heldout population

MEASURED RESULT: Every heldout evaluation retains all 2,984 cases: 2,696 natural and 288 generated. Natural totals are 50,926 reference words and 1,413 RAW errors, RAW WER 2.774614%. The 52 source groups, 878 lexical-error and 1,818 lexical-zero natural cases remain fixed. CAL has 1,900 cases and HPO DEVELOPMENT 796; legacy108/new2588 and clean/other subsets remain separately reported in the receipt. These subsets overlap; do not sum them into new exposure. Corpus split names beginning with train describe heldout source provenance, not reuse as student TRAIN diagnostics.

FACT: Failure-inclusive counts retain invalid/capped outputs and generated structural failures. Completed-repair and introduced-error lower/upper values are scorer alignment bounds, separate from 95% source-group percentile intervals. A nonempty denominator is required. No failed row is dropped, regenerated or converted into a completed repair.

## Descriptive adaptation trajectory

MEASURED RESULT: All four observations exist and independently bind their saved completed state. Intermediate observations are descriptive only; no best checkpoint, LR, recipe or duration is selected. Exact full-panel output statuses are retained, including initialization invalid UTF8 and every capped generated output.

| Exact reporting label | Nominal presentations | Actual presentations | Update | Offset | Natural errors | Natural WER | Completed repair bounds | Introduced bounds | Natural invalid/capped | Generated decoder invalid/capped |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| initialization | 0 | 0 | 0 | 0 | 50,926 | 100.000000% | 0–0 | 49,648–49,652 | 2,696 | 288 |
| 2-pass nominal milestone — first completed update at/after boundary | 28,226 | 28,228 | 7,057 | +2 | 1,534 | 3.012214% | 84–84 | 205–205 | 1 | 69 |
| 5-pass nominal milestone — first completed update at/after boundary | 70,565 | 70,568 | 17,642 | +3 | 1,565 | 3.073086% | 105–105 | 257–257 | 1 | 171 |
| 10-pass exact endpoint | 141,130 | 141,130 | 35,283 | 0 | 1,650 | 3.239995% | 120–120 | 357–357 | 0 | 63 |



## Observation costs at actual states

MEASURED RESULT: Timings attach to actual completed updates/presentations; nominal milestones and signed offsets remain separate. Decode/scorer components are included inside observation wall time, which is included inside the physical recipe interval.

| Exact reporting label | Nominal presentations | Actual presentations | Update | Offset | All 2,984 statuses | Observation seconds | Decode component seconds | Scorer component seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| initialization | 0 | 0 | 0 | 0 | {"invalid_utf8": 2984} | 8525.970953 | 7901.264797 | 5.389383 |
| 2-pass nominal milestone — first completed update at/after boundary | 28,226 | 28,228 | 7,057 | +2 | {"capped": 70, "complete": 2914} | 7214.049868 | 5343.791777 | 11.141651 |
| 5-pass nominal milestone — first completed update at/after boundary | 70,565 | 70,568 | 17,642 | +3 | {"capped": 172, "complete": 2812} | 10059.125263 | 7636.503629 | 14.241679 |
| 10-pass exact endpoint | 141,130 | 141,130 | 35,283 | 0 | {"capped": 63, "complete": 2921} | 7074.588477 | 4916.474747 | 10.757864 |



## Exact ten-pass adequacy

MEASURED RESULT: Only update 35,283 at nominal/actual 141,130 presentations and offset 0 supplies adequacy. All 2,696 natural outputs complete; generated outputs contain 225 complete sequences and 63 retained capped sequences, with all 288 failing generated structural conformance. Generated repair is descriptive for ByT5 and is not an added adequacy gate.

| Frozen gate | Result |
| --- | --- |
| completed_natural_repair_lower_positive | PASS |
| completed_natural_repair_lower_support_at_least_two_groups | PASS |
| natural_WER_strictly_below_RAW | FAIL |
| prescribed_completion_resolved | PASS |

MEASURED RESULT: Natural WER is 1,650/50,926 = 3.239995%, versus RAW 1,413/50,926 = 2.774614%. The endpoint repairs 120 source errors with lower/upper bounds 120/120, introduces 357/357, and has lower-bound repair support in 37 source groups. It fails natural WER strictly below RAW and is not adequate under the frozen contract. CALCULATION: 1,413 - 120 + 357 = 1,650; net 237 more lexical errors than RAW. Descriptive 95% group-bootstrap WER interval: [2.782617, 3.756010] percent. This sampling interval is separate from scorer alignment bounds.

MEASURED RESULT: Source lexical identity is 2323/2,696, source byte identity 1102/2,696 and target lexical exactness 1676/2,696. All fixed natural subsets, source-correct preservation coverage and generated category/view counts are disclosed in the registered receipt; none alters adequacy.

## Budget and stop

MEASURED RESULT: Unique training extent is 141,130 presentations and 35,283 updates; full attempt wall time is 79862.099614 seconds. CALCULATION: 22.183917 hours. Logged training totals 21,143.834539 seconds and all four observation/save costs are inside the attempt interval and are not added again. Checkpoint weights and private heldout outputs remain outside Git with safe inventory hashes. No final/sealed training or inference, teacher/TTS data, extra pass, LR trial or rescue follows. Stop for frontier scientific interpretation.

FRONTIER_MODEL_REVIEW_REQUIRED
