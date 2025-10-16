# Alternative Approaches Evaluation

Quantitative comparison of the primary design and implementation decisions for Phase 2. Effort hours reflect UX + FED pairing time; ROI score = (User Impact % × Severity Weight) ÷ Effort.

---

## 1. Muted Text Contrast Remediation

| Option | Palette | Effort (hrs) | User Impact | Accessibility Margin | Pros | Cons | ROI | Decision |
|--------|---------|--------------|-------------|----------------------|------|------|-----|----------|
| A | `#6c7280` (Phase 2 draft) | 3 | 88% of doc pages | 4.52:1 | Minimal delta from existing brand, aligns with Tailwind slate-500 analogs; preserves dark-mode parity with single override. | Narrow WCAG buffer (0.02) leaves little headroom for future background adjustments. | 29.3 | **Selected** — fastest path with acceptable buffer once paired with 3:1 large-text fallback. |
| B | `#667085` (darker slate) | 5 | 88% | 5.02:1 | Adds 0.5 contrast buffer improving low-vision comfort; still brand-consistent. | Requires rebalancing `text-secondary` + `border` tokens; dark mode adjustments to avoid 2.0:1 on dark surfaces. | 26.4 | Rejected for Phase 2; consider in Phase 3 when full grayscale refactor scheduled. |
| C | `#4b5563` (near-secondary) | 6 | 88% | 6.62:1 | Maximizes contrast, no risk of WCAG regression. | Collapses hierarchy between secondary and muted styles; requires typographic tweaks to retain visual differentiation. | 20.7 | Rejected — reduces typographic depth; over-corrects relative to brand tone. |

---

## 2. Responsive Strategy for Themes 2 & 3

| Option | Description | Effort (hrs) | Issues Solved | Risks | Dependencies | ROI | Decision |
|--------|-------------|--------------|---------------|-------|--------------|-----|----------|
| A | Full mobile-first refactor (rewrite layout + component CSS) | 90 | All 7 responsive issues + future proofing | Requires refactoring base theme, risk of regression across 795 pages. | Requires 3 sprint weeks, coordination with dev team. | 7.1 | Scope exceeds Phase 2 capacity. |
| B | Targeted breakpoint patches (add `@media` fixes per component) | 35 | UI-020–025 | Patchwork may reintroduce drift; duplicates hard-coded values. | Minimal; can start immediately. | 14.6 | Insufficient longevity; contradicts design system goals. |
| C | **Hybrid tokenized approach** (define breakpoint tokens + responsive utilities, retrofit components) | 48 | UI-020–025 + sets foundation for Phase 3 | Requires buy-in to adopt new utility classes; moderate regression risk mitigated via testing. | Dependent on spacing token rollout (Theme 2). | 18.3 | **Selected** — balances sustainability with achievable effort. |

---

## 3. Code Collapse Accessibility Pattern

| Option | Implementation | Effort (hrs) | Issues Covered | Pros | Cons | Risk | Decision |
|--------|----------------|--------------|----------------|------|------|------|----------|
| A | Keep pseudo-element, add `aria-live` | 6 | UI-001, UI-003 | Minimal template work; limited CSS delta. | Screen readers still ignore `::after`; fails core requirement. | High (fails WCAG 4.1.2) | Rejected. |
| B | Replace with inline DOM node (`div.collapsed-notice` + `role="status"`) | 18 | UI-001, UI-003, UI-004, UI-021 | Works for SR + visual users; supports translations; consistent with W3C accordion pattern. | Requires Sphinx template edits + JS adjustments. | Low once tests added. | **Selected**. |
| C | Use native `<details>/<summary>` | 22 | UI-001, UI-003, UI-004 | Native accessibility; reduced JS. | Requires restyling to match design; `<summary>` semantics conflict with copy button; browsers treat as interactive text, altering layout. | Medium (layout + keyboard regressions) | Defer — candidate for Phase 3 exploration. |

---

## 4. Spacing System Strategy

| Option | Description | Effort (hrs) | Issues Impacted | Pros | Cons | ROI | Decision |
|--------|-------------|--------------|-----------------|------|------|-----|----------|
| A | Adopt strict 8px baseline (4/8/16/24/32) with utility classes | 40 | UI-005, UI-007, UI-008, UI-014, UI-018, UI-019, UI-021, UI-023, UI-030 | Aligns with existing design vocabulary; easy mental model; simplifies responsive adjustments. | Requires audit of legacy 10px/12px spacing; utility naming decisions. | 16.2 | **Selected**. |
| B | Fluid spacing (clamp-based) | 55 | Same set + potential future components | Provides smooth scaling between breakpoints. | Higher implementation complexity; needs design QA for each breakpoint; risk of inconsistent line heights. | 12.5 | Not chosen for Phase 2; consider for hero/marketing surfaces later. |
| C | Component-scoped spacing (keep per-component values) | 18 | Limited subset | Minimal disruption. | Maintains inconsistency; fails to create systemized approach; duplicates logic. | 9.1 | Rejected. |

---

## 5. Design Token Technology Stack

| Option | Format | Effort (hrs) | Tooling Impact | Pros | Cons | Governance Fit | Decision |
|--------|--------|--------------|----------------|------|------|----------------|----------|
| A | CSS custom properties + JSON manifest (current plan) | 16 | Works with Sphinx + Streamlit | No new build tooling; instant theming; facilitates downstream adoption. | Requires documentation for JS consumers; CSS var fallback needed for legacy browsers (IE11 out of scope). | Aligns with current repo stack. | **Selected**. |
| B | SCSS variables compiled to CSS | 28 | Needs Sass build step | Supports compile-time math, extends to other preprocessors. | Adds build dependency; Streamlit injection still needs CSS. | Misaligned with Python-first toolchain. | Rejected. |
| C | Python constants exported to both Sphinx + Streamlit | 32 | Tight integration with backend | Ensures single source of truth. | Coupling design to Python release cadence; harder for external consumers; requires bundler for CSS output. | Risky for multi-surface use. | Defer pending design system service discussion. |

---

## Summary

- **Adopt tokenized hybrid responsive approach**, enabling both documentation and Streamlit surfaces to share the same breakpoint logic.
- **Inline DOM accessibility pattern** ensures conformance with WCAG 4.1.2 (Name, Role, Value) without sacrificing visual fidelity.
- **CSS custom properties + JSON manifest** remain the source of truth, lowering effort while keeping governance simple.

