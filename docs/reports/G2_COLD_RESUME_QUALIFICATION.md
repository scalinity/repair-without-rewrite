# Generation-2 cold resume qualification

FACT: Reported at 2026-10-07T14:25:34.123556+00:00, reviewed source commit `daaf98f59d1567d2aa5f85982769a6a9d4c287a3`. All runs use development seed 42 and distinct qualification IDs. All seven scientific recipes remain AUTHORIZED_UNSTARTED.

MEASURED RESULT: All six boundary paths and six mid-update paths pass exact deterministic replay. No numerical tolerance was relaxed. Boundary snapshots follow actual update 5 and replay updates 6–25. Mid snapshots follow one completed microbatch of pending update 6; replay finishes update 6, then completes updates 7–26. The pending completion is additional to the next twenty complete actual updates.

| Stream | Path | Matched actual updates | Next complete updates | Load seconds | Total path seconds |
|---|---|---:|---:|---:|---:|
| B100-D0-U8.attempt01 | boundary | 20 | 20 | 1.885643 | 41.958883 |
| B100-D0-U8.attempt01 | mid | 21 | 20 | 1.855207 | 37.367043 |
| C101-D0-U8.attempt01 | boundary | 20 | 20 | 1.907516 | 69.722532 |
| C101-D0-U8.attempt01 | mid | 21 | 20 | 1.818213 | 69.885910 |
| B100-D1-U1.attempt01 | boundary | 20 | 20 | 1.845983 | 88.728836 |
| B100-D1-U1.attempt01 | mid | 21 | 20 | 1.709391 | 90.303398 |
| C101-D1-U1.attempt01 | boundary | 20 | 20 | 1.769445 | 346.550507 |
| C101-D1-U1.attempt01 | mid | 21 | 20 | 1.746186 | 362.886012 |
| B100-D1-U8.attempt01 | boundary | 20 | 20 | 1.736687 | 36.464412 |
| B100-D1-U8.attempt01 | mid | 21 | 20 | 1.719574 | 37.491303 |
| C101-D1-U8.attempt01 | boundary | 20 | 20 | 1.723877 | 62.238301 |
| C101-D1-U8.attempt01 | mid | 21 | 20 | 1.710072 | 65.151213 |

FACT: Each fresh process verifies the complete control artifact and snapshot before model construction. Loss, optimizer step, canonical clock, denominators, presentation/native-consumption records and combined deterministic model/optimizer/accumulator/reader hash match the saved control at every required update. Persisted final snapshot arrays and metadata are reconstructed separately with NumPy by `benchmarks/g2_native_independent.py`. No G2 stream/trainer/save/load/state-hash helper is imported by that reviewer.

FACT: Evidence is `experiments/manifests/generation_2/cold-*.attempt01.*.json`, `independent-native.attempt01.json` and corresponding complete external `cold-resume-v1/` artifacts. All resume states are qualification-only and forbidden as scientific initializers.

G2_EXACT_COLD_RESUME_QUALIFIED
