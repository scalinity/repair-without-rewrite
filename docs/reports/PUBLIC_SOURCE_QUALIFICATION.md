# Public-source qualification — bounded foundation

**2026-10-05 UTC: PARTIAL; metadata inventory measured, audio populations unqualified.** The development manifest is provisional and candidate independent. It is not a corpus freeze or a PUB-GATE 2/3 pass. No recognizer, learned comparator, training, listening, annotation, access grant, or final inference was used for this inventory.

## Acquired evidence and rights

The [official LibriSpeech-PC release](https://www.openslr.org/145/) supplies text manifests, preserves original LibriSpeech partitions after dropping failed restoration samples, and declares CC BY 4.0. Its README distinguishes normalized restored `text` from unprocessed restored `text_raw`; it contains no audio. Parent audio is separately distributed by [LibriSpeech OpenSLR 12](https://www.openslr.org/12/) under CC BY 4.0. Retain attribution and license notices if later using or distributing derivative data.

The 25,892,530-byte [manifest archive](https://www.openslr.org/resources/145/manifests.tar.gz) was fetched at `2026-10-05T05:02:16.517217+00:00`, HTTP 200. SHA256: `96d4eae2222b29b66437a21959252419bcd4762e5042e71e023790171054d1c0`; archive `LICENSE.txt` SHA256: `039883f832c9c0f816ca974487253bd742cfb04ebd207ee9ef39a49913dbb23f`. These are content revisions, since OpenSLR does not expose a Git revision. Raw archive/pages stay in ignored `exports/source-qualification/`; [public_sources.json](../../experiments/manifests/public_sources.json) records requested URLs, UTC retrievals, HTTP outcomes, sizes and content hashes without reproducing references.

## Actual LibriSpeech-PC inventory

Counts below come from reading all seven released JSONL members, not from a model card or original LibriSpeech population. Durations are manifest values, not decoded-audio measurements. Speaker/chapter counts are per partition; they must not be summed as globally distinct clusters. Book identities remain unknown.

| Official partition | Rows / unique IDs | Speakers | Chapters | `text` differs from `text_raw` | Audio-qualified cases |
|---|---:|---:|---:|---:|---:|
| dev-clean | 2,530 | 39 | 94 | 999 | 0 |
| dev-other | 2,728 | 33 | 89 | 1,210 | 0 |
| test-clean | 2,417 | 39 | 83 | 1,050 | 0 |
| test-other | 2,856 | 33 | 90 | 1,336 | 0 |
| train-clean-100 | 26,041 | 251 | 585 | 14,156 | 0 |
| train-clean-360 | 95,404 | 921 | 2,095 | 50,934 | 0 |
| train-other-500 | 134,679 | 1,159 | 2,771 | 74,771 | 0 |

Total metadata rows: **266,655**. No duplicate stable ID occurs within a partition and no empty `text` occurs. [public_lspc_inventory.json](../../experiments/manifests/public_lspc_inventory.json) preserves member hashes, manifest duration totals, selected training speakers, counts and explicit unknowns. The attempted standalone OpenSLR `CHAPTERS.TXT` URL returned HTTP 404; chapters are not silently treated as books.

The working development field is `text`, marked `PROVISIONAL_NOT_FROZEN`; both field hashes are retained. The design says restored punctuation/capitalization references but does not settle the release's two fields explicitly. Their 144,456 differing rows require a pre-freeze field decision. No field choice is claimed equivalent to raw spoken intent; these are reference-restoration targets, and punctuation/case differences are handled by the specified evaluation views.

## Provisional roles and leakage boundaries

[public_lspc_roles.development.jsonl](../../experiments/manifests/public_lspc_roles.development.jsonl) contains all 10,531 official DEV/test metadata rows plus 311 rows from one whole training speaker per training partition. Training speakers `8014`, `3330`, `1367` were chosen by a source-only SHA256 ranking with development partition seed `120101`; neither hypotheses nor model outcomes entered selection. The seed is a grouping fixture choice, not a final model seed.

Connected speaker/chapter/book identities, available exact audio hashes, long exact reference fingerprints and same-corpus long near-duplicate text are grouped before roles. The declared near rule uses Unicode 15.1 NFC, case folding, Unicode word-regex tokens, five-word shingles, at least 20 words and Jaccard at least 0.90. This is a provisional leakage signature, not `lexical_eval_v1`, a model normalizer, or a claim that short generic sentences imply common provenance. Unknown book/audio identities remain null. Final membership is retained; known relatives are excluded from other roles. DEV membership is retained unless connected to final. Training groups are hash-partitioned into train and reserved calibration.

| Role | Rows | Connected groups represented |
|---|---:|---:|
| train | 202 | 2 |
| HPO development | 5,166 | 71 |
| reserved calibration | 109 | 1 |
| sealed final metadata | 5,273 | 72 |
| excluded known final overlap | 92 | 1 |

The 92 exclusions form one DEV speaker group connected to a final group by long reference overlap. A single group can be represented in both final and excluded role counts. Neither 72 final groups nor 5,273 rows establishes sufficient statistical power. Group closure covers this bounded manifest only: the full 256,124-row training-source near-duplicate sweep, book mapping, educational/tokenizer-corpus overlap and cross-corpus source identities remain pending. Final payload references appear only in the ignored source archive and qualification process; committed role records contain hashes. `require_development_role` rejects final, calibration and excluded records; downstream consumers must call it before using any record for development.

## SLUE-VoxCeleb

The [official ASAPP dataset card](https://huggingface.co/datasets/asapp/slue/blob/67f7da031721a14cc391c7fa7c8d96411282d8a3/README.md) describes normalized transcription, speaker identity and clip start/end seconds; labels were released in January 2024. Its published VoxCeleb counts are 5,777 train, 1,454 validation and 3,553 test. These are **published, not inventoried** counts. The card declares CC BY 4.0 for the subset/transcriptions/times while preserving the original audio owners' copyright notice; these notices must remain in future source records. The [official toolkit](https://github.com/asappresearch/slue-toolkit) documents its ASR subset: excluding 23 Mixed and 104 Disagreement sentiment rows produces 3,426 test rows. The proposed primary population retains sentiment labels unless a separate structural exclusion applies.

At `2026-10-05T05:02:16.950135+00:00`, the public Hub metadata returned revision `67f7da031721a14cc391c7fa7c8d96411282d8a3`, `gated=auto`. The pinned README fetched HTTP 200; pinned `fine-tune.tsv`, `dev.tsv`, `test.tsv`, and VoxCeleb `LICENSE` returned HTTP 401 at 05:03:33 UTC. Access depends on a contact/agreement step. No login, token use, permission grant or contact submission was attempted. Status: **AUTO-GATED ACCESS PENDING; zero locally inventoried rows and zero audio-qualified cases**. No placeholder rows substitute for unavailable TSVs.

On authorized acquisition, stable source IDs and speaker/video connected groups must be established from actual metadata, and the official start/end crop must be applied exactly once. The lexical reference is `normalized_text`; this source supplies no formatted gold. Valid empty references require explicit legitimate designation. Actual video families, reference validity, crop validity, decoding, Parakeet hypotheses, ambiguity and source-error totals remain unknown.

## F03 and decision boundary

The development contract distinguishes missing, null, non-string, invalid UTF-8, documented sentinels, undesignated empty strings, and an explicitly designated legitimate empty reference. A literal `N/A` is not guessed to be a sentinel. Genuine empty references remain scoreable under the canonical accounting rules. The LS-PC adapter does not infer legitimate designation from an empty string. This implements accepted F03 prospectively; neither immutable registry text nor the frozen protocol was changed.

Twenty targeted tests passed in 0.02 seconds: genuine-empty/sentinel distinctions, deterministic grouping, crossed family closure, final overlap exclusion, role barriers, provisional field hashing, and weight-free byte-interface conformance. The [test evidence](../../experiments/manifests/public_data_tests.json) records code identities. Passing fixtures does not qualify source populations.

**Readiness:** metadata and development role tooling are usable provisionally. Public natural H1 remains blocked on audio and reference contracts, all source-error denominators `e_S`, cluster/power and scorer coverage qualification; SLUE also needs authorized gated access. H2 synthetic work can proceed within its own gates. Upstream recognizer, restoration model, ByT5 and Qwen pretraining overlap remains unknown unless independently documented. No contamination assurance follows from this inventory.
