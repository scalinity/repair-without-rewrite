# Generation-2 failure-inclusive expanded qualification evaluation

FACT: Recorded 2026-10-07T18:11:20.522978+00:00; reviewed repository source commit `c33d975540236722cf6b5daf050921c79d3579ec`. This report never identifies its own future commit. All seven scientific recipes remain AUTHORIZED_UNSTARTED.

MEASURED RESULT: Sixteen complete 2,984-case panels are retained: two archived G1 3e-4 endpoints, initialization and endpoint for all six native qualification cells, and initialization and update100 for ByT5. Invalid byte decodes and incomplete/capped generations remain in the score/status accounting. No result was removed because it was poor.

FACT: The full public numeric tables, hashes, counts and separate alignment bounds are in `experiments/manifests/generation_2/expanded-evaluation-summary.attempt01.json`. Subsets include all 2,696 natural cases, legacy108, new2588, CAL1900, HPO796, each official split, natural-clean/other, and each of the three frozen generated views. The natural subsets are overlapping views of the same panel.

| Panel | Cases | Natural cases | Natural status counts |
|---|---:|---:|---|
| BENCH-B100-D0-U8-final | 2984 | 2696 | `{"capped": 1, "completed": 2694, "invalid_byte_decoding": 1}` |
| BENCH-B100-D0-U8-initial | 2984 | 2696 | `{"capped": 2639, "invalid_byte_decoding": 57}` |
| BENCH-B100-D1-U1-final | 2984 | 2696 | `{"capped": 8, "completed": 2688}` |
| BENCH-B100-D1-U1-initial | 2984 | 2696 | `{"capped": 2639, "invalid_byte_decoding": 57}` |
| BENCH-B100-D1-U8-final | 2984 | 2696 | `{"completed": 2683, "invalid_byte_decoding": 13}` |
| BENCH-B100-D1-U8-initial | 2984 | 2696 | `{"capped": 2639, "invalid_byte_decoding": 57}` |
| BENCH-C101-D0-U8-final | 2984 | 2696 | `{"completed": 2695, "invalid_or_capped": 1}` |
| BENCH-C101-D0-U8-initial | 2984 | 2696 | `{"abstained": 470, "completed": 295, "invalid_or_capped": 1931}` |
| BENCH-C101-D1-U1-final | 2984 | 2696 | `{"completed": 2690, "invalid_or_capped": 6}` |
| BENCH-C101-D1-U1-initial | 2984 | 2696 | `{"abstained": 470, "completed": 295, "invalid_or_capped": 1931}` |
| BENCH-C101-D1-U8-final | 2984 | 2696 | `{"completed": 2696}` |
| BENCH-C101-D1-U8-initial | 2984 | 2696 | `{"abstained": 470, "completed": 295, "invalid_or_capped": 1931}` |
| ByT5-qualification-initial | 2984 | 2696 | `{"invalid_utf8": 2696}` |
| ByT5-qualification-update100 | 2984 | 2696 | `{"capped": 8, "complete": 2688}` |
| archived-G1-B100-3e-4-endpoint | 2984 | 2696 | `{"completed": 2696}` |
| archived-G1-C101-3e-4-endpoint | 2984 | 2696 | `{"completed": 2696}` |

FACT: Native qualification endpoints follow fixed timing measurements and differ in actual update and exposure counts. ByT5 ends after exactly 100 qualification updates. Their descriptive contrasts are not the matched 10M scientific contrasts; all seven scientific recipes remain unstarted, and qualification weights are forbidden as scientific initializers.

FACT: Descriptive uncertainty uses the 52 natural source groups with 10,000 shared PCG64 seed 42 bootstrap draws and 95% percentile intervals. WER, completed-repair lower/upper and introduced-error lower/upper are reconstructed separately; the RAW source WER comparator is included. Shared draws pair the same source-group samples for every contrast. These intervals do not measure training-seed uncertainty, H1, comparator adequacy or quality-based initializer/recipe selection.

MEASURED RESULT: The independent evaluator rebuilds membership, failure counts and integer scoring bounds directly from all sixteen complete records files and their hashes. It reconstructs intervals with integer multiplicity matrix products instead of the producer's indexed bootstrap arrays. Every required panel and all paired contrasts pass. Evidence: `experiments/manifests/generation_2/independent-evaluation.attempt01.json`.

FACT: The two archived controls are read-only reevaluations, with zero new training. Their original G1 eligibility and failure dispositions remain unchanged. CAL references are used for descriptive scoring only, not training or calibration fit; the post-qualification overlay records 30,401 new student CAL uses: 30,400 in sixteen complete panels, plus one scored but unwritten reference use from retained pre-training ByT5 attempt 01. One CAL ID has seventeen uses; the other 1,899 have sixteen. The failed output and score are unavailable and are not reconstructed.

G2_EXPANDED_QUALIFICATION_EVALUATION_RECONSTRUCTED
