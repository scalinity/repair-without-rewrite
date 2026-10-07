# Generation-2 serialized cost and retained storage projection

FACT: Recorded 2026-10-07T18:11:20.522978+00:00; reviewed repository source commit `c33d975540236722cf6b5daf050921c79d3579ec`. This report never identifies its own future commit. All seven scientific recipes remain AUTHORIZED_UNSTARTED.

CALCULATION: Total serialized Generation-2 forecast is **91.179828 hours**, including completed qualification/source construction and all seven future recipes, plus exactly one 25% reserve. The ceiling is 96 hours. Cost disposition: `PASS_G2_COST_CEILING_ONLY`. No recipe, population, learning rate, evaluation cap or margin was changed to fit the ceiling.

| Component | Class | Hours |
|---|---|---:|
| Completed qualification and shared work | MEASURED | 15.658602 |
| Seven future scientific recipes | CALCULATED | 57.150498 |
| Untimed bounded mechanical checks/failures | ASSUMED | 0.133333 |
| Source creation gap | CALCULATED | 0.001429 |
| Subtotal | CALCULATED | 72.943863 |
| Single 25% reserve | CALCULATED | 18.235966 |
| Total serialized forecast | CALCULATED | 91.179828 |

| Future recipe | Training hours | Evaluation hours | Diagnostics hours | Save hours | Startup hours | Total hours |
|---|---:|---:|---:|---:|---:|---:|
| G2-B100-D0-U8-seed42-lr3e-4 | 0.671207 | 6.329217 | 0.229371 | 0.017990 | 0.000881 | 7.248665 |
| G2-C101-D0-U8-seed42-lr3e-4 | 1.604899 | 4.326242 | 0.146817 | 0.014516 | 0.000884 | 6.093358 |
| G2-B100-D1-U1-seed42-lr3e-4 | 0.411888 | 6.402365 | 0.228771 | 0.017119 | 0.001010 | 7.061153 |
| G2-C101-D1-U1-seed42-lr3e-4 | 1.377205 | 3.997169 | 0.122355 | 0.013830 | 0.000962 | 5.511521 |
| G2-B100-D1-U8-seed42-lr3e-4 | 0.518421 | 5.787888 | 0.202396 | 0.014930 | 0.000959 | 6.524594 |
| G2-C101-D1-U8-seed42-lr3e-4 | 1.483461 | 3.704006 | 0.121970 | 0.013704 | 0.000950 | 5.324091 |
| G2-ByT5-D1-10pass-seed42-lr3e-4 | 9.697086 | 9.677586 | 0.000000 | 0.011544 | 0.000900 | 19.387116 |

CALCULATION: Native training uses each condition's frozen complete endpoint exposure divided by its measured conservative rate. Six full development panels are charged at the larger initialization/endpoint panel time, two greedy and two forced diagnostics at the larger corresponding cost, and each unique required save at the largest measured save time. ByT5 charges 35,283 updates at its conservative update time, four full panels at the larger measured panel time, and four saves at the larger measured snapshot time; the final short batch is charged at the full-batch rate. Measured qualification elapsed times already include their full panels, diagnostics and snapshots. Failed C101 control attempt01 is charged and retained. Failed pre-training ByT5 attempt01 and its independent mechanical record audit are separately charged as measured shared work. The exact shared-receipt set contains 36 entries; no failed attempt is removed from the sum.

ASSUMED: Eight bounded failures/storage checks without dedicated total timers receive one minute each, visibly separate from measured work. The measured archive/source/qualification totals are not replaced by estimates.

UNPRICED: researcher/implementation time and engineering unit/full-suite tests; electricity; unrelated host activity; final campaign or paper completion. These categories are not described as zero cost.

MEASURED RESULT: Independent cost reconstruction agrees on every recipe and shared component, one quarter reserve and the 96-hour comparison. Its arithmetic reconciliation tolerance is 1e-6 seconds; no model, scoring or replay tolerance is relaxed. Evidence: `experiments/manifests/generation_2/cost-projection.attempt01.json` and `experiments/manifests/generation_2/independent-cost.attempt01.json`.

CALCULATION: The retained storage forecast includes every successful, failed and partial current artifact. Current retained logical bytes are 131,905,804,617; allocation sums are not unique physical APFS blocks. Remaining conservative storage is 185.712373432 GiB; literal free space used for the forecast is 455.388824463 GiB; calculated free space at high water is 269.676451031 GiB. The minimum is 250 GiB. Storage disposition: `PASS_G2_RETAINED_STORAGE_FORECAST`. Evidence: `experiments/manifests/generation_2/storage-reforecast.attempt02.json`.

PASS_G2_COST_CEILING_ONLY
