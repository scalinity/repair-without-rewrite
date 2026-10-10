# Manuscript scientific figure package v1

FACT — Prepared 2026-10-10 on `codex/manuscript-figures-v1`, based exactly on accepted preparation checkpoint `2550823ca8f4f3c3ceb15a0de775e43878291422`. Frozen scientific checkpoint: `609f97f31979d469ad8551d06b2c07c3513181ec`. This package implements F01–F08 in the [accepted registry](CLAIM_AND_FIGURE_REGISTRY_V1.md) using its public aggregates. It changes no scientific treatment, evidence or claim status and does not authorize manuscript submission or a new experiment.

## Completed figures and tables

Each item has vector SVG, vector PDF with embedded text fonts, a 180-dpi PNG preview, a complete caption/provenance note and a numeric source map. Tables are rendered as tables. PDF is the fixed-typography publication export; SVG uses the declared Vera/DejaVu/Arial sans-serif font stack and selectable text. Export page dimensions accommodate all labels without reducing table body text below 11 points. The blue/orange series use different marker shapes; C101 trajectories additionally use open/filled markers. Color is not the sole identifier.

| ID | Approved content / visual form | Exports | Caption / provenance / exact data |
|---|---|---|---|
| F01 | G1 scratch outcomes; separate natural and generated tables | [SVG](figures/F01.svg) · [PDF](figures/F01.pdf) · [PNG](figures/F01.png) | [Caption](figures/F01.caption.md) · [Data](figures/F01.data.json) |
| F02 | G2 B100/C101 factorial WER panels, exact endpoint table and interaction table | [SVG](figures/F02.svg) · [PDF](figures/F02.pdf) · [PNG](figures/F02.png) | [Caption](figures/F02.caption.md) · [Data](figures/F02.data.json) |
| F03 | Completed/raw repairs, introduced errors and failures; separate lexical-zero stratum table | [SVG](figures/F03.svg) · [PDF](figures/F03.pdf) · [PNG](figures/F03.png) | [Caption](figures/F03.caption.md) · [Data](figures/F03.data.json) |
| F04 | Three C101 trajectories: full initialization scale, post-initialization detail and count companion | [SVG](figures/F04.svg) · [PDF](figures/F04.pdf) · [PNG](figures/F04.png) | [Caption](figures/F04.caption.md) · [Data](figures/F04.data.json) |
| F05 | ByT5 trajectory: full/detail WER panels, nominal/actual schedule and separate failure counts | [SVG](figures/F05.svg) · [PDF](figures/F05.pdf) · [PNG](figures/F05.png) | [Caption](figures/F05.caption.md) · [Data](figures/F05.data.json) |
| F06 | D0/D1 exact frequency-mass, repair/identity/first-pass and phase-charge tables | [SVG](figures/F06.svg) · [PDF](figures/F06.pdf) · [PNG](figures/F06.png) | [Caption](figures/F06.caption.md) · [Data](figures/F06.data.json) |
| F07 | Whole-output outcomes and reference-aware non-deployable oracle ceiling/interval tables | [SVG](figures/F07.svg) · [PDF](figures/F07.pdf) · [PNG](figures/F07.png) | [Caption](figures/F07.caption.md) · [Data](figures/F07.data.json) |
| F08 | All 13 physical recipe intervals and nested ByT5/G1 timing-component tables | [SVG](figures/F08.svg) · [PDF](figures/F08.pdf) · [PNG](figures/F08.png) | [Caption](figures/F08.caption.md) · [Data](figures/F08.data.json) |

## Regeneration

Run from the repository root with Python 3.12 and the existing document-tool runtime. The verified runtime is Python 3.12.14, ReportLab 4.4.9, pypdf 6.10.0 and Poppler `pdftoppm` 26.09.0. The project environment and dependency lock are unchanged. ReportLab supplies the existing Vera font files; no font/software payload is newly vendored. The isolated research environment does not contain these document libraries; the available bundled document runtime was used without installation.

```sh
python3 tools/manuscript_figures/regenerate_v1.py
python3 tools/manuscript_figures/validate_v1.py
```

`python3` must refer to that document runtime and `pdftoppm` must be available on its command path. The generator uses public tracked paths only, checks accepted inventory hashes before exporting, imports no research modules, and emits five files per figure. It performs no inference, scientific rescore, bootstrap rerun or private-payload access. Existing scientific source files are never executed.

For a separate reproducibility check, choose an empty external output directory:

```sh
python3 tools/manuscript_figures/regenerate_v1.py --output-dir ../figure-regeneration-v1
python3 tools/manuscript_figures/validate_v1.py --figure-dir ../figure-regeneration-v1
```

FACT — A second final rendering produced all **40 files byte-identically**, including SVG, PDF, PNG, captions and numeric maps. [Regeneration receipt](../../experiments/manifests/manuscript_figures/regeneration.attempt01.json) records their SHA-256 identities. Different font/renderer versions may change export bytes; the stated runtime binds this byte-reproduction result.

## Numerical verification and interpretation

FACT — The separate [validator](../../tools/manuscript_figures/validate_v1.py) does not import the generator or scientific code. It independently rereads source fields/report cells, checks declared six-decimal precision, parses SVG marks and PDF vector paths, and checks PDF/SVG labels. The final run passes **3,299 mechanical assertions**, covering **441 source-bound measurements, 439 displayed source-bound numeric labels and 62 plotted numeric marks**. Method labels, axis ranges, population denominators and RAW identity zeros were also checked against the approved definitions. See [validation](FIGURE_DATA_VALIDATION_V1.md), the [separate-path review](../reviews/MANUSCRIPT_FIGURE_DATA_INDEPENDENT_REVIEW.md) and [final receipt](../../experiments/manifests/manuscript_figures/validation.attempt03.json).

FACT — All source hashes match the complete accepted inventory. No scientific verification status is upgraded: F01/F02/F04/F05/F08 and F03 endpoint accounting rely on historical independent reconstruction; F03 detailed lexical-zero decomposition, F06 detailed phase/identity/first-pass accounting and F07 detailed oracle intervals retain limited reconstruction. F06 repair distributions and F07 point proposal/oracle aggregates have historical independent reaggregation.

FACT — B100 WER above 100% remains visible. Alignment bounds are count-identification ranges, not confidence intervals. F02 group intervals describe source-group sampling, not training-seed variability. Trajectory connections join only observed states. D0-U1 is archived/rescored, not retrained. ByT5 nominal 2/5 labels retain actual presentation offsets. No retrospective winner is selected. Every oracle result is reference-aware and non-deployable. Timing components are nested and never added twice.

## Unavailable elements and preserved boundaries

FACT — No approved figure is blocked. Unavailable finer trajectories, probabilities, training-seed/domain uncertainty, exact kernel time, G2 all-in operational span and monetary costs are not invented. F04/F05 do not draw group intervals; their availability and classification are stated in captions. No new per-case points or smoothing is used. Full reconstruction of the detailed retrospective calculations remains outstanding.

FACT — Experimental evidence, research code, immutable design inputs, model/checkpoint identities, other worktrees/branches, `ORCHESTRATION.html` and all three automation settings files are unchanged. Orchestration is owned elsewhere; a future owner realignment would add this completed parallel documentation package, its links and mechanical-check counts. The historical 514-test result remains historical; baseline/end scientific suites are NOT RUN because neural/model tests exceed this task's documentation/aggregate-only authority. No build, dependency modification, corpus acquisition, acceptance fitting, Generation 3, final training or sealed inference occurred.

MANUSCRIPT_FIGURE_PACKAGE_PREPARED
