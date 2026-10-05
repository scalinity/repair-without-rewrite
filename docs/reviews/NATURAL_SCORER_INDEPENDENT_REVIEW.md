# Independent natural scorer coverage review

**Disposition: PASS for selected natural DEVELOPMENT output scoring; representative H1 coverage remains unqualified.** Both ByT5 recipes and B100/C101 natural-output parity pass. Static interface and failure mapping checks also pass in the bounded cases below. This review is independent of the scorer implementer. The reviewer owns this document only and has not changed model, scorer or data code. No accelerator workload, final/sealed inference or human annotation was used.

FACT: The reviewer read the repository authorization, kickoff/package contracts, accepted findings, canonical Part IV.1–IV.9, registry primary scorer contract, existing scorer qualification report and prior independent review. Existing synthetic arithmetic evidence and RAW-copy source audits remain useful, but do not establish natural nonidentity candidate coverage.

## Interface and failure mapping

The current development API is `prepare_source(reference, source)` followed by `score_output(prepared, Output(text, status), Limits(...))`. `lexical` in `src/scoring/text.py` returns the lexical tuple; there is no `lexical_eval_v1` function. `distance` in the scorer modules computes unit-cost token edit distance; there is no `levenshtein` function in the existing oracle. Initial new-runner import names were flagged and corrected before the costly adaptation launch.

MEASURED RESULT: An independently hand-derived 11-case status/text matrix on `R="a b", S="x b"` passed. Complete reference output has eS=1, eO=0, raw/completed repair [1,1], introduced [0,0]. A capped or timeout reference prefix retains eO=0 and raw repair [1,1], but completed repair [0,0]. Genuine completed empty output remains complete, with eO=2, raw repair [0,0] and introduced [1,1]. Invalid UTF-8, invalid C, missing output, abstention and no-prefix timeout each observe empty text with eO=2 and zero completed repair, even if an accompanying nominal text says "a b". `complete` with null text maps to missing; `complete` with a surrogate maps to invalid UTF-8. Three additional zero-cell/state/move-budget cases preserve the same eO and completion rules. These are bounded interface fixtures, not natural model observations.

Source masks and the full source-preflight hash are validated before candidate scoring. The reviewer found no output-dependent reference choice, denominator change or rematerialization of an unavailable source mask in the inspected interface. Computational cap counts must inspect `fallback_reason`, including a closed-form point result reached after a local graph cap; total point identification does not establish local occurrence identity.

## Prospective independent output check

Before inspecting new candidate outputs, the reviewer declared this plan: retain every preselected natural row, decode native byte IDs independently under the strict start/EOS/byte/UTF-8 rules, recompute lexical tokens with the pinned Unicode 15.1 tables and a separately written scanner, recompute eS/eO/eSO with an independent rolling-row recurrence, and compare repair/introduction extrema with an independently written dense seven-move lexicographic recurrence for every triple whose full cube has at most 250,000 cells. Larger triples retain independent distance, conservation and envelope checks; they are not removed from coverage. The declared scorer work caps remain 4,000,000 pair cells, 250,000 joint states and 1,750,000 examined moves. No favorable cap increase, manual tie resolution or output-based sample redraw is permitted.

Natural full-text candidate panels will be kept separate by recipe/checkpoint. RAW-copy controls have their own status and denominator, and will not substitute for nonidentity candidate evidence. Both byte changes and lexical changes will be counted because formatting changes can retain the O=S lexical identity. Independent CPU timings describe this selected workload and do not qualify exclusive machine performance while other work is active.

INFERENCE: A small LS-PC-only development panel can qualify the scoring path on its actual outputs. Its point coverage or narrow intervals cannot alone establish H1 precision, reference recoverability, cross-domain source support or paired cluster uncertainty. The registered SLUE half-weight remains unavailable while access is unresolved. No H1 primary result or publication gate is implied by this review.

## Attempt01 actual natural outputs

MEASURED RESULT: The reviewer independently checked all 72 natural rows from three repeated ByT5 checkpoint panels, using a new lexical scanner which reads the pinned folding/whitespace tables directly, strict native-ID decoding, an independent rolling-row distance recurrence and a fresh dense seven-move lexicographic recurrence. Expected values never called production scorer, existing oracle, lattice or traceback code. Every complete dense cube fits the predeclared 250,000-cell review bound; the largest is 39,304 cells. Independent lexical/dense verification took 3.479475 seconds on CPU. This is review cost, not a production-throughput measurement.

All 72 rows agree on strict decoded text/status, reference/source/output lexical counts, eS/eO/eSO, conditional S/O cost, repair/introduction extrema, reference damage, insertion damage, edited-but-unresolved extrema, completion credit and raw conservation. Reference/source byte hashes and every repeated source-preflight binding agree. The scorer retains every invalid row.

| Checkpoint | Natural requests | Complete | Byte-change flags | Complete lexical changes | eS / reference words | eO | Raw repair | Completed repair | Introduced |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 24 | 0 | 24 invalid observations | 0 | 20 / 416 | 416 | 1 | 0 | 397 |
| 200 | 24 | 24 | 13 | 1 | 20 / 416 | 21 | 0 | 0 | 1 |
| 600 | 24 | 24 | 5 | 0 | 20 / 416 | 20 | 0 | 0 | 0 |

The sole complete lexical change is `4572-112381-0006` at step 200: source error1 becomes output error2, repair [0,0], introduced [1,1]. Step 600 has formatting changes but remains O=S under the lexical policy. Step 0 invalid UTF-8/native outputs correctly map to empty observations; removing one source insertion earns raw diagnostic repair 1 but no valid-completion repair. Its 24 lexical nonidentity flags describe failed empty observations, not valid restoration evidence.

MEASURED RESULT: All 72 scorer rows are exact points, with zero computational caps and zero aggregate repair/introduction widths. Maximum graph size is 34 states/33 edges and maximum examined moves 238. The captured root run reports 1.147675 seconds including traced preflight/export, Python traced peak 2,418,279 bytes and process RSS 31,850,496 bytes. These memory views overlap. The reviewer checked the recorded counters and artifact identity; the dense audit's runtime is a distinct measurement and does not independently reproduce these production timing/memory values.

There are 24 distinct requests, not 72 independent cases. More precisely, they occupy 17 source components, with source errors in 9 cases from 8 components. Twelve requests are HPO development and twelve calibration. The wording `independent_cases:24` in the summary denotes distinct request identities; it must not be read as 24 statistically independent source clusters.

Reviewed identities:

- `exports/foundation-repair/byt5-natural-adaptation-attempt01/outputs.jsonl`: `86d151695d818107feaeb4aab33533632123d15cb09eff3b3e348347df9b7161`.
- `exports/foundation-repair/natural-scorer-attempt01/records.jsonl`: `c1fff3dffcb966c841c6ad31873e2b26c9d56edbd4003ec5081dd8a20c5a23bf`.
- `exports/foundation-repair/natural-scorer-attempt01/source_preflights.json`: `4c8a27723f501280cfd2423ea5fd0dc4d4b4db9136c9f8237f996eaf2d3b4258`.
- `src/scoring/triple.py`: `1709603f910e46c85eb9b18dbb574cf988dd0d7aab701d3be1ff0e62144a00e1`.
- `src/scoring/records.py`: `7b031fa76c408b22ff2c1435236b6d38338bfddef5c83b2fd347c4660624108e`.
- `src/scoring/text.py`: `4db62c3238c830ec25faf979beb656dcc7b882f0843b318d973934b4f340111d`.

INFERENCE: Attempt01 qualifies the actual failure/copy path and one natural damage transition. It supplies no successful natural repair transition and very little complete lexical nonidentity diversity. Its zero-width result does not estimate scorer behavior on representative useful B/C edits or establish H1 identification. Additional prospectively bounded recipe and B/C natural outputs remain to be reviewed; no changed scorer budget is justified by this result.

## Attempt02 actual natural outputs

MEASURED RESULT: All 72 second-recipe natural output/score rows pass the same independent strict-decoding, lexical, distance and dense-extrema checks. The independently recomputed R/S bytes, source components and source-preflight bindings are identical to attempt01. The largest dense cube remains 39,304 cells and independent lexical/dense audit cost is 3.255557 seconds. The two recipes expose repeated observations of the same 24 requests from 17 components, not 48 new source cases or 144 independent observations.

| Checkpoint | Requests | Complete | Byte-change flags | Complete lexical changes | eO | Raw repair | Completed repair | Introduced |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 24 | 0 | 24 invalid observations | 0 | 416 | 1 | 0 | 397 |
| 200 | 24 | 24 | 15 | 8 | 30 | 0 | 0 | 10 |
| 600 | 24 | 24 | 8 | 2 | 22 | 0 | 0 | 2 |

The shared denominator remains 416 reference words and 20 source errors. All 72 rows are point-identified, with no cap or raw repair/introduction width; maximum 34 states/33 edges/238 attempted moves. The root's captured traced/exported cost is 1.152892 seconds, traced peak 2,417,216 bytes and process RSS 31,899,648 bytes. Independent parity verifies count/cap counters and identities; it does not convert the separate dense review cost into production timing or repeat the root's memory profile.

The source-correct cases `5694-64038-0014` and `1970-26100-0004` each acquire one introduced error at the final checkpoint. Earlier step 200 has eight complete lexical changes, including one three-error change, for introduced 10 and no repair. These are legitimate natural nonidentity candidate outputs rather than constructed edits; they qualify the observed damage branch. They still do not demonstrate successful natural repair or representative C edit distributions.

Resolved documentation finding: the root preserved attempt01's original `independent_cases` field and added `exports/foundation-repair/natural-scorer-attempt01/independence_label_correction.json`, explicitly identifying24 distinct requests/17 components and 9 error-bearing requests/8 components. Attempt02 now uses `distinct_requests` and `source_components`. The reviewer inspected the sidecar; no raw result or repeated-panel denominator was rewritten.

Reviewed second-run identities:

- `exports/foundation-repair/byt5-natural-adaptation-attempt02/outputs.jsonl`: `06eefe36d128c491ca2f1a81fae6323b7223147a097184df45c11d09a7a7e2c4`.
- `exports/foundation-repair/natural-scorer-attempt02/records.jsonl`: `2f8377bb5ba6f4bd5625811fb1b02876e66a9d2f39ce6a9dbdd3f61d6b43ef5d`.
- `exports/foundation-repair/natural-scorer-attempt02/source_preflights.json`: `4c8a27723f501280cfd2423ea5fd0dc4d4b4db9136c9f8237f996eaf2d3b4258`.

INFERENCE: Selected natural-output scoring is correct on both reviewed recipes, including native failure and observed natural damage. Broader coverage remains conditional on the forthcoming B/C outputs. No cap adjustment, added human resolution, final candidate inference or favorable exclusion is warranted.

## B100 complete natural decodes

MEASURED RESULT: All 48 original B100 native calls are complete. The reviewer reconstructed the literal byte map directly from all 16,064 merge pairs in the trained artifact, checked the entire saved byte-map equality, rejected control/noninteger IDs, expanded each original native token sequence, decoded strict UTF-8 and matched original and transported output bytes. Every status maps to the same complete result, every source/target/role/component binding matches, and both repeats return identical token IDs, output bytes and status. The original completion marker is supported by the inspected decoder's EOS branch; its exported literal token list intentionally excludes EOS. This audit verifies expansion and the recorded terminal status, not a second accelerator inference.

Fresh dense seven-move and pinned lexical checks reproduce all 48 eS/eO/eSO values, conditional cost, repair/introduction, reference/insertion damage, edited-unresolved extrema and completion accounting. Maximum dense cube is 39,304 cells; independent literal/lexical/dense audit cost is 5.492042 seconds. A separate dense forward/reverse lexicographic recurrence then collected every optimal-column reference/source event without reusing production pair lattices or oracle code. Its 24 distinct triple computations reproduce both repeats' 48 reference and source event-set records in 1.634624 seconds.

The output transport labels 300/301 identify repeat 0/repeat 1 at the same frozen model; they do not represent new training checkpoints or 48 distinct examples. There are 24 requests from 16 source components. TRAIN and heldout calibration must remain separate:

| Population, per repeat | Requests | Words | Source errors | Output errors | Complete | Complete lexical changes | Completed repair | Introduced | Exact target | Locally ambiguous cases |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Fitted TRAIN | 12 | 278 | 10 | 0 | 12 | 5 | 10 | 0 | 12 | 0 |
| Heldout calibration | 12 | 258 | 2 | 280 | 12 | 12 | 0 | 278 | 0 | 12 |

All 48 primary total results are points, zero caps, zero repair/introduction widths, with maximum 112 states/192 edges/784 examined moves. Exact primary totals coexist with extensive local uncertainty: each heldout repeat has 220/258 reference occurrences with variable event/occurrence mapping, and all 12 heldout cases have some local ambiguity (maximum 30 reference occurrences in one case). No literal point identification follows from the primary total points. The independent dense event-set audit confirms this distinction.

The captured root production score run reports 1.644206 seconds including traced preflight/export, traced peak 2,718,322 bytes and process RSS32,473,088 bytes. The reviewer validates artifact/counter identities and separately reports its CPU verification cost; these are not exclusive production-throughput replications. All score records identify `B100_native_greedy`, and the transported/source-preflight identities retain the exact public natural inputs.

Reviewed B100 identities:

- `exports/foundation-repair/b100-real-calibration-attempt01/decodes.jsonl`: `f21ec359406ed1d5d7bf6ca445f9fb69b8f06645f16405cbfcf4498591457af9`.
- `exports/foundation-repair/b100-natural-output-transport-attempt01/outputs.jsonl`: `5212d79120d016815850a6cc6a1e9e5cd62753e28a9c9f66655e0748c3b945d0`.
- `exports/foundation-repair/natural-scorer-b100-attempt01/records.jsonl`: `6aa5e734874d839ddc39ed3108812e7934d1df061c61e6c8aef07cf4e5e7fd11`.
- `exports/foundation-repair/natural-scorer-b100-attempt01/source_preflights.json`: `0e615a04a6d2fd3fb3b9f59ec349fc8fde8fb1bdda1d9558768f52ef9d77817b`.

INFERENCE: This audit adds genuine natural nonidentity repair, heavy heldout damage and local-ambiguity observations to the scorer qualification. The successful repairs are entirely fitted TRAIN memorization; the 12 heldout requests have no useful repair and high damage. The pooled repair fraction 10/12 must not be used as heldout utility evidence. Arithmetic and selected output coverage pass, while learning/H1 admission remain separate decisions. The subsequent C101 review below closes the remaining output audit.

## C101 complete source-bound programs

MEASURED RESULT: All 48 original C101 calls are complete. The reviewer independently rendered every emitted program directly from raw source bytes, validating 76 predicted edits across both repeats. Checks cover the exact source SHA-256/byte length, END terminal, exact integer ordered/nonoverlapping offsets, UTF-8 replacement text and legal scalar/BPE pointer boundaries. Source BPE literals were expanded directly from the saved merge-derived byte map; cumulative offsets and scalar-boundary mask match the exact hash-bound calibration selection. Every independently rendered output matches native and transported bytes. All roles/source groups and the complete request roster match B100. Both repeats return identical program, bytes and status.

The C export retains complete replacement strings/programs, not the raw generated replacement token IDs or a full END_EDIT/action trajectory. Therefore independent per-generated-ID expansion/grammar verification is unavailable for C. This is an explicit evidence limit; the reviewer does not invent a token trace or claim a second neural inference. The source-bound emitted program, its END marker, exact pointer legality and complete rendering are independently verified.

Fresh dense lexicographic extrema and dense forward/reverse all-optimal columns reproduce all 48 count and local event-set records: eS/eO/eSO, conditional cost, repair/introduction, reference/insertion damage, edited-but-unresolved counts, source/reference event sets and completion accounting. There are 24 distinct dense triples, maximum 39,304 cells, and combined independent rendering/lexical/dense review cost 2.903738 seconds. All statuses and model-view identities agree with `C101_native_greedy`.

| Population, per repeat | Requests | Words | Source errors | Output errors | Complete | Complete lexical changes | Completed repair | Introduced | Exact target | Locally ambiguous cases |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Fitted TRAIN | 12 | 278 | 10 | 0 | 12 | 5 | 10 | 0 | 12 | 0 |
| Heldout calibration | 12 | 258 | 2 | 91 | 12 | 12 | 0 | 89 | 0 | 10 |

All 48 primary totals are exact points, with zero caps and repair/introduction width. Maximum graph size is 63 states/80 edges with 441 examined moves. Local ambiguity remains in 10/12 heldout requests and 87/258 reference occurrences per repeat. TRAIN has no local ambiguity. The source-preflight bytes/hash are identical to B100, so differences cannot come from a changed denominator, candidate-specific source mask or source redraw.

The captured production run reports 1.244123 seconds including traced preflight/export, Python traced peak 2,423,917 bytes and process RSS 31,883,264 bytes. Independent dense parity is a separate CPU measurement. These memory views overlap; neither their sum nor this small-workload rate estimates a full natural evaluation campaign.

Reviewed C101 identities:

- `exports/foundation-repair/c101-real-calibration-attempt01/decodes.jsonl`: `0cd7f1101d01b9577a10d5b0f1e53835ddb632f04ec83ff68f4ce922b895c2e0`.
- `exports/foundation-repair/c101-natural-output-transport-attempt01/outputs.jsonl`: `01ce43c54a2da4a78aad9608b1709e96f45fa07f35025b8203d336ff9a2fb2c5`.
- `exports/foundation-repair/natural-scorer-c101-attempt01/records.jsonl`: `08dfbe1e400d3d558feaf7fd320eb8f5ed5c1ad4cd1a91271cd850ba05c9ee73`.
- `exports/foundation-repair/natural-scorer-c101-attempt01/source_preflights.json`: `0e615a04a6d2fd3fb3b9f59ec349fc8fde8fb1bdda1d9558768f52ef9d77817b`.
- `exports/foundation-repair/bc-real-calibration-selection-attempt02.json`: `0bfe80a6eaf8a5c6ad6abf03d88dd3b6a80cddb9380709a985d555158bf02166`.

## Final scope and limits

MEASURED RESULT: All 240 reviewed scorer rows pass independent distance/extrema checks. Both B/C streams additionally pass independent complete byte rendering and every local event-set check. Every row has point-identified primary totals and no scorer cap or aggregate attribution width under the unchanged deterministic budgets. The 240 records are repeated recipe/checkpoint/timing observations of 47 distinct requests from 28 known source components: 12 HPO, 23 calibration and 12 fitted TRAIN. They are not 240 independent natural samples.

INFERENCE: The selected DEVELOPMENT scorer path is qualified on legitimate nonidentity natural outputs, including successful fitted repair, heavy heldout damage, native byte failures and extensive local occurrence ambiguity. No unexplained arithmetic disagreement remains. Total identification and local identification differ: point repair/introduction totals do not certify literal correspondence when the recorded event sets vary.

The B/C runs are bounded fixture-fitting/calibration work, not the six 10M development recipes or final H1 training. All positive B/C repair belongs to fitted TRAIN. Heldout B/C calibration has only two source errors, neither repaired, and substantial introduced damage. C's smaller damage count than B's in this workload is not H1 success. ByT5 has no useful heldout restoration in either bounded recipe. The absence of large-cap triples and nonzero count intervals in this selected panel does not establish their absence at useful outputs, broader lengths, full source supply or final inference volume. SLUE access, equal-domain primary endpoints, literal qualification, paired cluster uncertainty and final H1 precision remain unavailable. No final/sealed candidate inference, source exclusion, altered scorer budget or human resolution was used.
