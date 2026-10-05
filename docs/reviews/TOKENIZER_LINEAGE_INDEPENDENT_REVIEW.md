# Tokenizer and data-lineage review

Status: **PASS — ACTUAL DEVELOPMENT ARTIFACT LINEAGE AND INDEPENDENT CONFORMANCE; NOT A PAPER FREEZE**.

This review began independently from baseline `c81d08f95566d1e797f14a6217286e5dfcf33ab5`: the supplied canonical Section 11, registry task/reference contract, released LS-PC README, `src/models/tokenizer.py`, tests and previous reports were examined directly. The reviewer reproduced a strict scalar-type defect before receiving authorization to implement its repair and the incremental trainer. Accordingly, the original findings and oracle comparisons are independent reproductions; the new trainer is reviewer-authored implementation with parity evidence, not an independently reviewed real-corpus freeze. A later artifact/lineage check remains required.

## Exact reversible interface and reproduced defect

The retained map is correct: literal bytes 0–255; 64 reserved IDs 256–319; learned merges beginning at 320; exactly 16,064 learned merges are necessary to reach 16,384 entries. Literal control-looking spellings are encoded as ordinary bytes. Decode concatenates bytes before strict UTF-8 decoding; invalid Unicode input and malformed output fail explicitly. Source boundaries remain byte/code-point maps with a legal-pointer mask. No pretrained tokenizer is imported.

At baseline tokenizer SHA256 `b1dbb553ef9a6c796ed7fcf7c2894f0a30db84decbd3c98d706bed72056727fe`, the following actual calls were accepted:

| Input | Observed behavior |
|---|---|
| `decode([65.0])` | Produced `A` |
| `decode([True])` | Produced literal byte 1 |
| `frame_source(..., task_id=308.0)` | Emitted floating task ID 308.0 |
| `ByteBPE([(97.0,98.0)])` | Accepted float merge symbols and decoded `ab` |
| `digit_isolation="false"` | Enabled digit isolation through truthiness |

Python numeric equality allowed noninteger IDs to alias canonical IDs. The repair validates exact integer types for literal IDs, merge symbols, merge count, trusted task IDs and saved vocabulary size, and exact boolean type for the digit policy. It rejects bool-as-int and floating aliases without changing valid maps, merges or byte semantics.

Repaired tokenizer SHA256: `c6b7452659ae1654ca36d868f33367d17b03df0ad3325b58e993ccaf454d7372`. Regression-test SHA256: `1eaca6f5c6f54475b0e2725a6ba5466fc54b05fba79d17bda0ba64850b52e639`.

An independently constructed fixed-map fixture audit executed **20,000 exact round trips**: 10,000 unique strings, 625 per each of 16 categories, under unrestricted and digit-isolating policies. It found **zero failures and zero unintended reserved IDs**, and rejected nine malformed/unsupported trusted task controls. Categories included prose, digits, versions, CamelCase, snake_case, kebab-case, scientific names, URLs, macOS/Windows-looking paths, flags, commands, percentages/currency, emoji, combining marks and literal control spellings; every string also retained repeated spaces, tabs and CRLF. These were fixture strings and hand-specified merge maps, not released corpus training. Fixture-list SHA256 was `25adc57fd33195695965a78ef1e9368775be19a94cb854570340caf242efdfe0`, with 360,625 test UTF-8 bytes per policy and **zero training bytes**.

The pure tokenizer/edit check passed **67 tests**. After adding optimized-trainer parity coverage, the same pure suite passed **79 tests in 0.14 seconds**. A mistakenly broader first check also executed tiny B/C tensor tests and retained **73 passed / 1 failed**: cache parity maximum difference `0.00044950843` versus `0.00002`. Root independently identified this as the existing default MLX TF32 numerical policy and had already obtained 180 baseline passes with `MLX_ENABLE_TF32=0`. This was not a tokenizer-dependent failure; this review did not alter B/C code, relax its tolerance or rerun an accelerator workload.

## Deterministic optimized training implementation

The original educational trainer rescans and rewrites every sequence at every merge; this is an unsuitable unmeasured default for the full 16,064-merge corpus. The new `src/models/tokenizer_training.py` uses indexed linked nodes, live adjacent-pair occurrence sets and a lazy frequency heap, updating only affected edges. It retains the original rule exactly: count every adjacent occurrence, including overlaps; select highest frequency, with ascending numeric pair as the tie-break; replace left-to-right nonoverlapping occurrences within each document/segment. No implicit normalization, new word boundary, Unicode remapping, pretrained tokenizer, external trainer or new package is used. A pure standard-library implementation avoids silently assuming third-party trainer ties or pretokenization are equivalent.

Parity tests compare complete merge lists and encoding against `ByteBPE.train` on eight adversarial fixture/policy combinations and 60 seeded random fixture/policy combinations. They cover overlapping repetitions, count ties, document-boundary isolation, digit policy, emoji/combining bytes, whitespace, literal controls, input-order reversal, streaming input, exhaustion and invalid scalar configuration. The educational trainer remains available as a distinct small-corpus oracle.

Trainer SHA256: `dc19057f15512d884a594f6a4c6b8152fba0c92df907df496a7978d577fe7805`. Trainer-test SHA256: `4644a88b6ca3d2298e2de6597df0bfa0bf74ab91141e7d280d037e80162b76eb`.

`train_development_byte_bpe` returns a tokenizer and deterministic receipt containing training-manifest SHA256, exact trainer/tokenizer implementation hashes, complete configuration, ordered length-prefixed UTF-8 corpus-content hash, document/content counts, training bytes, reserved-map and merge-list canonical hashes, and vocabulary size. It explicitly states that the manifest hash **does not establish admission**. The caller must verify eligible train roles before supplying documents, record source IDs/component counts and exact saved artifact-byte hashes, and preserve a separate freeze receipt. Input ordering affects the ordered-corpus receipt; pair selection and learned merges are invariant to document permutation.

At the initial interface-review stage no full corpus run or 16,064-merge artifact existed. The actual artifact was subsequently trained by root and independently checked below. No MODEL-0 V6 result or paper-tokenizer freeze is claimed by this review. Source-qualified train rows are the sole permitted real input; HPO, calibration, excluded and sealed-final rows remain outside merge fitting. Admitted text alone may support tokenizer fitting; audio/ASR qualification is a separate dependency for natural restoration pairs. `ByteBPE.save` still embeds `DEVELOPMENT_NOT_FROZEN`; root's separate hash-bound receipt explicitly defines the DEVELOPMENT freeze while retaining that historical embedded label. Source framing must travel with tokenizer/manifest identity in the qualified reader/run records.

## Prospective DEVELOPMENT reference recommendation

The official [LS-PC release](https://www.openslr.org/145/) is a restoration of punctuation and capitalization. Its acquired official archive SHA256 is `96d4eae2222b29b66437a21959252419bcd4762e5042e71e023790171054d1c0`; the directly inspected `README.txt` member SHA256 is `858f0f727a709100928e8a527398b437ece62bad78cbed3169050e65643903c5`. It distinguishes ASR-training-normalized `text` from restored `text_raw` without that preprocessing. The [authors' paper, Section 5](https://arxiv.org/pdf/2310.02943) describes retaining only period/comma/question-mark punctuation, inserting punctuation spaces and collapsing whitespace for ASR training.

The defensible smallest policy for this project's `restore_reference` task is: **train on unchanged `text_raw` and designate it as the DEVELOPMENT full-written reference; apply the unchanged `lexical_eval_v1` only for lexical scores; use the original bytes for surface diagnostics**. Preserve `text` and its hash as a separately named official processed-ASR secondary view. Removed apostrophes/hyphens can change lexical tokens under the specified scorer, so the two fields must not be assumed lexically interchangeable or silently selected by score. This is a task-semantics inference, not an assertion that the release uniquely mandates our policy or that raw restored text has been independently acoustically verified.

SLUE retains its released `normalized_text` under the same lexical scorer, with no formatted-gold claim. LS-PC surface diagnostics remain domain-specific. The unknown second-domain supply does not license reweighting the fixed equal-domain endpoint. Root accepted this prospective development recommendation before fitting and owns the amendment record; immutable supplied contracts and final paper protocol remain unchanged.

## Actual trained-artifact independent reproduction

Root completed `development-tokenizer-attempt02` after corpus admission. Attempt01 failed on an explicit schema join before manifest creation or fitting; its `failure.txt` remains preserved. The reviewer did **not** rerun fitting or execute an accelerator workload. At `2026-10-05T08:54:46.542383+00:00`, independent code reconstructed the train-only corpus directly from the official archive's three training members, checked all role/manifest joins, and verified the saved artifact and independently expanded merge byte strings. No DEV/test payload member was read.

| Independently reproduced property | Result |
|---|---:|
| Distinct admitted train IDs / documents | 45,729 |
| Distinct raw document contents | 45,716 |
| Train source components | 314 |
| Actual unchanged `text_raw` UTF-8 bytes | 8,423,028 |
| HPO/calibration/excluded/final IDs in corpus | 0 |
| Corpus components shared with held-out roles | 0 |
| Either-field literal train/final reference-hash intersections | 0 |
| Base bytes / reserved IDs / learned merges | 256 / 64 / 16,064 |
| Total vocabulary | 16,384 |
| Independent merge-expansion byte-map mismatch | 0 |
| New actual-trained-map adversarial round trips | 10,000 |
| Round-trip failures / unintended reserved IDs | 0 / 0 |
| Invalid trusted controls / malformed decodes rejected | 10 / 7 |
| Invalid Unicode surrogate input | Rejected |

Every admitted ID was found exactly once in the training archive, both released-field hashes matched its role record, and every corpus entry's `text_raw` hash, byte count and component matched. Corpus IDs were exactly the complete sorted admitted train-ID set. Current role manifests, full ignored role manifest and corpus manifest matched their bound identities; the exact ordered length-prefixed corpus hash reproduced the trainer receipt. The trained-map adversarial audit reused the independent 16-category fixture-list identity recorded above, distinct from the root runner's randomly generated audit. It additionally checked legal code-point pointer masks, offsets and raw source hashes against direct calculations. It completed in 0.388065 seconds, a CPU tokenizer conformance measurement, not model throughput.

| Bound artifact | Independently verified SHA256 |
|---|---|
| `configs/tokenizer_development/tokenizer.json` | `b125551f3c3627edc9cb8d325bc70bfd8340df1518f03d0fd16d140ff7ace6ca` |
| `configs/tokenizer_development/special_tokens.json` | `db75b2bec29e695e7843ac530fbe2dec4a5be128c713fe3186ea2e4d6efa03e2` |
| `development_tokenizer_corpus.attempt01.jsonl` | `db1b58fb43da32cded6dc58c7c2ad9dd2d2595e5e6b03b1935b4a4616f8db10a` |
| Qualified source-role manifest | `56c5889d952c83120267ea92b4aaf8bcec63dff61a34e83ce531c9be97b3eb98` |
| Ordered length-prefixed corpus content | `894e1dcd4876ac5f66066f080bdfe35b42246a772098b713412fe180b3917a60` |
| Canonical learned-merge list | `80b7a0eb48016a4b35dbed110b04193d142aa5a320254d0d04c3afad05147fb3` |

The actual trainer/tokenizer/runner code hashes matched the launch and receipt; full merge fitting took 18.702986 seconds according to the preserved root receipt. That elapsed time was inspected, not independently rerun. Digit isolation is explicitly false. The separate receipt states `QUALIFIED_DEVELOPMENT_TOKENIZER_FROZEN_BY_HASH_NOT_PAPER_FREEZE`; its scope does not freeze `paper_protocol_v2`, select a final tokenizer, qualify source-hypothesis construction, or admit the six B/C probes.

## Historical qualification-receipt discrepancy and verified reconciliation

One exact lineage assertion failed and was reported immediately: tokenizer launch/receipt binds supply-qualification SHA256 `5a79189acf9f300a82f39545189ec74885244f8e8d528ccb7e1597a5cef75853`, but the mutable working summary initially hashed `25156f4954bcfe1e550be376b15b3128004d8a5571e7aea1cd4127e9eebfc3cf` and later `d0b1de70c2d2a7c7bbc7ad711a4d771fa91a22ef399651b0482aaeeee7616842` during review. The role manifest, corpus, ignored full-role manifest and all artifact/code bindings remained stable and independently matched. Full lineage PASS was withheld until this was resolved; the failed assertion remains documented here.

Root subsequently preserved `exports/training-supply-qualification-attempt02/tokenizer_launch_bound_qualification.json`. Independent hashing reproduced **exactly** the launch-bound `5a79189a…f75853` identity. The corresponding `tokenizer_launch_bound_training_supply.py` independently reproduced its bound code SHA256 `be2db61d4fe0fa387eb02e8d3fec9bd44374f6e312f371adb5ac98030ddb620f`.

An independent recursive comparison of every original JSON leaf found only two changed original values in the enriched current summary: `code_sha256` and `elapsed_seconds`. No original role subfield, eligibility rule, component membership, archive/member hash, ID/hash binding or raw-field policy changed. Added fields provide independent-verification receipts, explicit decisions and deduplicated-volume counts. Independently diffing the preserved/current data modules confirmed that the sole code change adds distinct-raw-target volume reporting after role assignment. The retained `tokenizer_launch_to_enriched_qualification_semantic_diff.json` records the reconciliation; its substantive claim was reproduced rather than merely trusted. Original tokenizer launch/receipt bytes and hashes were not edited. **Exact historical supply-summary lineage is now closed.**

## Review decision and boundary

The real artifact's consistent `text_raw` policy, complete train-only source-ID/content binding, 16,384 arithmetic, exact saved loading, adversarial round trips, historical supply-summary binding and separate DEVELOPMENT freeze identity have now been reproduced. No merge-fitting input or model-selection result used sealed-final payloads or candidate-dependent eligibility in the checked path. Unrestricted merging is the operative DEVELOPMENT digit policy; these checks do not select its final scientific efficiency tradeoff. No final/sealed candidate inference, final protocol freeze or B/C model-training admission is implied.
