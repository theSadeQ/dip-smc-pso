# Tooling Validation Summary (Wave 0)

| Check | Result | Evidence |
|-------|--------|----------|
| Sphinx dev server | PASS | `http://localhost:9000` smoke test (14 Oct 2025) |
| Node.js runtime | PASS (v22.19.0) | `node --version` |
| Playwright Python | PASS (1.47.0) | `playwright install chromium` |
| Lighthouse CI config | PASS (A11y target >=95) | `.lighthouse/lighthouserc.json` |
| axe-core config | PASS (WCAG AA, 0 critical) | `.axe/axe.config.json` |
| Percy setup | PASS (4 viewports) | `package.json` percy block |

Detailed logs: see `./tooling_validation.md` for the full Wave 0 validation narrative.

Initial Lighthouse/axe baseline executions deferred to Wave 1 once token fixes are merged.
