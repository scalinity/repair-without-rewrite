# Post-10M DEVELOPMENT decision

MEASURED RESULT — **CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE**. FACT — Campaign freeze SHA-256 `43a97ef40acbb2efebaf4941931934969c093e23f77b69bfd132f236755b1dd3`. [campaign-freeze.attempt01.json](../../experiments/manifests/six_10m_probes/campaign-freeze.attempt01.json). Endpoint decisions: [endpoint-selection.attempt01.json](../../experiments/manifests/six_10m_probes/endpoint-selection.attempt01.json). Descriptive tables and raw-output/resource hash bindings: [descriptive-tables.attempt01.json](../../experiments/manifests/six_10m_probes/descriptive-tables.attempt01.json).

| Arm | Eligible ranking | Selected peak LR |
| --- | --- | --- |
| B100 | [] | None |
| C101 | [] | None |


MEASURED RESULT — Every recipe completed the prescribed endpoint; all six endpoint metrics and failed gates are in the arm-selection reports. The frozen eligibility and exact ranking were applied without a subjective tie or intermediate-checkpoint override.

| Recipe | WER errors / 2,270 | WER | Repair | Completed repair | Support groups | Introduced errors | Introduced rate | Preserved / 2,210 | Byte / lexical identity / 108 | Invalid or incomplete |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B100 / 1e-04 | 2208 | 97.268722% | 6–6 | 6–6 | 3 | 2150–2150 | 94.713656%–94.713656% | 91–100 | 0 / 0 | 0 |
| C101 / 1e-04 | 121 | 5.330396% | 0–0 | 0–0 | 0 | 57–57 | 2.511013%–2.511013% | 2153–2153 | 88 / 90 | 0 |
| B100 / 3e-04 | 2584 | 113.832599% | 2–2 | 2–2 | 2 | 2522–2522 | 111.101322%–111.101322% | 121–132 | 0 / 0 | 0 |
| C101 / 3e-04 | 128 | 5.638767% | 0–0 | 0–0 | 0 | 64–64 | 2.819383%–2.819383% | 2148–2148 | 87 / 87 | 0 |
| B100 / 6e-04 | 2664 | 117.356828% | 2–2 | 2–2 | 2 | 2602–2602 | 114.625551%–114.625551% | 126–146 | 0 / 0 | 0 |
| C101 / 6e-04 | 109 | 4.801762% | 0–0 | 0–0 | 0 | 45–45 | 1.982379%–1.982379% | 2168–2168 | 96 / 96 | 0 |


| Recipe | Clean /96 | Mixed /96 | Required-only /96 | Whole case /288 | Genuine repaired cases /192 | Repaired fields /288 | Structure failures /288 | Decoder failures /288 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B100 / 1e-04 | 0 | 0 | 0 | 0 | 0 | 0 | 288 | 0 |
| C101 / 1e-04 | 93 | 32 | 6 | 131 | 49 | 55 | 70 | 0 |
| B100 / 3e-04 | 0 | 0 | 0 | 0 | 0 | 0 | 288 | 3 |
| C101 / 3e-04 | 96 | 42 | 11 | 149 | 79 | 90 | 19 | 0 |
| B100 / 6e-04 | 0 | 0 | 0 | 0 | 0 | 0 | 288 | 0 |
| C101 / 6e-04 | 96 | 30 | 6 | 132 | 54 | 60 | 43 | 0 |


FACT — Neither arm has an eligible recipe. No LR is selected for either arm and the current prospective 150M campaign is not admissible. This measured DEVELOPMENT result does not prove either architecture can never work.

DESCRIPTIVE INFERENCE — B100 failure-inclusive natural WER and zero generated required repair threaten the planned comparison. C101 generated learning supports a narrower observation that the model can learn some approved editing tasks; natural viability must still be established under an explicitly approved future design. Lower training loss and efficient decoding cannot replace the registered viability criteria.

FUTURE SCIENTIFIC DECISION — The next step is a separate Astra adequacy/comparator/scope/final-cost review using the complete preserved evidence. Any scientific change requires explicit authorization; no extra trial or final campaign has started. No H1 confirmation is claimed: seed42 is an HPO/development seed, final three-seed training has not occurred, paper_protocol_v2 is unfrozen and final populations remain sealed/unrun.

FACT — Campaign hard stop: no seventh LR recipe, alternative seed, final150M, sealed inference, paper_protocol_v2 freeze, A100 or H2. The two selected-model descriptive comparison is unavailable if either arm has no selected viable endpoint.

CURRENT_150M_CAMPAIGN_NOT_ADMISSIBLE
