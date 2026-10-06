# Six 10M campaign report consistency — independent review

MEASURED RESULT — **Review PASS. Campaign disposition: CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE.** A separate CPU path reconstructed the decisions and checked the five result reports against retained native records. No unresolved report, metric-table, figure or decision discrepancy was found.

FACT — Reviewed source HEAD `18afad540772c4bee3b5aadbce811b3e9b24b550`; review date `2026-10-06T12:47:05.412033+00:00`. Receipt: [independent-report-consistency.attempt02.json](../../experiments/manifests/six_10m_probes/independent-report-consistency.attempt02.json), SHA-256 `1d14c687aa955d01758c365552c10b42cd68450d2f125778471c5f4fa49c379b`. The receipt binds every inspected report, native checkpoint metadata/COMPLETE file, output file, score receipt, frozen input and figure. It does not include a recursive hash of this document or the independent-review summary.

## Independent path and scope

FACT — `exports/six-10m-report-consistency-review.py`, SHA-256 `4d3efa5cef316e474d18988571948b869fb1b65e0beaef8eb9593a59d55b57f3`, uses only the Python standard library. It imports no campaign collector, trainer, scorer, model, MLX or Torch. It reads all 14,256 retained records, sums natural score counts and correspondence bounds, and reconstructs generated conformance with exact prefix/delimiter/suffix parsing of the frozen two-slot scaffolds. It compares the actual ordered IDs and source/reference hashes with the frozen panel at all 36 endpoints. This is independent aggregate reconstruction; canonical scoring and dense alignment correctness are covered by the separate metric review.

FACT — `exports/six-10m-report-consistency-resources.py`, SHA-256 `9278d1bfd6cec00014419a1af9b7fa62069d8106a073ba026fbac82125054174`, independently streamed all 1,830 native optimizer-update records. Its measured exposure totals, synchronized host-wall sums, observed memory peaks and endpoint word/decoder burdens reproduce every main resource row and wall-time total. Neither reviewer script ran inference or used an accelerator. Private text, arrays and logs remain ignored; public evidence contains counts, permitted IDs and hashes.

MEASURED RESULT — The provenance review separately reconstructed actual bytes/tensors in all 78 NPZ states and compared every presentation and complete queue across all six raw logs. Evidence: [independent-provenance.attempt14.json](../../experiments/manifests/six_10m_probes/independent-provenance.attempt14.json), SHA-256 `d3ee82eb5809525d9ab84ff80ea14291cdccbc7957538b35db82df3cdf5c3f49`, and [SIX_10M_PROVENANCE_INDEPENDENT_REVIEW.md](SIX_10M_PROVENANCE_INDEPENDENT_REVIEW.md). This report checked each resulting identity against native COMPLETE and metadata plus start/terminal receipts; it did not repeat heavy tensor hashing.

MEASURED RESULT — The metric review independently reproduced 14,256 canonical score records, 42,768 integer distance checks and 11,783 bounded dense alignment checks. Dense-oracle coverage is not claimed for its 2,473 cases outside the fixed budget. Evidence: [independent-metrics-final-selection.attempt01.json](../../experiments/manifests/six_10m_probes/independent-metrics-final-selection.attempt01.json), SHA-256 `e655ac7ddf418a7ba56458156f475232f2369934867134f6f6f9170c29a65316`; [independent-metrics-curve-consistency.attempt07.json](../../experiments/manifests/six_10m_probes/independent-metrics-curve-consistency.attempt07.json), SHA-256 `018e1723a1991ef615a9ea92cd00d2015bb57c54f3db2bb0950b756ffa024f36`; [SIX_10M_METRICS_INDEPENDENT_REVIEW.md](SIX_10M_METRICS_INDEPENDENT_REVIEW.md).

## Reconstructed provenance and populations

MEASURED RESULT — Exactly six starts and six completed terminal attempt01 receipts exist, in the prospectively frozen alternating order. Every start is seed42 with a clean working tree and null resume. The campaign freeze is SHA-256 `43a97ef40acbb2efebaf4941931934969c093e23f77b69bfd132f236755b1dd3`; all six prospective entries remain AUTHORIZED_UNSTARTED. Execution status is recorded separately rather than rewriting that freeze.

| Recipe | Initial parameter SHA-256 | Final parameter SHA-256 |
| --- | --- | --- |
| `B100-seed42-lr1e-04` | `2739837ff4ad4ff26475dca5a37608d9c46a1c7ff34f8778f24eadb18b8e8044` | `c50b13888a96f011dc9242afe42fa3dd84a86a42554d670e495b5a4b3b92da0f` |
| `C101-seed42-lr1e-04` | `9671ba3aaf0afb9fe22302fe140512db7bdf7e31f4d9e439bc13c75edafc2ff1` | `6b7c29788836ee96c2a0a5eadf91363ee4dada52003b81310617284b51f03ba1` |
| `B100-seed42-lr3e-04` | `2739837ff4ad4ff26475dca5a37608d9c46a1c7ff34f8778f24eadb18b8e8044` | `2adea1f910d549abdce3e3d8819454cfce4b21193600f7bd07ac7db1408fc023` |
| `C101-seed42-lr3e-04` | `9671ba3aaf0afb9fe22302fe140512db7bdf7e31f4d9e439bc13c75edafc2ff1` | `a3c2ec251f86e7b87f67f7d71b7ff6b9f460000c9f4c28640cbec8c297388450` |
| `B100-seed42-lr6e-04` | `2739837ff4ad4ff26475dca5a37608d9c46a1c7ff34f8778f24eadb18b8e8044` | `f76f3542fc688eac39669c4ef5f8e4b11ce440296728edbcc38f5e9775e93cfa` |
| `C101-seed42-lr6e-04` | `9671ba3aaf0afb9fe22302fe140512db7bdf7e31f4d9e439bc13c75edafc2ff1` | `cbce2f5f843dc55e6cc32856bf611690e2cd9a2b4cee240bf3e059ea8815904f` |

MEASURED RESULT — Architecture-specific initial identities match across all three LRs per arm. All six finish at update **305**, **10,007,223 canonical exposures**, last ordinal **134,590**. Final COMPLETE/NPZ identities and all 13 save endpoints per recipe are enumerated in the receipt and verified against independent provenance. Each inspected native boundary has the matching optimizer step/exposure, zero pending charge and an empty queue.

MEASURED RESULT — Frozen ledger SHA-256 `21c3f5838f5c7e85f258e8eef25b2b38884a2023199afc5d1852d68155b04f2f`; shared scientific projection SHA-256 `8f7a7b25e47112113ef7934d3e8f0190bd76b8bd6f1c3521aa3f93fbdba33dec`. Frozen panel SHA-256 `5043ed60d6ce8f891ee8e30255fabaa40fcac37b0a043c1a85dd88178832ce4e`; all 36 ordered panels have exactly 108 natural and 288 generated cases. Nominal endpoints 0, 1M, 3M, P0, P1 and 10M map to updates 0, 31, 92, 204, 285 and 305. Direct ID equality is checked; reviewer-specific encoded ID digests need not share an encoding.

## Reconstructed eligibility and exact ranking

MEASURED RESULT — Natural WER remains failure-inclusive with reference denominator 2,270 and RAW 64/2,270. Generated repaired-case counts use 192 repair-bearing cases and are never pooled with natural words/cases. All generated structural and decoder failures are retained separately.

| Recipe | Completion | WER < RAW | Completed repair lower >0 | ≥2 support groups | Generated required repair | Outcome |
| --- | --- | --- | --- | --- | --- | --- |
| B100-seed42-lr1e-04 | PASS | FAIL | PASS | PASS | FAIL | INELIGIBLE |
| C101-seed42-lr1e-04 | PASS | FAIL | FAIL | FAIL | PASS | INELIGIBLE |
| B100-seed42-lr3e-04 | PASS | FAIL | PASS | PASS | FAIL | INELIGIBLE |
| C101-seed42-lr3e-04 | PASS | FAIL | FAIL | FAIL | PASS | INELIGIBLE |
| B100-seed42-lr6e-04 | PASS | FAIL | PASS | PASS | FAIL | INELIGIBLE |
| C101-seed42-lr6e-04 | PASS | FAIL | FAIL | FAIL | PASS | INELIGIBLE |

MEASURED RESULT — Exact lexicographic keys are WER, introduced upper rate, negative completed repair lower, natural failures, negative generated mixed success and peak LR. Only eligible endpoints enter ranking.

| Recipe | Exact six-stage key |
| --- | --- |
| B100-seed42-lr1e-04 | `(1104/1135, 215/227, -6, 0, 0, 1/10000)` |
| C101-seed42-lr1e-04 | `(121/2270, 57/2270, 0, 0, -32, 1/10000)` |
| B100-seed42-lr3e-04 | `(1292/1135, 1261/1135, -2, 0, 0, 3/10000)` |
| C101-seed42-lr3e-04 | `(64/1135, 32/1135, 0, 0, -42, 3/10000)` |
| B100-seed42-lr6e-04 | `(1332/1135, 1301/1135, -2, 0, 0, 3/5000)` |
| C101-seed42-lr6e-04 | `(109/2270, 9/454, 0, 0, -30, 3/5000)` |

MEASURED RESULT — B100 eligible ranking `[]`, selected recipe/LR `null`. C101 eligible ranking `[]`, selected recipe/LR `null`. These independently reconstructed decisions match both selection reports and the machine-readable decision. No ineligible or intermediate checkpoint was selected.

## Report and figure checks

MEASURED RESULT — All 39 required campaign answers are present and traceable to the frozen manifests, qualification receipts, native outcomes, independently reconstructed counts and explicit scientific limits. The review checked six initialization rows, six endpoint identity rows, every endpoint outcome table, six five-gate rows, six exact-rational rows, all 36 natural curve rows, all 36 generated curve rows and all 36 training curve rows. The authorized baseline receipt reports 372 tests; final validation attempt02 reports 379 tests and unchanged frozen scientific source identities. Report links resolve to the intended public artifacts; every result report ends with the campaign disposition token.

MEASURED RESULT — All 18 axes across three V2 SVGs reproduce the native count series through the documented linear or symlog screen transforms, including all six exposure points and separate generated decoder-failure curves. The three V2 PNGs were inspected: rotated endpoint labels and wrapped captions are readable. Original figures remain retained. The V2 layout correction changes no data, axis scale, denominator or scientific decision.

DESCRIPTIVE INFERENCE — Undergeneration, destructive rewriting and copy-dominant behavior are labelled as interpretations of output counts, identity and errors. Repair-count onset is distinguished from viability; exact late WER ordering is descriptive. No new material-improvement threshold, extra exposure or preferred ineligible LR is introduced.

FUTURE SCIENTIFIC DECISION — Adequacy, comparator/scope and final-cost interpretation belong to separately authorized Astra review. The reports make no H1 confirmation and claim no final seed, 150M training, sealed inference, A100, H2 or paper_protocol_v2 freeze.

FACT — This separately labelled public receipt retains all measured checks and original scientific hashes. Its non-public original is preserved outside the repository; two reviewer-script path keys are expressed repository-relatively.

## Findings and retained review diagnostics

FACT — Critical findings: none. Warning findings: none. No scientific artifact or root report required correction. Positive observations: independent artifact reconstruction agrees with the endpoint-only decisions; output failures and negative outcomes remain visible; source and population identities remain fixed.

FACT — Two failed reviewer preparation attempts remain hash-bound in the receipt. Attempt01 treated the native integer `output_words` as a sequence. Attempt02 required a trailing semicolon in an SVG stroke style, which dashed paths omit. Corrected reviewer expressions passed in attempt03. Native recipes, raw scores, root reports and figures were unchanged. These are review diagnostics, separate from the empty scientific failure ledger.

MEASURED RESULT — No recorded numerical replay, interruption/resume or unresolved reader/checkpoint failure exists. Actual interrupted resume and numerical replay were not exercised; no unrun recovery check is reported as passed. Independent review reproduces the registered negative disposition without implementing a scientific change.

CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE
