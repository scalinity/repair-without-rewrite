# Independent MODEL-0 V6 / real-shard training review

2026-10-05. Independent CPU-only review of the owned reader, training runner, pinned artifacts and checkpoint bytes. No accelerator training/inference, sealed candidate inference, build, production access or publication was performed by this reviewer. The authoritative continuation requests the already qualified MODEL-0; the prospective amendment explicitly keeps the canonical MODEL-1 educational ladder and the separate source-conditioned research convergence gate distinct.

## Independent reconstruction

I rejoined admitted IDs to the pinned official archive independently of `load_targets`, checked both released reference hashes, and compared every returned reader target to that join. IDs are unique and sorted; all selected references use unchanged `text_raw`. The archive digest is `96d4eae2222b29b66437a21959252419bcd4762e5042e71e023790171054d1c0`. No calibration or sealed-final ID participates in this training/evaluation reader.

The tokenizer corpus manifest contains exactly the 45,729 admitted training IDs, their raw-target hashes and source-group IDs, with no HPO/calibration IDs. Its SHA256 is `db1b58fb43da32cded6dc58c7c2ad9dd2d2595e5e6b03b1935b4a4616f8db10a`; the artifact records that same training-manifest digest. The trained tokenizer artifact hashes to `b125551f3c3627edc9cb8d325bc70bfd8340df1518f03d0fd16d140ff7ace6ca`. Full training and HPO round trips passed during this independent re-encoding, with no reserved IDs emitted by literal encoding.

| Recomputed quantity | Train | HPO development |
|---|---:|---:|
| Rows / source groups | 45,729 / 314 | 898 / 12 |
| Distinct raw-target hashes | 45,716 | 898 |
| Raw UTF-8 bytes | 8,423,028 | 85,970 |
| Literal BPE tokens | 1,683,355 | 18,305 |
| Added BOS/EOS positions | 91,458 | 1,796 |
| Full serialized stream | 1,774,813 | 20,101 |
| Discarded final incomplete-block positions | 228 | 55 |
| Complete 257-position storage blocks | 6,905 | 78 |
| Stored packed positions | 1,774,585 | 20,046 |
| Native inputs / shifted labels per pass | 1,767,680 / 1,767,680 | 19,968 / 19,968 |

The independently reconstructed int32 packed hashes exactly match the run identities: train `d9e29bccfe24abc75dd30ba9d5d7dc945982709af1b6fa8b0c437ae9fc12bc46`, development `52b2cbc884c620766f61d80544bd4bd7b94d40cb8b45072dda690628da5f6dfc`. Train and HPO have **zero shared source groups**. Full graph/overlap qualification is separately reproduced in `TRAINING_SUPPLY_INDEPENDENT_REVIEW.md`; this review directly checks the admitted manifest, target join and tokenizer/train/HPO boundaries rather than claiming to reproduce that entire graph a second time.

The runner stores 257 positions but feeds `ids[:, :-1]` to the causal model and supervises `ids[:, 1:]`. Each batch of 16 therefore performs exactly 4,096 native input positions and 4,096 valid labels. There is no padding. BOS/EOS are explicit real-work control positions: one training pass contains 91,076 reserved input positions and 91,055 reserved labels; development contains 1,783 reserved input positions and 1,787 reserved labels. Reported totals must not be described as exclusively lexical tokens.

At the 10M threshold the complete-update endpoint is **2,442 updates / 10,002,432 native inputs**, about **5.6585 presentations** of the fixed native-input corpus. The same fixed seed-42 block permutation repeats without reshuffling. Independent presentation counting finds 4,547 blocks presented six times and 2,358 presented five times. This is repeated real-corpus exposure, not 10M unique tokens. Tail truncation and cross-document packing are declared and unchanged between training and evaluation construction. Independent suffix-length checks show the discarded tail removes five complete training rows plus 16 positions of one preceding row, and two complete HPO rows plus five positions of one preceding row. Thus 45,724 train / 896 HPO rows contribute packed positions; the manifest's 45,729 / 898 are loaded-corpus counts. All 314 / 12 source groups remain represented.

## Receipt lineage and numerical/training code

The tokenizer's launch-bound qualification hash `5a79189acf9f300a82f39545189ec74885244f8e8d528ccb7e1597a5cef75853` is reproduced from the preserved exact bytes at `exports/training-supply-qualification-attempt02/tokenizer_launch_bound_qualification.json`. The later current receipt hashes to `d0b1de70c2d2a7c7bbc7ad711a4d771fa91a22ef399651b0482aaeeee7616842`, as bound by V6. Independent JSON comparison shows added verification/deduplicated-volume metadata, timing and implementation/test hashes; roles, group closure, admitted manifest and actual target corpus did not change. Thus this is documented receipt evolution, not a silently substituted training corpus.

Static review of `src/models/core.py`, `src/models/training.py`, `src/data/development_reader.py` and `benchmarks/model0_real_shard.py` finds unchanged MODEL-0 dimensions and parameter ownership. Analytic count is 4,194,304 embedding parameters + 6 × 737,792 block parameters + 256 final norm parameters = **8,621,312**. Decoder forward uses causal masking; evaluation invokes loss only and never optimizer updates. Gradient sums are divided once by the full batch's valid-label denominator, globally clipped, and passed to bias-corrected AdamW. Decay applies once to matrix leaves, including the single tied embedding owner. FP32 master parameters/moments/accumulation and BF16 working execution retain the previously qualified numerical policy. Every inspected update is finite.

Independent ledger calculations use peak LR 0.0003, 200,000-token warmup, continuous cosine decay to 0.1 of peak at 10M, beta1 0.9, beta2 0.95, epsilon 1e-8, matrix decay 0.1 and global clip norm 1. The phase boundary must not restart this schedule or optimizer. One microbatch is one complete update here; no unreported accumulation occurs. The six pure reader regression tests passed in 0.01 s.

## Preserved provenance defect and replacement trajectory

`model0-v6-phase1-attempt01` reached 5,001,216 inputs with held-out CE 9.764476873935797 → 6.278499505458734. Its checkpoint/ledger are internally consistent, but complete runtime/model/optimizer identities and initial-weight digest were absent from the pre-update record. I flagged this gap independently. Root retained its summary, checkpoint and `provenance_limitation.txt`, charged its exposure, and restarted the same mathematical/data recipe as attempt02. Attempt01 does **not** supply the qualified V6 trajectory or count toward attempt02's 10M criterion.

The replacement runner records pre-update code hashes for the runner, model, trainer, reader, tokenizer encoder and parameter-hash helper. `provenance.json` records MLX 0.32.3, NumPy 2.2.6, GPU/Apple M5 Pro identity and `MLX_ENABLE_TF32=0`; `initial_identity.json` is written before entering the training loop and records the initial weights, full model dimensions, precision inventory, optimizer, schedule, source identities and initial held-out result. Its initial hash `e0275c484f477899fe10f2da41e1ab9adb080ca327780d86b33980d40b09d835` exactly matches the earlier correctness-qualified seed-42 scratch initialization; no trained checkpoint is imported at this initial phase.

## Qualified phase 1 audit

`model0-v6-phase1-attempt02` contains **1,221 contiguous updates / 5,001,216 native inputs and labels**. Every ledger step/token/denominator/LR was independently recomputed, all recorded loss/gradient norms are finite, and saved cursor 19,536 matches 16 blocks per update. Its saved data order exactly matches an independent NumPy seed-42 permutation of 6,905 blocks.

Held-out CE is 9.764476873935797 at initialization and 6.278499505458734 at 5,001,216 tokens, on the same 19,968 HPO labels. The earlier 4,096,000-token CE is 6.403979766063201. These are the runner's native forward measurements; this reviewer independently validates selection, denominators, code, hashes and recorded comparisons, but does not claim a separate model-forward recomputation.

The completed checkpoint's array digest is `8136b71809833133cebbc017519b6ddd585e2f7423a2e9641762c9324702df6b` and metadata digest is `c7326d013236bffe716a8711b0540167432b148bde767e0030e9790f23a53d98`; both verify against `COMPLETE.json`. Direct NumPy inventory finds 56 uniquely named model leaves totaling exactly 8,621,312 FP32 parameters, equal-size FP32 first/second moments and accumulator, finite values throughout, nonnegative second moments, and zero saved accumulation. Independently recomputed parameter digest is `9ab987890761533c3317c381592da05cbaa08de26411057dab32c30d73230268`, matching the summary. Phase-1 allocation peak is 2,093,510,896 bytes, reported RSS peak 730,873,856 bytes, timed training/evaluation segment 76.92976841700147 s, and summed update durations 76.39686087323935 s. This segment excludes pre-loop corpus encoding/initial evaluation; the checkpoint timing field also includes post-save evaluation/hash/report work. These timings are scoped measurements, not complete operation/device-time or thermal telemetry.

## Phase 2 / cold-resume audit

`model0-v6-phase2-attempt02` adds 1,221 updates from the saved phase-1 checkpoint. Its restored weight hash, token count, optimizer step and held-out result exactly equal the independently checked phase-1 endpoint. Combined ledgers contain **2,442 contiguous updates / 10,002,432 native inputs and labels**, with saved final cursor 39,072. I independently recomputed every denominator, token increment and scheduled LR, including the first resumed update (step 1,222, LR 0.00016909718727688822 at 5,005,312 tokens). There is no optimizer/schedule/data-order reset. The final LR is 0.00003.

Final held-out CE **6.022597875350561** is lower than initialization **9.764476873935797**, the actual saved 5,001,216-token checkpoint's **6.278499505458734**, and the earlier 9,216,000-token evaluation's **6.0315627073630305**. Improvement versus the saved checkpoint is 0.25590163010817246. The HPO data/token hashes and 19,968-label denominator remain identical across these comparisons. This demonstrates source-disjoint held-out language-loss improvement within this bounded clean-target LM task; it does not demonstrate useful ASR restoration.

Final checkpoint `COMPLETE.json` hashes independently verify: arrays `5fd51880208e2270a8c2df6b15ae8555a664f8e33aff1532f7c8f331374225b0`, metadata `58702253bcd8a65a07775f971197707ea653616bd39c9edf8a2a8ca404548b19`. Direct NumPy reconstruction yields final model hash `9641c9068135ff7a7b6141e6009fbca5b8ab845a79365285fa49e3b484e265a4`. Parameter count, FP32 ownership, finite model/moment values, nonnegative second moments and zero accumulator remain qualified. Peak MLX allocation stays 2,093,510,896 bytes through both phases; recorded phase-2 RSS is 775,831,552 bytes. The two timed training/evaluation segments total 154.73540320800385 s; summed update durations are 153.59925403821399 s. These exclude pre-loop work and do not certify full-machine pressure, thermal telemetry or isolated device-active time.

One **remaining provenance capture limitation** was independently flagged while phase 2 was early: its pre-loop `initial_identity.json` identifies the temporary freshly initialized model before `load_checkpoint`, while the actual resumed starting-weight/checkpoint path is recorded only in its final `summary.json`. The code hash, already complete immutable parent checkpoint, final restored digest/held-out result, continuation cursor/order and continuous schedule make the observed cold-resume lineage independently auditable afterward. They do not create a pre-update resumed-model receipt retroactively. Full compliance with the owner's before-every-expensive-run capture instruction must therefore distinguish this limitation from the successful mathematical result.

## Final disposition

**PASS for the owner-requested ≥10M MODEL-0 real-shard convergence criterion; resumed-phase pre-update provenance capture remains incomplete.** No model, optimizer, leakage, token-accounting or checkpoint-content defect was found in the completed trajectory. Its observed source-disjoint held-out loss improves versus both initialization and an actual earlier saved checkpoint. This reviewer does not attest complete pre-update provenance for phase 2. A session report must retain that caveat or supply a separately qualified pre-update resume record/run, without relabeling retrospective evidence as pre-run capture.

Even this completed bounded diagnostic does not complete the canonical MODEL-1 educational campaign, establish the separate source-conditioned restoration convergence gate, consume a B/C 10M recipe slot, qualify final inference or freeze the paper protocol. Historical attempt01's additional 5,001,216 native inputs remain charged; cumulative V6 execution through these artifacts is 15,003,648 inputs, of which 10,002,432 belong to the reviewed attempt02 trajectory.
