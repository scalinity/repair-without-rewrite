# Generation-2 source preparation

FACT — The prospective decision is committed at `98c0610`; physical storage qualification is committed at `d03f343`. This step freezes requests before recognition. It does not qualify hypotheses, D1, the expanded panel, or native student training.

MEASURED RESULT — The unchanged approved metadata joins exactly 14,113 TRAIN, 1,900 CAL and 796 HPO rows, with 52 natural DEVELOPMENT groups and no cross-role source-group or derivation-family overlap. The original 1,024 TRAIN and 108 natural DEVELOPMENT sources and reference bytes match the census. The historical `calibration_development_consumed` label binds to its original CAL role; the historical panel is unchanged. See `experiments/manifests/generation_2/metadata-census-summary.attempt01.json` and `source-join-implementation.attempt01.json`.

FACT — `parakeet-requests.attempt01.json` freezes 13,089 new TRAIN and 2,588 new DEVELOPMENT unique calls, followed by the already frozen 32+32 replay calls. The maximum is 15,741; no new source call has run. `development_calibration_consumption_generation_2.attempt01.json` records all 1,900 duration-eligible CAL rows prospectively, preserves the prior overlay and prohibits fitting on them.

MEASURED RESULT — The already available official archives yield all 1,566 required train-clean-100, 443 dev-clean and 353 dev-other recordings. Every extracted FLAC is mono PCM16 at 16 kHz and has 32,000–192,000 decoded samples. Original archive sizes, official MD5 and SHA256 match before extraction. Private audio and inventories remain on the bound external root; public receipts are `audio-*.attemptNN.json`. train-clean-100 attempt01 failed before native audio access because the test environment lacked soundfile; attempt02 used the unchanged pinned source environment and passed. The failed console/start record is retained.

FACT — The guarded downloader is acquiring only the official train-clean-360 and train-other-500 archives directly on external storage. This report makes no claim that either acquisition has completed. No required row can be dropped, replaced or truncated. A completed extraction remains audio qualification only.

MEASURED RESULT — Ten source-join/audio tests and eight whole-presentation U8 tests pass. The integrated suite passes 412 tests, zero failures or skips, in 34.97 seconds; `source-preparation-full-tests.attempt01.json` binds the retained log. U8 native gradients, checkpoints and resume have not been qualified.

FACT — `scientific-status.attempt01.json` records all seven G2 recipes as AUTHORIZED_UNSTARTED. Zero scientific slots, teacher calls, TTS calls or final/sealed runs occurred. No Time Machine snapshot or dependency lock changed.

PROPOSED NEXT ACTION — Finish official acquisition, qualify every remaining native recording, construct the exact frozen recognizer requests, and retain all failed attempts. Complete historical/native/resume/ByT5/cost and independent admission checks before any separate execution session.

G2_SOURCE_REQUESTS_FROZEN_AUDIO_ACQUISITION_IN_PROGRESS
