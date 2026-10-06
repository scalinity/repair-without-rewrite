# Six 10M probe campaign — independent provenance review

Review date: 2026-10-06T12:27:06.866890+00:00

MEASURED RESULT — Provenance reconstruction passed for all six registered recipes. The final CPU checker ran with `--require-complete`, reconstructing 78 native checkpoints, 36 frozen evaluations, all six initial parameter identities, and 305 complete queues per recipe. No provenance discrepancy requiring campaign repair was found.

FACT — This review covers provenance, six-slot accounting, presentation identity, native checkpoint state, reader cursors, evaluation population identity, and recorded failure/resume accounting. It does not reproduce WER, repair bounds, eligibility, ranking, or LR selection. Those checks belong to the separate metric/selection review.

## Evidence and method

The unchanged checker is `benchmarks/six_10m_provenance_independent.py`, SHA-256 `b07b2343be430726a50e5585683e5d9752e4c41420a8763d179865e92930ca6a`. It uses the standard library and NumPy to reconstruct accepted rows and the ledger, read native NPZ arrays, and compute parameter/optimizer identities. It imports neither the campaign wrapper nor native trainer, MLX, or Torch, and does not instantiate a neural model.

Final evidence:

- `experiments/manifests/six_10m_probes/independent-provenance.attempt14.json`, SHA-256 `d3ee82eb5809525d9ab84ff80ea14291cdccbc7957538b35db82df3cdf5c3f49`.
- `experiments/manifests/six_10m_probes/independent-provenance-full-projection.attempt01.json`, SHA-256 `fa1bf285356a03b9d79dd8af2c873b5b89182de88985c7907d34fdfb02a813d9`.
- Private direct-comparison draft `exports/storage-checks/six-recipe-full-projection-attempt01.json`, SHA-256 `0319e8a3ffb69db84c6b4c6692a60036f75c7782dcad78d3442d90d189c4f321`. The public binding carries counts and hashes; raw text and arrays remain ignored.

A separate streaming comparison read all six raw update logs together, matching every presentation and complete queue against the frozen ledger. It checked raw byte length, terminal-bound SHA-256, and exact EOF. This is separate from the checker's native-input and tensor reconstruction path.

## Freeze, source, and slots

FACT — Authorized checkpoint: `7868302afc43e3cbd475464452f57912a9c2cf97`. Pre-run manifest source: `1ad1ea1f0313d548e8af6cfaf75d5ff87fee6feb`. Manifest SHA-256: `43a97ef40acbb2efebaf4941931934969c093e23f77b69bfd132f236755b1dd3`. Published pre-run checkpoint: `c4c28517ddb60e1d802adcac45351ee034c23070`. All six manifest entries remain `AUTHORIZED_UNSTARTED`, preserving the prospective inventory; execution receipts record later outcomes.

MEASURED RESULT — Frozen relevant source/configuration/data identities were verified at each start commit. Every start recorded a clean working tree, seed 42, and null resume. Directory accounting found exactly six start receipts, six terminal receipts, six registered recipe directories, and only `attempt01` per recipe. The registered alternating order was reproduced.

| Order | Recipe | Start source commit | Outcome |
| --- | --- | --- | --- |
| 1 | `B100-seed42-lr1e-04` | `c4c28517ddb60e1d802adcac45351ee034c23070` | COMPLETED |
| 2 | `C101-seed42-lr1e-04` | `5f75e483c68281105330e29820878aafd91a15b2` | COMPLETED |
| 3 | `B100-seed42-lr3e-04` | `7f207c1956253823113dc6e0ddbd115574aab928` | COMPLETED |
| 4 | `C101-seed42-lr3e-04` | `fb9f0cdfc4cda3d04784111f17baa1ddd12f3591` | COMPLETED |
| 5 | `B100-seed42-lr6e-04` | `6652667557ba18944039096c3c52c58551fcf61e` | COMPLETED |
| 6 | `C101-seed42-lr6e-04` | `1f398126de6f869f03f39c368a1bec08759b3013` | COMPLETED |

## Initial and endpoint states

MEASURED RESULT — All three B100 initial model, optimizer moment, and full NPZ identities match. All three C101 initial identities independently match. B100 has 100,686,336 parameters and 525 saved arrays; C101 has 101,081,859 parameters and 549 saved arrays. These identities were reconstructed from native bytes without rerunning initialization.

| Recipe | Initial parameter SHA-256 | Final parameter SHA-256 |
| --- | --- | --- |
| `B100-seed42-lr1e-04` | `2739837ff4ad4ff26475dca5a37608d9c46a1c7ff34f8778f24eadb18b8e8044` | `c50b13888a96f011dc9242afe42fa3dd84a86a42554d670e495b5a4b3b92da0f` |
| `C101-seed42-lr1e-04` | `9671ba3aaf0afb9fe22302fe140512db7bdf7e31f4d9e439bc13c75edafc2ff1` | `6b7c29788836ee96c2a0a5eadf91363ee4dada52003b81310617284b51f03ba1` |
| `B100-seed42-lr3e-04` | `2739837ff4ad4ff26475dca5a37608d9c46a1c7ff34f8778f24eadb18b8e8044` | `2adea1f910d549abdce3e3d8819454cfce4b21193600f7bd07ac7db1408fc023` |
| `C101-seed42-lr3e-04` | `9671ba3aaf0afb9fe22302fe140512db7bdf7e31f4d9e439bc13c75edafc2ff1` | `a3c2ec251f86e7b87f67f7d71b7ff6b9f460000c9f4c28640cbec8c297388450` |
| `B100-seed42-lr6e-04` | `2739837ff4ad4ff26475dca5a37608d9c46a1c7ff34f8778f24eadb18b8e8044` | `f76f3542fc688eac39669c4ef5f8e4b11ce440296728edbcc38f5e9775e93cfa` |
| `C101-seed42-lr6e-04` | `9671ba3aaf0afb9fe22302fe140512db7bdf7e31f4d9e439bc13c75edafc2ff1` | `cbce2f5f843dc55e6cc32856bf611690e2cd9a2b4cee240bf3e059ea8815904f` |

Common initial optimizer/NPZ identities:

- B100: first moment `b802af61a659f72d0d32361def122bb499f82201fcd5f2d8bc5c64bd10471627`; second moment `75ecf1fed0d101eff29c8aa272873e877b9de2872c0167b1f1bed1581abf98fa`; full NPZ `488d3ba292f0df45420d6920d25591b1e65c07e149c0b3fdddd4159b8bf3df82`.
- C101: first moment `778349fdd465a0fb4fd4f2d07be543ecfa46ae89739ba0fcbc2a10b235bbd090`; second moment `0ecfb30d012baead42f3fe74cb9e32d141508d606babc09b747c4d0f1c4d71dc`; full NPZ `a5e574c00177ac7d97440ad643053cc7279b7600c547de97c26220dd466f1cc3`.

MEASURED RESULT — Every native `COMPLETE.json` inventory, metadata hash, and NPZ hash was verified. Parameters, moments, accumulators, counts, dtypes, finiteness, and zero complete-boundary accumulators were reconstructed. Model/configuration/optimizer/runtime identities and the exposure LR clock matched the freeze. Each completed checkpoint has an empty pending queue and correct committed update/exposure cursor. Exact final optimizer, NPZ, metadata, and publication identities are enumerated per recipe in the final receipts.

Compaction preserved logical native bytes and publication hashes; physical allocation is a storage measurement. Separate qualification: `docs/reviews/SIX_10M_STORAGE_INDEPENDENT_REVIEW.md`. This final review performed no storage mutation.

## Presentations, queues, and reader states

MEASURED RESULT — All six recipes consumed ledger SHA-256 `21c3f5838f5c7e85f258e8eef25b2b38884a2023199afc5d1852d68155b04f2f`: 134,591 whole presentations, ordinals 0–134,590, and 305 complete queues. Each reaches 10,007,223 canonical exposures at update 305. Every actual presentation charge, source/target/anchor digest, channel, phase, ID, and cumulative exposure matched its frozen row. Native token/event inputs, whole-queue denominators, LR, phase, and finite loss/gradient accounting were checked independently.

The common scientific projection SHA-256 is `8f7a7b25e47112113ef7934d3e8f0190bd76b8bd6f1c3521aa3f93fbdba33dec`. Encoding is one compact, sorted-key UTF-8 JSON object plus newline per presentation, over the fields listed in the public receipt. Timing and native architecture-specific encoding remain in raw logs and are checked separately from this common projection.

MEASURED RESULT — All 13 reconstructed reader cursor/deficit states match across all six recipes. Exact state hashes remain in the receipts.

| Update | Canonical exposures | Last presentation ordinal | Frozen evaluation |
| --- | --- | --- | --- |
| 0 | 0 | -1 | yes |
| 31 | 1,017,149 | 13,838 | yes |
| 61 | 2,001,130 | 27,230 | save only |
| 92 | 3,018,478 | 41,095 | yes |
| 122 | 4,002,553 | 54,485 | save only |
| 153 | 5,019,821 | 68,330 | save only |
| 183 | 6,004,173 | 81,721 | save only |
| 204 | 6,693,230 | 91,100 | yes |
| 214 | 7,021,296 | 95,556 | save only |
| 244 | 8,005,412 | 108,974 | save only |
| 275 | 9,022,609 | 122,797 | save only |
| 285 | 9,350,642 | 127,234 | yes |
| 305 | 10,007,223 | 134,590 | yes |

CALCULATION — Across six runs, the logs contain 1,830 optimizer updates and 807,546 presentation consumptions. These are repeated applications of the same ledger; each recipe's endpoint remains 10,007,223 exposures. No shortened final update or phase-boundary queue flush was observed.

## Evaluation identity

MEASURED RESULT — All 36 output files have the same 396 ordered IDs: 108 natural and 288 generated cases, with populations kept distinct. Panel SHA-256: `5043ed60d6ce8f891ee8e30255fabaa40fcac37b0a043c1a85dd88178832ce4e`. Checker ordered-ID encoding digest: `a1bec42c01599a9601cd8bbaf8defb0ce7b0118f61a86f76e80794a225bfcffe`. Source/target identities and nominal-to-complete endpoint mappings matched the frozen panel and manifest.

Mapped evaluation updates are 0, 31, 92, 204, 285, and 305. This reconstructs 14,256 case instances, including the complete ordered panel at every recipe/endpoint. Case identity alone does not establish model quality; scoring and output-failure classification require the separate metric review.

## Failures, resumes, and retained diagnostics

MEASURED RESULT — Every recipe completed `attempt01`. No qualifying numerical failure, replay, interruption receipt, or resume was recorded. Every raw log ends exactly after update 305 and its SHA-256 matches its terminal receipt. No unresolved reader/checkpoint identity discrepancy was found.

Actual interrupted or numerical-failure replay was not exercised by this campaign. This review verifies stored state and the absence of recorded events; it does not report an unrun replay as passed.

FACT — Reviewer diagnostics remain separate from the empty scientific failure ledger:

- `experiments/manifests/six_10m_probes/independent-provenance.attempt01.json`, SHA-256 `4a0dfad68780ecc2167b51596e9daffe956769baefea79c36596782aa0645710`, retains the early checker's `checkpoint treatment mismatch` expectation failure. The qualified checker recognizes the native `mlx.core.bfloat16` identity; native treatment was not changed to satisfy the review.
- `exports/storage-checks/six-recipe-prefix-diagnostic.attempt01.json`, SHA-256 `3abc2d859e2af3067372495df189d4ad8ead9c0bf430bf90effc4b0e82dbce4c`, retains a reviewer-only field-name error. The corrected direct comparison maps ledger `end_exposure` to consumed `cumulative_canonical_exposure` and passed without a scientific artifact change.
- `exports/storage-checks/provenance-review-render-diagnostic.attempt01.json`, SHA-256 `895aeb0da2373149b764fecc7e627ecf8c095d01c0268243aa4967a65df43855`, retains a report-render preflight error expecting `selected_lr` rather than the actual `selected_peak_lr`. The failed preflight wrote no report or scientific artifact; only rendering was corrected.

All numbered partial receipts and prefix bindings remain intact. Final evidence does not rewrite earlier partial or failed diagnostic claims.

## Recorded campaign decision and limits

FACT — `experiments/manifests/six_10m_probes/endpoint-selection.attempt01.json`, SHA-256 `5d385e5760853992d7eb0c448cfc390352cab36a2e302ff6cb5995e99ef8bdfa`, records `CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE`: both eligible rankings empty, both selected peak LRs and recipes null. This is the separately recorded outcome; this provenance review does not independently establish scoring or eligibility.

MEASURED RESULT — The six-run provenance contract is reproduced. No provenance defect requires rewriting a run, adding a recipe, or changing scientific treatment. This review used the frozen DEVELOPMENT artifacts and CPU reconstruction only; it performed no sealed inference, final training, accelerator workload, or model-selection action.

CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE
