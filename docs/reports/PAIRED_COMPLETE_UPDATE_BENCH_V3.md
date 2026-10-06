# Paired complete-update BENCH v3 — 2026-10-05

**ATTEMPT03 QUALIFIED: both full native BENCH runs, all four exact cold resumes and independent actual-consumption audits pass.** Qualification uses exact B100/C101, the revised lexical profile, frozen common mixed reader, real DEVELOPMENT tokenizer and peak LR 3e-4 on the actual canonical-exposure clock. No six-probe slot is consumed, no LR is selected and no final/sealed candidate is decoded.

## Native implementation and complete objective

Frozen implementation: `28298ad886aa321882aa0530a18421e7d4e3553e`. The common queue stops at the first whole presentation reaching **32,768 canonical anchors**. BF16 working tensors use FP32 master weights, moments, loss sums and gradient accumulation. B100 uses 16-example microbatches and divides valid target/EOS sums by the whole queue count. C101 uses four-example microbatches and full-queue action/start/end/vocabulary denominators, omitting zero-count components. There is no second loss division. Clipping, AdamW application and accumulator clearing each occur once per completed queue.

Fresh attempt03 uninterrupted controls each complete **22 updates / 9,825 presentations / 721,724 canonical exposures**. The first shared queue is **32,815 exposures / 444 examples**, with B100 **28** and C101 **111** microsteps. First losses are finite: B100 **9.851723745465279**, C101 **17.28481255285442**. These arm-specific objectives are not directly compared as model quality. Independent checking reproduces every native row, tensor/target/event label, legal pointer, encoder position, padding count, full denominator, canonical boundary and continuous LR endpoint; all 22 ordered B/C queues match. These controls qualify the repaired checkpoint; uninterrupted C101 trajectory exactly reproduces attempt02.

## Atomic checkpoint and cold qualification

Checkpoints preserve whole queued objective, microbatch partition/completed offset, FP32 pending gradients and moments, model/master state, RNG, reader deficits/cursors/reuse state and code/data/runtime identities. Hash/dtype/shape/finite-state validation and actual masked native forward readback precede atomic publication. Restore verifies the same identities and objective/clock consistency.

Historical attempt01 is retained as superseded qualification. Independent static review found that a rehashed committed-exposure change from 32,815 to 32,816, and an optimizer-step change from one to two at 32,815, lacked required clock rejection guards. The corrected save/load validates strict nonnegative integer counters, zero-step/zero-exposure consistency, `committed >= step*32768` for enforced queues, reader endpoint `committed+pending`, BENCH phase-charge sums and finite saved loss. Tiny test queues retain their explicit complete-target exception. This changes checkpoint rejection, not the approved mathematics.

B100 attempt02 boundary and mid-update cold processes each match **21 complete updates 2–22 exactly**; C101 boundary also matches all 21. C101 mid-update fails at update2. An isolated diagnostic reproduces exact saved/loaded pending arrays and loss, then reproduces the failure: original loss **14.96543151512742**, cold-mid loss **14.965431524440646**, with 410 differing array leaves. Sorted checkpoint JSON changes C component order from action/start/end/vocabulary to action/end/start/vocabulary; dictionary equality validates counts but does not restore reduction order. The repaired loader reconstructs the validated original-order denominator object. It also rejects nonzero empty-boundary accumulator counters/arrays/loss. No component weight, objective, clipping or optimizer formula changes.

All six native control/cold gates repeated as attempt03 under the new freeze and pass. Mid replay completes pending queue 2 then updates 3–22; boundary replay includes the next 20 plus one additional complete update. Exact state hashes, reader hashes, losses, LR, denominators and ordered IDs are required without tolerance relaxation. See [independent fairness audit](PAIRED_READER_FAIRNESS_AUDIT_V3.md) and [attempt02 disposition](../../experiments/manifests/lexical_reader_v2/native-qualification-attempt02-disposition.json).

## Full BENCH gate

Each arm must separately complete **five whole warmup updates**, **100 whole timed updates**, and an additional sustained whole-update segment lasting **at least 1,200 seconds**. The unchanged queue selector balances P0/P1/P2 canonical exposure in the pilot proportions while retaining complete frozen queues and persistent phase cursors. BENCH does not reset the LR at phase or segment boundaries; the future 305-update recipe ledger remains unchanged.

The full native pipeline records canonical charge/overshoot, examples/microsteps, actual consumption, loss denominators/decisions, source and decoder/event positions, padding, reader, forward/backward, synchronization, accumulation and optimizer timings. Timed/sustained mean/median/p95 and canonical/native/example throughput, MLX allocation, macOS RSS, system memory/swap, thermal/power indicators and throughput drift require completed runs before reporting a PASS. Forecast rate is the slower of full sustained throughput and the final sustained quarter.

Initial/final atomic save/readback and all **396 frozen DEVELOPMENT cases** are priced for each arm. Decode caps remain B100 256 tokens, C101 64 edits / 256 decoder positions. Capped/invalid/abstained cases stay in the timing population and private outputs; they do not become exclusions or a model-quality admission criterion.

Host: Apple M5 Pro, 48 GiB, 18 logical CPUs, macOS 27.2 arm64. Accelerator jobs run serially. Full BENCH measurements and actual paired BENCH fairness are complete. Source payloads, tensors, checkpoints, raw failures and evaluation outputs remain ignored private artifacts. Public summaries contain aggregate measurements and hash identities.

## Measured complete BENCH

Original immutable BENCH summaries retain `BENCH_00_COMPLETE_FAIRNESS_REVIEW_PENDING`, the status at measurement completion. Their independent receipts and closure now supply the final PASS; the measurement records are not rewritten. The qualification native implementation is `28298ad886aa321882aa0530a18421e7d4e3553e`.

| Measurement | B100 | C101 |
|---|---:|---:|
| Whole warmups | 5 | 5 |
| Timed complete updates | 100 | 100 |
| Additional sustained updates | 258 | 76 |
| Sustained wall seconds | 1,202.8245932499995 | 1,200.2798671250057 |
| All complete BENCH updates | 363 | 181 |
| All canonical exposure | 11,910,268 | 5,938,207 |
| All presentations | 160,109 | 79,827 |
| Timed anchors/second | 7,832.36927999746 | 2,071.25675984284 |
| Sustained anchors/second | 7,037.9413985265255 | 2,077.3055253957077 |
| Conservative anchors/second | 7,037.9413985265255 | 2,044.1932927973103 |
| Last/first sustained-quarter throughput | 1.0916629921002314 | 0.9931863184912737 |
| Recorded training peak MLX bytes | 4,093,362,692 | 3,365,844,548 |
| Recorded process peak RSS bytes | 5,148,753,920 | 5,131,649,024 |

Conservative B uses full sustained throughput (lower than its last quarter 7,858.141478); conservative C uses the last quarter (2,044.193293, below full sustained 2,077.305525). Native rate differences are computational, not model-quality evidence.

| Arm / segment | Update mean / median / p95 seconds | Native positions/sec | Examples/sec | Reader seconds | Forward/backward | Synchronization | Accumulation | Optimizer |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B100 / timed | 4.181509 / 4.155781 / 5.610714 | 7628.229 | 105.297 | 0.426085 | 377.021708 | 0.157913 | 15.086857 | 19.714211 |
| B100 / sustained | 4.654426 / 4.600620 / 6.191244 | 6853.994 | 94.629 | 1.078706 | 1085.510669 | 0.386248 | 38.577042 | 55.221951 |
| C101 / timed | 15.817666 / 15.940482 / 16.672572 | 1406.028 | 27.845 | 0.793213 | 1506.960366 | 0.506943 | 57.218353 | 9.237322 |
| C101 / sustained | 15.772166 / 15.856314 / 16.781270 | 1410.154 | 27.943 | 0.576258 | 1142.088017 | 0.421752 | 43.663812 | 7.013196 |

All-update charge ranges B 32,768–32,950, C 32,768–32,890; overshoot ranges 0–182 and 0–122. B examples/update range 361–457, microsteps 23–29; C361–457 and 91–115. All-update native totals: B source 6,308,325, target/EOS 5,290,765, source padding 5,571,422, decoder padding 2,784,558; C source 3,145,127, event positions 885,303, source padding 1,361,818, decoder padding 0. C objective decisions are action 205,670, start 125,843, end 125,843 and vocabulary 553,790. The [aggregate](../../experiments/manifests/lexical_reader_v2/native-bench-aggregates.attempt03.json) preserves complete per-segment distributions, component decisions, phase/channel/view charges and equality/repair counts.

Independent comparison matches all **181 common queues / 79,827 presentations / 5,938,207 exposures**. B's unmatched 182 queues / 80,282 presentations / 5,972,061 exposures are fully independently checked. B phase charges are P0 7,919,891 / P1 3,167,923 / P2 822,454; C 3,943,223 / 1,583,849 / 411,135. No omitted tail is presented as matched. Each arm and each warmup/timed/sustained segment passes both concentration checks. All-arm entry/separator fractions are B 20.107895% /20.210158%, C 20.225721% /20.173469%. Both native runs have finite losses and no recorded qualification failures.

## Memory and machine context

MLX peaks are maxima recorded during training updates; RSS is sampled process memory across the monitored span, not a guaranteed whole-job or whole-machine peak. B has 28 system snapshots: swap-used first/max/last **11,747.06 /15,044.19 /11,874.50 M**, reported free-memory range 26–86%. C has 46 snapshots: **11,714.44 /11,714.44 / 5,861.44 M**, free-memory range 68–86%. Swap was already in use before either run; no zero-swap claim is made. All recorded samples report AC power, no recorded thermal/performance warning and no CPU power status. These are sampled indicators, not proof of absent throttling. Raw snapshots are private and hash-bound in each summary.

## Exact resume and evaluation cost

All four current cold replays pass 21 complete updates 2–22. B boundary/mid cold-load seconds are 1.183204 /1.107982; C 1.621159 /1.683322. Independent checking verifies FP32 pending/master/model/moment state, source captures, reader hashes, loss, clock, denominators, RNG and immutable identities. Initial/final BENCH inventories also pass: B 525 arrays / 100,686,336 FP32 model parameters; C 549 / 101,081,859, finite exact shapes/dtypes and zero boundary accumulators. [Closure receipt](../../experiments/manifests/lexical_reader_v2/independent-bench-closure.attempt03.json).

| Arm / panel | Cases | Decode seconds | Scorer seconds | Complete panel seconds | Completion statuses |
|---|---:|---:|---:|---:|---|
| B100 / initial | 396 | 427.168516 | 41.260783 | 475.107230 | {"capped": 388, "invalid_byte_decoding": 8} |
| B100 / final | 396 | 75.672122 | 1.359340 | 77.188892 | {"completed": 396} |
| C101 / initial | 396 | 241.261636 | 0.769462 | 242.153608 | {"abstained": 78, "completed": 90, "invalid_or_capped": 228} |
| C101 / final | 396 | 13.722900 | 1.283269 | 15.140248 | {"completed": 396} |

All 396 cases remain in each panel and forecast, including failed/capped/abstained decodes. Completion is not correctness. Startup/save/load and the per-case envelope are priced in [cost v2](BC_10M_PROBE_COST_PROJECTION_V2.md). Final integrated suite: **372 passed in 33.25s**, TF32 disabled. Zero six-probe slots consumed.

PAIRED_COMPLETE_UPDATE_BENCH_QUALIFIED
