# Independent native calibration review

Reviewer: MODEL-0/shared-core owner reviewing the independently written `benchmarks/native_calibration.py`. This is independent review of the runner and evidence accounting, not independent review of the shared training implementation authored by the reviewer. No model was loaded and no accelerator work ran for this review.

## Snapshot and disposition

At **2026-10-05 05:39:39 UTC**, `experiments/native-calibration-attempt01/` had **5 warmup, 100 timed and 2,942 thermal complete-update records**. `summary.json` was absent and the 20-minute thermal/resume phases were still running. Thermal completion, final restart comparisons and whole-run acceptance were **PENDING**, not PASS. The most recent observed row was optimizer step 3,047, with 3,120,128 processed fixture tokens, 1,020 valid targets and four microbatches for that update. Loss rounded to zero on the repeatedly trained fixed random blocks; this is no language-learning result.

The inspected runner matches commit `9dbef2b8673721a1face6a7c7a87a520fdfb140d` exactly, SHA-256 `379fba6df9690c8578e5cbce6526b5365b9dfbc65a2b147286a8953b36e69386`. The recorded dirty working tree includes other agents' unrelated work; it is preserved in provenance rather than represented as a clean checkout. Config, token manifest, MODEL-0 gate evidence, `uv.lock`, and the gate-qualified `core.py`/`training.py` hashes matched their recorded identities at the review snapshot. V0–V4 were all PASS in that exact gate record.

**Overall disposition: scoped geometry measurement with incomplete full BENCH-00 qualification.** No calendar projection is justified by this selected geometry. A subsequent process-restart audit will be a separately named supplement, not a rewrite of the original run.

## Complete-update and arithmetic checks

The runner creates the canonical MODEL-1 decoder geometry: vocabulary 16,384, width 768, 14 layers, 12 query/4 KV heads, FFN width 2,048, configured context 1,024 and exact inventory total **100,685,568**. Each measured update performs four `Trainer.accumulate` calls and one `Trainer.update` with global clipping and AdamW. The trainer evaluates each loss/gradient and FP32 accumulation buffer during microsteps, and evaluates the updated model, both moment trees and the cleared accumulator before returning. The runner repeats state evaluation and synchronizes before ending its update timer. Obsolete gradients are not appended to a growing history; logs contain scalar records.

All four inputs are materialized when NumPy saves the manifest before timing. Five completed warmups are excluded from the 100 fixed timed updates. Model/optimizer initialization is separately timed. The backend is the explicit reference attention path; compilation is disabled. The BF16 working policy retains FP32 master leaves, moments and accumulation, with FP32 score/softmax/loss reductions. The source code applies a full causal mask and the normal one-position target shift. No padding is present, so all 255 target decisions per microbatch are valid. The fixed dense case does not qualify padding, variable lengths, encoder/cross-attention or native fused backward performance.

**Geometry detail:** `sequence_length=256` describes each serialized token block. `causal_loss` calls the model on its first **255 positions**, predicting the following 255 labels. Thus each full update processes 1,024 accounted block tokens, executes four length-255 model forwards/backwards, and normalizes by **1,020 valid labels**. These distinct quantities should remain explicit in the report.

## Finding BENCH-R01 — full BENCH-00 workload remains unqualified

Canonical Section 19.7 requires 32,768 nominal processed/canonical tokens per update, the selected length/batch grid, a representative actual reader/mask/loss mixture, correctly padded small batches, a real dataset-path segment, and per-task native length/event distributions. This run uses **1,024** nominal fixture tokens per update and reuses four fixed random blocks. Its configuration explicitly labels this input kind, which is correct, but a general BENCH-00 PASS label or scaling the measured token rate into a full campaign would exceed the evidence. The current run can establish the declared small dense decoder geometry's complete-update timing and sustained behavior only.

The full thermal requirements also include whole-run and last-five-minute rates, per-minute rates, p50/p95 and first-five versus last-five degradation. Raw per-update timings can support compute-time window summaries; the runner does not save absolute monotonic timestamps for exact wall-time binning. Initial/final `pmset` warnings are not continuous temperature, fan or power observations. Active/cache MLX memory, RSS, pressure, swap growth and measured GPU utilization are not collected by the runner. Its global peak field includes later checkpoint/reload and simultaneous control/restored model residency, so it must not be presented as training-only steady-state memory. These fields remain missing or unavailable rather than inferred from one peak.

Required disposition: preserve the random-geometry labels and mark full BENCH-00/data/resource/campaign qualification incomplete. Derive available window statistics transparently from recorded update elapsed times, with their boundary convention identified.

## Finding BENCH-R02 — original resume acceptance is narrower than the contract

The checkpoint implementation writes FP32 master weights, both moments, accumulation, counters, schedule, identities, data order/cursor and explicit RNG states, checks readback/forward/hash integrity, then publishes a new completed directory. The runner correctly saves at an update boundary and later performs 20 control and 20 restored updates on the same fixed batch list.

However, the original runner restores a second Trainer in the **same process**, whereas Section 19.7 requests restarting the disposable benchmark process. Its acceptance compares all parameter leaves and **first moments only**. It does not compare second moments, the complete loss/LR trajectory, data cursor/order, scheduler position, RNG or accumulator/counters after continuation. Those 40 continuation updates are also absent from `updates.jsonl`; they are additional measured work outside its recorded warmup/timed/thermal exposure rows. A zero endpoint parameter/first-moment difference is valuable scoped evidence, but does not independently establish the whole registered resume-state contract.

Root has assigned a separate 20-update fresh-process audit after the thermal run. It must preserve the original run and record its own checkpoint/manifest, each continuation row, complete parameter/moment/state digests and counter comparisons. Its completion remains PENDING here.

## Provenance and evidence limits

`provenance.json` captures commit/dirty status, input/config/gate/lock hashes, seed 42, initial weights, power/thermal warnings and an environment-report reference. The inspected consumed core/training code hashes match the gate evidence. The reference to `ENVIRONMENT_INITIAL.json` identifies an earlier environment snapshot; the runtime lock hash in the benchmark provenance is the run's actual pinned-lock identity and should be cited explicitly if that earlier snapshot has a different lock hash. A saved runtime dtype inventory and machine/software manifests at the actual run boundary would strengthen evidence; the recipe states the policy but is not a runtime dtype measurement.

Fixed random tokens are in IDs 384–16,383 with no reserved control literals. There is no public source shard, tokenizer/reader, augmentations, B/C event density, pretrained comparator, ASR or TTS in this workload. The 150M schedule is a development timing scaffold at seed 42, not a final seed or a final training trajectory. The thermal trajectory and additional resume work must be charged to the development ledger. Checkpoint disk bytes/write/load memory remain to be verified from completed artifacts.

This review found no concrete omission of backward, loss, accumulation, clipping or AdamW from the timed operation. The material open issues concern the scope of the selected workload, missing resource/time evidence and the breadth of the original resume assertion. Source inspection does not prove final thermal stability; that remains dependent on the completed raw run.
