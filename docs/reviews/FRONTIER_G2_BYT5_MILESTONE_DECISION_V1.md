# Frontier G2 ByT5 Milestone Decision v1

Date: 2026-10-07  
Reviewed execution checkpoint: `1300a7c50f2b97eed477d2b2c464fcd80e4fbba3`  
Qualified source: `2c27cff28a31ae64220df9b06094a914e94dd0f3`  
Execution branch: `codex/g2-execution`

## A. Decision

**AUTHORIZE_FIRST_COMPLETED_UPDATE_AT_OR_AFTER_MILESTONE**

Bind each nominal milestone to the earliest completed optimizer update whose cumulative training presentations reach or exceed its nominal presentation count.

Update numbers denote completed optimizer updates; initialization is update zero. Count presentations incorporated into those completed updates, not prefetched or partially accumulated records.

FACT: This read-only review verified the clean execution checkpoint and all seven unchanged, unstarted recipe manifests. No files were changed, no model was run, and no test suite was rerun.

## B. Contract interpretation

INFERENCE: “After N complete passes” requires a trained state incorporating at least `N × 14,113` presentations. The preceding updates incorporate fewer presentations and therefore cannot truthfully represent a state after those complete passes.

The wording alone does not specify the earliest among all possible later states. However, **between the two proposed mappings, only Option A satisfies “after.”** Choosing the earliest qualifying completed update supplies the smallest deterministic clarification: it introduces neither arbitrary additional delay nor a checkpoint-selection choice.

Section Q of `docs/reviews/FRONTIER_POST_10M_SCIENTIFIC_DECISION_V1.md` binds ten passes, 35,283 updates, the final two-record batch, and endpoint-only adequacy. The frozen recipe:

`experiments/manifests/generation_2/recipe-G2-ByT5-D1-10pass-seed42-lr3e-4.attempt01.json`

also binds continuous batching without pass-boundary flushing. Its SHA-256 is:

`cd74653ce9af7a155560884e1b34d1e936392ed9fce61558345b1d8ac442b5df`

The crossings are supported by the review request, `docs/reviews/G2_BYT5_MILESTONE_INDEPENDENT_REVIEW.md`, and its hash-bound arithmetic receipt. The runner qualification and admission reports establish the existing training extent; they do not supply a different intermediate mapping.

This decision follows the contract’s semantics and completed-state constraint. It does not depend on convenience, cost, or expected model quality. No scientific recipe outcome informs it.

## C. Exact 2-pass binding

CALCULATION:

| Field | Binding |
|---|---:|
| Nominal presentations | 28,226 |
| Completed optimizer update | 7,057 |
| Actual presentations | 28,228 |
| Offset: actual minus nominal | +2 |

Exact reporting label:

**“2-pass nominal milestone — first completed update at/after boundary”**

## D. Exact 5-pass binding

CALCULATION:

| Field | Binding |
|---|---:|
| Nominal presentations | 70,565 |
| Completed optimizer update | 17,642 |
| Actual presentations | 70,568 |
| Offset: actual minus nominal | +3 |

Exact reporting label:

**“5-pass nominal milestone — first completed update at/after boundary”**

## E. Exact 10-pass binding

CALCULATION:

| Field | Binding |
|---|---:|
| Completed optimizer update | 35,283 |
| Nominal presentations | 141,130 |
| Actual presentations | 141,130 |
| Offset | 0 |

Exact reporting label:

**“10-pass exact endpoint”**

The last optimizer update retains its qualified two-record batch. Initialization remains update zero with zero nominal and actual presentations.

## F. Training-trajectory effect

The authorized mapping changes none of the following:

| Training property | Effect |
|---|---|
| Presentation order | Unchanged |
| Number and sequence of optimizer updates | Unchanged |
| Batch membership, including crossing batches | Unchanged |
| Training gradients | Unchanged |
| Optimizer state along the training trajectory | Unchanged |
| Final 10-pass model state | Unchanged |

These are implementation invariants. Saving and evaluation must preserve training state and RNG progression, and training must resume in its required mode.

No batch may be split or flushed at an intermediate pass boundary. No optimizer reset or partially accumulated state may substitute for a completed checkpoint.

INFERENCE: The invariance follows from preserving every training operation and adding only non-interfering observation at the specified completed states. This review does not claim to have executed a new trajectory comparison.

## G. Scientific interpretation

The two intermediate evaluations remain **descriptive adaptation-trajectory observations**.

ByT5 adequacy remains assessed exclusively at the exact ten-pass endpoint. Neither intermediate result may select a recipe, LR, model, training duration, or final checkpoint. No best-checkpoint selection is introduced.

The mapping determines the intermediate evaluated model states, their exact presentation counts, their labels, and their measured evaluation charges. It does not change the adequacy gate or authorize any broader scientific change.

## H. Reporting requirements

- **Manifests:** For every scheduled save/evaluation, record `nominal_passes`, `nominal_presentations`, `optimizer_update`, `actual_presentations`, `presentation_offset` defined as actual minus nominal, and the exact reporting label. Bind the execution schedule to the original qualified recipe and this decision. Preserve the original qualification manifest.
- **Scientific report:** Publish nominal and actual presentation counts side by side, with completed update numbers and signed offsets. Use the exact labels above.
- **Plots/tables:** Show both counts in the plotted annotation, accompanying table, or figure caption. For a quantitative training-progress axis, use actual presentations; if expressed in passes, use `actual_presentations / 14,113`. Do not label the intermediate states as exactly 2.000 or 5.000 passes.
- **Cost accounting:** Associate each save/evaluation charge with its actual update and presentation count while retaining its nominal milestone. Charge measured time and retained failures under the existing policy. Keep forecasts distinguished from measurements.

There remain four scheduled evaluation states: initialization, the two bound intermediate states, and the exact endpoint. The +2 and +3 offsets are already within the fixed 141,130-presentation training stream; they are not additional training presentations or updates beyond the endpoint.

## I. Prospective amendment

For Generation-2 ByT5, a nominal pass milestone is observed at the first completed optimizer update whose cumulative incorporated training presentations reach or exceed the nominal count. Preserve continuous batch-four training across pass boundaries and the final two-record batch. Bind the 2-pass milestone to update 7,057 at 28,228 actual presentations versus 28,226 nominal (+2); bind the 5-pass milestone to update 17,642 at 70,568 actual presentations versus 70,565 nominal (+3). Retain initialization at update zero and the exact 10-pass endpoint at update 35,283 and 141,130 presentations. Publish nominal and actual counts, signed offsets, and the labels specified in Frontier G2 ByT5 Milestone Decision v1. Intermediate results are descriptive only; endpoint-only adequacy and all qualified training operations remain unchanged.

## J. Sol continuation authorization

Resume the existing `codex/g2-execution` session for `scalinity/repair-without-rewrite` under the existing seven-recipe execution authorization, with this narrow clarification:

1. **Record this decision verbatim** as `docs/reviews/FRONTIER_G2_BYT5_MILESTONE_DECISION_V1.md`, preserving its date, reviewed checkpoint, qualified source, and disposition.
2. **Commit and publish that decision alone**, after the required publication-safety checks, before affected implementation or campaign freeze. Preserve existing history.
3. **Append Section I prospectively** to `docs/reviews/PROSPECTIVE_AMENDMENTS.md`, then mechanically bind the intermediate endpoints to updates 7,057 and 17,642. Preserve the original qualified recipe; record the additional binding in versioned execution artifacts.
4. **Update tests, execution manifests, and report labels prospectively.** Verify that each selected update is the first qualifying completed state; initialization, final accounting, batch membership, and the training sequence remain unchanged. Preserve an independent arithmetic check. Realign `docs/LOG.md` and `ORCHESTRATION.html` with the resulting record.
5. **Reproduce the existing 465-test baseline before implementation** and run the complete suite afterward: at least 465 passed, zero skipped, zero failed, with no removed baseline coverage or regressions. Save both receipts. Report unrun checks as unverified.
6. **Reverify execution prerequisites**, including the bound external artifact root, storage policy and forecast, and all seven unstarted slots. Freeze and publish the Generation-2 execution campaign with the exact endpoint bindings, labels, code/configuration identities, and existing scientific constraints.
7. **Then execute the seven recipes serially in the already authorized order:**
   1. `G2-B100-D0-U8-seed42-lr3e-4`
   2. `G2-C101-D0-U8-seed42-lr3e-4`
   3. `G2-B100-D1-U1-seed42-lr3e-4`
   4. `G2-C101-D1-U1-seed42-lr3e-4`
   5. `G2-B100-D1-U8-seed42-lr3e-4`
   6. `G2-C101-D1-U8-seed42-lr3e-4`
   7. `G2-ByT5-D1-10pass-seed42-lr3e-4`
8. **Make no other scientific-design change.** Preserve B/C design, D0/D1, U1/U8, populations, ByT5 model, batch size, loss, LR, optimizer, presentation order, pass count, final endpoint, scorer, eligibility, recipe order, and storage policy. Existing stop conditions and escalation requirements remain binding. Final training, sealed inference, and protocol freeze remain unauthorized.

This frontier review ends with the decision. Implementation and scientific execution belong to the subsequent Sol continuation.

AUTHORIZE_FIRST_COMPLETED_UPDATE_AT_OR_AFTER_MILESTONE
