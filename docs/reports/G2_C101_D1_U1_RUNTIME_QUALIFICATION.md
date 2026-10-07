# C101 D1-U1 Generation-2 runtime qualification

FACT: Reviewed source base `9824752f98509dfec904119119d460f8144a103d` at 2026-10-07T10:31:21.254413+00:00. BENCH source commit `32c97f7a3ae26ea84730af130727d39a47ac82dc`; each process records its config/data/code hashes and clean or captured dirty bookkeeping state. All runs use development seed 42 and qualification IDs. All seven scientific recipes remain AUTHORIZED_UNSTARTED.

MEASURED RESULT: Five warmups, 100 timed actual updates and 1202.902209s sustained pass, with 179 total actual updates and 5,872,244 canonical exposures. All three phases are covered: {"P0": 3911018, "P1": 1567454, "P2": 393772}. Conservative throughput is 2018.223078 canonical anchors/s; total BENCH elapsed time is 5677.699602s.

MEASURED RESULT: Both complete 2,984-case panels and both 304-case greedy/forced diagnostics are retained. Initial full-panel time is 2398.301557s; endpoint full-panel time is 65.546787s. Initial statuses: {"abstained": 522, "completed": 377, "invalid_or_capped": 2085}; endpoint statuses: {"completed": 2969, "invalid_or_capped": 15}. Every invalid/capped output remains included. These are runtime and failure-accounting results, without utility, H1, quality-based LR selection or comparator-adequacy claims.

CALCULATION: Conservative throughput is the minimum of full sustained update-wall throughput, last-quartile update-wall throughput, and charge divided by the complete sustained loop including guards and journal/system snapshots. Snapshot rates below divide dense array bytes by the complete save/publication/readback duration; they are composite rates and are not cache-cold or pure device bandwidth claims.

| Snapshot | Array bytes | Complete save seconds | Composite MiB/s |
|---|---:|---:|---:|
| initial | 1,617,471,512 | 3.694396 | 417.535 |
| boundary | 1,617,471,512 | 3.774829 | 408.639 |
| mid | 1,617,471,512 | 3.681558 | 418.991 |
| final | 1,617,471,512 | 3.829853 | 402.768 |

MEASURED RESULT: Fresh boundary replay matches updates 6–25 exactly in 346.550507s, with 1.769445s load time. Fresh mid-update replay completes pending update 6 and exactly matches updates 7–26, in 362.886012s, with 1.746186s load time. Loss, clocks, denominators, native consumption and deterministic state hashes match exactly on both paths; no tolerance was relaxed.

FACT: Evidence: `experiments/manifests/generation_2/bench-C101-D1-U1.attempt01.json`, the two `cold-C101-D1-U1.attempt01.*.json` receipts, and corresponding complete external `bench-v1/` and `cold-resume-v1/` artifacts. Full six-stream independent reconstruction, expanded archived/ByT5 evaluations, final cost/storage and launch admission remain pending until all required artifacts close. Qualification weights remain retained and forbidden as scientific initializers.

G2_C101_D1_U1_RUNTIME_AND_COLD_PATHS_QUALIFIED
