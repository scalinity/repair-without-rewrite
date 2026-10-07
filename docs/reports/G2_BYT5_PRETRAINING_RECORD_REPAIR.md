# G2 ByT5 pre-training record repair

FACT: Reviewed source base `54d707e1c71e1e23cf13441b5d878b2bd049da23`. Qualification attempt 01 stopped with `TypeError: Object of type set is not JSON serializable` while writing its first initial-evaluation score. The canonical scorer returns sets. The runner now writes records through the existing, unchanged `src/scoring/triple.py::serialize`; scoring, populations, capacities, optimizer, backend and seed are unchanged.

MEASURED RESULT: Independent portable CPU readback confirms the retained initial checkpoint has zero completed optimizer updates and empty optimizer state. The partial initial records file has zero bytes, no steps file and no COMPLETE marker. The traceback and original runner control flow establish that the first CAL case `1093-132891-0004` was decoded and scored before writing failed. Its decoded output is unavailable; no score or output is reconstructed. One actual CAL reference use is retained separately from complete-panel records.

MEASURED RESULT: The failed attempt consumed 14.011871291 seconds. The CPU mechanical audit consumed 1.646109458 seconds. Both durations enter the measured cost sum. The complete 1,198,624,003-byte initial snapshot and failed partial remain retained. Evidence: `experiments/manifests/generation_2/byt5-qualification.attempt01.json` and `byt5-record-repair.attempt01.json`.

MEASURED RESULT: Four synthetic scorer statuses round-trip every field using an independent recursive conversion and preserve aggregate values. The targeted CPU suite passes 33 checks, zero failures/skips; evidence: `qualification-cpu-tests.attempt08.json`. The final integrated suite and completed ByT5 independent audit remain unrun.

FACT: Attempt 02 is predeclared before execution as the sole 100-update training trajectory, starting again from unchanged official weights with the same config, corpus, panel and seed hashes. Attempt 01 trained zero updates. No numerical replay is consumed; no automatic retry is allowed. Both archived expanded endpoints already pass with zero new training. All six native BENCHs and twelve cold paths remain accepted and will not be repeated. All seven scientific recipes remain AUTHORIZED_UNSTARTED.

PASS_MECHANICAL_PRETRAINING_RECORD_REPAIR
