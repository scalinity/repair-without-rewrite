# Bounded foundation decision — no freeze

**Foundation repair is required before preparing PUB-GATE 3.** Correctness and scoped native execution are evidenced; useful held-out restoration, a credible adapted comparator, full source qualification and the one-month campaign are not established. No final campaign or freeze is authorized by this report.

Owner-specified working paper title: *Repair Without Rewrite*. Subtitle: *A Controlled Comparison of Full-Transcript Generation and Compact Editing Under Matched Source Exposure*.

## Required readiness answers

1. **Did scorer correctness pass for development?** Yes, for the implemented word-level arithmetic. [Scorer qualification](SCORER_FOUNDATION_REPORT.md) covers 21 red/green fixtures, 3,375 exhaustive triples, 10,000 fixed-seed trials, independent all-path review, normalization, failure mapping and fixed eligibility. The [final integrated suite](raw/final_foundation_tests_attempt01.txt) passed 180 tests in 18.64 s. Natural literal extraction, full population joins and statistics remain unqualified; this is not PUB-GATE 2.

2. **What fraction has exact joint scoring versus bounds/caps?** The [502 synthetic cases](../../experiments/scorer-profile-attempt01/summary.json) all finished joint computation; 501/502 had point totals, one had a sharp interval, zero capped. In the [12 real DEV source audit](../../experiments/public-dev-source-score-attempt02/summary.json), each reference field had 10/12 finished joint computations and 2/12 joint-state caps. All 12 RAW identity totals are provably zero repair/introduction, including the two closed-form cap results; local joint correspondence remains unavailable on those rows. O=S cannot estimate candidate-output coverage. No final population coverage estimate exists.

3. **Are ambiguity widths small enough for H1?** Unknown. Synthetic maximum repair width was one, with 27 local ambiguities. Neither that restricted sample nor real-source identity outputs establishes the paired H1 precision or the introduced-error margin. Natural nonidentity DEV outputs and cluster-aware uncertainty are required.

4. **Did MODEL-0 pass the ladder?** [V0–V5, V7 and V8 passed](MODEL0_CORRECTNESS_REPORT.md), including exact 8,621,312 parameters and independent NumPy math. V6 real-shard ≥10M convergence is NOT_RUN. The 16,384-entry permitted-corpus tokenizer is not trained. Thus the complete ladder did not pass.

5. **Did B/C contracts pass?** Yes in the declared mechanical scope: exact counts 100,686,336 / 101,081,859; source/cross/causal masks, pointer/events, byte-bound source renderer, canonical labels and whole-update component normalization. [B/C report](BC_CORRECTNESS_REPORT.md) preserves the independently found source-binding repair. Both exact models memorized 4/4 matched pairs after a failed aggressive recipe. This is not held-out correction.

6. **What are sustained B/C rates?** Not measured. [Six short samples](BENCH00_NATIVE_CALIBRATION.md) ran 20 timed updates each after five warmups: B mean 0.114881–0.124798 s/update, C 0.118924–0.204125 across event densities. Only the decoder geometry has a 20-minute segment: 4.325589 updates/s on four fixed blocks. Those are distinct workloads and noncanonical exposure units.

7. **What is peak memory?** B/C short samples peaked at 2.551–3.042 billion MLX allocation bytes. Decoder training-phase maximum was 2,888,425,680 bytes; whole-run dual-trainer peak 4,499,394,776. ByT5 RSS was 2,713,403,392; Qwen maximum observed driver allocation 8,389,722,112. [Speech allocator/RSS views](ASR_TTS_NATIVE_PROBE.md) are separate. These views overlap and are not summed; full-machine pressure/swap qualification is missing.

8. **B/C decode rates on representative lengths?** Unqualified. Four random B calls hit cap32 in 0.138700–0.157390 s; two random C calls abstained at one position in 0.012981–0.014230 s, without rendering. The exact memorization outputs are two-byte fixtures. Neither result establishes valid representative-length throughput or a speed advantage.

9. **Useful held-out correction at 10M?** NOT_RUN. [The admission report](BC_10M_DEVELOPMENT_PROBES.md) identifies missing source/training/tokenizer, V6 and representative BENCH prerequisites. No recipe slot is consumed and no candidate result is fabricated.

10. **Identity collapse?** The first B memorization rehearsal emitted capped repeated `a`; C damaged an identity example. The repaired rehearsal completed all four outputs exactly. Identity collapse/aggressive rewrite on held-out natural data or at 10M remains unknown. Teacher-forced loss alone failed as an output-success proxy.

11. **Are three LR candidates informative?** Unknown; the seed42 10M recipes at 1e-4, 3e-4 and 6e-4 have not run. The isolated LR0.003→0.0003 memorization repair also changed update count and is not a controlled LR sweep.

12. **Is 150M adequate?** Unknown. No held-out learning curves or canonical-exposure calibration exist. Retain the prospective endpoint pending permitted-data/V6/10M evidence; amend before freeze if those curves fail to support the finite-budget question. Do not infer adequacy from memorization.

13. **Is ByT5 adaptation credible?** Not yet. Exact official weights and native byte/loss/backend paths passed engineering checks, but all four pre/post decode calls capped and produced invalid prefixes after ten synthetic updates. [The complete evidence](COMPARATOR_AND_PRIOR_WORK_QUALIFICATION.md) supports feasible execution, not adequate adaptation or impossibility. A useful DEV recipe and disclosed budget remain necessary.

14. **ConstDecoder outcome?** Concrete official-code/task incompatibility: old CUDA-forced Torch/Transformers path, semantic-parsing targets and incomplete task assets. The initial bounded scan did not justify opening the conditional port budget. No open-ended reproduction or invented active-human hours were charged.

15. **Are public policies usable?** Partially. LS-PC metadata/rights and full book/project closure are established. `text` versus `text_raw` remains provisional. SLUE TSV/license files returned 401 behind an agreement/contact gate; actual rows/audio are zero. [Source report](PUBLIC_SOURCE_QUALIFICATION.md) records these conditions. Two measured MLX Parakeet outputs are long repeated `<unk>` strings; further representative source construction is stopped pending diagnosis. Preprocessing equivalence to NVIDIA/NeMo is unqualified. Current counts apply only to that exact development runtime. Neither planned primary population is fully admitted.

16. **Actual source-error denominators and clusters?** The 12-group, 67.705-s DEV panel has 12 API-completed hypotheses. Both fields have 198 reference lexical tokens and eS=3,094, RAW WER=15.626263 (1,562.626%). The two repeated-unknown sources account for 3,090 errors; no row is dropped. Source masks count 176 certainly correct / 22 certainly erroneous reference occurrences. [Dual-field audit](../../experiments/public-dev-source-score-attempt02/summary.json) preserves all records; lexical agreement between fields here does not settle formatted-target choice. Metadata roles are HPO898/12, sealed5,273/19, excluded4,671/2; no admitted bounded training/calibration rows. SLUE eS is unavailable and the fixed equal-domain endpoint undefined.

17. **Scorer cost?** The synthetic profile took 3.703143 s for 502 cases including tracing/export; maximum 23,969 states / 91,520 edges. The 24-record dual-field natural source audit took 128.260990 s, traced peak326,243,099 bytes / RSS683,229,184, with two250,000-state caps per field. Maximum completed graph edges33 excludes unavailable capped graphs. Identity counts remain exact despite caps. CPU tests/coding could overlap; this repeated dual-field identity workload does not price final outputs or paired bootstrap, which is NOT_MEASURED.

18. **Does H1 fit ≤30 days from this state?** Not established. [The prerequisite calendar](BENCH00_NATIVE_CALIBRATION.md) starts with approved access/field/grouping and permitted training/tokenizer supply, then V6/representative calibration, useful paired probes/comparator adaptation, DEV precision/cost and owner review. No unsupported month forecast replaces these dependencies.

19. **Device hours with 25% reserve?** Not estimable in the registered workload. A qualified operation ledger would be multiplied by 1.25. Current synthetic rates, failed decodes and two-utterance TTS cannot price the six final B/C runs, natural/stress inference, credible comparator, transfer and statistics. Actual spent operation intervals are recorded separately in [the session report](BOUNDED_FOUNDATION_SESSION_REPORT.md).

20. **Active researcher time remaining?** Unknown. No human active-time clock or qualified remaining-task estimates exist. Agent execution wall time is not active researcher time; the ConstDecoder cap is an authorization bound, not time spent.

21. **Keep H2 stretch?** Yes. Original CPU TTS and pinned MLX ASR execute locally, but alternate MPS TTS original-path parity failed, target fidelity/screening/common-support/yield and longer distributions remain unqualified. H1 text readiness stays independent of H2 common-support.

22. **Keep A100 stretch?** Yes. Decoder geometry cost is useful engineering evidence, but it does not justify adding its final campaign to an unpriced H1 core. No final A100 run occurred.

23. **Is the proposed 2,400 stress panel adequate?** Not yet established. [The restricted 288-case DEV grammar](STRESS_GENERATOR_FOUNDATION.md) covers all eight categories/four cells/three views; source-only inverse succeeds 288/288, with 89 unique references and explicit duplicate/strong-baseline limits. Cross-partition typed bundles were repaired independently; semantic-family/near-duplicate and broader composition qualification remain pending. The final 2,400 cases are not generated/frozen or demonstrated sufficient for claims.

24. **Is B/C-only Whisper affordable?** Unknown. No pinned native Whisper timing/admission sample or qualified eligible transfer ledger exists. Keep transfer conditional on measured cost; do not extrapolate Parakeet timing to Whisper.

25. **What remains for F01/F02/F03?** F01 primary predecessor verification/controlled-extension positioning is complete prospectively; integrate it before freeze. F02 needs the qualified H1 scope, learning/precision evidence and prerequisite-aware reserved budget. F03's legitimate-empty distinction/accounting works in development; reconcile the working registry before source/final freeze. [Prospective amendments](../reviews/PROSPECTIVE_AMENDMENTS.md) additionally require actual full-parent grouping, explicit LS-PC field choice, natural literal/statistical qualification and precise backend-path disclosure. Immutable supplied files are unchanged.

The next authorized repair dependency is source/reference/training-supply qualification, followed by tokenizer/V6/representative native calibration. A separately requested access agreement, new annotation, final inference, freeze or final training must wait for owner authorization. All failed attempts remain evidence. No result demonstrates paper readiness or invalidates the entire research question.

FOUNDATION_REPAIR_REQUIRED
