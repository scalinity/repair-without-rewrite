# Development tokenizer qualification

Status: **QUALIFIED_DEVELOPMENT_TOKENIZER_FROZEN_BY_HASH_NOT_PAPER_FREEZE**.

The specified reversible byte BPE was trained on admitted **train-role LS-PC `text_raw` only** and independently verified against the source archive, source-role manifest and saved artifact. It contains **16,384 entries: 256 literal bytes + 64 reserved IDs + 16,064 learned merges**. No HPO, calibration, excluded or sealed-final ID entered fitting. This closes the DEVELOPMENT tokenizer prerequisite; it does not authorize the B/C probe grid or freeze the paper protocol.

## Permitted corpus and reference semantics

The prospective development amendment designates unchanged released `text_raw` as the full-written `restore_reference` target. The processed `text` and both hashes remain available as separately identified source views. The [official release](https://www.openslr.org/145/) and [authors' paper, Section 5](https://arxiv.org/pdf/2310.02943) distinguish restored text from ASR-oriented punctuation/whitespace preprocessing. Lexical evaluation remains the separate `lexical_eval_v1` operation; it never replaces training bytes. SLUE retains released `normalized_text` and no formatted-gold claim; its unavailable supply does not reweight the equal-domain endpoint.

| Independently verified training quantity | Value |
|---|---:|
| Unique source IDs / documents | 45,729 |
| Unique raw document contents | 45,716 |
| Source components | 314 |
| Speakers / books / projects | 420 / 413 / 421 |
| Training UTF-8 bytes, including repeated document contents | 8,423,028 |
| Admitted corpus IDs outside train role | 0 |
| Component intersections with calibration/HPO/final | 0 |
| Either-field literal train/final reference-hash intersections | 0 |

`experiments/manifests/development_tokenizer_corpus.attempt01.jsonl` is the hash-only fitting-corpus manifest. Its IDs exactly equal the complete sorted admitted train-ID set. Independent source reconstruction found every ID exactly once in the three official training members, checked both released-field hashes, and matched every corpus entry's raw hash, byte length and component. No DEV/test payload member was read by the fitting runner or this artifact-verification pass. Text admission supports this tokenizer fit; it does not qualify train audio or recognizer hypotheses.

| Corpus/qualification identity | SHA256 |
|---|---|
| Official source archive | `96d4eae2222b29b66437a21959252419bcd4762e5042e71e023790171054d1c0` |
| Qualified source-role manifest | `56c5889d952c83120267ea92b4aaf8bcec63dff61a34e83ce531c9be97b3eb98` |
| Fitting-corpus manifest | `db1b58fb43da32cded6dc58c7c2ad9dd2d2595e5e6b03b1935b4a4616f8db10a` |
| Ordered length-prefixed UTF-8 corpus bytes | `894e1dcd4876ac5f66066f080bdfe35b42246a772098b713412fe180b3917a60` |
| Exact launch-bound supply qualification | `5a79189acf9f300a82f39545189ec74885244f8e8d528ccb7e1597a5cef75853` |

The mutable supply summary gained independent-audit/deduplicated-volume reporting after launch. Its launch-bound original bytes and code are preserved under `exports/training-supply-qualification-attempt02/tokenizer_launch_bound_qualification.json` and `tokenizer_launch_bound_training_supply.py`. Independent hashing and recursive semantic comparison verified the exact historical binding and unchanged admission/grouping/source identities. The original tokenizer launch/receipt remain unchanged; the initially failed hash assertion and subsequent verified reconciliation are recorded in `docs/reviews/TOKENIZER_LINEAGE_INDEPENDENT_REVIEW.md`.

## Trainer configuration and saved identity

The standard-library incremental trainer retains the educational trainer's exact pair-count, tie and replacement rules. It updates live linked occurrences without rescanning the entire corpus at each merge. Small fixture parity covers complete merge lists/encodings, ties, overlapping repeats, document boundaries, Unicode, digit segmentation and document reordering. No pretrained tokenizer or new tokenizer package supplies merges.

| Configuration | Value |
|---|---|
| Trainer | `incremental_linked_occurrences_v1` |
| Requested/learned merges | 16,064 / 16,064 |
| Encoding / normalization | Strict UTF-8 / none |
| Document boundaries | Never merge across documents |
| Pair frequency | All adjacent occurrences, including overlaps |
| Merge tie policy | Highest count, then ascending numeric pair |
| Replacement policy | Left-to-right, nonoverlapping |
| Random seed | None; trainer has no randomness |
| Input ordering | Stable source-ID sort; length-prefixed bytes bind exact order |
| Digit isolation | `false`, unrestricted DEVELOPMENT merges |

Unrestricted merging is the operative development configuration, not a final digit-policy efficiency selection. Final tokenizer selection and PUB-GATE 3 remain pending.

| Implementation/artifact | SHA256 |
|---|---|
| `src/models/tokenizer.py` | `c6b7452659ae1654ca36d868f33367d17b03df0ad3325b58e993ccaf454d7372` |
| `src/models/tokenizer_training.py` | `dc19057f15512d884a594f6a4c6b8152fba0c92df907df496a7978d577fe7805` |
| Fitting/qualification runner | `037d2382d2d76857a55cb079faa5b74f7b56d8fe6a1dada85040596272613161` |
| `configs/tokenizer_development/tokenizer.json` | `b125551f3c3627edc9cb8d325bc70bfd8340df1518f03d0fd16d140ff7ace6ca` |
| `configs/tokenizer_development/special_tokens.json` | `db75b2bec29e695e7843ac530fbe2dec4a5be128c713fe3186ea2e4d6efa03e2` |
| Canonical merge list | `80b7a0eb48016a4b35dbed110b04193d142aa5a320254d0d04c3afad05147fb3` |
| Canonical reserved-ID map | `2ead86e69e75b28be3563a3313c4e29b88fdd772410c5a4b2d42f767f2f46f58` |

The saved `special_tokens.json` contains the complete retained numeric map: bytes 0–255; controls/reserved 256–319, including `restore_reference=308`; merge symbols 320–16,383. Independent expansion of every merge reproduced the entire saved literal-byte map. Artifact loading validates the map and reserved allocation. Literal control-looking strings never allocate reserved IDs; only the trusted serializer can insert the allowed task controls. Exact integer/boolean validation rejects floating and boolean ID aliases and malformed configuration.

## Attempts, conformance and development freeze

Attempt01 failed on the runner's previous-schema field join **before manifest creation or fitting**. `exports/foundation-repair/development-tokenizer-attempt01/failure.txt` preserves that outcome. Attempt02 completed 16,064 merges in **18.702986 seconds**, as recorded in its preserved root receipt; the reviewer inspected that time and did not repeat fitting.

The root runner reloaded the actual saved tokenizer and passed **10,000 round trips**, zero unintended reserved IDs and six invalid task-control rejections. An independent verification passed **another 10,000 actual-trained-map round trips** over 16 categories, including combining marks, emoji sequences, paths, URLs, flags, snake_case, CamelCase, repeated spaces, tabs, CRLF and literal task/sentinel spellings. It independently checked concatenated-byte decoding, source hashes, offsets and legal code-point boundaries. Ten malformed/unsupported trusted task IDs, seven malformed/control literal decodes and an invalid Unicode surrogate were rejected. Its fixture-list SHA256 was `25adc57fd33195695965a78ef1e9368775be19a94cb854570340caf242efdfe0`; failures and unintended reserved IDs were both **zero**. The pure tokenizer/edit/parity regression suite passed **79 tests**.

`exports/foundation-repair/development-tokenizer-attempt02/launch.json` captures HEAD, dirty state/diff, exact code/corpus/source identities and input ordering. Its separate `receipt.json` records the trainer configuration, corpus counts/hashes, learned-map identities, saved artifact hashes and conformance results. **That receipt freezes these exact bytes for DEVELOPMENT by hash.** The artifact schema retains its historical embedded `DEVELOPMENT_NOT_FROZEN` label; the external receipt explicitly defines the development freeze without editing or misrepresenting that embedded state. Neither file claims a paper-tokenizer freeze.

No final/sealed candidate output was seen in this branch. No final protocol, digit-policy scientific selection or paper tokenizer was frozen. No private LocalFlow data, model weights or gated SLUE payload contributed to fitting. ASR source qualification, real-shard/model gates, representative native calibration and B/C probe admission remain separate.

**QUALIFIED_DEVELOPMENT_TOKENIZER_FROZEN_BY_HASH_NOT_PAPER_FREEZE**
