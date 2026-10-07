# Generation-2 official native audio qualification

FACT — The prospective source census contains 16,809 recordings: 14,113 TRAIN, 1,900 CAL and 796 HPO. All five official native splits are retained, with no subset, replacement, resampling or source-recognizer outcome exclusion.

MEASURED RESULT — Direct official acquisition completed in 2,585.130160 seconds. The two new archives total 53,642,979,491 bytes. train-clean-360 matches official MD5 `c0e676e450a7ff2f54aeade5171606fa` and SHA-256 `146a56496217e96c14334a160df97fffedd6e0a04e66b9c5af0d40be3c792ecf`; train-other-500 matches MD5 `d1a0fd59409feb2c614ce4d30c387708` and SHA-256 `ddb22f27f96ec163645d53215559df6aa36515f26e01dd70798188350adcb6d2`. Receipts: `experiments/manifests/generation_2/source-archives.attempt01.json` and the completed inventories in `source-archives-v1/` under the privately bound external root.

MEASURED RESULT — Every requested native archive member was found exactly once. All 16,809 recordings are mono PCM16 FLAC at 16 kHz, with 32,000–192,000 samples and complete source-role/group/family/member/hash inventories. Split counts are 1,566 / 6,689 / 7,758 TRAIN and 443 / 353 DEVELOPMENT for train-clean-100 / train-clean-360 / train-other-500 / dev-clean / dev-other. Receipts: successful `audio-<split>.attemptNN.json` records; payloads and exact inventories remain outside Git in `source-audio-v1/`.

MEASURED RESULT — The successful extractions retained 2,302,541,093 native FLAC bytes and 124294.2237500 seconds of decoded audio, taking 157.613807 seconds in aggregate. These costs include archive rehashing, full streaming extraction, sync and atomic readback; they are separate from network acquisition and source recognition.

FACT — Failed train-clean-100 attempt01 and train-clean-360 attempts01/02 remain beside successful attempts. The first used an environment without soundfile; the latter two failed before extraction on incorrect configuration/payload key names. Only mechanical path/key handling was repaired. Their original console/source hashes and external originals are retained; no source datum was changed or excluded.

FACT — The frozen 15,741-call request list was published before recognition. Source construction is in progress under its separate numbered attempt. This audio result does not qualify hypotheses, replay determinism, native text capacities, expanded support, student runners, cost or launch admission. All seven scientific recipes remain AUTHORIZED_UNSTARTED. No teacher, TTS, final or sealed call occurred.

PROPOSED NEXT ACTION — Complete the frozen source calls and exact 64-record replay, then qualify every corpus/panel/capacity/lineage join before student qualification.

G2_OFFICIAL_NATIVE_AUDIO_QUALIFIED
