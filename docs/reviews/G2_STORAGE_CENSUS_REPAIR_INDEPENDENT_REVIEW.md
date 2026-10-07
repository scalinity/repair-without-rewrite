# Independent retained-storage alias census reconstruction

FACT: Recorded 2026-10-07T18:06:34.671882+00:00; reviewed source base `3ba9bd5462f43baf83a454de533c0ad8d19ee869`. This is a mechanical accounting repair; no scientific recipe, population, checkpoint allowance, root policy or model run changes.

MEASURED RESULT: Storage forecast attempt01 stopped before emitting a forecast because it rejected every symbolic link. Independent inspection found 39 pytest directory aliases, all inside `qualification-v1/` on the bound physical volume. Their link payloads sum to 5,153 logical bytes with zero reported allocated payload blocks. The real directories and files remain retained. The corrected census counts link payloads with lstat, never follows aliases and therefore never counts their target data twice. External or unresolved targets still stop accounting; actual complete checkpoints still forbid symlink payloads.

MEASURED RESULT: A separate os.walk(followlinks=False), os.lstat and strict realpath/device path reconstructs every per-area file/link count and logical/allocation sum exactly. Future checkpoint-size and explicit allowance code is byte-identical to the retained original; literal free space remains the physical capacity gate. File allocation sums are not unique physical APFS allocation.

MEASURED RESULT: 25 targeted CPU checks pass with zero failures/skips, including three new cases for an internal directory alias, an external alias and an unresolved alias. The failed forecast retains 0.6854960420168936 measured supervisor process-wall seconds. Independent audit attempt01 stopped on a mistaken assumption that the unstarted scientific directory existed; its 0.808561667 observed tool-command seconds include a three-line test-summary read. No directory was created to satisfy the check. Audit attempt02 passes in 1.0945931669557467 measured seconds. All failures, original code, tracebacks and audit code remain outside Git with public hash receipts. All three measured failure/audit costs remain in the exact 36-entry shared cost set; storage forecast attempt02 is separately predeclared. No neural qualification is rerun.

FACT: This independent software path is run in the root session and does not claim an external frontier-model decision. All seven recipes remain AUTHORIZED_UNSTARTED. Evidence: `experiments/manifests/generation_2/storage-reforecast.attempt01.json`, `storage-census-repair.attempt01.json`, `storage-census-repair.attempt02.json` and `qualification-cpu-tests.attempt10.json`.

PROPOSED NEXT ACTION: Resume only storage forecast attempt02, cost reconstruction, final engineering suite and independent admission. Any capacity or 96-hour block remains a block.

PASS_INDEPENDENT_IN_ROOT_ALIAS_CENSUS_REPAIR
