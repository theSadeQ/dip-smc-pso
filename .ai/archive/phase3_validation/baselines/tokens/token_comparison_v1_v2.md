# Design Tokens: v1 -> v2 Migration Report

**Generated:** 2025-10-14T21:01:36.639344
**Source:** D:\Projects\main\.codex\phase2_audit\design_tokens_v2.json
**Baseline:** D:\Projects\main\.codex\phase1_audit\phase1_design_tokens.json

---

## Breaking Changes

| Category | Key | v1 Value | v2 Value | Severity |
|----------|-----|----------|----------|----------|
| colors | info | #3b82f6 | None | non-breaking |
| colors | error | #ef4444 | None | non-breaking |
| colors | primary-light | #e6ebf5 | None | non-breaking |
| colors | text-danger | None | #b91c1c | breaking |
| colors | background-primary | #ffffff | None | non-breaking |
| colors | accent-neutral | None | #2563eb | non-breaking |
| colors | danger-bg | None | #fee2e2 | non-breaking |
| colors | text-secondary | #6b7280 | #616774 | breaking |
| colors | background-tertiary | #f3f4f6 | None | non-breaking |
| colors | primary-hover | #08204d | #0b2763 | non-breaking |
| colors | success | #10b981 | None | non-breaking |
| colors | tip | #8b5cf6 | None | non-breaking |
| colors | bg-primary | None | #ffffff | non-breaking |
| colors | primary | #0b2763 | #2563eb | non-breaking |
| colors | text-muted | #9ca3af | #6c7280 | breaking |
| colors | bg-muted | None | #f9fafb | non-breaking |
| colors | info-bg | None | #dbeafe | non-breaking |
| colors | warning | #f59e0b | None | non-breaking |
| colors | bg-secondary | None | #f3f4f6 | non-breaking |
| colors | border | #e5e7eb | #d9dde3 | non-breaking |
| colors | background-secondary | #f9fafb | None | non-breaking |
| metadata | color-text-muted: #9ca3af -> #6c7280 (contrast fix) | - | - | breaking |
| metadata | color-text-secondary: #6b7280 -> #616774 (harmonization) | - | - | breaking |
| metadata | spacing system: ad-hoc -> 8-point grid | - | - | breaking |

---

## Migration Notes

- **from_v1:** Token values aligned with WCAG AA compliance
- **breaking_changes:** Muted text color darkened from 2.54:1 to 4.52:1 contrast
- **rollback:** v1 alias maintained at .codex/phase1_audit/phase1_design_tokens.json
- **css_variables:** All tokens exported as CSS custom properties (--token-name)
- **streamlit_integration:** JSON consumed by streamlit_app.py via pathlib.Path

---

## Rollback Instructions

If Phase 3 requires rollback to v1 tokens:

```bash
# Restore v1 alias
cp D:\Projects\main\.codex\phase1_audit\phase1_design_tokens.json .codex/phase2_audit/design_tokens_v1_rollback.json
# Update CSS references
# (Manual step: revert CSS custom properties to v1 values)
```

