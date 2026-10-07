# Generation-2 ByT5 intermediate milestone review request v1

FACT: Recorded 2026-10-07. Reviewed qualified source: `2c27cff28a31ae64220df9b06094a914e94dd0f3`. Execution branch: `codex/g2-execution`, created from that exact source. This is a review request, not a returned frontier decision. No schedule choice is adopted and no scientific recipe slot is consumed.

## 1. Measured problem

MEASURED RESULT: The qualified continuous batch-four ByT5 stream has no completed optimizer-update boundary at exactly two or five complete passes. The frozen recipe binds 14,113 rows per pass, 141,130 presentations, 35,283 updates, a final batch of two, no pass-boundary flush, and save/evaluation milestones `[0, 2, 5, 10]`. It does not map the two intermediate milestones to actual updates.

| Pass milestone | Exact presentation count | Last completed update at or before milestone | Presentations at that update | First completed update at or after milestone | Presentations at that update |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 | 0 |
| 2 | 28,226 | 7,056 | 28,224 | 7,057 | 28,228 |
| 5 | 70,565 | 17,641 | 70,564 | 17,642 | 70,568 |
| 10 | 141,130 | 35,283 | 141,130 | 35,283 | 141,130 |

CALCULATION: The two-pass boundary is inside update 7,057, whose zero-based pass indices are `[1, 1, 2, 2]`. The five-pass boundary is inside update 17,642, with pass indices `[4, 5, 5, 5]`. These counts concern training presentations; no student result has been observed in this execution session.

## 2. Evidence and qualification limits

FACT: `docs/reviews/FRONTIER_POST_10M_SCIENTIFIC_DECISION_V1.md`, section Q, prescribes initialization and 2/5/10-pass saves/evaluations. `experiments/manifests/generation_2/recipe-G2-ByT5-D1-10pass-seed42-lr3e-4.attempt01.json` binds that schedule and continuous batching without a pass-boundary flush. `src/data/g2_byt5.py` yields batches across pass boundaries. `tests/data/test_g2_byt5.py` explicitly checks such a crossing.

MEASURED RESULT: `experiments/manifests/generation_2/execution-preflight.attempt01.json` reconstructs the crossings using the qualified batch generator and hash-verified D1 pairs. `experiments/manifests/generation_2/execution-independent-byt5-milestones.attempt01.json` independently enumerates the finite integer batch endpoints without importing that generator, any model, or any trainer. The independent path is `benchmarks/g2_byt5_milestone_independent.py`; its review is `docs/reviews/G2_BYT5_MILESTONE_INDEPENDENT_REVIEW.md`.

FACT: The qualified ByT5 neural trajectory executes exactly 100 updates and evaluates initialization/update100. Its independent review verifies full ten-pass batch accounting and the final short batch. Those checks establish the existing training plan, but they do not bind or exercise the 2/5-pass scientific save/evaluation mapping. No existing qualification receipt is being relabelled as a failed neural trajectory.

MEASURED RESULT: The current baseline reproduces 465 collected and passed, zero skipped or failed. All seven immutable recipe hashes and unstarted states reproduce; D0/D1/panel hashes and live external storage pass. The original forecast remains 91.179828399557 serialized hours, and its qualified high-water free-space calculation remains 269.676451031 GiB. These prerequisite passes do not settle the intermediate schedule.

## 3. Smallest candidate choices for the frontier decision

PROPOSED NEXT ACTION: Bind one explicit intermediate mapping prospectively, before publishing the execution campaign freeze or consuming recipe 1:

1. Use the first completed optimizer update reaching each milestone: updates 7,057 and 17,642, with presentation counts 28,228 and 70,568. Report nominal passes and actual counts/overshoot separately. Preserve all training batches, 35,283 updates, the final short batch, and endpoint-only adequacy.
2. Use the preceding completed optimizer updates: 7,056 and 17,641, at 28,224 and 70,564 presentations. This preserves training but needs an explicit revision of the wording “after 2/5 complete passes,” since those model states precede the nominal counts.

FACT: Flushing a short optimizer batch at an exact pass milestone is outside the frozen contract. It changes actual update geometry and later batch membership. It is not a mechanical alternative to either mapping above. Evaluating or saving an interrupted partial batch also requires a separately specified model/gradient/cursor state; that state is not prospectively defined for these ByT5 milestones.

## 4. Controls and interpretation at risk

INFERENCE: Either completed-update mapping can preserve the scientific training treatment and exact final ten-pass state. The choice changes which model state supplies two descriptive intermediate evaluations, how their pass labels are interpreted, and their measured decode/resource charges. The final ten-pass adequacy gate is not inherently changed by either mapping. Exact pass-boundary optimizer flushing would additionally confound optimizer granularity, batch denominators and subsequent training trajectory.

FACT: The seven-recipe execution freeze must bind save/evaluation endpoints before recipe 1. The current request explicitly escalates evaluation-rule changes and requires the owner to switch the session to Astra and authorize a material scientific choice. No such choice is made here. B/C, ByT5 training, data, losses, optimizer, initialization, scoring, caps and viability remain unchanged.

PROPOSED NEXT ACTION: In Astra, settle the two mappings and their labels explicitly, or establish from the existing contract why a unique mapping is already required. Record any returned frontier decision verbatim as a separately dated/versioned decision and commit it alone before affected implementation. Reverify the exact source, storage, unstarted states and baseline, then finish the execution freeze and run the seven recipes in the authorized order. No final training is authorized.

FRONTIER_MODEL_REVIEW_REQUIRED
