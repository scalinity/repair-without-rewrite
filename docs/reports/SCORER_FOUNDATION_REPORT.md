# Scorer foundation report

Status: DEVELOPMENT MATHEMATICAL FOUNDATION PASSED; natural-population qualification remains pending. No PUB-GATE is claimed passed.

MEASURED RESULT: Initial red fixture suite: **21 failed** with NotImplementedError (`scorer_fixture_red.txt`); after implementation **21 passed** (`scorer_fixture_green.txt`). Broader attempt01:37passed; attempt02:38passed in16.68seconds (`scorer_qualification_attempt02.txt`). Attempts are preserved. A pre-output lattice-unavailable eligibility issue found during self-review was repaired and covered by an additional regression.

| Contract | Status | Evidence |
|---|---|---|
| Independent unit Levenshtein | PASS | Oracle suffix recurrence differs from rolling-row scorer |
| All optimal R/S and R/O lattices | PASS | 225 tiny pair families, all path/edge memberships and reference masks |
| Compatible triple conditional optimum and all ties | PASS | 3,375 alphabet{a,b},length0–3 triples compared to exhaustive all-seven-move path enumeration |
| Direct repair/introduction extrema, conservation, local reference event sets | PASS | Exhaustive path parity and 10,000 separately structured dense DP trials |
| Source masks fixed before O | PASS | Hash seals, failure outputs, and unavailable-preflight regression |
| Fixed denominators, empty reference, genuine empty/failed output | PASS | Corpus numerator retention and undefined zero denominators |
| Capped valid prefix / invalid C / UTF-8 / missing / abstention | PASS | Raw observation preserved, primary completion repair alwayszero on failed calls |
| Unicode15.1NFC/defaultcasefold/scanner/raworigins | PASS | Official19,074-row normalization suite; quote/hyphen/symbol/control/byte/scalar fixtures |
| Metamorphic checks | PASS | Duplication/order, bijective rename/reversal, isolated repair/damage, JSON, cap envelopes |
| Independent500development parity | PASS on synthetic DEV | Preselected SHA-bound500token triples(maxactual12,declaredcap64), independent dense lexicographic DP; not a natural population qualification batch |
| Computational qualification | MEASURED on synthetic DEV | 502cases including longrepetition and insertion-gap tie |
| Independent agent review | PENDING at this report version | Review artifact appended separately |
| Natural literal extractor / actual public alignment precision | NOT QUALIFIED | No natural literal gold or source-specific500-case batch created |

The oracle never imports/calls optimized alignment code. Tiny enumeration visits every monotone path; development parity uses a dense lexicographic prefix recurrence, while the scorer uses independent pair lattices and a conditional jointDAG. Conditional S/O can exceed ordinary S/O distance: canonical a,b,c cyclicfixture gives4 versus2 and repair/introduction2each. Raw repair−introduced=eS−eO holds at both interval endpoints. Completion-gated repair intentionally does not obey that conservation on failures.

MEASURED RESULT: Computational sample elapsed3.703143s,135.561cases/s including JSON export and Pythonallocation tracing. Maximum23,969jointstates,91,520retained admissible edges examined and167,783attemptedmoves. Pythontracedpeak39,117,567bytes; processRSS97,222,656bytes(macOS). 0natural-budgetcapcases/502; 1countintervalambiguouscases; 27localambiguouscases; maxrawrepairwidth1. Exactsyntheticcoverage100%; this is not an estimate for public H1 populations. Raw per-case and summary evidence: `experiments/scorer-profile-attempt01/`. Coding/modelcorrectness may have overlapped theCPU sample; no exclusive native scorer throughput is claimed.

FACT: The Unicode normalization/category backend isunicodedata2==15.1.0; runtimebinaryhash contributes to thepolicyidentity along withCaseFolding/PropList hashes. Official Unicode conformance tables and [license](https://www.unicode.org/license.txt) are preserved. Provenance offsets trace decomposition,reordering,composition and casefold expansion; noncontiguous/shared rawspans remain explicitly unavailable. No general semantic aliasing is implemented.

INFERENCE: reference_triple_v1 is ready for bounded development arithmetic use. Its natural-population feasibility, actual source-error denominators, literal yield, identification widths and precision still require source qualification and output-blind development inventories. Synthetic no-cap frequency cannot justify future PUB-GATE2.

Implementation/data identities at this report generation:

- `src/scoring/oracle.py`: `c8cc04e5c21ebfc20912c498f95887ca88fae32b79cafe96b493796dea3f7609`
- `src/scoring/triple.py`: `d19ac55c43d12cc6ab994845f36b6eb5bc311d1e0114d3a195ddc905da055586`
- `src/scoring/text.py`: `4db62c3238c830ec25faf979beb656dcc7b882f0843b318d973934b4f340111d`
- `src/scoring/records.py`: `d9fe4eba4fcc85e52ad3551accc77bfe54b22f4ff1d94e0209b97bdae275baeb`
- `tests/scoring/test_fixtures.py`: `e608be09466a74e0ad01df2d5e59888feaa8aaa2cb1649be886577f78c035450`
- `tests/scoring/test_qualification.py`: `8aba052a87cc323126b3463e88ae5a890dd37355eb2ecb99b4080ae953023c86`
- `experiments/manifests/scorer_development_parity.json`: `ba851b894bff402aa9a4539244584e6a2adcb61ee7cf4cb953924c7d6c89f68a`
- `uv.lock`: `0588833586a988d03b6e14fdc0cdb79b59df031d46650b4c648dc9a5c1dbe822`

PROPOSED NEXT ACTION: Complete independent review, then run a separately preselected publicdevelopment parity/runtime batch once sourcecontracts are available. Retain all realdata ambiguity and cap outcomes without manual rescue.
