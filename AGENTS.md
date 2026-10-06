# Repair Without Rewrite — research repository rules

This repository holds the research for *Repair Without Rewrite: A Controlled Comparison of Full-Transcript Generation and Compact Editing Under Matched Source Exposure*. It is public, isolated from production LocalFlow, and its work will be reviewed by others: every claim, decision and failure must be traceable from these files.

## Authority and scope

- Supplied v1.2 inputs in `docs/design-inputs/` are immutable; their hashes are in `docs/design-inputs/SHA256SUMS`. The v1.2 PDF is canonical; the extracted canonical Markdown is byte-identical to the PDF's embedded attachment.
- Before consequential changes, read `KICKOFF_PROMPT.txt`, `PACKAGE_README.md`, the accepted review, the registry and the canonical specification, then the newest `docs/reports/BC_10M_PROBE_ADMISSION_DECISION_V*.md` and `docs/reviews/PROSPECTIVE_AMENDMENTS.md`.
- Only bounded foundation/development is authorized. No final seeds 1729/2718/31415, final 150M runs, sealed candidate inference, protocol freeze, cloud spending or production changes. No remote publication unless the owner's authorization for that session includes it. No human annotation or listening queues.
- The specification and registry change only through a prospective amendment appended to `docs/reviews/PROSPECTIVE_AMENDMENTS.md` before any affected result exists. Never change a protocol, margin, population or recipe after seeing outcomes.
- A consequential scientific choice that no accepted decision binds is not the implementer's to make. Stop that line of work with `FRONTIER_MODEL_REVIEW_REQUIRED` and write the request: the measured problem, its evidence, the smallest candidate choices, and the controls or confounds. Record the returned frontier decision verbatim as `docs/reviews/FRONTIER_<TOPIC>_DECISION_V<n>.md`, with its date, reviewed commit and disposition, and commit it alone before any implementation.
- Owner authorization is required, separately each time, before: the six seed-42 10M probes, protocol freeze (PUB-GATE 3), final training, sealed or final inference, cloud spending, publication, and any agreement that shares the owner's details (e.g. SLUE access).
- Stop conditions and the forbidden compensations are in `KICKOFF_PROMPT.txt` section 15. A stop is reported, not worked around.

## Evidence

- Every measured claim points to an on-disk artifact. No result exists only in a chat message.
- Before every expensive run, record: clean or explicitly captured dirty state, config hash, data-manifest hash, code commit, seed, a unique output directory, and a verified resume path.
- Number attempts (`*.attempt01.json`, `attempt02`, …). Keep failed attempts beside successful ones; never overwrite, delete or amend history to hide a failure.
- Label claims as FACT, MEASURED RESULT, CALCULATION, INFERENCE or PROPOSED NEXT ACTION. In cost tables, keep MEASURED, CALCULATED, ASSUMED and UNPRICED apart.
- Report unmeasured things as unmeasured. Equality over zero rows is not a pass; a planned action is never described as done.
- Every report ends with exactly one disposition token on its own last line. A report never embeds its own future commit hash.
- High-risk mathematics, scoring, accounting and resume work gets an independent review through a separate code path, saved as `docs/reviews/<TOPIC>_INDEPENDENT_REVIEW.md`. CPU-only reviews may overlap an accelerator job.
- References and latent annotations never enter inference input. Final or sealed references never enter training, calibration or prompt tuning. Record every use of calibration rows in `experiments/manifests/development_calibration_consumption*.json`.

## Layout and naming

- `docs/design-inputs/` immutable inputs · `docs/reviews/` decisions, independent reviews and amendments · `docs/reports/` measured outcomes, named in `UPPER_SNAKE_CASE.md`, versioned `_V2`, `_V3` rather than rewritten · `experiments/manifests/<line>/<name>.attemptNN.json` receipts · `benchmarks/` entry points · `src/`, `tests/`, `configs/`.
- `exports/` and `checkpoints/` are ignored and hold private payloads. Raw text, audio, model weights, private alignment audits, credentials, environments and agent state are never committed. Public manifests carry hashes, counts and permitted stable IDs only.
- Public files use repository-relative paths; absolute local paths are non-public identifiers. Preserve an original that contained one outside Git, then publish a separately labelled public version.

## Reproducibility

- Python 3.12. Create the environment with `uv sync --locked --no-build`; run tests with `MLX_ENABLE_TF32=0 .venv/bin/python -m pytest`. Reproduce the baseline test count before changing anything and again at the end, and save both receipts in the line's manifests.
- Only the root session changes the dependency lock. Development seed is 42; seeds 1729, 2718 and 31415 are reserved for final runs.
- Do not run build, compiler or bundler commands. Python execution and tests are allowed. No React `useEffect`.
- One accelerator workload at a time: coordinate with root before any MLX training or timing. Keep correctness and test runs bounded; no 10M probe before its prerequisite gates.

## Sources and prior work

- Cite sources by URL or DOI and verify primary sources before relying on them. Positioning against the closest prior work follows accepted finding F01.
- Record licence, access conditions and attribution for every third-party dataset, model and table (see `docs/reports/PUBLIC_SOURCE_QUALIFICATION.md` and `configs/tokenizer_development/ATTRIBUTION.md`). The repository has no licence yet; do not add one without the owner.

## Git and publishing

- Workers are not alone in this repository: respect others' edits and change only assigned files. The root session makes commits.
- Use the existing Git identity. No co-author, "Generated with" or other attribution lines in commits, pull requests, tags or notes.
- Commit messages are impersonal and technical: what changed and why, in the imperative. Small reviewable commits, one per qualified step.
- Stage files by name; never `git add -A`. Never commit agent or runtime state (`.claude/`, `.codex/`, `.agent/`, `.agents/` are ignored). Do not rewrite history.
- Before any push, scan the staged change for credentials and non-functional personal identifiers, including absolute local paths, and save the receipt as `publication-safety.attemptNN.json` in the line's manifests.

## Keep the orchestration page current

`ORCHESTRATION.html` is the plain-language progress page for the paper. It is committed so reviewers can follow the work.

- After every completed step — a commit that finishes a unit of work, records a decision, changes what may run next, or moves a file-ownership boundary — realign the page in the same commit or the next. Update the as-of commit, the "where the paper is" station, each step's state and badge, the eligibility lines, the lanes, open questions, and the counts (commits, reports, independent reviews, passing tests). Add the step to its change-log timeline.
- Check every figure against the record — the newest admission decision, the amendments, receipts and `git log` — never against memory of the session.
- Realignment edits content in place and keeps the layout. A new section or layout change is a design change: plan it first, then build it.
- Keep the page public-safe (repository-relative paths only). After editing, confirm there is no horizontal overflow at the viewer's window width and at phone width, and do not pin the viewer's tab with Playwright's `browser_resize`.
- If another session owns the page or has uncommitted changes in it, leave it and say in the log entry what would have changed.

## Log

`docs/LOG.md` is the append-only history of the work, newest entry last. Every completed step appends one entry in the same commit as the change. Each entry gives the date and time, the base commit, the step, the files changed, the disposition, the evidence, what was realigned on the orchestration page, and what was left undone. Never edit or delete a past entry; a correction is a new entry that names the one it corrects.
