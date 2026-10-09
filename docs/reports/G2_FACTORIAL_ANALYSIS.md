# G2 factorial analysis

FACT: Recorded 2026-10-09T13:58:35.728134+00:00; reviewed execution source `9e737af0e5168e2b2b7a6d960274e2ded7d724be` on `codex/g2-execution`. This report does not identify its own future commit. Generation 2 remains DEVELOPMENT evidence.

FACT: Published prospective freeze `4fbb852f26b8b8cb6edd4433bf1446b41e1f59b1` precedes clean launch `c3d6724b7838be62881f87f6505bd3e474b72849`. The freeze remains unchanged: `experiments/manifests/generation_2/execution-campaign-freeze.attempt01.json`, SHA-256 `084be260a7f6797d9e138839fe56660c3ce47cb6d92d813c4c3a518b3344cb14`. All seven prescribed recipes completed in frozen serial order, one scientific attempt each, without numerical replay, rescue intervention or quality-based selection.

MEASURED RESULT: Registered result reconstruction `experiments/manifests/generation_2/scientific-results.attempt01.json` (SHA-256 `510e0efceec1127f38d524f8ca71a224cbaea59cd8206f5dc138889d9be74edd`) and separate independent reconstruction `experiments/manifests/generation_2/scientific-results-independent.attempt01.json` (SHA-256 `8f952fc01a96e2e8468c4ac65234de5922bc3aad1984155f1803aecc8d8b5cf7`) agree. The independent path verifies 42 complete heldout panels of 2,984 cases, canonical rescoring, separate edit distances/generated parsing, exact factorial fractions, shared bootstrap draws, endpoint-only gates and separate TRAIN diagnostics.

## Registered contrast and uncertainty contract

FACT: B100 remains 100,686,336 parameters and C101 101,081,859. D0 is 1,024 original natural pairs; D1 is 14,113 qualified natural pairs. Preserve seed42, 15/15/20/10/40 allocation, P0/P1/P2, fixed peak LR 3e-4 and qualified cosine schedule, AdamW, precision, B16/C4 microbatches, 10M nominal canonical exposure excluding PAD, and exact U1/U8 optimizer geometry. The presentation ledger is identical within each D across arms and update regimes; D0 and D1 actual endpoint overshoots differ. Archived D0-U1 G1 3e-4 controls are rescored on the expanded panel without retraining.

MEASURED RESULT: Every heldout evaluation retains all 2,984 cases: 2,696 natural and 288 generated. Natural totals are 50,926 reference words and 1,413 RAW errors, RAW WER 2.774614%. The 52 source groups, 878 lexical-error and 1,818 lexical-zero natural cases remain fixed. CAL has 1,900 cases and HPO DEVELOPMENT 796; legacy108/new2588 and clean/other subsets remain separately reported in the receipt. These subsets overlap; do not sum them into new exposure. Corpus split names beginning with train describe heldout source provenance, not reuse as student TRAIN diagnostics.

FACT: Failure-inclusive counts retain invalid/capped outputs and generated structural failures. Completed-repair and introduced-error lower/upper values are scorer alignment bounds, separate from 95% source-group percentile intervals. A nonempty denominator is required. No failed row is dropped, regenerated or converted into a completed repair.

FACT: Analyze B100 and C101 separately. For each metric, with a=D0-U1, b=D0-U8, c=D1-U1 and d=D1-U8, report D1 at U1=c-a, D1 at U8=d-b, U8 at D0=b-a, U8 at D1=d-c and interaction=(d-c)-(b-a). Exact rational effects use full fixed-population denominators.

CALCULATION: Descriptive 95% percentile intervals use 10,000 paired source-group bootstrap draws, PCG64 seed42, all cases in each of 52 resampled groups. Shared draw-index SHA-256 `ca7289b19fcdde43e36592843d88bc89d9aa3f2361120a120cd3df4c9ec336d0` independently reproduces across all metrics, systems and contrasts. Alignment bounds remain separate from sampling intervals. The bootstrap does not measure training-seed uncertainty, determine eligibility or establish H1.

## B100 fixed cells

MEASURED RESULT: The four prespecified cells share the expanded heldout panel.

| Cell | Origin | Natural errors | WER | 95% WER interval, percent | Completed repair bounds | Introduced bounds |
| --- | --- | --- | --- | --- | --- | --- |
| D0-U1 | archived, no new training | 58,493 | 114.858815% | [112.965125, 116.940350] | 76–77 | 57,156–57,157 |
| D0-U8 | G2 prescribed endpoint | 63,344 | 124.384401% | [120.576000, 128.539106] | 66–69 | 61,997–62,000 |
| D1-U1 | G2 prescribed endpoint | 56,572 | 111.086675% | [109.312852, 112.930836] | 85–88 | 55,244–55,247 |
| D1-U8 | G2 prescribed endpoint | 16,997 | 33.375879% | [32.279222, 34.370571] | 44–45 | 15,628–15,629 |



## B100 independent contrasts

CALCULATION: Effect and interval columns are percentage points. WER and introduced-rate decreases indicate fewer errors; completed-repair-rate increases indicate more completed repair. Completed repair is divided by 1,413 source errors; introduced error and WER by 50,926 reference words. Lower and upper alignment estimands are reported separately.

| Metric | Effect | Exact fraction | Effect, pp | 95% interval, pp |
| --- | --- | --- | --- | --- |
| WER | D1_effect_at_U1 | -1921/50926 | -3.772140 | [-6.227171, -1.299263] |
| WER | D1_effect_at_U8 | -46347/50926 | -91.008522 | [-95.330865, -86.991400] |
| WER | U8_effect_at_D0 | 4851/50926 | +9.525586 | [7.024782, 12.151481] |
| WER | U8_effect_at_D1 | -39575/50926 | -77.710796 | [-79.339627, -76.226811] |
| WER | difference_in_differences | -22213/25463 | -87.236382 | [-90.379734, -84.259554] |
| completed_repair_lower | D1_effect_at_U1 | 1/157 | +0.636943 | [-0.709328, 2.083333] |
| completed_repair_lower | D1_effect_at_U8 | -22/1413 | -1.556971 | [-3.181560, 0.058447] |
| completed_repair_lower | U8_effect_at_D0 | -10/1413 | -0.707714 | [-2.149112, 0.632940] |
| completed_repair_lower | U8_effect_at_D1 | -41/1413 | -2.901628 | [-4.224446, -1.636963] |
| completed_repair_lower | difference_in_differences | -31/1413 | -2.193914 | [-4.179345, -0.000000] |
| completed_repair_upper | D1_effect_at_U1 | 11/1413 | +0.778485 | [-0.566854, 2.257065] |
| completed_repair_upper | D1_effect_at_U8 | -8/471 | -1.698514 | [-3.277798, -0.151389] |
| completed_repair_upper | U8_effect_at_D0 | -8/1413 | -0.566171 | [-1.908878, 0.720482] |
| completed_repair_upper | U8_effect_at_D1 | -43/1413 | -3.043171 | [-4.372366, -1.724138] |
| completed_repair_upper | difference_in_differences | -35/1413 | -2.476999 | [-4.338239, -0.507964] |
| introduced_lower | D1_effect_at_U1 | -956/25463 | -3.754467 | [-6.205235, -1.281031] |
| introduced_lower | D1_effect_at_U8 | -46369/50926 | -91.051722 | [-95.376533, -87.045859] |
| introduced_lower | U8_effect_at_D0 | 4841/50926 | +9.505950 | [7.009838, 12.131666] |
| introduced_lower | U8_effect_at_D1 | -19808/25463 | -77.791305 | [-79.426914, -76.299931] |
| introduced_lower | difference_in_differences | -44457/50926 | -87.297255 | [-90.434246, -84.343739] |
| introduced_upper | D1_effect_at_U1 | -955/25463 | -3.750540 | [-6.202424, -1.279413] |
| introduced_upper | D1_effect_at_U8 | -46371/50926 | -91.055649 | [-95.382124, -87.046282] |
| introduced_upper | U8_effect_at_D0 | 4843/50926 | +9.509877 | [7.014129, 12.137145] |
| introduced_upper | U8_effect_at_D1 | -19809/25463 | -77.795232 | [-79.427377, -76.304250] |
| introduced_upper | difference_in_differences | -44461/50926 | -87.305109 | [-90.446498, -84.350564] |



## C101 fixed cells

MEASURED RESULT: The four prespecified cells share the expanded heldout panel.

| Cell | Origin | Natural errors | WER | 95% WER interval, percent | Completed repair bounds | Introduced bounds |
| --- | --- | --- | --- | --- | --- | --- |
| D0-U1 | archived, no new training | 2,461 | 4.832502% | [4.346289, 5.371956] | 5–6 | 1,053–1,054 |
| D0-U8 | G2 prescribed endpoint | 3,173 | 6.230609% | [5.597195, 6.886230] | 9–9 | 1,769–1,769 |
| D1-U1 | G2 prescribed endpoint | 5,484 | 10.768566% | [9.207387, 12.313305] | 14–14 | 4,098–4,098 |
| D1-U8 | G2 prescribed endpoint | 4,095 | 8.041079% | [6.906683, 9.170769] | 18–18 | 2,702–2,702 |



## C101 independent contrasts

CALCULATION: Effect and interval columns are percentage points. WER and introduced-rate decreases indicate fewer errors; completed-repair-rate increases indicate more completed repair. Completed repair is divided by 1,413 source errors; introduced error and WER by 50,926 reference words. Lower and upper alignment estimands are reported separately.

| Metric | Effect | Exact fraction | Effect, pp | 95% interval, pp |
| --- | --- | --- | --- | --- |
| WER | D1_effect_at_U1 | 3023/50926 | +5.936064 | [4.627537, 7.156455] |
| WER | D1_effect_at_U8 | 461/25463 | +1.810470 | [0.996316, 2.622191] |
| WER | U8_effect_at_D0 | 356/25463 | +1.398107 | [1.014430, 1.784161] |
| WER | U8_effect_at_D1 | -1389/50926 | -2.727487 | [-3.618234, -1.865235] |
| WER | difference_in_differences | -2101/50926 | -4.125594 | [-5.050752, -3.203511] |
| completed_repair_lower | D1_effect_at_U1 | 1/157 | +0.636943 | [0.125154, 1.241804] |
| completed_repair_lower | D1_effect_at_U8 | 1/157 | +0.636943 | [-0.199873, 1.488516] |
| completed_repair_lower | U8_effect_at_D0 | 4/1413 | +0.283086 | [-0.174376, 0.778569] |
| completed_repair_lower | U8_effect_at_D1 | 4/1413 | +0.283086 | [-0.438284, 0.977433] |
| completed_repair_lower | difference_in_differences | 0/1 | +0.000000 | [-0.801786, 0.740147] |
| completed_repair_upper | D1_effect_at_U1 | 8/1413 | +0.566171 | [0.000000, 1.179253] |
| completed_repair_upper | D1_effect_at_U8 | 1/157 | +0.636943 | [-0.199873, 1.488516] |
| completed_repair_upper | U8_effect_at_D0 | 1/471 | +0.212314 | [-0.328953, 0.745806] |
| completed_repair_upper | U8_effect_at_D1 | 4/1413 | +0.283086 | [-0.438284, 0.977433] |
| completed_repair_upper | difference_in_differences | 1/1413 | +0.070771 | [-0.766292, 0.860684] |
| introduced_lower | D1_effect_at_U1 | 3045/50926 | +5.979264 | [4.661826, 7.212548] |
| introduced_lower | D1_effect_at_U8 | 933/50926 | +1.832070 | [1.009345, 2.652786] |
| introduced_lower | U8_effect_at_D0 | 358/25463 | +1.405962 | [1.021674, 1.793481] |
| introduced_lower | U8_effect_at_D1 | -698/25463 | -2.741232 | [-3.627322, -1.883323] |
| introduced_lower | difference_in_differences | -1056/25463 | -4.147194 | [-5.072127, -3.228106] |
| introduced_upper | D1_effect_at_U1 | 1522/25463 | +5.977300 | [4.661782, 7.211752] |
| introduced_upper | D1_effect_at_U8 | 933/50926 | +1.832070 | [1.009345, 2.652786] |
| introduced_upper | U8_effect_at_D0 | 715/50926 | +1.403998 | [1.018891, 1.792552] |
| introduced_upper | U8_effect_at_D1 | -698/25463 | -2.741232 | [-3.627322, -1.883323] |
| introduced_upper | difference_in_differences | -2111/50926 | -4.145230 | [-5.070389, -3.226354] |



## Limits and candidate status

INFERENCE: D1 changes natural-data diversity, error prevalence and domain composition together; these contrasts do not isolate sample count. U8 changes optimizer-update granularity under fixed within-D presentations and canonical extent. The data/update interaction describes those registered treatments on this DEVELOPMENT panel, with differing cross-D actual overshoot disclosed.

MEASURED RESULT: Both scratch D1-U8 endpoints fail the frozen WER gate. Neither an improvement relative to a weak cell nor a bootstrap interval admits a candidate. D1-U8 remains the predeclared joint-intervention candidate; there is no subjective winning-cell selection, intermediate selection or new recipe.

FRONTIER_MODEL_REVIEW_REQUIRED
