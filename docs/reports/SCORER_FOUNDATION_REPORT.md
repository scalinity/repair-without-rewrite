# Scorer foundation report

**Development arithmetic qualification: PASS in the tested scope. Natural-population and publication qualification: incomplete.**

MEASURED RESULT: The required unimplemented fixture run produced 21 failures with `NotImplementedError`; the implemented run passed all 21 fixtures. Both [red](scorer_fixture_red.txt) and [green](scorer_fixture_green.txt) receipts remain intact. Qualification attempts 01–05 preserve subsequent changes and test counts. The latest complete suite has 56 tests; its exact elapsed time and slowest checks are in [attempt05](scorer_qualification_attempt05.txt). No publication gate is claimed passed.

| Contract | Status | Evidence |
|---|---|---|
| Exact unit Levenshtein and optimal pair lattices | PASS | Independent suffix distance/all-path oracle; 225 binary pairs, length 0–3 |
| Compatible triple objective and every conditional-optimum tie | PASS | All 3,375 binary R/S/O triples, length 0–3, against complete seven-move path enumeration |
| Repair/introduction extrema and raw conservation | PASS | Exhaustive parity and 10,000 fixed-seed dense-DP trials; both extrema satisfy repair − introduced = eS − eO |
| Source occurrence/gap consensus and fixed-subset extrema | PASS | Separate reviewer enumerated 225 pairs and 343 triples, using neither optimized nor existing oracle alignment code |
| Source-defined eligibility and integrity | PASS | Source masks fixed before output; full preflight hash seals bytes, tokens, masks, cached lattice and raw offsets; candidate alteration/tampering tests |
| Empty references, fixed denominators and failed calls | PASS | Legitimate empty differs from missing/null/sentinel; insertion numerators retained; all-zero denominators undefined |
| Invalid/missing/abstained C, malformed UTF-8 and valid capped prefix | PASS | Failure rows retained; raw observation and completion-gated repair exported separately |
| Unicode 15.1 policy and raw provenance | PASS | Official 19,074-row NFC conformance; pinned full default case folding, scanner, quotes, hyphens, symbols and controls |
| Metamorphic/serialization checks | PASS | Duplication/order invariance, isolated repair/damage, renaming/reversal and JSON round trips |
| 500 preselected development triples | PASS, synthetic DEV | Manifest-bound triples, maximum actual length 12, compared with independent dense lexicographic DP |
| Equal-domain primary aggregation | PASS | Fixed 0.5/0.5 weights with exact rational ledgers; unavailable domain cannot be dropped or reweighted; pooled ratios labelled secondary |
| Independent review | PASS for reviewed arithmetic | [Review and preserved resolved finding](../reviews/SCORER_INDEPENDENT_REVIEW.md) |
| Natural literal extraction and full population schema/statistics | NOT QUALIFIED | No natural literal denominators, typed anchor matching, paired cluster uncertainty or sealed upstream identities yet |
| Actual natural alignment coverage and H1 identification | NOT MEASURED | No qualified ASR/reference development population has been generated |

The tiny oracle enumerates complete paths and never calls optimized alignment code. The larger development oracle uses a dense lexicographic prefix recurrence; the scorer instead traverses independently built pair lattices and a conditional joint DAG. The canonical cyclic a/b/c example has conditional S/O cost 4 although unrestricted pair distance is 2, with repair/introduction 2 each. Completion-gated repair intentionally does not satisfy raw conservation on failed calls.

Two implementation discrepancies were repaired without deleting failed evidence. Self-review found that an unavailable pre-output R/S lattice could be rematerialized during candidate scoring; an explicit unavailable sentinel now preserves fixed source eligibility. Independent review found that joint-budget exits widened even proved total identities: O=S must retain [0,0], O=R must retain repair=eS and introduced=0, and S=R must retain repair=0 and introduced=eO. All cap exits now preserve those totals while leaving unavailable local correspondence unavailable. Separate provenance and equal-domain checks close the review's additional integrity/aggregation concerns.

MEASURED RESULT: [Synthetic computational profile](../../experiments/scorer-profile-attempt01/summary.json) processed 502 cases in 3.703143 seconds, or 135.561 cases/s including JSON export and Python allocation tracing. Every joint computation finished under its declared budgets: 0/502 caps, 501/502 point-identified raw count results, 1/502 sharp count interval, 27/502 local ambiguities, maximum repair interval width 1. Maximum graph size was 23,969 states and 91,520 edges; maximum attempted moves 167,783. Python traced peak was 39,117,567 bytes and process peak RSS 97,222,656 bytes. These views overlap and must not be added. Parallel coding/correctness may have affected this CPU measurement. This historical profile retains its captured commit/dirty identity; later repairs do not retroactively change its code provenance.

The profile contains 500 manifest-selected synthetic cases plus two alignment stress cases. Its 100% finished-joint rate and narrow widths do not estimate natural H1 coverage or precision. No final data was consumed, no manual ambiguity rescue occurred, and no favorable cap/failure row was removed.

FACT: `unicodedata2==15.1.0` is pinned. Backend binary identity and official CaseFolding/PropList hashes contribute to policy identity; official tables and the [Unicode license](https://www.unicode.org/license.txt) are preserved. Decomposition, reordering, composition and case-fold expansion retain original scalar/byte provenance. Shared or noncontiguous raw spans remain explicitly unavailable. Normalization is not semantic equivalence.

INFERENCE: `reference_triple_v1` is suitable for bounded development arithmetic in this scope. A natural-population claim still requires source/reference policy approval, raw pinned recognizer hypotheses, an output-blind development parity/runtime inventory, literal eligibility and cluster-aware analysis. Unknown manifest fields remain null with an explicit qualification status.

Current reviewed identities:

- `src/scoring/oracle.py`: `c8cc04e5c21ebfc20912c498f95887ca88fae32b79cafe96b493796dea3f7609`
- `src/scoring/triple.py`: `1709603f910e46c85eb9b18dbb574cf988dd0d7aab701d3be1ff0e62144a00e1`
- `src/scoring/text.py`: `4db62c3238c830ec25faf979beb656dcc7b882f0843b318d973934b4f340111d`
- `src/scoring/records.py`: `7b031fa76c408b22ff2c1435236b6d38338bfddef5c83b2fd347c4660624108e`
- `tests/scoring/test_fixtures.py`: `e608be09466a74e0ad01df2d5e59888feaa8aaa2cb1649be886577f78c035450`
- `tests/scoring/test_qualification.py`: `1211996e192847616799fc2e046fcb8b4b2665889db0f18d99cfd6c31f513935`
- `tests/scoring/test_independent_review.py`: `747e6b33780eba68029bde5ac53436dcd7e0e82a02fb2c0983fd9f5699844ae7`
- `experiments/manifests/scorer_development_parity.json`: `ba851b894bff402aa9a4539244584e6a2adcb61ee7cf4cb953924c7d6c89f68a`
- `uv.lock`: `e75b50786f73f24295d832126ded45906dab774e3f94f6967cff7a5ee7ddcfb0`

PROPOSED NEXT ACTION: Qualify the source/reference development contract, generate raw development hypotheses, then run a separately preselected natural parity/coverage batch. Retain every cap, ambiguity, invalid output and unavailable region.
