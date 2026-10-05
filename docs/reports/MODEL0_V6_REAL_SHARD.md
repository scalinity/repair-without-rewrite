# MODEL-0 V6 on admitted real material

Exact correctness-qualified MODEL-0 passed the bounded real-shard criterion without architecture changes: 8,621,312 parameters, width256, six layers, four query/two KV heads, FFN704, vocabulary16,384, context1,024. The prospective naming clarification in [amendments](../reviews/PROSPECTIVE_AMENDMENTS.md) preserves the immutable MODEL-1 campaign contract; this does not qualify B/C restoration convergence.

Only admitted TRAIN `text_raw` and source-disjoint HPO targets were read through the hash-bound reader. TRAIN loaded45,729 rows/314 components; HPO898 rows/12 components. Stable-ID BOS/target/EOS streams were packed into257-position blocks and shifted to256 native inputs/labels. TRAIN has6,905 blocks and1,767,680 input positions per presentation; HPO78 blocks and19,968 valid loss labels. Incomplete tails discard228 TRAIN and55 HPO stream positions;45,724/896 rows contribute positions, with all314/12 components retained. No sealed target enters fitting or evaluation.

The seed42 block permutation repeats deterministically.2,442 batch16 updates reach10,002,432 native inputs and valid labels:5.6585 full presentation equivalents, not10M unique language tokens. TRAIN’s raw BPE content is1,683,355 tokens plus91,458 BOS/EOS controls before packing. B/C paper-canonical restoration anchors are not substituted for this causal-LM count.

| Held-out checkpoint | CE on19,968 labels |
|---|---:|
| Initial random weights |9.764476874|
| Saved5,001,216-input checkpoint |6.278499505|
| Cold-resumed10,002,432 endpoint |6.022597875|

The endpoint improves0.255901630 over the actual saved midpoint and improves on the9.216M intermediate6.031562707. Every loss/gradient/model/moment is finite. AdamW uses beta(.9,.95), epsilon1e-8, decay.1, clip1; FP32 master/moments/accumulation, BF16 working arithmetic, native attention, TF32 explicitly disabled. LR is token-based peak3e-4,2% warmup, cosine floor.1, uninterrupted across cold resume. Initial weight SHA256 is`e0275c484f477899fe10f2da41e1ab9adb080ca327780d86b33980d40b09d835`; final is`9641c9068135ff7a7b6141e6009fbca5b8ab845a79365285fa49e3b484e265a4`.

Qualified phase1/phase2 loop wall times are76.929768/77.805635seconds, including in-loop evaluations and ledger I/O, excluding corpus encoding, initialization and pre-loop evaluation. Peak MLX allocation2,093,510,896bytes; process RSS730,873,856/775,831,552bytes overlaps that allocation. Post-loop checkpoint timer.188328/.190855seconds also includes final evaluation/hash/report work. `pmset` reported no recorded thermal/performance warning; temperature/utilization were not measured. No concurrent accelerator job ran.

Ignored evidence remains under `exports/foundation-repair/model0-v6-phase{1,2}-attempt02`: pre-update HEAD, dirty diff, code/config/runtime/tokenizer/manifest identities, initial weights, contiguous update/evaluation ledgers, atomic checkpoint COMPLETE hashes and summary. Phase2 `initial_identity` describes scratch pre-load weights; its actual resumed-start receipt was recorded in the final summary, not before updates. The [independent CPU review](../reviews/MODEL0_V6_INDEPENDENT_REVIEW.md) verified that restored weights/CE exactly match phase1 COMPLETE bytes, all reader order/cursors/schedule agree and endpoint arrays are finite. This retrospective resume-identity limitation remains disclosed; no receipt was rewritten.

Attempt01’s5,001,216 inputs are preserved as a provenance-limited partial run. Its mathematical repeat is identical, but it lacked full pre-update runtime/initial identity. Total session V6 expenditure is15,003,648 native inputs; the qualified trajectory is10,002,432. Prior failed/memorization evidence remains intact. No six B/C10M recipe slot was used.

Independent reconstruction checked full official TRAIN/HPO targets, every field hash, exact BPE streams, checkpoint arrays and token LR on all2,442 steps. Reader regressions passed. DEVELOPMENT convergence and generalization on the admitted LS-PC slice are evidenced; cross-domain/final restoration quality and paper freeze are not established.

PASS
