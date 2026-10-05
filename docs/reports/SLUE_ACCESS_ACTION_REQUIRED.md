# SLUE access action required

Status: **AUTO-GATED ACCESS PENDING**. Checked October 5, 2026. Only this acquisition branch is stopped; LS-PC source, tokenizer and training-supply work may continue within their own gates.

The [official ASAPP dataset page](https://huggingface.co/datasets/asapp/slue) currently requires the owner to share contact information and accept access conditions while signed into Hugging Face. Its public card is visible, but visibility is not permission to acquire gated payloads. The [official toolkit](https://github.com/asappresearch/slue-toolkit) identifies that Hub release as the source of released test labels; its January 2024 notice supersedes its older text about submitting predictions for hidden-label scoring.

The owner must:

1. Sign into their own Hugging Face account and open [asapp/slue](https://huggingface.co/datasets/asapp/slue).
2. Review the displayed conditions and contact-information disclosure, then personally accept/submit the official access request if they agree.
3. Once access is granted, make that already-authorized account available to the normal local Hugging Face client. Do not paste credentials into chat, reports or Git. The agent can then verify permission and acquire the pinned assets normally.

No agreement was accepted, no contact information was submitted, no browser sign-in was attempted, and no restricted payload was downloaded. The normal local Hub client had **no available credential** when checked; this does not assert anything about uninspected browser sessions.

The current read-only check used the actual pinned official DEV-label path:

```json
{
  "checked_utc": "2026-10-05T08:41:40.886369+00:00",
  "credential_available": false,
  "operation": "HEAD pinned official VoxCeleb DEV label path only; no acceptance or payload download",
  "url": "https://huggingface.co/datasets/asapp/slue/resolve/67f7da031721a14cc391c7fa7c8d96411282d8a3/data/voxceleb/dev.tsv",
  "http_status": 401
}
```

This preserves the previous acquisition failures in `PUBLIC_SOURCE_QUALIFICATION.md` and `experiments/manifests/public_sources.json`. There are **zero acquired/inventoried SLUE rows in this branch**. The published VoxCeleb counts remain 5,777 train, 1,454 validation and 3,553 test; they are not local qualification counts. After authorized acquisition, preserve speaker/video closure, released `normalized_text`, exact crop bounds, and license/attribution notices described in the [official dataset card](https://huggingface.co/datasets/asapp/slue/blob/67f7da031721a14cc391c7fa7c8d96411282d8a3/README.md).

The fixed equal-domain endpoint remains undefined until SLUE is available and qualified. No LS-PC-only reweighting, substitution, alternate download route or primary-population amendment is admitted here. Do not execute the toolkit's older download script to route around the currently observed gate.
