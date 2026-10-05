# Independent scorer review — bounded development

Reviewed 2026-10-05 UTC by the source/prior agent, independently of the scorer implementer. Canonical Part IV, lines 4758–5292, was read in full for this review. Scope: `src/scoring/{triple,records,text,oracle}.py` and existing scorer tests. No scorer implementation was edited by the reviewer. This review does not qualify natural public populations, a frozen scorer, or PUB-GATE 2.

**Disposition: new finite-domain checks pass after one general budget-fallback correction.** No unresolved mathematical disagreement was found in the additional domains below. The source/error eligibility checks are independent of the production traceback and of the existing oracle's alignment routines.

## Resolved finding: closed-form totals lost on a local joint-budget failure

Before correction, `score_tokens(R=['a'], S=O=['b'], Limits(pair_cells=100, joint_states=0))` returned raw repair `[0,1]` and introduced `[0,1]`. Pairwise lattices existed, so its existing closed-form branch did not apply; the joint-budget abort widened even the proved identity totals. Canonical IV.7/IV.9 specify repair and introduced totals `[0,0]` when O=S regardless of local correspondence availability. O=R and S=R had the same routing issue. This was overly broad identification, not evidence of false positive repair.

Root corrected all fallback exits through `_known_totals_on_fallback`, retaining exact proved totals while leaving local graph/subset outputs unavailable. The reviewer added nine combinations of identity/perfect-output/perfect-source and pair-cell/state/move failure budgets. All now pass; none fabricates local eligibility from total equality. The finding is retained here rather than omitted from the successful final disposition.

## Independent verification added

[test_independent_review.py](../../tests/scoring/test_independent_review.py) constructs complete pair/triple path lists from scratch, evaluates their columns and filters complete paths by exact objectives. It imports production routines only to obtain the actual result. Expected results do not call production or existing-oracle distance, lattice, pruning or traceback code.

- **225 pairs:** every binary sequence of length 0–3 against every other. Checks all reference and source occurrence sets, certain-correct/error labels, complete invariant insertion-gap index sequences and unique-path certificates. This adds the source/gap consensus dimensions missing from the existing pair-oracle comparison.
- **343 triples:** every binary sequence of length 0–2 for R/S/O. Checks conditional S/O cost, repair/introduced extrema, source-token event sets including reference/gap attribution, and sharp additive fixed-correct damage and fixed-error repair extrema. The source subsets are derived from independently enumerated pre-output pair paths.
- **9 budget fixtures:** the three proved total identities remain points under local graph/pair failure, while local events and subset outputs remain unavailable.
- **1 failure/empty-reference fixture:** a capped observed output against an empty reference contributes two insertion errors to a corpus with one reference word; primary repair is zero and the failure is retained. The pooled WER is two, not zero or an omitted-row rate.

Initial correction verification: **12 tests passed in 0.21 seconds**. Four additional exact-domain/provenance-tamper cases were then added and passed in the follow-up 19-test run including three native-probe interface tests. Counts refer to exercised finite cases inside those tests, not natural utterances or model outputs. The review did not repeat the root's entire 3,375-triple/10,000-property/500-synthetic development suite; that evidence has its own provenance. It did inspect the independence of the existing all-path and dense reference routines. Shared mathematical definitions are necessary; shared alignment/pruning data flow is absent.

## Inspected invariants and remaining scope

The implementation retains integer pair constraints and conditional S/O optimization, handles insertion rewards columnwise, directly verifies introduced extrema by conservation, uses deterministic traversal and declared move order, and preserves frozen source masks when a later candidate could otherwise rematerialize them. Source error/deletion eligibility does not require a unique source index; certain source-correct occurrences do. The independently enumerated source/gap domains found no candidate-dependent eligibility change.

The pooled `aggregate(records)` helper is now explicitly labelled secondary. Root added `equal_domain_aggregate` with fixed 0.5/0.5 natural-domain weights and exact rational ledgers. Independent hand-derived domains verify primary WER 1/2 versus pooled 3/4 and primary completed repair 1/2 versus pooled 1/4. An empty or absent domain cannot be dropped or reweighted; undefined endpoints stay undefined. Actual natural population identities, paired identification contrasts and cluster uncertainty still need their sealed analysis inputs.

Natural literal extraction, whole-interior typed parsing, invariant output anchor matching, fixed literal denominators and the complete population/case/view record schema remain pending. Secondary subset outputs can be unavailable while primary totals are exact; no total fast path establishes literal surface preservation. The generated structural parser belongs to the separate generator foundation and must remain completion-gated independently of lexical fallback.

Root extended the preflight hash to cover reference/source bytes and tokens, masks, cached R/S lattice and raw-offset provenance, and validates it before scoring. Independent offset and lattice tampering fixtures now block candidate scoring. This addresses the internal cache integrity concern raised during review. Upstream case/population/view/reference-policy bindings remain explicitly null until sealed manifests exist, rather than inventing identifiers.

This review supports continued development-only scorer use in its tested scope. It does not establish whole-natural-corpus exact coverage, runtime feasibility at final output volume, source rights/reference quality, statistical power, or publication readiness.

## Reviewed code identity

SHA256 snapshot after the corrected independent tests:

```json
{
  "src/scoring/triple.py": "1709603f910e46c85eb9b18dbb574cf988dd0d7aab701d3be1ff0e62144a00e1",
  "src/scoring/records.py": "7b031fa76c408b22ff2c1435236b6d38338bfddef5c83b2fd347c4660624108e",
  "src/scoring/text.py": "4db62c3238c830ec25faf979beb656dcc7b882f0843b318d973934b4f340111d",
  "src/scoring/oracle.py": "c8cc04e5c21ebfc20912c498f95887ca88fae32b79cafe96b493796dea3f7609",
  "tests/scoring/test_independent_review.py": "747e6b33780eba68029bde5ac53436dcd7e0e82a02fb2c0983fd9f5699844ae7"
}
```
