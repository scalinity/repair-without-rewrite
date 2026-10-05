# Bounded natural ByT5 development adaptation

**Valid native completion was established; useful lexical restoration was not.** Two prospectively bounded recipes used the exact official `google/byt5-small@68377bdc18a2ffec8a0533fef03b1c513a4dd49d` weights, 299,637,760 FP32 parameters on MPS, eager attention and explicitly disabled CPU fallback. The earlier ten-update invalid probe remains unchanged. Its native byte255 prefix, missing EOS and invalid UTF-8 are independently reproduced in [the review](../reviews/BYT5_ADAPTATION_INDEPENDENT_REVIEW.md).

## Data and recipes

Training uses all 1,024 admitted natural TRAIN hypotheses from 48 components, with unchanged LS-PC `text_raw` references. They contain 22,745 reference words, 521 ASR errors, 334 source-error rows and 690 lexically correct rows. Neither gold references nor error masks enter the encoder. Evaluation keeps the original twelve HPO hypotheses and twelve prospectively hash-selected calibration requests: 24 distinct requests, 17 source components, 416 reference words and 20 source errors. Fifteen requests are lexically source-correct. Every train/panel source family is disjoint. Calibration evaluation consumes these twelve IDs for development; it never fits them. The [consumption overlay](../../experiments/manifests/development_calibration_consumption.attempt01.json) also records subsequent native-decode development use, preserving original role metadata and untouched remainder.

Exactly two recipes were allowed: raw source at LR3e-4; then the literal prefix `Restore transcript: ` at LR1e-4. Each used 600 updates, batch4, seed42 deterministic shuffled/repeated TRAIN order, constant LR, full-model AdamW beta(.9,.999), epsilon1e-8, decay.01 and clip1. No extra recipe, output-dependent sample change or oversampling was introduced. Complete source/prefix/target byte admission uses capacity512 including EOS, never truncation. Maximum observed native source/target length is237 before the twenty-byte prefix; the slice fits both recipes. Greedy decoding allows512 new positions, EOS1/PAD0/decoder-start0, strict byte+3 mapping and strict UTF-8. No sentinel stripping or forced completion rescues outputs. Four repeated-input RAW-copy diagnostics per panel are excluded from natural results; preservation is assessed on naturally eS=0 requests.

## Natural results

RAW has 20/416 word errors, WER4.8076923%. Both unadapted panels produced 0/24 valid completions and 100% failure WER. Invalid outputs map to empty observation and zero completed repair.

| Recipe / updates | Valid completions | Output errors | WER | Useful / damaged cases | Clean lexical preservation |
|---|---:|---:|---:|---:|---:|
| Raw LR3e-4 / 200 |24/24|21|5.0481%|0 / 1|15/15|
| Raw LR3e-4 / 600 |24/24|20|4.8077%|0 / 0|15/15|
| Prefix LR1e-4 / 200 |24/24|30|7.2115%|0 / 8|10/15|
| Prefix LR1e-4 / 600 |24/24|22|5.2885%|0 / 2|13/15|

At recipe1's endpoint, five byte changes are exclusively case/punctuation changes; all outputs are lexical copies of the source. Recipe2 introduces one word error in each of two initially correct requests and has no useful correction. Validity, lower loss, surface changes and copy preservation are separate from useful restoration.

Every loss and preclip gradient norm is finite. Recipe1's first/last train loss is1.4426036/.2751951; recipe2's1.3979942/.2916923. Large first-step norms are clipped under the declared policy; maxima247.263/328.903 remain recorded. Each recipe presents 2,400 examples, 124,102 common project-BPE anchors and295,080 supervised native byte positions including EOS. Source-native positions are293,222/341,222; the48,000 difference exactly equals the twenty-byte prefix ×2,400 presentations. There are1,024 unique training sources, not2,400 independent observations per recipe.

Synchronized update timers total283.785/300.027seconds. Post-baseline wall including later panels/checkpoint work is356.310/381.268seconds; baseline decoding adds70.006/68.759seconds. Their accounted subtotal is876.343seconds, excluding cold-load/preparation. Peak process RSS is6,997,868,544/7,800,586,240bytes; update-boundary Metal driver maxima14,815,412,224/14,569,521,152bytes overlap RSS and are sampled, not continuous physical-memory peaks. Short-check affordability does not prove an affordable useful final comparator.

## Evidence and repair decision

Ignored `exports/foundation-repair/byt5-natural-adaptation-attempt{01,02}/` retains pre-run HEAD/dirty diff, actual model/config/code/data/tokenizer/runtime hashes, seed/order/role IDs, initial precision/model identity, all1,200 updates and168 generated-ID records, full failure/baseline panels and adapted checkpoints. Exact pinned weight SHA256 is`5c5aaf56299d6f2d4eaadad550a40765198828ead4d74f0a15f91cbe0961931a`; config`7845fb21b320f3fa05392ce151143502cf08729c8c89732da3293615885d3e83`. Adapted checkpoints hash`375406ad9b2db34b201bdf39f0207942cf4f3d077b3f993b392614eeed47312c` and`4a99dd6504c2ecbdc96928da3c812bba0394a3972e72adff25dc802ff2dd9722` and remain external.

Independent review reconstructs every native generation, lexical distance, deterministic selection/exposure counter and checkpoint hash. Five interface/recipe regressions pass. Capacity, strict byte/EOS serialization and finite optimization are supported within this short admitted slice. Useful correction is the remaining adequacy problem. These recipes jointly vary prefix and LR, so they cannot isolate causal prompt versus optimization effects; insufficient exposure, error diversity, recoverability and optimizer adequacy remain unresolved. This is a bounded local recipe failure, not an architectural rejection or scratch-superiority result. Further tuning requires a separately declared diagnosis and budget; none is silently added here.

No final/sealed candidate inference, final training, production change, human annotation/listening, final recipe selection or paper-protocol freeze occurred.

REPAIR_REQUIRED
