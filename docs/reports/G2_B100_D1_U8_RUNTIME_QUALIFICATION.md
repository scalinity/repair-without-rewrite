# B100 D1-U8 Generation-2 runtime qualification

FACT: Reviewed source base `b273ab8e36abdd5f6564f7c179e255c6f996caa4` at 2026-10-07T12:05:26.775173+00:00. BENCH source commit `9824752f98509dfec904119119d460f8144a103d`; each process records its config/data/code hashes and clean or captured dirty bookkeeping state. All runs use development seed 42 and qualification IDs. All seven scientific recipes remain AUTHORIZED_UNSTARTED.

MEASURED RESULT: Five warmups, 100 timed actual updates and 1200.672635s sustained pass, with 1,699 total actual updates and 6,967,298 canonical exposures. All three phases are covered: {"P0": 4632706, "P1": 1862698, "P2": 471894}. Conservative throughput is 5361.484296 canonical anchors/s; total BENCH elapsed time is 5559.459424s.

MEASURED RESULT: Both complete 2,984-case panels and both 304-case greedy/forced diagnostics are retained. Initial full-panel time is 3472.733069s; endpoint full-panel time is 362.789346s. Initial statuses: {"capped": 2922, "invalid_byte_decoding": 62}; endpoint statuses: {"capped": 28, "completed": 2943, "invalid_byte_decoding": 13}. Every invalid/capped output remains included. These are runtime and failure-accounting results, without utility, H1, quality-based LR selection or comparator-adequacy claims.

CALCULATION: Conservative throughput is the minimum of full sustained update-wall throughput, last-quartile update-wall throughput, and charge divided by the complete sustained loop including guards and journal/system snapshots. Snapshot rates below divide dense array bytes by the complete save/publication/readback duration; they are composite rates and are not cache-cold or pure device bandwidth claims.

| Snapshot | Array bytes | Complete save seconds | Composite MiB/s |
|---|---:|---:|---:|
| initial | 1,611,136,656 | 3.722129 | 412.801 |
| boundary | 1,611,136,656 | 3.978661 | 386.185 |
| mid | 1,611,136,656 | 3.851955 | 398.888 |
| final | 1,611,136,656 | 4.134528 | 371.626 |

MEASURED RESULT: Fresh boundary replay matches updates 6–25 exactly in 36.464412s, with 1.736687s load time. Fresh mid-update replay completes pending update 6 and exactly matches updates 7–26, in 37.491303s, with 1.719574s load time. Loss, clocks, denominators, native consumption and deterministic state hashes match exactly on both paths; no tolerance was relaxed.

FACT: Evidence: `experiments/manifests/generation_2/bench-B100-D1-U8.attempt01.json`, the two `cold-B100-D1-U8.attempt01.*.json` receipts, and corresponding complete external `bench-v1/` and `cold-resume-v1/` artifacts. Full six-stream independent reconstruction, expanded archived/ByT5 evaluations, final cost/storage and launch admission remain pending until all required artifacts close. Qualification weights remain retained and forbidden as scientific initializers.

G2_B100_D1_U8_RUNTIME_AND_COLD_PATHS_QUALIFIED
