# B100 / C101 10M development-probe admission

**Status: NOT STARTED. No 10M recipe slot has been consumed.**

FACT: The authorized prospective roster remains seed 42, three 10M canonical-exposure recipes per arm, peak LR 1e-4 / 3e-4 / 6e-4, C component weights 1.0. It is not frozen and no final seed has run.

MEASURED RESULT: Exact B100/C101 mechanical tests and matched four-pair correctness overfits are documented in [BC_CORRECTNESS_REPORT.md](BC_CORRECTNESS_REPORT.md). The first aggressive-LR rehearsal failed complete-output criteria despite reducing loss; the lower-LR, longer rehearsal passed 4/4 complete exact outputs for both architectures. All failures remain preserved. These are memorization fixtures with no held-out examples, rather than any of the six 10M recipes.

Admission remains closed because the full 16,384-entry training-derived tokenizer, permitted training mixture and source/group leakage qualification are incomplete; MODEL-1 V6 real-shard convergence is not run; full representative BENCH-00 is not qualified; and the actual natural source/reference development contract and useful comparator adaptation remain unresolved. A fixed random-token thermal sample and synthetic B/C timing samples establish scoped geometry cost only.

No claim is made about useful held-out correction, identity collapse at 10M, aggressive rewriting at 10M, LR discrimination, the adequacy of 150M exposure, or interpretability of 50M/100M/150M learning curves. Unknown results remain unknown. The first tiny recipe's copy collapse is retained as a concrete warning that teacher-forced loss alone is insufficient.

PROPOSED NEXT ACTION: Resolve the source/reference and grouping contracts, train and hash the permitted tokenizer, pass V6 and representative native calibration, then preregister and run the paired seed-42 recipes. Evaluate complete held-out outputs with fixed source denominators and all failure/bound records. No final campaign or protocol freeze follows automatically.
