# Six 10M probe checkpoint storage: independent CPU review

FACT: This review qualifies byte-preserving storage handling. It does not qualify model outcomes, checkpoint restoration on the accelerator, or completion of the six-recipe campaign. The reviewer changed diagnostic copies only; the campaign's original checkpoint directories were left to the execution session.

The reviewed helper is `benchmarks/six_10m_storage.py`, SHA-256 `cf0d37f3cef3318b4efb0350d898cd5ae2d651c96de8790aab8ceac50938a9b0`. The native trainer, frozen campaign wrapper, scientific configuration, NPZ representation and checkpoint paths are unchanged by this helper.

## Documentation and method

FACT: The installed macOS `fcntl(2)` manual documents `F_PUNCHHOLE` as deallocating an aligned byte range without changing file size; subsequent reads return zero bytes. The installed MacOSX SDK `sys/fcntl.h` defines command 99 and `fpunchhole_t`: two 32-bit unsigned fields followed by two 64-bit `off_t` fields. The reviewed implementation uses the 24-byte `struct.pack("=IIqq", 0, 0, offset, length)` representation. No compiler or accelerator was used.

The helper first verifies `arrays.npz` against the native `COMPLETE.json`. It copies to a new adjacent temporary file and punches only contiguous, block-aligned runs whose original 4,096-byte blocks are entirely zero. It fsyncs the copy, verifies its size and full logical SHA-256 against both the original and the native manifest, reads every NPZ entry through its CRC, and atomically replaces the same path. It verifies the published hash, fsyncs the directory and writes a new storage receipt. Existing receipt or receipt-partial paths reject before checkpoint mutation. A pre-existing checkpoint copy-partial path also rejects before publication.

FACT: CPU fixtures covered five zero-run arrangements, including an all-zero aligned EOF, a partial zero tail, interspersed nonzero blocks and a sub-block file. The original-digest rejection and stale receipt-partial rejection were exercised. The copied native checkpoint tests compared every NumPy array's shape, dtype and values against the untouched campaign input, in addition to whole-file hashes and CRC readback. Native `COMPLETE.json` and `metadata.json` remained byte-identical.

## Measured footprints

MEASURED RESULT: Both qualified checkpoint copies had 1,611,136,656 logical NPZ bytes and 525 arrays. Physical sizes below are `st_blocks * 512`, rather than logical length.

| Diagnostic copy | Physical input bytes | Physical result bytes | Logical-byte identity |
| --- | ---: | ---: | --- |
| Initial B100, documented `ditto --hfsCompression` | 1,460,338,688 | 1,331,167,232 | Exact |
| Initial B100, pretruncate and nonzero-block writes | 1,460,338,688 | 1,460,191,232 | Exact |
| Initial B100, explicit hole punch | 1,460,338,688 | 404,418,560 | Exact |
| B100 completed update 31, qualified helper | 1,577,517,056 | 1,208,897,536 | Exact |

MEASURED RESULT: `ditto` did not apply transparent compression: the copied file had no compression flag or `com.apple.decmpfs` attribute. Pretruncating and skipping writes also yielded little physical reduction on this filesystem. Explicit hole punching reclaimed the expected zero ranges. The initial diagnostic punched 303 runs comprising 1,206,718,464 bytes, with no punch errors. The dense update-31 checkpoint had dense model and Adam moments, with all 131 accumulator arrays zero at its complete update boundary; its measured reduction was 368,619,520 physical bytes.

MEASURED RESULT: Independent tensor reconstruction gave initial B100 parameter hash `2739837ff4ad4ff26475dca5a37608d9c46a1c7ff34f8778f24eadb18b8e8044`, matching the pre-run freeze. Update 31 gave `1f7baaa92be43c727be10d4e344e678664c4cc987f9a5cb5919f1639bd55ca79`, at 1,017,149 canonical exposures. The NPZ identities were respectively `488d3ba292f0df45420d6920d25591b1e65c07e149c0b3fdddd4159b8bf3df82` and `5c675dd2c8ed99ad6cbb702dc74319c4176c34ab37066eaeb735aaef1886a8b6` before and after handling.

## Scope and limits

INFERENCE: Identical logical NPZ, metadata and completion-manifest bytes at the original checkpoint path preserve the inputs seen by the existing native loader. This CPU review did not import MLX or execute its masked-forward restoration check. Byte identity and full NumPy readback are measured; accelerator restoration remains the execution session's native checkpoint verification.

CALCULATION: Seventy-eight saved checkpoints at the measured B100 update-31 footprint would occupy 94,294,007,808 physical NPZ bytes. This extrapolation does not establish campaign capacity. It excludes C101 size differences, later checkpoint footprints, evaluation and raw logs, failed states or replays, transient copy headroom and unrelated volume changes. Initial checkpoints are smaller after handling. Free volume bytes measured during the dense diagnostic were 103,912,378,368; that observation is time-specific. Capacity must continue to be checked against actual saves and available transient headroom.

FACT: The initial extended-attribute receipt attempt failed because the installed Python lacked `os.listxattr`, after logical hash and array checks had completed. A separate receipt preserved that diagnostic failure; the repeat used the operating system's attribute tool. Transparent compression and pretruncate diagnostics did not provide adequate savings. These are storage diagnostic outcomes, not numerical training failures, invalid scientific attempts, or consumed recipe replays.

No scientific treatment, source information, model tensor value, objective, exposure clock, evaluation population, LR schedule or recipe slot was changed by the reviewed storage operation. No campaign provenance PASS is inferred from this qualification.

## Evidence

- `experiments/manifests/six_10m_probes/independent-provenance-storage.attempt01.json` through `attempt07.json`: preserved diagnostic outcomes, whole-file identities, array reconstruction and footprint measurements.
- `experiments/manifests/six_10m_probes/independent-provenance-storage-helper.attempt01.json` and `attempt02.json`: helper executions on copied initial and dense checkpoints.
- `exports/storage-checks/`: ignored diagnostic copies retained with their exact logical bytes.

EXACT_CHECKPOINT_STORAGE_CPU_QUALIFIED
