# Optimized Implementation Sequencing

Three-week execution plan incorporating dependency mapping, resource loading, and buffers. Durations expressed in working days (D). Quick wins embedded to prove value without jeopardizing system work.

---

## High-Level Timeline (Gantt-style Outline)

```
Week 1   |D1|D2|D3|D4|D5|
Theme 1 Accessibility  █████████
Theme 6 Color Tokens    █████
Theme 2 Spacing System     ███████
Design Tokens v2 JSON/CSS ███
Stakeholder Sync #1        ▼

Week 2   |D6|D7|D8|D9|D10|
Theme 4 Typography        ██████
Theme 3 Responsive             ███████
Quick Wins Dev                 ███
Mockups Wave 1           ███████
Stakeholder Sync #2             ▼

Week 3   |D11|D12|D13|D14|D15|
Theme 5 Interaction        ████
Theme 7 Streamlit               ██████
Risk Mitigation & QA      █████
Roadmap + Documentation        █████
Final Review & Handoff             ▼
```

Legend: █ = active work, ▼ = milestone reviews.

---

## Critical Path

1. **Token System v2 (D1–D3)** → unlocks spacing, typography, responsive, Streamlit work.
2. **Accessibility & Color Fixes (D1–D4)** → necessary before mockups & QA sign-off.
3. **Responsive Utilities (D6–D10)** → dependent on spacing tokens; required before Streamlit alignment.
4. **Mockups & Review Cycle (D8–D13)** → stakeholders must approve before final roadmap.
5. **Documentation + Validation Pack (D12–D15)** → final handoff gating Phase 3 start.

Critical path buffer: 1.5 days reserved end of Week 3 (D14 afternoon–D15 morning) for unforeseen rework.

---

## Detailed Sequencing

| Day(s) | Workstream | Key Activities | Dependencies | Owner(s) | Deliverables |
|--------|------------|----------------|--------------|----------|--------------|
| D1 | Kickoff | Align on success metrics, confirm resource availability, baseline analytics exports. | None | PM + Leads | Meeting notes, KPI baseline. |
| D1–D3 | Theme 1 & 6 | Token updates, contrast fixes, prefers-reduced-motion patterns, accessibility spec authoring. | Phase 1 audit | UX + A11y | Updated token files, before/after CSS, validation plan. |
| D2–D5 | Theme 2 | Define spacing utilities, retrofit key components, document usage guidelines. | Token draft | UX + FED | `spacing-scale.md`, utility CSS, screenshots. |
| D3 | Stakeholder Sync #1 | Present token/spacing concepts for early feedback. | Work-in-progress specs | UX Lead | Recorded review, action items. |
| D4–D5 | QA Prep | Build validation scripts, set up Lighthouse + axe baselines. | Theme 1/2 drafts | QA | Test plans (VALIDATION_PROCEDURES.md). |
| D6–D8 | Theme 4 | Typography hierarchy recalibration, heading/label updates. | Tokens approved | UX | Type scale matrices, CSS updates. |
| D6–D10 | Theme 3 | Responsive utilities & breakpoints, implement on nav, footer, hero, code controls. | Spacing utilities | FED | Responsive CSS, annotated mockups. |
| D7–D9 | Quick Wins Build | Implement UI-002, UI-001/4, UI-005 fixes in staging. | Accessibility spec | FED | Live staging demo, regression results. |
| D8–D9 | Mockups Wave 1 | Produce annotated visuals for Themes 1–4. | Specs matured | Visual/UX | 10 annotated mockups. |
| D10 | Stakeholder Sync #2 | Showcase quick wins, gather feedback on mockups. | Completed quick wins | UX Lead | Demo recording, sign-off email. |
| D11–D12 | Theme 5 | Define interaction states, update anchor rail, FAB, coverage filters. | Prior themes done | UX + FED | Interaction spec, prototype snippet. |
| D11–D13 | Theme 7 | Streamlit theme tokens, CSS injection, alignment spec authoring. | Tokens finalised | FED | `STREAMLIT_ALIGNMENT_SPECIFICATION.md`, config files. |
| D12–D13 | Risk Mitigation | Execute targeted tests (screen reader, mobile), update risk log. | Themes 1–5 built | QA + A11y | Risk log updates, test evidence. |
| D13 | Final Review Prep | Assemble PHASE2_PLAN_ENHANCED draft, cross-check success criteria. | All specs produced | UX | Draft deliverables. |
| D14 | Week 3 Review | Present final documentation, incorporate stakeholder feedback. | Completed docs | UX + PM | Action list for final polish. |
| D14–D15 | Documentation & Handoff | Finalize all markdown deliverables, publish decision log, prepare Phase 3 onboarding deck. | Feedback resolved | UX | Complete `.codex/phase2_audit` package + roadmap. |

---

## Parallelisation Opportunities

- **Accessibility (Theme 1)** and **Color (Theme 6)** run concurrently with **Spacing (Theme 2)** — different owners, minimal dependencies.
- **Typography (Theme 4)** overlaps with final day of **Spacing (Theme 2)** once tokens locked.
- **Quick wins** share code control template work with Theme 3; pair programming reduces duplicated effort.
- **Streamlit alignment** overlaps with Week 3 QA, provided token exports are frozen by end of Week 2.

---

## Governance & Checkpoints

- **Daily 15-minute stand-up** focusing on blockers tied to critical path.
- **Twice-weekly risk review** referencing `RISK_ASSESSMENT_DETAILED.md`.
- **Stakeholder approvals** captured in `DECISION_LOG.md` (target ≤24h acknowledgement).
- **Definition of Done per theme**: implementation-ready CSS, before/after snippet, validation steps, mockups where applicable.

---

## Buffer Strategy

- 0.5 day reserved in Week 2 for rework from Sync #2.
- 1 day reserved in Week 3 for documentation polish and final QA retests.
- Capacity contingency: design lead retains 20% slack each week for emergent dependencies or stakeholder escalations.

