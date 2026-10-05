# Independent initial secret-scan classification

Every one of the **970 `generic-api-key` findings** in the initial full-history scanner report was inspected against its actual recorded commit, file and line. The scanner report had redacted its value fields; each exact original value was recovered uniquely from the preserved Git blob and the recorded match context. Exact original blobs, lines, values, fingerprints and verification evidence are retained privately outside the repository. No candidate value is reproduced here.

| Classification | Findings |
|---|---:|
| Real credential | 0 |
| Synthetic credential-shaped fixture value | 0 |
| Code or metadata hash producing a scanner pattern match | 970 |
| Unclassified | 0 |

The 970 hash findings comprise:

- **960 panel-selection digests** in four synthetic stress JSONL artifacts. Every value was independently recomputed from its recorded generator version and complete deterministic seed tuple. These are selection metadata, including when they occur in synthetic fixtures.
- **6 tokenizer asset digests** in the two Qwen configuration/result artifacts. Their exact fields and pinned-asset provenance were inspected alongside the recorded writer, which hashes file bytes and checks declared asset equality before model loading.
- **4 source/test file digests** in three MODEL0 evidence artifacts. Every value matched the SHA-256 of its corresponding source or test Git blob at the finding's recorded commit.

The reviewed population spans **9 files, 4 recorded commits and 970 distinct finding fingerprints**. Nine finding blobs and seven additional verification-source blobs were preserved verbatim before classification. Each finding has its own classification and evidence in the private receipt.

No source value was redacted, no Git history or index was changed, no network request was made, and no global rule or pattern allowlist was created by this review. These classifications apply to the exact supplied initial findings; they do not establish clearance for unrelated credentials or personal identifiers, later findings, or the complete publication candidate. The separate full-tree/full-history publication audit remains authoritative for those checks.
