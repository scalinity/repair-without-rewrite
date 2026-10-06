# Work log

Append-only history of the research work, newest entry last. Every completed step adds one entry in the same commit as the change (rules in `AGENTS.md`, "Log"). Past entries are never edited or deleted; a correction is a new entry naming the one it corrects. An entry cites the commit it started from; `git log` gives the entry's own commit.

Times are local (EDT, UTC−4). Entries 1–5 were backfilled on 2026-10-05 from `git log` and each session's own reports; entries from 6 onward are written as the work happens.

---

## 1 · 2026-10-05 00:59–02:52 · bounded foundation kickoff

- **Base:** none (repository creation). **Commits:** `9217cb1`…`c81d08f` (23).
- **Step:** build and check the bounded foundation authorized by the independent review (AUTHORIZE BOUNDED FOUNDATION ONLY).
- **Changed:** immutable design inputs and authorization recorded; independent scorer oracle and reference-triple scorer; public metadata contracts and the ICASSP 2025 predecessor verified; MODEL-0 mathematical and checkpoint core; native calibration runner and resume audit; B100/C101 mechanics with matched memorization (first recipe failed, preserved); restricted stress grammar; pinned ByT5, Qwen, Parakeet and Kokoro probes with failures retained; public book/project family closure; README; publication privacy mapping and clean-clone check; public repository created.
- **Disposition:** `FOUNDATION_REPAIR_REQUIRED`. Tests: 180 passed.
- **Evidence:** `docs/reports/BOUNDED_FOUNDATION_SESSION_REPORT.md`, `docs/reports/FOUNDATION_GO_NO_GO.md`, `docs/reports/PUBLICATION_REPORT.md`.
- **Left undone:** useful held-out learning, credible ByT5, full source qualification, one-month fit.

## 2 · 2026-10-05 06:28–06:29 · foundation repair

- **Base:** `c81d08f`. **Commits:** `2fad2b1`…`f24712e` (9).
- **Changed:** Parakeet source path repaired and narrowed; LS-PC training supply closed through full parent and reference closure (1,024 TRAIN pairs / 48 groups admitted); 16,384-entry development tokenizer trained; MODEL-0 V6 passed on 10,002,432 real-shard inputs; two bounded ByT5 adaptations screened (`REPAIR_REQUIRED`); sustained natural B/C updates measured; natural non-identity scorer qualified; six probes kept gated.
- **Disposition:** `FOUNDATION_REPAIR_REQUIRED` (probe admission V1). Tests: 259 passed.
- **Evidence:** `docs/reports/FOUNDATION_REPAIR_SESSION_REPORT.md`, `docs/reports/BC_10M_PROBE_ADMISSION_DECISION.md`.
- **Left undone:** mixed-reader qualification and the chosen complete-update regime.

## 3 · 2026-10-05 16:35 · paired reader and BENCH audit

- **Base:** `f24712e`. **Commits:** `f456121`, `928fd03`.
- **Changed:** independent reviews of the reader contract, canonical/native accounting, and resume/BENCH arithmetic; admitted-pool preflight. The approved 30/20/10/40 shares did not bind how examples are built, reused or counted, so the line stopped before choosing.
- **Disposition:** `FRONTIER_MODEL_REVIEW_REQUIRED` (admission V2). Tests: 259 passed. Six probe slots used: 0.
- **Evidence:** `docs/reports/PAIRED_READER_BENCH_SESSION_REPORT.md`, `docs/reports/BC_10M_PROBE_ADMISSION_DECISION_V2.md`.

## 4 · 2026-10-05 19:32–19:45 · frontier reader decision v1 and profile measurement

- **Base:** `928fd03`. **Commits:** `bd882ce`, `da8dc18`, `1b114ff`.
- **Changed:** Frontier Reader/Curriculum Decision v1 recorded verbatim before implementation (`READER_DESIGN_AUTHORIZED`). The TRAIN empirical corruption profile was implemented and measured: 92.0492% of retained weight was punctuation, case and whitespace, and 508 of 842 raw-different records were lexically identical. Nothing was filtered or reweighted; the line stopped.
- **Disposition:** `FRONTIER_MODEL_REVIEW_REQUIRED` (admission V3). Tests: 275 passed. Six probe slots used: 0.
- **Evidence:** `docs/reviews/FRONTIER_READER_CURRICULUM_DECISION_V1.md`, `docs/reports/EMPIRICAL_CORRUPTION_PROFILE_QUALIFICATION.md`, `docs/reports/BC_10M_PROBE_ADMISSION_DECISION_V3.md`, `docs/reports/FRONTIER_READER_IMPLEMENTATION_SESSION_REPORT.md`.

## 5 · 2026-10-05 20:25–22:02 · lexical corruption decision v2 and reader implementation

- **Base:** `1b114ff`. **Commits:** `ab8fe95`…`28298ad` (5).
- **Changed:** Frontier Corruption-Profile Decision v2 recorded before implementation (`CORRUPTION_PROFILE_REVISION_AUTHORIZED`, lexical-first profile). Profile implemented with independent parity (profile estimation qualified); lexical mixed reader and complete-update qualification implemented; inconsistent checkpoint exposure and optimizer clocks rejected; C101 component reduction order preserved across cold resume. Six seed-42 pilot configurations written; none run.
- **Disposition:** none committed for this range. The session's admission V4 was still a draft at the time of entry 6 (qualification attempt 03 in progress after a reproduced and repaired C101 mid-resume failure).
- **Tests:** 372 passed (`experiments/manifests/lexical_reader_v2/integrated-component-order-repair-validation.attempt01.json`). Six probe slots used: 0.
- **Evidence:** `docs/reviews/FRONTIER_CORRUPTION_PROFILE_DECISION_V2.md`, `docs/reports/LEXICAL_CORRUPTION_PROFILE_V2_QUALIFICATION.md`, `docs/reviews/LEXICAL_CORRUPTION_PROFILE_V2_INDEPENDENT_REVIEW.md`.

## 6 · 2026-10-05 22:50 · repository conventions, step log and orchestration page

- **Base:** `28298ad`.
- **Step:** set the conventions a reviewed research repository needs, and make progress visible.
- **Changed:** `AGENTS.md` rewritten: every existing rule kept, plus authority and scope, evidence, layout and naming, reproducibility, sources, Git and publishing, orchestration upkeep, and log rules. `CLAUDE.md` created; it imports `AGENTS.md`, so there is one copy of the rules. `docs/LOG.md` created with entries 1–5 backfilled. `ORCHESTRATION.html`, first written at 20:05 against `1b114ff` as a local file, was realigned to `28298ad`, switched to repository-relative paths, given a change-log timeline, and prepared for commit.
- **Disposition:** none (documentation only).
- **Orchestration:** step 1 marked done (decision v2); step 3 implemented; step 4 in progress; counts updated to 42 commits, 34 reports, 16 independent reviews, 372 passing tests.
- **Published:** committed on `main` (no branch, so no merge) and pushed while the attempt-03 qualification session was still running. Only this entry's files were staged, by name; that session's uncommitted work was left untouched. The push also published its five unpushed commits (`ab8fe95`…`28298ad`), so the publication-safety scan covered the whole push range: `experiments/manifests/orchestration/publication-safety.attempt01.json`.
- **Left undone:** realign the orchestration page again when admission V4 is committed.

## 7 · 2026-10-06 00:20 · lexical reader and paired qualification close-out

- **Base:** `e4b2eb4`; native code freeze `28298ad`.
- **Step:** finish lexical profile/reader qualification, full native BENCH, independent fairness, cost and admission V4.
- **Changed:** seven required reports, retained safe attempt receipts and final validation, complete-native aggregate and six-probe cost calculator, plus seven cost-accounting tests. The separate conventions commit is preserved; all eight frozen runtime-source hashes remain unchanged.
- **Disposition:** `AUTHORIZE_10M_BC_DEVELOPMENT_PROBES`. Final suite: 372 passed in 33.25s, TF32 disabled. Six probe slots used: 0.
- **Evidence:** all four cold resumes match 21 complete updates 2–22 exactly; B 5/100/258 BENCH (1,202.824593s sustained), C 5/100/76 (1,200.279867s). Independent review checks all 181 shared queues and all 182 additional B queues; all per-segment concentration alarms are false. Conservative rates B 7,037.941399 / C 2,044.193293 anchors/sec. All-six forecast 11.442153h including one 25% reserve; final-paper campaign remains unpriced.
- **Failures retained:** attempt01 clock rejection gaps; attempt02 C-mid JSON reduction-order failure; independent-checker and generator failures. The current code makes all exact attempt03 gates pass without tolerance relaxation.
- **Orchestration:** realignment follows in the next documentation commit against this qualification record, with light/dark/phone checks. The page is clean and has no other worktree checkout.
- **Left undone:** all six actual 10M recipes, learned-quality/LR selection, final 150M/final seeds, sealed inference, protocol freeze, cloud/production changes and unrelated units 7/8. Actual scientific runs require an explicitly authorized NEW session.
