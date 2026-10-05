# Independent Parakeet numerical/source review

Reviewed 2026-10-05. This reviewer wrote and ran a separate CPU reference audit, inspected the installed package and the implementation owner's raw replay/intervention artifacts, and did not run MLX inference, change dependencies, generate training pairs, or touch sealed/final inputs. The research baseline was `c81d08f95566d1e797f14a6217286e5dfcf33ab5`; implementation/review files remain distinct from that baseline.

**Decision: QUALIFIED_WITH_NARROWED_RUNTIME. R1 is resolved.** The frame-bound intervention removes a concrete invalid memory-access geometry, produces finite ordinary transcripts for the unchanged cohort twice, and adds guards that refuse numerical failure instead of emitting apparently valid source text. Qualification is confined to the explicit single-item 2–12-second development contract with the same pinned inputs/runtime and common hypotheses. It does not establish NVIDIA/NeMo transcript equivalence or qualify untested long-input inference. Known frontend deviations must remain part of the explicit development recognizer identity.

## Findings and disposition

**R1 — qualification boundary must match evidence, RESOLVED.** The initial adapter admitted `(0,60]` seconds, but the whole-model evidence covers the preselected 2–12-second cohort, actually 2.35–10.41 seconds. The implementation owner subsequently narrowed its guard to exactly 16 kHz and 32,000–192,000 samples. This reviewer independently executed CPU-only acceptance/rejection checks at both boundaries and invalid rates/types and inspected the added regression. Longer/shorter inputs remain unqualified. The 24-call receipt precedes this narrowing-only change; no frontend/decoder math changed, and every retained case lies inside the narrower contract. No extra long-input source construction is inferred.

**R2 — retained frontend math differs materially from the authoritative reference, disclosed limitation.** A frame-only repair can define a scientifically usable development source generator if its identity is explicit and all correctors receive identical frozen hypotheses. It cannot be labeled faithful NeMo preprocessing. A full frontend-parity intervention would be a separate attempt/configuration and should not be pooled with the frame-only causal experiment.

**R3 — original NaN creation point remains unobserved, disclosed limitation.** The instrumented original path was finite on both formerly pathological clips. This is consistent with memory allocation/execution perturbation; it cannot serve as a captured original NaN onset. The defect is established independently, and the intervention/mechanism evidence is strong, but the report must distinguish a demonstrated bounds defect and effective repair from proof of the exact invalid bytes consumed in the original failure.

## Independently verified identities and inputs

All seven cached model assets matched the original manifest's byte sizes and SHA-256 values. The weight file has **627,052,166 F32 parameters on disk**; BF16 runtime weights arise from `from_pretrained` casting. The model/config/tokenizer identities therefore did not change during this review:

| Asset | SHA-256 |
| --- | --- |
| model.safetensors | `05e01c7f396c298cf7d23f61da7b504adeab698f0aaeafd9c82d198625464592` |
| config.json | `f320f1292511f34ec47f513755fe20fd01dbfc09a925d42730e66059a6e1ef4c` |
| tokenizer.model | `eacec2b0a77f336d4a2ca4a25a7047575d3c2b74de47e997f4c205126ed3135e` |
| tokenizer.vocab | `41130ff456706304a1adec782ccc9e003c4d417e8e324353d281be958cac4e17` |

The config's 8,192 joint vocabulary entries exactly match the token strings in `tokenizer.vocab`. Entry zero is `<unk>` and the blank index is 8,192. The installed package decodes from the config vocabulary directly; it does not load `tokenizer.model`. The separately pinned, different WordPiece-style `vocab.txt` is not used by this path; its presence is not a diagnosis of tokenizer corruption.

Installed `audio.py`, `conformer.py`, `parakeet.py`, and `rnnt.py` hashes match the prior static audit exactly. The independently observed runtime is `parakeet-mlx 0.5.2`, MLX `0.32.3`, NumPy `2.2.6`, PyTorch `2.8.0`, librosa `0.11.0`, SciPy `1.18.1`, soundfile `0.13.1`. `audio.py` remains SHA-256 `88ea1d5210b3ff42ad31322691a4f6cbda7e6a3b281931b95ce6b954bcf89751`.

All **12/12** actual FLAC hashes match the unchanged audio manifest, SHA-256 `63b130e821d68af89db2b25b864217afb5e70aa921b3d9cc5b31e76693663159`. All files are mono, 16 kHz, PCM16, nonempty and finite. The package's exact FFmpeg mono/16 kHz/PCM16 decoding produced integer arrays **identical** to soundfile decoding for every clip. Thus there was no measured resampling change, malformed waveform, additional crop, or input NaN. Amplitude extrema across the cohort are -0.850189209 and +0.817535400, with clip RMS 0.0284662–0.130627. The two pathological inputs had 77,520 and 53,200 samples, exactly their recorded 4.845 and 3.325 seconds.

The requested `load_audio` dtype is ignored by 0.5.2: decoding produces FP32 after PCM16 scaling. The localization artifacts show FP32 waveform, windowed FFT input, logmel, encoder, initial prediction network and joint outputs despite BF16 runtime parameter storage. No inference of BF16 preprocessing/activations is justified from the weight label. Chunking was disabled; the exercised frontend is single-item. Ragged batches, streaming, alternative attention, other dtypes and model revisions are not qualified here.

## Failure reproduction, geometry and intervention

This reviewer parsed the unchanged replay independently. Its 14 calls retain the original two microprobe repeats and all 12 cohort cases. Cases `4572-112381-0006` and `251-118436-0004` again contain **610/420 tokens**, respectively, with every confidence nonfinite; the other ten cases have ordinary finite outputs. The replay calls SHA-256 is `3b3c7e78efab85c3349483c59d9388a33cfb6b8012617af1618d6cd1e0726b20`. This is an actual unchanged failure reproduction, not an inference from the old report.

The installed STFT declares frames using the 400-sample window length while its view spans 512 samples. With 256 reflected samples at each end, the valid count is `floor(N/160)+1`. The legacy count adds one frame for seven of the twelve inputs. For the two pathological clips the counts are 486 versus 485, and 334 versus 333. The final declared frame extends **80 samples beyond logical waveform storage**. This is an invalid bound even though the corresponding padded window entries are zero.

An independently allocated NumPy sentinel experiment did **not** read invalid memory: it explicitly extended the logical waveform by 80 NaNs. Multiplication by the zero-valued window tail left NaNs; one FFT frame became nonfinite, then per-feature normalization contaminated **all** normalized mel elements. This happened for both pathological clips and both normal affected controls. A finite-valued invalid tail need not poison output, explaining why a bounds condition can affect seven clips while only two fail. That explanation is an inference about the original allocator contents, not a measurement of them.

The decoded failure pattern is compatible with zero token and duration decisions repeated to the configured ten-symbol escape limit: the original encoder lengths 61 and 42 produce precisely 610 and 420 tokens. There is no numerical finiteness gate before upstream `argmax`. Entropy confidence computation can serialize NaN after nonfinite logits. This decoder observation identifies the failure's propagation/amplification behavior, not its unobserved first cause.

The instrumented original localization attempt has zero nonfinite elements at every recorded stage for all six clips. Its records SHA-256 is `5728a133eb6d964088fc175c7052fe97476ed48b847059cabfc24272f1701e85`. Recording intermediate arrays changes evaluation and allocation, so that receipt does **not** locate the original NaN creation point.

The independently inspected frame-repair attempt contains **24/24** finite outputs, no pure-unknown result, and exactly byte-identical hypotheses across the two complete passes. Its records SHA-256 is `cb1e431a861524f644dcc40efe905fa845536f66ba49d763199f0741f5d04226`. Both formerly pathological cases now return ordinary speech hypotheses. The adapter changes frame geometry while retaining the remaining feature math, restores its process-local intervention on exit, and refuses nonfinite waveform/FFT/logmel/encoder/joint/alignment states. Source quality/error scores remain a separate assessment; finite transcripts alone do not establish acoustic truth or final adequacy.

## Authoritative feature-level comparison

The [official v3 model card](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) identifies NeMo 2.4 as its runtime. This audit used [official NeMo preprocessing at commit 2381f42](https://github.com/NVIDIA-NeMo/NeMo/blob/2381f42f6979449b5b99538f8f80135831009b51/nemo/collections/asr/parts/preprocessing/features.py), the v2.4.0 tag. Both tag and commit downloads have SHA-256 `cd25ac7919400771891bd6f0a6827c108c5472b9198aaed1b65824b13eeb0c9c`.

The CPU audit extracts and executes the **unchanged official** `FilterbankFeatures`, normalization and frame-splicing definitions with their actual defaults, pinned geometry, and `.eval()`. It does not install NeMo, modify its code, or claim official neural inference. The upstream source, including its license header, is retained only in the ignored artifact directory. No upstream implementation is copied into the tracked diagnostic.

| Operation | Installed 0.5.2 / frame-only identity | Official NeMo v2.4.0 evaluation |
| --- | --- | --- |
| Dither | Ignored | Disabled in evaluation; training-only noise |
| Preemphasis | 0.97, unchanged first sample | Same |
| Hann | Periodic | Symmetric / nonperiodic |
| Shorter window in FFT | Left-aligned; trailing zeros | Centered; 56 zeros at each side |
| Frames | Legacy uses win_length; repair uses n_fft | `floor(N/160)+1` |
| Spectrum power | `(|Re|+|Im|)^2` | `Re^2+Im^2` |
| Mel basis | librosa 128-bin Slaney, FP32 | Same |
| Log additive guard | `1e-5` | Default `2^-24` |
| Normalization | Population standard deviation | Sample standard deviation, plus `1e-5` |

The magnitude difference is substantive: L1-based power can be twice true complex power before the mel transform. The pinned config omits log-guard and preemphasis overrides, so those official defaults matter. The remaining differences affect ordinary clips too; the frame repair does not silently resolve them.

All six requested control classes were measured from the same decoded input waveforms. The NumPy legacy comparison uses **only safe frames**, so the following discrepancies isolate the retained feature conventions from invalid-tail access:

| Case | Control class | Official valid frames | Official features finite | Safe legacy vs official RMS | Maximum absolute discrepancy |
| --- | --- | ---: | --- | ---: | ---: |
| 4572-112381-0006 | Pathological | 485 | Yes | 0.376499 | 2.889376 |
| 251-118436-0004 | Pathological | 333 | Yes | 0.436324 | 2.792956 |
| 3081-166546-0007 | Normal affected | 566 | Yes | 0.383517 | 4.532862 |
| 6599-38591-0009 | Normal affected | 485 | Yes | 0.330296 | 4.951380 |
| 5536-43358-0006 | Normal unaffected | 1042 | Yes | 0.369250 | 3.806958 |
| 8288-274162-0010 | Normal unaffected | 236 | Yes | 0.354294 | 2.201232 |

An independently written NumPy reconstruction of **official** math agrees with the executed official CPU class at RMS errors `6.720e-7` to `3.278e-6`; maximum errors range `1.752e-5` to `1.022e-4`. These are observed values, not a widened or predeclared pass tolerance. Torch versus SciPy FFT/reduction ordering need not be bit-identical. No full-model NVIDIA transcript, output-length or timing comparison was performed: NeMo is not installed in the isolated probe runtime, and no official neural runtime/weight mapping was installed or qualified. This explicitly uses the requested feature-level fallback, not a claim that reference inference is intrinsically impossible.

The six official CPU feature calls sum to 0.009431 seconds in the retained replay (imports/setup excluded). This tiny diagnostic is not a native ASR timing benchmark. NumPy emitted divide/overflow/invalid warnings at some matrix operations, but returned features were finite and the initial/replayed metrics matched. A separate scalar contraction produced finite mel energies on every clip and agreed with matrix multiplication within `4.768e-7`; power maxima were at most 275.828 and mel-energy maxima at most 5.178. The exception-flag warnings remain unexplained and are disclosed; they are not evidence of actual returned nonfinite values or of the original MLX pathology.

Reproducer: `benchmarks/parakeet_reference_audit.py`. It performs only CPU preprocessing and exact input/model hash checks and requires an explicit local reference-source path. Retained receipt: `exports/foundation-repair/parakeet-reference-cpu-attempt01/reference_receipt.json`, SHA-256 `025170387b1121205de2d006ca0914aaf69908edb859289890c70ed427ff2f5d`; cached upstream source is beside it as `official_features_v2.4.0.py`.

## Upstream check and remaining limits

The fetched upstream master `audio.py` is byte-identical to the installed file. No frontend fix was found by that exact current-file comparison. [Commit 00638864](https://github.com/senstella/parakeet-mlx/commit/00638864b7cbaab26ddc072d9b14c2c5edef7d68) fixed recognizing the `hann` name and reflected padding in August 2025; it does not fix this frame formula or establish feature equivalence. [Issue 46](https://github.com/senstella/parakeet-mlx/issues/46) reports hallucination/alignment concerns and requests comparison with the original model, but supplies no diagnosis or validated patch for these clips. It is contextual evidence, not a confirmed explanation.

[PyPI 0.5.2](https://pypi.org/project/parakeet-mlx/0.5.2/) publishes wheel SHA-256 `50afb6ddb62237a6486e214482c25ef12759832fda3cd514e159938fa5970d9c`, uploaded June 5, 2026. The upstream releases page contains no published release notes and its tags API was empty at this check. The reviewed runtime was preserved; no automatic upgrade or model substitution occurred.

The bounds regression tests independently construct NumPy FFTs, exercise all 160 input-length residues and noncontiguous source input, and test invalid geometry/nonfinite refusal. Their whole-model limit remains the measured cohort. This review inspected those tests without executing an accelerator workload, and independently executed all 160 length-residue arithmetic checks plus the new pure duration guards on CPU. The final reviewed adapter SHA-256 is `ff13c8d6a16f6fc553536e025da6f7b63ce10a56f873e3efb02c5f3112000b30`; the regression file is `58cb72adf11bf70837436c8f3e95abc3b12b1d13ae2dd07577a53fbc10fc5330`. The owner reports nine checks passed after the duration narrowing; this reviewer does not present that accelerator-containing test execution as its own.

For the narrowed identity, future development source construction must retain input/source-role/model/runtime hashes, source-only eligibility, complete failures, and identical hypotheses across all compared correctors. The original 1,562.626% WER, repeated-unknown outputs, withdrawal records and caps remain untouched. This review does not admit six 10M B/C recipe probes, establish full training supply, freeze a final protocol, or claim sealed/final candidate inference.

## Bounded extension: 1,120 real training/calibration recordings

This reviewer subsequently audited `benchmarks/development_asr_pairs.py` and the complete `development-asr-pairs-attempt01` selection/provenance/summary/pair artifacts using **CPU-only** parsing, hash checks, official target joins, audio-file inspection and independent selection reconstruction. No new inference or listening was performed. **Extension disposition: PASS for the recorded 1,120 source hypotheses within the already qualified runtime.** The preceding frontend and causal limitations remain unchanged.

The ordered selection is exactly reproducible from the admitted role manifest: restrict to `train-clean-100`, manifest duration 2–12 seconds, then sort stable IDs by SHA-256 of the literal namespace `development-real-pairs-120101:` followed by the ID. The first 1,024 `train` and 96 `calibration` IDs exactly match the saved selection and output order. Neither source hypotheses, source-error rates, output lengths nor recognition quality participate in this selection. The implementation writes selection before model loading. Although its target reader allows development/HPO targets in memory, this generator selects **zero HPO and zero sealed/final rows** for audio acquisition or ASR execution. Every selected parent component has both `has_final=false` and `has_development=false` in the qualification artifact.

All 1,120 IDs are unique. The training subset spans 48 source components and calibration spans five, with no shared component. The independent family check also found no shared speaker, chapter, book, project or metadata component across those two subsets. This verifies this extension's binding to the already reviewed leakage closure; it does not replace the independent full-supply grouping review.

Every inherited role/family/reference field matches its admitted manifest row. The reviewer separately joined all selected IDs to official released training-side JSON entries without opening test-member references: each saved audio path, `target=text_raw`, `official_processed_target=text`, and both target hashes matches the release literally. The declared development target policy remains prospective and does not become a final paper freeze.

All **1,120 extracted FLAC SHA-256 values** match the pair records. Actual file inspection confirms mono 16 kHz PCM16 and duration 2.01–12.0 seconds, totaling **8,849.2248125 seconds**. Actual durations agree with released manifest durations within one sample's rounding. The original 6,387,309,499-byte official train-clean-100 archive was independently SHA-256 verified against the acquisition receipt (`d4ddd1d5a6ab303066f14971d768ee43278a5f2a0aa43dc716b0e64ecbbbf6e2`); the recorded official MD5 comparison is PASS. The original target archive and all seven model assets also pass their pinned hash checks.

The provenance's selection, roles, supply, config, tokenizer, generator, adapter and reader hashes all match their current bytes. The adapter remains exactly `ff13c8d6a16f6fc553536e025da6f7b63ce10a56f873e3efb02c5f3112000b30`, the reviewed 2–12-second implementation. `MLX_ENABLE_TF32=0`, MLX 0.32.3, parakeet-mlx 0.5.2, BF16 runtime weights and FP32 waveform/features are recorded. The installed frontend remains byte-identical to the originally audited package. Runtime execution/concurrency statements come from the retained launch provenance; this CPU reviewer did not independently observe continuous accelerator scheduling.

Every selection has exactly one saved pair record; all 1,120 report `COMPLETED`, and the summary has zero failures. Source strings and their SHA-256 values are preserved and independently checked. There are **zero empty sources, zero pure-unknown sources and zero literal `<unk>` occurrences** anywhere in the saved hypotheses. Source lengths range from 15–236 Unicode characters/UTF-8 bytes and 3–48 whitespace-delimited words. Those are descriptive output lengths, not tokenizer counts or neural tensor dimensions. No row was filtered or replaced on output quality.

**Numerical-record limitation:** this pair generator saves source text and completion status, not each full aligned result or intermediate tensor shape. Its hash-matched adapter checks waveform, FFT, logmel, encoder, every joint decision and returned token alignment finiteness before returning; therefore the completed status is consistent with those checks. This reviewer cannot independently re-read 1,120 historical confidence arrays or reproduce their tensor shapes from the retained pair files, and makes no claim that those arrays were preserved. This is narrower evidence than the full 12-clip repair/localization receipts.

**Metadata-status limitation:** all pair rows retain the parent supply field `audio_qualification=NOT_QUALIFIED`. That is the unmodified, pre-acquisition parent-metadata status, not a new per-clip waveform assessment. The new observed waveform/hash checks above and the source-construction receipts establish this selected extension's operation separately. Keep that distinction explicit; do not relabel the entire admitted text supply acoustically qualified or rewrite the historical parent qualification record.

The complete pair-processing loop spans **156.586116875 seconds** after model load; saved per-row times sum to **154.256178658 seconds**. The additional loop time includes metadata/write overhead. Imports, selection, acquisition/extraction, asset checks and model loading precede this timer and are not included in those figures. Reported peak MLX allocation is 2,308,669,986 bytes; it is not process RSS or continuously observed utilization. This is a bounded selected clean-training subset, not a full source campaign forecast or a representative primary-domain rate.

| Retained extension artifact | Independently verified SHA-256 |
| --- | --- |
| selection.json | `505f1eeb71ffad659504a4db7e4addd49668887b49b491a8458cca19b05ee23f` |
| provenance.json | `6babe46a69bb8068032350d040161fdc936a8f9af008d259ed117373a4966f2f` |
| summary.json | `e9a03878ebeaf8d634eb2f40f7f1535045c3d6f55c665a057da89b9d04fdf566` |
| pairs.jsonl | `ce4a170a086afee430085c4e6f665e8af58b8c68091afc27f10ee403c81951d8` |

The narrow development source qualification remains supported. There is no additional whole-model reference equivalence, arbitrary duration/precision/batch qualification, final/sealed candidate result, protocol freeze or six-probe admission in this extension review.
