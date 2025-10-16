# Phase 1 Deep Dive Analysis

This document expands the Phase 1 audit by exposing systemic root causes, quantifying user impact, and identifying edge cases that must be covered during remediation.

---

## Methodology Cheat Sheet

- **Frequency scale (1–5)**: 1 = rare edge page (<5% traffic), 3 = targeted flow (10–40% sessions), 5 = present on nearly every visit (>80% sessions).
- **Severity scale (1–10)**: 3 = cosmetic annoyance, 5–6 = noticeable friction, 8 = high accessibility/usability risk, 10 = critical blocker.
- **Impact score**: Frequency × Severity (max 50). Scores ≥24 demand Wave‑1 attention.

---

## Refined Clustering & Shared Root Causes

| Cluster | Issues | Refined Root Cause | Dependencies / Notes |
|---------|--------|--------------------|----------------------|
| **Accessibility Semantics & Contrast** | UI-001, UI-002, UI-003, UI-004, UI-013, UI-015, UI-031 | Visual emphasis relies on color alone; assistive tech hooks missing; reduced-motion prefs ignored. | Requires token updates (`--color-text-muted`, semantic palettes), DOM changes for status messaging, prefers-reduced-motion overrides. |
| **Spacing Scale Debt** | UI-005, UI-007, UI-008, UI-014, UI-019, UI-021, UI-023, UI-030 | Mixed 4/6/10/12px increments without baseline creates drift between sections. | Establish 4/8/12/16/24/32px scale, retrofit layout utilities, cascade into responsive theme. |
| **Navigation Information Architecture** | UI-009, UI-017, UI-018, UI-020, UI-022, UI-024, UI-025, UI-026, UI-032 | Desktop-first assumptions produce overwhelming link density and poor indicator states. | Requires breakpoint tokens + layout templates; impacts controllers, quick navigation, anchor rail. |
| **Typographic Hierarchy & Readability** | UI-006, UI-010, UI-011, UI-016, UI-028, UI-034 | Heading/label levels lack contrast and semantic cues; uppercase microcopy reduces legibility. | Needs type scale v2 (ratio + weights), semantic color pairing, style guide alignment. |
| **Interaction & Feedback Patterns** | UI-001, UI-003, UI-004, UI-026, UI-027, UI-033 | Hover-only affordances and weak states obscure system status. | Requires shared interaction tokens (opacity, focus, elevations) and ARIA patterns. |
| **Brand & Streamlit Divergence** | UI-010, UI-029 + all Streamlit theme gaps | Streamlit app bypasses design tokens, leading to visual drift. | Must export token package + CSS bridge; rely on Theme 7 specification for adoption. |

**Hidden linkage call-outs**:
- UI-002 (muted text) and UI-031 (callout contrast) both depend on a disciplined grayscale ramp—resolve together to avoid rework.
- UI-007 footer spacing, UI-023 mobile footer, and UI-030 pager alignment all fall out of the same spacing baseline debt.
- UI-018 wide navigation and UI-022 mobile grid stem from the absence of explicit max-width utilities.

---

## Dependency Graph (textual)

- **Token Layer Dependencies**
  - `color.text-muted` → UI-002, UI-007, UI-023, UI-030, UI-031, Streamlit metadata styling.
  - `spacing.md` & `spacing.lg` → UI-005, UI-007, UI-009, UI-018, UI-021, UI-023.
  - `breakpoint.mobile` & `breakpoint.tablet` → UI-020, UI-021, UI-022, UI-023, UI-024, UI-025.
- **Component-Level Dependencies**
  - Code controls template → UI-001, UI-003, UI-004, UI-005, UI-021 (markup + JS updates in lockstep).
  - Admonition partial → UI-013, UI-014, UI-015, UI-031 (shared SCSS partial; requires single refactor pass).
  - Controllers quick navigation → UI-009, UI-017, UI-018, UI-032 (needs new IA spec before CSS tweaks).
- **Experience Dependencies**
  - Accessibility fixes (UI-002/3/4/15/31) feed legal compliance risk mitigation—must precede visual polish.
  - Responsive reflow (UI-020–025) depends on spacing tokens and typographic hierarchy updates to avoid churn.

---

## Cascading Impact Table

| Change Package | Primary Issues Solved | Secondary Impacts | Additional Actions Required |
|----------------|-----------------------|-------------------|-----------------------------|
| Update grayscale tokens (`--color-text-muted`, secondary ramps) | UI-002, UI-007, UI-023, UI-030, UI-031 | Dark theme override uses same token (docs `_static/custom.css:458`) → must refresh; Streamlit and generated docs (multiple `_build` dirs) inherit tokens. | Regenerate `design_tokens_v2.*`, update dark-mode variables, add migration note for downstream teams. |
| Code controls refactor (real DOM status node, opacity defaults) | UI-001, UI-003, UI-004, UI-005, UI-021 | Requires JS update for button targeting; translation strings for status text; impacts print styles. | Document new markup snippet, add SR regression tests, ensure copy button alignment unaffected. |
| Spacing baseline utilities (8px grid) | UI-005, UI-007, UI-008, UI-014, UI-018, UI-019, UI-021, UI-023, UI-030 | Must audit `base-theme.css` legacy classes; Streamlit layout needs equivalent spacing map. | Introduce `u-stack-*` utility classes, update layout documentation, run regression at 320/768/1024 widths. |
| Responsive nav grid templates | UI-020, UI-021, UI-022, UI-023, UI-024, UI-025, UI-032 | Interacts with typography adjustments (heading sizes) and spacing tokens. | Define breakpoint tokens, update Sphinx templates, ensure no CLS (cumulative layout shift). |
| Accessibility motion/contrast hardening | UI-013, UI-015, UI-026, UI-027, UI-033 | Some animations defined in multiple files; high-contrast media queries might raise specificity conflicts. | Centralize motion tokens, add prefers-reduced-motion variants, document QA steps for Windows High Contrast Mode. |

---

## User Impact Scoring Matrix

| Issue | Frequency (1-5) | Severity (1-10) | Impact Score | Notes |
|-------|----------------|-----------------|--------------|-------|
| UI-001 | 4 | 6 | 24 | Affects ~234 code blocks; 65% of sessions interact with code samples. |
| UI-002 | 5 | 10 | 50 | Muted text appears on nearly every doc page; blocks low-vision users. |
| UI-003 | 3 | 8 | 24 | Collapsed notices appear when sections default collapsed (~40% of code blocks). |
| UI-004 | 2 | 9 | 18 | Screen reader users (~8% sessions) miss disclosure state entirely. |
| UI-005 | 3 | 6 | 18 | Visible on pages with master controls (~45% of docs by traffic). |
| UI-006 | 3 | 5 | 15 | Status badges used across component docs and changelog pages. |
| UI-007 | 4 | 6 | 24 | Footer personas present on 90% of overview pages; scan failure confuses audiences. |
| UI-008 | 3 | 4 | 12 | Hero nav cards on home and category pages (~35% views). |
| UI-009 | 3 | 7 | 21 | Mega list on controllers flows (~25% traffic) overwhelms navigation. |
| UI-010 | 3 | 5 | 15 | Controllers nav misuses semantic color; brand confusion risk. |
| UI-011 | 2 | 6 | 12 | Coverage matrix consulted weekly by QA team (~12% sessions). |
| UI-012 | 2 | 4 | 8 | Same table readability drop primarily for data reviewers. |
| UI-013 | 3 | 5 | 15 | Animated admonitions across tutorials (~40% pages) cause motion issues. |
| UI-014 | 3 | 4 | 12 | Admonition layout misalignment on tutorials (~40% pages). |
| UI-015 | 3 | 6 | 18 | Warning text misuses color; affects inline admonitions across docs (~30% pages). |
| UI-016 | 3 | 4 | 12 | Enumerated steps in tutorials (~35% pages) hard to follow. |
| UI-017 | 3 | 5 | 15 | Controllers bullet formatting (~25% traffic) reduces readability. |
| UI-018 | 3 | 7 | 21 | Wide columns hamper scanning on controllers (~25% traffic). |
| UI-019 | 3 | 4 | 12 | Overview paragraphs on many modules (~30% pages). |
| UI-020 | 4 | 8 | 32 | 40% mobile traffic sees broken titles; damages brand perception. |
| UI-021 | 4 | 6 | 24 | Mobile controls stacking hits mobile docs users (40% traffic). |
| UI-022 | 4 | 8 | 32 | Mobile nav cards on landing pages degrade key entry points. |
| UI-023 | 4 | 6 | 24 | Mobile footer metadata readability on ~60% mobile sessions. |
| UI-024 | 3 | 6 | 18 | Tablet nav grid overflow hits 18% tablet traffic. |
| UI-025 | 2 | 4 | 8 | Tablet anchor rail oversized; mid-tier frequency (~18% traffic). |
| UI-026 | 3 | 6 | 18 | Anchor state clarity affects deep readers (~45% sessions). |
| UI-027 | 3 | 4 | 12 | Back-to-top button contrast low; feature triggered on long pages (~30% sessions). |
| UI-028 | 3 | 4 | 12 | Quick reference cards used by onboarding (~20% traffic). |
| UI-029 | 2 | 3 | 6 | Icon inconsistency on quick reference (~20% traffic). |
| UI-030 | 3 | 4 | 12 | Footer pager misalignment on nearly all docs (~95% pages) but low friction. |
| UI-031 | 3 | 6 | 18 | Callout contrast low across style guide and notes (~35% pages). |
| UI-032 | 2 | 3 | 6 | Breadcrumb overflow primarily on controllers (~15% traffic). |
| UI-033 | 2 | 7 | 14 | Coverage matrix navigation roadblock for QA/PM (~12% sessions). |
| UI-034 | 3 | 4 | 12 | Hero bullet readability drop on landing (~35% sessions). |

**Prioritisation takeaway**: UI-002, UI-020, UI-022, UI-007, UI-021, UI-023 constitute the highest compound impact beyond the critical accessibility trio.

---

## Edge Case Validation Checklist

| Scenario | Impacted Issues | Validation Actions | Owner |
|----------|----------------|--------------------|-------|
| **RTL + non-Latin locales** | UI-020, UI-021, UI-022, UI-032 | Render sample Arabic & Chinese titles/labels; ensure hyphenation fallback uses `overflow-wrap` not forced breaks; verify breadcrumb truncation respects RTL. | Frontend Dev + Localization QA |
| **prefers-reduced-motion** | UI-001, UI-003, UI-013 | Emulate reduced-motion in Chrome/Safari; confirm animations and transitions disable while focus states remain visible. | Accessibility Specialist |
| **High zoom (200%) & Windows High Contrast** | UI-002, UI-003, UI-015, UI-031 | Run browser zoom + Windows HCM; capture contrast ratios with axe DevTools; ensure borders/focus outlines remain visible. | Accessibility Specialist |
| **Low-bandwidth mobile (3G throttling)** | UI-020, UI-021, UI-022, UI-023 | Use Chrome throttling; ensure nav grid and code controls load progressively and avoid content jumps. | Frontend Dev |
| **Touch + keyboard hybrid input (Surface devices)** | UI-001, UI-026 | Navigate via touch & tab; ensure focus styles appear even after touch interactions. | QA |
| **Print to PDF** | UI-003, UI-005, UI-021 | Confirm collapsed code expands for print; duplicate bars removed; controls hidden in print stylesheet. | QA |
| **Dark mode parity** | UI-002, UI-007, UI-023, UI-031 | Toggle Furo dark theme; validate new grayscale tokens keep ≥4.5:1 contrast. | UX Designer |
| **Streamlit theme adoption** | UI-010, UI-029 + Theme 7 | Apply exported tokens in Streamlit staging; ensure button, spacing, and typography tokens propagate without breaking widgets. | Frontend Dev |

---

## Next Steps

- Feed token, spacing, and responsive dependencies into Theme specifications.
- Use this matrix to drive `EFFORT_IMPACT_MATRIX.md` scoring and sequencing constraints.
- Share edge-case checklist with QA to seed validation procedures.

