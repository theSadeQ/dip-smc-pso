# Design Token Validation (Phase 3 Wave 0)

- Source file: `../phase2_audit/design_tokens_v2.json`
- Version: 2.0.0
- MD5 checksum: `d48a8fe56eee4515461a027e1298105f`
- Breaking changes: 24 (see `baselines/tokens/token_comparison_v1_v2.md`)

## Critical Token Snapshot

Refer to `baselines/tokens/token_values_critical.json` for the complete machine-readable export that powers UI-002/003/004/020-027 fixes. Key highlights:

| Token | New Value | Target Issues |
|-------|-----------|---------------|
| --color-text-muted | #6c7280 | UI-002 |
| --color-code-notice-bg | #1b2433 | UI-003 |
| --color-code-notice-text | #f8fbff | UI-003 |
| --spacing-stack-sm | 12px | UI-005 |
| --spacing-stack-md | 16px | UI-007, UI-008 |
| --spacing-inline-sm | 8px | UI-009 |
| --font-size-h1-mobile | 2.25rem | UI-020 |
| --font-weight-link | 600 | UI-026 |

Checksums are logged in `baselines/tokens/checksums.json` (generated Wave 0).
