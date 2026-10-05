# Scorer qualification on natural DEVELOPMENT outputs

**Measured aggregate alignment is informative on genuine changed natural outputs, including substantial introduced damage. Final H1 precision and local/literal identification are not established.** This extends the earlier identity-only audit; it does not replace its original 250,000-state cap records or manually resolve an ambiguity.

## Fixed sources, full panels and independence

The existing source/reference preflight is computed before each candidate is scored and frozen by source, reference, mask and preflight hashes. The unchanged Unicode 15.1 `lexical_eval_v1`, pair-cell limit 4,000,000, joint-state limit 250,000 and move-work limit 1,750,000 apply. The [runner](../../benchmarks/natural_output_scoring.py) rejects missing/duplicate requests or changed preflight source/reference bytes. All preselected outputs are retained; identity outputs, failures and unfavorable outputs are not filtered from the natural profile.

ByT5 has 24 distinct requests: twelve unchanged HPO recordings plus twelve prospectively consumed CALIBRATION requests, from 17 source components. Nine requests in eight groups contain lexical source errors. Two recipes × panels at steps 0/200/600 give 144 scored records, not 144 independent cases. Four explicitly authored RAW-copy controls per generation panel are separate diagnostics and excluded from the natural profile.

B100/C101 share a different frozen 24-request panel: twelve fitted TRAIN fixtures in eleven components and twelve held-out CALIBRATION requests in five source-disjoint components. Density thirds and source-length quantiles determined selection before model outputs. Two repetitions label the same post-fit model and requests; they are not additional training, independent cases, independent source groups or independent timing sessions. The 23-row union of CALIBRATION requests consumed by comparator/native development is explicitly overlaid in [consumption metadata](../../experiments/manifests/development_calibration_consumption.attempt01.json); 6,248 role-level CALIBRATION rows remain untouched.

Original natural-scorer attempt01 called its 24 requests `independent_cases`. The ignored original summary is preserved; a separate correction records **24 distinct requests / 17 components**, and its [public receipt](../../experiments/manifests/foundation_repair/natural-scorer-attempt01.json) contains that correction. Later summaries use distinct requests/components. No repetition or source-row total supplies statistical independence.

## ByT5 natural changes and failures

Every panel has 416 reference words and 20 fixed source errors. Native bytes are decoded under the independently qualified ByT5 interface; invalid UTF-8 is not repaired or replaced with a favorable source copy. An invalid/incomplete output maps to the scorer's declared empty failure view; any internal repair count on that view does not become completed repair.

| Recipe / panel | Valid complete / 24 | Byte / lexical nonidentity | Output errors | Completed repair | Introduced units |
|---|---:|---:|---:|---:|---:|
| Both initial models | 0 | 24 / 24 | 416 | 0 | 397 |
| Raw source LR3e-4, step200 | 24 | 13 / 1 | 21 | 0 | 1 |
| Raw source LR3e-4, step600 | 24 | 5 / 0 | 20 | 0 | 0 |
| Prefix LR1e-4, step200 | 24 | 15 / 8 | 30 | 0 | 10 |
| Prefix LR1e-4, step600 | 24 | 8 / 2 | 22 | 0 | 2 |

All 144 records have point-identified repair/introduced totals, zero cap/fallback count, zero total bound width and zero reported local ambiguity. Maximum optimized joint states/edges/move work are 34 / 33 / 238. At initialization the failure view has one internal repair unit; completed repair remains zero. The two measured scorer processes take **1.147675 / 1.152892 seconds** including fixed-source preparation, tracing and record export; preflight costs **0.173052 / 0.171615 seconds**. Python traced peaks are **2,418,279 / 2,417,216 bytes**; RSS **31,850,496 / 31,899,648 bytes** is a separate overlapping process view. These are local CPU timings, not independent replicated performance estimates.

Evidence: [raw-recipe receipt](../../experiments/manifests/foundation_repair/natural-scorer-attempt01.json), [prefix-recipe receipt](../../experiments/manifests/foundation_repair/natural-scorer-attempt02.json), [adaptation report](BYT5_DEVELOPMENT_ADAPTATION.md). Failed and changed rows all remain in ignored full output/score ledgers.

## B100 natural correction and substantial damage

B100 completes all 48 native calls. Strict expansion of the actual frozen BPE token IDs reproduces every recorded output. Both repeats have identical bytes, tokens and statuses; the following counts use one repeat to avoid doubling the case population.

| Role / 12 requests | Reference words | Fixed source errors | Output errors | Byte / lexical changes | Completed repair | Introduced |
|---|---:|---:|---:|---:|---:|---:|
| Fitted TRAIN | 278 | 10 | 0 | 11 / 5 | 10 | 0 |
| Held-out CALIBRATION | 258 | 2 | 280 | 12 / 12 | 0 | 278 |

The pooled 10/12 repaired-source-error figure is entirely fixture memorization; held-out utility is zero and CALIBRATION WER is 108.5271%. This is legitimate nonidentity scorer stress evidence, not evidence that a tiny fixture fit generalizes or that the unrun 10M recipes failed.

All 48 records have point totals, zero caps and zero total bound width. Maximum optimized states/edges/move work are **112 / 192 / 784**. **Every one of the twelve CALIBRATION requests has local ambiguity**, involving 220 of its 258 reference occurrences per repeat; fitted TRAIN has none. Independent dense forward/reverse costs reproduce every local reference/source event set. Point totals therefore do not authorize local literal/typed attribution or a manual tie choice.

The B100 scorer process takes **1.644206 seconds**, including **0.245656 seconds** of preflight, tracing and export. Python traced peak is **2,718,322 bytes**, process RSS **32,473,088 bytes**. [Payload-free B100 receipt](../../experiments/manifests/foundation_repair/natural-scorer-b100-attempt01.json) pins the original output, preflight, provenance and record hashes.

## C101 matched natural output audit

C101 completes all 48 calls. Each stored program binds the correct source identity, uses legal nonoverlapping UTF-8 boundaries and independently renders to the exact recorded output. No invalid-prefix source rescue occurs. Both repeats return identical programs/statuses/bytes. Native decoder positions are runtime measurements; generated replacement token IDs were not exported, so rendered strings cannot independently establish their original BPE segmentation.

| Role / 12 requests, one repeat | Reference words | Fixed source errors | Output errors | Byte / lexical changes | Completed repair | Introduced |
|---|---:|---:|---:|---:|---:|---:|
| Fitted TRAIN | 278 | 10 | 0 | 11 / 5 | 10 | 0 |
| Held-out CALIBRATION | 258 | 2 | 91 | 12 / 12 | 0 | 89 |

All twelve fitted targets are exact; none of the twelve held-out targets is exact. C predicts one edit on every held-out request, with six recorded decoder positions; its held-out WER is 35.2713%, against RAW 0.7752%. Lower damage than B in this fixture-fit setting does not establish a trained representation advantage or successful held-out repair.

All 48 score records have point totals, zero caps and zero total widths. Maximum optimized states/edges/move work are **63 / 80 / 441**. Ten of twelve CALIBRATION cases have local ambiguity, involving 87 of 258 reference occurrences per repeat; TRAIN has none. These local sets remain unresolved despite exact aggregate totals. The independent dense count/local audit reproduces them without choosing an alignment.

The C scorer process takes **1.244123 seconds**, including **0.236257 seconds** of preflight, tracing and export. Traced peak is **2,423,917 bytes**, process RSS **31,883,264 bytes**. The [C101 receipt](../../experiments/manifests/foundation_repair/natural-scorer-c101-attempt01.json) pins original native/transport/preflight/score evidence. Across both ByT5 screens and B/C panels, all **240 records** remain retained, representing **47 distinct requests / 28 known components**: twelve HPO, 23 consumed CALIBRATION and twelve fitted TRAIN requests. These are repeated observations, not 240 independent cases or proof of undisclosed source independence.

## Independent reproduction and practical interpretation

The [independent review](../reviews/NATURAL_SCORER_INDEPENDENT_REVIEW.md) reconstructs source/reference lexical tables, strict native decoder transport and every record using a separate dense seven-move full-state oracle. It verifies count extrema, repaired/introduced decomposition, failure mapping and all local correspondence sets for B100/C101. Maximum dense state cube is 39,304 cells. ByT5 dense verification takes about 3.48/3.25 CPU seconds; B100 count/local audits take 5.4920/1.6346 seconds. C audit timing is recorded separately in the review. These review runtimes are not substituted for optimized scorer timing.

The observed nonidentity natural totals are narrow enough for bounded DEVELOPMENT use, even on severe introduced damage. No claim extends that result to unseen long/repeated text or the original pathological hypotheses: original capped records remain evidence. Aggregate alignment width, local correspondence ambiguity and statistical precision are different questions. H1 statistical precision, paired cluster bootstrap cost, typed/literal coverage, full natural/stress roster and the fixed equal-domain endpoint remain unqualified while SLUE is unavailable. No final output, human adjudication or paper freeze was used.
