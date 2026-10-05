# Paired complete-update BENCH qualification — 2026-10-05

**NOT RUN / NOT QUALIFIED.** The [mixed-reader contract](PAIRED_MIXED_READER_QUALIFICATION.md) requires frontier review before its scientific presentation process can be constructed. No new 32,768-anchor update attempt, smaller candidate update, warmup, timed training, thermal segment or checkpoint rehearsal occurred. This is a contract stop; there is no measured claim that 32k fails memory, is too slow, or needs a different architecture.

## Prospectively recovered regime

Canonical §19.2 (line 1999) requires accumulating variable-length presentations until approximately 32k canonical anchors, finishing the last whole example and logging the true total. Registry lines 374–375 and 520–522 specify the initial 32,768 target subject to BENCH, actual masks/loss/reader, five complete warmups,100 complete timed updates, ≥20-minutes thermal and 20-update resume. Actual microbatch sizes/partition/buckets can be qualified faithfully. A shared queued presentation range must be fixed first; B/C can split that same range differently, including a final shorter microbatch. An arm cannot consume extra examples merely to fill its own last microbatch.

The approved models remain B100 = 100,686,336 and C101 = 101,081,859 parameters. Registered working BF16, master/moments/accumulation FP32; AdamW β(.9,.95), ε 1e-8, matrix decay .1, norm decay 0, tied matrix once and global clip 1. B uses complete-update target/EOS valid-token normalization. C uses precomputed whole-update action/start/end/vocabulary denominators, zero-component omission, one FP32 accumulator and clip/update once without another division. Source/causal/cross-attention/PAD/pointer/byte-boundary masks remain required.

Checkpoint publication defaults to optimizer boundaries (canonical 2056/2083); cold processes must compare 20 continued updates against uninterrupted control. Canonical 2262/3466 permits mid-accumulation only with complete accumulators and denominators. The continuation explicitly requires testing a permitted mid-update case. Because the canonical contract permits full-state mid-accumulation saves, boundary-default wording alone does not authorize substituting a prohibition proof. The future BENCH must qualify that partial-state case unless the owner explicitly supplies a contract prohibition; no such prohibition or partial-state qualification exists here. The existing causal helper's partial-state capability does not prove a B/C mixed-reader resume contract. Atomic completion, finite arrays/moments, reader identity/counters, RNG, LR, phase and next presentation must be validated in the chosen wrapper.

The 20-minute representative thermal segment is separate from the fixed 5+100 screen. No previous zero-LR short-fixture exception is promoted to this gate. The new BENCH must prospectively bind its LR/clock to the approved training path. Under the user’s conditional requirement, LR0 cannot substitute if that contract requires a realistic nonzero-LR path; no new unconditional LR gate or benchmark LR is selected here. Initial state, exact HEAD/dirty diff/config/code/reader/tokenizer/data/runtime/seed hashes and timing boundaries must be captured before each expensive attempt.

## Required measurements and current disposition

| Item | B100 | C101 |
|---|---|---|
| Nominal canonical target |32,768, untested|32,768, untested|
| Chosen executable regime / microbatch / accumulation |Not chosen|Not chosen|
| Five complete warmups |Not run|Not run|
|100 complete timed updates |Not run|Not run|
|≥20-minute complete-update thermal segment |Not run|Not run|
| New update mean/median/p 95, anchors/s, native positions/s/examples/s |Unmeasured|Unmeasured|
| Microsteps/examples/update, exact range/overshoot, padding |Unmeasured|Unmeasured|
| Peak MLX, RSS, pressure/swap, thermal/power indicators |Unmeasured|Unmeasured|
| Reader preparation/synchronization/materialization costs |Unmeasured|Unmeasured|
| Save/load, cold 20-update control, next IDs/phase/channel/counters/state |Not run|Not run|
| Partial-accumulation equivalence or rejection proof |Not qualified|Not qualified|

The [independent resume/BENCH review](../reviews/PAIRED_RESUME_BENCH_INDEPENDENT_REVIEW.md) inspects actual source/checkpoint helpers and old raw ledgers. Reusable mechanics and exact prior arithmetic do not qualify the new population/regime. No architecture, loss or update-target redesign was performed.

## Historical measurements retained with their actual scope

The existing [native calibration](BENCH00_NATIVE_CALIBRATION.md) used 12 cycling natural TRAIN fixtures, four requests/update (184–238 old diagnostic anchors),300 fits at 3e-4 and a zero-LR thermal path. Prior B/C sustained wall rates were 1,711.563/849.602 diagnostic anchors/s; medians .122868/.240982 seconds/update; MLX peaks 2,954,780,473/3,352,386,426 bytes. Those memory/time values belong only to that historical workload. Its held-out CAL outputs do not establish useful repair. Prior causal cold-resume 20-step equality used fixed random blocks, not a mixed reader. No old evidence is overwritten.

## 10M cost projection

**One 10M B recipe: unpriced. One 10M C recipe: unpriced. All six serialized recipes including 25% reserve: unpriced.** A numeric forecast using the previous four-request rate would change the workload while claiming to price the registered experiment. No six-slot training was executed.

Once the reader and regime qualify, for arm `a` calculate:

`T_a = U_a * mean_sustained_complete_update_wall_seconds_a + reader_cost_excluded_from_update_wall_a + save_and_cold_load_cost_a + sum_registered_DEV_panels(decode_wall_a + scorer_wall_a) + other_declared_excluded_costs_a`.

`U_a` comes from actual common completed-update anchor ranges through the first update reaching 10M, including overshoot. Under a nominal exact 32,768 charge only, arithmetic gives 306 updates; actual variable-length complete ranges may differ. This 306 is an illustration, not a scheduled run count. Use a conservative representative sustained rate and include measurable load/warm/initialization once under a declared policy. If update wall already includes reader work, do not add it again.

`T_six_with_reserve = 1.25 * sum(T_B,1e-4 + T_B,3e-4 + T_B,6e-4 + T_C,1e-4 + T_C,3e-4 + T_C,6e-4)` on the single M5 Pro with serialized neural jobs.

| Cost category | Evidence class | Currently priceable for chosen 10M recipe? |
|---|---|---|
| Qualified mixed complete-update useful compute |Required new measurement|No|
| Reader/generation preparation and update I/O |Required new measurement; scope must prevent double count|No|
| Checkpoint verification/write/cold load |Required new B/C measurement; previous causal figures do not substitute|No|
| Registered DEV decode panel/cadence |Schedule/panel not yet bound; prior tiny call times are historical|No|
| Scorer |Prior nonidentity CPU timings measured on fixed 48/72 record runs; new panel cardinality/length distribution unknown|No|
|25% reserve |Prospectively specified arithmetic multiplier 1.25|Only after base costs exist|
| Neural serialization |Required scheduling assumption; no parallel rate multiplication|Yes as a constraint, no numeric duration|

No total duration, one-month feasibility or final 150M projection is inferred from this ledger. No cloud/API spending occurred. Frontier review must first bind the missing reader and pilot treatment; faithful regime qualification follows afterward.
