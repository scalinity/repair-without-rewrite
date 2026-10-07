# Generation-2 U1/U8 geometry qualification

FACT — Immutable whole-presentation 32,768-anchor master queues precede all student training. U8 cuts each master after the first whole presentation satisfying `8C >= jQ` for each `j=1..7`; its eighth contiguous subqueue reaches the original endpoint. Every subqueue is nonempty and their ordered concatenation equals U1 exactly. There is no exact 4,096-anchor threshold.

| Condition | Masters / U1 updates | U8 updates | Endpoint exposure | Final ordinal | U8 charge range |
| --- | ---: | ---: | ---: | ---: | ---: |
| D0 | 305 | 2,440 | 10,007,223 | 134,590 | 3,887–4,283 |
| D1 | 305 | 2,440 | 10,006,223 | 136,754 | 3,941–4,250 |

MEASURED RESULT — Separate accepted-reader reconstruction reproduces every presentation in both complete ledgers. Independent integer prefixes/bisect reproduce every first-crossing cut, B target-plus-EOS denominator, C action/start/end/vocabulary denominator, B16/C4 microbatch partition, completed exposure and LR sample. CPU scientific cursor restore is checked at every actual boundary. Full-model optimizer/checkpoint/resume qualification remains pending.

FACT — The 200,000-exposure warmup and continuous cosine clock use completed actual exposure. FP32 masters/moments/accumulators and sensitive arithmetic, BF16 working operations, inherited optimizer, clipping and objective normalization remain fixed. No second division or rescaling is added. U8 bundles update frequency, clipping, noise, LR sampling, moment horizon, decay and normalization granularity; it does not isolate step count alone.

FACT — B/C and U1/U8 share exact presentations and exposure within D. Across D, endpoint exposure differs by 1,000 and final ordinals/interleaving differ; cross-D ledger equality is not claimed.

| Frozen identity | D0 SHA256 | D1 SHA256 |
| --- | --- | --- |
| Full ledger | `21c3f5838f5c7e85f258e8eef25b2b38884a2023199afc5d1852d68155b04f2f` | `4927980826095d6e2f5d74f37c17d43e233acf3356ccb99d16a1930b29b3a60f` |
| Master queues | `f522465b45f41ae75052625878cd3c2292fb708b64f18074dd0a3830cfe414d8` | `0360ec02e5a3e8a6e64817e4f7c37c2f872cf40f5ce29163adc946ef574c290f` |
| Actual updates | `607fefa427cc31672ca93b080d291847a91829917d285c8bb5e6df078e9df5b3` | `1948f01d5c8a134e9cb77dd50742a8f45030da7e131e3148a2bd4ab9516c1349` |
| 304-case diagnostics | `87d8c57cc98a32ce4db654559859d4986e5781bd8a178599f8dbda9c7f5d4ac1` | `847133c3fa187ac185e988c5f6271675ba1993eba1b61f84b020ea798a97e007` |

MEASURED RESULT — Both diagnostic panels independently reproduce: 64 TRAIN lexical-error cases, 64 lexical-zero cases, their 128 identity views, and clean/mixed views of 24 generated TRAIN bases present in the actual ledger. Selection uses the frozen seed-42 SHA namespaces, never student outputs. Diagnostics are training diagnostics, not held-out adequacy evidence; teacher-forced component losses remain separate from greedy scores.

FACT — Seven hashed configuration manifests freeze the prescribed endpoints and remain AUTHORIZED_UNSTARTED. Scientific cursors reject BENCH cursor scope; compatibility/BENCH/cold/ByT5 qualification weights are forbidden as scientific initializers. No scientific recipe launcher is supplied by this qualification.

Evidence: `experiments/manifests/generation_2/corpus-freeze.attempt01.json`, `independent-corpus.attempt01.json`, `recipe-*.attempt01.json`, and `pre-corpus-full-tests.attempt01.json` (455 passed, zero failures/skips, 42.76 seconds). Full native BENCH, twelve cold replays, ByT5 and cost/admission checks remain unrun.

G2_U1_U8_GEOMETRY_QUALIFIED
