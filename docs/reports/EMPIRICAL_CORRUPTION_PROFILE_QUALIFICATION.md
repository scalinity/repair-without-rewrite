# Empirical corruption profile qualification — 2026-10-05

**FRONTIER_MODEL_REVIEW_REQUIRED. The approved empirical table was estimated faithfully, but reader admission stops at the owner's surface-policy-artifact gate.** No generated population, inverse-qualified corruption pool or full reader is certified by this measurement.

The prospective [Astra decision](../reviews/FRONTIER_READER_CURRICULUM_DECISION_V1.md) was recorded verbatim and committed separately at `bd882ceea205c2f9e0547fa49337e94e1b042fad`, before implementation. Starting local and remote main were clean/equal at `928fd0305206ad6d6130d0667d1b206baa521a64`; the [baseline receipt](../../experiments/manifests/frontier_reader/baseline-validation.attempt01.json) records **259 passing tests**. The supplied design and registry remain unchanged.

## Measured TRAIN-only estimation

[Runner](../../benchmarks/empirical_corruption_profile.py) and [estimator](../../src/data/empirical_corruption.py) use all **1,024 frozen TRAIN pairs / 48 groups exactly once**. All 96 CALIBRATION pairs are excluded from estimation; HPO, final, private data and student outputs are absent. Pair file SHA256 is `ce4a170a086afee430085c4e6f665e8af58b8c68091afc27f10ee403c81951d8`. Every selected row rejoins the currently qualified TRAIN role/group/family and both released-reference hashes. Strict reference and hypothesis byte hashes are checked.

Alignment identity is `raw-codepoint-all-optimal-edge-consensus-v1`: unit-cost raw Unicode-codepoint Levenshtein, **no normalization**. Exact integer prefix/suffix optimal-path counts identify each edit edge present on every optimal path. An edge includes operation, reference coordinate, hypothesis coordinate and both literal payloads. An arbitrary traceback never supplies an observation. Raw distances, all ambiguous candidate edges and every consensus observation remain in the ignored private alignment audit.

The implementation only estimates the specified substitution/deletion/insertion table. A supported entry needs at least **five distinct records AND three groups**. Sampling weight is retained consensus occurrences. Unsupported entries have zero weight. The measured support range among retained entries is **5–212 records / 4–45 groups**. Descriptive tags do not filter or change these weights.

Evidence: [measurement](../../experiments/manifests/frontier_reader/empirical-profile-measurement.attempt01.json), [complete aggregate table including unsupported entries and co-occurrences](../../experiments/manifests/frontier_reader/empirical-profile-table.attempt01.json), [public preflight](../../experiments/manifests/frontier_reader/empirical-profile-preflight.public.attempt01.json). The exact raw input-hash inventory and per-record alignment audit remain under ignored `exports/frontier-reader/empirical-profile-attempt01/`; their hashes are bound in the measurement.

| Quantity | Measured |
|---|---:|
| Raw unit edit-distance mass | 3,089 |
| Consensus edit occurrences | 2,330 |
| Unit mass omitted because no consensus exists | 759 |
| Consensus occurrences rejected by support | 217 |
| Retained weighted occurrences | 2,113 |
| Supported literal entries / unsupported entries | 67 / 398 |
| Supported two-operation co-occurrence entries | 85 |
| Records with ambiguous edits / multiple optimal paths | 229 / 229 |
| Possible optimal edit edges / ambiguous possible edges | 4,254 / 1,924 |
| CPU estimation wall, including input binding | 24.300607 seconds |

The mass reconciles exactly: **3,089 = 759 + 217 + 2,113**. Ambiguity removes **24.5711%** of raw unit edit mass. Support removes **9.3133%** of consensus occurrences, or **7.0249%** of raw unit edit mass. Combined rejection is **31.5960%** of raw unit mass. Alternative candidate edges are a different denominator: 1,924/4,254 = **45.2280%**. They are not 1,924 observed errors.

## Actual retained composition

| Operation | Occurrence weight | Share |
|---|---:|---:|
| Substitution | 938 | 44.3919% |
| Deletion | 879 | 41.5996% |
| Insertion | 296 | 14.0085% |

| Descriptive effect | Occurrence weight | Share |
|---|---:|---:|
| Punctuation | 1,372 | 64.9314% |
| Case only | 525 | 24.8462% |
| Whitespace / boundary | 48 | 2.2717% |
| Other characters | 168 | 7.9508% |

**Punctuation plus case comprise 89.7776%; adding whitespace gives 92.0492%.** In this actual supported table, punctuation entries contain only punctuation payloads, and whitespace entries contain only whitespace payloads; this is not a mixed lexical/punctuation tag inflating the total.

The largest entry is deletion of a literal double quote: **433 occurrences / 212 records / 40 groups**, or **20.4922%** of the entire retained weight. Next are comma deletion (246 / 187 / 45), comma insertion (204 / 175 / 44), and comma-to-period substitution (99 / 96 / 40). All remain in the table unchanged. No word-confusion, homophone or phonetic interpretation is asserted.

A separate [descriptive audit](../../experiments/manifests/frontier_reader/raw-surface-descriptive-audit.attempt01.json) applies the existing `lexical_eval_v1` only to report source differences, never to filter this profile: **508 of 842 raw-different records (60.3325%) have identical lexical sequences**. Including the 182 byte-identical records, **690/1,024** have no lexical source error. The remaining 334 have 521 lexical edit units against 22,745 reference units (2.2906% aggregate source WER). Raw and lexical distances use different units and are not subtracted or pooled.

## Severity and co-occurrence

Zero mass is preserved exactly: **182/1,024 = 17.7734375%**.

| Phase | Severity 0 | Severity 1 | Severity 2 |
|---|---:|---:|---:|
| P0 | 182/1,024 | 842/1,024 | 0 |
| P1/P2 | 182/1,024 | 218/1,024 | 624/1,024 |

The full uncapped raw distance distribution is in the measurement: distances 0–15, 17–20, 23 and 42 occur, maximum 42; all 1,024 observations are retained. Severity comes from raw distance, independently of alignment/support rejection.

Co-occurrence requires distinct records/groups and distinct original positions. Codepoint slots and insertion gaps are represented separately. Only pairs of supported elementary entries meeting the joint five-record/three-group threshold receive nonzero joint weight. This is a diagnostic table; no two-operation candidate or inverse-qualified pool has been admitted.

## Freeze boundary and stop

The estimated aggregate table is hash-bound at **`5df3800d7a29e370abdce36bd489989482d5d878765612b5a14a4b2cab1fc310`**. This is an estimation-table hash, **not** a complete frozen reader/profile bundle. Renderer implementation, generated-base manifest, proposal/rejection ledger, accepted variants, source-only union inverse qualification and population hashes were not constructed after the scientific stop. No claim is made that required strata are empty or nonempty.

**Measured problem:** the largest 40% treatment would be estimated overwhelmingly from raw transcription surface conventions. The majority of raw-error records have no lexical discrepancy under the existing task scorer. Quote/punctuation/case reconstruction dominates, while literal other-character support is small. This strongly implicates a reference/recognizer surface-policy effect rather than a profile dominated by lexical recognizer repair.

**Inference and limitation:** this does not prove every punctuation/case error is undesirable or that no valid restoration study could use this distribution. It does establish the condition the owner explicitly required to escalate: faithful use of this measured profile is scientifically questionable for the proposed matched-corruption intervention. A raw surface-restoration experiment could be a defensible *explicitly accepted* choice; the implementation agent may not make that choice.

Smallest frontier choices worth considering, **none implemented**:

1. Explicitly retain the measured raw profile and justify the surface-dominated treatment/claim boundary.
2. Prospectively change profile estimation or operation eligibility to separate lexical and surface-policy effects, retaining exact written targets and disclosing the resulting new distribution.
3. Prospectively revise the generated corruption applicability/support contract if the approved technical population cannot support the intended empirical treatment.

B100/C101, source-only inference, C representation/renderer, objectives, weights, tokenizer, optimizer/clip, channel totals, paired exposure, update target, six LR slots and H1 attribution remain unchanged. Changing the profile, eligibility or severity would change the data intervention and effective repair difficulty; it could not be compared as if it were the same approved curriculum. Any changed population requires fresh qualification, frozen hashes and symmetric B/C consumption.

[Independent review](../reviews/EMPIRICAL_CORRUPTION_PROFILE_INDEPENDENT_REVIEW.md) separately checks the raw inputs, consensus algorithm and table. [Tests](../../tests/data/test_empirical_corruption.py) include independent exhaustive optimal-path enumeration, raw Unicode/ambiguity, support thresholds, severity/zeros, co-occurrence and role/reuse rejection. Integrated validation is reported in the [session report](FRONTIER_READER_IMPLEMENTATION_SESSION_REPORT.md).

**No BENCH, six-probe slot, final seed, final/sealed candidate inference or protocol freeze occurred.**

FRONTIER_MODEL_REVIEW_REQUIRED
