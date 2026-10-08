# Independent Generation-2 ByT5 2-pass nominal checkpoint review

Date: 2026-10-08T19:48:04.598333+00:00

Reviewed base: `fe3fde65c5798606ac6c1fcebf0da7451d65459f`. Evidence: `experiments/manifests/generation_2/scientific-byt5-prefix-independent.update07057.attempt01.json`. The receipt hash-binds the separate CPU checker, immutable prefix snapshot and completed checkpoint. No model was constructed or executed by the review; the original serial parent and sole scientific child remain undisturbed.

| Exact reporting label | Nominal passes | Nominal presentations | Completed optimizer update | Actual presentations | Signed presentation offset |
|---|---:|---:|---:|---:|---:|
| 2-pass nominal milestone — first completed update at/after boundary | 2 | 28,226 | 7,057 | 28,228 | +2 |

MEASURED RESULT: All 7,057 completed updates independently reconstruct the frozen seed-42 shuffled D1 record order, presentation indices, pass indices and offsets. Every batch contains four records; native source and target byte counts independently reproduce from the corresponding raw strings plus EOS. The qualified constant LR remains 3e-4. Logged losses and gradient norms are finite. Update 7,056 incorporates 28,224 presentations, before the 28,226 nominal boundary; update 7,057 incorporates 28,228 and is the first completed state at or after it. Its crossing batch retains pass indices `[1, 1, 2, 2]`. No flush, split, reordered record or optimizer reset occurs.

MEASURED RESULT: The complete checkpoint inventory contains one serialized-state payload of 3,595,841,611 bytes. Its SHA-256 is `c6652039d8e9989ff90c7c08bdd15812ec2b70aad66e86411ad1bd688f224c53`. CPU-only inspection verifies the completed update/presentation cursors, training mode, all 172 model-state tensors, 299,637,760 unique parameters, finite FP32 model tensors and AdamW moments, step 7,057 for every optimizer parameter and the qualified optimizer settings. CPU and MPS RNG state are retained. The completed-update gradient-resume policy remains inherited zero_grad before the next batch. The independent portable-state hash is `6057ed5b0ca9be72533f6cdc16578916cc9d8b31f44ed4cfcfc3d3377233a88f`. This verifies the saved state and accounting; exact execution of future training and future evaluation state preservation remain unrun at this cutoff.

CALCULATION: The unchanged full-stream geometry remains 141,130 presentations, 35,283 optimizer updates and a final two-record batch. The calculated 5-pass crossing batch remains `[4, 5, 5, 5]` at update 17,642. These are future schedule calculations, not claims that those updates have executed. Actual pass-equivalent progress here is `28,228 / 14,113`; this state is not exactly 2.000 passes. Quantitative progress uses actual presentations, with nominal counts and the signed offset retained separately.

MEASURED RESULT: Logged training intervals for this prefix total 4302.232741 seconds. The independent CPU review took 11.646211 seconds. Training, checkpoint and evaluation intervals belong to the physical recipe attempt once. Full recipe and completed intermediate evaluation costs remain UNRUN; monetary cost remains UNPRICED. The +2 offset is already inside the fixed 141,130-presentation stream and adds no optimizer step, pass or unique training extent.

MEASURED RESULT: All 47 frozen scientific sources, three scientific inputs, three frontier identities, 21 qualification receipts, 12 external artifact identities, seven original qualified recipes and the separate four-state ByT5 schedule remain unchanged. Bound-volume identity/access/free-space checks pass before and after the CPU check.

FACT: Six B/C outcomes are complete and all seven slots consumed. ByT5 initialization remains independently verified. The 2-pass nominal evaluation is active and has no completed observation receipt at this cutoff; its results are UNVERIFIED. Both intermediate observations remain descriptive only, with no model, LR, duration or checkpoint selection. ByT5 adequacy remains solely at the exact ten-pass endpoint, update 35,283 and 141,130 presentations. Full scientific gates, factorial/accounting reconstruction, post-campaign reports and a new complete suite remain UNRUN until all seven outcomes exist and the accelerator is idle. The last complete suite remains 505 passed, zero failures/skips; nine later targeted CPU analysis tests pass. No scientific treatment or final/sealed work changes.

PASS_INDEPENDENT_BYT5_COMPLETED_PREFIX_AND_CHECKPOINT
