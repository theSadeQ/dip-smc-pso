# Validation Procedures

Structured test plans aligned to the seven remediation themes. Each checklist must pass before theme sign-off. Document evidence (screenshots, Lighthouse reports) in project wiki.

---

## Theme 1 – Accessibility Critical

| Step | Action | Tool / Command | Expected Result | Owner |
|------|--------|----------------|-----------------|-------|
| 1 | Run automated contrast audit on staging (`/docs/index.html`). | Chrome DevTools Lighthouse (Accessibility) | Score ≥ 95; no contrast violations logged. | Accessibility Specialist |
| 2 | Verify screen reader announcement of collapse status. | NVDA + Chrome; trigger collapse toggle. | Status message read: “Code block collapsed. Press enter to expand.” | Accessibility Specialist |
| 3 | Check `prefers-reduced-motion` handling. | macOS Safari → System Prefs → Reduce Motion. | Collapse animations disabled; focus states intact. | Frontend Dev |
| 4 | Manual keyboard traversal of code controls. | Physical keyboard | Focus order: Copy → Collapse → Expand; `Enter` toggles state; `Space` activates buttons. | QA |

## Theme 2 – Spacing System

| Step | Action | Tool | Expected Result | Owner |
|------|--------|------|-----------------|-------|
| 1 | Compare hero layout before/after (pixel diff). | Percy snapshot at 1440px | Visual diff shows consistent 8px multiples, no overlapping modules. | UX Designer |
| 2 | Inspect footer metadata spacing at 320px. | Chrome Device Toolbar (iPhone SE) | Metadata block uses 12px line-height; no text collisions. | QA |
| 3 | Audit for legacy spacing classes. | `rg -n \"spacing-\" docs/_static` | No orphaned legacy classes; new utilities documented. | Frontend Dev |

## Theme 3 – Responsive Mobile-First

| Step | Action | Tool | Expected Result | Owner |
|------|--------|------|-----------------|-------|
| 1 | Validate navigation grid at 320px/375px/768px. | BrowserStack (iPhone 13, Pixel 5, iPad Mini) | Single column <=375px, two columns at 768px, balanced gutter. | QA |
| 2 | Test mobile code control stacking. | Chrome Device Toolbar (Pixel 5) | Buttons stack with 12px gap; no overflow. | Frontend Dev |
| 3 | Monitor CLS/LCP. | Lighthouse Mobile | CLS <0.1; LCP <2.5s after responsive updates. | PM / DevOps |

## Theme 4 – Typography Hierarchy

| Step | Action | Tool | Expected Result | Owner |
|------|--------|------|-----------------|-------|
| 1 | Generate type scale specimen page and review. | Custom Storybook / Typography doc | All headings follow ratio; body copy remains 16px w/ 1.6 line-height. | UX Designer |
| 2 | Run text zoom accessibility test (200%). | Firefox + `Ctrl +` | Content reflows without clipping; anchors remain visible. | Accessibility Specialist |
| 3 | Contrast check for inline warnings. | WebAIM Contrast Checker (#b91c1c on bg) | Ratio ≥4.5:1 for new palette. | UX Designer |

## Theme 5 – Interaction Patterns

| Step | Action | Tool | Expected Result | Owner |
|------|--------|------|-----------------|-------|
| 1 | Test right-rail anchor states. | Tab navigation + screen reader | Active anchor uses color + indicator; SR announces “Current section”. | Accessibility Specialist |
| 2 | Back-to-top FAB hover/focus states. | Mouse + keyboard | Hover adds elevation; focus ring visible; button label accessible to SR. | QA |
| 3 | Coverage matrix sticky header. | Scroll test at 1440px | Header remains visible; no jitter. | Frontend Dev |

## Theme 6 – Color System Compliance

| Step | Action | Tool | Expected Result | Owner |
|------|--------|------|-----------------|-------|
| 1 | Run design token diff (v1 → v2). | `json-diff design_tokens_v1.json design_tokens_v2.json` | Only approved tokens change; log diff in decision log. | Design Ops |
| 2 | Validate dark mode overrides. | Toggle theme switcher in docs | Muted text passes ≥3:1 in dark mode; gradients still legible. | UX Designer |
| 3 | Color blindness simulation. | Stark / Polypane | Key states remain distinguishable in Deuteranopia/Protanopia/Tritanopia. | UX Designer |

## Theme 7 – Streamlit Alignment

| Step | Action | Tool | Expected Result | Owner |
|------|--------|------|-----------------|-------|
| 1 | Launch Streamlit staging with theme flag enabled. | `streamlit run streamlit_app.py --theme dip` | Gradient buttons, spacing, typography match documentation tokens. | Frontend Dev |
| 2 | Keyboard navigation across widgets. | Browser keyboard | Buttons, tabs, metrics focusable; focus ring matches docs. | QA |
| 3 | Contrast and performance check. | axe DevTools + Chrome Performance | No contrast violations; CSS injection adds <3KB gzip overhead. | Accessibility Specialist |
| 4 | Wide mode regression. | Toggle “Use wide mode” in Streamlit sidebar | Layout remains aligned; wrappers respect max-width. | QA |

---

## Regression Sweep (All Themes)

1. **Automated**: GitHub Action running `pytest` visual diff + Lighthouse (desktop & mobile).
2. **Manual Smoke**: Cross-browser check (Chrome, Firefox, Safari, Edge latest) for docs homepage, controllers reference, coverage matrix, Streamlit dashboard.
3. **Print-to-PDF**: Ensure code expands and spacing remains consistent.
4. **Analytics hooks**: Confirm events (e.g., code collapse toggles) still fire via Segment/GA.

Record pass/fail in QA tracker; unresolved defects block Phase 2 completion report.

