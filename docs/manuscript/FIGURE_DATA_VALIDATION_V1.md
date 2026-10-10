# Figure data validation v1

FACT — Public-aggregate mechanical verification on 2026-10-10, from accepted preparation checkpoint `2550823ca8f4f3c3ceb15a0de775e43878291422` and frozen scientific checkpoint `609f97f31979d469ad8551d06b2c07c3513181ec`. This is an export/data-transcription audit, not fresh scientific outcome reconstruction. No protected/private transcript, reference, audio, model array or per-case score file was opened.

## Executed checks

FACT — The final independent implementation [`validate_v1.py`](../../tools/manuscript_figures/validate_v1.py) passes **3,299 assertions**. It imports neither the renderer nor research/scoring/training code. Its source traversal and numeric formatting are separate implementations; its PDF audit reads actual vector drawing operations rather than trusting renderer metadata. All eight PDFs contain vector content with no raster scientific layer. SVG labels, SVG plot coordinates, PDF labels/placement and PDF plot coordinates match source values. Source-bound rates/intervals are reproduced to six decimals, and integer counts/fractions exactly. Axis ticks and RAW identity constants are presentation/definition values, not fabricated measurements.

| Figure | Source-bound measurements | Displayed source-bound numeric labels | Numeric plot marks (including repeated detail views/baselines/intervals) | Result |
|---|---:|---:|---:|---|
| F01 | 61 | 61 | 0 | PASS |
| F02 | 33 | 33 | 18 | PASS |
| F03 | 22 | 22 | 0 | PASS |
| F04 | 127 | 126 | 35 | PASS |
| F05 | 37 | 36 | 9 | PASS |
| F06 | 56 | 56 | 0 | PASS |
| F07 | 31 | 31 | 0 | PASS |
| F08 | 74 | 74 | 0 | PASS |
| Total | 441 | 439 | 62 | PASS |

FACT — All 126 evidence-source entries, 130 public-receipt bindings and seven immutable design bindings in the complete accepted [inventory](../../experiments/manifests/manuscript_development_evidence/evidence-inventory.attempt01.json) retain their SHA-256 identities. Entries overlap; those counts are not distinct scientific populations. Per-figure `.data.json` files bind repository-relative source paths, JSON field/index locators or exact Markdown line/cell/token locators, transformation units, labels and source hashes. No private artifact path is dereferenced.

CALCULATION — Direct public-count arithmetic independently agrees with the registered values:

- WER is output-error count / reference words ×100, for all six G1 endpoints and all 42 G2 tables; G1 uses 2,270 words and G2 uses 50,926. G2 retains all 2,696 natural cases, 288 generated cases and 1,413 RAW errors. G1 RAW is 2.819383%; G2 RAW is 2.774614%.
- B100/C101 interactions reproduce the exact WER fractions `-22213/25463` and `-2101/50926`; multiplication by 100 gives −87.236382/−4.125594 pp. The recorded intervals remain descriptive group intervals.
- Raw conservation agrees at both alignment endpoints. C101 uses 20 raw repairs, not its 18 completed repairs. ByT5 gives `1413 - 120 + 357 = 1650`.
- D0 frequency mass gives `763+261=1024`, `763*18+261*19=18693`; D1 gives `8688+5425=14113`, `8688+2*5425=19538`. Means are 18.254883/1.384397. Registered charge-based equivalents use `1000665/54812` and `1000628/721825`, giving 18.256312/1.386247.
- Better/equal/worse categories sum to 2,696 in each fixed proposal arm. Oracle conservation gives gains 2/3/109 from RAW minus oracle errors 1,411/1,410/1,304. ByT5 gain is 0.214036 pp, approximately 7.714% of RAW errors. Leading-decimal oracle intervals are checked explicitly against `[0, .010418]`, `[0, .013181]`, `[.154027, .288196]` pp.
- Nonoverlapping physical recipe totals give 23,128.912421 seconds / 6.424698 hours for G1 and 132,122.121229 seconds / 36.700589 hours for G2. Nested training/observation/decode/scorer fields are displayed separately and are not summed into these totals.

## Historical verification scope

| Figure / component | Evidence status retained |
|---|---|
| F01 | Historically independent G1 metrics/provenance/selection reconstruction; dense-oracle coverage remains 11,783/14,256, not complete dense coverage |
| F02 | Historically independent G2 scores, exact factorial fractions and shared group-bootstrap reconstruction |
| F03 endpoints | Historically independent G2 scores and conservation |
| F03 lexical-zero table | Recorded retrospective decomposition; detailed new decomposition not fully requalified in frontier v3 |
| F04 | Historically independent frozen C101 observations; no new checkpoint inspection |
| F05 | Historically independent ByT5 observations/milestone bindings; only exact ten-pass supplies adequacy |
| F06 repair distributions | Independently reaggregated in historical frontier v3 |
| F06 phase/identity/first-pass detail | Recorded retrospective accounting with narrower independent coverage |
| F07 point proposal/oracle aggregates | Independently reaggregated in historical frontier v3 |
| F07 oracle intervals | Recorded retrospective group intervals; not fully independently repeated in v3 |
| F08 | Historically independent native ledger/resource accounting; no fresh private-log reconstruction |

FACT — The same Sol session authored the renderer and executed the separate mechanical validator. This provides an independent software path, not another human review or a new scientific independent-reconstruction receipt. Historical independence is attributed only to the existing reviews. Plotting upgrades no claim.

## Rendering, reproducibility and failures

FACT — All eight PDF-rendered PNG previews were inspected for legibility, clipping, overlapping labels, table alignment, units, full-scale initialization, RAW visibility and oracle warnings. F02/F04 were also inspected in grayscale: circle/square/open-circle markers preserve series identity. Static vector exports have no responsive browser layout; no viewer tab was resized. Formal color-vision simulation was NOT RUN. The numerical layout check verifies plot coordinates and label placement, not semantic recoverability.

FACT — A separate final regeneration produced all **40 files byte-identically** under Python 3.12.14 / ReportLab 4.4.9 / pypdf 6.10.0 / Poppler 26.09.0. [Regeneration receipt](../../experiments/manifests/manuscript_figures/regeneration.attempt01.json) binds all output hashes. The source and final vector exports passed the separate validator after the final content/layout changes.

FACT — Failures are retained. Render attempt01 stopped because `D0 P0` occurs in two different public tables; a table-specific locator fixed the mechanical ambiguity. Attempt02 rendered successfully but visual QA found leading-decimal oracle bounds parsed at the wrong magnitude. The parser was corrected before final numerical validation or publication. Attempts03–05 record corrected rendering and layout refinement. Original diagnostics remain outside Git; public [render receipts](../../experiments/manifests/manuscript_figures/render.attempt01.json) retain failure dispositions and diagnostic hashes. Initial and expanded successful [validation attempt01](../../experiments/manifests/manuscript_figures/validation.attempt01.json), [attempt02](../../experiments/manifests/manuscript_figures/validation.attempt02.json) and [final attempt03](../../experiments/manifests/manuscript_figures/validation.attempt03.json) are all retained. No scientific source or historical result was changed to fix export defects.

## Safety and unrun checks

FACT — Publication safety covers the complete staged package, including SVG text/descriptions, PDF extracted text/metadata, captions, scripts, numeric maps and new receipts; PNG previews are rendered from the same verified PDFs. Credential and non-functional personal-identifier findings are zero, with the receipt saved as `experiments/manifests/manuscript_figures/publication-safety.attempt01.json`. The staged whitespace check passes. Other branch/worktree heads, original working status, orchestration bytes and three automation settings files retain their captured identities.

FACT — Scientific test suites at baseline and closeout: NOT RUN. The historical 514-test count remains historical. Private/scientific rescore, bootstrap rerun, neural execution, kernel timing, protected reference access and full retrospective reconstruction: NOT RUN. Missing finer trajectories/probabilities, seed/domain uncertainty and costs remain unavailable. No required approved visual element is blocked; those limitations remain explicit rather than replaced by invented data.

PASS_MECHANICAL_FIGURE_DATA_VALIDATION
