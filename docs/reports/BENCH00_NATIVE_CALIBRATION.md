# Native resource calibration — bounded foundation

**Scoped geometry measurements completed; full representative BENCH-00 and campaign schedule remain unqualified.** No measured token rate here is substituted for a paper-canonical exposure rate.

## Hardware and runtime identity

FACT: [Environment snapshot](ENVIRONMENT_INITIAL.json) identifies an Apple M5 Pro MacBook Pro, Mac17,8 / MGEC4LL/A, 18 CPU cores (6 super / 12 performance), 20 GPU cores, 48 GB unified memory, macOS 27.2 build 26B5091g. The decoder benchmark used Python 3.12.15, MLX 0.32.3, the explicit reference attention path, `MLX_ENABLE_TF32=0`, BF16 working arithmetic and FP32 master parameters/moments/accumulation. No explicit compile/build command was used. MLX wheel identity is pinned in `uv.lock`; a source commit is not exposed by that wheel. Initial power was AC, power mode 0; initial/final `pmset` reported no thermal/performance warning. Sensor temperature, continuous fan/power and GPU utilization were unavailable or unmeasured.

The [run provenance](../../experiments/native-calibration-attempt01/provenance.json) records commit `9dbef2b`, actual dirty state, current runtime-lock hash, seed 42, config, data and qualified V0–V4 evidence hashes. The environment snapshot's earlier lock hash is historical. Checkpoint/model weights and downloaded assets remain ignored, outside Git.

## Exact MODEL-1 geometry and thermal segment

MEASURED RESULT: The exact 100,685,568-parameter decoder executed five full warmups, 100 timed updates, a 20-minute sustained segment and checkpoint continuation. Vocabulary 16,384, width 768, 14 layers, 12 query / 4 KV heads, SwiGLU 2,048, configured context 1,024. Each update accumulated four batch-one serialized 256-token blocks; shifted causal attention actually operated on 255 positions with 255 valid labels per microstep. Thus 1,024 fixture tokens and 1,020 loss labels were charged per update. All four fixed random blocks were reused; no reader, augmentation, padding or public length distribution was timed.

Forward, loss, backward, FP32 accumulation, clipping, AdamW, both moments, updated parameters and cleared accumulator were materialized and synchronized. No mask was removed. The [independent runner review](../reviews/BENCH_INDEPENDENT_REVIEW.md) verifies those boundaries and preserves the workload limitations.

| Quantity | Measurement |
|---|---:|
| 100 timed updates | 22.817860 s; mean 0.228179 s; median 0.228267 s |
| Timed p95 | 0.233658 s/update |
| Sustained segment | 5,190 updates; 1,200.161542 s wall time |
| Sustained update timer total | 1,199.836527 s |
| Sustained rate | 4.325589 updates/s; 4,429.403 serialized fixture tokens/s; 4,412.101 valid labels/s |
| Sustained median / p95 | 0.229351 / 0.243785 s/update |
| First / last five update-minutes | 4,402.133 / 4,494.202 fixture tokens/s |
| Last / first mean update-time ratio | 0.979514 |
| First completed warmup | 0.504884 s |
| Training-phase maximum MLX allocation | 2,888,425,680 bytes |
| Whole-run peak including dual-trainer resume | 4,499,394,776 bytes |
| Checkpoint write/verify / load/restore | 1.220263 / 1.092636 s |

The first/last windows use cumulative completed-update timers, excluding JSON/I/O gaps; whole boundary-crossing updates are retained. They are not exact wall-clock temperature bins. The first warmup includes lazy operator initialization and is not an explicit compilation-overhead measurement. MLX allocation and process RSS overlap; they must not be added. This runner did not collect RSS, pressure or swap deltas, so whole-machine fit and a no-swap guarantee remain unqualified. No competing neural work ran; CPU tests, coding and network acquisition could overlap.

Evidence: [summary](../../experiments/native-calibration-attempt01/summary.json), [derived statistics and conventions](../../experiments/native-calibration-attempt01/analysis.json), [all 5,295 logged updates](../../experiments/native-calibration-attempt01/updates.jsonl). Another 40 original continuation updates were performed outside that ledger. Total original fixture exposure is 5,463,040 serialized tokens, rather than a real-language or paper-canonical budget.

MEASURED RESULT: The original same-process next-20-update comparison had zero maximum absolute parameter and first-moment difference. A separate [fresh-process audit](../../experiments/native-resume-audit-attempt01/summary.json) then ran 20 control and 20 restored updates in distinct processes. Every loss/LR/state row, final parameter/m/v/accumulator digest, counters, scheduler, cursor and saved RNG state matched exactly. Its additional 40,960 fixture tokens and checkpoint cost are separately recorded. The fixed data path does not exercise a real reader or stochastic augmentation. This closes the scoped process-restart defect without changing the original run's provenance.

## B100 / C101 complete-update samples

MEASURED RESULT: After [final B/C mechanical admission](raw/bc_final_gate.json), six exact-geometry recipes each executed five warmups and 20 timed complete updates: 150 updates total, 120 timed. All losses/norms were finite. BF16 working computation, FP32 master/moments/one accumulator, reference attention, and eight genuinely masked source-padding positions were used. Source bytes, trusted controls, target bytes, decoder events and synthetic byte-anchor counts are separate. No trained 16k BPE anchor price or representative natural distribution exists yet.

| Arm/source length | Edits K / replacement tokens R | C decoder positions | Mean s/update | Maximum MLX allocation bytes |
|---|---:|---:|---:|---:|
| B100 / 64 | full target | — | 0.114881 | 2,551,766,247 |
| B100 / 256 | full target | — | 0.124798 | 2,551,762,087 |
| C101 / 256 | 0 / 0 | 1 | 0.118924 | 2,551,288,311 |
| C101 / 256 | 1 / 1 | 5 | 0.126401 | 2,628,655,673 |
| C101 / 256 | 8 / 8 | 33 | 0.162335 | 3,041,815,867 |
| C101 / 256 | 8 / 64 | 89 | 0.204125 | 3,041,847,995 |

Evidence: [sample summary](../../experiments/manifests/stress_bc_native_samples_attempt01/summary.json), [independent identity/count receipt](raw/bc_native_samples_attempt01.json), [update ledger](../../experiments/manifests/stress_bc_native_samples_attempt01/steps.jsonl). These are short synthetic samples, not sustained B/C rates. Event/head/feedback costs are jointly included; this is no isolated pointer-head ablation.

MEASURED RESULT: Four fresh-random B calls hit a 32-position cap (0.138700–0.157390 s); two C calls abstained at one position (0.012981–0.014230 s). C rendering was not reached. [Complete call/failure ledger](../../experiments/manifests/stress_bc_native_samples_attempt01/decode_calls.jsonl) retains every result. Neither valid representative-length decoding nor a C-versus-B speedup is established.

## Pretrained and speech runtime samples

MEASURED RESULT: Exact official ByT5-small executed CPU/MPS FP32 forward parity, ten full-model AdamW updates and four bounded decode calls. Parity maximum logit error 0.00040436 passed its predeclared tolerances. Updates took 3.501855 s for 500 native supervised labels; first-update cost 1.773401 s, later updates about 0.175–0.184 s. Total path elapsed 15.091969 s, process peak RSS 2,713,403,392 bytes. All four calls capped at 64 new tokens and produced invalid/nonbyte UTF-8 prefixes: zero valid completions and zero primary repair. This small synthetic adaptation is not credible natural-task qualification. [Full result](../../experiments/manifests/public_byt5_probe_attempt01.json).

MEASURED RESULT: Exact official Qwen3-4B-Instruct-2507, revision cdbee75f17c01a7cc42f958dc650907174af0554, executed 4,022,468,096 BF16 parameters on MPS, eager greedy decoding, no CPU fallback. Cold load/transfer took 1.692186 s. Two 84-token input requests each generated 17 tokens and completed with EOS, taking 4.496131 / 1.220317 s. Both retained one source error: repair/introduction zero. Maximum observed MPS driver allocation was 8,389,722,112 bytes; process RSS is a separate view. The prompt remains a development candidate. [Full result](../../experiments/manifests/public_qwen_probe_attempt01.json).

MEASURED RESULT: Parakeet's separately pinned MLX path executed twelve book/project-closed DEV clips (67.705 s) plus two initial repeats. The warmed panel took2.561881 s (RTF0.037839), materialized load2.586989 s, initial calls1.520687/0.116225 s and total process8.579619 s. Observed MLX peak2,248,335,928 bytes; RSS1,008,386,048 is separate. Two API-completed calls emitted610/420 repeated`<unk>` tokens with NaN confidence. Static STFT frame-bound errors affect7/12 clips; NaN causation is unproven. This path's numerical/original-NVIDIA equivalence and representative construction are NOT_QUALIFIED/STOPPED. No favorable-row subset supplies an ASR construction rate. [Full speech evidence](ASR_TTS_NATIVE_PROBE.md).

MEASURED RESULT: Alternate official MPS Kokoro calls took6.094832/0.925336 s, total25.554521 s, but original-waveform transform parity FAILED at unchanged1e-4. A separately declared original TorchSTFT CPU path took0.301054/0.266767 s for two authored utterances totaling6.275s audio, import1.912680 s/load0.895870 s, total3.558657 s, RSS1,536,311,296 bytes. The paths are not pooled. Target fidelity, longer text, voices and screening yield remain unqualified; no listening supplied evidence.

CPU scorer cost:502 synthetic cases in3.703143 s,135.561cases/s with tracing/export, max23,969states/91,520edges, zero caps, one raw interval and27local ambiguities. The actual twelve-source dual-field RAW audit took128.260990 s for24records; each field had2joint-state caps at250,000 states, with proved identity totals retained. Traced peak326,243,099bytes/RSS683,229,184 overlap. [Scorer report](SCORER_FOUNDATION_REPORT.md) distinguishes arithmetic qualification from natural coverage. Cluster bootstrap/statistical runtime has not been measured.

## Requested campaign projections and calendar

| Cost to project | Current evidence and precise missing dependency |
|---|---|
| Three-seed 150M B100 / C101 campaigns | Not estimable in paper-canonical units: tokenizer/mixture/actual length-event distribution and representative 32k-update calibration missing |
| Credible ByT5 comparator adaptation | Not estimable: native path works, useful adaptation and actual budget remain unqualified |
| Natural model inference | Not estimable: no qualified output-length/failure distribution or full source population |
| Compact 2,400-case stress inference | Not estimable: panel not frozen and valid B/C decode behavior not established |
| B/C-only Whisper transfer | Not measured: exact Whisper audio/runtime support, request costs and eligible transfer population missing |
| CPU scorer/bootstrap | Synthetic scorer microbenchmark measured; natural caps/state distributions and paired cluster bootstrap missing |
| TTS / Parakeet construction | Only bounded selected path measurements; accepted generation yield, actual selected real-audio hours and rejection/retry costs missing |

CALCULATION: A 25% reserve means multiplying a qualified measured cost ledger by 1.25. The necessary ledger is not yet available; there is no valid total device-hour value or <=30-day assertion. Multiplying a synthetic byte rate by 150M BPE exposures or extrapolating a capped/abstained call would silently change the unit/workload. The former 1/4/8 TFLOP assumptions are not used to fill those gaps.

The prerequisite-aware queue is: approved public field/access and connected grouping → permitted training supply/tokenizer → V6 and representative native reader/length/32k-update calibration → paired B/C 10M recipes and credible ByT5 adaptation → actual DEV inference/scorer/cluster precision → final H1 scope and cost ledger with reserve → owner review and a separately authorized freeze/final campaign. Source access, missing training supply and useful learning block the queue now; independent static writing/code work can overlap, neural jobs remain serialized. Remaining active researcher time is unmeasured, and agent wall time cannot substitute for human active hours.

INFERENCE: The selected 100M geometries fit their measured native allocations and execute full updates on this M5 Pro. That is useful feasibility evidence. It does not establish useful repair, full BENCH-00, adequate precision, B/C speed superiority, a one-month campaign, H2 affordability or publication readiness.
