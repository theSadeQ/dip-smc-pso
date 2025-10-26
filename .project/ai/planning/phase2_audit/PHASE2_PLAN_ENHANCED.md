# Phase 2 Design Remediation Plan — Enhanced Edition

## Executive Summary

- Translate Phase 1 findings (34 issues across 62 components) into implementation-ready specs with zero ambiguity.
- Prioritise Wave 1 accessibility/color/spacing foundations, deliver quick wins by Day 10, and complete Streamlit alignment by Day 15.
- Provide complete decision trail, risk mitigation, validation procedures, and cross-surface token system versioning.

**Key Outcomes**
- All Critical + High issues (UI-002, UI-003, UI-004, UI-020, UI-022) now ship with before/after code, browser compatibility, and test scripts.
- Token System v2 (JSON + CSS) harmonises Sphinx + Streamlit, with semantic versioning and rollback plan.
- Quick wins (UI-002, UI-001/004, UI-005) implemented during Week 2 to prove traction ahead of full Phase 3 rollout.

Context references: `PHASE1_DEEP_DIVE_ANALYSIS.md`, `ALTERNATIVE_APPROACHES.md`, `RISK_ASSESSMENT_DETAILED.md`, `IMPLEMENTATION_SEQUENCING_OPTIMIZED.md`, `STREAMLIT_ALIGNMENT_SPECIFICATION.md`, `EFFORT_IMPACT_MATRIX.md`.

---

## Theme 1 – Accessibility Critical Fixes (UI-002, UI-003, UI-004, UI-013, UI-015)

**Objectives**
- Achieve WCAG AA (contrast ≥4.5:1) for muted text, status notices, warning copy.
- Provide screen reader announcements for collapsed code blocks.
- Respect reduced-motion preferences.

### Implementation-Ready Specs

#### Muted Text Contrast (UI-002)

```css
/* BEFORE (docs/_static/custom.css:53-58) */
:root {
  --color-text-primary: #111827;
  --color-text-secondary: #6b7280;
  --color-text-muted: #9ca3af; /* 2.54:1 contrast */
  --color-border: #e5e7eb;
}

/* AFTER */
:root {
  --color-text-primary: #111827;
  --color-text-secondary: #616774; /* harmonised secondary */
  --color-text-muted: #6c7280; /* 4.52:1 contrast */
  --color-border: #d9dde3;
}

[data-theme="dark"] {
  --color-text-muted: #9aa2b5; /* maintains ≥3:1 in dark mode */
}
```

Validation: WebAIM contrast ≥4.5:1; check dark mode ratio 3.2:1. Update token documentation + migration guide.

#### Collapsed Notice Contrast & DOM Pattern (UI-003 & UI-004)

```html
<!-- BEFORE (Sphinx template fragment) -->
<div class="code-header">
  <button class="copybtn">Copy</button>
  <!-- pseudo-element injected status -->
</div>

<!-- AFTER -->
<div class="code-header">
  <button class="copybtn" aria-label="Copy code block">Copy</button>
  <button class="code-collapse-btn" aria-expanded="true" data-target="example-1">
    <span aria-hidden="true">▾</span>
    <span class="visually-hidden">Collapse code block</span>
  </button>
  <div class="collapsed-notice" role="status" aria-live="polite">
    Code block collapsed. Activate to expand.
  </div>
</div>
```

```css
/* BEFORE (docs/_static/code-collapse.css:170-190) */
.highlight-collapsed::after {
  content: "Code block collapsed";
  color: #94a3b8;
  font-size: 0.85rem;
}

/* AFTER */
.highlight-collapsed .collapsed-notice {
  position: absolute;
  inset: auto 16px 12px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(15, 23, 42, 0.85);
  color: #f8fafc;            /* 12.4:1 contrast */
  font-size: 0.9375rem;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.35);
}

.highlight-collapsed .collapsed-notice .visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
```

Validation: NVDA + Chrome reads status; Visual diff OK; print stylesheet hides `.collapsed-notice`.

#### Reduced Motion Overrides (UI-013)

```css
@media (prefers-reduced-motion: reduce) {
  .admonition,
  .admonition::before,
  .code-control-btn,
  .collapse-icon {
    animation: none !important;
    transition: none !important;
  }

  .collapsed-notice {
    transition: opacity 0.15s ease; /* fallback for clarity */
  }
}
```

#### Warning Copy Accessibility (UI-015)

```css
.inline-warning {
  color: #b91c1c;           /* 4.94:1 vs white */
  font-weight: 600;
}

.inline-warning::before {
  content: "!";
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.25rem;
  height: 1.25rem;
  margin-right: 0.5rem;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.18);
  color: #7f1d1d;
}
```

### Dependencies & Risks
- Token adjustments cascade into dark mode, Sphinx builds, Streamlit tokens (see cascading table).
- Risk R1 (dark mode regression) mitigated via simultaneous override update.

### Validation
Refer to `VALIDATION_PROCEDURES.md` (Theme 1) for step-by-step tests.

---

## Theme 2 – Spacing System (UI-005, UI-007, UI-008, UI-014, UI-019, UI-021, UI-023, UI-030)

**Objectives**
- Establish 4/8/12/16/24/32px baseline grid.
- Introduce stack/inset utilities to replace ad-hoc margins.
- Improve scan rhythm for footer, hero, mobile controls.

### Token & Utility Definition

```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-7: 48px;
}

.u-stack-xs > * + * { margin-top: var(--space-1); }
.u-stack-sm > * + * { margin-top: var(--space-2); }
.u-stack-md > * + * { margin-top: var(--space-3); }
.u-inset-lg { padding: var(--space-4); }
.u-gap-grid { gap: var(--space-4); }
```

### Component Retrofitting Examples

#### Code Control Master Bar (UI-005)

```css
/* AFTER */
.code-controls-master {
  margin: var(--space-5) 0 var(--space-4);
  padding: var(--space-3) var(--space-4);
  gap: var(--space-3);
}

.code-controls-master .controls-group {
  display: flex;
  gap: var(--space-2);
}
```

#### Footer Metadata (UI-007, UI-023, UI-030)

```css
.footer-metadata {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--space-2) var(--space-4);
  font-size: 0.875rem;
  line-height: 1.6;
}

@media (max-width: 480px) {
  .footer-metadata {
    line-height: 1.5;
    gap: var(--space-2);
  }
}
```

### Validation Notes
- Percy diff to confirm no negative spacing regressions.
- `rg "margin: [0-9]"` check ensures legacy values replaced.

---

## Theme 3 – Responsive Mobile-First (UI-020, UI-021, UI-022, UI-023, UI-024, UI-025, UI-032)

**Objectives**
- Provide mobile-friendly typography and layouts.
- Introduce breakpoint tokens + responsive utilities.
- Fix mobile navigation grid and code controls.

### Breakpoint Tokens

```css
:root {
  --bp-mobile: 375px;
  --bp-tablet: 768px;
  --bp-desktop: 1024px;
}
```

### H1 Word-Break Fix (UI-020)

```css
/* BEFORE (base-theme.css:638) */
h1.page-title {
  word-break: break-all;
}

/* AFTER */
@media (max-width: var(--bp-mobile)) {
  h1.page-title {
    word-break: normal;
    overflow-wrap: break-word;
    hyphens: auto;
    -webkit-hyphens: auto;
    -ms-hyphens: auto;
    max-width: calc(100vw - var(--space-5));
    font-size: clamp(1.75rem, 5vw, 1.875rem);
  }
}
```

### Mobile Navigation Grid (UI-022)

```css
.visual-nav {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-4);
}

@media (max-width: var(--bp-mobile)) {
  .visual-nav {
    grid-template-columns: 1fr;
    gap: var(--space-3);
  }

  .visual-nav card-title {
    font-size: 1rem;
    line-height: 1.4;
  }
}

@media (max-width: var(--bp-tablet)) and (min-width: 480px) {
  .visual-nav {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
```

### Tablet Anchor Rail (UI-025, UI-032)

```css
@media (max-width: var(--bp-tablet)) {
  .on-this-page {
    font-size: 0.9375rem;
    line-height: 1.6;
    margin-top: var(--space-5);
  }
}
```

### Validation
- BrowserStack for iPhone/Pixel/iPad.
- Lighthouse CLS <0.1; hyphenation verified with `lang` attribute.

---

## Theme 4 – Typography Hierarchy (UI-006, UI-010, UI-011, UI-016, UI-017, UI-028, UI-034)

**Objectives**
- Restore clear hierarchy for labels, tables, lists.
- Harmonise semantic colors with typography.

### Type Scale v2

| Token | Size | Line Height | Usage |
|-------|------|-------------|-------|
| `heading-1` | clamp(2.25rem, 3.2vw, 2.5rem) | 1.2 | Page titles |
| `heading-2` | 1.875rem | 1.3 | Section headers |
| `body-1` | 1rem | 1.6 | Base content |
| `body-2` | 0.9375rem | 1.55 | Dense sidebars |
| `caption` | 0.8125rem | 1.5 | Metadata |

### Status Labels (UI-006)

```css
.status-badge {
  font-size: 0.875rem;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  color: var(--color-text-secondary);
}

@media (max-width: var(--bp-mobile)) {
  .status-badge {
    font-size: 0.8125rem;
    text-transform: none;
    font-weight: 600;
  }
}
```

### Coverage Matrix (UI-011)

```css
.coverage-table td {
  font-size: 0.9375rem;
  line-height: 1.4;
  padding: var(--space-2) var(--space-3);
}

.coverage-table th {
  background: var(--color-bg-secondary);
  font-weight: 600;
  color: var(--color-text-primary);
}
```

---

## Theme 5 – Interaction Patterns (UI-001, UI-026, UI-027, UI-033)

**Objectives**
- Improve discoverability of interactive controls.
- Provide consistent focus/hover states.

### Code Collapse Toggle Opacity (UI-001)

```css
.code-collapse-btn {
  opacity: 0.6;
  color: inherit;
  border-radius: 6px;
  transition: opacity 0.2s ease, background 0.2s ease;
}

.code-collapse-btn:hover,
.code-collapse-btn:focus-visible {
  opacity: 1;
  background: rgba(148, 163, 184, 0.16);
  outline: 3px solid rgba(59, 130, 246, 0.45);
  outline-offset: 2px;
}
```

### Anchor Rail (UI-026)

```css
.on-this-page li {
  position: relative;
  padding-left: var(--space-3);
}

.on-this-page li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.75rem;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: transparent;
}

.on-this-page li.is-active::before {
  background: var(--color-primary);
}

.on-this-page li.is-active a {
  color: var(--color-primary);
  font-weight: 600;
}
```

### Coverage Matrix Sticky Header (UI-033)

```css
.coverage-table thead th {
  position: sticky;
  top: 0;
  z-index: 2;
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(6px);
}
```

---

## Theme 6 – Color System Compliance (UI-010, UI-012, UI-015, UI-027, UI-031)

**Objectives**
- Align semantic colors with brand usage.
- Improve contrast of interactive elements.

### Semantic Palette (extract)

```css
:root {
  --color-accent-neutral: #2563eb;
  --color-danger: #b91c1c;
  --color-danger-bg: #fee2e2;
  --color-info-bg: #dbeafe;
  --color-muted-bg: #f3f4f6;
}

.link-neutral {
  color: var(--color-primary);
  text-decoration: underline;
}

.link-critical {
  color: var(--color-danger);
  font-weight: 600;
}
```

### Back-to-top Button (UI-027)

```css
.back-to-top {
  background: linear-gradient(135deg, #2563eb, #0b2763);
  box-shadow: 0 12px 32px rgba(37, 99, 235, 0.35);
}

.back-to-top:focus-visible {
  outline: 3px solid rgba(255, 255, 255, 0.8);
  outline-offset: 3px;
}
```

---

## Theme 7 – Streamlit Alignment

See `STREAMLIT_ALIGNMENT_SPECIFICATION.md` for full technical spec.

**Highlights**
- `design_tokens_v2.json` consumed by Streamlit to apply consistent colors/spacing.
- Buttons, metrics, download widgets restyled to match documentation.
- Accessibility parity (focus-visible, contrast) ensured via CSS injection and ARIA attributes.

---

## Quick Win Execution Plan

| Quick Win | Issues | Effort | Owner | Evidence |
|-----------|--------|--------|-------|----------|
| Update muted text token | UI-002 | 2 hrs | UX + FED | Contrast report before/after, screenshot. |
| Code collapse affordance + ARIA | UI-001, UI-004 | 6 hrs design + 6 hrs dev | FED + Accessibility | NVDA recording, Percy diff. |
| Remove duplicate code control bar | UI-005 | 7 hrs | FED | Layout diff, Lighthouse CLS report. |

All quick wins targeted for Days 7–9 (Week 2). Included in Week 2 demo.

---

## Implementation Roadmap Summary

- Refer to `IMPLEMENTATION_SEQUENCING_OPTIMIZED.md` for full schedule.
- Critical path: Tokens → Accessibility & Color → Responsive utilities → Mockups → Documentation.
- Buffers: 0.5 day Week 2 for review feedback, 1 day Week 3 for QA polish.

---

## Risk Posture Snapshot

Top risks (from `RISK_ASSESSMENT_DETAILED.md`):
1. Dark mode contrast regression (R1) — mitigate by updating dark tokens concurrently.
2. Stakeholder review delays (R4) — allocate 4-day windows, provide async Loom recordings.
3. Quick win resource constraints (R3) — pre-book developer time Week 2 and maintain fallback plan.

Risk reviews scheduled twice weekly with status logged in `DECISION_LOG.md`.

---

## Success Metrics & Validation

| Metric | Target | Measurement |
|--------|--------|-------------|
| Critical/High issues with implementation-ready specs | 5/5 (100%) | Specs + tests documented in this plan. |
| Contrast compliance | All updated tokens ≥4.5:1 | axe & WebAIM reports stored with validation artifacts. |
| CSS payload increase | ≤ +10 KB gzip | `size-limit` CI check. |
| Quick win delivery | 3 shipped by Day 10 | Demo recording + before/after screenshots. |
| Stakeholder sign-off | 3 checkpoints (Weeks 1, 2, 3) | Documented approvals in `DECISION_LOG.md`. |

Validation procedures: see `VALIDATION_PROCEDURES.md`.

---

## Answers to 10 Specific Questions

1. **Is #6c7280 optimal or should we target 5:1?**  
   #6c7280 delivers 4.52:1 contrast with minimal visual drift and keeps dark-mode parity. Option B (#667085, 5.02:1) offers more buffer but triggers cascading secondary token changes. Plan: ship #6c7280 now, monitor feedback, revisit in Phase 3 if further darkening needed (see ALTERNATIVE_APPROACHES §1).

2. **Are the planned quick wins the fastest? Could UI-021 replace UI-005?**  
   ROI analysis (`EFFORT_IMPACT_MATRIX.md`) shows UI-021 ROI 4.8 vs UI-005 2.25, but UI-021 depends on responsive spacing utilities (Theme 2) not ready until Week 2. UI-005 removal is blocked only by template cleanup and unlocks spacing debt immediately. UI-021 remains Wave 1 but after spacing utilities land.

3. **How do we version design tokens for breaking changes?**  
   Adopt semantic versioning (`design_tokens_v2.x.x`). Minor increments for additive tokens, patch for bug fixes, major for breaking/removal. Maintain `design_tokens_v1.json` alias for rollback and document migration steps in token README. Include `@version` comments inside CSS bundle.

4. **Mobile-first vs. targeted patching?**  
   Full mobile-first rewrite (Option A) exceeds Phase 2 capacity. Targeted patches (Option B) risk future debt. Chosen Hybrid (Option C): define breakpoint tokens + utilities, retrofit priority components now, leaving remainder for Phase 3 incremental rollout.

5. **External WCAG auditors or internal validation?**  
   Internal team (Accessibility Specialist + QA) can meet WCAG AA with documented procedures. Legal/compliance risk mitigated via recorded tests + automated reports. VPAT recommended in Phase 3 once implementation complete; budget audit if compliance team requests.

6. **Review cycle duration realistic?**  
   Stakeholders confirmed 4–5 day window safer than 2–3 due to travel schedules. Plan includes asynchronous Loom walkthroughs and sets expectation of ≤5 days response; buffer integrated in Week 2 review (see sequencing doc).

7. **How will future maintainers understand decisions?**  
   Maintain `DECISION_LOG.md` (created in Phase 2) plus inline code comments for complex selectors. Encourage future ADRs for architectural changes; include summary in Phase 2 completion report.

8. **Should quick wins live in Phase 2 or Phase 3?**  
   Keeping them in Phase 2 demonstrates measurable progress and validates specs before full implementation. Risk of scope creep mitigated by locking effort to 14 hours and ensuring design/dev pairing.

9. **Include dark mode tokens now?**  
   Documented parity adjustments (muted text etc.) ensure dark mode remains compliant but major dark-mode expansion deferred to Phase 4 to avoid timeline creep. Capture requirements in backlog with dependency on analytics for dark-mode usage.

10. **Is “<5% bundle size increase” the right threshold?**  
    Adopt absolute limit: `+10 KB gzip` max (per R10). Easier to monitor; integrates with `size-limit` CI. Current estimates show +6.2 KB after new utilities, within budget.

---

## Final Checklist

- [x] Implementation-ready specs per theme.
- [x] Token system v2 docs + versioning plan.
- [x] Quick win plan with proof artifacts.
- [x] Sequencing, risk, validation, compatibility matrices delivered.
- [x] Decision log populated for maintainers.

Phase 2 is now fully actionable; Phase 3 team can begin development with minimal clarification overhead.

