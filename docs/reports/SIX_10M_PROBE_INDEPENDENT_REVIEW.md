# Six 10M probes — independent review

MEASURED RESULT — **Independent review PASS; campaign disposition CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE.** Both independently reconstructed eligible rankings are empty. No LR is selected for B100 or C101. Review PASS describes reproduction of the campaign; all six recipes remain scientifically ineligible under the registered DEVELOPMENT rule.

FACT — Campaign freeze SHA-256 `43a97ef40acbb2efebaf4941931934969c093e23f77b69bfd132f236755b1dd3`; authorized checkpoint `7868302afc43e3cbd475464452f57912a9c2cf97`. This report combines separate artifact-based reviews rather than relying on the main campaign report alone.

| Required review | Method and reproduced result | Evidence |
| --- | --- | --- |
| A. Provenance and six-slot accounting | Six fresh seed42 starts, six completed attempt01 outcomes, frozen order and source/config identities | [Provenance review](../reviews/SIX_10M_PROVENANCE_INDEPENDENT_REVIEW.md) |
| B. Presentation-ledger identity | All six full logs match 134,591 whole presentations, 305 complete queues, shared ledger and scientific projection | [Full projection receipt](../../experiments/manifests/six_10m_probes/independent-provenance-full-projection.attempt01.json) |
| C. Endpoint/population identity | 78 native saves, 36 evaluations, exact ordered 396 IDs and six common exposure mappings | [Provenance receipt](../../experiments/manifests/six_10m_probes/independent-provenance.attempt14.json) |
| D. Metric/scorer reproduction | 14,256 canonical records, 42,768 integer distances, 11,783 bounded dense checks; generated grammar independently parsed | [Metric review](../reviews/SIX_10M_METRICS_INDEPENDENT_REVIEW.md) |
| E. LR-selection reproduction | All five gates and exact Fraction keys, arm-independent endpoint-only rankings and null selections | [Metric selection receipt](../../experiments/manifests/six_10m_probes/independent-metrics-final-selection.attempt01.json) |
| F. Checkpoint/resume/failure accounting | Native tensors/optimizer/reader cursors verified; no recorded numerical failure, replay or resume; actual interruption replay not exercised | [Provenance review](../reviews/SIX_10M_PROVENANCE_INDEPENDENT_REVIEW.md) |
| G. Curves and report consistency | Separate CPU counts/grammar/Fraction reconstruction, all five result reports and 39 answers, all 36 curve rows per table, 18 SVG axes, 1,830 native resource records | [Report consistency review](../reviews/SIX_10M_REPORT_CONSISTENCY_INDEPENDENT_REVIEW.md) |

## Independently reconstructed outcomes

MEASURED RESULT — Every recipe reaches update 305, 10,007,223 actual canonical exposures and ordinal 134,590. All three B100 initial parameter hashes are `2739837ff4ad4ff26475dca5a37608d9c46a1c7ff34f8778f24eadb18b8e8044`; all three C101 hashes are `9671ba3aaf0afb9fe22302fe140512db7bdf7e31f4d9e439bc13c75edafc2ff1`. Provenance reconstructed these from actual saved tensors, with matching architecture-specific initial optimizer/NPZ identities. Each of the six endpoint parameter, COMPLETE and NPZ hashes is reproduced in the provenance and report-consistency receipts.

| Recipe | Natural errors / reference words | Completed repair bounds | Lower support groups | Genuine generated repaired cases /192 | Eligibility |
| --- | --- | --- | --- | --- | --- |
| B100-seed42-lr1e-04 | 2208/2270 | 6–6 | 3 | 0/192 | INELIGIBLE |
| C101-seed42-lr1e-04 | 121/2270 | 0–0 | 0 | 49/192 | INELIGIBLE |
| B100-seed42-lr3e-04 | 2584/2270 | 2–2 | 2 | 0/192 | INELIGIBLE |
| C101-seed42-lr3e-04 | 128/2270 | 0–0 | 0 | 79/192 | INELIGIBLE |
| B100-seed42-lr6e-04 | 2664/2270 | 2–2 | 2 | 0/192 | INELIGIBLE |
| C101-seed42-lr6e-04 | 109/2270 | 0–0 | 0 | 54/192 | INELIGIBLE |

MEASURED RESULT — All B100 recipes pass completion, positive completed natural repair and multi-group support, and fail WER below RAW and genuine generated repair. All C101 recipes pass completion and genuine generated repair, and fail WER below RAW, positive completed natural repair and multi-group support. Natural RAW is 64/2,270. Every output remains failure-inclusive, and generated denominators remain separate.

| Arm | Exact eligible ranking | Selected recipe | Selected peak LR |
| --- | --- | --- | --- |
| B100 | `[]` | `null` | `null` |
| C101 | `[]` | `null` | `null` |

FACT — The six-stage key is lowest natural WER, lowest introduced-error upper rate, highest completed-repair lower count, fewest natural failures, highest generated mixed success, then lower peak LR. All six exact rational keys are reproduced in the metric and report-consistency reviews. Empty eligibility does not select a best ineligible recipe. No intermediate checkpoint, cross-arm comparison or subjective tie changes this result.

## Reproduction receipts and coverage

FACT — Final evidence hashes:

- Provenance attempt14: `d3ee82eb5809525d9ab84ff80ea14291cdccbc7957538b35db82df3cdf5c3f49`.
- Metric final-selection attempt01: `e655ac7ddf418a7ba56458156f475232f2369934867134f6f6f9170c29a65316`.
- Metric curve-consistency attempt07: `018e1723a1991ef615a9ea92cd00d2015bb57c54f3db2bb0950b756ffa024f36`.
- Independent report-consistency attempt02: `1d14c687aa955d01758c365552c10b42cd68450d2f125778471c5f4fa49c379b`.

MEASURED RESULT — Every frozen panel evaluation uses 108 natural and 288 generated cases; 14,256 case instances were retained across 36 evaluations. All approved checkpoint and evaluation exposures match. Source/config/scientific identities remain frozen. Natural correspondence bounds are alignment bounds, not confidence intervals. Dense-oracle reproduction has fixed-budget coverage rather than an unbounded claim.

MEASURED RESULT — Required baseline qualification reproduced 372 tests at the authorized checkpoint. The qualified execution wrapper added seven tests before training. Final integrated validation attempt02 reproduced 379 passing tests; [final-validation.attempt02.json](../../experiments/manifests/six_10m_probes/final-validation.attempt02.json). Sum of serialized recipe wall intervals is 23128.912421s; exact accelerator kernel time remains unmeasured.

FACT — Failed mechanical preparation and reviewer diagnostics remain retained and hash-bound. Two G preflights corrected reviewer assumptions about an integer word count and SVG style punctuation; no scientific artifact changed. No unresolved scientific defect, numerical replay or resume event was found. An actual interrupted recovery was not exercised, so this report does not claim one passed.

## Interpretation and hard stop

DESCRIPTIVE INFERENCE — The reproduced evidence supports an interpretable negative result under this exact frozen design. It does not prove that either architecture can never work. Generated C101 task learning does not replace natural viability; isolated positive B100 repair counts do not offset introduced errors and WER above RAW.

FUTURE SCIENTIFIC DECISION — A separately authorized Astra review may interpret adequacy, comparator evidence, scope and cost before any proposed treatment change. This campaign stops with exactly six consumed slots. No H1 confirmation, final-seed run, final150M, sealed inference, A100, H2 or paper_protocol_v2 freeze occurred.

CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE
