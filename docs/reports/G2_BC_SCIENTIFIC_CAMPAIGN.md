# G2 B/C scientific campaign

FACT: Recorded 2026-10-09T13:58:35.728134+00:00; reviewed execution source `9e737af0e5168e2b2b7a6d960274e2ded7d724be` on `codex/g2-execution`. This report does not identify its own future commit. Generation 2 remains DEVELOPMENT evidence.

FACT: Published prospective freeze `4fbb852f26b8b8cb6edd4433bf1446b41e1f59b1` precedes clean launch `c3d6724b7838be62881f87f6505bd3e474b72849`. The freeze remains unchanged: `experiments/manifests/generation_2/execution-campaign-freeze.attempt01.json`, SHA-256 `084be260a7f6797d9e138839fe56660c3ce47cb6d92d813c4c3a518b3344cb14`. All seven prescribed recipes completed in frozen serial order, one scientific attempt each, without numerical replay, rescue intervention or quality-based selection.

MEASURED RESULT: Registered result reconstruction `experiments/manifests/generation_2/scientific-results.attempt01.json` (SHA-256 `510e0efceec1127f38d524f8ca71a224cbaea59cd8206f5dc138889d9be74edd`) and separate independent reconstruction `experiments/manifests/generation_2/scientific-results-independent.attempt01.json` (SHA-256 `8f952fc01a96e2e8468c4ac65234de5922bc3aad1984155f1803aecc8d8b5cf7`) agree. The independent path verifies 42 complete heldout panels of 2,984 cases, canonical rescoring, separate edit distances/generated parsing, exact factorial fractions, shared bootstrap draws, endpoint-only gates and separate TRAIN diagnostics.

## Fixed campaign and populations

FACT: B100 remains 100,686,336 parameters and C101 101,081,859. D0 is 1,024 original natural pairs; D1 is 14,113 qualified natural pairs. Preserve seed42, 15/15/20/10/40 allocation, P0/P1/P2, fixed peak LR 3e-4 and qualified cosine schedule, AdamW, precision, B16/C4 microbatches, 10M nominal canonical exposure excluding PAD, and exact U1/U8 optimizer geometry. The presentation ledger is identical within each D across arms and update regimes; D0 and D1 actual endpoint overshoots differ. Archived D0-U1 G1 3e-4 controls are rescored on the expanded panel without retraining.

MEASURED RESULT: Every heldout evaluation retains all 2,984 cases: 2,696 natural and 288 generated. Natural totals are 50,926 reference words and 1,413 RAW errors, RAW WER 2.774614%. The 52 source groups, 878 lexical-error and 1,818 lexical-zero natural cases remain fixed. CAL has 1,900 cases and HPO DEVELOPMENT 796; legacy108/new2588 and clean/other subsets remain separately reported in the receipt. These subsets overlap; do not sum them into new exposure. Corpus split names beginning with train describe heldout source provenance, not reuse as student TRAIN diagnostics.

FACT: Failure-inclusive counts retain invalid/capped outputs and generated structural failures. Completed-repair and introduced-error lower/upper values are scorer alignment bounds, separate from 95% source-group percentile intervals. A nonempty denominator is required. No failed row is dropped, regenerated or converted into a completed repair.

## Exact prescribed endpoint results

MEASURED RESULT: Counts below use all 2,696 natural and 288 generated cases at the prescribed final optimizer state. Generated repair counts require complete, structurally valid genuine required repair.

| Recipe | Natural errors | WER | Completed repair bounds | Introduced bounds | Repair groups lower | Natural invalid/capped | Generated genuine repair cases | Frozen viability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B100-D0-U8 | 63,344 | 124.384401% | 66–69 | 61,997–62,000 | 28 | 0 | 0 | FAIL |
| C101-D0-U8 | 3,173 | 6.230609% | 9–9 | 1,769–1,769 | 7 | 0 | 63 | FAIL |
| B100-D1-U1 | 56,572 | 111.086675% | 85–88 | 55,244–55,247 | 35 | 0 | 0 | FAIL |
| C101-D1-U1 | 5,484 | 10.768566% | 14–14 | 4,098–4,098 | 11 | 110 | 66 | FAIL |
| B100-D1-U8 | 16,997 | 33.375879% | 44–45 | 15,628–15,629 | 22 | 0 | 0 | FAIL |
| C101-D1-U8 | 4,095 | 8.041079% | 18–18 | 2,702–2,702 | 11 | 26 | 23 | FAIL |



## Frozen endpoint gates

FACT: All five gates must pass. Exact machine keys, truth values and endpoint bindings are preserved in the registered receipt. D1-U8 is the predeclared joint-intervention candidate in each arm; other cells do not form a selection menu.

| Recipe | completed_natural_repair_lower_positive | completed_natural_repair_lower_support_at_least_two_groups | generated_genuine_required_repair_completed | natural_WER_strictly_below_RAW | prescribed_completion_resolved |
| --- | --- | --- | --- | --- | --- |
| B100-D0-U8 | PASS | PASS | FAIL | FAIL | PASS |
| C101-D0-U8 | PASS | PASS | PASS | FAIL | PASS |
| B100-D1-U1 | PASS | PASS | FAIL | FAIL | PASS |
| C101-D1-U1 | PASS | PASS | PASS | FAIL | PASS |
| B100-D1-U8 | PASS | PASS | FAIL | FAIL | PASS |
| C101-D1-U8 | PASS | PASS | PASS | FAIL | PASS |

MEASURED RESULT: Every B/C endpoint fails natural WER strictly below RAW. All B100 endpoints also fail genuine generated required repair. Both scratch D1-U8 candidates fail. No subjective winning cell or LR is selected.

## Generated heldout outputs

MEASURED RESULT: Generated decoder completion and required-repair conformance are different counts; incomplete/invalid/structurally wrong cases remain in all 288 denominators.

| Recipe | Decoder complete / 288 | Decoder invalid/capped | Structure invalid | Genuine repaired fields | Genuine repair cases | Whole-case conformance | Mixed success |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B100-D0-U8 | 288 | 0 | 288 | 0 | 0 | 0 | 0 |
| C101-D0-U8 | 288 | 0 | 32 | 69 | 63 | 138 | 36 |
| B100-D1-U1 | 287 | 1 | 288 | 0 | 0 | 0 | 0 |
| C101-D1-U1 | 288 | 0 | 28 | 81 | 66 | 140 | 29 |
| B100-D1-U8 | 225 | 63 | 288 | 0 | 0 | 0 | 0 |
| C101-D1-U8 | 288 | 0 | 42 | 27 | 23 | 108 | 8 |



## Descriptive adaptation observations

FACT: Initialization and all five post-initialization observations are retained. Quantitative progress uses actual canonical exposure. Only prescribed final endpoints enter adequacy; no intermediate selection or quality-based stopping occurred.

| Recipe | Nominal canonical exposure | Actual canonical exposure | Completed update | Natural WER | Completed repair bounds | Introduced bounds | Natural invalid/capped |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B100-D0-U8 | 0 | 0 | 0 | 1196.066842% | 0–0 | 607,750–607,754 | 2,696 |
| B100-D0-U8 | 1,000,000 | 1,017,149 | 248 | 364.124416% | 47–51 | 184,092–184,096 | 836 |
| B100-D0-U8 | 3,000,000 | 3,018,478 | 736 | 119.318226% | 72–74 | 59,423–59,425 | 0 |
| B100-D0-U8 | 6,666,667 | 6,693,230 | 1,632 | 120.221498% | 65–68 | 59,876–59,879 | 1 |
| B100-D0-U8 | 9,333,334 | 9,350,642 | 2,280 | 123.748184% | 58–61 | 61,665–61,668 | 0 |
| B100-D0-U8 | 10,000,000 | 10,007,223 | 2,440 | 124.384401% | 66–69 | 61,997–62,000 | 0 |
| C101-D0-U8 | 0 | 0 | 0 | 86.857401% | 0–0 | 42,935–42,939 | 2,401 |
| C101-D0-U8 | 1,000,000 | 1,017,149 | 248 | 2.792287% | 0–0 | 9–9 | 0 |
| C101-D0-U8 | 3,000,000 | 3,018,478 | 736 | 3.161450% | 1–1 | 198–198 | 1 |
| C101-D0-U8 | 6,666,667 | 6,693,230 | 1,632 | 4.318030% | 6–6 | 792–792 | 0 |
| C101-D0-U8 | 9,333,334 | 9,350,642 | 2,280 | 4.999411% | 8–8 | 1,141–1,141 | 1 |
| C101-D0-U8 | 10,000,000 | 10,007,223 | 2,440 | 6.230609% | 9–9 | 1,769–1,769 | 0 |
| B100-D1-U1 | 0 | 0 | 0 | 1196.066842% | 0–0 | 607,750–607,754 | 2,696 |
| B100-D1-U1 | 1,000,000 | 1,016,836 | 31 | 98.505675% | 136–140 | 48,888–48,892 | 0 |
| B100-D1-U1 | 3,000,000 | 3,017,745 | 92 | 104.443703% | 98–100 | 51,874–51,876 | 1 |
| B100-D1-U1 | 6,666,667 | 6,692,124 | 204 | 120.824333% | 98–99 | 60,219–60,220 | 9 |
| B100-D1-U1 | 9,333,334 | 9,349,783 | 285 | 110.393512% | 88–90 | 54,897–54,899 | 6 |
| B100-D1-U1 | 10,000,000 | 10,006,223 | 305 | 111.086675% | 85–88 | 55,244–55,247 | 0 |
| C101-D1-U1 | 0 | 0 | 0 | 86.857401% | 0–0 | 42,935–42,939 | 2,401 |
| C101-D1-U1 | 1,000,000 | 1,016,836 | 31 | 2.774614% | 0–0 | 0–0 | 0 |
| C101-D1-U1 | 3,000,000 | 3,017,745 | 92 | 2.774614% | 0–0 | 0–0 | 0 |
| C101-D1-U1 | 6,666,667 | 6,692,124 | 204 | 2.774614% | 0–0 | 0–0 | 0 |
| C101-D1-U1 | 9,333,334 | 9,349,783 | 285 | 10.872639% | 18–18 | 4,152–4,152 | 109 |
| C101-D1-U1 | 10,000,000 | 10,006,223 | 305 | 10.768566% | 14–14 | 4,098–4,098 | 110 |
| B100-D1-U8 | 0 | 0 | 0 | 1196.066842% | 0–0 | 607,750–607,754 | 2,696 |
| B100-D1-U8 | 1,000,000 | 1,016,836 | 248 | 191.585830% | 87–90 | 96,259–96,263 | 660 |
| B100-D1-U8 | 3,000,000 | 3,017,745 | 736 | 103.200723% | 88–92 | 51,234–51,238 | 63 |
| B100-D1-U8 | 6,666,667 | 6,692,124 | 1,632 | 46.754114% | 47–47 | 22,444–22,444 | 6 |
| B100-D1-U8 | 9,333,334 | 9,349,783 | 2,280 | 36.071948% | 45–46 | 17,002–17,003 | 0 |
| B100-D1-U8 | 10,000,000 | 10,006,223 | 2,440 | 33.375879% | 44–45 | 15,628–15,629 | 0 |
| C101-D1-U8 | 0 | 0 | 0 | 86.857401% | 0–0 | 42,935–42,939 | 2,401 |
| C101-D1-U8 | 1,000,000 | 1,016,836 | 248 | 2.774614% | 0–0 | 0–0 | 0 |
| C101-D1-U8 | 3,000,000 | 3,017,745 | 736 | 2.774614% | 0–0 | 0–0 | 0 |
| C101-D1-U8 | 6,666,667 | 6,692,124 | 1,632 | 3.481522% | 2–2 | 362–362 | 1 |
| C101-D1-U8 | 9,333,334 | 9,349,783 | 2,280 | 6.267918% | 10–10 | 1,790–1,790 | 6 |
| C101-D1-U8 | 10,000,000 | 10,006,223 | 2,440 | 8.041079% | 18–18 | 2,702–2,702 | 26 |



## Heldout copying and exactness

MEASURED RESULT: These descriptive natural counts use the same 2,696 cases, without changing gates.

| Recipe | Source byte identity | Source lexical identity | Target byte exact | Target lexical exact |
| --- | --- | --- | --- | --- |
| B100-D0-U8 | 0 | 0 | 0 | 0 |
| C101-D0-U8 | 2,056 | 2,127 | 463 | 1,431 |
| B100-D1-U1 | 0 | 0 | 0 | 0 |
| C101-D1-U1 | 2,149 | 2,149 | 541 | 1,504 |
| B100-D1-U8 | 285 | 288 | 71 | 218 |
| C101-D1-U8 | 2,179 | 2,193 | 540 | 1,530 |



## TRAIN diagnostics remain separate

MEASURED RESULT: Each data condition freezes 304 diagnostic cases: 64 lexical-error, 64 lexical-zero, 128 reference-as-source identity views and 48 generated TRAIN views. Every B/C recipe evaluates greedy outputs and teacher-forced losses at initialization and endpoint, producing 12 independently rescored diagnostic states. Identity outputs and generated TRAIN repair do not count toward heldout gates. The receipt publishes each generated category/cell/view and each teacher-forced component with coverage, denominators, mean case loss and denominator-weighted loss. Unavailable components remain unavailable; losses are not compared as a common B/C objective.

| Recipe/update | TRAIN stratum | Cases | Invalid/capped | Source lexical identity | Target lexical exact | Completed repair bounds | Introduced bounds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B100-D0-U8/update0 | natural_lexical_error | 64 | 64 | 0 | 0 | 0–0 | 13,041–13,041 |
| B100-D0-U8/update0 | natural_lexical_error/identity | 64 | 64 | 0 | 0 | 0–0 | 12,304–12,304 |
| B100-D0-U8/update0 | natural_lexical_zero | 64 | 64 | 0 | 0 | 0–0 | 15,528–15,528 |
| B100-D0-U8/update0 | natural_lexical_zero/identity | 64 | 64 | 0 | 0 | 0–0 | 14,511–14,511 |
| B100-D0-U8/update2440 | natural_lexical_error | 64 | 0 | 0 | 64 | 113–113 | 0–0 |
| B100-D0-U8/update2440 | natural_lexical_error/identity | 64 | 0 | 64 | 64 | 0–0 | 0–0 |
| B100-D0-U8/update2440 | natural_lexical_zero | 64 | 0 | 64 | 64 | 0–0 | 0–0 |
| B100-D0-U8/update2440 | natural_lexical_zero/identity | 64 | 0 | 64 | 64 | 0–0 | 0–0 |
| B100-D1-U1/update0 | natural_lexical_error | 64 | 64 | 0 | 0 | 0–0 | 17,670–17,670 |
| B100-D1-U1/update0 | natural_lexical_error/identity | 64 | 64 | 0 | 0 | 0–0 | 15,632–15,632 |
| B100-D1-U1/update0 | natural_lexical_zero | 64 | 64 | 0 | 0 | 0–0 | 15,929–15,929 |
| B100-D1-U1/update0 | natural_lexical_zero/identity | 64 | 64 | 0 | 0 | 0–0 | 17,223–17,223 |
| B100-D1-U1/update305 | natural_lexical_error | 64 | 0 | 0 | 0 | 13–13 | 1,568–1,568 |
| B100-D1-U1/update305 | natural_lexical_error/identity | 64 | 0 | 0 | 0 | 0–0 | 1,627–1,627 |
| B100-D1-U1/update305 | natural_lexical_zero | 64 | 0 | 0 | 0 | 0–0 | 1,477–1,477 |
| B100-D1-U1/update305 | natural_lexical_zero/identity | 64 | 0 | 0 | 0 | 0–0 | 1,415–1,415 |
| B100-D1-U8/update0 | natural_lexical_error | 64 | 64 | 0 | 0 | 0–0 | 17,670–17,670 |
| B100-D1-U8/update0 | natural_lexical_error/identity | 64 | 64 | 0 | 0 | 0–0 | 15,632–15,632 |
| B100-D1-U8/update0 | natural_lexical_zero | 64 | 64 | 0 | 0 | 0–0 | 15,929–15,929 |
| B100-D1-U8/update0 | natural_lexical_zero/identity | 64 | 64 | 0 | 0 | 0–0 | 17,223–17,223 |
| B100-D1-U8/update2440 | natural_lexical_error | 64 | 0 | 4 | 0 | 4–4 | 428–428 |
| B100-D1-U8/update2440 | natural_lexical_error/identity | 64 | 0 | 4 | 4 | 0–0 | 437–437 |
| B100-D1-U8/update2440 | natural_lexical_zero | 64 | 0 | 8 | 8 | 0–0 | 368–368 |
| B100-D1-U8/update2440 | natural_lexical_zero/identity | 64 | 0 | 6 | 6 | 0–0 | 354–354 |
| C101-D0-U8/update0 | natural_lexical_error | 64 | 58 | 6 | 0 | 0–0 | 1,272–1,272 |
| C101-D0-U8/update0 | natural_lexical_error/identity | 64 | 55 | 9 | 9 | 0–0 | 1,241–1,241 |
| C101-D0-U8/update0 | natural_lexical_zero | 64 | 60 | 4 | 4 | 0–0 | 1,354–1,354 |
| C101-D0-U8/update0 | natural_lexical_zero/identity | 64 | 58 | 6 | 6 | 0–0 | 1,307–1,307 |
| C101-D0-U8/update2440 | natural_lexical_error | 64 | 0 | 1 | 25 | 56–56 | 114–114 |
| C101-D0-U8/update2440 | natural_lexical_error/identity | 64 | 0 | 64 | 64 | 0–0 | 0–0 |
| C101-D0-U8/update2440 | natural_lexical_zero | 64 | 0 | 44 | 44 | 0–0 | 73–73 |
| C101-D0-U8/update2440 | natural_lexical_zero/identity | 64 | 0 | 64 | 64 | 0–0 | 0–0 |
| C101-D1-U1/update0 | natural_lexical_error | 64 | 57 | 7 | 0 | 0–0 | 1,262–1,262 |
| C101-D1-U1/update0 | natural_lexical_error/identity | 64 | 49 | 15 | 15 | 0–0 | 1,122–1,122 |
| C101-D1-U1/update0 | natural_lexical_zero | 64 | 60 | 4 | 4 | 0–0 | 1,165–1,165 |
| C101-D1-U1/update0 | natural_lexical_zero/identity | 64 | 58 | 6 | 6 | 0–0 | 1,133–1,133 |
| C101-D1-U1/update305 | natural_lexical_error | 64 | 3 | 47 | 0 | 0–0 | 121–121 |
| C101-D1-U1/update305 | natural_lexical_error/identity | 64 | 1 | 57 | 57 | 0–0 | 65–65 |
| C101-D1-U1/update305 | natural_lexical_zero | 64 | 3 | 54 | 54 | 0–0 | 115–115 |
| C101-D1-U1/update305 | natural_lexical_zero/identity | 64 | 0 | 59 | 59 | 0–0 | 21–21 |
| C101-D1-U8/update0 | natural_lexical_error | 64 | 57 | 7 | 0 | 0–0 | 1,262–1,262 |
| C101-D1-U8/update0 | natural_lexical_error/identity | 64 | 49 | 15 | 15 | 0–0 | 1,122–1,122 |
| C101-D1-U8/update0 | natural_lexical_zero | 64 | 60 | 4 | 4 | 0–0 | 1,165–1,165 |
| C101-D1-U8/update0 | natural_lexical_zero/identity | 64 | 58 | 6 | 6 | 0–0 | 1,133–1,133 |
| C101-D1-U8/update2440 | natural_lexical_error | 64 | 0 | 52 | 0 | 0–0 | 60–60 |
| C101-D1-U8/update2440 | natural_lexical_error/identity | 64 | 0 | 58 | 58 | 0–0 | 29–29 |
| C101-D1-U8/update2440 | natural_lexical_zero | 64 | 1 | 57 | 57 | 0–0 | 58–58 |
| C101-D1-U8/update2440 | natural_lexical_zero/identity | 64 | 0 | 60 | 60 | 0–0 | 15–15 |



## Exposure and native cost

MEASURED RESULT: Separate ledger reconstruction verifies every completed optimizer update, presentation identity, actual denominators, LR/phase clocks, all 82 campaign checkpoints and 40 observations. Cost source: `scientific-accounting-independent.attempt01.json`; review `docs/reviews/G2_SCIENTIFIC_ACCOUNTING_INDEPENDENT_REVIEW.md`.

| Recipe | Unique updates | Unique presentations | Actual canonical exposure | Attempt wall seconds MEASURED |
| --- | --- | --- | --- | --- |
| B100-D0-U8 | 2,440 | 134,591 | 10,007,223 | 10286.654194 |
| C101-D0-U8 | 2,440 | 134,591 | 10,007,223 | 9010.581726 |
| B100-D1-U1 | 305 | 136,755 | 10,006,223 | 7276.738185 |
| C101-D1-U1 | 305 | 136,755 | 10,006,223 | 8864.873318 |
| B100-D1-U8 | 2,440 | 136,755 | 10,006,223 | 8631.517741 |
| C101-D1-U8 | 2,440 | 136,755 | 10,006,223 | 8189.656452 |

FACT: Checkpoint/observation/training component times are already inside attempt wall time and are not added again. Numerical failed/replay work would be charged physically once without enlarging unique extent; no such scientific attempt occurred. Failed CPU checks remain retained separately. Electricity, depreciation and local monetary price are UNPRICED; device kernel time and all-in operational span are UNMEASURED here.

## Development interpretation

MEASURED RESULT: Both predeclared scratch D1-U8 candidates fail frozen viability. This campaign supplies diagnostic DEVELOPMENT evidence and descriptive intervention contrasts. It does not establish H1, final-population superiority, architecture incapability or paper success. No final seeds, sealed inference, 150M training or protocol freeze occurred. Stop for frontier interpretation; no unregistered rescue follows.

FRONTIER_MODEL_REVIEW_REQUIRED
