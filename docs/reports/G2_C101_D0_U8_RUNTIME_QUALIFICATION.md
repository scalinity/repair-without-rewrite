# C101 D0-U8 Generation-2 runtime qualification

FACT: Reviewed source base `0158153d65347fe17ada112b0cbca8d11ee78476` at 2026-10-07T06:54:49.903881+00:00. BENCH source commit `40c9839625a83fbd4474b80170ed9800d072daa6`; each process records its config/data/code hashes and clean or captured dirty bookkeeping state. All runs use development seed 42 and qualification IDs. All seven scientific recipes remain AUTHORIZED_UNSTARTED.

MEASURED RESULT: Five warmups, 100 timed actual updates and 1200.462670s sustained pass, with 612 total actual updates and 2,509,952 canonical exposures. All three phases are covered: {"P0": 1663211, "P1": 665350, "P2": 181391}. Conservative throughput is 1732.061355 canonical anchors/s; total BENCH elapsed time is 4413.267766s.

MEASURED RESULT: Both complete 2,984-case panels and both 304-case greedy/forced diagnostics are retained. Initial full-panel time is 2595.745285s; endpoint full-panel time is 71.343932s. Initial statuses: {"abstained": 522, "completed": 377, "invalid_or_capped": 2085}; endpoint statuses: {"completed": 2983, "invalid_or_capped": 1}. Every invalid/capped output remains included. These are runtime and failure-accounting results, without utility, H1, quality-based LR selection or comparator-adequacy claims.

CALCULATION: Conservative throughput is the minimum of full sustained update-wall throughput, last-quartile update-wall throughput, and charge divided by the complete sustained loop including guards and journal/system snapshots. Snapshot rates below divide dense array bytes by the complete save/publication/readback duration; they are composite rates and are not cache-cold or pure device bandwidth claims.

| Snapshot | Array bytes | Complete save seconds | Composite MiB/s |
|---|---:|---:|---:|
| initial | 1,617,471,512 | 3.904708 | 395.046 |
| boundary | 1,617,471,512 | 3.755973 | 410.690 |
| mid | 1,617,471,512 | 3.696439 | 417.305 |
| final | 1,617,471,512 | 4.019745 | 383.741 |

MEASURED RESULT: Fresh boundary replay matches updates 6–25 exactly in 69.722532s, with 1.907516s load time. Fresh mid-update replay completes pending update 6 and exactly matches updates 7–26, in 69.885910s, with 1.818213s load time. Loss, clocks, denominators, native consumption and deterministic state hashes match exactly on both paths; no tolerance was relaxed.

FACT: Evidence: `experiments/manifests/generation_2/bench-C101-D0-U8.attempt01.json`, the two `cold-C101-D0-U8.attempt01.*.json` receipts, and corresponding complete external `bench-v1/` and `cold-resume-v1/` artifacts. Full six-stream independent reconstruction, expanded archived/ByT5 evaluations, final cost/storage and launch admission remain pending until all required artifacts close. Qualification weights remain retained and forbidden as scientific initializers.

G2_C101_D0_U8_RUNTIME_AND_COLD_PATHS_QUALIFIED
