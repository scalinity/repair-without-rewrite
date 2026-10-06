# Six B100/C101 10M development-probe cost projection v2 — 2026-10-05

**COMPLETE MEASURED PROJECTION: six future recipes total 11.442153 hours serialized with one 25% reserve.** The projection prices six future, unstarted seed-42 DEVELOPMENT recipes on the measured Apple M5 Pro, 48 GiB, macOS 27.2 host. It does not price a final-paper campaign or establish one-month feasibility. No probe slot is consumed.

## Accounting method

Each recipe uses the shared actual whole-update endpoint **10,007,223 canonical exposures / 305 complete updates**, rather than rounding down to nominal 10M. The 200,000-exposure LR warmup is already part of this endpoint. The five BENCH warmup updates are not added again as extra scientific training.

Training time is actual exposure divided by the **slower of full sustained throughput and final sustained-quarter throughput**. That rate includes native reader/packing/capture, forward/backward, synchronization, FP32 accumulation, optimizer and serialized update logging. Initial-control timing through the first full endpoint at or above 200,000 contributes only its positive excess above sustained-rate pricing; diagnostic hashing makes this conservative.

There are **13 deduplicated save endpoints** and **six DEVELOPMENT evaluation endpoints** per recipe. Save latency uses the maximum measured initial/final BENCH or boundary/mid reference save/readback. Load latency uses the maximum of the two cold loads; one initial load is charged conservatively even though future seed-42 recipes start fresh. Each evaluation retains all **396 cases**, using the sum of per-case maximum initial/final decode times, independently the sum of per-case maximum scorer times, and the maximum observed panel overhead. Capped/invalid/abstained cases remain counted. These timing envelopes do not select a learning rate or claim model quality.

One interruption per recipe is assumed: one save, one load, one whole-update replay at the measured sustained rate, and 30 seconds for restart. Shared one-time profile estimation, full accepted-pool generation, CPU ledger construction and frozen-panel construction are charged once across all six recipes, even when frozen private artifacts already exist. Native reader costs already inside throughput are not charged a second time.

Let `T_B` and `T_C` include all per-recipe training, startup, checkpoint, evaluation/scorer and recovery components before reserve; let `S` be measured shared construction. The serialized total is **`1.25 * (3*T_B + 3*T_C + S)`**. Single-arm recipes also report before-reserve and 25%-reserve amounts, but those reserved single amounts are not reserved again in the six-run total.

## Evidence categories and limitations

**MEASURED:** complete native BENCH and conservative sustained rates; all initial/final 396-case decode/scorer timings; atomic save/readback, both cold loads, startup and initial control timings; profile 25.673543 seconds, accepted-pool generation 448.028534 seconds, full CPU ledger construction 70.270997 seconds and exact frozen-panel reconstruction 2.999699 seconds. Both completed BENCH runs and all cold-resume gates are hash-bound in the [calculation](../../experiments/manifests/lexical_reader_v2/six-probe-cost-projection.attempt03.json).

**CALCULATED:** actual endpoint divided by measured rate; 13 saves and six evaluation envelopes; per-arm component totals; three recipes per arm plus shared construction and one exact 25% reserve.

**ASSUMED:** sustained and per-case decode timing envelopes transfer to all three LRs; one interruption per recipe and 30-second restart; conservative initial load; shared construction repeated once from scratch. No LR/quality conclusion follows from these assumptions.

**UNPRICED:** future intermediate-checkpoint decode variation outside observed envelopes; additional interruptions beyond the stated allowance; final 150M runs, other baselines, sealed evaluation and paper production. These exclusions prevent a final-paper feasibility claim.

The calculator rejects missing 5/100/ 1,200-second BENCH gates, failed qualification, nonpositive/nonfinite rate, incomplete 21-update cold replay, started recipes, duplicate endpoints and missing/duplicate 396-case panel IDs. Seven targeted accounting tests pass; those tests use synthetic accounting inputs and do not constitute native timing evidence. The calculator runs only after both BENCH attempts are complete, without importing a model or executing a neural call.

The scientific recipes remain configured and unstarted. [V4](BC_10M_PROBE_ADMISSION_DECISION_V4.md) admits them scientifically; execution belongs to a separately authorized new session.

## Measured component calculation

| Seconds per recipe before reserve | B100 | C101 |
|---|---:|---:|
| evaluation decode | 2563.011099 | 1465.817987 |
| evaluation panel overhead | 40.067587 | 0.804473 |
| evaluation scorer | 247.623151 | 7.727315 |
| initial load | 1.183204 | 1.683322 |
| measured initial control excess | 9.621260 | 4.403234 |
| one interruption recovery allowance | 38.022540 | 49.476637 |
| reader data model startup | 2.532515 | 2.499471 |
| routine atomic saves | 28.164769 | 22.168969 |
| training after warmup at sustained rate | 1393.478923 | 4797.600616 |
| training warmup at sustained rate | 28.417401 | 97.838106 |

| Future work | Before reserve | With 25% reserve |
|---|---:|---:|
| One B100 recipe | 1.208923h | 1.511154h |
| One C101 recipe | 1.791672h | 2.239590h |
| All six, shared construction once | 9.153722h | 11.442153h |

Shared construction is 546.972772 seconds. Reserved total is 41191.750631 seconds (about 11h26m32s). Per-panel conservative decode/scorer envelopes are B 427.168516 / 41.270525 seconds and C 244.302998 / 1.287886. Per-save maxima are B 2.166521, C 1.705305; cold-load maxima B1.183204, C 1.683322. All 13 saves and six 396-case evaluations are counted. Zero recipe slots consumed; `paper_protocol_v2` remains unfrozen.

SIX_DEVELOPMENT_PROBE_COST_PROJECTION_COMPLETE
