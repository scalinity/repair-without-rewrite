# Independent Generation-2 ByT5 2-pass nominal observation review

Date: 2026-10-08T21:51:49.436210+00:00

Reviewed base: `12d7e5a827da023a3dfb1af1c374be9dc33d2d3b`. Evidence: `experiments/manifests/generation_2/scientific-observation-independent-G2-ByT5-D1-10pass-seed42-lr3e-4.update07057.attempt03.json`; retained failed-write attempt01 and failed-launch attempt02. The receipts hash-bind the separate CPU checker, failed logs/partial receipt, immutable observation and previously independently verified checkpoint. The original serial job remains undisturbed. No model was constructed or executed by this review.

| Exact reporting label | Nominal passes | Nominal presentations | Completed optimizer update | Actual presentations | Signed presentation offset |
|---|---:|---:|---:|---:|---:|
| 2-pass nominal milestone — first completed update at/after boundary | 2 | 28,226 | 7,057 | 28,228 | +2 |

MEASURED RESULT: All 2,984 unique heldout case IDs exactly match the ordered frozen panel: 2,696 natural and 288 generated cases. Both completed observation payloads and their inventory reproduce. The observation state identity matches the independently hashed update-7,057 checkpoint; its COMPLETE and serialized-state payload hashes reproduce. Every row retains the exact milestone, frontier identity and original qualified recipe hash. The entire completed prefix was independently verified in `docs/reviews/G2_BYT5_2PASS_CHECKPOINT_INDEPENDENT_REVIEW.md`.

| Independently reconstructed decoding status | Cases |
|---|---:|
| complete | 2,914 |
| capped | 70 |

MEASURED RESULT: A separate byte-decoding implementation reproduces each stored text, status and reason from generated numeric IDs. Completed sequences have decoder-start PAD, terminal EOS and strict valid UTF8 bytes; capped sequences retain 512 emitted positions, valid decoded prefixes and the missing-EOS-at-cap reason. All 70 capped outputs remain retained. No dropping, repair, regeneration or treatment change occurs. Scientific WER, repair gates and endpoint adequacy remain UNRUN.

MEASURED RESULT: The 1,900 calibration IDs/hash independently reconstruct from natural panel rows. The receipt binds the complete observation and records no training, sealed-reference or recipe/checkpoint-selection use. Completed campaign observations at this cutoff record 72,200 calibration evaluations; repeated observations do not enlarge the unique calibration population or unique training extent.

| Measured observation component | Seconds |
|---|---:|
| Complete observation interval | 7214.049868 |
| Per-case decoding intervals | 5343.791777 |
| Per-case scoring intervals | 11.141651 |

FACT: Decode/scoring intervals are included in the observation interval, which belongs to the physical recipe attempt once. Its cost attaches to actual update 7,057 and 28,228 actual presentations, while 28,226 nominal presentations and +2 remain separately reported. The offset is inside the fixed 141,130-presentation training stream and adds no optimizer step, pass or unique training exposure. Monetary cost remains UNPRICED; full-recipe accounting remains UNRUN. The passing independent CPU check took 6.968966 measured seconds.

FACT: Checker attempt01 failed while sorting mixed null/text decoding-reason keys for JSON serialization; its source/log and zero-byte partial receipt remain retained outside Git and hash-bound in a separately labelled public failure record. Checker attempt02 failed to launch after a correction-preparation assertion; no checks ran and its log remains retained. Attempt03 maps a null reason to an explicit count label and passes. Failed-check durations are UNMEASURED. These reporting/launch failures caused no scientific source, artifact, process, replay or treatment changes.

MEASURED RESULT: All 47 frozen scientific sources, three scientific inputs, three frontier identities, 21 qualification receipts, 12 external artifact identities, seven original qualified recipe hashes and the separate four-state ByT5 schedule remain unchanged. Bound-volume identity/access/free-space checks pass before and after the CPU check.

FACT: Six B/C outcomes remain complete and all seven slots consumed. ByT5 has completed initialization and its 2-pass nominal observation; prescribed training is active. Both intermediate observations remain descriptive only, with no model, LR, duration or checkpoint selection. Adequacy remains solely at the exact ten-pass endpoint, update 35,283 and 141,130 presentations. Quantitative progress uses actual presentations; actual pass-equivalent progress at this observation is `28,228 / 14,113`, not exactly 2.000 passes. Full campaign scoring/gates, factorial/accounting reconstruction, four post-campaign reports and a new complete suite remain UNRUN until all seven outcomes exist and the accelerator is idle. Last complete suite: 505 passed, zero failures/skips; nine later targeted CPU analysis tests pass. No final/sealed work occurs.

PASS_INDEPENDENT_SCIENTIFIC_OBSERVATION_AND_STATE
