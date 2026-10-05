# Independent public-audio barrier review

Reviewed 2026-10-05 UTC at HEAD `6f51470f30420ef7caa04ba0eb46f56f04c4ce73`. Read-only implementation review of `benchmarks/asr_tts_native_probe.py`, `src/data/public_inventory.py`, the source-role contracts, focused fixtures, and current pinned input artifacts. No implementation or dependency was changed; no audio decoding, listening, MLX/Torch import, model loading or inference occurred in this review.

**Disposition: PASS for the current pinned 12-case public development panel. No blocking defect was found in its CLI admission path or full official-parent closure.** This qualifies the stated source barrier, not recognizer accuracy, reference policy, acoustic truth, broader training supply or final freeze.

## Full parent closure

`chapter_families` reads every non-comment chapter in the supplied official CHAPTERS.TXT before selecting text rows. Its union graph uses typed speaker, project and book identities, so a training chapter absent from the bounded text inventory can still connect a development chapter to a final chapter. Component identities are hashes of all sorted chapter IDs in that component. Titles do not define identity and are not copied into roles. The role builder then groups by this component as well as the source families and text leakage rules; final membership takes precedence and its non-final relatives are excluded.

An independent breadth-first traversal of the actual complete chapter graph reproduced all **392 component hashes across 5,831 chapters**. All **10,842 current role rows** matched official speaker/book/project/component identities and the metadata hash. Every current HPO-development row was disjoint from components containing **any official test-clean/test-other chapter**, including chapters beyond the selected training-speaker subset. This check used metadata and returned role hashes, without reading sealed reference payloads or final audio.

Focused existing CPU tests passed: **5 passed, 20 deselected in 0.08 seconds**, using `.venv/bin/python -m pytest tests/data/test_contracts.py -q -k 'official or actual_attempt02 or training_parent'`. They include the unselected-training-chapter bridge, malformed/duplicate chapter rejection, actual final-family separation, and the distinction between potential parent-only training supply and qualified training roles.

## Current input binding

The CLI calls `validate_asr_source_barrier` before importing model runtimes or creating the output directory. It verifies the pinned role and audio manifest hashes, rejects duplicate role IDs, and joins each clip's upstream recording stem to an HPO-development LibriSpeech-PC row. It requires complete speaker/chapter/book/project/component identities, the same upstream path and official development split, matching speaker/chapter, both exact PC text hashes, the local audio-file hash, and distinct selected groups/speakers. Present selection role/group/family declarations must agree. The joined source receipt is saved before model loading.

The actual pure barrier passed **12 cases against target quota 20**. Independently, the selected local file bytes were compared with their exact `LibriSpeech/<audio_filepath>` members in the original dev-clean/dev-other archives: **12/12 equal**. Both complete archive SHA-256 values matched the pinned acquisition manifest. Thus the actual bytes entering this panel are development archive recordings assigned to final-disjoint parent components; the original withdrawn selection does not enter this panel. No model output selected or replaced a source in this review.

The runtime validator consumes an independently qualified role manifest; it does not independently rebuild closure or establish archive membership. The current row audio hashes are pending at the metadata-role stage, so archive-member provenance comes from the acquisition artifact and the independent byte comparison above, while runtime audio hashes detect later byte changes. Arbitrarily repinning a mislabeled audio/role manifest would require a new source qualification. Optional absent selection declarations are derived from the matched role row; the current pinned panel contains them explicitly. The internal `parakeet` helper is not a separate admission API: direct calls bypass the full CLI join and must not be used as a new qualified route.

## Failure and output semantics

Role/hash/reference/source failures at admission propagate before model import as a nonzero process exit. Import/load/device failures after provenance setup produce `FAILED_LOAD_OR_RUNTIME` with exception/traceback and a nonzero exit. A transcription exception produces a retained per-call `FAILED` row with `hypothesis=null`; any such row makes the arm `PARTIAL_FAILURE` and exits nonzero. Successful calls retain the untouched library text and alignment data. `COMPLETED` denotes returned inference, not correct recognition; an empty recognized string remains a raw hypothesis for source-error scoring.

Each clip is rehashed immediately before transcription. A changed file, invalid duration or audio-info exception at this stage aborts the arm through its explicit failure summary. Such pre-call failures do not receive a separate failed-call row; already written calls remain, so that arm must not be presented as a complete panel. Microprobe repeats are separately identified and their audio/time are charged in the complete attempted-work accounting. Neither a returned hypothesis nor the barrier's PASS freezes the competing PC reference policies or establishes adequate error support.

Complete training-source near-duplicate qualification and external/tokenizer contamination remain pending. Parent-only training bounds are explicitly potential supply, with no audio qualification or training-role assignment. This review found no basis to strengthen those claims.

## Reviewed identities

```json
{
  "benchmarks/asr_tts_native_probe.py": "a9d89a6451efdc0214d80c1f4f908b5c99a4a8ecd7af1941927f349ee2b3a7c0",
  "src/data/public_inventory.py": "34a99a91043e7f5c5ef0077421593c1cfa47de403fe1f7817b17d4affd82032c",
  "official_CHAPTERS.TXT": "2e9db25c250a143b031ca003180acfce84b364e31fbc79250e306303e6f25306",
  "public_lspc_roles.development.attempt02.jsonl": "d579d1c6d2e3b0bb2dcc48613ac0c448414ceb998ae6a098c9cabe21fa4fa159",
  "manifest.book_closed.attempt03.json": "63b130e821d68af89db2b25b864217afb5e70aa921b3d9cc5b31e76693663159",
  "dev-clean.tar.gz": "76f87d090650617fca0cac8f88b9416e0ebf80350acb97b343a85fa903728ab3",
  "dev-other.tar.gz": "12661c48e8c3fe1de2c1caa4c3e135193bfb1811584f11f569dd12645aa84365"
}
```
