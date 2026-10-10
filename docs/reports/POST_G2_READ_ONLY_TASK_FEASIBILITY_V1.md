# Post-G2 Read-Only Task Feasibility Study v1

**CALCULATION — The bounded study completed.** Exposure counts, cached proposal scores, C101 programs and whole-output oracle gains reconcile with the frozen evidence.

**INFERENCE — Acceptance alone cannot materially rescue the prescribed scratch outputs.** ByT5 contains useful corrections, but the available descriptive features do not establish a reliable acceptance policy. D1 substantially increased independent natural examples while providing very little repetition per example.

All new results below are **CALCULATION** from retained artifacts. **MEASURED RESULT** identifies previously recorded experimental results. No new neural experiment occurred.

## A. Verified input identities and coverage

**FACT — Repository identities verified locally and against the live remote:**

| Binding | Verified identity |
|---|---|
| Frozen scientific branch | `codex/g2-execution` |
| Frozen scientific checkpoint | `609f97f31979d469ad8551d06b2c07c3513181ec` |
| Authority branch and unchanged working HEAD | `codex/post-g2-feasibility-record` |
| Authority checkpoint | `f7dda7bbeddfcb21d9ac7c7441bf8158afbcd06a` |
| Qualified G2 source | `2c27cff28a31ae64220df9b06094a914e94dd0f3` |
| Decision v2 SHA-256 | `874957b90a0dd33cffbde3b9a60980be88d06b3733b74b0b4de3e28180f3f88b` |

The authority checkpoint adds the recorded decision and documentation. Scientific objects were read directly from the frozen checkpoint without switching branches.

**FACT — Required receipt hashes match:**

```text
execution-campaign-freeze.attempt01.json
084be260a7f6797d9e138839fe56660c3ce47cb6d92d813c4c3a518b3344cb14

scientific-results.attempt01.json
510e0efceec1127f38d524f8ca71a224cbaea59cd8206f5dc138889d9be74edd

scientific-results-independent.attempt01.json
8f952fc01a96e2e8468c4ac65234de5922bc3aad1984155f1803aecc8d8b5cf7

scientific-accounting-independent.attempt01.json
3dfdad614f2b16bda60e97a454f9dc08b6eb8a132e710ebaf18dc0d271bb8334
```

These receipts are under `experiments/manifests/generation_2/`.

**FACT — Principal private input hashes match:**

| Input, relative to the supplied private root | SHA-256 |
|---|---|
| `corpus-qualification-v1/D0.attempt01/natural.jsonl` | `d391197b246ce17512d9d2f293544623180eb539602897c6264f83a387d50713` |
| D0 `presentations.jsonl` | `21c3f5838f5c7e85f258e8eef25b2b38884a2023199afc5d1852d68155b04f2f` |
| D0 `diagnostics.json` | `87d8c57cc98a32ce4db654559859d4986e5781bd8a178599f8dbda9c7f5d4ac1` |
| `frozen-d1-v1/D1.attempt01/natural.jsonl` | `b47cfe25af372425acc25abd965b6087b52e52abc4134a33223f1b33a4f0ab33` |
| D1 `presentations.jsonl` | `4927980826095d6e2f5d74f37c17d43e233acf3356ccb99d16a1930b29b3a60f` |
| D1 `diagnostics.json` | `847133c3fa187ac185e988c5f6271675ba1993eba1b61f84b020ea798a97e007` |
| `expanded-development-v1/panel.attempt01/panel.json` | `7a92da674399991fb1e282811f984e4018536e81b5400901038f78f44b5bb097` |

**FACT — Prescribed endpoint output hashes match:**

| Endpoint | Cached output SHA-256 |
|---|---|
| B100-D1-U8, update 2,440 | `83e1f0861d00249edaee7a58b8646d6ed686d01d389cd429413d953da8453a38` |
| C101-D1-U8, update 2,440 | `4209b1adbdf96dc2c3bea49ad6c25a09b1419a179168d7638436874dcc07b133` |
| ByT5, exact ten-pass update 35,283 | `311e0733e2f129e6b01b41a2f4acb748d752aadd219c155be3f7e24b72c15230` |

Their exact paths are bound by the corresponding `scientific-observation-…attempt01.json` receipts.

**CALCULATION — Verified coverage:**

| Check | Coverage |
|---|---:|
| Frozen scientific source hashes | 47/47 |
| Scientific input hashes | 3/3 |
| Qualification receipt hashes | 21/21 |
| Freeze-bound external payload hashes | 12/12 |
| Campaign observation receipts | 40/40 |
| Campaign plus archived heldout panels | 42/42 |
| Retained heldout rows checked for membership and totals | 125,328 |
| TRAIN diagnostic states, kept separate | 12 × 304 rows |
| Prescribed endpoint rows freshly text-scored | 3 × 2,984 = 8,952 |
| ByT5 endpoint ID sequences independently byte-decoded | 2,984 |
| Valid endpoint C programs rendered with legal pointer boundaries | 2,958 |
| Completion inventories checked | 46 |
| Private payloads hash-checked and rechecked | 166; 4,117,473,816 bytes |

Every heldout panel contains **2,696 natural and 288 generated cases**. Natural coverage is **52 groups, 50,926 reference words, 1,413 RAW errors, 878 error-bearing cases and 1,818 lexical-zero cases**.

Construction records contain only **14,113 TRAIN, 1,900 CAL and 796 HPO DEVELOPMENT records**. TRAIN and natural DEVELOPMENT groups are disjoint. D0’s 1,024 pairs are an exact source/target-hash subset of D1.

The external volume UUID hash, root inode, filesystem and root-binding hash match the frozen storage identity.

## B. Exact natural exposure and repetition

**CALCULATION — Independently reconstructed from presentation ledgers:**

| Quantity | D0 | D1 |
|---|---:|---:|
| Natural repair records | 1,024 | 14,113 |
| Records with zero repair presentations | 0 | 0 |
| Repair presentations | 18,693 | 19,538 |
| Repetition distribution | 763 × 18; 261 × 19 | 8,688 × 1; 5,425 × 2 |
| Mean repair presentations per record | 18.254883 | 1.384397 |
| Repair canonical exposure | 1,000,665 | 1,000,628 |
| Lexical-error records | 334 | 5,373 |
| Error-bearing presentations | 6,102 | 7,390 |
| Error-bearing canonical exposure | 366,186 | 421,428 |
| Lexical-zero, surface-only records | 508 | 6,470 |
| Surface-only repair presentations | 9,269 | 9,007 |
| Separate reference-as-source identity presentations | 28,040 | 29,365 |
| Identity repetition | 632 × 27; 392 × 28 | 12,974 × 2; 1,139 × 3 |
| Identity canonical exposure | 1,501,032 | 1,501,003 |
| First natural presentation, ending exposure | 302 | 268 |
| First complete natural repair pass, ending exposure | 547,635 | 7,218,011 |
| TRAIN reference words, one distinct-record pass | 22,745 | 294,431 |
| TRAIN lexical source errors, one distinct-record pass | 521 | 9,269 |

Charge-based natural pass equivalents reproduce **18.256312 for D0** and **1.386247 for D1**.

**INFERENCE — D1 tested increased diversity under approximately fixed natural charge.** Its average repair repetition is about **13.2 times lower**. Its first complete natural pass finishes after P0. These results support limited natural learning opportunity; they do not establish that more exposure would produce useful transfer.

The natural files also contain identity views. Those views were separated from repair records in the reconstruction.

## C. Per-phase and per-group support

**CALCULATION — Natural phase allocation:**

| Condition/phase | Repair presentations | Error-bearing | Surface-only | Repair charge | Identity presentations | Identity charge | Repair/error groups |
|---|---:|---:|---:|---:|---:|---:|---:|
| D0 P0 | 12,456 | 4,070 | 6,174 | 666,666 | 18,681 | 1,000,061 | 48/47 |
| D0 P1 | 4,979 | 1,614 | 2,479 | 266,669 | 7,481 | 399,991 | 48/47 |
| D0 P2 | 1,258 | 418 | 616 | 67,330 | 1,878 | 100,980 | 48/47 |
| D1 P0 | 13,026 | 4,968 | 5,978 | 666,666 | 19,526 | 1,000,060 | 314/308 |
| D1 P1 | 5,221 | 1,937 | 2,445 | 266,651 | 7,853 | 400,043 | 314/285 |
| D1 P2 | 1,291 | 485 | 584 | 67,311 | 1,986 | 100,900 | 283/195 |

**CALCULATION — Complete channel accounting.** Each cell is presentations/canonical charge. `identity_minimal` includes natural identity and generated minimal presentations.

| Condition/phase | identity_minimal | rules | natural | empirical |
|---|---|---|---|---|
| D0 P0 | 30,601/2,000,055 | 15,895/1,333,367 | 12,456/666,666 | 31,790/2,666,638 |
| D0 P1 | 12,250/799,970 | 6,357/533,299 | 4,979/266,669 | 12,717/1,066,695 |
| D0 P2 | 2,759/202,066 | 1,176/134,839 | 1,258/67,330 | 2,353/269,629 |
| D1 P0 | 31,446/2,000,054 | 15,895/1,333,367 | 13,026/666,666 | 31,790/2,666,638 |
| D1 P1 | 12,622/800,022 | 6,357/533,299 | 5,221/266,651 | 12,717/1,066,695 |
| D1 P2 | 2,866/201,812 | 1,175/134,649 | 1,291/67,311 | 2,349/269,059 |

**CALCULATION — Natural repair supervision denominators:**

| Presented supervision | D0 | D1 |
|---|---:|---:|
| Gold action labels | 54,976 | 60,289 |
| Gold start-pointer labels | 36,283 | 40,751 |
| Gold end-pointer labels | 36,283 | 40,751 |
| Gold vocabulary labels | 92,798 | 104,694 |
| Replacement tokens, excluding END-EDIT | 56,515 | 63,943 |
| Additional natural-identity action labels | 28,040 | 29,365 |

These native denominators are distinct from canonical exposure, lexical error counts and optimizer steps.

Complete per-group accounting and exact diagnostic-case exposure appear in the appendices.

## D. Proposal benefit and damage

**CALCULATION — Natural endpoints, all 2,696 cases:**

| Quantity | B100-D1-U8 | C101-D1-U8 | ByT5 ten-pass |
|---|---:|---:|---:|
| Better than RAW | 2 | 3 | 67 |
| Equal to RAW | 297 | 2,197 | 2,360 |
| Worse than RAW | 2,397 | 496 | 269 |
| Output errors | 16,997 | 4,095 | 1,650 |
| WER | 33.375879% | 8.041079% | 3.239995% |
| Raw repair bounds | 44–45 | 20 | 120 |
| Completion-qualified repair bounds | 44–45 | 18 | 120 |
| Introduced-error bounds | 15,628–15,629 | 2,702 | 357 |
| Invalid/incomplete outputs | 0 | 26 | 0 |
| Lexical-zero cases damaged, of 1,818 | 1,600 | 288 | 183 |
| Errors in originally lexical-zero cases | 10,151 | 1,614 | 239 |
| Cases with both raw repair and introduced damage | 37 | 16 | 11 |
| Groups with completion-qualified repair, lower bound | 22 | 11 | 37 |
| Groups with introduced errors, lower bound | 52 | 51 | 50 |

Fresh canonical text scoring reproduces the saved repair and introduction bounds on all prescribed endpoint rows. B has one alignment-interval case; C and ByT5 are exact points.

**CALCULATION — Generated endpoints remain separate:**

| Quantity, denominator 288 | B100 | C101 | ByT5 |
|---|---:|---:|---:|
| Lexically better/equal/worse than RAW | 5/0/283 | 117/156/15 | 3/32/253 |
| Decoder complete | 225 | 288 | 225 |
| Decoder invalid/capped | 63 | 0 | 63 |
| Structurally invalid | 288 | 42 | 288 |
| Structure-qualified genuine repair cases | 0 | 23 | 0 |
| Structure-qualified repaired fields | 0 | 27 | 0 |
| Whole-case conformance | 0 | 108 | 0 |

The structural quantities above are retained qualified results from the hash-bound scientific summary. Fresh lexical improvements do not replace structural qualification.

**CALCULATION — ByT5’s natural benefit/damage distribution:**

| Output relationship | Cases | Completed repairs | Introductions |
|---|---:|---:|---:|
| Better | 67 | 115 | 6 |
| Equal | 2,360 | 5 | 5 |
| Worse | 269 | 0 | 346 |

Its useful proposals are real, while damage remains widespread across groups.

## E. Independent oracle reconciliation

For complete cached outputs only, both calculations agree:

\[
G=\sum_i\max(0,e_{S,i}-e_{O,i})
=\sum_i e_{S,i}-\sum_i\min(e_{S,i},e_{O,i}).
\]

An incomplete output contributes RAW to the second formulation and zero gain to the first.

**CALCULATION:**

| Prescribed endpoint | Beneficial complete cases | Supporting groups | Maximum removable errors | Oracle errors | Oracle WER |
|---|---:|---:|---:|---:|---:|
| B100-D1-U8 | 2 | 2 | **2** | 1,411 | 2.770687% |
| C101-D1-U8 | 3 | 3 | **3** | 1,410 | 2.768723% |
| ByT5 ten-pass | 67 | 36 | **109** | 1,304 | 2.560578% |

ByT5’s ceiling is **0.214036 WER percentage points**, approximately **7.714% of RAW errors**.

Raw conservation independently reconciles at both alignment endpoints:

```text
B100: 1,413 − [44,45] + [15,628,15,629] = 16,997
C101: 1,413 − 20 + 2,702 = 4,095
ByT5: 1,413 − 120 + 357 = 1,650
```

**INFERENCE — A whole-output acceptance mechanism has negligible scratch headroom.** The ByT5 ceiling motivates further investigation, but supplies no deployable performance claim or general recoverability bound.

## F. C101 program failure decomposition

**CALCULATION — Prescribed natural endpoint:**

| Quantity | Lexical-error cases | Lexical-zero cases |
|---|---:|---:|
| Cases | 878 | 1,818 |
| Gold requires a byte edit | 878 | 1,240 |
| Immediate no-edit | 661 | 1,518 |
| Nonempty valid program | 207 | 284 |
| Invalid/incomplete | 10 | 16 |
| Complete canonical gold-span sequence | 1 | 547 |
| Exact spans, wrong replacement text | 1 | 7 |
| Nonempty program with differing span sequence | 206 | 275 |
| Canonical gold-program agreement | 0 | 540 |
| Rendered target byte-exact | 0 | 540 |
| Rendered target lexical-exact | 0 | 1,530 |
| Lexical damage | — | 288 |

Among valid programs:

| Event diagnostic | Error-bearing cases | Lexical-zero cases |
|---|---:|---:|
| Missing canonical gold-span events | 2,147 | 1,937 |
| Wrong or extra span events | 586 | 789 |
| Matched spans with wrong replacement text | 268 | 316 |
| Cases with any missing canonical span | 856 | 1,135 |
| Cases with any wrong/extra span | 194 | 266 |

These event diagnostics can overlap. Canonical span mismatch is not automatically output error: alternate programs could render the correct target. Here, no valid natural endpoint program achieved byte-exact correctness through an alternate canonical program.

Of the valid lexical-zero cases requiring surface edits, **235 acquire lexical damage**. Failed outputs remain separately included in the full 288 damaged-case count.

**CALCULATION — Frozen TRAIN error samples:**

| Quantity, 64 cases each | D0-U8 | D1-U8 |
|---|---:|---:|
| Immediate no-edit | 0 | 52 |
| Nonempty programs | 64 | 12 |
| Complete gold-span sequence | 63 | 1 |
| Canonical gold-program agreement | 24 | 0 |
| Exact spans, wrong replacements | 39 | 1 |
| Rendered lexical-exact | 25 | 0 |

**MEASURED RESULT — Retained teacher-forced diagnostics** also show a D0 replacement bottleneck and broad D1 fitting failure. Those losses are not inference-time confidence, and their component denominators are not interchangeable.

**CALCULATION — Single-event omission counterfactual:** Each event was omitted individually from its fixed valid natural endpoint program.

| Result of omission | Events |
|---|---:|
| Omission reduces errors: event harmful in that program | 1,452 |
| Omission increases errors: event helpful in that program | 8 |
| Omission leaves error count unchanged | 569 |

There are **491 active valid programs**: 471 contain a harmful event, seven contain a helpful event, and five contain both. Lexical-zero programs contain 839 harmful and 308 neutral events.

These are reference-aware analytical counterfactuals. No arbitrary subsets were searched, and isolated event effects were not summed into an achievable repair total.

**INFERENCE — C101 has multiple bottlenecks:** missed activation, localization, replacement and harmful action. A generic incentive to edit does not address all of them.

## G. Inference-time acceptance-feature analysis

Only source/output quantities and TRAIN-only support were used as features. References supplied descriptive outcome labels.

### Frozen lexical edit-count bins

**CALCULATION — Natural cases.** `I/D/S` are aggregate insertion/deletion/substitution counts under a fixed illustrative minimum-distance traceback: match, substitution, deletion, insertion priority. Their composition can depend on alignment ties; total lexical edit distance does not.

| Model | Bin | Cases | Better/equal/worse | Invalid | I/D/S |
|---|---|---:|---|---:|---|
| B100 | 0 | 288 | 0/288/0 | 0 | 0/0/0 |
| B100 | 1 | 147 | 1/7/139 | 0 | 0/8/139 |
| B100 | 2 | 286 | 0/2/284 | 0 | 71/120/381 |
| B100 | 3–4 | 518 | 1/0/517 | 0 | 274/408/1,118 |
| B100 | ≥5 | 1,457 | 0/0/1,457 | 0 | 1,562/4,048/7,906 |
| C101 | 0 | 2,193 | 0/2,193/0 | 0 | 0/0/0 |
| C101 | 1 | 41 | 2/3/36 | 0 | 0/13/28 |
| C101 | 2 | 56 | 0/1/55 | 0 | 4/29/79 |
| C101 | 3–4 | 152 | 0/0/152 | 0 | 20/164/346 |
| C101 | ≥5 | 254 | 1/0/253 | 26 | 53/1,142/936 |
| ByT5 | 0 | 2,323 | 0/2,323/0 | 0 | 0/0/0 |
| ByT5 | 1 | 249 | 21/32/196 | 0 | 28/7/214 |
| ByT5 | 2 | 106 | 36/5/65 | 0 | 62/26/124 |
| ByT5 | 3–4 | 17 | 10/0/7 | 0 | 17/4/33 |
| ByT5 | ≥5 | 1 | 0/0/1 | 0 | 0/5/0 |

**CALCULATION — Generated cases:**

| Model | Bin | Cases | Better/equal/worse | Invalid/capped | I/D/S |
|---|---|---:|---|---:|---|
| B100 | 0 | 0 | 0/0/0 | 0 | 0/0/0 |
| B100 | 1 | 0 | 0/0/0 | 0 | 0/0/0 |
| B100 | 2 | 0 | 0/0/0 | 0 | 0/0/0 |
| B100 | 3–4 | 10 | 0/0/10 | 0 | 0/0/33 |
| B100 | ≥5 | 278 | 5/0/273 | 63 | 3,516/871/2,689 |
| C101 | 0 | 132 | 0/132/0 | 0 | 0/0/0 |
| C101 | 1 | 34 | 27/7/0 | 0 | 0/0/34 |
| C101 | 2 | 62 | 53/8/1 | 0 | 2/21/101 |
| C101 | 3–4 | 33 | 25/2/6 | 0 | 1/29/94 |
| C101 | ≥5 | 27 | 12/7/8 | 0 | 3/108/52 |
| ByT5 | 0 | 15 | 0/15/0 | 0 | 0/0/0 |
| ByT5 | 1 | 0 | 0/0/0 | 0 | 0/0/0 |
| ByT5 | 2 | 21 | 3/14/4 | 0 | 0/3/39 |
| ByT5 | 3–4 | 32 | 0/3/29 | 0 | 15/17/81 |
| ByT5 | ≥5 | 220 | 0/0/220 | 63 | 3,304/635/1,108 |

Zero populated bins remain zero observations, not passed strata.

### Length and continuous relative burden

Burden is \(d(S,O)/\max(1,|S|)\). The following are **CALCULATION**, with medians followed by full ranges.

| Model/outcome | Source words | Output words | Relative burden |
|---|---|---|---|
| B better, n=2 | 15 [14–16] | 15.5 [14–17] | .1295 [.0714–.1875] |
| B equal, n=297 | 9 [2–29] | 9 [2–29] | 0 [0–.5] |
| B worse, n=2,397 | 20 [2–50] | 18 [1–45] | .3125 [.0323–2.5] |
| C better, n=3 | 18 [16–25] | 17 [15–27] | .0625 [.0556–.24] |
| C equal, n=2,197 | 17 [2–50] | 17 [2–50] | 0 [0–.25] |
| C worse, n=496 | 20 [3–48] | 18 [0–46] | .2466 [.0323–1] |
| ByT5 better, n=67 | 21 [2–43] | 22 [3–44] | .08 [.0263–1] |
| ByT5 equal, n=2,360 | 18 [2–50] | 18 [2–50] | 0 [0–.25] |
| ByT5 worse, n=269 | 19 [3–44] | 19 [3–44] | .0714 [.0227–.6667] |

ByT5 burden quartiles are **.0590/.0800/.1277** for beneficial proposals and **.0417/.0714/.1111** for harmful proposals. Median source/output byte lengths are **116/117** versus **105/107**, with overlapping ranges.

Generated median source/output words and burden are:

| Model/outcome | Source/output words | Burden |
|---|---|---:|
| B better | 11/11 | .4545 |
| B worse | 16/12 | 1 |
| C better | 16/15 | .1379 |
| C equal | 15/15 | 0 |
| C worse | 16/14 | .25 |
| ByT5 better | 14/13 | .1429 |
| ByT5 equal | 10.5/10.5 | .125 |
| ByT5 worse | 16/18 | .5 |

### Completion and C event count

Natural B and ByT5 outputs all complete, so completion provides no within-endpoint natural discrimination.

**CALCULATION — C event-count relationships:**

| Valid event-count bin | Cases | Better/equal/worse |
|---|---:|---|
| 0 | 2,179 | 0/2,179/0 |
| 1 | 18 | 0/9/9 |
| 2 | 65 | 1/7/57 |
| 3–4 | 237 | 0/2/235 |
| ≥5 | 171 | 2/0/169 |
| Invalid/incomplete, separate | 26 | 0/0/26 |

### TRAIN support as an available signal

A proposal is “entirely supported” only when every lexical edit unit is alignment-consensus identified and meets the fixed TRAIN support rule. No-edit cases receive a separate label.

**CALCULATION — Core-only support, without neighboring words:**

| Model | Entirely supported: better/equal/worse | Partly supported: better/equal/worse | No supported unit: better/equal/worse | No lexical edit |
|---|---|---|---|---:|
| B100 | 1/0/3 | 0/0/50 | 1/9/2,344 | 288 |
| C101 | 1/0/4 | 0/0/132 | 2/4/360 | 2,193 |
| ByT5 | 9/0/61 | 1/0/10 | 57/37/198 | 2,323 |

C’s partly supported category retains all 26 invalid outputs. With one-word or three-word flanks, **none of the three endpoints’ proposed lexical correction units meets the support rule**.

**INFERENCE — Descriptive relationships exist, but usable acceptance separation is unestablished.** In particular, 61 of ByT5’s 70 entirely core-supported changed outputs are harmful. Greater edit burden is not monotonically associated with greater benefit in ByT5.

**UNAVAILABLE — Token/action probabilities, probabilistic confidence and calibration.** No threshold, detector, calibrator or policy was fitted or selected.

## H. Source-only recoverability and support

**CALCULATION — Exact collisions:**

| Population | Records | Duplicate raw-source keys | Byte-target conflicts | Lexical-target conflicts |
|---|---:|---:|---:|---:|
| D1 TRAIN | 14,113 | 0 | 0 | 0 |
| Natural DEVELOPMENT | 2,696 | 1, containing 2 rows | 0 | 0 |
| Combined | 16,809 | 1, containing 2 rows | 0 | 0 |

Lexically normalized source keys also reveal **zero conflicting lexical-target keys**.

**INFERENCE — There is no exact-source collision witness of reference ambiguity in these retained populations.** Most sources are unique, so absence of collisions does not establish source-only recoverability or acoustic truth.

### Local mappings

Mappings were extracted only from lexical edit edges present on **every minimum source/reference alignment**. Distinct records and groups determine support; presentation repetition does not increase support.

Context is explicit:

- Core-only: edited lexical token or insertion gap.
- One-word flanks: one immediately adjacent source word on each side; ordinarily a three-word window for a single-token substitution.
- Three-word flanks: three adjacent source words on each side.

**CALCULATION — D1 TRAIN:**

| Mapping context | Distinct correction mappings | Supported mappings | Supported occurrences | Supported mappings with alternative TRAIN outcomes |
|---|---:|---:|---:|---:|
| Core-only | 3,970 | 65 | 1,650 | 65 |
| One-word flanks | 6,386 | 1 | 10 | 1 |
| Three-word flanks | 6,450 | 0 | 0 | 0 |

The core-supported mappings span **5–688 records and 3–199 groups**. The one supported mapping with one-word flanks spans **10 records in 10 groups**.

“Alternative outcomes” includes preservation of the same source token in other TRAIN contexts. It identifies limits of the local key; it does not establish contradictory references for identical complete inputs.

**CALCULATION — TRAIN alignment coverage:**

| Quantity | Count |
|---|---:|
| Lexical error units | 9,269 |
| Consensus correction units | 6,462 |
| Consensus substitutions/insertions/deletions | 5,233/907/322 |
| Error units not assigned a unanimous local edge | 2,807 |
| Records with multiple optimal alignments | 1,191 |

**CALCULATION — DEVELOPMENT gold correction support:**

| Context | Supported units, of 1,413 source errors | Cases with a supported unit |
|---|---:|---:|
| Core-only | 255 | 219 |
| One-word flanks | 2 | 2 |
| Three-word flanks | 0 | 0 |

There are **983 alignment-consensus DEVELOPMENT error units**; remaining units retain alignment uncertainty.

**CALCULATION — Normalization versus surface restoration:** 508/690 D0 and 6,470/8,740 D1 lexical-zero repair records have different source/target bytes. DEVELOPMENT has 1,240/1,818 such records.

Deterministic lexical normalization makes these pairs scoring-equivalent. It does not certify recovery of the designated raw surface. Unsupported mappings, alternative local outcomes and unidentified semantic/acoustic recoverability remain unresolved.

## I. Group-aware uncertainty and limitations

**CALCULATION — The exact registered shared draws reproduce:**

```text
10,000 draws; PCG64; seed 42; 52 source groups
int64 draw-index SHA-256:
ca7289b19fcdde43e36592843d88bc89d9aa3f2361120a120cd3df4c9ec336d0
```

All cases within each sampled group remain together.

| Endpoint | 95% WER interval, % | 95% net damage versus RAW, pp | 95% oracle gain, pp |
|---|---|---|---|
| B100 | [32.279222, 34.370571] | [29.584542, 31.562922] | [0, .010418] |
| C101 | [6.906683, 9.170769] | [4.319582, 6.184775] | [0, .013181] |
| ByT5 | [2.782617, 3.756010] | [.336630, .599331] | [.154027, .288196] |

These are descriptive group-sampling intervals.

Three uncertainties remain distinct:

1. **Scoring alignment:** B’s repair/introduction bounds; exact distances and oracle gain remain reconciled.
2. **Group sampling:** the intervals above.
3. **Training seed:** unmeasured by this analysis; only the prescribed seed-42 treatments exist here.

CAL and HPO remain consumed DEVELOPMENT evidence. No partition becomes untouched validation. Local mapping coverage is an operational support measure, not a semantic inferability estimate.

## J. Ranked root-cause interpretation

**INFERENCE:**

| Rank | Interpretation | Supporting evidence | Causal limit |
|---|---|---|---|
| 1 | Scratch proposal quality and source-faithful generalization are inadequate | Oracle gains 2/3; B damages 1,600 lexical-zero cases; C has no lexical-exact error-bearing endpoint output | Does not isolate conditioning, copying bias or memorization |
| 2 | D1 natural repair learning opportunity is sparse | One or two presentations; first full pass at 7,218,011; selected D1 TRAIN error samples remain unfitted | More exposure could strengthen memorization or overcorrection |
| 3 | C has distinct activation, localization and replacement failures | 661 heldout misses; active span failures; D0 TRAIN has 39 exact-span/wrong-replacement cases | Canonical-program mismatch alone is not output failure |
| 4 | ByT5’s useful correction is overwhelmed by harmful action | 120 repairs, 357 introductions; 109-error oracle headroom; 269 harmful cases | Available feature summaries establish no effective policy |
| 5 | Surface supervision complicates lexical preservation | Most TRAIN lexical-zero pairs still require byte edits; substantial lexical damage occurs there | No surface-objective ablation identifies a causal effect |
| 6 | Local support is sparse and context-sensitive | 65 supported core mappings, one with immediate flanks, none with wider flanks | Does not prove natural correction impossible or predominantly acoustically ambiguous |

**MEASURED RESULT — B100-D0-U8 fits all 64 selected TRAIN error cases lexically while reaching 124.384401% heldout WER.**

**INFERENCE — This supports narrow fitting without successful transfer.** D0 and D1 diagnostic samples differ, so their fitting contrast is not a matched-example causal estimate.

## K. One recommended next scientific direction

**PROPOSED NEXT ACTION — Request a prospective preservation-aware acceptance-feasibility design using the already prescribed fixed ByT5 proposals.**

The next frontier decision should specify the source-only information contract, independent fitting/evaluation populations, and a required benefit-versus-RAW criterion before authorizing any fitting or execution. Existing consumed DEVELOPMENT data cannot supply fresh validation.

This recommendation selects no threshold, fitted model, checkpoint, neural treatment or Generation-3 recipe. Further scratch execution should remain suspended pending that decision.

## L. Unresolved scientific uncertainties

- Whether B’s failure primarily reflects weak conditioning, narrow memorization or copying/generalization difficulty.
- Whether substantially more natural exposure would produce useful transfer.
- Whether useful C edits can be identified without references.
- Whether a prospective acceptance policy can retain meaningful ByT5 benefit with sufficiently little damage.
- The prevalence of reference ambiguity among unique complete sources.
- The causal effect of surface-target supervision.
- Appropriate architecture, optimizer geometry and training horizon.
- Robustness across seeds, recognizers, domains and longer inputs.

## M. Work not performed or unavailable

**FACT — Not performed:**

- Neural training, inference or model forward passes.
- Detector/calibrator fitting, threshold tuning or model selection.
- Teacher, TTS, ASR, paid API calls or downloads.
- Dataset changes, human annotation or listening.
- Protected final/sealed reference access.
- Test-suite execution, builds or benchmarks.
- Checkpoint-array loading or a full archive/checkpoint integrity rerun.
- Persistent analysis files, commits, pushes or orchestration updates.
- Generation 3 or final-paper campaign execution.

Generated structural diagnostics use retained qualified results; all prescribed endpoint lexical scores were freshly reproduced. The historical 514-test result was read as retained evidence and was not rerun.

**CALCULATION — Resource measurement:** the metered in-memory analysis session lasted approximately **18.6 minutes**, used approximately **84 seconds of process CPU time**, and peaked at **1.92 GiB RSS**. A final short read identified B’s sole interval case. The resource limits were not approached.

## Appendix 1. Complete natural TRAIN group accounting

**CALCULATION.** Group labels are the first eight hexadecimal characters of the original group IDs. Uniqueness was verified across all 366 TRAIN/DEVELOPMENT groups; no grouping changed.

Each vector is:

```text
records,error_records,surface_only_records,
repair_presentations,error_presentations,surface_presentations,
repair_charge,identity_presentations,identity_charge
```

Columns are **group, D1 vector, D0 vector**. `-` means no D0 records or presentations.

```text
00a03f8b 48,22,18,68,33,22,3194,99,4703 -
02525810 57,21,20,85,32,30,3895,124,5746 42,16,13,765,292,236,35299,1149,53091
029359f4 72,22,43,96,30,55,4458,147,6917 -
037489a6 30,8,16,40,11,20,2000,63,3031 -
0616f68f 69,8,43,105,11,67,4587,145,6335 -
0747f2b5 51,24,20,73,32,31,4227,103,6011 -
076d5206 94,33,44,124,45,57,6050,195,9281 -
07cae9d5 64,25,33,94,38,49,5134,134,7418 -
09507d24 6,2,4,9,3,6,597,13,823 -
09956054 27,6,18,36,10,22,1806,56,2760 -
0a06ebf2 45,21,19,66,29,29,3548,93,4989 -
0a6faec0 17,5,6,23,7,9,1259,35,1791 -
0ad3e4ff 52,23,21,72,33,27,4058,109,6119 -
0ee8ee20 23,15,6,32,21,7,2104,47,2987 -
0eebd15a 13,6,7,19,8,11,1145,27,1661 -
0f78f7ab 71,27,27,92,40,31,4126,149,6573 -
100766c6 46,21,22,63,29,29,3753,96,5738 -
10dc5135 32,8,21,45,10,32,2625,67,3961 -
11245898 44,9,26,56,11,35,3302,90,5214 -
13a23cdb 71,32,29,104,46,43,5036,149,7273 -
145bdaaa 93,42,45,125,57,61,6915,195,10547 -
14840ebe 16,6,6,22,9,9,1208,33,1869 -
15f8842b 28,8,14,37,12,17,1577,64,2694 21,6,10,382,110,182,15998,575,24031
176c7e43 14,3,7,18,5,8,1176,29,1927 -
17e71876 17,8,7,23,9,10,1493,38,2516 -
1854c596 163,66,70,221,87,98,10845,343,17037 34,19,8,618,347,145,36606,930,54958
18c29b76 15,4,10,18,5,11,622,31,1057 -
18fb48fd 16,4,10,20,4,13,1234,33,1999 -
1a4a1152 77,26,35,106,35,48,6412,160,9594 31,12,12,564,217,221,36858,853,55795
1aa9af33 37,12,19,51,16,26,2303,77,3551 -
1afce7c7 20,7,10,26,10,13,1370,42,2104 -
1b834841 9,2,7,14,2,12,540,19,769 -
1bf3632f 18,7,9,25,9,13,1339,37,2043 -
1d483c39 35,9,23,50,11,35,2574,73,3843 -
1e56217b 131,38,72,172,47,100,8330,271,13103 23,8,14,421,145,257,19553,631,29421
1e7fb53d 24,9,12,33,13,17,1697,49,2535 -
1f74da64 64,29,27,88,42,37,4600,134,6860 -
1f7f91a0 23,9,12,28,12,12,1618,48,2928 -
1fc707a5 74,25,38,103,38,52,4669,154,7096 -
207e0a05 29,8,12,47,14,18,2429,59,3003 -
20a4dcfe 14,4,10,20,6,14,962,30,1484 -
213610d0 115,67,46,151,89,58,8347,242,13436 -
214848b2 14,3,7,19,4,11,855,30,1380 -
21848ee7 38,13,19,53,17,27,2945,81,4489 -
22bc9333 45,6,34,63,8,48,2807,92,4098 -
23c8f0f3 119,39,60,168,55,84,8736,246,12814 -
244e5aa4 27,8,12,36,10,18,2222,57,3455 -
254378be 64,41,21,88,54,31,5536,135,8545 -
26bf2f46 77,43,24,105,60,31,6257,158,9474 -
2705b473 135,51,53,195,70,82,10527,275,14615 30,7,15,543,126,272,21309,823,32297
2754dd31 18,7,10,26,10,15,1842,39,2689 -
27f6b599 69,29,28,99,40,41,4317,145,6333 -
2a2849c5 12,4,5,16,5,7,926,25,1517 9,4,4,164,72,74,10250,247,15421
2a82ffc3 25,6,13,39,10,19,2105,51,2771 11,5,4,201,92,73,12101,303,18271
2b8455fc 36,23,11,44,29,11,2098,74,3638 -
2d2ae1fb 13,4,8,20,5,14,1410,27,1883 -
2d75633d 12,2,9,17,2,13,945,25,1435 -
2df4e6f7 45,20,21,61,25,30,2551,97,3949 -
2e509257 31,14,16,45,20,24,2685,64,3902 -
2f33f022 48,18,24,67,25,34,3157,103,4879 -
2fa15136 62,32,26,86,45,36,4510,131,6917 -
2fe7730d 12,1,9,16,1,13,798,26,1372 9,1,6,164,18,109,8184,245,12193
3134eabd 37,27,5,49,35,6,2531,79,4141 -
314bfeb3 13,4,6,17,5,8,831,27,1353 -
31c5ebcd 57,15,34,75,19,46,3835,118,5908 -
33ef0d0f 58,20,22,77,26,29,4183,118,6372 9,5,3,167,92,56,11117,248,16506
342bc09e 18,3,13,28,5,20,1722,39,2441 -
34455d5b 39,18,18,49,25,20,2807,80,4388 -
34d9b3ec 10,2,7,17,4,12,787,21,1007 6,0,5,109,0,91,5253,167,7985
35509f30 194,63,97,253,81,127,12321,404,19698 -
3595e331 22,9,6,33,15,10,1855,45,2481 -
36264b28 139,61,51,194,87,70,8744,288,12902 -
364d8d1d 27,5,10,35,7,13,1803,55,2787 18,3,8,330,54,148,17380,497,26289
36a22040 10,5,2,13,7,3,791,21,1227 -
36e729f9 16,6,8,20,8,10,1134,34,1952 -
378e618a 23,5,15,29,6,18,1117,49,1837 -
387986b5 26,10,10,36,14,14,2006,54,3020 10,5,4,181,91,72,10707,276,16302
38fdbff9 50,13,30,69,17,41,3431,101,5097 -
39516316 21,2,15,30,3,21,1488,43,2075 -
3963dabb 17,4,12,25,6,18,1615,35,2289 -
399f0ba0 34,5,20,47,7,27,1851,70,2846 23,3,13,419,55,237,17367,631,26141
3a08d3ea 156,69,53,218,99,72,11624,331,17545 -
3bb272c4 10,0,8,14,0,12,702,21,1009 -
3c7d951f 16,5,9,20,7,11,1082,33,1771 -
3e0816c6 39,15,19,49,17,25,2349,82,4008 -
3e430f63 26,16,8,35,21,11,2171,54,3360 -
3f1a6225 21,8,4,30,11,7,1716,43,2321 -
4116c529 59,29,20,83,41,28,4475,124,6596 -
4259d482 54,19,25,75,24,36,3931,113,5849 42,14,21,771,258,383,40141,1156,60098
42adaa56 23,10,8,34,15,12,2026,48,2776 -
432f9018 108,53,48,156,75,72,6976,223,9869 -
4353d18b 68,16,39,92,22,52,4952,141,7583 -
43cf72b2 21,4,16,31,6,23,1489,43,2005 -
43f5087c 8,0,6,10,0,8,698,17,1179 -
459cb90a 47,13,28,59,15,37,2545,97,4113 -
464c7972 101,27,51,135,33,72,7235,205,10995 8,1,5,146,18,91,9224,218,13804
46e5b463 56,22,25,80,31,36,4888,116,6988 13,4,7,239,75,128,15325,354,22632
473a7f16 35,18,15,46,22,21,2392,74,3908 25,11,12,453,200,216,24519,685,37225
47733640 84,39,42,112,53,56,4888,173,7337 -
47cf55df 93,49,29,131,68,43,5511,194,8054 -
47d8c2a5 15,6,6,24,10,8,1512,34,2164 -
48053289 25,8,14,31,10,17,1783,54,3034 -
48ed9bae 31,12,17,44,16,24,2642,66,4038 -
4a4c9cf7 15,6,6,22,8,9,1530,32,2194 -
4ae44e42 47,25,22,61,31,30,3263,96,5132 -
4bcf6098 26,6,17,38,10,25,1900,54,2726 -
4ed0d054 27,12,14,43,19,23,1823,56,2538 -
50b4f331 31,6,20,39,9,25,1873,65,3103 8,1,5,149,19,92,7703,217,11213
527ed948 20,3,12,27,4,17,1309,41,1999 -
52ba4b67 12,7,3,18,10,5,946,25,1295 8,6,1,146,110,18,7230,218,10778
52eba353 42,20,14,63,32,20,3467,85,4583 -
5324c0f0 18,6,12,27,8,19,1723,37,2339 -
5660879e 6,2,4,10,3,7,516,13,683 -
56784d7c 36,18,12,49,22,18,2739,76,4342 21,10,8,383,183,145,21075,577,31755
56ac19d2 50,16,26,73,24,37,3327,103,4811 16,3,13,294,56,238,16518,437,24635
57720e15 39,17,19,53,22,28,2271,81,3529 25,9,13,455,165,236,18057,682,26936
57954afc 34,8,21,41,10,24,1975,70,3304 -
5813e4d2 29,5,20,42,6,29,1756,59,2431 -
590df0df 19,6,11,25,7,15,1129,39,1789 -
594cf657 43,14,22,60,18,32,2638,91,3961 -
596e2d3e 13,1,8,17,1,10,887,27,1425 -
598a5a81 153,38,90,205,50,127,10411,317,15923 39,9,25,718,166,460,32012,1066,47566
598b8e0a 26,5,15,36,7,21,2014,53,2965 -
5ba1ce80 25,11,12,30,13,14,1626,53,2921 -
5d147af8 24,3,18,32,4,23,1562,49,2401 -
5d522c7c 9,2,6,14,3,10,824,19,1089 8,1,6,145,18,109,8271,219,12495
6066955b 24,8,11,32,12,15,1726,49,2759 23,8,11,423,146,203,23921,633,35831
629b9983 123,36,65,167,49,86,6615,258,10098 -
632b594c 18,6,6,24,9,8,1070,37,1539 -
63932a8b 55,14,29,71,19,37,3615,116,5890 -
63f23831 36,7,24,51,10,35,3367,74,4872 23,5,15,421,91,276,27373,633,41185
65238a96 25,4,14,34,7,19,1566,52,2328 -
65c21f25 13,1,6,17,1,8,615,28,1010 -
66700a68 57,22,29,84,31,44,4690,123,6791 -
66835d20 25,2,18,34,2,25,1920,52,2930 -
66c597c3 31,10,14,45,12,22,2149,67,3315 -
66f8dc7c 16,8,5,26,14,7,1770,33,2245 -
66fba789 22,3,18,30,3,25,1380,45,2097 -
685c5472 72,19,34,103,28,49,4359,150,6416 -
699ab5b2 19,8,8,25,10,11,1427,40,2224 -
6a3f8e36 111,42,55,151,60,74,6629,228,9934 -
6afd18b4 18,7,7,26,9,10,1328,37,1991 -
6b86710d 15,14,1,20,18,2,912,31,1415 -
6d3271fe 32,11,10,47,16,14,2663,67,3693 -
6d3ac3b9 73,20,28,106,28,39,5804,148,8126 -
6dfc81a3 17,2,14,24,3,20,1340,36,2020 -
70b9ad47 29,8,11,43,13,15,2003,59,2703 -
70d7fb0d 150,68,56,209,94,78,10731,309,15905 -
71e266e0 28,9,15,42,14,22,2118,59,2943 -
728239ab 3,0,3,4,0,4,184,7,319 -
73c12a0c 50,9,25,69,13,33,3255,102,4866 -
73fb0980 41,26,13,50,31,17,2968,83,4847 -
7473c2e2 28,9,16,42,12,26,2224,58,3150 -
75417131 16,5,9,21,5,14,997,33,1567 14,4,8,255,72,146,12229,382,18376
767aa72d 45,15,19,57,20,23,2477,93,4135 -
7b01334b 27,5,18,36,8,24,1716,57,2657 -
7bf88331 47,27,14,61,35,18,3197,97,5197 -
7c47c1c9 81,17,51,112,24,72,5848,167,8653 -
7d9c8c16 12,6,4,17,8,7,827,27,1281 -
7e702710 47,12,25,68,17,36,3504,96,4880 -
7f1696de 18,4,10,27,6,14,1939,37,2631 -
822e2faa 99,28,43,129,37,54,7447,214,12160 29,5,14,531,92,257,28863,793,43025
8231d0ee 26,6,16,38,8,24,1528,53,2111 18,3,13,328,55,236,12128,495,18325
839d4144 9,2,7,10,2,8,580,20,1152 -
855dd67d 22,7,13,32,10,18,1726,46,2552 -
88a0a5fb 18,5,10,25,6,13,937,39,1475 -
8a7ee74e 39,17,15,58,25,24,3410,81,4795 -
8aa32a80 103,44,47,145,61,65,6215,217,9471 -
8bf0ad93 42,11,24,58,15,31,2624,86,3860 -
8c4c0cee 288,206,74,388,277,101,16212,603,25097 -
8cae3fbb 180,72,73,250,105,95,13496,371,20469 36,12,18,654,220,325,38658,984,58210
8cae78cb 28,7,14,42,9,22,1966,58,2834 -
8cbbf75d 45,11,31,57,14,39,2791,95,4483 31,8,22,569,148,403,26773,848,39894
8e4ced5a 19,10,8,30,14,14,1492,43,2155 -
8f94974e 16,9,6,22,13,8,1200,34,2028 -
9013ee05 45,16,19,59,24,23,3357,93,5087 -
9058b7b4 10,5,4,12,6,5,746,21,1293 -
91a06c42 22,6,15,27,8,18,1667,45,2825 16,4,11,289,72,199,17555,436,26482
92089766 193,78,65,265,108,91,13425,409,20513 -
92c8b62d 26,11,8,39,16,11,1845,53,2527 -
93510f2d 22,6,13,27,7,17,1485,46,2520 15,2,12,273,36,219,14155,410,21280
93591297 45,26,12,67,40,17,3583,91,4799 -
93d25c42 16,6,8,24,9,12,1250,36,1922 -
94b2ce1d 35,12,17,49,19,21,2607,75,4063 -
953f43fe 24,10,6,32,12,9,1920,49,3027 17,5,5,313,94,91,19719,465,29237
95e630e0 14,5,6,16,5,8,880,29,1589 -
95fc8995 53,18,18,79,25,25,3787,110,5230 -
96f2bd23 20,5,14,25,5,19,1385,41,2325 -
96f7854d 24,7,11,30,9,13,1408,49,2167 -
986e4258 20,9,10,30,12,16,1762,41,2449 12,7,5,218,127,91,11808,329,17831
9881756c 33,12,11,47,18,18,2175,68,3088 -
99c6e934 16,3,9,27,5,15,1487,33,1849 -
9a617f07 99,33,48,134,42,66,6526,209,10275 61,22,27,1119,401,497,59609,1665,88783
9d14f4ce 16,6,10,21,7,14,1227,34,1982 13,4,9,236,72,164,14064,354,21048
9d3879eb 20,6,13,28,7,20,1478,41,2245 -
9d77f83e 30,9,14,45,13,21,2395,63,3325 -
9df6b9a6 29,7,16,42,10,22,2156,59,2999 -
a042d947 20,10,10,27,13,14,1301,41,2017 -
a0810a62 83,38,35,122,53,53,6116,170,8432 -
a20849a2 39,8,22,55,11,32,2329,82,3352 -
a2588293 38,20,16,50,27,20,2706,77,4183 -
a272b9c5 20,10,6,29,15,8,1707,41,2481 15,7,4,276,130,73,16804,413,25101
a4b30943 36,11,16,43,13,18,2021,76,3674 -
a53620ef 51,22,26,75,30,41,3745,108,5368 -
a5921260 132,29,80,185,42,109,9983,274,14990 53,14,32,963,256,578,55925,1450,84008
a5b84e39 18,6,10,25,7,16,1475,37,2111 -
a67a27be 17,10,6,23,15,7,1553,37,2483 14,7,6,255,129,108,16501,382,24712
a9e1f240 96,46,40,130,65,53,6402,200,9968 -
aae101bb 53,21,19,78,28,31,4402,108,6054 -
ab04ee08 55,15,30,76,21,42,3456,116,5352 -
abe3f470 64,26,31,91,37,44,5389,135,7855 21,7,10,384,127,184,23224,570,34474
abf286d3 213,85,101,298,118,141,15258,445,22445 -
acaa1284 39,17,18,52,23,23,3122,81,4931 -
ae291f9f 44,20,18,64,25,29,3316,91,4641 -
aec53c61 72,46,22,101,64,32,5315,148,7968 -
afb6b516 83,32,37,109,43,49,5415,172,8324 32,13,13,583,236,237,29905,877,45129
b07307d8 41,16,18,60,26,25,1938,85,2717 -
b16bf2e4 14,4,9,18,5,11,934,29,1561 -
b2142ec2 121,85,34,167,116,49,8745,248,13010 -
b3166f82 3,0,3,6,0,6,398,7,481 -
b39a4ff4 36,17,12,53,25,19,3291,76,4562 -
b3c3611f 43,30,7,64,43,11,3368,87,4555 -
b4d6d45e 50,18,27,75,27,40,5271,105,7397 -
b503b448 97,37,46,139,53,65,7111,199,10041 -
b5fd82cc 76,42,30,107,57,45,5697,160,8792 -
b6481094 89,42,35,122,55,50,5478,183,8229 -
b70d8d8a 21,6,14,27,9,16,1283,43,2019 -
b70de2db 60,29,21,85,39,30,4373,122,6378 -
b7eccda4 24,7,10,33,9,13,1887,49,2889 -
b92be2fa 16,5,10,21,6,13,953,33,1487 -
ba1089fc 21,9,10,31,12,16,2037,43,2841 -
ba3683cc 51,21,23,70,28,34,3818,108,5836 -
ba56a471 101,46,38,136,59,52,6262,209,9699 -
bb96dc71 91,32,41,129,44,60,6357,188,9292 -
bc302c18 37,2,23,52,3,34,2388,76,3434 -
bcefa231 37,19,13,51,26,20,3159,78,4860 -
bdf56357 88,44,32,127,66,43,6659,184,9394 10,6,3,181,109,54,10005,272,14998
beb0b6d4 78,24,35,111,34,48,5063,164,7520 -
c0190764 32,11,12,42,16,14,2164,65,3349 -
c0523633 11,4,5,14,5,7,698,23,1121 -
c1c724a2 37,20,14,47,25,19,2933,75,4587 -
c1de3f99 66,29,33,94,40,48,5524,140,8198 -
c1e38659 42,16,17,61,22,23,2839,87,4033 -
c24d9326 49,22,20,68,29,29,2950,103,4493 -
c30e5888 119,40,63,158,54,81,7872,252,12328 -
c42fabcd 91,25,47,121,28,67,6117,189,9825 -
c4682031 40,16,16,63,25,25,3661,81,4771 31,14,11,565,255,200,31987,850,48176
c5515ab3 119,40,51,161,57,72,7247,247,10813 -
c64f076a 95,45,46,136,67,63,6642,196,9404 -
c6528d69 13,4,5,18,4,7,1126,28,1778 -
c6cc9f8c 61,24,23,87,32,36,4721,127,6933 -
c74be017 82,26,46,112,40,58,5400,169,8193 -
c7680019 24,7,8,38,11,13,1938,49,2481 -
c7e29ff5 13,3,6,20,5,7,1080,28,1548 -
c8da6a04 19,8,8,29,11,13,1269,39,1785 -
cabc224d 26,6,12,39,8,18,2291,53,3315 -
cb71a72e 5,1,3,6,1,4,310,11,539 -
cc46665f 35,9,14,45,10,18,2031,72,3398 -
cc5d598a 24,12,10,36,17,16,2080,51,2965 -
cc7df1db 17,4,11,22,5,14,1266,35,2083 -
ccd5378e 29,14,11,36,18,14,1942,59,3227 -
ccdef35f 9,0,7,14,0,11,840,19,1153 -
cda7b0de 74,28,32,104,41,45,4636,153,7011 -
ce4059b7 36,10,24,47,11,34,2243,74,3436 -
ce5e172a 26,6,11,37,10,14,1441,55,2159 -
cf363568 16,3,7,21,6,7,1185,33,1779 -
cf536822 45,7,25,67,9,39,2961,95,4319 -
d055ab10 7,4,2,9,5,3,581,15,961 -
d092a2ad 21,6,13,36,9,24,1596,44,1956 -
d09cfe74 25,3,17,38,6,25,1806,53,2409 -
d0cfbd57 10,3,7,13,4,9,577,21,897 -
d38d5b5d 65,31,24,89,43,32,4549,135,6965 -
d3b7ea0e 35,7,14,50,11,20,2342,73,3309 24,4,9,438,72,166,18724,652,27780
d3e83350 17,4,8,24,5,11,1416,35,2089 -
d4c7688a 22,5,12,29,6,17,1575,45,2299 -
d50fe070 27,11,16,34,15,19,2058,58,3410 -
d6c5b996 48,15,23,61,20,30,3389,98,5368 -
d76b3252 15,3,9,20,4,12,1184,32,1900 -
d79026d1 40,15,22,51,20,28,3031,82,4772 17,8,9,311,147,164,20941,467,31389
d9aab6f6 25,6,16,36,8,24,1784,53,2771 -
da0e506b 7,1,4,10,2,6,412,15,643 -
dcd47312 66,27,25,86,33,34,4032,136,6308 -
dd8b7e78 12,4,7,18,5,11,1164,25,1621 -
ddb5e572 21,3,15,32,4,23,1858,45,2567 10,2,6,181,36,109,11737,276,17920
dfabd6f6 34,16,12,46,23,15,2780,71,4087 -
e0bcdfda 36,16,14,50,21,21,2438,75,3727 -
e14db981 13,4,7,19,6,10,1081,28,1658 -
e16864c8 12,2,9,17,3,13,839,25,1215 -
e6a239df 78,67,10,107,91,15,5699,159,8487 -
e7dd4823 39,21,18,60,31,29,3226,79,4381 -
e8481964 15,2,6,20,4,7,990,31,1557 -
e9299528 15,4,8,21,4,11,1097,31,1659 -
e9720cd8 55,25,26,76,33,36,4452,116,6748 -
eb089d19 56,18,22,80,25,31,4520,116,6416 -
eb3b26f8 21,9,9,31,15,12,2239,43,3001 -
eb64cb85 42,14,14,56,20,18,2922,86,4512 -
ec588196 10,3,6,12,3,8,644,21,1169 -
ec5b37be 107,20,60,145,28,82,7701,219,11513 -
eec4fed8 63,28,31,88,41,42,4056,131,5893 -
ef7b8331 21,3,13,28,4,18,1270,45,2139 -
f00cd6e9 74,32,39,106,49,54,5372,151,7389 -
f0e47c6c 78,26,26,103,37,35,5359,162,8454 -
f2bdc335 80,34,30,111,48,42,6483,170,10164 -
f3cf909f 56,23,23,71,27,30,3965,115,6417 -
f57bdf89 20,7,10,28,9,14,1400,41,2067 -
f8bfa4d1 14,3,5,22,6,7,1354,29,1855 -
f8c48d0e 54,21,22,76,28,32,3892,114,5768 -
f8e6af12 60,20,29,91,30,46,4559,123,6023 -
f99df4a5 22,9,10,31,12,14,1575,48,2372 -
f9c236ac 30,6,15,44,9,23,2356,63,3349 -
fbc17276 10,2,7,13,2,9,613,22,1062 -
fbc4e803 66,29,31,89,38,43,4199,134,6476 -
fd7b8cb8 83,31,37,120,45,54,6452,174,9182 -
ff621c1a 76,41,24,104,55,33,5404,154,7916 -
```

Vector sums reproduce all Section B totals.

## Appendix 2. Complete natural DEVELOPMENT group distribution

**CALCULATION.** Columns are:

```text
group
cases,RAW_errors,reference_words
oracle_gain_B,C,ByT5
completed_repair_lower_B,C,ByT5
introduced_lower_B,C,ByT5
lexical_zero_damaged_cases_B,C,ByT5
```

```text
04821e51 43,23,781 0,0,4 1,0,4 236,50,4 24,4,2
12adc322 25,18,585 0,0,1 1,0,3 186,27,9 11,2,4
21fcf791 11,6,271 0,0,2 0,0,2 81,10,1 7,0,0
22eb01a4 28,7,698 0,0,0 0,0,0 242,35,0 22,5,0
237c1fb4 20,13,363 0,1,4 0,3,4 153,20,2 14,3,1
26f7153e 65,16,1345 0,0,1 1,0,1 450,13,3 54,4,2
342e5aee 43,29,820 0,0,0 0,1,0 218,45,4 18,3,2
36de4956 28,8,584 0,0,0 0,0,0 179,106,4 21,7,2
4b8d5d2b 28,3,774 0,0,0 0,0,0 225,2,1 24,1,1
4c65e425 52,16,1058 0,0,2 0,1,3 275,60,11 40,6,9
51dc4445 17,7,370 0,0,3 0,0,3 103,13,1 10,1,1
589de516 38,23,656 0,0,0 1,1,0 207,37,5 24,2,5
5a1cc328 68,37,895 0,0,9 0,1,9 229,73,17 31,15,8
5a91d5a5 50,25,1057 0,0,6 3,0,6 367,20,0 33,3,0
6445b27e 32,17,812 0,0,1 2,0,2 231,38,2 21,3,1
661dc98f 69,19,1002 0,0,0 0,0,0 336,40,13 50,7,6
70dcbfd6 15,11,291 1,0,2 2,0,2 70,20,2 7,1,1
8188226b 147,58,2934 0,0,1 4,3,1 903,243,13 95,18,8
8eaf08bf 73,62,1112 0,0,3 0,0,3 301,32,9 28,3,3
91fbac4c 38,29,794 0,0,1 1,0,1 199,55,8 23,5,4
9201f371 51,28,987 0,0,3 2,1,3 290,107,14 30,7,6
9253d6a8 132,79,2279 0,0,1 4,0,1 808,141,12 74,14,5
92f7d566 50,39,1190 0,0,0 0,0,1 406,69,15 24,5,6
974a6fb0 63,34,1085 0,0,4 2,0,4 313,58,7 35,8,6
98c3ef18 28,3,655 0,0,0 0,0,0 189,31,1 23,4,1
9b00aeb8 95,28,1155 0,0,0 0,0,0 337,101,15 61,19,9
9ccf44cd 62,42,1056 0,0,1 0,0,1 313,2,1 34,1,1
9e3e2bc3 30,16,658 0,0,0 0,0,0 234,3,2 17,0,1
9f85cf4e 14,4,270 0,0,0 0,0,0 86,2,1 11,1,0
a0572433 63,46,1432 0,0,4 3,0,5 438,38,7 36,3,4
a4467178 57,80,931 0,0,1 0,0,1 258,60,17 11,4,3
a59a53ec 73,27,1698 0,0,3 1,0,4 582,83,14 51,9,7
a83c754d 43,23,957 0,0,4 0,0,4 273,44,2 26,3,1
adff3eaf 120,72,1835 0,1,1 1,1,1 556,92,12 61,11,6
b922e647 19,8,360 0,0,1 0,0,1 140,12,2 11,2,2
bb2fc9e9 12,6,220 0,0,0 0,0,0 77,14,6 6,4,2
bc739a48 104,23,2058 0,0,2 0,0,2 515,32,4 72,6,4
c32b8e73 33,19,838 0,0,7 0,0,7 290,51,7 20,6,3
c5dcc8ce 75,88,1540 0,1,3 4,3,6 457,138,16 30,10,6
d7800d66 17,21,350 0,0,2 0,0,2 108,9,2 9,1,1
dcaa10c6 88,33,1303 0,0,6 3,1,6 392,107,6 56,14,3
dfb7e7a6 83,29,1087 0,0,4 1,0,5 307,37,22 42,10,10
e2100cfb 107,87,2649 0,0,4 4,2,4 878,236,13 56,17,7
e2803796 15,10,209 0,0,0 0,0,0 56,3,1 7,0,0
e42b0307 28,14,507 0,0,2 0,0,2 144,14,4 15,3,2
e5cae71e 29,11,492 0,0,5 1,0,5 135,0,3 17,0,2
ede2c32c 74,24,1176 0,0,2 1,0,2 307,71,13 51,9,8
f0388b4d 19,4,355 0,0,0 0,0,0 104,5,5 13,1,3
f5413fe3 17,12,385 0,0,0 0,0,0 126,35,1 8,1,0
f55222e6 48,22,903 1,0,7 1,0,7 285,72,9 33,7,6
fd3205c6 130,45,2597 0,0,2 0,0,2 866,63,12 85,7,8
fecba8fb 27,9,507 0,0,0 0,0,0 167,33,2 18,8,0
```

For group `fecba8fb`, B’s upper repair and introduction counts are each one higher than the displayed lower count. This is the sole interval case, `2346-152201-0041`; every other displayed repair/introduction count is exact.

## Appendix 3. Exact diagnostic-record presentation counts

**CALCULATION.** Each row starts with a zero-based index in the frozen condition’s `diagnostics.json`, followed by presentation counts for successive entries.

Indices 0–255 contain natural and corresponding identity views; 256–303 contain generated views. These are exact variant-identity counts. Initialization exposure is zero for all cases; the vectors below describe the completed endpoint.

D0:

```text
0   18,27,19,28,19,27,18,27,19,28,18,27,18,27,18,27,18,27,18,27,19,27,18,27,18,27,18,27,18,28,18,27
32  18,27,18,28,19,27,18,27,19,27,18,27,18,28,18,27,18,28,19,27,18,27,18,27,19,27,18,27,19,27,18,27
64  19,28,19,27,19,27,18,28,18,27,18,27,18,27,18,27,18,28,18,27,18,27,19,27,18,27,18,28,18,27,19,28
96  18,27,18,28,18,28,18,27,18,27,18,28,19,27,18,27,18,28,19,27,18,27,18,27,18,27,18,28,18,28,18,28
128 19,27,18,27,18,28,19,27,19,28,18,28,19,28,18,28,18,27,18,28,18,28,19,28,18,27,19,27,18,27,18,27
160 18,28,18,28,18,28,18,27,18,27,18,27,18,27,18,27,18,28,18,27,18,27,18,27,18,27,18,28,19,27,18,27
192 19,27,18,27,18,27,18,27,18,27,18,27,18,27,18,28,18,27,18,28,18,28,19,27,19,27,18,27,18,28,18,28
224 18,27,19,27,18,27,18,27,19,28,19,28,18,27,19,28,18,27,18,28,19,27,19,27,18,28,18,28,18,28,18,28
256 0,4,0,3,1,4,330,2343,344,2443,266,1882,1,5,1,4,1,4,0,3,1,3,1,2,1,4,1,4,1,3,0,4
288 1,5,1,4,1,6,1,5,0,4,1,4,1,6,1,5
```

D1:

```text
0   1,2,1,2,1,2,1,2,2,2,1,2,2,3,2,2,1,3,2,2,1,2,1,2,1,2,1,2,2,2,1,2
32  1,2,1,3,1,3,1,2,1,2,1,2,1,2,2,2,2,2,1,2,2,2,1,2,2,2,1,2,1,2,1,2
64  1,2,1,2,1,3,1,2,1,3,2,2,1,2,1,2,2,2,1,2,2,2,1,2,1,2,1,2,1,3,1,2
96  2,2,1,2,1,2,1,2,1,2,1,2,1,2,2,2,1,2,2,2,1,3,1,3,1,2,1,2,1,2,1,2
128 1,2,2,2,1,3,2,2,2,2,2,2,1,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,1,3
160 1,2,2,2,1,2,1,2,1,2,1,2,1,2,2,2,2,3,1,2,1,2,1,2,1,2,2,2,2,2,2,2
192 2,2,1,2,1,2,1,2,1,2,1,2,1,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2
224 1,2,2,2,1,2,1,2,1,2,1,2,1,2,1,2,2,2,1,2,1,2,2,2,1,2,2,2,1,2,2,2
256 0,4,1,3,1,3,330,2343,344,2443,266,1882,0,4,1,4,1,4,1,2,1,4,1,4,1,4,1,4,0,3,1,5
288 1,5,1,4,1,6,1,5,1,5,1,5,1,6,1,4
```

Five D0 and three D1 generated diagnostic variants have zero exact presentations. No natural diagnostic repair or identity view has zero endpoint exposure.

## N. Verification of unchanged state

**FACT — Before/after checks agree:**

- Working HEAD, branch, local refs and Git index are unchanged; working tree remains clean.
- Live scientific and authority remote refs remain at the supplied commits.
- All 166 consumed private payload hashes match on final recheck.
- `ORCHESTRATION.html` remains at SHA-256 `bf73ca2ac482f8413981e9af4f438aa05ef2b7c05d46cf95b10020e21881c18d`.
- `docs/LOG.md` remains at SHA-256 `5b14ffad043a83ff12492d069cbd19adcb09d6dd7a512f7ca1daa5c0761e9f5d`.
- The continuation automation remains **PAUSED**, byte-unchanged at SHA-256 `870d277d47c840fce6f77c54f5566d279ddc7274da808d947ee445432f984da9`.
- No persistent task files were written. The in-memory analysis process was closed.

This report authorizes no fitting, training, model selection, Generation 3 or final-paper campaign.

FRONTIER_MODEL_REVIEW_REQUIRED
