# Generation-2 ByT5 runner qualification

FACT: Reported at 2026-10-07T17:47:14.812454+00:00, reviewed source commit `01578311c75d10e8f4b2da67add9a9f2cd672c3f`. All runs use development seed 42 and distinct qualification IDs. All seven scientific recipes remain AUTHORIZED_UNSTARTED.

MEASURED RESULT: The pinned official ByT5-small revision `68377bdc18a2ffec8a0533fef03b1c513a4dd49d` completed exactly 100 qualification optimizer updates and 400 TRAIN presentations. The native FP32 MPS runner uses eager attention, no fallback, no task prefix, batch 4, LR 3e-4, AdamW beta1 .9/beta2 .999/epsilon 1e-8/decay .01, and global gradient clip 1. There are 299,637,760 unique parameters.

| Measurement | Value |
|---|---:|
| Mean update seconds | 0.658475 |
| Conservative update seconds | 0.989414 |
| Complete training-loop seconds | 98.941447 |
| Initial full-panel seconds | 8709.827223 |
| Update100 full-panel seconds | 6125.936260 |
| Initial snapshot seconds | 2.489973 |
| Update100 snapshot seconds | 10.389620 |
| Total qualification seconds | 14954.561119 |

CALCULATION: Conservative update time is the maximum of the 100-update mean, last-25 mean, and whole training-loop time divided by 100. The frozen scientific extent is 14,113 distinct TRAIN pairs, ten complete passes, 141,130 presentations, 35,283 continuous batch-4 updates, and a final two-row batch. Pass crossings never introduce extra short batches. The final short-batch tensor/loss geometry is checked with a forward pass and no 101st optimizer update. The legacy 600-update/900-second adaptation extent does not apply to this approved G2 recipe.

MEASURED RESULT: Every required D1 source and target fits the 512-position native byte-plus-EOS capacity; no row is truncated, replaced or dropped. Both full 2,984-case greedy panels are retained, with any invalid/incomplete output retained under existing scoring rules. Generation uses input IDs and attention masks only; references are used afterward by the scorer. Complete checkpoint model/moments/RNG state is exact on portable CPU readback.

FACT: Independent index arithmetic, UTF8/EOS counts, every logged 100-update presentation/denominator, all ten-pass counts, both full panels, and portable Torch state are verified in `independent-byt5.attempt01.json`. No G2 batching/interface/trainer helper is imported. Evidence is `experiments/manifests/generation_2/byt5-qualification.attempt02.json`, `independent-byt5.attempt01.json` and complete external `byt5-v1/` artifacts. Qualification weights are retained and forbidden as scientific initializers; the future scientific run begins from the official pinned weights. Attempt01 failed while serializing its first initial score, before any optimizer update. Its complete initial snapshot and partial remain retained, its measured duration is charged, and its one unwritten CAL use is counted separately. The mechanical repair uses the existing canonical scorer serializer; attempt02 is the sole actual 100-update qualification trajectory with unchanged scientific config and source/panel/official-weight hashes. This check establishes runner/resource correctness, not comparator adequacy.

MEASURED RESULT: macOS-reported peak process RSS is 9,402,466,304 bytes (8.756729 GiB). At the 100 update-end observations, maximum MPS allocation is 5,408,765,184 bytes (5.037305 GiB), and maximum MPS driver allocation is 11,841,470,464 bytes (11.028229 GiB). These are observed step-end device values, not a continuous device peak claim. All observations remain in the complete steps log. The final two-row forward check has 292 native target labels and finite loss 0.124805450; it performs no additional optimizer update.

G2_BYT5_RUNNER_QUALIFIED
