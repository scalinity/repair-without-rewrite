# B100 10M LR selection

FACT — Campaign freeze SHA-256 `43a97ef40acbb2efebaf4941931934969c093e23f77b69bfd132f236755b1dd3`. [campaign-freeze.attempt01.json](../../experiments/manifests/six_10m_probes/campaign-freeze.attempt01.json). Endpoint decisions: [endpoint-selection.attempt01.json](../../experiments/manifests/six_10m_probes/endpoint-selection.attempt01.json). Descriptive tables and raw-output/resource hash bindings: [descriptive-tables.attempt01.json](../../experiments/manifests/six_10m_probes/descriptive-tables.attempt01.json).

MEASURED RESULT — Selected LR: **none**. Eligible lexicographic ranking: `[]`. Every eligible recipe is ranked only at its completed 10M endpoint, independently within this arm. Ineligible recipes have no selection rank.

| Recipe | 1 completion | 2 WER < RAW | 3 repair lower > 0 | 4 ≥2 support groups | 5 generated required repair | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| B100-seed42-lr1e-04 | PASS | FAIL | PASS | PASS | FAIL | INELIGIBLE |
| B100-seed42-lr3e-04 | PASS | FAIL | PASS | PASS | FAIL | INELIGIBLE |
| B100-seed42-lr6e-04 | PASS | FAIL | PASS | PASS | FAIL | INELIGIBLE |

The ranking uses exact fractions: lowest natural WER, lowest introduced-error upper rate, highest completed-repair lower count, fewest natural incomplete/invalid outputs, highest generated mixed success, then lower peak LR. The following values permit reproduction; they do not rank ineligible recipes.

| Recipe | WER | Introduced upper rate | Completed repair lower | Natural failures | Generated mixed success | Peak LR |
| --- | --- | --- | --- | --- | --- | --- |
| B100-seed42-lr1e-04 | 1104/1135 | 215/227 | 6 | 0 | 0 | 1/10000 |
| B100-seed42-lr3e-04 | 1292/1135 | 1261/1135 | 2 | 0 | 0 | 3/10000 |
| B100-seed42-lr6e-04 | 1332/1135 | 1301/1135 | 2 | 0 | 0 | 3/5000 |

MEASURED RESULT — Natural RAW is 64/2,270 (2.819383%) on 108 fixed cases. Bounds are scorer alignment bounds, not confidence intervals.

| Recipe | WER errors / 2,270 | WER | Repair | Completed repair | Support groups | Introduced errors | Introduced rate | Preserved / 2,210 | Byte / lexical identity / 108 | Invalid or incomplete |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B100 / 1e-04 | 2208 | 97.268722% | 6–6 | 6–6 | 3 | 2150–2150 | 94.713656%–94.713656% | 91–100 | 0 / 0 | 0 |
| B100 / 3e-04 | 2584 | 113.832599% | 2–2 | 2–2 | 2 | 2522–2522 | 111.101322%–111.101322% | 121–132 | 0 / 0 | 0 |
| B100 / 6e-04 | 2664 | 117.356828% | 2–2 | 2–2 | 2 | 2602–2602 | 114.625551%–114.625551% | 126–146 | 0 / 0 | 0 |


| Recipe | Clean /96 | Mixed /96 | Required-only /96 | Whole case /288 | Genuine repaired cases /192 | Repaired fields /288 | Structure failures /288 | Decoder failures /288 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B100 / 1e-04 | 0 | 0 | 0 | 0 | 0 | 0 | 288 | 0 |
| B100 / 3e-04 | 0 | 0 | 0 | 0 | 0 | 0 | 288 | 3 |
| B100 / 6e-04 | 0 | 0 | 0 | 0 | 0 | 0 | 288 | 0 |

FACT — Intermediate checkpoints cannot be selected. The rule was not weakened, no extra LR or seed was run, and this is DEVELOPMENT/HPO evidence rather than H1 confirmation. Independent reproduction is documented in [SIX_10M_PROBE_INDEPENDENT_REVIEW.md](SIX_10M_PROBE_INDEPENDENT_REVIEW.md).

CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE
