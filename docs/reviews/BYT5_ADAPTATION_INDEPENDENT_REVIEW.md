# ByT5 development adaptation independent review

Review date: 2026-10-05. Scope: development only. This reviewer performed no model inference or accelerator workload, changed no implementation, and inspected no sealed candidate outputs. Root owns the native adaptation screen. This document records independent CPU reproduction of both completed natural adaptation attempts, retained baseline failures and pre-run repairs.

## Initial contract and preserved failure

Read the repository authorization, accepted findings, kickoff/package materials, comparator qualification, prospective amendments, canonical source §§9.1, 11.4 and 19.8, and the draft registry's ByT5/runtime/exposure/failure requirements. The pretrained comparator must retain its official native byte interface; the project's BPE is an accounting anchor only. Source input is raw one-best plus trusted task framing. A reference or case-specific error mask must not enter the encoder. Valid restoration behavior, useful corrections and source-disjoint generalization must be checked separately from loss reduction.

Pinned model identity is `google/byt5-small@68377bdc18a2ffec8a0533fef03b1c513a4dd49d`, weight SHA256 `5c5aaf56299d6f2d4eaadad550a40765198828ead4d74f0a15f91cbe0961931a`, config SHA256 `7845fb21b320f3fa05392ce151143502cf08729c8c89732da3293615885d3e83`. The local acquisition receipt and model config identify the same revision, decoder start/PAD=0, EOS=1, vocabulary=384 and untied embeddings. The native runner must recompute the actual asset hashes before loading.

Independent standard-library decoding of every original `public_byt5_probe_attempt01.json` ID sequence reproduced **0/4 complete valid outputs**. Each sequence begins decoder-start 0, then byte255 (ID258), emits 64 native tokens and never emits EOS. The output IDs are within the legal byte range 3–258, but the first byte makes strict UTF-8 decoding fail. This is a more specific diagnosis than merely naming a non-byte/sentinel error. The report SHA256 reproduced as `dc2988494f73b5c1298ba7585b096b2405c5db5a1245d8504ee891e3c4445f61`. The historical attempt remains unchanged; no byte stripping, replacement decoding or forced EOS repairs it.

Existing ByT5 regressions independently executed: **3 passed** (`tests/data/test_byt5_probe.py`). They cover terminal EOS, capped valid prefixes, strict invalid UTF-8, decoder-start handling, PAD after EOS, source capacity rejection, supervised EOS, PAD-loss masking and a real decoder-start attention position. Code inspection agrees: `byt5_batch` uses UTF-8 byte+3 IDs plus EOS, pads sources with 0, ignores target padding with -100, shifts target labels, and masks decoder positions from nonignored labels. An empty target still supervises EOS.

An independent expected-vector check additionally compared nine byte round trips (empty, accented scalar, combining sequence, emoji, NUL/newline/tab, literal sentinel/PAD spellings, repeated spaces and mixed path/flag text) and a ragged batch including an empty/NUL target. All exact byte-ID, mask, shifted-input and supervised-count expectations agreed. Recomputed local model-config SHA256 matches the pinned value above.

## Pre-run defects reported to root

The first draft of `benchmarks/byt5_development_adaptation.py` could not import: independent CPU `importlib.import_module` reproduced `ImportError: cannot import name 'lexical_eval_v1' from 'src.scoring.text'`. The draft also imported nonexistent `levenshtein` from `src.scoring.oracle`; the repository APIs are `lexical` and `distance`. This is a runner defect, not model or adaptation evidence. Root was notified before a native screen.

Other draft findings were reported before launch: original twelve HPO examples lacked upfront capacity validation; the model config hash was logged but not compared to its pinned value; pair source hashes/runtime were not explicitly checked; and the nominal two-recipe guard allowed four learning-rate/prefix combinations. The draft's four `identity-control` rows repeated unchanged corrupted HPO inputs with the source string designated as evaluation target. Those are RAW-copy diagnostics, not independent clean-input identity-preservation cases. Naturally source-correct rows are the defensible clean-source diagnostic; copy-control summaries must remain separate from natural performance.

Independent CPU inspection of the first twelve repaired source records confirms twelve distinct unchanged HPO IDs, complete source lengths 28–172 byte IDs including EOS (48–192 with `Restore transcript: `), and target lengths 29–169 including EOS. All fit the proposed 512 capacity. Using the repository's frozen lexical normalization and a separately written rolling-row edit-distance implementation, the unchanged HPO baseline has **198 reference words / 5 source errors = 2.5252525% WER**, eight lexically source-correct cases and three byte-identical cases. These source-correct cases can measure preservation without a fabricated identity target or feeding the reference as model input. This confirms context admission for this small panel only.

## Independent verification criteria

- Recompute pair-manifest/config/model/tokenizer hashes; join each selected stable ID to its admitted role and target hashes; verify training and held-out parent groups are disjoint. Preserve failure/cap admissions and selection reasons, rather than silently filtering poor ASR/corrector behavior.
- Verify task prefix plus raw source plus EOS and clean target plus EOS fit the declared capacities. Check full panel lengths and overflow counts; a short admitted slice cannot qualify arbitrary context or the whole official development population.
- Verify training uses train rows only and held-out rows never enter the optimizer. Name whether the evaluation partition is HPO or previously untouched calibration; new use of calibration for recipe comparison consumes its untouched role for subsequent guard fitting.
- Reconstruct native labels, decoder inputs, valid decision counts, encoder/decoder masks and common target-anchor exposure totals. Check literal control-looking text stays bytes, not tokenizer-interpreted sentinel IDs.
- Inspect bounded recipes, optimizer/learning schedule, seed/order, clipping, finite losses/gradients and recorded completed-update costs. A failed recipe cannot be replaced invisibly, and decreasing raw train loss is not a validity or useful-correction criterion.
- Independently decode raw generated IDs with strict UTF-8 and EOS/PAD rules, then independently compute lexical Levenshtein distances for R/S and R/O, reference word totals, changed/identity outputs, clean-source damage and useful correction counts. Compare those recomputed counts to the implementing report, including empty failure accounting and valid capped-prefix WER.

## Corrected natural screen and independent launch reproduction

Root repaired the draft before launch: imports now use the actual lexical API and local edit distance; the guard allows exactly `(3e-4, no prefix)` and `(1e-4, Restore transcript prefix)`, with at most 600 updates; all twelve original HPO rows receive complete capacity admission before loading weights; both pinned model/config hashes are checked; pair source hashes are verified; consumed calibration IDs are explicitly recorded; and the duplicated-input controls are named `raw-copy-control`. These controls remain separate from the natural panel. Five relevant regressions independently pass (`test_development_adaptation.py` plus `test_byt5_probe.py`). No reviewer accelerator work ran.

Independent reproduction of `byt5-natural-adaptation-attempt01/provenance.json` verified all **9 captured hashes** against current bytes. All **1,120** selected pair IDs are unique and join to their exact admitted roles, component/family identities, raw/processed target hashes, source hypothesis hash and explicit repaired source-runtime identity. Each has completed source status and 2–12-second audio duration. There are **1,024 train rows in 48 groups** and **96 calibration rows**. The selected 24-case panel contains the unchanged twelve HPO cases and the deterministically hashed twelve calibration IDs in **17 groups**, with **zero train/panel group intersection**. The twelve calibration IDs are consumed for comparator development, leaving **84** of this acquired calibration slice untouched. Maximum source and target native lengths are both **237** including EOS, so the 512 limit admits all selected pairs, including the second recipe's 20-byte prefix. This is qualification of this acquired slice, not arbitrary model context or full-domain feasibility.

An independent strict decoder reconstructed all 28 baseline generations from raw IDs; a full-matrix Levenshtein program, separate from the runner's rolling-row distance, reproduced all recorded lexical distances and word totals. The natural baseline is **24 invalid UTF-8 outputs / 0 valid completions**, **416 reference words**, **20 raw-source errors (4.8076923% RAW WER)** and **416 output errors (100% WER under empty-failure accounting)**. All 24 outputs differ from their source under that failure mapping. Fifteen natural cases are lexically source-correct; all fifteen are damaged by the unadapted invalid-output baseline. The four duplicated RAW-copy diagnostic requests are excluded from these counts. The baseline-only output snapshot SHA256 was `661e212a658db6aa59c2ca88b0c524098c2823ebae2b42b23a05cd4c27d8a37f`; completed append-only file digests are recorded below.

## Attempt01 completed: validity repaired; useful lexical correction absent

Independently decoded **all 84** retained generated-ID records, checked their declared text/status/byte-change/source-length/generated-position fields, and recomputed every R/S and R/O lexical distance. Natural results exclude each panel's four duplicated RAW-copy requests:

| Completed updates | Valid / cases | Output errors / 416 words | WER | Useful cases | Damaged cases | Clean lexical cases preserved | Complete byte-identity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 / 24 | 416 | 100% | 0 | 24 | 0 / 15 | 0 / 24 |
| 200 | 24 / 24 | 21 | 5.0480769% | 0 | 1 | 15 / 15 | 11 / 24 |
| 600 | 24 / 24 | 20 | 4.8076923% | 0 | 0 | 15 / 15 | 19 / 24 |

RAW has 20/416 errors. At update600, all five byte-changed natural outputs are **lexically identical to their raw source**; they change case or punctuation only. Thus this recipe repairs invalid completion behavior and preserves clean lexical content, but has no observed lexical repair on this panel. Neither loss decline nor valid surface changes meet the recorded aggregate-WER-improvement/useful-correction decision. Preservation is measured only in fifteen small natural cases; it is not a universal safety assertion.

A separate deterministic replay of the seed42 shuffle and every four-row selection reproduced **all 600** step ledgers: **124,102 common project-tokenizer anchors**, **293,222 encoder native tokens** and **295,080 supervised native target positions including EOS**. All recorded losses and preclip gradient norms are finite. First/last training loss is 1.4426036/0.2751951; maximum recorded preclip norm is 247.263. The qualified train slice itself contains 22,745 reference words, 521 source errors (2.2906133% WER), 334 source-error rows, 690 lexically clean rows and 182 byte-identity rows; useful-error supervision exists, though the bounded screen presents only 2,400 training examples over 1,024 unique sources. The acquired 96-row calibration slice contains 2,072 words and 59 source errors, before deterministic twelve-row panel selection.

Measured synchronized update times sum to **283.785s**. The attempt summary records **356.310s** after baseline, including later panels and checkpoint work, plus **70.006s** baseline decoding. Their sum is a **426.316s accounted wall subtotal**, not complete cold-load/preparation/end-to-end time. Peak reported RSS is 6,997,868,544 bytes; maximum update-boundary sampled Metal allocations are 5,644,308,992 allocated and 14,815,412,224 driver bytes. These sampled maxima are not a continuously measured device peak and must not be added to RSS as independent physical-memory quantities. FP32 parameter/optimizer-state identities are retained in the initial-identity/summary artifacts.

Recomputed checkpoint SHA256 agrees: `375406ad9b2db34b201bdf39f0207942cf4f3d077b3f993b392614eeed47312c` for 1,198,628,971 bytes. Completed attempt artifact SHA256 values are:

| Artifact within `exports/foundation-repair/byt5-natural-adaptation-attempt01/` | Recomputed SHA256 |
| --- | --- |
| provenance.json | `16c872e22792beae058b96b444602f86be4d05989bb55baa916a3cbe4c5566f8` |
| initial_identity.json | `6ecc1d8336ed3fd930c5601b1229f96dff1b9d9e584839550037569083c7011d` |
| outputs.jsonl | `86d151695d818107feaeb4aab33533632123d15cb09eff3b3e348347df9b7161` |
| steps.jsonl | `dd4b674946c39d41e39dc141208455aee226b98a9ffb4ef86230be164490fd3f` |
| summary.json | `a2f6ec3683c2af3d9d0cc07c6524d4073f44f62e0e8053490a09e65e4d3dce79` |

## Attempt02 completed: valid completions; lexical damage without useful repair

The second exact predeclared tuple uses learning rate 1e-4 and literal trusted prefix `Restore transcript: `, keeping all 1,024 training IDs, all 24 panel IDs, calibration consumption, seed 42 shuffle, optimizer, capacities and 600-update allowance unchanged. Independently verified its nine launch hashes and equality of those selections to attempt01. No error-dependent selection, extra recipe or oversampling occurred.

Reconstructed **all 84** output records and independently reproduced their strict validity, lexical distances, word totals and change fields. All source/reference/group/role fields in both completed attempts additionally join back to the admitted role manifest and exact frozen source hypotheses; the RAW-copy diagnostic targets are separately checked as the raw source. Attempt02 natural results are:

| Completed updates | Valid / cases | Output errors / 416 words | WER | Useful cases | Damaged cases | Clean lexical cases preserved | Complete byte-identity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 / 24 | 416 | 100% | 0 | 24 | 0 / 15 | 0 / 24 |
| 200 | 24 / 24 | 30 | 7.2115385% | 0 | 8 | 10 / 15 | 9 / 24 |
| 600 | 24 / 24 | 22 | 5.2884615% | 0 | 2 | 13 / 15 | 16 / 24 |

At update600, six byte-changed natural outputs are surface-only changes. The two remaining lexical changes damage initially correct cases `5694-64038-0014` and `1970-26100-0004`, introducing one ordinary word error each. No natural final case reduces its R/O distance below the original R/S distance. The sixteen byte-identical completions are preservation behavior, not repair credit.

Independently replayed **all 600** completed step selections: **124,102 anchors**, **295,080 supervised native target positions**, **341,222 encoder native tokens**. The source-token difference of 48,000 exactly equals 20 prefix bytes × four examples × 600 updates; no target or common-anchor difference occurs. All losses and preclip norms are finite; first/last train loss is 1.3979942/0.2916923 and maximum preclip norm 328.903. Synchronized update times sum to **300.027s**; recorded post-baseline wall is **381.268s** and baseline **68.759s**, giving a **450.027s accounted subtotal** with the same cold-load/preparation limitation as attempt01. Peak reported RSS is 7,800,586,240 bytes; maximum update-boundary sampled Metal allocated/driver values are 5,537,303,040/14,569,521,152 bytes. The original attempt remains preserved.

Recomputed adapted-checkpoint SHA256 agrees: `4a99dd6504c2ecbdc96928da3c812bba0394a3972e72adff25dc802ff2dd9722`, 1,198,628,971 bytes. Completed attempt02 artifact SHA256 values are:

| Artifact within `exports/foundation-repair/byt5-natural-adaptation-attempt02/` | Recomputed SHA256 |
| --- | --- |
| provenance.json | `cf83d1bff5fcb7b9508386d6d9f6879fa67d3c23e615446d4b09eef2c2773cc1` |
| initial_identity.json | `6ecc1d8336ed3fd930c5601b1229f96dff1b9d9e584839550037569083c7011d` |
| outputs.jsonl | `06eefe36d128c491ca2f1a81fae6323b7223147a097184df45c11d09a7a7e2c4` |
| steps.jsonl | `f3b8695922a98c1c986d727197fbaccdf46e455fae8576229347736f7bf8be29` |
| summary.json | `c0ee9ba6b47c7d2ac6e4b71ea563333fcf468579e090d582e1f80707a5ed6b60` |

## Independent disposition across both recipes

**Execution/interface review passes within the measured narrow slice; credible useful correction does not.** Two 600-update recipes on the same source-disjoint natural panel establish finite full-model native optimization and 24/24 valid final completions at the observed lengths. They do not improve aggregate lexical WER over RAW or produce a single useful final case. Recipe01 is lexical identity plus surface changes; recipe02 adds two lexical damages. The criterion is evaluated from generated IDs and literal bound sources/targets, independently of training loss.

The evidence rejects interpreting invalid pretraining output as an unrepaired byte-interface defect or claiming that capacity truncation caused these outcomes: complete admission, EOS/byte/PAD semantics and pinned model identity are checked, and adapted outputs complete validly. The remaining adequacy problem is useful restoration under the disclosed small training regime. These two recipes jointly change prefix and learning rate, so they do **not** causally isolate prompt versus optimization. The artifacts do not distinguish insufficient exposure, training-error diversity, input recoverability or optimizer adequacy. The 521 training errors supply actual correction supervision; their presence alone does not guarantee that this bounded adaptation suffices. No architecture failure, full-context qualification, final recipe freeze or scratch-superiority claim follows.

Both recipes' accounted wall subtotals sum to **876.343s** plus unmeasured cold-load/preparation work; every attempted recipe and every failed/pretrained panel is retained. The observed affordability of these short checks does not establish an affordable useful final comparator. Do not promote a valid copy path to a credible correction baseline or launch further undeclared tuning to manufacture a pass. Further adaptation needs a prospective diagnosis/budget decision within the authorized development boundary. No final/sealed candidate inference, final training, production modification or protocol freeze was performed by this reviewer.

REPAIR_REQUIRED
