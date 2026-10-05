# Independent B/C contract review

Reviewer responsibility: MODEL-0/shared mathematical-core owner reviewing the separately implemented B/C modules. The reviewer did not implement `bc.py` or `edits.py`. This review is independent for B/C arrangement, event/renderer mechanics and the rehearsal script; it is **not** an independent review of the reviewer's shared core implementation.

Scope: canonical v1.2 Sections 8–11, 17–19; `src/models/bc.py`, `src/models/edits.py`, `tests/models/test_bc.py`, `tests/models/test_edits.py`, and the original `stress_bc_exact_overfit_development/run.py`/results. Static inspection and one CPU-only API-contract reproducer were performed. No accelerator workloads ran during this review.

## Finding P2 — bind the encoded content and pointer map to the exact source

At the reviewed `C101.greedy_edits` entry point, `source`, `source_ids`, `encoder_positions`, `byte_offsets` and `legal` are separate arguments. The only initial relationship checked is the lengths of `byte_offsets` and `encoder_positions`. The emitted `EditProgram` then obtains a newly computed hash from `source_identity(source)`. Consequently, the renderer's correct source-hash check cannot detect that the model encoded a different source or that a caller supplied a stale token/byte map.

Concrete CPU-only reproducer: source `a`, encoded source `[[308,259,98]]` (content byte `b`), encoder positions `(1,2)`, byte offsets `(0,1)`, legal mask `[True,True]`, and a fixed END action. The current API returns `status=completed`, output `a`, and the SHA-256 hash for `a`, despite encoding `b`. This uses no trained model, stochastic decision or GPU operation; it tests whether the boundary assertion exists.

The reproducer used `mx.set_default_device(mx.cpu)` and a fake object with `config.max_context=16`, zero embeddings/states, `encode`/`decode` returning zeros, and `action_logits` returning `[0,1,0]`. It invoked the real `C101.greedy_edits` method. The observed result was:

```text
Device(cpu, 0)
source bytes: b'a'; encoded content byte: b'b'
status: completed; output: 'a'; decoder_positions: 1
program.source_sha256:
ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb
```

Required repair: bind these fields before encoding/generation. A suitable direct check reconstructs each content token's bytes from `source_ids` at the preceding-token positions `encoder_positions[1:]`, requires their concatenation to equal the exact supplied source bytes, verifies cumulative byte offsets, ordered/content-only encoder positions, and the legal UTF-8 mask including first/terminal boundaries. A single validated tokenized-source object is another possible interface. Keep malformed-source/map failures explicit.

This finding **does not explain** the observed overfit failures: the four recorded rehearsal examples supply consistent source/maps. It is a separate stale-input/offset invariant gap. It was sent to the B/C owner and root for repair. The finding remains open until the implementation and regression evidence are reviewed.

## Contracts that match the specification on static review

- B supervision uses decoder inputs `[BOS,*target_bytes]` and targets `[*target_bytes,EOS]`; EOS is supervised, not treated as an input target at the same position. The whole-update B valid-target denominator includes each EOS once. Greedy B begins with BOS and uses one-token self/cache plus reused cross K/V, stopping on EOS or retaining a capped valid prefix.
- Encoder/source information is used through the bidirectional shared encoder and each decoder's cross-attention. There is no RoPE on cross-attention. Valid-source masks reach encoder attention and decoder cross-attention. Teacher forcing does not add reference information to the source tensor; it supplies only gold preceding events required by the supervised contract.
- C boundary features use the source-start separator for the first boundary and the immediately preceding content-token state thereafter. Four separate width-128 pointer projections plus the three-way affine classifier are present. Default leaf-count tests enumerate the intended 100,686,336 / 101,081,859 totals.
- Start pointers are masked below the preceding edit's end. Conditional end pointers are masked below the selected start. Legal UTF-8 token boundaries are masked separately. This enforces order and `end>=start` when the supplied map is valid.
- Event teacher forcing and greedy decoding use exactly one BOS. EDIT/start share the current state; start feedback is EDIT embedding plus selected boundary; end feedback is END-EDIT embedding plus selected end feature; ordinary replacements and the END-EDIT delimiter each append an input. Terminal END/ABSTAIN append none. `1+R+3K`, `R+K`, `K`, `K`, `K+1` match the code.
- END-EDIT is included in C's vocabulary loss and denominator. An empty replacement still trains its delimiter; identity trains only END. The shared whole-update component denominators are precomputed before microsteps. Each microbatch differentiates component sum/whole-component count, accumulates once in FP32, and uses `already_normalized=True`, followed by one clip/AdamW step. No additional shared-token division was found.
- The renderer validates full grammar, source hash/length, original byte coordinates, UTF-8/BPE boundaries and ordered/non-overlapping edits before copying. It uses original source coordinates, including repeated literal occurrences. Invalid/capped/ABSTAIN programs are not turned into invented successful output prefixes.
- Canonical labels use a deterministic leftmost scalar-value minimum-edit decomposition and legal-boundary expansion/merging. The existing exhaustive and seeded Unicode tests cover exact reconstruction. This review found no concrete mismatch in the decomposition/renderer logic.

## Test and learning interpretation

The B/C numerical test suite uses 16-wide one/one-layer fixtures; its six recorded passing tests establish reduced-geometry mask/cache/feedback/gradient mechanics, while its exact default leaf inventory establishes counts. It does not by itself qualify exact-geometry gradients, cache equivalence or learning. The original exact rehearsal does exercise the complete default architectures.

The original same-four-pair 80-update rehearsal at constant LR 0.003 failed its completed exact-output condition: B 0/4, C 3/4; C had a finite loss spike to 174.322085. B's EOS supervision, target shift and denominator are correct on review. No silent bug in C's event shift or component-normalization path was identified. These observations leave optimization at that LR as a live explanation; they do not prove that lowering LR will repair it, that the architectures cannot learn, or that a loss decrease establishes useful correction.

Retain those failed artifacts. A separately identified matched lower-LR rehearsal may test optimization after source-binding repair and exact-geometry diagnostics. Its result must remain a bounded toy qualification, not a substitute for held-out source-dependent correction or a 10M development probe. BENCH-00, tokenizer/data qualification and final/publication gates remain separate.


## Repair follow-up — BC-R01 closed for the input-boundary defect

At 2026-10-05 05:39 UTC the repaired `bc.py` had SHA-256 `d58022e956b3adbd8d6a1c635ef9a7774efbd83aa5f8d8d65643c8f2d53be067`. The historical finding and failing reproducer above are preserved. Their references to the “current API” describe the pre-repair snapshot, not this repaired version.

The new pure-Python `validate_source_binding` runs before `encode`. It requires the designated source-start separator, a complete contiguous content-position map, the trusted restore-reference prefix (with optional BOS), and only EOS/PAD after the mapped content. It reconstructs literal bytes from every mapped content token and requires exact equality with the supplied source's UTF-8 bytes. It checks cumulative offsets beginning at zero and ending at the exact source length, and requires the legal mask to equal the UTF-8 codepoint-boundary predicate. `greedy_edits` additionally requires any supplied source-validity mask to have matching shape, Boolean dtype, and all mapped source-start/content positions enabled.

Independent verification used the selected pure regression test only: `MLX_ENABLE_TF32=0 .venv/bin/python -m pytest tests/models/test_bc.py -k source_binding -q` returned **1 passed, 6 deselected in 0.08 s**. Its fake `NeverEncode` object makes any attempt to encode the original mismatched source fail the test. No MLX array, model construction or forward operation is performed by this selected test. Additional independent pure-object calls rejected masked content, masked source-start, wrong mask shape/dtype, a different task prefix, a false initial legal boundary and a missing terminal offset. The valid optional-BOS/EOS/PAD framing was accepted. These calls also used a `NeverEncode` object and performed zero MLX array/forward operations.

**Disposition:** the concrete stale-source/map defect is closed by static review and the pure entry-point regression. This does not establish that every possible malformed Python object produces the same exception class, or substitute for accelerator numerical regression. The owner's earlier pure evidence is retained in `docs/reports/raw/bc_source_binding_pure_attempt03.txt` and `bc_source_binding_review.json`; its recorded source hash identifies an earlier repair snapshot, while this independent review identifies the later inspected snapshot above. The combined seven-test numerical suite remains pending the benchmark accelerator release at this review time.

The separately recorded lower-LR matched exact rehearsal reportedly completed B 4/4 and C 4/4 at LR 0.0003. The historical LR 0.003 failures remain relevant and must remain on disk. No held-out/source-dependent natural correction or final-study qualification follows from four trained toy pairs. The original fixtures' source bindings were also checked under the repaired contract by the owner; that supports the interpretation that BC-R01 did not cause the historical optimization failures.
