# MODEL-0 correctness foundation

**MEASURED RESULT — bounded development qualification.** V0–V5, V7 and V8 passed on the pinned MLX 0.32.3 native Metal backend with `MLX_ENABLE_TF32=0`. V6 was not run. This is not completion of the full correctness ladder, a publication gate, a language-quality result, or BENCH-00.

The exact MODEL-0 implementation has **8,621,312 uniquely owned trainable parameters**: one 16,384×256 embedding, six causal blocks of 737,792 parameters, and one 256-scale final RMSNorm. The decoder has 4 query / 2 KV heads, head dimension 64, SwiGLU width 704, adjacent-coordinate RoPE base 10,000, epsilon 1e-6, and no biases or dropout. Matrices are stored in output-by-input order, the transpose of the specification's notation. Parameter shapes, names, dtypes and counts are in `raw/model0/exact_geometry.json`.

## Executed gates and their limits

| Gate | Status | Executed evidence |
|---|---|---|
| V0 shapes/count/dtypes | PASS | Exact MODEL-0 leaf count and forward; tiny seq2seq leaf enumeration; exact-model post-update master/moment/accumulator FP32 inventories and BF16 working policy. |
| V1 attention/masks/cache | PASS | Independent NumPy GQA oracle, native/reference forward and Q/K/V gradients; exact causal future-perturbation equality; adjacent RoPE zero/norm/relative-dot checks; padding and all-masked rejection; tiny bidirectional/cross masks and projected cross-K/V reuse. Exact MODEL-0 cached 1/3/4-token chunks also match full forward. |
| V2 deterministic forward | PASS | Repeated FP32/BF16 execution, independent complete tiny explicit-weight NumPy FP64 decoder forward, exact-model reference/native parity. |
| V3 gradients | PASS | Finite nonzero intended leaves in FP32/BF16; numerical derivatives on a 2×2 linear projection and tiny decoder embedding/down projections at 1e-3 relative tolerance. Tiny decoder numerical loss is independently recomputed in NumPy FP64. Exact MODEL-0 native/reference mean-CE gradients and direction agree. |
| V4 fixed 4×64 overfit | PASS | Exact MODEL-0, seed 42: mean CE 9.751412→**0.008716893**, teacher accuracy **100%**, 30 of 2,000 allowed updates, 7,680 processed fixture tokens. Fixed batch has 256 tokens and 252 shifted targets. |
| V5 fixed 2k corpus | PASS | Exact MODEL-0 on exactly **2,000 fixed token positions**: CE 9.744438→**0.097204573**, teacher accuracy 100%, 40 of 5,000 allowed updates, 80,000 processed tokens. All **20/20 designated 32-token greedy continuations** from 8-token prefixes match exactly. |
| V6 real-shard convergence | NOT_RUN | Canonical gate requires at least 10M MODEL-1 real-shard tokens, held-out loss improvement versus initialization and an earlier checkpoint, plus separate source-conditioned development convergence. Synthetic MODEL-0 memorization is not a substitute. |
| V7 next-20-update resume | PASS | Exact MODEL-0 BF16 native path: interrupted/resumed next 20 updates have identical loss, LR, recorded token/cursor progress and final FP32 parameter bytes. Tiny tests also restore mid-accumulation gradients/denominators and Python, NumPy, explicit-key MLX and augmentation RNGs. |
| V8 seed reproducibility | PASS | Same seed and fixed data/backend repeat the exact short trajectory and final parameter bytes. Second development seed **43** reaches CE **0.004919071**, 100% accuracy, in 30 updates on the same 4×64 fixture. |

These are deliberately easy, non-conflicting periodic token fixtures. V4 uses a 16-token cycle and V5 a 64-token cycle. The 2,000 corpus positions are not 2,000 independent linguistic examples. The tests show mathematical learning/memorization and checkpoint mechanics; they establish neither reference restoration nor held-out language utility. No final seed was used.

The V4/V5/V8 test optimizer has decay disabled and peak LR 0.003, with the recorded token-based warmup/cosine schedule. This is an isolated overfit recipe, not the paper's 1e-4/3e-4/6e-4 sweep or a selected final recipe. No curriculum or final schedule was frozen.

## Numerical policy and preserved failures

The first suite attempt had **14 failures / 22 passes**. One was an implementation API error: MLX 0.32.3 `sum` accepts no `dtype` argument. This was corrected by reducing an already-FP32 loss array. Other FP32 comparisons showed maximum errors around 6.4e-4, including differences between single-token and batched cached execution. MLX's documented default can use reduced-precision FP32 matrix operations on this hardware. Disabling that route with `MLX_ENABLE_TF32=0` resolved those failures at the original tolerances. See the [official precision documentation](https://ml-explore.github.io/mlx/build/html/usage/precision.html).

The second suite attempt had **1 failure / 35 passes**: finite differencing a down-projection derivative near 0.0065 by subtracting FP32 losses about 6 apart was numerically ill-conditioned. The final test computes those central differences through an independent NumPy FP64 forward, retains the 1e-3 derivative tolerance, and checks the same well-conditioned largest-gradient coordinates. No derivative tolerance was widened.

An exact-model pre-overfit check also failed when applying the BF16 absolute-gradient tolerance to an **unnormalized seven-label loss sum**: 35 of 4,194,304 embedding elements failed, with maximum offending absolute difference **0.06250226**. Its original output is retained. The corrected test differentiates canonical **mean CE**, dividing both loss paths by the **seven valid labels**. This is a normalization clarification, not a tolerance increase. It retains atol/rtol 0.02/0.02 and independent direction checks. For the corrected exact-model test, the largest per-leaf gradient discrepancy is **0.013672113**. The zero FP32 discrepancy and BF16 direction checks are retained in the exact-geometry record.

| Exact MODEL-0 comparison | FP32 | BF16 |
|---|---:|---:|
| Native/reference forward max absolute difference | 9.536743e-7 | 0 |
| Cached/full max absolute difference | 1.072884e-6 | 6.103516e-5 |
| Reference mean CE | 9.841774940 | 9.842430115 |
| Native mean CE | 9.841774940 | 9.841604233 |
| Largest native/reference mean-gradient difference | 0 | 0.013672113 |

FP32 comparisons use atol 1e-5 / rtol 1e-4; BF16 bounded-tensor checks use atol/rtol 0.02, with positive gradient direction dot products. Uneven microbatch accumulation uses a per-leaf normwise FP32 relative tolerance below 1e-5. Causality, shape, byte and reserved-ID assertions are exact. The TF32 default remains unqualified for these contracts; dtype names alone do not certify FP32 computation.

All failures remain on disk: `raw/model0/pytest_attempt_01.txt`, `pytest_attempt_02.txt`, and `v4_attempt_01.txt`. Attempt 03 passed 36 tests after an interim finite-difference conditioning fix. Attempt 04 passed **37 tests** in **0.66 seconds**, including the stronger independent full-forward/FP64 derivative oracle. Pytest duration is a correctness duration, not a training benchmark.

## Optimizer, accumulation and checkpoint behavior

Master leaves remain FP32. Differentiable casts supply BF16 working projections/residuals. RMS statistics, attention softmax and CE reductions use FP32. The explicit AdamW has beta1 0.9, beta2 0.95, epsilon 1e-8, bias correction, matrix-only decoupled decay, and global clipping after whole-update accumulation. The tied embedding has one leaf and is updated once. Two scalar steps match independent calculations. Unequal microbatch valid counts match an equivalent complete batch; gradients are divided once by the whole valid-target denominator.

`GradientAccumulator.gradients(already_normalized=True)` supports C's separately normalized component objective without a second shared-token division. C's event/loss qualification is reported separately by the B/C owner.

The checkpoint stores FP32 model, both moments, optimizer step/policy, token scheduler and count, data order/cursor, phase, exact identity metadata, explicit keyed MLX RNG, Python and NumPy RNGs, augmentation RNG, and mid-accumulation buffer/count/pending exposure/loss state. Atomic new-directory publication follows array readback, shape/dtype/checksum checks and a finite forward probe. Partial writes never become complete checkpoints. The explicit-key policy avoids using the opaque global MLX RNG during training. A caller introducing other stochastic MLX operations must use the saved key path.

The exact MODEL-0 checkpoint is `checkpoints/model0_bounded_resume/`: **138,056,061 bytes**, measured write/read times **0.175931 / 0.112901 seconds**. These include the separate accumulator and verification overhead. They are one bounded correctness checkpoint on a warm local system; they are not a storage/IO forecast for BENCH-00. The reader/sampler integration beyond the fixed test schedule remains unqualified.

## Byte-BPE interface

The reversible trainer/encoder/decoder and trusted serializer preserve raw UTF-8 bytes, spaces, CRLF, combining marks and literal control-looking strings. The full canonical **64 reserved IDs** and the byte/merge allocation are explicit. Source maps distinguish token-to-byte offsets, code-point-to-byte offsets, and legal UTF-8 pointer boundaries. Decoding joins byte strings before strict UTF-8 decoding; malformed Unicode, reserved/unknown literal IDs and invalid merge maps reject.

Two **development-only 336-entry tokenizers** (256 bytes + 64 reserved + 16 learned toy-corpus merges), with unrestricted versus digit-isolating segmentation, each passed **10,000 exact round trips** over 16 categories with **zero unintended reserved IDs**. Total: **20,000 executed string-policy checks**. The independent 10k evaluation strings did not enter merge training.

| Policy | Tokens/UTF-8 byte | p50 / p95 tokens | Total encode/decode time | Above 1,024 tokens |
|---|---:|---:|---:|---:|
| Unrestricted | 0.968055 | 15 / 29 | 0.025887 s | 0 |
| Digit isolation | 0.974840 | 15 / 30 | 0.026136 s | 0 |

These toy-merge values do not select the final digit policy or qualify real identifier/context efficiency. The **16,384-entry tokenizer has not been trained**, and no 16,064-merge artifact is fabricated. The exact model nevertheless uses its required 16,384 embedding rows. Final permitted tokenizer supply, corpus/merge identity and model-cost comparisons remain pending. `dev_source_frame_v1_not_frozen` is a trusted development interface, not final paper serialization.

## Provenance and resource accounting

Identity records show Python **3.12.15**, MLX **0.32.3**, default GPU device, **Apple M5 Pro**, Metal architecture `applegpu_g17s`, reported unified memory **51,539,607,552 bytes**, and `MLX_ENABLE_TF32=0`. Exact hardware bin, OS/power/thermal state and dependency identities belong in the root hardware report. No GPU utilization or isolated sustained rate is inferred here.

V4 seed 42 took **1.541644 s**, V5 **4.018222 s** including greedy continuation checks, and V8 seed 43 **0.792651 s**. The exact-model training ledger records **108,672 processed fixture tokens**, including **13,312 repeated/resume/reproducibility tokens**. Tiny unit-test execution and evaluation tokens are separate from that training exposure ledger; failed numerical-check attempts performed no optimizer updates. Other agents' CPU work may overlap these durations. These measurements are not BENCH-00, and no one-month forecast follows from them.

Machine-readable gate evidence is `raw/model0/gate_evidence.json`; exact code/config hashes and run identities are in `v4_identity.json` and `remaining_identity.json`. Data, initial/final parameter hashes, optimizer/schedule inventories and per-update ledgers are in `v4_seed42.json`, `v5_seed42.json`, `v8_seed43.json` and their `_steps.jsonl` companions. Resume trajectories are in `resume_reproducibility.json`; tokenizer distribution evidence is in `tokenizer_roundtrip.json`.

**PROPOSED NEXT ACTION:** independently review the owned mathematical/optimizer/checkpoint code, then use V0–V4 evidence to admit the separately owned native calibration. Keep V6, real data/tokenizer qualification and source-conditioned useful-learning gates pending. No final confirmatory training, sealed inference, protocol freeze, cloud spending or production LocalFlow modification occurred in this subtask.
