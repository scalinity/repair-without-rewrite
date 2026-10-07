# Generation-2 ByT5 milestone independent reconstruction

FACT: Recorded 2026-10-07; reviewed qualified source `2c27cff28a31ae64220df9b06094a914e94dd0f3` and the unchanged ByT5 recipe. This review uses a separate arithmetic path; it is not an external frontier-model decision.

MEASURED RESULT: `benchmarks/g2_byt5_milestone_independent.py` independently enumerates completed batch endpoints from the frozen integer counts. It imports no G2 batching, model, trainer, scorer or accelerator helpers. The saved receipt is `experiments/manifests/generation_2/execution-independent-byt5-milestones.attempt01.json`, which binds the exact recipe and review-code hashes.

MEASURED RESULT: The finite stream has 141,130 presentations, 35,283 updates and a final two-row batch. Milestones zero and ten have exact optimizer boundaries. Milestone two lies between updates 7,056/7,057 at 28,224/28,228 presentations; milestone five lies between updates 17,641/17,642 at 70,564/70,568. A separate reconstruction through the qualified `training_batches` function agrees on those counts and crossings in `execution-preflight.attempt01.json`.

INFERENCE: Training accounting is coherent. The qualified manifest has not chosen which completed model state supplies the two intermediate scientific evaluations. The 100-update neural qualification and final-batch check do not independently establish that missing mapping. No tolerance, schedule, training data or optimizer treatment is changed by this arithmetic audit.

FACT: All seven scientific slots remain unconsumed. No scientific training, scientific evaluation, numerical replay, final seed, sealed inference or protocol freeze occurred. The review request records candidate choices and the interpretation affected; this review selects none.

FRONTIER_MODEL_REVIEW_REQUIRED
