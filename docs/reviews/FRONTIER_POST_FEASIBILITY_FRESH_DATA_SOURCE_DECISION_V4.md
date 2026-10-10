# Post-Feasibility Fresh-Data Source Decision v4

Date: 2026-10-10  
Scope: read-only scientific-design adjudication

## A. Final disposition

**AUTHORIZE_ALTERNATIVE_CORPUS_QUALIFICATION_DESIGN**

Select exactly one alternative for a bounded prerequisite:

**Mozilla Common Voice Scripted Speech 26.0 — British English**  
Publisher dataset ID: **`cmrt6zrob000zmm07yqwjlpwi`**

**This is a design decision only. The candidate remains NOT QUALIFIED.** It authorizes no acquisition, implementation, source construction, inference, fitting, evaluation, or repository change.

**INFERENCE:** Further immediate effort recovering TED-LIUM through its unavailable historical routes has lower value than establishing whether this specific Mozilla release has accessible, adequate metadata. The next investment should answer that narrow question.

The original independence requirement remains binding. Speaker-disjoint splits alone are insufficient.

## B. Exact reviewed Git and scientific identities

**VERIFIED:** The local repository was clean on `codex/post-feasibility-v3-record`. Live remote identities matched the supplied scientific and documentation branches.

| Identity | Verified commit |
|---|---|
| Current documentation | `b432690ca137f4fb4946f3fe5579a6b6069844f1` |
| Frozen G2 execution | `609f97f31979d469ad8551d06b2c07c3513181ec` |
| Previously recorded authority | `f7dda7bbeddfcb21d9ac7c7441bf8158afbcd06a` |
| G2 qualification | `2c27cff28a31ae64220df9b06094a914e94dd0f3` |

**VERIFIED:** Frozen execution is an ancestor of the previous authority, which is an ancestor of the current documentation checkpoint. The seven scientific campaign reports and independent reviews inspected were byte-identical to their frozen execution versions.

The review included the complete preceding fresh-data qualification report, complete v3 decision, complete v2 decision, complete feasibility study and appendices, Post-G2 development decision, four G2 reports, and three independent reviews.

| Recorded document | SHA-256 |
|---|---|
| Frontier v3 | `8f1670fe501c365573f3fc5fb194a48de2d80b43e0df4e4c381d7d38aecad7b9` |
| Frontier v2 | `874957b90a0dd33cffbde3b9a60980be88d06b3733b74b0b4de3e28180f3f88b` |
| Complete feasibility study | `698bc4a54e07c09db8e0c63228836ffaec32ec664a5c68edb2e86a5c900976d0` |

**FACT — retained scientific identity:** The proposer remains:

- `google/byt5-small`
- Revision `68377bdc18a2ffec8a0533fef03b1c513a4dd49d`
- Exact ten-pass checkpoint: update **35,283**
- State SHA-256: `d6b319df934d7be5c2c3f9d6b7294e8df4cc3e4d92120a09cec78b497f315373`

Private checkpoint payloads were not loaded or freshly rehashed during this adjudication.

## C. Evidence supporting the TED-LIUM blocker

**FACT — retained qualification findings:** The original archive, both official-linked mirrors, and the paper-linked publisher route failed. No verified official alternative, original inventory, qualified parser, eligible-segment census, connected-component census, project-overlap clearance, or storage plan was established.

**VERIFIED this review:** OpenSLR resource 51 still returned “Resource not found.” Historical URLs and checksums establish an expected artifact identity; they do not establish current acquisition availability. [OpenSLR resource 51](https://www.openslr.org/51/)

The original paper reports 2,351 talks, 2,028 speakers, 268,231 segments and 452 aligned hours. TFDS reports 268,263 training examples. The **32-example discrepancy remains unresolved**. [TED-LIUM 3 paper](https://arxiv.org/abs/1805.04699), [TFDS catalog](https://www.tensorflow.org/datasets/catalog/tedlium)

The torchaudio checksum remains a historical expectation:

`ad1e454d14d1ad550bc2564c462d87c7a7ec83d4dc2b9210f22ab4973b9eccdb`

It is not a hash verified against an acquired project artifact. [Torchaudio release metadata](https://docs.pytorch.org/audio/2.8/_modules/torchaudio/datasets/tedlium.html)

**DECISION:** Suspend immediate TED-LIUM recovery work. Preserve its qualification result and evidence. A subsequently supplied official restoration can be considered through another bounded decision; this decision authorizes no continuing recovery search.

## D. Independent assessment of the Mozilla candidate

**VERIFIED — publication identity, not payload properties:** The official page identifies the selected release, its curator, source release, packaging, and listed archive.

| Field | Publisher claim |
|---|---|
| Dataset | Common Voice Scripted Speech 26.0 — British English |
| Steward | MDC Curators |
| Dataset ID | `cmrt6zrob000zmm07yqwjlpwi` |
| Release date | July 20, 2026 |
| Parent release | `cv-corpus-26.0-2026-06-12`, English |
| Listed filename | `common-voice-scripted-speech-26-0-britis-0fe481c3.tar.gz` |
| Packaging / size | TSV and MP3; approximately 6.97 GB |
| TRAIN | 201,330 clips; 3,244 speakers |
| DEV / TEST | 5,302 / 8,708 clips |
| Selection | Previously validated recordings; accent filtering; no age or gender filtering |

The filename spelling above is intentional. These are publisher statements, not an independently inspected archive inventory. [Exact publisher page](https://mozilladatacollective.com/datasets/cmrt6zrob000zmm07yqwjlpwi)

**VERIFIED:** The publisher documents public dataset-summary and metadata endpoints. Bounded unauthenticated requests to both endpoints for this dataset returned **HTTP 403** during this review. No checksum, exact archive byte count, or row-level metadata was obtained. The response does not establish whether authentication, access controls, or another service restriction caused the failure. No bypass was attempted. [Official API documentation](https://mozilladatacollective.com/api-reference/docs)

**INFERENCE:** This is a credible candidate for metadata qualification because its original publisher supplies an identifiable release and a documented access mechanism. Its actual payload availability and scientific suitability remain unverified.

## E. Release, license and availability comparison

| Requirement | TED-LIUM 3 legacy TRAIN | Selected Mozilla release |
|---|---|---|
| Original-source provenance | Published release and historical official routes | Identified publisher-hosted derived release |
| Current acquisition | Retained archive requests failed; no verified alternative | Page available; payload access unverified; metadata requests returned 403 |
| Download size | Approximately 50.59 GiB, catalog-reported | Approximately 6.97 GB, publisher-reported |
| Extracted size | Unverified | Unverified |
| Representation | Historical SPH/STM | Publisher reports MP3/TSV |
| Group metadata | Original inventory unavailable | Speaker/prompt fields documented generally; exact sidecars unavailable |
| License | Historically documented CC BY-NC-ND 3.0 | Publisher reports CC0-1.0, with platform access/use conditions |
| Qualification | Not qualified | Not qualified |

**FACT:** CC0 addresses copyright and related rights within its scope; it does not establish that privacy, third-party rights, or separately accepted platform conditions are irrelevant. [CC0 legal text](https://creativecommons.org/publicdomain/zero/1.0/legalcode.en)

**FACT:** Mozilla’s consumer terms require the applicable account/access process and dataset terms. They restrict reidentification and unauthorized redistribution. The publisher separately explains its prohibition on rehosting Common Voice datasets. No account, terms acceptance, access request, payment, or download was initiated. [Consumer terms](https://mozilladatacollective.com/terms/consumers), [Rehosting explanation](https://community.mozilladatacollective.com/faq-why-cant-i-re-host-or-share-common-voice-datasets-that-i-download-from-mdc/)

**PROPOSED NEXT ACTION:** If public metadata remain unavailable, the owner must personally determine whether to establish/sign into an MDC account, accept the applicable terms, and request permitted metadata access. An API credential is optional and requires separate authorization. Account creation must not be presumed to resolve the observed 403 responses.

Derived ASR hypotheses, illustrative examples, and public record-level artifacts require a specific terms assessment before publication. Aggregate results, hashes, and reproducibility code should be planned without assuming that raw prompts, audio, or dataset copies may be republished.

## F. Speaker, prompt and derivation-family grouping verdict

**DECISION:** Preserve connected source-family closure. Do not substitute speaker-only grouping.

Common Voice recordings are readings of supplied prompts. Different speakers can therefore share the same underlying text. The general schema includes `client_id`, `sentence_id`, `sentence`, and potentially sentence-source metadata; these fields have different meanings and are not interchangeable independence guarantees. [Official scripted-speech schema](https://github.com/common-voice/cv-dataset/blob/main/datasets/scripted-speech/README.md)

The required graph must connect records through:

1. Equal publisher speaker identifiers.
2. Equal recording identities, aliases, or verified duplicate-audio hashes.
3. Equal prompt identifiers or exact normalized prompt text.
4. The prospectively specified near-duplicate rule below.
5. Known shared or derived underlying document, book, article, talk, or other source material.

Use transitive closure. A speaker linked to several prompts can connect their other speakers and source families into a much larger component.

**Do not equate an entire publisher, release, or topic category with one underlying work.** Conversely, a coarse source label such as “Wikipedia” does not establish article-level provenance. Missing lineage is unresolved information, not evidence of independence.

### Prospective textual-family rule

This decision explicitly extends the repository’s existing leakage rule for short scripted prompts:

- Form leakage-signature tokens using **Unicode NFC, casefolding, and the existing Unicode `\w+` tokenization**.
- Link exact signatures at **every nonempty length**.
- Retain the existing **minimum-20-word, word-5-gram Jaccard ≥0.90** rule.
- Additionally link two nonempty, space-joined signatures \(s,t\) when their Unicode-character Levenshtein distance satisfies:

\[
d(s,t)\leq \left\lfloor0.10\max(|s|,|t|)\right\rfloor.
\]

These rules are combined with **OR**, alongside the identifier and provenance links.

**PROPOSED DESIGN:** The additional fixed rule conservatively covers highly similar short prompts. It is not a claim to detect every semantic paraphrase. Known derivation links remain mandatory, and an independent review must assess whether the available provenance supports the intended family claim.

This normalization is for leakage analysis only. It must not rewrite references, model inputs, or the registered scorer.

No threshold search, edge removal, prompt-frequency filtering to break components, or alternative grouping may be used to obtain enough cases.

## G. Case/group sufficiency and uncertainty

**UNVERIFIED:** Eligible case counts, connected-component counts, and capped capacity are presently unavailable.

The publisher’s 3,244 TRAIN speakers are not 3,244 independent components. The complete graph could contain substantial transitive merging. A giant component remains one component and contributes at most 60 admitted cases.

Required populations remain:

| Role | Cases | Minimum independent components |
|---|---:|---:|
| FIT | 4,000 | 80 |
| SELECT | 2,000 | 40 |
| EVAL | 6,000 | 100 |

Meeting a total component count is insufficient: the fixed hash assignment, component cap, case ranking, and resulting selected populations must satisfy every role separately.

**INFERENCE:** The advertised clip supply is large enough to justify a metadata census. It does not establish that 12,000 admissible cases exist under the actual independence contract.

### EVAL information gate

The v3 requirement of **100,000 reference words and 1,000 RAW errors** remains binding.

**CALCULATION:**

- 100,000 words across 6,000 cases requires **16.67 words per case**.
- Publisher-reported TRAIN hours and clips imply approximately **4.92 seconds per clip**.
- If selected EVAL had that mean duration, reaching the word gate would imply approximately **203 words per minute**.

This calculation is a planning warning, not a prediction of the selected population. Short prompted clips create a material risk that the word gate will fail.

The reference-word count can be checked from the fixed provisional allocation when permitted metadata become available. RAW-error sufficiency cannot be established without separately authorized source construction.

Neither gate may be rescued by selecting longer prompts, concatenating clips, changing quotas or salts, or replacing cases after outcomes.

## H. Reference and recognizer construction verdict

**PROVISIONAL reference field:** The publisher’s `sentence` field, preserved exactly after a verified TSV parse.

The general schema describes this as the prompt to be read. Community validation supports its intended correspondence to speech, but it does not prove perfect verbatim acoustic transcription. The study must therefore retain a reference-conditional lexical claim and must not infer acoustic truth from text alone. [Common Voice primary paper](https://aclanthology.org/2020.lrec-1.520.pdf)

Before qualification, establish:

- Exact curated-archive headers, encoding, escaping and null conventions.
- Whether `sentence_id`, duration and source-provenance sidecars are included.
- Whether reference conflicts or aliases occur.
- What publisher validation and exclusion markers mean for this release.
- Whether duration metadata describe the complete original clip.

The general schema’s `segment` field is a dataset category, **not a start/end timestamp pair**. General upstream documentation is not proof that every described sidecar exists in this curated archive.

**DECISION:** Do not invent punctuation cleanup, annotation removal, case restoration, or reference normalization. Preserve the registered lexical scorer separately.

The retained recognizer identity is:

- `mlx-community/parakeet-tdt-0.6b-v3`
- Revision `ed2b7e8c15f9aaa0b5772e2efb986255eaef7e15`
- Qualified runtime: `parakeet-mlx-0.5.2-frame-bound-v1-single-fp32-wave-bf16-weights`

**FACT:** Its prior qualification does not automatically qualify this MP3 source boundary. Codec decoding, channel handling, resampling, and exact full-clip duration require later independent verification.

The prospective construction should preserve the full clip and frozen loader’s mono 16-kHz PCM16 representation. Decoder/resampler identities must be bound before recognition. No trimming, stitching, quality-based retry, or source replacement is authorized.

## I. Scientific domain-shift implications

**DECISION:** Prompted speech narrows the population claim but does not invalidate the source-only acceptance hypothesis.

A successful experiment would establish capability on the frozen, publisher-selected Common Voice British-English population. It would not establish:

- Universal speech correction.
- A TED-talk result.
- A clean within-domain replication of G2.
- Representative performance for all British speakers or accents.
- Independence from unknown upstream model pretraining.

The accent selection is based on supplied tags and includes mixed labels. Treat the release as a fixed publisher-selected population; do not silently reinterpret it as a verified demographic or accent census.

The 2,696-case G2 DEVELOPMENT panel remains consumed historical evidence. It must not contribute cases, threshold selection, or pooled outcomes to prospective EVAL.

**INFERENCE:** The historical ByT5 oracle headroom—109 errors across beneficial whole-output proposals—supports one bounded attempt to qualify fresh data. It does not predict transferable benefit or justify indefinite acquisition effort.

## J. Storage and compute feasibility

**CALCULATION:** If the rounded 6.97-GB figure uses decimal units, it corresponds to approximately **6.49 GiB**. This is materially smaller than the catalog-reported TED-LIUM archive.

It does not establish a complete storage budget.

The required high-water accounting is:

\[
H=A+X+P+O+M+T+F+C\leq80\text{ GiB},
\]

where:

- \(A\): retained downloaded archive.
- \(X\): extracted audio and source metadata.
- \(P\): selected decoded audio.
- \(O\): ASR, proposal and conditional-score outputs.
- \(M\): qualification and scientific manifests.
- \(T\): simultaneous temporary files.
- \(F\): retained failed attempts.
- \(C\): any incremental cache or model-artifact duplication.

**CALCULATION:** Twelve thousand 12-second clips stored as mono 16-kHz PCM16 require at most approximately **4.292 GiB**, excluding headers. This bound does not cover compressed originals, intermediate representations, or duplicate buffers.

**UNVERIFIED:** Exact archive bytes, extracted bytes, temporary-file behavior, failed-attempt reserve, and the complete experimental peak remain unknown.

**STORAGE_FEASIBILITY_UNVERIFIED**

A later plan must inventory the archive and demonstrate selective extraction or another explicit bounded sequence. Do not download the approximately 89-GB parent English corpus to repair missing metadata. Do not create a TFDS conversion, delete G2 evidence, thin snapshots, or increase the ceiling.

The proposed metadata prerequisite retains a limit of **one working day, two CPU-compute hours, and 8 GiB working memory**. Inability to compute exact closure within those limits is a reported blocker; approximate edge omission is not permitted.

## K. Selected data-source direction

**PROPOSED NEXT ACTION:** Conduct, after separate owner authorization:

`POST_FEASIBILITY_CV26_BRITISH_METADATA_QUALIFICATION_V1`

Its first objective is to establish whether authoritative metadata can support the required census and provenance checks **before acquiring audio**.

Do not run parallel searches for additional corpora. Do not continue TED-LIUM recovery within this prerequisite.

If this candidate cannot satisfy the unchanged independence and population requirements, return that failure to frontier review. Sol must not substitute another dataset or weaken the contract.

## L. Exact bounded next qualification protocol

### Phase 1 — Metadata and provenance qualification

This phase is designed here but **not executed or automatically authorized**.

**1. Bind the release.** Record the exact dataset ID, curator, parent release, listed archive name, immutable file/version identifier if available, expected checksum, exact bytes, publication date, terms versions and official acquisition route. A filename or “Latest Version” label alone is insufficient.

**2. Establish permitted metadata access.** Use public documentation and metadata endpoints or metadata already lawfully supplied by the owner. Do not initiate account actions, download archives or samples, accept terms, or bypass access controls. If required metadata are unavailable, stop with a precise metadata request.

**3. Restrict case eligibility to publisher TRAIN.** DEV and TEST contribute no admitted cases. Their metadata may be used solely for graph bridges and exclusion checks where available and permitted.

**4. Require a complete relevant metadata census.** Necessary fields include clip identity/path, speaker identifier, prompt identifier and text, locale, duration, known source lineage, and available duplicate-recording identities. A sample cannot establish full connected components.

**5. Construct closure before filtering or capping.** Apply Section F across the complete available release metadata. Preserve bridge records even when they later fail duration eligibility. Do not split components by discarding bridge cases.

**6. Bind stable IDs.** Use SHA-256 of canonical UTF-8 JSON, without optional whitespace:

```text
["RWR_CV26_BRITISH_CASE_V1",
 "cmrt6zrob000zmm07yqwjlpwi",
 "cv-corpus-26.0-2026-06-12",
 "en",
 "<exact publisher relative clip path>"]
```

The displayed formatting illustrates the array; serialization must be fixed and independently reproduced. Reject ambiguous paths, aliases, missing required identifiers, and conflicting duplicate identities.

Define each component ID as SHA-256 of:

```text
RWR_CV26_BRITISH_COMPONENT_V1\n
<sorted member stable IDs, separated by newline, without a trailing newline>
```

Freeze the graph universe and release identity before deriving these IDs.

**7. Apply project exclusions to whole components.** Compare only permitted existing identifiers, hashes, lineage metadata and leakage fingerprints against G1 TRAIN, G2 D1 TRAIN, consumed DEVELOPMENT, and permitted protected-family metadata.

Do not open protected references or derive new fingerprints from them. If existing protected metadata cannot support the necessary comparison, stop and identify exactly what is missing. Different dataset names do not establish independence.

**8. Verify duration metadata.** Preliminary eligibility requires complete-clip durations inclusively between 2,000 and 12,000 milliseconds, with authoritative units and semantics. Rounded catalog summaries are insufficient. Final audio verification remains deferred.

**9. Preserve v3 allocation.**

- Component assignment: SHA-256 of `POST_FEASIBILITY_ACCEPTANCE_V1|<component_id>`, interpreted as an unsigned integer, modulo six.
- Remainders 0–1: FIT; 2: SELECT; 3–5: EVAL.
- Case ranking: SHA-256 of `POST_FEASIBILITY_CASE_V1|<stable_id>`.
- Apply the existing 60-case component cap and exact v3 ranking/selection order.
- Require 4,000/2,000/6,000 selected cases and 80/40/100 selected components.

No rebalance, alternate salt, reshuffle, or quota relaxation.

**10. Check the fixed EVAL word count.** Use the registered lexical scorer on the fixed provisional selection, solely as a population-information check. Keep reference contents out of acceptance-policy design. Failure of 100,000 words stops qualification.

**11. Produce a complete storage forecast and independent review.** Independently reproduce parsing, identifiers, graph closure, exclusions, assignments, capped counts, reference-word totals and storage arithmetic through a separate code path when execution is separately authorized.

### Phase 2 — Potential bounded acquisition

**NOT AUTHORIZED by this decision.**

If Phase 1 cannot proceed without an official metadata package or corpus archive, request separate owner approval identifying:

- Exact publisher artifact and access conditions.
- Expected checksum and bytes.
- Private destination and retention obligations.
- Full 80-GiB high-water accounting.
- Permitted extraction and inspection scope.
- Attempt handling and stop conditions.

Prefer a publisher-provided metadata-only artifact. If only the complete archive exists, acquisition approval must explicitly cover that fact. Extract and inspect metadata before expanding audio.

Before any later Parakeet recognition, independently verify audio identities, complete-clip boundaries, decoding/resampling, final duration eligibility, reference semantics, exclusions, population sufficiency, and the storage plan. Acquisition success alone does not admit the experiment.

## M. Acceptance and stop criteria

Metadata qualification succeeds only when every required binding is established, reproducible and independently reviewed.

Stop if any of the following occurs:

- Official access or required terms cannot be established.
- Exact version, expected artifact identity or complete metadata are missing.
- Speaker, recording, prompt or derivation-family closure cannot be supported.
- Protected-family exclusion requires forbidden reference access.
- Exact/near-duplicate coverage remains materially unresolved.
- Any fixed role lacks cases or independent components.
- Provisional EVAL contains fewer than 100,000 reference words.
- Reference conventions require an invented interpretation.
- Storage feasibility cannot be established within 80 GiB.
- Completing the prerequisite requires prohibited acquisition, writes, model work or additional scientific choices.

A giant component is a valid negative qualification result.

The later 1,000-RAW-error gate remains prospective. It must not become outcome-based case selection or trigger EVAL top-ups.

Independent review must settle unresolved population bindings **before model work begins**.

## N. Prospective scientific amendment — copy-ready text

```text
POST-FEASIBILITY FRESH-DATA SOURCE AMENDMENT V4
Date: 2026-10-10

Reviewed documentation checkpoint:
b432690ca137f4fb4946f3fe5579a6b6069844f1

Frozen scientific checkpoint:
609f97f31979d469ad8551d06b2c07c3513181ec

Disposition:
AUTHORIZE_ALTERNATIVE_CORPUS_QUALIFICATION_DESIGN

This amendment selects exactly one alternative fresh-data candidate:
Mozilla Common Voice Scripted Speech 26.0 — British English,
Mozilla Data Collective dataset cmrt6zrob000zmm07yqwjlpwi.

The publisher identifies parent release cv-corpus-26.0-2026-06-12,
locale en, and archive
common-voice-scripted-speech-26-0-britis-0fe481c3.tar.gz.
Exact artifact bytes, checksum, inventory, accessibility and population
properties remain subject to qualification.

TED-LIUM 3 legacy TRAIN remains NOT QUALIFIED. Immediate recovery work
is suspended. No additional corpus search or substitution is authorized.

The next designed prerequisite is:
POST_FEASIBILITY_CV26_BRITISH_METADATA_QUALIFICATION_V1.

Only publisher TRAIN records may become cases. Publisher DEV and TEST
records are excluded from admitted populations; permitted metadata may
be used to preserve graph bridges and detect overlap.

Independence remains defined by connected speaker, recording, prompt
and underlying source/derivation families. Speaker-disjoint publisher
splits alone do not satisfy this requirement.

Leakage signatures use the existing Unicode NFC, casefold and Unicode
word-token convention. Exact signatures link at every nonempty length.
Retain the registered minimum-20-word, word-5-gram Jaccard >=0.90 rule.
Additionally link nonempty space-joined signatures s and t when their
Unicode-character Levenshtein distance is at most
floor(0.10 * max(length(s), length(t))).
These rules are combined with identifier, duplicate-audio and known
source-derivation links. This leakage normalization does not rewrite
references, model inputs or scoring.

Construct full transitive closure before eligibility filtering,
component caps and role assignment. Do not remove bridge records,
cut edges, replace components with speakers, tune duplicate thresholds
or relax source-family exclusions to reach quotas.

Sections L and M of the complete Frontier Source Decision v4 bind
stable identifiers, metadata scope, exclusion checks, reference and
duration qualification, stage separation, review and stop conditions.
That complete decision must accompany this amendment.

Preserve the v3 hash assignment, case ranking, 60-case component cap,
FIT 4,000 / SELECT 2,000 / EVAL 6,000 populations and minimum
80 / 40 / 100 independent components. Preserve the EVAL information
gates of 100,000 reference words and 1,000 RAW errors. No outcome-based
selection, top-up, reallocation or quota relaxation is permitted.

The proposed reference field is the original publisher sentence field,
conditional on verified parsing and semantics. No invented text cleanup,
annotation removal or acoustic-truth assertion is authorized.

The changed prospective domain is publisher-selected prompted speech.
Any future result applies to that frozen population. Historical G2
DEVELOPMENT remains consumed, immutable and excluded from prospective
EVAL.

The fixed ByT5 proposer, exact ten-pass checkpoint, source-only input,
whole-output choice, mandatory RAW fallbacks, conditional-score
comparison, exactly two ridge fits, registered selection logic,
success gates, failure-inclusive evaluation and group-aware uncertainty
remain unchanged under v3 Sections O2–O10, P and Q.

This is scientific DESIGN ONLY. Phase 1 is metadata/provenance
qualification. Phase 2 acquisition requires separate owner approval.
Neither phase authorizes Parakeet recognition, ByT5 generation,
conditional scoring, policy fitting or final evaluation.

The Phase 1 design is bounded to one working day, two CPU-compute hours
and 8 GiB working memory. The prospective experiment retains the
80-GiB incremental high-water ceiling, including archives, extraction,
temporary files, failed attempts and retained outputs.

Account creation, terms acceptance, access requests, credentials,
payments, downloads, implementation and repository publication require
their own explicit owner authorization. Protected references may not
be opened.

All historical scientific evidence remains immutable. Continuation
automation remains paused. Generation 3, final training, sealed
inference and protocol freeze remain unauthorized or held.

Qualification failure returns to frontier review. Successful metadata
qualification does not automatically admit or launch model work.
```

## O. Sol handoff for the next prerequisite only

This handoff is executable **only after separate owner authorization** for the stated prerequisite.

```text
FRONTIER-MODEL ESCALATION RULE

You are Sol, the implementation and analytical execution model.
Execute only the owner-authorized scope of
POST_FEASIBILITY_CV26_BRITISH_METADATA_QUALIFICATION_V1.

If completion requires an unbound scientific choice, another dataset,
weaker grouping, protected references, acquisition without approval,
repository writes, model work or policy fitting, stop and report
FRONTIER_MODEL_REVIEW_REQUIRED. Give the exact blocker, primary
evidence, missing authority and smallest adjudication options.

IDENTITY AND SCOPE

Repository:
/Users/danny/Documents/Tools/LocalFlowResearch

Project:
Repair Without Rewrite: A Controlled Comparison of Full-Transcript
Generation and Compact Editing Under Matched Source Exposure

Expected documentation checkpoint:
b432690ca137f4fb4946f3fe5579a6b6069844f1

Expected documentation branch:
codex/post-feasibility-v3-record

Frozen scientific checkpoint:
609f97f31979d469ad8551d06b2c07c3513181ec

Perform bounded metadata/provenance qualification only.
This prompt supplies no acquisition or model-execution permission.

WHAT ELSE IS IN FLIGHT

Own no repository files. Do not switch branches or modify the worktree.
Preserve all scientific evidence and the paused continuation automation.
Do not begin acceptance implementation, inference, fitting, evaluation,
Generation 3 or final/sealed work.

STARTUP ORDER

1. Read AGENTS.md.
2. Verify current HEAD, branch, index and clean worktree. If a later
   documentation checkpoint exists, establish its authorized ancestry.
3. Read the complete Frontier Source Decision v4 and its amendment.
   If either is unavailable, stop; do not reconstruct it from this prompt.
4. Read:
   docs/reviews/FRONTIER_POST_FEASIBILITY_SCIENTIFIC_DECISION_V3.md
   docs/reviews/FRONTIER_POST_G2_SCIENTIFIC_DECISION_V2.md
   docs/reports/POST_G2_READ_ONLY_TASK_FEASIBILITY_V1.md
   and the complete preceding Fresh Data Qualification v1.
5. Verify supplied scientific identities without reviewing main as a
   substitute for the frozen campaign.
6. Resume from existing verified receipts if this prerequisite is
   already partly complete; do not repeat access failures indefinitely.

EXACT CANDIDATE

Mozilla Common Voice Scripted Speech 26.0 — British English
Publisher ID: cmrt6zrob000zmm07yqwjlpwi
Parent: cv-corpus-26.0-2026-06-12, locale en
Listed archive:
common-voice-scripted-speech-26-0-britis-0fe481c3.tar.gz

Publisher page:
https://mozilladatacollective.com/datasets/cmrt6zrob000zmm07yqwjlpwi

API documentation:
https://mozilladatacollective.com/api-reference/docs

The prior review obtained HTTP 403 from the public dataset-summary and
metadata endpoints. No checksum, exact bytes or row census was obtained.
Do not infer that an account will resolve this response or bypass it.

WHAT TO SETTLE

Establish official artifact identity, lawful metadata access, exact
reference conventions, duration metadata, complete family closure,
project exclusions, fixed population counts and storage feasibility.

Apply v4 Sections F, L and M exactly. Preserve all speaker, recording,
prompt and known source-family connections, including transitive bridges.
Use TRAIN only for cases. Never equate speaker counts with components.

Preserve v3 role hashing, ranking, 60-case cap and exact 4,000/2,000/6,000
cases with at least 80/40/100 selected components. Check the fixed EVAL
reference-word gate when permitted metadata support it. RAW-error
sufficiency remains unavailable without later authorized recognition.

Use only already permitted protected-family metadata. Do not open
protected references or generate new fingerprints from protected text.
Missing exclusion coverage is a blocker.

CONSTRAINTS

One working day; at most two CPU-compute hours and 8 GiB memory.
Read public documentation/metadata and already permitted local evidence.
No corpus/model payload downloads, samples, account actions, terms
acceptance, credentials, payments or access requests.
No persistent analysis files, repository edits, tests, benchmarks,
commits, pushes, automation changes, model loading or forward passes.
No human annotation or listening. No alternative corpus search.

If required row metadata exist only inside an archive, stop and specify
the exact separately approvable metadata/acquisition request.
Phase 2 is not authorized.

VERIFICATION

Distinguish FACT, VERIFIED, CALCULATION, INFERENCE, UNVERIFIED and
PROPOSED NEXT ACTION. A publisher claim is not an inspected property.
An unrun check is never PASS. Report unavailable bindings explicitly.
Any eventual census requires independent verification before model work.

CLOSEOUT

1. Report exact reviewed identities, sources and access results.
2. Report qualified and unresolved bindings separately.
3. Report case/component capacity only when the complete required census
   and fixed assignment have actually been verified.
4. Report full high-water accounting or STORAGE_FEASIBILITY_UNVERIFIED.
5. State the smallest next owner/Astra action; do not execute it.
6. Verify unchanged repository, index, branches and orchestration.
   State which private-artifact checks were not performed.
7. Return the report in the conversation and stop with:
FRONTIER_MODEL_REVIEW_REQUIRED
```

## P. Explicit authorizations still required

The following remain separate decisions or owner actions:

1. Recording and publishing this decision and amendment.
2. Executing the bounded metadata prerequisite.
3. Account setup, terms acceptance, access requests or credential use.
4. Any metadata-package or audio acquisition.
5. Implementation and execution of later parsing, audio qualification and independent verification.
6. Frontier acceptance of all remaining population/reference bindings.
7. Parakeet source construction.
8. ByT5 generation, conditional scoring, policy fitting and one-time evaluation.

No successful prerequisite automatically grants the next authorization.

## Q. Prohibitions and next scientific boundary

**VERIFIED:** Repository HEAD, index, tracked contents and inspected branch identities remained unchanged. The continuation automation remained **PAUSED**, with unchanged configuration hash.

No repository files were written. No tests, benchmarks, downloads, account actions, protected-reference access, model loading, inference, fitting, commits, pushes or automation changes were performed. Private scientific payloads were not accessed; their complete integrity was not independently re-audited here.

The next scientific boundary is **a complete, independently checked source-population binding**. The selected candidate must earn qualification through provenance, reference correctness, connected-family independence, fixed population sufficiency and storage feasibility.

If it fails, retain that result. Do not weaken the evaluation to preserve the experiment.

**AUTHORIZE_ALTERNATIVE_CORPUS_QUALIFICATION_DESIGN**
