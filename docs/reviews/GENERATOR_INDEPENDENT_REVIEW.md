# Independent generator review — bounded development

Reviewed 2026-10-05 UTC by the source/prior agent. Scope: source-only inverse, structural parser/target endpoints, latent versus model-input exports, and partition safety in `src/generation/stress.py`; canonical Part V source-only inverse/split/parser contracts were read directly. No generator implementation was edited by the reviewer.

**Disposition: restricted development mechanics pass after correcting complete-bundle leakage detection.** This supports development use of the declared toy grammar. It does not qualify the final 25-category/30,000-case pool or 9,000-case panel, natural recoverability, unseen-family generalization, or acoustic branches.

## Source-only inverse

The inverse takes source text plus the public catalog, policy and state cap. It does not accept a case-specific template ID, latent values, offsets, selected corruption mask or operation trace. It tests every compatible visible grammar. The constructor separately compares the unique derived target to the latent target; the target does not select an inverse. Numeric confusable alphabets, field-specific separators, finite unit aliases and polarity spelling define a deliberately restricted synthetic corruption relation. The deterministic public-grammar baseline has this same source-only contract and is expected to solve qualified examples.

Eight independent category fixtures use manually written corrupted fields and hand-derived clean values; they do not use the constructor's latent trace to choose expected answers. They cover signs, polarity, versions, paths, identifiers, units, repeated equal occurrences and multiple bindings, including composed transformations. All unique answers and deterministic inverse-cap failures pass. Further fixtures show unrestricted prose and unlisted Unicode look-alikes do not receive a numeric inverse, a valid changed numeric value remains its observed canonical value, and erased polarity is not recovered from a hidden reference. Under the separate underdetermined policy, an empty polarity slot admits four targets and produces no unique target.

The symbolic core closure is finite and its compatible canonical forms are explicit. Inverse state counts measure compatible-template/candidate closure states, not the number of scanned catalog regexes or byte operations. Runtime measurements must retain input lengths alongside that count. The current catalog has one typed two-slot constructor, four scaffold cells per category and only two coarser semantic relation patterns; eight categories and 32 DEV cells do not mean 32 independent linguistic mechanisms. No general natural-ASR inverse theorem follows.

## Model payload and parser endpoints

The measured 288-row development input export contains exactly `case_id`, `source_utf8`, `task_id`; reference text, latent field values, allowed forms, offsets and operation traces occur only in the separate latent export. All 288 source strings match their joined latent records. `case_id` is bookkeeping and includes category/view; downstream model tokenization must receive only the source string and common task framing, not a serialized whole row.

Independent output mutations confirm complete consumption: prefixes, suffixes, duplicate scaffold and truncation cannot pass whole-case conformance or structure-qualified fields. A wrong but uniquely parsed second slot preserves the first slot's match and fails only its own target value. An incomplete outcome earns no field success. Exact occurrence IDs and fixed source-correct/repair roles remain evaluator data. These are exact task-conformance endpoints, not claims of all semantic damage or natural prevalence. Source-visible witnesses are absent in this development export; typed invertibility, rather than hidden redundancy, supplies its recoverability certificate.

## Resolved finding: latent bundles were checked only by names

The initial split validator checked exact source/reference hashes and template/base-group IDs. Partition-prefixed scaffold text and IDs allowed the same complete bound negation values to recur across train/DEV without detection. The independent repro parsed clean visible train/DEV source strings, found equal values while complete source hashes differed, and expected a `bundle` rejection. Before correction: **1 failed, 12 passed in 0.06 seconds**. This was a cross-partition content check failure, even though a larger template/semantic split still required separate qualification.

The generator owner added a content signature of ordered typed canonical values, roles, bindings, multiplicity and relations, excluding split-dependent names/scaffold prefixes. Lexical-family and parent/case/base-group lineage checks were also added. Numeric value domains are now disjoint by partition and the toy polarity bundles are separated before drawing values. The independent test now injects the formerly possible equal bundle under different split scaffolds and confirms rejection; it does not weaken the required rejection merely because normal generation no longer creates the collision.

After correction: **13 independent tests passed in 0.04 seconds**. The existing measured artifact reports 288 cases, 96 base-group IDs, 267 distinct sources and 89 distinct references for its earlier code identity; those are historical measured counts and are not silently recomputed under new code. Duplicate content within one partition is not extra independent replication. Future construction must record collisions/dependency groups and count unique content alongside formal lineage IDs.

Near-duplicate thresholds, complete template-family pack assignment and the final family graph remain **PENDING**. Common digits/units may be shared grammar primitives, but partition-renamed scaffold prefixes alone cannot justify an unseen-semantic-mechanism claim. The current checks detect exact bundles, lexical identity and parent lineage; they do not certify all near duplicates or final independent-family breadth. Test value generation remains explicitly rejected by the development API, and no test seed or final pool was generated in this review.

## Evidence limits

[test_generator_independent_review.py](../../tests/data/test_generator_independent_review.py) contains the independent fixtures. The current independently checked model/latent export is under `experiments/manifests/stress_split_repair_20261005T054436Z/`; that fresh artifact reports 288 cases, 96 base groups, 267 distinct sources, 89 distinct references and zero typed-bundle collisions in its 96-row training-split audit. Earlier flawed-split exports remain retained under their original identities. The public inverse baseline's perfect development conformance is a construction diagnostic; it cannot establish that neural restoration is necessary or that useful natural learning occurred. No model, human annotation, listening, TTS or recognizer was used by this review.

Reviewed SHA256 snapshot:

```json
{
  "src/generation/stress.py": "0d83fdc4a2a54720d7269041d2698582cea9fc8b14a75605e5c547af14ca28ec",
  "tests/data/test_generator_independent_review.py": "5edc9f9001dde55103058a760e6857274654f85feb74c8ac6bd59aa0e0abfadf",
  "experiments/manifests/stress_split_repair_20261005T054436Z/model_inputs.jsonl": "d83b4afb54c7685ce43e2219bdf27893e09aed7347d61b2055f57fa8c566b8cd",
  "experiments/manifests/stress_split_repair_20261005T054436Z/latents.jsonl": "fc8dad695c28f2f1be326546e1e528d5bdff7f548c23aea6ee7d74957c701cb1"
}
```
