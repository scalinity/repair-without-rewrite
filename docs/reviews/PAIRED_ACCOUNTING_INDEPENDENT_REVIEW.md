# Paired canonical/native accounting independent review

Disposition: **FRONTIER_MODEL_REVIEW_REQUIRED for the missing consequential reader/accounting choices.** The existing loss/count contracts and admitted natural-pool arithmetic are reproducible. They do not qualify a new paired mixed presentation stream or its BENCH-00 workload. No B/C 10M probe, new optimizer update, model forward/backward, MLX import, final inference, or protocol freeze was performed by this reviewer.

This review was performed independently against HEAD `f24712ed3b33e2396efbf4de89cf7409051ace4a` on 2026-10-05. Its ownership is this file only. Existing source, protocols, calibration attempts and raw evidence remain unchanged. The owner's continuation is identified below by SHA-256. Its frontier-escalation instruction supersedes an inference that a plausible development default is automatically authorized.

## Authoritative canonical charge

[Canonical §10.4](../design-inputs/EXTRACTED_CANONICAL_SOURCE.md#104-versioned-data-exposure-and-compute-ledgers), lines 1087–1110, and §12.3, line 1317, define the charge of presentation `i` as:

`c_i = number of project-tokenizer tokens in the frozen trusted accounting serialization of (trusted controls, clean accounting anchor_i, full written target_i)`.

The clean accounting anchor is the latent clean **spoken rendering** for generated pairs and the frozen existing official reference for real pairs. It is not the corrupted source. Trusted framing/EOS are counted once according to that serializer; padding is excluded. `C_paper = sum(c_i)` over presentations, including disclosed repetitions. The accounting anchor is never additional model input. Paired corruption views share the anchor, target and charge even when actual source length changes. Registry lines 344–352 preserve this distinction from native work and from the source-dependent product ledger.

This is the exact authoritative semantic formula. A universal numeric `+3`, `+4`, or another control constant is **not specified**. The canonical source explicitly refers to a serializer specification and explicit BOS/EOS/delimiter rules, but no adopted accounting serializer was found in the supplied source, registry, prospective amendments, protocol authorization or configuration. The reserved map in canonical §11.2, lines 1183–1205, identifies possible token IDs; it does not specify their accounting sequence or occurrences. The tokenizer artifact fixes the encoding of literal segments and reserved IDs, not the missing accounting framing.

Where reserved delimiters separate independently encoded literal anchor and target segments, the familiar decomposition would be `len(encode(anchor)) + len(encode(target)) + framing_count`. That decomposition requires the exact frozen serializer; it is not permission to choose `framing_count`. Neither C's event count nor B's supervised target length can determine it.

The prior [natural calibration runner](../../benchmarks/bc_real_calibration.py), line 50, uses `2 * len(encode(target)) + 3` for real-reference diagnostic fixtures. Its public report and prospective amendment expressly limit that workload to supplementary natural-shape calibration. It is not an adopted universal mixed-data charge. For generated data, clean spoken rendering and written target can differ; replacing the clean rendering with a second target copy changes the registered anchor. Canonical §15.2, lines 1553–1557, explicitly requires text corruption to start from the same spoken rendering as TTS rather than an already formatted target.

Existing native source serializers also have distinct scopes: [tokenizer.py](../../src/models/tokenizer.py), lines 164–170, emits `[BOS, task, SEP, source, EOS]` and labels itself `dev_source_frame_v1_not_frozen`; the prior natural benchmark, lines 45–46, emits `[task, SEP, source, EOS]`. The C source-binding interface accepts these variants. This is not proof that either variant is the canonical accounting serializer. The new reader must bind one explicit native framing identity and the separately approved accounting identity, rather than infer either from a prior counter.

## Complete updates, overshoot and partial state

Canonical §10.4, line 1110, requires the same predeclared presentation schedule and initial 32,768 canonical accumulation target if BENCH supports it. §19.2, line 1999, says to accumulate at variable lengths and **finish the last whole example**, then log the true charge and supervised denominator. Thus a whole-example threshold crossing is allowed; splitting a pair or changing one arm's order to manufacture a rounded total is forbidden. The final campaign stops after the common completed update first reaches 150M and reports overshoot (registry lines 374–378; canonical lines 1726–1728). That final-budget rule does not authorize a smaller final update just to hit 150M exactly.

Canonical §8.4, lines 810–836, requires accumulation followed by one normalization, one global clip, one AdamW update and accumulator clearing. Exposure is charged once per presented example, independently of microbatch partitioning and C event density. Padding may increase physical work but not `c_i`. Rejected candidates and failed presentations require explicit outcome/cost records; silently removing them cannot establish a matched stream.

Canonical §19.7, line 2083, explicitly rehearses an **update-boundary** checkpoint and 20 resumed updates. Canonical §19.11, lines 2262–2264, also permits a mid-accumulation save conditional on serializing the accumulator and denominator. It does not explicitly prohibit mid-update publication. Under the continuation's partial-case requirement, a claim of an intentionally prohibited partial checkpoint therefore needs actual authority; a missing implementation is not that authority.

The existing [checkpoint implementation](../../src/models/training.py), lines 188–290, preserves FP32 parameter/moment/gradient arrays, optimizer step, processed/pending count, scalar denominator, microbatch count, cursor/order/phase, RNG states, identities, backend and atomic completion hashes. It preserves failed temporary directories. For a future mixed C update, equivalent partial resume additionally requires the four **whole-update** denominators, the pending ordered example/label queue and completed microstep position, accounting sums, mixture/phase/order state, and generation state where applicable. The queue/counts can be stored directly or recovered through an exact hash-bound deterministic reconstruction; merely saving a next-row cursor is insufficient. Those requirements follow from the already specified objective and same-presentation resume requirement; they are implementation obligations, not an alternative loss design. This metadata is not present in the generic causal trainer's checkpoint schema.

A finite reader exhausting its schedule with a below-threshold partial update is a different question from stopping a final campaign at the first complete budget-crossing update. No explicit exhaustion policy selecting flush, discard, wrap or continuation was found. Until the presentation/repetition policy is approved, none may be silently chosen. No new partial-accumulation or cold-resume behavior has been qualified in this continuation.

The scheduler's unit is accumulated canonical exposure, not B target tokens or C decisions. The final schedule is continuous through 100M/140M difficulty changes, with 3M linear warmup and cosine decay to 10% at 150M (canonical lines 1075 and 1728; registry lines 372–373). The existing `Trainer.update` samples its schedule at `processed_tokens + pending_tokens`, records that endpoint and then clears pending state (lines 156–169). That is an inspected existing implementation convention. It cannot turn the generic trainer's default padded `ids.size` count into the paper clock, nor does the 150M schedule automatically declare a shortened pilot's phase plan. Lost or repeated work after infrastructure failure must remain visible alongside the successful-update counter.

## B and C loss/native-count contracts

B's encoder attends to all valid source positions; its decoder is causal and cross-attends to valid source positions with source PAD excluded. Canonical §9.3, lines 884–886, forbids unisolated packing and all-masked rows. B predicts the full written target plus EOS; BOS is a decoder input, not an additional target. Trusted source controls, source tokens and target padding are excluded from the supervised denominator. For a queued update:

`D_B = sum_i (ordinary target BPE tokens_i + 1 target EOS_i)`

`L_B = sum_j S_B,j / D_B`.

Accumulate gradients of unnormalized valid-target sums and divide once by `D_B`, or scale every microbatch sum by the same whole-update `D_B` before backpropagation and accumulate without a second division. Averaging microbatch means changes the objective when their valid lengths differ. Native encoder positions, native decoder positions and padded tensor positions remain separate ledgers. Reusing `Trainer.accumulate` unchanged would also reuse its causal-LM objective and `ids.size` default exposure, which can count padding (training.py lines 134–153); the existing explicit `processed_tokens` override alone does not supply the missing canonical serializer or B/C losses.

C's exact teacher-forced serialization is specified in canonical §9.4, lines 935–974, registry lines 288–295, and [edits.py](../../src/models/edits.py), lines 161–221. If example `i` has `K_i` source-relative edits and `R_i` ordinary replacement BPE tokens:

| Quantity | Per-example count |
|---|---:|
| C teacher decoder inputs | `1 + R_i + 3K_i` |
| Action labels, including terminal END/ABSTAIN | `K_i + 1` |
| Start pointer labels | `K_i` |
| End pointer labels | `K_i` |
| Vocabulary labels, including one END_EDIT per edit | `R_i + K_i` |

Identity contributes one BOS input and one END action, with zero pointer/vocabulary labels. An empty replacement still contributes its END_EDIT vocabulary label. Terminal END/ABSTAIN adds no extra EOS or feedback decoder input. The three per-edit feedback/input positions are the start feedback, end feedback and appended END_EDIT. Copied source gaps create no replacement loss.

Compute `D_action = sum_i(K_i+1)`, `D_start = D_end = sum_i K_i`, and `D_vocab = sum_i(R_i+K_i)` over the **entire queued update before** microbatch backpropagation. With all four registered component weights 1:

`L_C,j = sum_{k:D_k>0} S_C,j,k / D_k`.

Sum these gradients in one FP32 buffer, clip once, apply AdamW once, materialize state, then clear. Do not divide by microbatch count, canonical exposure, target-token count or the sum of C's decisions. A component with `D_k=0` contributes zero. `bc.py` lines 131–162 produce component loss sums; lines 227–232 use the caller-supplied whole-update denominators. `edits.py` lines 202–221 implement the required count aggregation and zero-component handling. The four component means are the declared representation objective, not a bug to repair into a common B denominator.

`GradientAccumulator.gradients(already_normalized=True)` (training.py lines 64–69) supports the specified already-weighted C gradients without division. Its default scalar-denominator path remains appropriate for an unnormalized B loss sum. AdamW lines 92–115 clips the accumulated global norm once and increments the optimizer step once; its uniquely keyed parameters, matrix-only decay and FP32 state policy agree with registry lines 367–370. These are inspected source properties, not newly measured accelerator execution.

## Independent CPU measurements

The root's preserved [pool audit](../../exports/paired-reader-bench/admitted-pool-audit-attempt01/summary.json) is a static inventory with `presentation_index:null`, zero mixed presentations and zero new optimizer updates. This reviewer independently reloaded the qualified trained tokenizer and official released targets through the existing reader; rejoined every natural pair to current role/group/reference hashes; checked strict source/target BPE round trips; derived `K`, `R` and all counts directly from source-bound ordered edits; verified exact rendering on legal UTF-8/BPE boundaries; and compared every inventory field. The independent CPU run took **4.677158 seconds**, imported no MLX module and found **zero discrepancies across all 1,120 rows**. No TRAIN/CAL source group intersected.

| Static admitted pool | TRAIN | CALIBRATION |
|---|---:|---:|
| Rows / source groups | 1,024 / 48 | 96 / 5 |
| Rows per group, min–max | 6–61 | 13–28 |
| Exact byte-identity pairs | 182 | 19 |
| Source bytes / target bytes | 123,605 / 124,396 | 11,171 / 11,257 |
| Raw source BPE / target BPE | 24,456 / 24,846 | 2,318 / 2,377 |
| Prior three-control native source positions | 27,528 | 2,606 |
| BOS-containing helper native source positions | 28,552 | 2,702 |
| B valid target+EOS labels | 25,870 | 2,473 |
| Gold edits `K` / replacement BPE `R` | 1,987 / 3,094 | 192 / 297 |
| C teacher decoder inputs | 10,079 | 969 |
| C action / start / end / vocabulary labels | 3,011 / 1,987 / 1,987 / 5,081 | 288 / 192 / 192 / 489 |
| Total C supervised decisions, distinct from C inputs | 12,066 | 1,161 |
| Common prior 1,024-context envelope rejections | 0 | 0 |
| **Prior diagnostic `2*target_BPE+3`; not registered canonical charge** | **52,764** | **5,042** |

CAL is reported solely as a disjoint inventory; it is not eligible TRAIN input. Earlier comparator/native development consumption remains governed by its preserved consumption receipt. The static full-pool inventory does not make consumed CAL untouched again.

The numerical divergence is substantial even on the same admitted natural examples: TRAIN B has 25,870 supervised target/EOS labels, while C has 10,079 teacher inputs and 12,066 supervised decisions. These cannot be interchanged with one another or with a paper-canonical budget. Native positions need not match to make canonical presentation exposure match.

Two independent CPU algebra checks expose common accumulation errors without executing a model. For B, microbatches with summed losses `(3,45)` and valid counts `(1,9)` yield the correct pooled mean `48/10 = 4.8`; averaging their means yields `4.0`. For C, an identity microbatch has counts `(1,0,0,0)` and sums `(2,0,0,0)`; a two-edit microbatch has counts `(3,2,2,5)` and sums `(12,8,10,20)`. Whole-update denominators `(4,2,2,5)` yield `16.5`, exactly matching the sum of globally normalized microbatch objectives. Averaging independently normalized microbatch objectives yields `9.5`. Zero-count components were omitted. These prove count/normalization algebra, not gradient equivalence, masks, resumed arrays or new reader behavior.

## Consequential missing choices and smallest escalation

The following choices were not adopted by the inspected authorities. They affect experiment validity and must not be selected merely to permit execution:

1. **Exact accounting serializer:** trusted control order/multiplicity, BOS/EOS/delimiter inclusion and anchor/target segment boundaries. Fixing one explicit shared version preserves the registered clean-anchor contrast; substituting corrupted-source counts, decoder positions or duplicate written targets for generated spoken anchors confounds it. The existing diagnostic constant is evidence to retain, not authority to generalize.
2. **Short development phase/schedule declaration:** canonical lines 1071–1075 require each 10M pilot's predeclared schedule; the 100M/40M/10M curriculum is specified for final trajectories. No inspected document assigns the shortened pilot across those phases or declares its exact difficulty/replay plan. The phase table cannot silently be proportionally compressed or treated as a 10M final-phase run. The registered LR grid, optimizer and component weights remain fixed; this is a missing declaration, not a proposed redesign.
3. **Presentation support/repetition/order and finite-stream exhaustion policy:** the 30/20/10/40 shares are canonical-exposure shares (canonical lines 1065 and 1546–1551), not row probabilities. Choosing those probabilities would not guarantee the shares when length distributions differ. Canonical lines 1720–1722 require frozen replay/difficulty/source policy and measured repetition, but provide no numerical source-group cap, unique-support threshold or drift tolerance. The existing target reader and technical DEV stress generator are not the new approved training presentation plan. Do not move their held-out lineages into TRAIN or treat a length-only static audit as that plan. The reader review owns the detailed construction gaps; this accounting review does not fill them in.

Whole-update component denominators, PAD exclusion, correct byte-bound maps, accumulator materialization and complete checkpoint fields are routine implementation requirements with explicit source authority. They do not need a new loss policy. Final complete-update overshoot is already specified and is not itself a missing choice.

The previous four-request natural calibration, with about 184–238 diagnostic anchors/update and explicitly approved supplemental thermal LR 0, cannot qualify the nominal 32,768 mixed regime. Canonical BENCH lines 2076–2083 and registry lines 520–522 require five complete warmups, 100 timed complete updates, actual reader/masks/loss, a separate 20-minute thermal segment and 20-update cold resume at the chosen regime. No inspected amendment transfers the earlier LR-0 permission or four-request regime to this new gate. A smaller regime or different effective training path requires the prospectively justified equivalence/authority requested by the owner, not a silent replacement. This review supplies no new BENCH throughput, memory result, ETA or reserve estimate.

The smallest review request is to resolve the exact accounting/pilot/presentation declarations while retaining the existing architecture, four-component C objective, canonical clean-anchor definition, mixture shares, final budget and primary estimand. Until that authority exists, dependent mixed-reader scheduling, timed BENCH and six probe admission remain unqualified. Failed and prior scoped attempts stay visible.

## Evidence identities

SHA-256 values were read from current bytes, not copied solely from reports:

| Input/evidence | SHA-256 |
|---|---|
| Owner continuation request | `99a33c159b32df82ef5b29a756d8be0b4d801507c7ae1495b5cd8b2e04b1ed7a` |
| `docs/design-inputs/EXTRACTED_CANONICAL_SOURCE.md` | `94746ef2c223f9f461d5dc92378961813e8f9377fe89fd5166dd9d6097ced746` |
| `docs/design-inputs/LocalFlow_Publication_Experiment_Registry_v2.txt` | `596932dd91e0b108936c3a7a80245f4f44df5cfeac4f13d6fda8cfb30412cfe0` |
| `docs/reviews/PROSPECTIVE_AMENDMENTS.md` | `74c4d40bd47badda6d09948a37183217fc567edcab738963b5cdf876a6bbdf22` |
| `experiments/protocol/development_authorization.json` | `4ebbf9c665948762c46b726d210cd0b62e0253bfd93ce3bed6a122b54f493702` |
| `src/data/development_reader.py` | `24f61cb4a8245831b112fd2a25aa26e332e1cea6526d1e6ddd69f25d7a2ad3f5` |
| `src/models/tokenizer.py` | `c6b7452659ae1654ca36d868f33367d17b03df0ad3325b58e993ccaf454d7372` |
| `src/models/edits.py` | `9a2b752fb50328e1f857a33fd011dee7e91681dfd5916938be0f1d706513e461` |
| `src/models/training.py` | `98fb789ff3e6fd9c20bfc6627be2153fdbc7527b362f50ca6b8acbd52a44f3b5` |
| `src/models/bc.py` | `d58022e956b3adbd8d6a1c635ef9a7774efbd83aa5f8d8d65643c8f2d53be067` |
| `benchmarks/bc_real_calibration.py` | `ac159325e27c0f832ded1a56b60612332d6c2c453ead1a7c1430ffebc9cac411` |
| Qualified `configs/tokenizer_development/tokenizer.json` | `b125551f3c3627edc9cb8d325bc70bfd8340df1518f03d0fd16d140ff7ace6ca` |
| Qualified `configs/tokenizer_development/special_tokens.json` | `db75b2bec29e695e7843ac530fbe2dec4a5be128c713fe3186ea2e4d6efa03e2` |
| Current admitted TRAIN/CAL/HPO role manifest | `56c5889d952c83120267ea92b4aaf8bcec63dff61a34e83ce531c9be97b3eb98` |
| Current training-supply qualification receipt | `d0b1de70c2d2a7c7bbc7ad711a4d771fa91a22ef399651b0482aaeeee7616842` |
| Prior natural `development-asr-pairs-attempt01/pairs.jsonl` | `ce4a170a086afee430085c4e6f665e8af58b8c68091afc27f10ee403c81951d8` |
| New static `admitted-pool-audit-attempt01/inventory.jsonl` | `0f09c51308928db215aed1aa7a50e6da52affba915d9025ea9a7e3e14633ed8b` |
| New static `admitted-pool-audit-attempt01/summary.json` | `3fea973e215f0f09a26e87f1702cf629b61d069a0f9f2fef5839352dfbd0a224` |

The reproduced pool/count checks pass within their CPU-only scope. **The new paired reader, complete-update BENCH, partial/cold-resume qualification and six probe authorization remain unestablished.**
