# Independent Generation-2 ByT5 5-pass nominal observation review

Date: 2026-10-09T03:54:54.364561+00:00

Reviewed base: `ab72152d2ee39b18fce7c15ecfea15567bbc8d98`. Evidence: `experiments/manifests/generation_2/scientific-observation-independent-G2-ByT5-D1-10pass-seed42-lr3e-4.update17642.attempt01.json`. The receipt hash-binds the separate CPU checker, immutable observation and previously independently verified checkpoint. The original serial job remains undisturbed. No model was constructed or executed by this review.

| Exact reporting label | Nominal passes | Nominal presentations | Completed optimizer update | Actual presentations | Signed presentation offset |
|---|---:|---:|---:|---:|---:|
| 5-pass nominal milestone — first completed update at/after boundary | 5 | 70,565 | 17,642 | 70,568 | +3 |

MEASURED RESULT: All 2,984 unique heldout case IDs exactly match the ordered frozen panel: 2,696 natural and 288 generated cases. Both completed observation payloads and their inventory reproduce. The observation state identity matches the independently hashed update-17,642 checkpoint; its COMPLETE and serialized-state payload hashes reproduce. Every row retains the exact milestone, frontier identity and original qualified recipe hash. The entire completed prefix was independently verified in `docs/reviews/G2_BYT5_5PASS_CHECKPOINT_INDEPENDENT_REVIEW.md`.

| Independently reconstructed decoding status | Cases |
|---|---:|
| complete | 2,812 |
| capped | 172 |

MEASURED RESULT: A separate byte-decoding implementation reproduces every stored text, status and reason from generated numeric IDs. Completed sequences have decoder-start PAD, terminal EOS and strict valid UTF8 bytes; capped sequences retain 512 emitted positions, valid decoded prefixes and the missing-EOS-at-cap reason. All 172 capped outputs remain retained. No dropping, repair, regeneration or treatment change occurs. Scientific WER, repair gates and endpoint adequacy remain UNRUN.

MEASURED RESULT: The 1,900 calibration IDs/hash independently reconstruct from natural panel rows. The receipt binds the complete observation and records no training, sealed-reference or recipe/checkpoint-selection use. Completed campaign observations at this cutoff record 74,100 calibration evaluations; repeated observations do not enlarge the unique calibration population or unique training extent.

| Measured observation component | Seconds |
|---|---:|
| Complete observation interval | 10059.125263 |
| Per-case decoding intervals | 7636.503629 |
| Per-case scoring intervals | 14.241679 |

FACT: Decode/scoring intervals are included in the observation interval, which belongs to the physical recipe attempt once. Its cost attaches to actual update 17,642 and 70,568 actual presentations, while 70,565 nominal presentations and +3 remain separately reported. The offset is inside the fixed 141,130-presentation training stream and adds no optimizer step, pass or unique training exposure. Monetary cost remains UNPRICED; full-recipe accounting remains UNRUN. The first executed five-pass observation checker passes in 7.904253 measured CPU seconds. Earlier failed CPU checks remain retained through the progress-receipt chain; no scientific replay or treatment change occurs.

MEASURED RESULT: All 47 frozen scientific sources, three scientific inputs, three frontier identities, 21 qualification receipts, 12 external artifact identities, seven original qualified recipe hashes and the separate four-state ByT5 schedule remain unchanged. Bound-volume identity/access/free-space checks pass before and after the CPU check.

FACT: Six B/C outcomes remain complete and all seven slots consumed. ByT5 has completed initialization and both prescribed intermediate observations; its original child process is training. Intermediate results remain descriptive only, with no model, LR, duration or checkpoint selection. Adequacy remains solely at the exact ten-pass endpoint, update 35,283 and 141,130 presentations. Quantitative progress uses actual presentations; actual pass-equivalent progress at this observation is `70,568 / 14,113`, not exactly 5.000 passes. Full campaign scoring/gates, factorial/accounting reconstruction, four post-campaign reports and a new complete suite remain UNRUN until all seven outcomes exist and the accelerator is idle. Last complete suite: 505 passed, zero failures/skips; nine later targeted CPU analysis tests pass. No final/sealed work occurs.

PASS_INDEPENDENT_SCIENTIFIC_OBSERVATION_AND_STATE
