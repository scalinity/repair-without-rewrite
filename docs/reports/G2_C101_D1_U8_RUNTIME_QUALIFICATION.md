# C101 D1-U8 Generation-2 runtime qualification

FACT: Reviewed source base `6823b3e0d2cf4ab0233ca935e2dbfcd9a3e48c35` at 2026-10-07T13:14:52.228378+00:00. BENCH source commit `b273ab8e36abdd5f6564f7c179e255c6f996caa4`; each process records its config/data/code hashes and clean or captured dirty bookkeeping state. All runs use development seed 42 and qualification IDs. All seven scientific recipes remain AUTHORIZED_UNSTARTED.

MEASURED RESULT: Five warmups, 100 timed actual updates and 1201.532719s sustained pass, with 654 total actual updates and 2,681,859 canonical exposures. All three phases are covered: {"P0": 1770537, "P1": 714430, "P2": 196892}. Conservative throughput is 1873.663500 canonical anchors/s; total BENCH elapsed time is 3965.826025s.

MEASURED RESULT: Both complete 2,984-case panels and both 304-case greedy/forced diagnostics are retained. Initial full-panel time is 2222.403708s; endpoint full-panel time is 54.512534s. Initial statuses: {"abstained": 522, "completed": 377, "invalid_or_capped": 2085}; endpoint statuses: {"completed": 2979, "invalid_or_capped": 5}. Every invalid/capped output remains included. These are runtime and failure-accounting results, without utility, H1, quality-based LR selection or comparator-adequacy claims.

CALCULATION: Conservative throughput is the minimum of full sustained update-wall throughput, last-quartile update-wall throughput, and charge divided by the complete sustained loop including guards and journal/system snapshots. Snapshot rates below divide dense array bytes by the complete save/publication/readback duration; they are composite rates and are not cache-cold or pure device bandwidth claims.

| Snapshot | Array bytes | Complete save seconds | Composite MiB/s |
|---|---:|---:|---:|
| initial | 1,617,471,512 | 3.703801 | 416.475 |
| boundary | 1,617,471,512 | 3.794894 | 406.478 |
| mid | 1,617,471,512 | 3.609348 | 427.374 |
| final | 1,617,471,512 | 3.721230 | 414.525 |

MEASURED RESULT: Fresh boundary replay matches updates 6–25 exactly in 62.238301s, with 1.723877s load time. Fresh mid-update replay completes pending update 6 and exactly matches updates 7–26, in 65.151213s, with 1.710072s load time. Loss, clocks, denominators, native consumption and deterministic state hashes match exactly on both paths; no tolerance was relaxed.

FACT: Evidence: `experiments/manifests/generation_2/bench-C101-D1-U8.attempt01.json`, the two `cold-C101-D1-U8.attempt01.*.json` receipts, and corresponding complete external `bench-v1/` and `cold-resume-v1/` artifacts. Full six-stream independent reconstruction, expanded archived/ByT5 evaluations, final cost/storage and launch admission remain pending until all required artifacts close. Qualification weights remain retained and forbidden as scientific initializers.

G2_C101_D1_U8_RUNTIME_AND_COLD_PATHS_QUALIFIED
