# B100/C101 10M development-probe admission decision v4 — 2026-10-05

**QUALIFIED: all six seed-42 10M B100/C101 DEVELOPMENT probes are scientifically admissible. Zero scientific recipe slots have started.** This report binds the approved lexical corruption decision, full reader, native qualification and measured cost. It does not select an LR, freeze `paper_protocol_v2`, or admit a final-paper campaign. Native implementation is frozen at `28298ad886aa321882aa0530a18421e7d4e3553e`; future recipes retain seed 42 and the original six slots.

The approved decision and prospective amendment were recorded at `ab8fe95` before implementation. The starting clean local/published checkpoint was `1b114ff485a2a59051bf7a2e39acec5774fd35a1`; the required baseline reproduced 275 passing tests. Source utterances, complete native captures, checkpoints, evaluation outputs and failed attempts remain in ignored private exports. Public manifests carry hashes and aggregate measurements.

## Admission questions

1. **Prior raw profile preserved?** Yes, byte-for-byte at SHA-256 `5df3800d7a29e370abdce36bd489989482d5d878765612b5a14a4b2cab1fc310`. Independent reconstruction matches. It remains a diagnostic of raw TRAIN reference-to-recognizer surface differences under the repaired Parakeet development runtime; it is not the active corruption relation.

2. **Exact revised estimator/version?** `development_lexical_corruption_v2`, alignment `lexical-projected-codepoint-all-optimal-edge-consensus-v2`. `Phi` joins pinned `lexical_eval_v1` token values with one ASCII separator. Projected reference-to-hypothesis unit codepoint edits count only coordinates/payloads unanimous across all optimal alignments. Support requires five distinct records and three groups. Each of 1,024 TRAIN pairs contributes once; CALIBRATION contributes zero.

3. **690 lexical-zero / 334 lexical-positive reproduced?** Yes, production and independent implementations exactly reproduce both counts across 48 source groups. Raw-zero count remains 182.

4. **Projected-distance distribution?** `{0:690, 1:103, 2:117, 3:42, 4:40, 5:11, 6:7, 7:2, 8:2, 9:2, 10:1, 11:2, 12:2, 13:1, 17:1, 21:1}`. This is uncapped projected codepoint distance, not realized generated token distance or WER.

5. **Omitted ambiguity mass?** 511 of 875 minimum-edit units (58.4%). Of the remaining 364 consensus occurrences, 135 fail support; reconciliation is `875 = 511 + 135 + 229`. There are 169 records with ambiguous edits/multiple optimal paths. Possible-edge counts use a separate denominator: 1,700 possible edges, 1,336 ambiguous edges.

6. **Supported entries?** 20 entries survive; 221 distinct entries fail support. Retained mass is 229 occurrences. Individual retained support spans 5–31 records and 4–21 groups.

7. **Retained S/D/I weights?** Substitution 49, deletion 106, insertion 74, totaling 229. Occurrence weight is retained without post-hoc reweighting.

8. **Actual supporting groups?** Lexical errors occur in 47 groups; 38 groups support retained entries. Every entry's complete hash-valued `source_group_ids`, all 48 group diagnostics and group-omission results are in the [revised table](../../experiments/manifests/lexical_reader_v2/lexical-profile-table.attempt01.json). Groups are clustered support, not additional independent records; no claim of equal group exposure is made.

9. **Leave-one-group-out sensitivity?** Across all 48 omissions, requalified retained mass ranges 193–229, supported entries 17–20 and conditional K=1 probability 0.300000–0.315951. The fixed full-table top ten are measured in every omission. Cached unanimous observations are reused; neither realignment nor tuning occurs.

10. **P1/P2 severity probabilities?** K=1 is 103/334 (30.8383%); K=2 is 231/334 (69.1617%). These are pre-support positive-record probabilities used as canonical-exposure weights. P0 has K=1 weight one; the empirical channel has K=0 weight zero.

11. **Supported class pairs?** SD 11 supporting records / 9 groups; SI 7/6; DD 16/12; DI 8/7; II 5/5. SS has 3/3, fails the record floor and receives weight zero. Pair weights count each record once after individual-entry support and nonoverlap admission. Independent literal payload draws within a supported class pair remain the declared generated-domain assumption.

12. **Retained-entry concentration alarm?** No. Largest entry is separator deletion: 33/229 = 14.4105%; the trigger is strictly greater than 50%.

13. **Separator-only table alarm?** No. Separator insertion/deletion mass is 50/229 = 21.8341%. No punctuation/case filter or raw-table mutation supplies this result.

14. **New profile hash?** `bc14b7ca5e8299ee8004cefb6deb67151ea93f1d44f48ea48d0b4619a9549b87`.

15. **Independent profile reproduction?** Yes. A separate lexical scanner and all-optimal set-intersection implementation reproduce all 1,024 record audits and the complete serialized table byte-for-byte, including support, ambiguity, class pairs, severity and all group omissions. See [independent profile review](../reviews/LEXICAL_CORRUPTION_PROFILE_V2_INDEPENDENT_REVIEW.md).

16. **Required generated pools nonempty?** Yes. All 160 required category/cell/view strata are nonempty, with both positive empirical severities represented as prescribed. Eight categories, 8,404 bases and 42,020 accepted views are frozen. Negation retains one base per cell; all other category/cells retain 300. No allocation is reassigned around a small or empty pool.

17. **Proposal/rejection rates?** 18,321 proposals produce 16,808 accepted empirical views (91.741717%), 642 ambiguous inverses (3.504176%) and 871 lexical-effect rejections (4.754107%). Unavailable and capped counts are zero. Failures have zero training charge; no hidden fallback noise or retry beyond 50 proposals is used. Complete reason counts and rates are in [reader qualification](PAIRED_MIXED_READER_QUALIFICATION_V3.md).

18. **Every empirical variant lexically changes?** Yes, all 16,808 accepted variants change each affected field and satisfy `L(S)!=L(R)` and `L(S)!=L(Y)`. K=1 applies one operation and K=2 applies two operations in distinct fields. Generated token distances are separately disclosed and do not replace requested K or the natural severity estimator.

19. **Realized-edit entry alarm?** No in the complete frozen 10M reader. Weight charges every applied edit by its presentation charge: 4,926,142 total; largest entry, delete `e`, is 994,303 (20.184213%). Actual BENCH also passes each arm and every segment; B largest 1,179,580/ 5,866,253 =20.107895%, C 591,840/2,926,175 =20.225721%.

20. **Realized separator-only alarm?** No in the complete frozen reader: 996,183/4,926,142 = 20.222377%. Accepted-pool counts, natural retained-table weights and whole-reader exposure are distinct denominators. Actual BENCH also passes: B 1,185,579/ 5,866,253 =20.210158%, C 590,311/2,926,175 =20.173469%; all segment alarms are false.

21. **Unique complete source-only inversion?** Yes for all 42,020 accepted generated views, independently reproduced. The qualifier enumerates the entire revised public union, including zero-operation spoken preimages and off-manifest targets. Hidden intended Y selects nothing; Y is compared only after unique qualification. Maximum proposal search is 11 states, maximum accepted search three, under the fixed 500-state bound.

22. **Complete generated-pool hash?** `dc9caac46145eee1e8d9ebea34ff486b3b08afffaee447d0bb22e12bef3fe8dc`.

23. **Realized 30/20/10/40 allocation?** Over 10,007,223 exposures: identity/minimal 3,002,091 (29.999242%); rules 2,001,505 (20.000604%); public real 1,000,665 (9.999427%); empirical 4,002,962 (40.000727%). Identity and minimal are separately 1,501,032 and 1,501,059. Whole examples remain indivisible; largest phase discrepancy is 93.2 exposures, within the admitted-charge bound.

24. **Whole-reader exact source==target?** 36,065 presentations / 2,051,330 exposures (20.498494%). This is measured from actual bytes across every channel, rather than inferred from identity allocation.

25. **Whole-reader lexical source==target?** 45,334 presentations / 2,537,309 exposures (25.354776%). The empirical channel itself has zero lexically neutral accepted views.

26. **Repair-required exposure?** Byte repair: 98,526 presentations / 7,955,893 exposures (79.501506%). Lexical repair: 89,257 / 7,469,914 (74.645224%). Each equality/repair pair partitions the entire reader.

27. **Natural/generated repetition?** Public-real records: 763 used 18 times, 261 used 19 times; separate identity records: 632 used 27 times, 392 used 28 times. All 48 groups appear. Generated bases used: 7,257; typed bundles: 1,801; distinct accepted variants including natural: 27,991. Base reuse ranges 1–6,427 and variant reuse 1–2,693; the four small negation bases form the high tail. There are 106,782 repeated source presentations and 6,499 cross-channel source hashes. Complete distributions/group counts are retained in the [dry-run summary](../../experiments/manifests/lexical_reader_v2/mixed-reader-dry-run.attempt02.json). Repetition adds no distinct empirical support.

28. **Pilot phase/LR configurations bound?** Yes. Six unstarted seed-42 configurations cover B100/C101 × 1e-4, 3e-4, 6e-4. Nominal phases are 6,666,667 / 2,666,667 / 666,666. Shared actual endpoint is update 305, exposure 10,007,223, ordinal 134,590, ledger hash `21c3f5838f5c7e85f258e8eef25b2b38884a2023199afc5d1852d68155b04f2f`. Warmup is included in the 10M budget at 200,000 exposures, then continuous cosine reaches 10% of peak at nominal 10M with no phase reset. All configs bind the same profile, accepted pools, tokenizer and 396-case DEVELOPMENT panel. BENCH uses peak 3e-4 only for performance qualification and does not select an LR.

29. **Identical ordered B/C presentations?** Yes. Fresh attempt03 controls match all 22 queues / 9,825 presentations / 721,724 exposures. BENCH matches all 181 common queues / 79,827 presentations / 5,938,207 exposures, including every ordered presentation ID, phase/channel, S/Y/R hash, canonical charge, cumulative exposure and common boundary. B has 182 additional queues, fully audited rather than claimed paired.

30. **Independent fairness confirmation?** Yes. Separate reconstruction checks every actual native row, tensor, target/EOS or event program, pointer/encoder position, legal mask, padding count and whole-queue denominator. Initial/final B 525 and C 549 checkpoint arrays, exact FP32 parameter counts, finiteness, zero accumulators, code/data/runtime identities and clocks pass. See [fairness audit](PAIRED_READER_FAIRNESS_AUDIT_V3.md) and [closure receipt](../../experiments/manifests/lexical_reader_v2/independent-bench-closure.attempt03.json).

31. **32,768-anchor complete updates qualified?** Yes. All native controls, cold paths and BENCH use first-whole-presentation endpoints and complete queued objectives. First queue is 32,815 exposures / 444 examples: B 28 microsteps, C 111. Full BENCH charge ranges B 32,768–32,950, C 32,768–32,890; common queues match despite native padding/partition differences.

32. **B microbatch/accumulation regime?** 16 examples per microbatch, BF16 working forward/backward, FP32 loss sums, master weights, moments and gradient accumulation. Divide every microbatch loss by the entire queued target/EOS count; no second division. Clip, AdamW update and accumulator clear once per complete common queue.

33. **C microbatch/accumulation regime?** Four examples per microbatch, same precision/update policy, with full-queue action/start/end/vocabulary component denominators. Zero-count components are omitted. Microbatch partitions and native padding differ while canonical scientific queues remain identical.

34. **Five complete warmups?** Yes, five per arm on the exact nonzero 3e-4 continuous pilot LR clock.

35. **100 complete timed updates?** Yes, 100 per arm; elapsed 418.883723s B and 1,583.990968s C, with finite actual objective/gradient updates.

36. **B sustained >=20 minutes?** Yes. 258 additional complete updates, 1,202.824593s, 8,465,409 canonical exposures.

37. **C sustained >=20 minutes?** Yes. 76 additional complete updates, 1,200.279867s, 2,493,348 canonical exposures.

38. **Conservative B rate?** 7,037.941398527 canonical anchors/sec, full sustained rate lower than final-quarter 7,858.141478.

39. **Conservative C rate?** 2,044.193292797 canonical anchors/sec, final-quarter rate lower than full sustained 2,077.305525.

40. **Peak memory/system pressure?** Recorded training MLX peaks: B 4,093,362,692 bytes, C 3,365,844,548; recorded process RSS B 5,148,753,920, C 5,131,649,024. These are monitored maxima, not guaranteed whole-job/whole-machine peaks. Swap-used first/max/last M: B 11,747.06 / 15,044.19 / 11,874.50; C 11,714.44 / 11,714.44 / 5,861.44. Reported free-memory ranges B 26–86%, C 68–86%. All sampled indicators show AC power and no recorded thermal/performance warning; no claim of zero swap or proven absent throttling. Host Apple M5 Pro 48GiB / 18 logical CPUs / macOS 27.2 arm64. Full scope and raw-snapshot hashes are in [BENCH v3](PAIRED_COMPLETE_UPDATE_BENCH_V3.md).

41. **Boundary resume?** Yes, fresh repaired-code attempt03 B and C each match 21 complete updates 2–22 exactly. Cold load B 1.183204s, C 1.621159s.

42. **B mid-update resume?** Yes. Fresh attempt03 restores pending queue 2 then matches updates 2–22, including the next 20 complete updates, exact FP32 state/reader hashes, losses, LR, denominators and ordered IDs. Cold load 1.107982s.

43. **C mid-update resume?** Yes under `28298ad`, all 21 exact updates 2–22, cold load 1.683322s. Preserved attempt02 failed update 2: original loss 14.96543151512742 versus 14.965431524440646 with 410 differing leaves. The causal diagnostic finds exact pending state but JSON-reordered reduction keys; restore now validates counts and reinstates original component order. No tolerance is relaxed.

44. **Cold next-20 equality?** Yes for all four fresh cold processes. Mid replay completes the pending update plus 20 further updates; boundary replay includes the next 20 plus one additional. Independent captures/array receipts pass. Attempt01 clock gaps and attempt02 C-mid failure remain historical, preserved evidence; all six qualification calls repeated under the final freeze. The repair changes no objective weight, clipping or optimizer formula.

45. **One-B 10M duration?** 4,352.122448s = 1.208923h before reserve; 5,440.153060s = 1.511154h with 25%. Includes actual 10,007,223 exposures, warmup, startup, 13 saves, load, six 396-case decode/scorer panels and one interruption allowance.

46. **One-C 10M duration?** 6,450.020129s = 1.791672h before reserve; 8,062.525162s = 2.239590h with 25%, using the same component accounting.

47. **All-six duration with 25% reserve?** 41,191.750631s = 11.442153h serialized on the measured M5 Pro. Formula `1.25 * (3*T_B + 3*T_C + shared)`; shared scratch construction 546.972772s is included once. All-six before reserve 32,953.400505s. [Cost projection](BC_10M_PROBE_COST_PROJECTION_V2.md) separates measured, calculated, assumed and unpriced items.

48. **Unpriced work?** Future intermediate-checkpoint decode variation outside the initial/final per-case timing envelope; interruptions beyond one per recipe; final 150M campaign, baselines, sealed evaluation and paper production. No one-month final-paper feasibility claim follows from development-probe pricing.

49. **Final/sealed candidate inference?** No. Only the frozen DEVELOPMENT panel is admitted for runtime pricing. Invalid/capped outputs remain in the timing population.

50. **`paper_protocol_v2` frozen?** No.

51. **Any six-probe slot consumed?** No. All six configurations remain `CONFIGURED_UNSTARTED_UNAUTHORIZED`, with zero consumed slots. Native controls/BENCH are separately labeled qualification jobs; their weights are discarded for probes.

52. **Another scientific-review trigger?** No. Revised table, accepted pools, complete CPU ledger and actual per-arm BENCH all pass entry/separator concentration limits. C101 cold failure was a reproduced checkpoint implementation defect; restoring the approved reduction order makes the fresh exact gate pass. No scientific treatment, architecture, objective, allocation, severity, scheduler, LR or protocol choice changed.

53. **Scientifically admissible six probes?** Yes, under the preserved frontier decision and fixed scientific recipe. Every required qualification gate passes, including complete native BENCH, independent matched consumption, all cold resumes and final integrated 372 tests in 33.25s. All six slots remain unstarted; BENCH weights must not seed them. This admission does not establish learned quality, select an LR or authorize final150M/sealed work. Publish this qualification checkpoint and stop; actual six runs require a separately authorized NEW session.

AUTHORIZE_10M_BC_DEVELOPMENT_PROBES
