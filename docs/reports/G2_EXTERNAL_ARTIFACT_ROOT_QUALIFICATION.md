# Generation-2 external artifact-root qualification — 2026-10-06

FACT — The post-10M scientific decision and exact Section Z amendment were published at `98c061066dab728f45ceac865b6d9b75288ef624` before Generation-2 model outputs. This step changes physical storage only. All seven scientific recipes remain AUTHORIZED_UNSTARTED, with zero scientific slots consumed.

## Physical binding and availability

FACT — `configs/generation_2/artifact_policy_v1.json` binds the separate GENERATION_2_ARTIFACT_ROOT using root/mount/UUID hashes. The exact private mapping is a versioned binding file on the authorized external volume, separate from the immutable Generation-1 archive. The Git repository and existing internal runtimes remain internal. Fifteen versioned areas cover sources, audio, hypotheses, corpus, frozen D1, DEVELOPMENT, BENCH, cold replay, controls, scientific checkpoints, ByT5, evaluations, private logs, binding and disposable fixtures.

MEASURED RESULT — Volume UUID hash is `d2830e5e525c9a1a3e6f9049cf42b53f7404f467e470683bf66058ed4f9c86f5`. The volume is writable, external solid-state PCI-Express storage, case-sensitive APFS, with SMART Verified. Literal free space before fixtures was 578.192 GiB; after cleanup it was 578.191 GiB. The 250 GiB gate passes using available filesystem blocks; no internal purgeable capacity is counted.

FACT — Availability checks create no missing root, select no alternate path, and import no model/network libraries. They reject missing mapping/root, changed volume identity, internal/read-only/non-case-sensitive destinations, insufficient literal space, and absolute/parent/symlink path escapes. Offline/local-only controls are provided for use after preflight and before model-library import. Missing-root simulation left the real volume mounted and created zero fallback files; no model initialized or network call ran. This qualifies the storage entry point. Future acquisition/training/checkpoint runners must each integrate and independently verify it before their qualification gate passes.

## Synthetic file and completion tests

MEASURED RESULT — Dedicated non-scientific fixtures tested create/write/flush/file fsync, directory fsync, atomic immutable-directory rename, COMPLETE inventory publication, SHA-256 readback, fresh-process reconstruction and interrupted-file rejection. Thirty-two atomic single-file replacements produced 334 concurrent-reader observations, with zero partial/missing payload observations. A 256 MiB sparse fixture used 32,768 allocated bytes and passed a separate fresh-process full-checksum readback. No scientific weights were used. Only the unique fixture directory created by this invocation was removed.

| 2 GiB dense fixture measurement | Result |
| --- | ---: |
| Sequential write, including file fsync | 0.580065 s / 3530.64 MiB/s |
| File fsync interval | 0.003146 s |
| Complete publication, hashes and readback | 2.303570 s |
| Read including SHA-256 | 0.694811 s / 2947.57 MiB/s |
| Fresh-process completion/hash reconstruction | 0.724592 s |
| 128 x 4 KiB files, individual sync and directory sync | 0.011267 s |

FACT — Reads may be served from cache. This is actual-volume storage viability, not cold-device throughput, power-loss survival, model BENCH or exact native training resume. OS fsync success is measured; hardware power-loss behavior is unmeasured. The native G2 checkpoint schema and its model/optimizer replay remain pending. G1 checkpoint validation and artifacts are unchanged.

## Storage forecast

MEASURED RESULT — Metadata joins reproduce 14,113 TRAIN, 1,900 CAL and 796 HPO candidates, all within the approved 2–12-second envelope. Total candidate duration is 34.526173 hours; PCM16 mono 16kHz equivalent is 3,977,415,159 calculated bytes. This is metadata qualification only; audio/hypotheses remain unqualified.

| New G2 component | Basis class | Minimum GiB | Likely GiB | Conservative GiB |
| --- | --- | ---: | ---: | ---: |
| missing official archives | ASSUMED_FROM_APPROVED_INVENTORY | 49.959 | 49.959 | 49.959 |
| extracted selected audio | CALCULATED_WITH_FORMAT_ALLOWANCE | 3.704 | 4.630 | 8.000 |
| hypotheses corpus and frozen manifests | ASSUMED | 0.100 | 0.500 | 2.000 |
| six BC BENCH streams | CALCULATED_WITH_ASSUMED_STORAGE_LAYOUT | 18.041 | 36.458 | 36.458 |
| twelve cold replay trajectories | CALCULATED_WITH_ASSUMED_STORAGE_LAYOUT | 0.000 | 18.229 | 18.229 |
| two historical compatibility controls | CALCULATED | 3.007 | 6.076 | 6.076 |
| one ByT5 qualification trajectory | CALCULATED_WITH_FORMAT_ALLOWANCE | 3.349 | 4.496 | 4.496 |
| expanded DEVELOPMENT and diagnostic outputs | ASSUMED | 0.500 | 2.000 | 4.000 |
| six future BC scientific recipes routine saves | CALCULATED | 117.268 | 118.487 | 118.487 |
| future ByT5 scientific recipe | CALCULATED_WITH_FORMAT_ALLOWANCE | 11.162 | 11.225 | 11.225 |
| full presentation ledgers and resume metadata | ASSUMED | 0.200 | 1.000 | 4.000 |
| private logs and receipts | ASSUMED | 0.250 | 2.000 | 8.000 |
| atomic publication transient | CALCULATED_WITH_ALLOWANCE | 3.007 | 4.000 | 8.000 |
| unallocated headroom and failed attempt reserve | ASSUMED | 8.000 | 16.000 | 32.000 |
| **Total** | **Mixed classes as above** | **218.547** | **275.060** | **310.929** |

CALCULATION — Conservative projected remaining capacity is 267.244 GiB, above the 250 GiB floor. Fixed B/C array sizes are measured G1 logical sizes; 78 routine scientific saves are fully included without assuming sparse savings. ByT5 sizes derive from 299,637,760 parameters and FP32 model/moments. Source archives remain the approved inventory estimate until acquired and hashed. Audio/outputs/logs/metadata and reserve include explicitly stated assumptions.

ASSUMED — BENCH preserves initial/final and boundary/mid snapshots for each of six configurations. Cold replay reads those immutable snapshots and retains one final full-array capture per trajectory plus all required next-20 state records. It does not duplicate its starting model arrays. The future implemented storage layout and actual byte totals must reproduce these assumptions before scientific execution admission. No scientific cadence, population or treatment was modified for space.

ASSUMED — 32 GiB of additional unallocated headroom covers a large partial archive or retained failed trajectory. Arbitrarily many failures are UNPRICED, not silently discarded. Reforecast from actual retained failures before further expensive work and stop if space is unsafe. The 25% time reserve is separate and remains unapplied here because model costs are unmeasured.

## Independent reconstruction and tests

MEASURED RESULT — A separate standard-library code path reconstructed the mounted volume identity, public/private binding hashes, forecast sums, 78-save formula, candidate stable-ID/group disjointness and 64-record replay preselection. Fresh child processes reconstructed dense and sparse COMPLETE inventories/checksums without the writer implementation. This is independent software-path verification; no external frontier-model review is claimed.

MEASURED RESULT — Twelve meaningful storage tests pass; integrated suite passes 391 tests in 33.32 seconds, zero skips/failures. The baseline remains the freshly reproduced 379 tests. No dependency/runtime change occurred.

Evidence: [external-root receipt](../../experiments/manifests/generation_2/external-root.attempt01.json), [provenance](../../experiments/manifests/generation_2/external-root-provenance.attempt01.json), [forecast](../../experiments/manifests/generation_2/storage-forecast.attempt01.json), [metadata census](../../experiments/manifests/generation_2/metadata-census-summary.attempt01.json), [independent reconstruction](../../experiments/manifests/generation_2/independent-storage.attempt01.json), [full tests](../../experiments/manifests/generation_2/storage-full-tests.attempt01.json).

PROPOSED NEXT ACTION — Acquire only the missing official TRAIN archives directly into the qualified external root, preserving complete failed attempts and original source identity/checksums. Then qualify all approved census audio and source hypotheses; no student training before corpus/panel support gates. All seven scientific recipes stay unstarted. No Time Machine snapshot operation occurred or is authorized.

G2_EXTERNAL_ARTIFACT_ROOT_QUALIFIED
