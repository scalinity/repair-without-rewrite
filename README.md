# Repair Without Rewrite

### A Controlled Comparison of Full-Transcript Generation and Compact Editing Under Matched Source Exposure

![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![MLX 0.32.3](https://img.shields.io/badge/MLX-0.32.3-black?logo=apple&logoColor=white)
![PyTorch 2.8.0](https://img.shields.io/badge/PyTorch-2.8.0-EE4C2C?logo=pytorch&logoColor=white)
![Transformers 4.55.4](https://img.shields.io/badge/Transformers-4.55.4-yellow)
![Unicode 15.1](https://img.shields.io/badge/Unicode-15.1-blue)
![Tests](https://img.shields.io/badge/Foundation_tests-180_passed-brightgreen)
![Status](https://img.shields.io/badge/Status-Foundation_repair_required-orange)

**Repair Without Rewrite** is a local research codebase investigating a specific question in automatic speech recognition: when a transcript needs correction, should a model generate the entire transcript again or produce a compact program of edits? The planned comparison pairs two randomly initialized Transformers with a shared encoder–decoder backbone, closely matched parameter counts, common source information, and matched training exposure. It measures repaired reference errors, errors introduced by correction, and the cost of producing a complete output. A deterministic renderer copies the compact model's untouched source spans byte for byte; whether the model chooses the right spans is an empirical question.

The repository implements the mathematical, data, and evaluation foundations needed to make that comparison auditable. It is separate from the LocalFlow application and contains **bounded development evidence, not completed paper results**.

> **Current disposition: `FOUNDATION_REPAIR_REQUIRED`.** The integrated suite passed **180 tests in 18.64 seconds**. Exact B100/C101 models passed a four-pair memorization rehearsal, but held-out correction and the planned 10M-exposure probes have not run. The full training tokenizer, source qualification, credible pretrained adaptation, and representative sustained benchmarks remain incomplete. No final training or protocol freeze has occurred. See the [foundation decision](docs/reports/FOUNDATION_GO_NO_GO.md) for the evidence and next dependencies.

## Table of Contents

- [Motivation](#motivation)
- [Research Systems](#research-systems)
- [Experimental Foundations](#experimental-foundations)
- [Safety & Correctness](#safety--correctness)
- [Architecture](#architecture)
- [Technical Highlights](#technical-highlights)
- [Tech Stack](#tech-stack)
- [Project Scale](#project-scale)
- [Development](#development)
- [Roadmap](#roadmap)
- [License](#license)

## Motivation

Correcting a transcript can remove a recognition error and introduce a new one in the same sentence. Whole-transcript generation also asks a model to reproduce words that may already be correct. Compact editing offers a different allocation of work: predict changes and let a renderer copy the rest. Fewer generated tokens, however, do not by themselves establish better preservation, useful correction, or faster complete requests.

This project studies that tradeoff under explicit controls. Released references supply the natural-text targets, while generated technical examples provide exact, restricted tasks without a new annotation queue. The intended contribution is controlled evidence about representation and rendering, including negative or inconclusive outcomes. It is not a claim to invent compact ASR editing: the [verified prior-work review](docs/reports/COMPARATOR_AND_PRIOR_WORK_QUALIFICATION.md) identifies *Predicting Compact Phrasal Rewrites with Large Language Models for ASR Post Editing* as a direct predecessor.

## Research Systems

### 1. A matched full-text and edit-program pair

B100 and C101 share an eight-layer encoder, four-layer decoder, width 768, SwiGLU width 2,048, and a tied vocabulary matrix. C101 adds source-boundary pointer projections and an action classifier. Both receive source text and trusted task framing; references and latent annotations are reserved for supervision and evaluation.

| Model | Trainable parameters | Output | Current evidence |
|---|---:|---|---|
| MODEL-0 | 8,621,312 | Causal token sequence | V0–V5, V7 and V8 passed; real-shard V6 not run |
| B100 | 100,686,336 | Complete restored transcript | Mechanical checks and 4/4 exact toy outputs |
| C101 | 101,081,859 | Ordered source-relative edits, then rendering | Mechanical checks and 4/4 exact toy outputs |

The exact models first failed the tiny output criterion despite lower training loss: B produced capped repetitions, while C damaged an identity example. A lower-learning-rate, longer rehearsal reached 4/4 exact outputs for both. These are two-byte memorization fixtures, with no held-out examples; the change in update count also prevents attributing the repair to learning rate alone. [Model foundation](docs/reports/MODEL0_CORRECTNESS_REPORT.md) · [B/C evidence](docs/reports/BC_CORRECTNESS_REPORT.md)

### 2. Source-relative editing and exact copying

The compact representation uses original UTF-8 byte coordinates, replacement text, and an explicit terminal decision. The renderer validates the entire program before copying source gaps. It rejects mismatched source hashes or lengths, illegal boundaries, overlapping edits, malformed UTF-8, and missing completion.

The model's encoded source is also checked against the literal source, cumulative byte offsets, legal boundary flags, and task framing before encoding. This additional check closes an independently discovered gap where a renderer could validate one source while the model saw another. Identity, insertion, deletion, replacement, adjacent edits, and repeated literals have explicit tests.

For `K` edits and `R` replacement tokens, C uses `1 + R + 3K` decoder positions and `R + K` vocabulary targets. Action, start-pointer, end-pointer, and vocabulary losses use separate whole-update denominators, avoiding a second division during gradient accumulation. These mechanical contracts preserve copied bytes; they do not guarantee correct edit selection. [Implementation](src/models/edits.py) · [Source binding and decoding](src/models/bc.py)

### 3. Reference/source/output error accounting

The scorer evaluates the released reference `R`, raw recognized source `S`, and candidate output `O`. It keeps reference/source and reference/output alignments minimum-edit, then retains every conditional optimum for the induced source/output alignment. Where those alignments disagree about repair or introduction, the result is an interval with explicit coverage.

Its raw counts obey:

```text
repaired errors − introduced errors = distance(R, S) − distance(R, O)
```

Repair uses the original source-error denominator; introduction uses reference words, including errors inserted anywhere in the output. Candidate outputs cannot change source eligibility. Failed, missing, invalid, capped, or abstained calls retain their records and receive no completed-repair credit; completion-gated credit is deliberately separate from raw conservation.

Qualification includes 3,375 exhaustive short triples, 10,000 fixed-seed trials, independent alignment implementations, and Unicode 15.1 normalization checks. Natural literal extraction and cluster-aware statistics remain unqualified. The synthetic computational profile is a fixture measurement, not an estimate of final-population coverage. [Scorer report](docs/reports/SCORER_FOUNDATION_REPORT.md)

### 4. Generated technical stress cases

The development generator covers signs and numerical values, negation, software versions, paths, programming identifiers, units and quantities, repeated literals, and multiple bindings. Each latent group retains clean, repair, and mixed views, so preservation and correction remain connected to the same underlying case.

The current **288-case development set** has 96 groups, 89 unique references, four template cells, and three views. A source-only inverse recovers all 288 targets under the restricted public grammar. That perfect deterministic baseline is a limitation of the present task difficulty, not evidence that a neural model is needed.

An independent review exposed reuse of complete typed payload bundles across partitions; the repaired validator checks the payloads without relying on partition names or scaffold prefixes. Broader semantic-family separation, near-duplicate grouping, and composition difficulty remain pending. The proposed 2,400-case evaluation panel is **not generated or frozen**. [Generator foundation](docs/reports/STRESS_GENERATOR_FOUNDATION.md) · [Independent review](docs/reviews/GENERATOR_INDEPENDENT_REVIEW.md)

### 5. Public-source admission and split barriers

Public metadata does not automatically become usable training or evaluation data. The source pipeline records access, rights, reference fields, upstream identities, and connected source groups. Book/project closure prevents shared material from crossing development and sealed roles, beyond a speaker-only split.

| Source | Established in this foundation | Remaining limit |
|---|---|---|
| LibriSpeech-PC | Closed metadata roles: 898 development rows / 12 groups; 5,273 sealed rows / 19 groups | Reference-field choice remains provisional; all 311 rows in the bounded training inventory are excluded |
| Full LS-PC training inventory | 52,482 potentially usable rows identified in metadata | Not admitted training supply |
| SLUE-VoxCeleb | Access barrier recorded | HTTP 401 behind an agreement/contact gate; zero actual rows or audio acquired |

The corrected speech probe selected 12 development clips from 12 eligible groups before inference. A pure pre-model join binds each recording to its role, source identities, reference hashes, and audio hash. Sealed metadata accounting is not sealed model inference. Neither planned natural primary population is fully admitted. [Source qualification](docs/reports/PUBLIC_SOURCE_QUALIFICATION.md)

### 6. Pretrained comparators with explicit adequacy limits

ByT5-small and Qwen3-4B-Instruct-2507 provide prospective pretrained comparisons. Their native interfaces use pinned assets, task-specific input contracts, explicit output validation, and recorded backend identities.

- **ByT5-small:** native loading, forward/loss checks, and ten synthetic updates executed. All four pre/post-training decode attempts capped and contained invalid prefixes. A credible adapted comparator has not been demonstrated.
- **Qwen3-4B-Instruct-2507:** two short synthetic greedy requests completed with valid text. Both had zero repair and zero introduced errors relative to their constructed targets. Natural prompt adequacy remains unknown.
- **ConstDecoder:** the bounded official-code scan found task, asset, and CUDA-path incompatibilities. No executable reproduction or model-performance conclusion follows from that scan.

These controls prevent a future comparison from relying solely on scratch-model behavior. Successful execution is recorded separately from useful restoration. [Comparator qualification](docs/reports/COMPARATOR_AND_PRIOR_WORK_QUALIFICATION.md)

### 7. Native runtime and speech-path qualification

The benchmark harness records complete operation boundaries, warmup, model/data/runtime identities, checkpoint behavior, and distinct memory views. A decoder-geometry workload completed a 20-minute segment at roughly 4,429 **fixture tokens/s**. It used fixed blocks rather than the paper's canonical exposure population. B/C evidence consists of short synthetic samples; sustained representative B/C rates and useful decode throughput remain unmeasured.

The pinned Parakeet-MLX path completed 12 clips covering 67.705 seconds of audio in 2.561881 seconds of summed warmed call time. Two initial repeated calls are accounted for separately; total fresh-process work was 8.579619 seconds. Two sources produced long repeated `<unk>` sequences: the retained panel has 3,094 source errors over 198 reference lexical tokens, with two joint-state caps per reference field. Static diagnostics found nonfinite token confidences and a preprocessing frame-bound defect; its causal role is unproven. Further representative source construction is stopped pending repair; preprocessing equivalence to the original NVIDIA/NeMo path is unqualified.

Kokoro's alternate MPS STFT path failed parity against its original mathematical path. A separately declared original CPU path completed two calls, but the unlistened waveforms do not establish target fidelity, acoustic quality, or screening yield. These bounded timings do not prove a speedup or a one-month campaign budget. [Native calibration](docs/reports/BENCH00_NATIVE_CALIBRATION.md) · [Speech probe](docs/reports/ASR_TTS_NATIVE_PROBE.md)

## Experimental Foundations

| Principle | Application |
|---|---|
| **Matched source exposure** | The planned comparison charges common source/target exposure independently of each representation's native decoder work; the full training tokenizer and exposure population are still pending. |
| **Representation plus renderer** | C's deterministic copying is part of the treatment, alongside its supervision and decision process. The comparison cannot isolate a pure neural-architecture effect. |
| **Reference-conditional outcomes** | Error counts describe agreement with a released reference, not all valid paraphrases, acoustic truth, or preservation of meaning. |
| **Useful repair and preservation together** | A future favorable result must survive repair and ordinary-error criteria as well as introduced-error analysis; copying everything is not sufficient. |
| **Fixed populations and failures** | Eligibility precedes candidate outputs. Ambiguity, caps, invalid calls, exclusions, and unavailable denominators remain visible. |
| **Independent correctness evidence** | Exhaustive oracles, numerical checks, metamorphic tests, and separate reviews support software claims without substituting for empirical model quality. |
| **Prospective scope changes** | Accepted review findings narrow the proposed core to B/C; acoustic treatment and A100 remain stretch work. No final protocol has been frozen. |

The [accepted design review](docs/reviews/Independent_Pre_Implementation_Review_v1_2_Accepted_Findings.md) and [prospective amendments](docs/reviews/PROSPECTIVE_AMENDMENTS.md) explain how the working plan differs from the immutable supplied specification.

## Safety & Correctness

The primary safeguards are against invalid experimental conclusions. Exact copying is a byte-level invariant, normalization is a scoring policy, and agreement with a reference is an operational outcome. None certifies semantic safety.

Source masks and denominators are sealed before output scoring. Genuine empty references differ from missing or malformed references; zero denominators remain undefined. Budget exits preserve proved total identities while leaving unavailable local correspondence unavailable. The planned equal-domain endpoint cannot silently drop an inaccessible domain or reweight the remaining one.

Failures remain part of the evidence: the unsuccessful memorization recipe, failed STFT parity, unavailable source access, invalid comparator outputs, and repeated-unknown ASR results are retained in their reports. No new human annotation or listening queue was used to turn these limitations into passed gates. The [foundation decision](docs/reports/FOUNDATION_GO_NO_GO.md) separates tested mechanics, pending research qualifications, and unrun experiments.

## Architecture

```text
┌────────────────────────────────────────────────────────────┐
│ Source and experiment contracts                             │
│ Released metadata → grouped roles → pre-model hash checks    │
│ Restricted stress grammar → source-only development cases    │
└──────────────────────────┬─────────────────────────────────┘
                           │ source text + trusted task framing
┌──────────────────────────▼─────────────────────────────────┐
│ Local model execution                                       │
│ B100 → complete text     C101 → edit program → byte renderer  │
│ ByT5 / Qwen → separately qualified comparator outputs        │
│ Explicit status, native work, timing and memory records      │
└──────────────────────────┬─────────────────────────────────┘
                           │ raw output + completion/failure status
┌──────────────────────────▼─────────────────────────────────┐
│ Evaluation and evidence                                     │
│ Reference + fixed source eligibility + output → counts/bounds│
│ Independent oracles → test receipts → qualification reports  │
└────────────────────────────────────────────────────────────┘
```

References and latent stress annotations enter supervision and evaluation through separate records, not the inference input. The first-party implementation lives in `src/`; `benchmarks/` contains bounded execution and profiling entry points. Manifests and reports capture the identities and scope of completed runs. Large local assets, environments, and checkpoints are separate from the source checkout's reproducible contracts.

| Location | Responsibility |
|---|---|
| [`src/models/`](src/models/) | Transformer math, optimizer/checkpoints, tokenizer, B/C decoding, edit labels and rendering |
| [`src/scoring/`](src/scoring/) | Unicode policy, pair/triple alignment, independent oracle, fixed-denominator records |
| [`src/data/`](src/data/) | Source admission, grouping, reference contracts and comparator interfaces |
| [`src/generation/`](src/generation/) | Restricted technical grammar, inverse qualification and split validation |
| [`src/inference/`](src/inference/) | Bounded native ByT5 and Qwen probes |
| [`docs/reports/`](docs/reports/) | Measured outcomes, failed attempts, qualifications and limits |
| [`docs/reviews/`](docs/reviews/) | Independent findings and prospective amendments |

This is an offline research workflow with no application server or deployment requirement.

## Technical Highlights

- **Independent numerical checks:** a NumPy FP64 forward path and selected finite differences test model math without using the same implementation as the reference.
- **Precision as an execution contract:** `MLX_ENABLE_TF32=0` resolved reduced-precision FP32 discrepancies at the existing tolerances; a dtype label alone was insufficient.
- **One owner for tied weights:** parameter enumeration rejects aliased trainable leaves so a tied embedding is updated once.
- **Cached decoding checks:** causal/self/cross-attention paths are checked against full execution, including reuse of projected cross-attention keys and values.
- **Exact continuation state:** checkpoint records include optimizer moments, data cursor, scheduler, RNGs, and partial gradient accumulation; MODEL-0's next 20 resumed updates matched uninterrupted execution.
- **Atomic checkpoint publication:** readback, shape/dtype/checksum verification, and a finite forward probe precede publication of a completed checkpoint directory.
- **Occurrence-aware editing:** original coordinates distinguish repeated literals without rewriting later offsets after an earlier edit.
- **Unicode provenance:** normalized lexical tokens retain original scalar and byte intervals; shared or noncontiguous spans remain explicitly unavailable.
- **Source-only stress qualification:** the inverse sees the visible string and public grammar, with hidden-reference equality checked only after recovery.
- **Complete-output accounting:** lower loss, a fast abstention, or a promising truncated prefix cannot stand in for a completed useful correction.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Scratch models and native arrays | MLX 0.32.3 on Apple Silicon / Metal |
| Pretrained model probes | PyTorch 2.8.0, Transformers 4.55.4 |
| Independent numerical reference | NumPy 2.2.6 |
| Unicode evaluation policy | `unicodedata2` 15.1.0 and pinned official Unicode tables |
| Tests | pytest 8.4.2 |
| Dependency identity | `pyproject.toml` and `uv.lock` |
| Evidence formats | JSON, JSONL, text receipts and SHA-256 identities |
| Separate speech runtime | Pinned Parakeet-MLX 0.5.2 and Kokoro 0.9.4 probe environment; see the [speech report](docs/reports/ASR_TTS_NATIVE_PROBE.md) |

## Project Scale

Snapshot of the bounded foundation on **2026-10-05**. Source counts exclude downloaded packages, model assets, and generated environments. Test duration is a correctness receipt, not a performance benchmark.

| Metric | Count / scope |
|---|---|
| First-party Python files in `src/` | 16 |
| Python test files in `tests/` | 13 |
| Integrated test receipt | 180 passed in 18.64 s |
| Exhaustive scorer triples | 3,375 |
| Fixed-seed scorer trials | 10,000 |
| Official NFC conformance rows | 19,074 |
| Exact B/C memorization panel | 4 pairs per model, no held-out set |
| Generated development stress cases | 288 cases / 96 groups / 89 unique references |
| Stress category × cell × view coverage | 8 × 4 × 3 |
| Corrected public speech panel | 12 clips / 12 groups / 67.705 s |
| Final confirmatory training runs | 0 |

Counts and claims were checked in the [two-pass README review](docs/reviews/README_TWO_PASS_REVIEW.md). Detailed findings and current admission decisions remain in the linked subsystem reports.

## Development

| Prerequisite | Requirement |
|---|---|
| Hardware / OS | Apple Silicon macOS for the current native MLX tests and probes |
| Python | 3.12; the project requires `>=3.12,<3.13` |
| Dependencies | Use the committed lockfile; keep research environments isolated |
| Large models and audio | Separate, explicitly admitted local assets; not required for the ordinary test suite |

From the repository root, create the locked environment using binary wheels:

```sh
uv sync --locked --no-build
```

Run the foundation tests with the qualified precision setting:

```sh
MLX_ENABLE_TF32=0 .venv/bin/python -m pytest
```

For the scorer tests alone:

```sh
.venv/bin/python -m pytest tests/scoring
```

No application build or server is needed. The test command does not launch the standalone training, comparator, or speech benchmark programs. Those require their own manifests, assets, scope, and exclusive accelerator scheduling. The existing test receipt establishes the recorded local environment; a fresh checkout should rerun the tests before relying on it.

## Roadmap

These are dependency-ordered qualifications, not scheduled or completed results.

| Direction | Next evidence needed |
|---|---|
| **Admit usable source and training data** | Resolve reference policy, source access and grouping; diagnose the pinned ASR failures and qualify its preprocessing path. |
| **Finish tokenizer and convergence gates** | Train/hash the permitted 16,384-entry tokenizer and pass real-shard V6 before larger probes. |
| **Measure representative native costs** | Sustained B/C complete updates, valid decoding at representative lengths, memory pressure and scorer/statistics cost. |
| **Establish useful development learning** | Paired seed-42 10M-exposure recipes, held-out complete outputs, and credible ByT5 adaptation with disclosed budgets. |
| **Qualify evaluation precision** | Natural nonidentity alignment coverage, literal extraction, cluster-aware uncertainty, and broader stress-family/composition checks. |
| **Review scope before freeze** | Integrate the accepted findings, justify any 150M endpoint, and price the full core with reserve before owner review. |
| **Keep extensions conditional** | Acoustic training, A100, and B/C-only Whisper transfer depend on separate qualification and measured affordability. |

## License

A repository-wide license has not been selected. Public visibility does not grant a general reuse license. Third-party data, model assets, and included Unicode material retain their own terms and attribution requirements; source access and licensing are documented in the qualification reports.

<p align="center"><em>Measure what a correction repairs, what it changes, and what it costs.</em></p>
