# B100 D1-U1 Generation-2 runtime qualification

FACT: Reviewed source base `32c97f7a3ae26ea84730af130727d39a47ac82dc` at 2026-10-07T08:44:12.285731+00:00. BENCH source commit `0158153d65347fe17ada112b0cbca8d11ee78476`; each process records its config/data/code hashes and clean or captured dirty bookkeeping state. All runs use development seed 42 and qualification IDs. All seven scientific recipes remain AUTHORIZED_UNSTARTED.

MEASURED RESULT: Five warmups, 100 timed actual updates and 1200.841516s sustained pass, with 352 total actual updates and 11,548,047 canonical exposures. All three phases are covered: {"P0": 7691008, "P1": 3085771, "P2": 771268}. Conservative throughput is 6748.207731 canonical anchors/s; total BENCH elapsed time is 6433.181861s.

MEASURED RESULT: Both complete 2,984-case panels and both 304-case greedy/forced diagnostics are retained. Initial full-panel time is 3841.419134s; endpoint full-panel time is 393.609855s. Initial statuses: {"capped": 2922, "invalid_byte_decoding": 62}; endpoint statuses: {"capped": 8, "completed": 2976}. Every invalid/capped output remains included. These are runtime and failure-accounting results, without utility, H1, quality-based LR selection or comparator-adequacy claims.

CALCULATION: Conservative throughput is the minimum of full sustained update-wall throughput, last-quartile update-wall throughput, and charge divided by the complete sustained loop including guards and journal/system snapshots. Snapshot rates below divide dense array bytes by the complete save/publication/readback duration; they are composite rates and are not cache-cold or pure device bandwidth claims.

| Snapshot | Array bytes | Complete save seconds | Composite MiB/s |
|---|---:|---:|---:|
| initial | 1,611,136,656 | 3.803000 | 404.023 |
| boundary | 1,611,136,656 | 4.604758 | 333.677 |
| mid | 1,611,136,656 | 4.246199 | 361.853 |
| final | 1,611,136,656 | 4.740712 | 324.107 |

MEASURED RESULT: Fresh boundary replay matches updates 6–25 exactly in 88.728836s, with 1.845983s load time. Fresh mid-update replay completes pending update 6 and exactly matches updates 7–26, in 90.303398s, with 1.709391s load time. Loss, clocks, denominators, native consumption and deterministic state hashes match exactly on both paths; no tolerance was relaxed.

FACT: Evidence: `experiments/manifests/generation_2/bench-B100-D1-U1.attempt01.json`, the two `cold-B100-D1-U1.attempt01.*.json` receipts, and corresponding complete external `bench-v1/` and `cold-resume-v1/` artifacts. Full six-stream independent reconstruction, expanded archived/ByT5 evaluations, final cost/storage and launch admission remain pending until all required artifacts close. Qualification weights remain retained and forbidden as scientific initializers.

G2_B100_D1_U1_RUNTIME_AND_COLD_PATHS_QUALIFIED
