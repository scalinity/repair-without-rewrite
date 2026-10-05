# Independent Pre-Implementation Review v1.2 — Accepted Findings

Status: ACCEPTED FOR BOUNDED FOUNDATION KICKOFF
Independent review decision: AUTHORIZE BOUNDED FOUNDATION ONLY

The independent GPT-6 Pro review found no BLOCKER findings. It explicitly authorized:
- independent scorer oracle and adversarial fixtures,
- MODEL-0 correctness work,
- B/C representation/loss/renderer conformance,
- public source/access qualification,
- BENCH-00,
- bounded comparator and development probes.

It did NOT authorize the final confirmatory training campaign or protocol freeze.

## F01 — MAJOR — Scientific distinctiveness

The v1.2 nearest-work audit omitted:

Hao Zhang, Felix Stahlberg, and Shankar Kumar,
"Predicting Compact Phrasal Rewrites with Large Language Models for ASR Post Editing,"
ICASSP 2025.

Before PUB-GATE 3, independently verify this work and revise the prospective contribution boundary around it.

Do not claim the first full-vs-compact ASR output-representation comparison.

The remaining prospective empirical lesson should center on:
- repaired vs introduced reference-error units,
- useful repair under matched presented-source exposure,
- whether reduced generation translates to lower complete native inference cost,
- explicit failure/ambiguity accounting.

No new expensive reproduction arm is automatically required.

## F02 — MAJOR — Scope / 30-day schedule

The broad v1.2 mandatory roster exceeds what H1 requires and is unlikely to be the best strict-month allocation from an unimplemented starting point.

Before PUB-GATE 3, either:
1. freeze a focused H1 roster,
2. demonstrate from measured timings that the broad roster fits,
3. or accept a longer calendar.

Independent-review preferred strict-month direction:
- H1 is the sole confirmatory core.
- B100-text and C101-text remain primary.
- H2 / B100-acoustic moves to stretch.
- A100 moves to stretch.
- ByT5-small remains the mandatory pretrained comparator.
- Qwen remains a frozen practical comparator.
- RAW and DET remain essential.
- Whisper transfer is B/C-only if affordable.
- common B/C guard analysis reuses cached outputs.
- reduce mandatory stress evaluation to a compact 2,400-case panel focused on eight high-value categories.
- preserve the full eligible natural primary population before cutting natural cases.

Proposed compact stress categories:
1. signs/numerical values
2. negation
3. software versions
4. paths
5. programming identifiers
6. units and quantities
7. repeated literals
8. multiple bindings

Preserve clean / repair / mixed views.

The review's example focused output roster was 158,016 learned outputs, a 62.9% reduction from 426,432.

This is a pre-freeze recommendation, not a frozen protocol.

## F03 — MINOR — Empty-reference contract

Canonical v1.2 retains legitimate empty-reference cases under explicit empty-reference accounting.
The draft registry requires nonempty references for primary normalized scoring.

Before source-manifest / PUB-GATE 3 freeze:
- reconcile the registry to the canonical legitimate-empty-reference rule,
- distinguish genuine empty reference from missing/null/sentinel,
- preserve appropriate source-insertion repair and output-insertion error accounting.

No evidence currently shows that the selected released populations actually contain qualifying empty references. This is a prospective contract consistency fix.

## No-Issue findings worth preserving

The independent review specifically found the following sufficiently handled:
- zero-new-annotation design,
- compatible triple-alignment existence,
- identity behavior,
- insertion accounting,
- candidate-independent coverage,
- failure credit,
- C renderer attribution,
- A/B attribution limits,
- parameter arithmetic,
- C event accounting,
- three-seed interpretation,
- multiplicity structure,
- acoustic-truth boundary,
- shared-hardware accounting,
- prospective unfilled fields,
- agent-written scientific software verification plan.

## Scorer verdict

KEEP AS SPECIFIED for bounded implementation and development qualification.

The reviewer judged the custom scorer mathematically coherent for the declared reference-error decomposition. It is not claimed as a novel universal metric.

## H1 verdict

H1 is well formed and ready for development qualification.

Bare B/C outputs remain primary.
C's deterministic renderer is constitutive to C.
The correct attribution is the full specified treatment: representation + renderer + supervision + decision process under the declared recipe.

## H2 verdict

MOVE H2 TO STRETCH for a strict one-month MVP.

Merely relabeling H2 secondary without removing its construction/training dependency does not save scope. If moved to stretch, H1 text-data readiness must be decoupled from acoustic common-support qualification.

## Stress-suite verdict

Keep exact generated tests, mixed repair/preservation, and unique source-visible recoverability.
Reduce mandatory model-evaluated stress scope before freeze if the strict-month plan is retained.

The review proposed:
8 categories × 4 template cells × 25 latent groups × 3 views = 2,400 cases.

## Final authorization boundary

No remediation is required before BOUNDED FOUNDATION implementation.

Before PUB-GATE 3 / final-run freeze, resolve:
- F01 nearest-work positioning,
- F02 final focused roster and measured schedule,
- F03 empty-reference consistency,
- useful-learning adequacy,
- ByT5 adaptation credibility,
- scorer/oracle conformance,
- identification widths / precision,
- practical-margin justification,
- exact source manifests / grouping / normalization / HPO / inference / statistics,
- complete native workload pricing.

Do not freeze paper_protocol_v2 or begin final confirmatory runs without a later owner authorization.
