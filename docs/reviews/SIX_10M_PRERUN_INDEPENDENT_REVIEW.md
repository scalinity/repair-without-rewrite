# Six 10M DEVELOPMENT probes: independent pre-run review — 2026-10-06

**INFERENCE: the frozen artifacts and final operational wrapper have no unresolved blocking static finding. Runtime and publication gates remain separate and must pass before the first optimizer update.** This review consumed no scientific recipe, imported no MLX, and executed no model, training or accelerator workload.

## Reviewed identities and evidence

FACT: The reviewed base is `7868302afc43e3cbd475464452f57912a9c2cf97`. The final reviewed `benchmarks/six_10m_campaign.py` SHA-256 is `897bf97e21aaad2d981edb4166b6617411d2ca49a3c9471ed8e1628b9700dafc`. Its test-source identity is recorded in the [final review receipt](../../experiments/manifests/six_10m_probes/prerun-independent-review.attempt03.json). This binds the reviewed file bytes rather than implying that an uncommitted wrapper is already a clean published checkpoint.

FACT: The controlling records were the canonical source and registry in `docs/design-inputs/`, the accepted findings, prospective amendments, [V4 admission](../reports/BC_10M_PROBE_ADMISSION_DECISION_V4.md), and [frontier reader decision](FRONTIER_READER_CURRICULUM_DECISION_V1.md), especially sections E–G. The review covered the complete native `src/models/paired_training_v3.py`, its optimizer/objective dependencies, all six registered recipe files, the wrapper and its related tests.

MEASURED RESULT: Independent standard-library reconstruction is retained in [attempt 01](../../experiments/manifests/six_10m_probes/prerun-independent-review.attempt01.json). Subsequent wrapper checks are retained in [attempt 02](../../experiments/manifests/six_10m_probes/prerun-independent-review.attempt02.json) and [attempt 03](../../experiments/manifests/six_10m_probes/prerun-independent-review.attempt03.json). No earlier receipt was replaced. Temporary synthetic check files contained no research source text or model payloads.

MEASURED RESULT: The baseline receipt's private log hash, authorized source commit, exit code zero and **372 passing tests** reproduce the recorded receipt. The independent reviewer verified that receipt and its log bytes; the reviewer did not rerun the integrated suite. Evidence: [baseline receipt](../../experiments/manifests/six_10m_probes/baseline-validation.attempt01.json).

## Frozen artifacts independently reconstructed

MEASURED RESULT: Actual bytes match the bound identities:

| Artifact | SHA-256 |
|---|---|
| DEVELOPMENT tokenizer | `b125551f3c3627edc9cb8d325bc70bfd8340df1518f03d0fd16d140ff7ace6ca` |
| Lexical corruption profile | `bc14b7ca5e8299ee8004cefb6deb67151ea93f1d44f48ea48d0b4619a9549b87` |
| Generated accepted pool | `dc9caac46145eee1e8d9ebea34ff486b3b08afffaee447d0bb22e12bef3fe8dc` |
| Frozen presentation ledger | `21c3f5838f5c7e85f258e8eef25b2b38884a2023199afc5d1852d68155b04f2f` |
| Frozen DEVELOPMENT panel | `5043ed60d6ce8f891ee8e30255fabaa40fcac37b0a043c1a85dd88178832ce4e` |

FACT: The ledger digest uses the owner-authorized correction of the truncated supplied hash, verified against actual bytes. No ledger, population or exposure rule was changed.

MEASURED RESULT: Independent reconstruction checked every accepted source/target/anchor byte hash and every ledger row's accepted-row hash, canonical charge, ordinal, presentation ID, exposure continuity and starting-exposure phase assignment. It separately reconstructed every first-whole-presentation 32,768-anchor queue, B target/EOS denominator, C action/start/end/vocabulary denominator, phase segment and channel charge. All **134,591 presentations**, **305 complete queues**, **10,007,223 canonical exposures**, and final ordinal **134,590** match the frozen update index. These are reconstructed planned endpoints, not executed neural updates.

MEASURED RESULT: All six recipe files retain seed 42, the three prescribed peaks per arm, identical data/panel identities and identical save/evaluation schedules. Their immutable registered status is `CONFIGURED_UNSTARTED_UNAUTHORIZED`, with `probe_slot_consumed=false`; the campaign freeze prospectively records the separate session authorization as `AUTHORIZED_UNSTARTED`. No registered execution-order field was found. The wrapper's alternating-arm, ascending-LR order therefore follows the authorized operational fallback.

MEASURED RESULT: The 13 deduplicated save-update indices are **0, 31, 61, 92, 122, 153, 183, 204, 214, 244, 275, 285, 305**. All six evaluation maps match independent reconstruction:

| Nominal exposure | Complete update | Actual exposure | Last ordinal |
|---:|---:|---:|---:|
| 0 | 0 | 0 | -1 |
| 1,000,000 | 31 | 1,017,149 | 13,838 |
| 3,000,000 | 92 | 3,018,478 | 41,095 |
| 6,666,667 | 204 | 6,693,230 | 91,100 |
| 9,333,334 | 285 | 9,350,642 | 127,234 |
| 10,000,000 | 305 | 10,007,223 | 134,590 |

MEASURED RESULT: The actual panel has 396 unique ordered IDs: 96 CALIBRATION natural pairs, 12 repaired HPO natural hypotheses, and 288 generated DEV cases. Every source/target hash and native-admission flag matches. All 96 consumed calibration IDs match the frozen consumption list. The ordered panel-ID digest is `c5e87da42b663c04cf5e2ac437e9ee0b153431cc3f95d8d4523ca008fc6c6d97`. Natural and generated denominators remain distinct.

## Native treatment and wrapper review

MEASURED RESULT: Eight native model/trainer/reader/qualification files match `28298ad886aa321882aa0530a18421e7d4e3553e` byte for byte. Their actual and native-freeze hashes are recorded in attempt 03. The wrapper does not replace their training objective, decoder, renderer, optimizer or scheduler.

INFERENCE: The native path preserves B's full-queue target/EOS normalization, C's full-queue component normalization and omission of zero-count components, FP32 masters/moments/accumulation, BF16 working computation, and one clipping/update/clear per common queue. The LR uses the completed canonical endpoint with 200,000-exposure warmup and continuous cosine decay to the fixed floor. Native checkpoint checks retain exact queue, partition, denominators, pending/completed charge, arrays, RNG, reader state, configuration/clock identity and masked-forward readback.

FACT: Fresh recipes construct the fixed architecture with seed 42, verify the exact parameter count, and compare initial parameter hashes with the architecture-specific freeze identity before loading any same-recipe resume state. Actual initial tensor identities have not been measured by this CPU reviewer; generating and publishing the campaign freeze and collecting all six actual start receipts remain required.

FACT: C component diagnostics use an additional pre-update forward over the same frozen complete queue at nonzero evaluation endpoints. They call the existing component-sum path, perform no gradient or optimizer update, and leave the native training objective intact. Their time is separately recorded from native update time; these diagnostic reductions are labelled separately from the native total. This adds monitoring work, not a new training recipe or exposure charge.

No unresolved critical static issue remains. The following operational findings were corrected before any recipe began:

- Replay now reconstructs a fresh reader before restoring a saved phase/cursor state, avoiding later-phase pool leakage into an earlier checkpoint.
- A restored endpoint receipt remains available when a failure occurs during final evaluation, preventing an empty endpoint list from breaking completion accounting.
- The freeze binds all source files and Unicode tables; execution checks the latent hash and exact frozen data map. Generated scoring retains only the 288 frozen DEV IDs and verifies their partition.
- Same-recipe external resume preserves attempts; a pending native queue is checked against the immutable ledger and completed through the existing microstep/finish path. SIGINT/SIGTERM interruption saves publish complete optimizer boundaries. Failed tensors, queue/objective/reader/RNG metadata and their hashes are retained.
- Generated structural-invalid outputs and category/view failure breakdowns remain visible, including completed outputs that fail the parser.
- Natural scorer resource caps retain all canonical rows and bounds. Whole-population local preservation is nullable when correspondence is unavailable; covered-subset counts and bounds are explicitly labelled.

MEASURED RESULT: Independent CPU execution of the sparse helper preserved exact logical bytes for empty, all-zero, interspersed-zero and trailing-zero payloads. A wrong expected digest retained both original bytes and the failed copy. Independent AST-extracted summary checks retained all 108 natural/288 generated synthetic cases, exposed one unavailable correspondence without inventing whole-population preservation, and counted a completed structural-invalid generated case separately from decoder failure. A second synthetic check recovered the full preservation bound when correspondence was available. These checks test operational edge handling and do not create scientific outcomes.

## Remaining execution gates

PROPOSED NEXT ACTION: The root session must complete its integrated suite against the final wrapper source, generate the campaign freeze with actual architecture-specific seed-42 initial identities, and commit/publish that freeze before the first recipe optimizer update. Source changes after this review require a renewed source-bound check.

FACT: This review does not claim six completed runs, actual recipe initialization equality, neural resume reproduction under every LR, endpoint eligibility, LR selections or final campaign acceptance. Those claims require the actual campaign artifacts and the separately required post-run independent reproduction. No final/sealed inference, protocol freeze, final training, extra LR or scientific rescue is authorized by this review.

PRERUN_STATIC_REVIEW_QUALIFIED_RUNTIME_GATES_PENDING
