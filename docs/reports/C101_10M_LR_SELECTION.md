# C101 10M LR selection

FACT — Campaign freeze SHA-256 `43a97ef40acbb2efebaf4941931934969c093e23f77b69bfd132f236755b1dd3`. [campaign-freeze.attempt01.json](../../experiments/manifests/six_10m_probes/campaign-freeze.attempt01.json). Endpoint decisions: [endpoint-selection.attempt01.json](../../experiments/manifests/six_10m_probes/endpoint-selection.attempt01.json). Descriptive tables and raw-output/resource hash bindings: [descriptive-tables.attempt01.json](../../experiments/manifests/six_10m_probes/descriptive-tables.attempt01.json).

MEASURED RESULT — Selected LR: **none**. Eligible lexicographic ranking: `[]`. Every eligible recipe is ranked only at its completed 10M endpoint, independently within this arm. Ineligible recipes have no selection rank.

| Recipe | 1 completion | 2 WER < RAW | 3 repair lower > 0 | 4 ≥2 support groups | 5 generated required repair | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| C101-seed42-lr1e-04 | PASS | FAIL | FAIL | FAIL | PASS | INELIGIBLE |
| C101-seed42-lr3e-04 | PASS | FAIL | FAIL | FAIL | PASS | INELIGIBLE |
| C101-seed42-lr6e-04 | PASS | FAIL | FAIL | FAIL | PASS | INELIGIBLE |

The ranking uses exact fractions: lowest natural WER, lowest introduced-error upper rate, highest completed-repair lower count, fewest natural incomplete/invalid outputs, highest generated mixed success, then lower peak LR. The following values permit reproduction; they do not rank ineligible recipes.

| Recipe | WER | Introduced upper rate | Completed repair lower | Natural failures | Generated mixed success | Peak LR |
| --- | --- | --- | --- | --- | --- | --- |
| C101-seed42-lr1e-04 | 121/2270 | 57/2270 | 0 | 0 | 32 | 1/10000 |
| C101-seed42-lr3e-04 | 64/1135 | 32/1135 | 0 | 0 | 42 | 3/10000 |
| C101-seed42-lr6e-04 | 109/2270 | 9/454 | 0 | 0 | 30 | 3/5000 |

MEASURED RESULT — Natural RAW is 64/2,270 (2.819383%) on 108 fixed cases. Bounds are scorer alignment bounds, not confidence intervals.

| Recipe | WER errors / 2,270 | WER | Repair | Completed repair | Support groups | Introduced errors | Introduced rate | Preserved / 2,210 | Byte / lexical identity / 108 | Invalid or incomplete |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C101 / 1e-04 | 121 | 5.330396% | 0–0 | 0–0 | 0 | 57–57 | 2.511013%–2.511013% | 2153–2153 | 88 / 90 | 0 |
| C101 / 3e-04 | 128 | 5.638767% | 0–0 | 0–0 | 0 | 64–64 | 2.819383%–2.819383% | 2148–2148 | 87 / 87 | 0 |
| C101 / 6e-04 | 109 | 4.801762% | 0–0 | 0–0 | 0 | 45–45 | 1.982379%–1.982379% | 2168–2168 | 96 / 96 | 0 |


| Recipe | Clean /96 | Mixed /96 | Required-only /96 | Whole case /288 | Genuine repaired cases /192 | Repaired fields /288 | Structure failures /288 | Decoder failures /288 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C101 / 1e-04 | 93 | 32 | 6 | 131 | 49 | 55 | 70 | 0 |
| C101 / 3e-04 | 96 | 42 | 11 | 149 | 79 | 90 | 19 | 0 |
| C101 / 6e-04 | 96 | 30 | 6 | 132 | 54 | 60 | 43 | 0 |

FACT — Intermediate checkpoints cannot be selected. The rule was not weakened, no extra LR or seed was run, and this is DEVELOPMENT/HPO evidence rather than H1 confirmation. Independent reproduction is documented in [SIX_10M_PROBE_INDEPENDENT_REVIEW.md](SIX_10M_PROBE_INDEPENDENT_REVIEW.md).

CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE
