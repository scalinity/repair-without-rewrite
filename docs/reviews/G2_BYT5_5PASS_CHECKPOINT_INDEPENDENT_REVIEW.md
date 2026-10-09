# Independent Generation-2 ByT5 5-pass nominal checkpoint review

Date: 2026-10-09T00:55:16.085547+00:00

Reviewed base: `848258e1a03b0772865971a2dfa3019d8f7d563f`. Evidence: `experiments/manifests/generation_2/scientific-byt5-prefix-independent.update17642.attempt01.json`. The receipt hash-binds the separate CPU checker, immutable full-prefix snapshot and completed checkpoint. The original serial parent and sole scientific child remain undisturbed; no model was constructed or executed by this review.

| Exact reporting label | Nominal passes | Nominal presentations | Completed optimizer update | Actual presentations | Signed presentation offset |
|---|---:|---:|---:|---:|---:|
| 5-pass nominal milestone — first completed update at/after boundary | 5 | 70,565 | 17,642 | 70,568 | +3 |

MEASURED RESULT: All 17,642 completed updates independently reconstruct frozen seed-42 shuffled D1 record order, presentation indices, pass indices and offsets. Every batch contains four records. Native source/target byte counts independently reproduce from raw strings plus EOS; constant LR remains 3e-4. Logged losses and gradient norms are finite. Update 17,641 incorporates 70,564 presentations, before the 70,565 nominal boundary; update 17,642 incorporates 70,568 and is the first completed state at or after it. Its crossing batch retains `[4, 5, 5, 5]`. No pass-boundary flush, split, reordered record or optimizer reset occurs.

MEASURED RESULT: The complete checkpoint inventory contains one serialized-state payload of 3,595,841,611 bytes, SHA-256 `61ec1e1efe41d698b67cea86c54e036c97eb2ec21634b3cd151f2382c2029cd5`. CPU-only inspection verifies completed update/presentation cursors, training mode, all 172 model-state tensors, 299,637,760 unique parameters, finite FP32 model tensors/AdamW moments, step 17,642 for every optimizer parameter, qualified optimizer settings and retained CPU/MPS RNG. The completed-update gradient-resume policy remains inherited zero_grad before the next batch. Independent portable-state hash: `abe7c0c28eb874ca90d31eccfd57398168a8637e7c752f14565ec83d0654db7d`. This verifies the saved state and accounting; future training and future evaluation state preservation remain unrun at this cutoff.

CALCULATION: The unchanged final geometry remains 35,283 optimizer updates, 141,130 presentations and a two-record last batch. These are future endpoint calculations. Actual pass-equivalent progress here is `70,568 / 14,113`; this state is not exactly 5.000 passes. Quantitative progress uses actual presentations, with nominal counts and signed offsets retained separately.

MEASURED RESULT: Cumulative logged training intervals through this checkpoint total 10215.431522 seconds. The earlier 2-pass prefix intervals are included in this total; adding the two prefix totals would double-count physical work. Training/checkpoint/evaluation intervals belong to the physical recipe attempt once. Full-recipe and completed 5-pass observation costs remain UNRUN; monetary cost remains UNPRICED. The +3 offset is inside the fixed 141,130-presentation stream and adds no optimizer step, pass or unique training extent. The passing CPU check took 11.516327 measured seconds.

FACT: A checker-preparation assertion ran before the intended +2-to-+3 reporting replacement and stopped before writing or launching a checker. Its failure record is retained privately and hash-bound in progress attempt20. Corrected preparation uses exact whole-number replacements; the first executed five-pass checker passes. The failed preparation performed no scientific checks or model execution and changed no scientific source/artifact/process. Its duration is UNMEASURED.

MEASURED RESULT: All 47 frozen scientific sources, three scientific inputs, three frontier identities, 21 qualification receipts, 12 external artifact identities, seven original qualified recipes and the separate four-state ByT5 schedule remain unchanged. Bound-volume identity/access/free-space checks pass before and after the CPU check.

FACT: Six B/C outcomes remain complete and all seven slots consumed. Initialization and the 2-pass nominal observation remain independently verified. The 5-pass nominal evaluation is active and has no completed receipt at this cutoff; its result is UNVERIFIED. Intermediate results are descriptive only, with no model, LR, duration or checkpoint selection. ByT5 adequacy remains solely at exact update 35,283 and 141,130 presentations. Full scientific gates, factorial/accounting reconstruction, four post-campaign reports and a new complete suite remain UNRUN until all seven outcomes exist and the accelerator is idle. Last complete suite: 505 passed, zero failures/skips; nine later targeted CPU analysis tests pass. No scientific treatment or final/sealed work changes.

PASS_INDEPENDENT_BYT5_COMPLETED_PREFIX_AND_CHECKPOINT
