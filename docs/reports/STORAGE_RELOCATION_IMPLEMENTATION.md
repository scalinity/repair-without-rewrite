# Storage relocation implementation — 2026-10-06

FACT — Storage-only relocation on clean `main` at base `abd8bc885ee754cb43b48d6197b8d93b011c24fb` preserved every copied file and all 78 scientific saves. The completed prior copy was verified before any internal removal. All 205 allowlisted items now have verified external copies and original-path compatibility links. The explicitly approved keep-set and six additional small path-sensitive helper scripts remain real internal files/directories.

MEASURED RESULT — Relocation integrity and runtime checks pass, but internal free space is 186.647 GiB. The 250 GiB minimum and 300 GiB preferred target are not met. This is partial completion of the storage objective; no Generation-2 workload starts.

## Copy and independent verification

The [machine-readable manifest](../../experiments/manifests/storage_relocation/relocation.attempt01.json) enumerates every allowlisted item, relative source/archive mapping, type, byte/allocation sizes, file/directory/link counts, matching tree identities, removal result and compatibility strategy. Exact local paths and per-file inventories remain private in the verification archive. Public path classes identify the evidence archive, future G2 root and private receipt bundle.

MEASURED RESULT — Primary sorted per-file verification compared relative path sets, types, permissions, lengths and SHA-256s for 35,928 regular files, six existing symlinks and 3,550 directories. Complete source/destination tree identities match: `aa829a56a3aa8c39276a0871aaa94f3efddfec86f6cedef62081c14f15f5b602`. A separate enumeration and operating-system full-byte comparison checked all 2,334 relocatable regular files: 176.079 GiB logical, zero discrepancies. Before removal, every original and destination was rechecked against its verified inode/device/size/mtime snapshot, the exact external volume identity was checked, and no open writers were found. Checkpoint triplets stayed together. Invalid diagnostic fixtures and failed attempts were preserved unchanged.

## Allocation and free space

| Population | Source logical GiB | Source allocated GiB | Archive logical GiB | Archive allocated GiB |
|---|---:|---:|---:|---:|
| `exports/` | 174.412 | 137.689 | 174.412 | 171.617 |
| `checkpoints/` | 3.130 | 3.130 | 3.130 | 3.089 |
| `exports/six-10m-probes/` | 119.326 | 85.546 | 119.326 | 117.047 |

MEASURED RESULT — The removed internal duplicates accounted for 139.280 GiB of file allocation before removal. The retained keep-set accounts for 1.539 GiB. These are file-allocation measurements, not realized free-space gains. Internal container free space changed from 193.940 to 186.647 GiB (-7.293 GiB observed change). External container free space is 578.248 GiB at closeout measurement (2026-10-06, 20:12:25 EDT).

FACT — One purgeable local Time Machine snapshot predates relocation. INFERENCE — It may retain removed-file extents; its exact retained byte contribution was not measured. Snapshot removal and unrelated cleanup are outside this authorization. No snapshot was changed. Sparse allocation differences are documented above; file bytes were not transformed, recompressed or rewritten.

## Internal keep-set and compatibility

The manifest lists the ten explicitly protected paths: two environments, six private regression inputs and both tracked `.gitkeep` files. Their bytes were rehashed after final validation and remain unchanged. Both root directories and mixed keep-set ancestors remain real internal directories. All 205 compatibility links use absolute targets under the verified archive, resolve without cycles, and preserve original logical names. No environment or protected file became a symlink.

Six additional files remain internal because their saved invocations derive the repository import root from their resolved script filename:

- `exports/six-10m-final-validation.attempt02.py`
- `exports/six-10m-final-validation.py`
- `exports/six-10m-build-reports.attempt01.py`
- `exports/six-10m-build-reports.py`
- `exports/six-10m-record-final.py`
- `exports/six-10m-record-completion.py`

Their external copies are also retained. No scientific code was changed to remove that location dependency.

## Regression and active-input qualification

| Phase | Collected | Passed | Skipped | Failed | Seconds |
|---|---:|---:|---:|---:|---:|
| baseline | 379 | 379 | 0 | 0 | 35.72 |
| staged | 379 | 379 | 0 | 0 | 35.93 |
| post | 379 | 379 | 0 | 0 | 35.65 |

MEASURED RESULT — The staged phase used external compatibility links while all internal originals were still held intact. The final phase ran after verified internal duplicate removal. Both pre-removal and final bounded checks loaded pinned Parakeet offline and official ByT5 through its local CPU loader; loaded Qwen's local tokenizer and checked every pinned shard; instantiated the frozen lexical reader; rejoined D0 pairs to the released source archive; read the panel and DEVELOPMENT tokenizer; verified COMPLETE hashes and read every array of all three root checkpoints and the G1 B/C 3e-4 endpoints. All six G1 populations retain 13 saves and six evaluation outputs each. Independent provenance tooling finds its original inputs. The isolated acquisition environment remains internal.

An isolated dangling-link simulation tested missing Parakeet, Qwen-tokenizer, ByT5 and checkpoint targets. Absolute-path checks passed before removal. A later relative Parakeet check initially failed its diagnostic assertion: attempt02 replaced `Session.request`, preventing the real offline adapter from running and conflating request construction with network transmission. That failed attempt is retained. Independent attempt03 left the installed offline adapter intact and blocked HTTP transport and socket connections; the relative model failed clearly with zero transport/socket calls. The real volume was never unmounted. The relative `exports/parakeet-...` name has valid Hugging Face identifier syntax; it is not inherently protected against remote fallback. Future calls must retain offline/local-only controls before library import or use an explicitly supported absolute local path. No research loader or configuration was modified.

## External volume and I/O

FACT — The expected external volume is writable, encrypted, case-sensitive APFS. Its identity hash is recorded in the manifest. The completed prior copy was not overwritten and no overlapping copy writer was started.

MEASURED RESULT — A dedicated 1.5 GiB synthetic temporary file measured 3438.1 MiB/s writes including fsync (0.003200s fsync), and 2548.5 MiB/s reads including SHA-256. The file alone was cleaned up. Reads may be cached; these results are an operational check, not cold-drive throughput, scientific weights or a Generation-2 BENCH.

FACT — The orchestration page was realigned in place and inspected at desktop/phone widths in both appearances. No horizontal overflow was detected. Two browser-launch diagnostics are retained; the final check used an already installed browser, with no download. The four temporary screenshots were inspected and removed. The private verification bundle contains 68 copied, SHA-256-verified files plus its verification receipt.

## Generation-2 storage boundary

FACT — The supplied relocation authorization identifies repaired pinned Parakeet and official ByT5 as active future G2 source/comparator inputs. Both remain accessible at their original logical paths. D0 pairs, pools, ledger, qualification records and all G1 evidence remain accessible. Qwen and Kokoro are retained historical source material; G2 authorizes zero TTS. Historical ByT5 adaptations, BENCH states and G1 checkpoints are not G2 student initializers.

A separate empty, writable G2 artifact root was created on the same external volume. It is outside the G1 evidence archive; its exact local mapping remains private. This scaffold is a candidate for future separately qualified acquisition, extraction, hypotheses, qualification and trajectories. No source archive download, hypothesis generation, TTS, inference, scientific training, G2 BENCH, final training or protocol freeze occurred. Scientific decisions and historical manifests were not rewritten.

PROPOSED NEXT ACTION — Review the unmet internal free-space objective through a separately authorized APFS allocation investigation. Preserve snapshots until their retained contents and removal scope are understood. Require the 250 GiB minimum and separately qualify the G2 artifact root before resuming the authorized G2 workflow.

PARTIAL_RELOCATION_COMPLETED
