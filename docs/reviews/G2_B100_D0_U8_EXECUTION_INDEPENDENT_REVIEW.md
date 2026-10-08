# Independent Generation-2 B100-D0-U8 completed execution review

Date: 2026-10-08T03:19:34.642721+00:00

Reviewed base: `568eeaf39a082ba9e82fd7117ff83a62faec2475`. The retained CPU review path is hash-bound in `experiments/manifests/generation_2/scientific-recipe-independent-G2-B100-D0-U8-seed42-lr3e-4.attempt02.json`.

MEASURED RESULT: A separate CPU accounting path reconstructs all 2,440 native update rows against the frozen ordered D0 presentation ledger and U8 geometry. Exact presentation IDs, source/target/anchor identities, channels/phases, cumulative charges, optimizer steps, master/subqueue indices, denominators and LR agree. The complete trajectory has 134,591 presentations, 305 completed master queues and 10,007,223 actual canonical exposure against 10M nominal. One scientific attempt completed; no replay or manual resume was used. The qualified fresh seed42 parameter identity agrees with the recorded launch gate.

MEASURED RESULT: The final output inventory, all 13 checkpoint payload inventories, metadata state identities and all six prescribed observation payload inventories reproduce. Every completed checkpoint has the expected optimizer step/exposure and no pending queue, charge or microbatch accumulation. The final checkpoint identity agrees with the outcome's final state. The heldout panel remains 2,984 cases at every observation; initialization and endpoint each preserve separate 304-case TRAIN greedy/forced diagnostics. Calibration-use receipts reproduce at all six states, totaling 11,400 evaluations without training use or selection.

MEASURED RESULT: Physical attempt wall time is 10286.654194 seconds. Logged training intervals sum to 2361.968268, observation intervals to 7590.863871, and save intervals to 60.027967. These intervals are already inside the attempt wall interval and are not added again. Unique scientific presentations/exposure count the trajectory once. Exact kernel time and monetary cost remain unmeasured/unpriced.

FACT: Failed bounded checker attempt01 is retained. Its first checkpoint assertion incorrectly compared an immutable inventory with a receipt envelope that adds I/O timing. The file inventories and schema agreed. Corrected attempt02 compares immutable identities, verifies the payloads, and records timing separately; qualified scientific code/results remain unchanged.

MEASURED RESULT: The recipe 2 start timestamp follows recipe 1's completed attempt interval. The active process inventory contains the original serial parent and one C101 scientific child. Recipe 2's immutable update-zero checkpoint verifies. Five recipes remain unstarted. All 47 frozen scientific source identities, scientific inputs and frontier decision/amendment hashes remain unchanged; live storage identity/access/free-space checks pass.

FACT: This review verifies execution extent, artifacts and bounded accounting. Scientific metric/gate reconstruction, cross-recipe matching, factorial contrasts, full campaign review and a new complete suite are UNRUN. Recipe 2 remains running, and no intermediate outcome selects a model or treatment. No final/sealed work occurs.

MEASURED RESULT: Recipe 2 has now completed its initialization observation. Independent receipt `experiments/manifests/generation_2/scientific-observation-independent-G2-C101-D0-U8-seed42-lr3e-4.update00000.attempt01.json` reproduces all six payload hashes, 2,984 heldout cases and separate 304-case TRAIN greedy/forced diagnostics. The observation state matches its verified update-zero checkpoint; its 1,900 calibration evaluations are recorded without training or selection use. Scientific training continues in recipe 2.

PASS_INDEPENDENT_COMPLETED_RECIPE_TRAJECTORY_AND_ARTIFACTS
