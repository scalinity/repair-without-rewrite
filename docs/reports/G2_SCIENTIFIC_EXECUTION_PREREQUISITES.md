# Generation-2 scientific execution prerequisites

Date: 2026-10-07T23:28:27.477046+00:00
Reviewed source base: `13a96d455c92b022c632ee1a64e566e4c6f96a36`
Branch: `codex/g2-execution`

FACT: The frontier milestone decision was published alone at `b1c565e341c1571fec15d4f918049c584246517b`; the exact amendment and four-state binding were published at the reviewed source base. The original seven qualified recipe manifests and all qualified scientific source, configurations, dependencies and tests remain byte-identical to `2c27cff28a31ae64220df9b06094a914e94dd0f3`.

MEASURED RESULT: The complete suite passes 505 tests, zero failures/skips, after the 465-test baseline and 477-test milestone binding. Launcher attempts 01/02 pass 501/503 tests; attempt03 covers the final implementation and 505 tests. Receipts and external log hashes are in `experiments/manifests/generation_2/execution-launcher-final-tests.attempt*.json`. The 28 added launcher cases cover fixed order, unresolved-outcome stops, completed-state observations, exact retained payload/state checks, single accelerator lock, completed ByT5 resume counts, portable checkpoint dtype/cursor checks, whole CAL consumption, and exact one-replay serialization.

FACT: New execution wrappers call the unchanged qualified native trainer, scientific iterator, checkpoint/restore, decoder and scorer. ByT5 uses pinned official weights, the unchanged continuous batch-four iterator, constant LR and qualified AdamW/FP32 MPS operations. Its completed-update checkpoint retains model, optimizer, CPU/MPS RNG and exact cursor; the next batch retains the qualified zero-grad operation. No pass-boundary flush, split batch or optimizer reset is introduced. Every descriptive observation checks that the trained state is unchanged and is atomically published separately. Completed observation reuse validates state and every payload hash. All CAL use receives a separate observed-use receipt. Failed partials and numerical states remain external and hash-bound; external-root loss fails closed.

MEASURED RESULT: Independent attempt03 directly reconstructs the corpus payload inventories, all original functional/configuration/test identities, 2,984-case panel, zero trajectories/slots, four milestone bindings and dense storage geometry. Attempt01's missing recipe argument is retained as a failed mechanical checker attempt. Attempt02 passed; attempt03 binds the final three launcher source hashes. No model was run by these prerequisite checks. See `benchmarks/g2_execution_independent.py` and its numbered receipts.

MEASURED RESULT: All twelve qualified native cold boundary/pending paths and independent qualification receipts retain their published hashes and dispositions. Installed NumPy 2.2.6, MLX 0.32.3, torch 2.8.0 and transformers 4.55.4 match qualification. The physical external-root identity/access/free-space checks pass. Storage reforecast attempt03 passes with 269.677 GiB conservative high-water free, above the unchanged 250 GiB floor; the independent calculation agrees exactly with the retained dense layout and explicit planning allowances.

PROPOSED NEXT ACTION: From a clean published execution source, freeze all scientific inputs, source hashes, recipes/order, schedule, milestone decisions, scoring/viability, stop/replay rules and artifact policy. Publish that freeze before recipe 1. The serial launcher then executes exactly the prescribed six B/C recipes followed by ByT5, with one scientific accelerator job at a time. Qualification initializers remain forbidden. No final/sealed run, paper protocol freeze, teacher/TTS, cloud or production work is authorized.

FACT: At this review, all seven recipes are AUTHORIZED_UNSTARTED; zero scientific trajectories/slots exist. Scientific execution of the wrappers is UNRUN. Previous qualification results are retained evidence, not a claim that the future scientific campaign completed.

GENERATION_2_EXECUTION_READY_FOR_FREEZE
