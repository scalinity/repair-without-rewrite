# Generation-2 native BENCH qualification

FACT: Reported at 2026-10-07T14:25:34.108692+00:00, reviewed source commit `daaf98f59d1567d2aa5f85982769a6a9d4c287a3`. All runs use development seed 42 and distinct qualification IDs. All seven scientific recipes remain AUTHORIZED_UNSTARTED.

MEASURED RESULT: All six fixed native streams completed five warmups, 100 timed actual updates, at least 1,200 seconds sustained while finishing the last update, both complete 2,984-case development evaluations, and the frozen 304-case greedy and forced-loss diagnostics. No qualification weight may initialize a scientific recipe.

| Stream | Warmups | Timed updates | Sustained seconds | Complete actual updates | Conservative anchors/s | Initial panel seconds | Final panel seconds |
|---|---:|---:|---:|---:|---:|---:|---:|
| B100-D0-U8.attempt01 | 5 | 100 | 1200.150549 | 1317 | 4141.473753 | 3797.530000 | 452.950826 |
| C101-D0-U8.attempt01 | 5 | 100 | 1200.462670 | 612 | 1732.061355 | 2595.745285 | 71.343932 |
| B100-D1-U1.attempt01 | 5 | 100 | 1200.841516 | 352 | 6748.207731 | 3841.419134 | 393.609855 |
| C101-D1-U1.attempt01 | 5 | 100 | 1202.902209 | 179 | 2018.223078 | 2398.301557 | 65.546787 |
| B100-D1-U8.attempt01 | 5 | 100 | 1200.672635 | 1699 | 5361.484296 | 3472.733069 | 362.789346 |
| C101-D1-U8.attempt01 | 5 | 100 | 1201.532719 | 654 | 1873.663500 | 2222.403708 | 54.512534 |

CALCULATION: The conservative rate is the minimum of the full sustained update-wall rate, last-quartile update-wall rate, and sustained charge divided by complete loop elapsed time. The last includes guards, journal writes and system snapshots. Qualification-only state hashing for updates 6–26 is separately timed and charged in qualification elapsed time. All three phase populations are covered. Total BENCH update counts may differ between arms because sustained timing ends by wall time; independent equality applies to their common nonempty actual-update prefix. The complete frozen scientific ledger equality is independently qualified separately.

MEASURED RESULT: External checkpoint timing below includes complete publication and readback; it is not a cache-cold or power-loss claim. Detailed write, exact-array readback and publication/fsync/hash/readback components remain in each receipt.

| Stream | Initial save s | Boundary save s | Mid-update save s | Final save s | Boundary load s | Mid-update load s |
|---|---:|---:|---:|---:|---:|---:|
| B100-D0-U8.attempt01 | 4.051972 | 4.418299 | 4.273988 | 4.981840 | 1.885643 | 1.855207 |
| C101-D0-U8.attempt01 | 3.904708 | 3.755973 | 3.696439 | 4.019745 | 1.907516 | 1.818213 |
| B100-D1-U1.attempt01 | 3.803000 | 4.604758 | 4.246199 | 4.740712 | 1.845983 | 1.709391 |
| C101-D1-U1.attempt01 | 3.694396 | 3.774829 | 3.681558 | 3.829853 | 1.769445 | 1.746186 |
| B100-D1-U8.attempt01 | 3.722129 | 3.978661 | 3.851955 | 4.134528 | 1.736687 | 1.719574 |
| C101-D1-U8.attempt01 | 3.703801 | 3.794894 | 3.609348 | 3.721230 | 1.723877 | 1.710072 |

CALCULATION: Dense array bytes divided by complete save/publication/readback or fresh-process load seconds gives composite snapshot throughput. It includes serialization, copying and validation and is not pure device bandwidth.

| Stream | Snapshot | Array bytes | Composite save MiB/s | Composite load MiB/s |
|---|---|---:|---:|---:|
| B100-D0-U8.attempt01 | boundary | 1,611,136,656 | 347.758 | 814.841 |
| B100-D0-U8.attempt01 | final | 1,611,136,656 | 308.420 | — |
| B100-D0-U8.attempt01 | initial | 1,611,136,656 | 379.198 | — |
| B100-D0-U8.attempt01 | mid | 1,611,136,656 | 359.500 | 828.209 |
| C101-D0-U8.attempt01 | boundary | 1,617,471,512 | 410.690 | 808.665 |
| C101-D0-U8.attempt01 | final | 1,617,471,512 | 383.741 | — |
| C101-D0-U8.attempt01 | initial | 1,617,471,512 | 395.046 | — |
| C101-D0-U8.attempt01 | mid | 1,617,471,512 | 417.305 | 848.383 |
| B100-D1-U1.attempt01 | boundary | 1,611,136,656 | 333.677 | 832.348 |
| B100-D1-U1.attempt01 | final | 1,611,136,656 | 324.107 | — |
| B100-D1-U1.attempt01 | initial | 1,611,136,656 | 404.023 | — |
| B100-D1-U1.attempt01 | mid | 1,611,136,656 | 361.853 | 898.858 |
| C101-D1-U1.attempt01 | boundary | 1,617,471,512 | 408.639 | 871.765 |
| C101-D1-U1.attempt01 | final | 1,617,471,512 | 402.768 | — |
| C101-D1-U1.attempt01 | initial | 1,617,471,512 | 417.535 | — |
| C101-D1-U1.attempt01 | mid | 1,617,471,512 | 418.991 | 883.377 |
| B100-D1-U8.attempt01 | boundary | 1,611,136,656 | 386.185 | 884.730 |
| B100-D1-U8.attempt01 | final | 1,611,136,656 | 371.626 | — |
| B100-D1-U8.attempt01 | initial | 1,611,136,656 | 412.801 | — |
| B100-D1-U8.attempt01 | mid | 1,611,136,656 | 398.888 | 893.535 |
| C101-D1-U8.attempt01 | boundary | 1,617,471,512 | 406.478 | 894.809 |
| C101-D1-U8.attempt01 | final | 1,617,471,512 | 414.525 | — |
| C101-D1-U8.attempt01 | initial | 1,617,471,512 | 416.475 | — |
| C101-D1-U8.attempt01 | mid | 1,617,471,512 | 427.374 | 902.033 |

MEASURED RESULT: MLX-reported peak allocation across each complete qualification process:

| Stream | Peak MLX allocation bytes | Peak GiB |
|---|---:|---:|
| B100-D0-U8.attempt01 | 4,092,727,684 | 3.811650 |
| C101-D0-U8.attempt01 | 3,365,794,634 | 3.134641 |
| B100-D1-U1.attempt01 | 4,093,214,596 | 3.812103 |
| C101-D1-U1.attempt01 | 3,365,981,777 | 3.134815 |
| B100-D1-U8.attempt01 | 4,092,593,540 | 3.811525 |
| C101-D1-U8.attempt01 | 3,365,813,566 | 3.134658 |

MEASURED RESULT: Every cell begins from exactly the accepted historical seed-42 initial arrays for its arm. The independent audit verifies the serialized array SHA256 in all six initial snapshots; the initial optimizer step, committed exposure and pending charge are zero. No qualification state is transferred into science.

FACT: B100 has 100,686,336 parameters and C101 has 101,081,859. Both keep the accepted native objectives, BF16 working weights and FP32 masters/moments/accumulators/sensitive reductions. B microbatch is 16 and C is 4. Each actual update divides by its own full label denominators once; it is not divided again by microbatch count or eight. LR follows committed canonical exposure with the accepted 200k warmup and continuous cosine schedule. G1 checkpoint validation remains unchanged. G2 uses `paired_complete_actual_update_resume_g2_v1`, including reader scope, master/subqueue/actual clocks, pending queue, gradients, optimizer/RNG state and forward/hash identity.

FACT: Evidence is `experiments/manifests/generation_2/bench-*.attempt01.json`, corresponding `cold-*.json`, `independent-native.attempt01.json`, and complete external `bench-v1/` and `cold-resume-v1/` artifacts. Initial/endpoint outputs and every invalid or incomplete decode are retained. These are runner/resource qualification results, without quality-based selection or an H1 adequacy claim.

G2_NATIVE_BENCH_QUALIFIED
