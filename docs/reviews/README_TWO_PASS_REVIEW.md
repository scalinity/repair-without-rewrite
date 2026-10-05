# README two-pass review

Date: 2026-10-05. Scope: `README.md` only, with this review as the verification record. No model run, dependency mutation, build, commit, push, protocol freeze, or experiment admission was performed for this documentation task.

## Reference and source basis

The live [MindFriend README](https://github.com/scalinity/MindFriend/blob/main/README.md) was fetched successfully through the GitHub contents API during this invocation. It supplied the portfolio structure: thesis, motivation, systems, foundations, correctness, architecture, technical highlights, stack, scale, roadmap, and license. A development section preserves and expands the original repository's brief test instructions. Its language and project claims were not copied.

Sources checked include the immutable canonical specification's thesis and model contracts, accepted pre-implementation findings, prospective amendments, current subsystem reports, current foundation decision, source/model/scorer implementations, test files, dependency declarations, and the integrated test receipt. The accepted review's focused B/C direction takes precedence over treating the original broad roster as an executed or frozen protocol. The public working title and subtitle follow the owner's supplied wording exactly.

## Pass 1 — accuracy against code and evidence

**Result: PASS for the README's bounded factual claims.** This is documentation verification, not independent requalification of the experiments.

| Claim family | Checked evidence and disposition |
|---|---|
| Foundation status | `docs/reports/FOUNDATION_GO_NO_GO.md`: `FOUNDATION_REPAIR_REQUIRED`; no final training or freeze. |
| Integrated tests | `docs/reports/raw/final_foundation_tests_attempt01.txt`: 180 passed in 18.64 s. The README labels this a recorded correctness receipt; tests were not rerun for a prose-only change. |
| Model sizes and mechanics | `src/models/core.py`, `src/models/bc.py`, `src/models/edits.py`, MODEL0 and B/C reports: exact 8,621,312 / 100,686,336 / 101,081,859 counts; event accounting, byte renderer and source-binding limit checked. |
| Learning evidence | Both exact B/C models achieved 4/4 toy memorization after the retained failed attempt. No held-out quality, 10M-probe result or controlled LR-only conclusion is claimed. MODEL-0 V6 and the full permitted-corpus tokenizer remain incomplete. |
| Scorer | Scorer report and implementation: conditional optimal-path accounting, raw conservation versus completion-gated credit, source-fixed eligibility, empty/missing distinctions and unavailable-domain handling. Exhaustive 3,375 triples, 10,000 trials and 19,074 NFC rows are explicitly scoped qualification counts. |
| Stress | Current repaired generator report: 288 development cases, 96 groups, 89 unique references, 8 categories, 4 cells, 3 views. Perfect public inverse is disclosed as a restricted-grammar limitation. Final 2,400 cases and broader families remain pending. |
| Public data | Current source report: HPO 898/12, sealed 5,273/19, all 311 bounded training rows excluded; 52,482 metadata-only potential training rows not admitted; SLUE 401 with zero actual acquisition. |
| Comparators and prior work | Comparator report: ByT5 four invalid/capped completions after ten toy updates; Qwen two valid toy completions with zero repair/introduction; bounded ConstDecoder incompatibility, without a model-quality claim. Direct compact-ASR predecessor is acknowledged. |
| Timing | Native calibration and ASR/TTS reports: sustained decoder fixture rate distinguished from short B/C samples and paper-canonical exposure. Parakeet's warm panel and initial repeated calls remain separate; ASR failures and preprocessing limits accompany the timing. Failed alternate MPS STFT and separately declared original CPU Kokoro remain separate. |
| Stack and commands | Versions match `pyproject.toml`; the separate speech environment is identified as separate. `uv sync --help` confirms `--locked` and `--no-build`. The full test command retains the qualified `MLX_ENABLE_TF32=0` setting. No installation was run during this review. |
| Paths | Relative Markdown links were checked against the working tree. File and module references were checked directly. |

The skill's `detect_scale.sh` was run from its actual installed skill directory while the working directory was the repository root. Its raw output was 12,971 Python files, 5 JavaScript files, and 18 Git commits. Inspection of the helper showed it excludes the root virtual environment but not the additional downloaded probe environments beneath `exports/`. Those numbers would overstate first-party scale and were not published in the README. Direct path-scoped counts establish **16 Python files in `src/` and 13 in `tests/`**. The changing commit count and irrelevant downloaded JavaScript packages were omitted. Domain-specific counts come from the named evidence above, not estimates.

No cost arithmetic, paper speedup, final population accuracy, or campaign-duration projection is asserted. The renderer's untouched-byte guarantee is explicitly separated from edit-selection quality and semantic safety.

## Pass 2 — scope, voice and reference alignment

**Result: PASS after corrections.** The draft was reread from title through license against the live reference's section order and density.

- The lead states the research question and intended controls, followed immediately by the current failure-to-advance disposition and its missing prerequisites.
- Seven subsystem sections carry concrete mechanisms, observed evidence and limitations. Tables distinguish architecture sizes, source admission and roadmap dependencies.
- The source/runtime, model-learning and scorer-coverage limits remain adjacent to the numbers that could otherwise be mistaken for paper results.
- The original test entry point is preserved with its required precision setting. Setup is brief and does not imply the benchmark programs are ordinary tests.
- Technical highlights give the reason for each mechanism, without claiming novelty from implementation alone.
- Badges reflect declared package versions and the recorded foundation result; no unsupported platform, CI, paper or license badge was added.
- The closing line restates measurement of repair, change and cost without promising superiority.
- The exact owner-supplied subtitle retains its requested capitalization. Development adds one section to the reference inventory because this repository is intended to be inspectable and runnable.
- A grammatical article was corrected in the source-binding explanation. The scale-helper contamination was corrected before publication rather than presented as repository size.
- No repository-wide reuse license was invented. The license section states that none is selected and preserves the third-party terms boundary.

## Public-safe README check

The README was scanned for common credential patterns, private-key headers, email addresses, and owner-specific absolute paths. No matches were found. All project links use repository-relative paths or the declared public portfolio reference; badges use public static URLs.

This check covers the README and this review only. The separate publication owner must complete the working-tree and full-history audit before the first public push; this review does not certify the rest of the repository or authorize publication.
