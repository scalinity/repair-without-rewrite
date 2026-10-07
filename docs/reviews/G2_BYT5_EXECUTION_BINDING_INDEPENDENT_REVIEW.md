# Generation-2 ByT5 execution binding independent review

FACT: Recorded 2026-10-07; reviewed source `b1c565e341c1571fec15d4f918049c584246517b`. This is an independent arithmetic code path, not a new scientific-design decision. The published frontier decision alone authorizes the mapping.

MEASURED RESULT: `benchmarks/g2_execution_schedule_independent.py` checks the versioned execution binding using the retained `benchmarks/g2_byt5_milestone_independent.py` finite integer endpoint enumeration. It imports neither the observation producer nor the training iterator, model, trainer or scorer. `experiments/manifests/generation_2/execution-schedule-independent.attempt01.json` binds both independent code paths, the original recipe, decision and execution binding.

CALCULATION: The first completed states at or above 28,226 and 70,565 are respectively update 7,057 / 28,228 presentations and update 17,642 / 70,568 presentations. Their preceding states contain 28,224 and 70,564. Update 35,283 is exact at 141,130 and retains a final batch of two. Initialization is zero. All four labels and all per-state original-recipe/frontier identities reproduce exactly.

MEASURED RESULT: Full suites before and after the binding pass 465 and 477 tests respectively, zero failures/skips. The original training iterator and baseline test files are unchanged. Synthetic full-stream regression enumerates all positions, shuffled record membership and the two crossing batches without model execution.

INFERENCE: The observation arithmetic, metadata and training-stream invariants satisfy the authorized clarification. No trajectory-invariance model experiment is claimed; runtime saving/evaluation must preserve training state and RNG, and that execution remains unrun here. Seven scientific recipes remain unstarted and the campaign freeze is not yet published.

G2_BYT5_EXECUTION_BINDING_QUALIFIED
