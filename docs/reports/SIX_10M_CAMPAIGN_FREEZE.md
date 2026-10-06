# Six 10M DEVELOPMENT campaign freeze

FACT: The pre-run campaign is frozen at SHA-256 `43a97ef40acbb2efebaf4941931934969c093e23f77b69bfd132f236755b1dd3` in `experiments/manifests/six_10m_probes/campaign-freeze.attempt01.json`, before any scientific optimizer update or recipe inference. Exact clean source commit: `1ad1ea1f0313d548e8af6cfaf75d5ff87fee6feb`. The authorized base is `7868302afc43e3cbd475464452f57912a9c2cf97`; the native implementation remains `28298ad886aa321882aa0530a18421e7d4e3553e`.

MEASURED RESULT: Fresh deterministic seed-42 initialization produces B100 parameter hash `2739837ff4ad4ff26475dca5a37608d9c46a1c7ff34f8778f24eadb18b8e8044` and C101 hash `9671ba3aaf0afb9fe22302fe140512db7bdf7e31f4d9e439bc13c75edafc2ff1`. Parameter counts are 100,686,336 and 101,081,859. These are pre-run construction identities, not pretrained or BENCH weights; every actual recipe independently constructs and verifies its initial state.

FACT: All six manifest entries are `AUTHORIZED_UNSTARTED`. Their execution order is:

1. `B100-seed42-lr1e-04`
2. `C101-seed42-lr1e-04`
3. `B100-seed42-lr3e-04`
4. `C101-seed42-lr3e-04`
5. `B100-seed42-lr6e-04`
6. `C101-seed42-lr6e-04`

FACT: The manifest binds every source/config/data hash, the corrected frozen ledger, the 396-case DEVELOPMENT panel and generated latents, model/optimizer/precision/cap settings, phase/exposure/LR clocks, 13 save endpoints, six evaluation endpoints, clipping, one-replay rule, exact endpoint-only eligibility and within-arm lexicographic selection, runtime versions and hardware. All six retain the shared actual endpoint: update 305, exposure 10,007,223, last ordinal 134,590. No seventh slot or final seed is authorized.

FACT: The preceding independent static review and 379-test operational suite are recorded in `docs/reports/SIX_10M_PRERUN_QUALIFICATION.md`. All frozen source hashes were rechecked after manifest creation. The actual recipe-start and endpoint receipts will establish consumed slots, completed outcomes and initialization equality across each arm's three LRs. Those outcomes do not yet exist.

PROPOSED NEXT ACTION: Publish this freeze, verify clean local/remote equality, then execute recipe 1 serially. Final/sealed inference, 150M training, A100/H2, cloud/production changes and `paper_protocol_v2` freeze remain outside authorization.

SIX_RECIPES_AUTHORIZED_UNSTARTED
