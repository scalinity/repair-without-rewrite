# B100 D0-U8 Generation-2 runtime qualification

FACT: Reviewed source base `40c9839625a83fbd4474b80170ed9800d072daa6` at 2026-10-07T05:40:31.679914+00:00. The BENCH starts from clean source commit `34f22412c82cfb8938a1f0a38490deca0b626f42` with its recorded config/data/code hashes. Both cold processes use the same frozen critical implementation/data identities and explicitly captured later dirty bookkeeping state. All runs are seed 42, qualification-only; all seven scientific recipes remain AUTHORIZED_UNSTARTED.

MEASURED RESULT: Five complete warmups, 100 timed actual updates and 1200.150549 sustained seconds pass. There are 1,317 total actual updates and 5,401,069 canonical exposures. All three phases are covered: P0 3,582,367, P1 1,440,364, P2 378,338. The conservative measured rate is 4141.473753 canonical anchors/s. BENCH elapsed time is 6053.079122s.

MEASURED RESULT: Both complete 2,984-case panels and both frozen 304-case greedy/forced diagnostics are retained. Initial full-panel wall time is 3797.530000s; endpoint wall time is 452.950826s. Initial statuses are {"capped": 2922, "invalid_byte_decoding": 62}; endpoint statuses are {"capped": 1, "completed": 2982, "invalid_byte_decoding": 1}. All capped/invalid records remain included. These counts establish runtime/failure accounting and do not establish useful correction, LR selection, comparator adequacy or H1 evidence.

CALCULATION: The conservative rate is the minimum of sustained update-wall throughput, last-quartile update-wall throughput and charge divided by whole sustained loop time, which includes guards and journal/system-snapshot overhead. Native complete snapshot rates below divide array bytes by complete save/publication/readback elapsed time; they are composite rates, not pure storage bandwidth or cache-cold claims. Detailed components remain in the receipt.

| Snapshot | Dense array bytes | Complete save seconds | Composite MiB/s |
|---|---:|---:|---:|
| initial | 1,611,136,656 | 4.051972 | 379.198 |
| boundary | 1,611,136,656 | 4.418299 | 347.758 |
| mid | 1,611,136,656 | 4.273988 | 359.500 |
| final | 1,611,136,656 | 4.981840 | 308.420 |

MEASURED RESULT: The fresh boundary process exactly matches the next twenty actual updates, 6–25, in 41.958883s, with 1.885643s load time. The fresh mid-update process finishes pending update 6 and then exactly matches updates 7–26: 21 matched actual completions, including the pending completion plus the next twenty, in 37.367043s, with 1.855207s load time. Loss, clock, denominators, native/presentation consumption and deterministic state hashes match at each required update. No tolerance was relaxed.

FACT: Evidence: `experiments/manifests/generation_2/bench-B100-D0-U8.attempt01.json`, `cold-B100-D0-U8.attempt01.boundary.json`, `cold-B100-D0-U8.attempt01.mid.json`, `storage-monitor.attempt06.json` and corresponding complete external `bench-v1/` and `cold-resume-v1/` artifacts. Full independent six-stream/native-state reconstruction remains unrun until all six streams and twelve cold paths complete. Pairwise native B/C consumption, the other five BENCHs, ten other cold paths, archived expanded evaluations, ByT5, complete evaluation tables, retained-storage/cost and launch admission remain pending. Qualification weights are retained and forbidden as scientific initializers.

G2_B100_D0_U8_RUNTIME_AND_COLD_PATHS_QUALIFIED
