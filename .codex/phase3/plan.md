# Phase 3 Implementation & Theming Plan

> **📍 For strategic context, see:** [Strategic Roadmap](../ STRATEGIC_ROADMAP.md) - Complete vision for Phases 3-6, including Phase 4 recommendations and Version 2.0 milestones.

## Objectives
- Ship the approved Phase 2 remediation concepts across Sphinx documentation, Streamlit dashboards, and shared assets while keeping UX debt from Phase 1 visible.
- Close or update the 34-item Phase 1 backlog (focus on UI-002/3/4/20/22 first) and record all commits against their originating issue IDs.
- Preserve design token integrity (v2 baseline) and ensure regenerated assets/tests reflect the updated theming.

## Inputs & References
- Phase 1 component inventory (`.codex/phase1_audit/phase1_component_inventory.csv`) and issue backlog (`phase1_issue_backlog.json`).
- Phase 2 specs: `PHASE2_PLAN_ENHANCED.md`, `IMPLEMENTATION_SEQUENCING_OPTIMIZED.md`, `STREAMLIT_ALIGNMENT_SPECIFICATION.md`, `design_tokens_v2` artifacts, `VALIDATION_PROCEDURES.md`.
- Risk + decision trackers: `DECISION_LOG.md`, `RISK_ASSESSMENT_DETAILED.md`, `EFFORT_IMPACT_MATRIX.md`.
- **Strategic Roadmap**: `../STRATEGIC_ROADMAP.md` - Long-term vision through Phase 6.

## Execution Waves
1. **Wave 0 - Kickoff & Environment Hardening (Days 0-1)**
   - Confirm contributors, tooling, and lint/test coverage (Sphinx build, Streamlit preview, Percy/Lighthouse, axe).
   - Snapshot current UI baselines for comparison (screenshots plus token checksums).
   - Align backlog grooming rules: link every task to `UI-###`, capture acceptance tests per `VALIDATION_PROCEDURES.md`.
   - Deliverable evidence stored in `phase3/` (see `changelog.md`, `baselines/`, and validation directories).

2. **Wave 1 - Foundations & Accessibility (Days 1-5)**
   - Merge token updates from Phase 2 (`--color-text-muted`, spacing scale, typography scale) into docs plus shared CSS.
   - Implement UI-002/003/004/001 quick wins; refactor collapsed code controls to new DOM structure with live regions.
   - Apply reduced-motion overrides, dark-mode parity tokens, and focus-visible treatments (UI-013, UI-026, UI-027).
   - Update Sphinx templates and partials for accessibility adjustments; run axe plus keyboard regression scripts.
   - Status: Wave 1 complete (axe + Lighthouse + NVDA/JAWS); Wave 2 spacing/responsive work next.

3. **Wave 2 - Spacing, Responsive Layout & Typography (Days 5-10)**
   - Roll out spacing utilities to navigation cards, hero, project information lists (UI-005/007/008/009).
   - Execute responsive utilities for 320px and 768px breakpoints (UI-020/022/023/024/025) using Phase 2 breakpoints.
   - Recalibrate headings/body typography per Theme 4 specs (UI-006/011/028/032/034).
   - Verify responsive behaviour in documentation plus testing surfaces; regenerate HTML diffs and update screenshots.
   - Resolve Lighthouse-noted sidebar navigation contrast issues as part of spacing/typography tune-up.

4. **Wave 3 - Interaction, Streamlit Parity & Asset Refresh (Days 10-15)** ✅ **COMPLETE (2025-10-16)**
   - ✅ Finish interaction polish: anchor rail state (UI-026), back-to-top button (UI-027), coverage filters (UI-033) and code block controls
   - ✅ Integrate Streamlit theme wrapper using `STREAMLIT_ALIGNMENT_SPECIFICATION.md`; align buttons, metrics, download flows, tabs
   - ✅ Replace mixed iconography (UI-029) and regenerate SVG/PNG assets; ensure metadata/test artifacts (coverage matrix, quick reference) rebuilt after CSS changes
   - ✅ Execute browser compatibility suite and finalize changelog entries tied to issue IDs
   - **Validation Results:** 4/4 criteria PASS (Visual: 0.0% diff, Performance: 1.07KB gzipped, Tokens: 18/18, Accessibility: 0 theme-induced violations)
   - **Evidence:** `.codex/phase3/WAVE3_FINAL_COMPLETION.md`, `.codex/phase3/validation/streamlit/wave3/VALIDATION_SUMMARY.md`

5. **Wave 4 - Consolidation & Phase 4 Prep (Days 15-18)**
   - Finalize documentation updates (Sphinx theme notes, Streamlit theme README, token changelog).
   - Capture before/after screenshot sets and contrast reports for Phase 4 verification.
   - Update `.codex/README.md`, `COMPLETION_SUMMARY.md`, and backlog states to reflect resolved issues plus residual risks.

## Backlog Translation
| Issue Cluster | Phase 1 IDs | Phase 3 Tasks | Deliverables |
|---------------|-------------|---------------|--------------|
| Accessibility & Contrast | UI-002, UI-003, UI-004, UI-013, UI-031 | Token updates, status notice component refactor, reduced-motion overrides | Updated CSS, ARIA patterns, axe reports |
| Spacing & Layout | UI-005, UI-007, UI-008, UI-009, UI-030 | Apply spacing utilities, consolidate control bars, adjust footer pager spacing | Utility CSS, layout snapshots |
| Typography | UI-006, UI-010, UI-011, UI-028, UI-032, UI-034 | Apply type scale, update link styles, adjust table typography | Type scale docs, before/after diffs |
| Responsiveness | UI-020, UI-021, UI-022, UI-023, UI-024, UI-025 | Implement breakpoint tokens, update navigation grids, optimize hero headlines | Mobile/tablet screenshots, responsive QA logs |
| Interaction & Feedback | UI-001, UI-026, UI-027, UI-033 | Enhance affordances, focus states, anchor navigation feedback | Interaction spec updates, GIF captures |
| Branding & Assets | UI-010, UI-029 | Standardize color usage, replace inconsistent icons/assets | Asset pack v3, brand usage notes |
| Streamlit Parity | UI-015, UI-017, UI-018, UI-019 | Apply token-driven theme, align widgets, sync navigation/metrics styling | Streamlit theme module, validation run |

## Working Practices
- **Branching & Changelog:** Create `phase3/*` branches per workstream, update `./changelog.md` with entries `YYYY-MM-DD | UI-### | Summary | Owner | Evidence`.
- **Definition of Done:** Implementation merged, axe and Lighthouse checks passed, responsive screenshots updated, backlog item status moved to Resolved, changelog entry added.
- **Testing:** Follow `VALIDATION_PROCEDURES.md` for axe, Lighthouse, Percy, keyboard path, and responsive matrix; rerun Streamlit smoke tests after each theme iteration.
- **Documentation:** Keep token docs (`DESIGN_SYSTEM.md`) in sync; add inline comments where selectors are sensitive to Streamlit DOM changes.
- **Stakeholder Touchpoints:** Weekly review using annotated mockups or live demos; capture decisions in `DECISION_LOG.md` within 24 hours.

## Risk & Mitigation Highlights
- **Dark Mode Regression (R1):** Pair accessibility QA with every color change; run dark theme snapshot diff nightly.
- **Timeline Pressure from Reviews (R4):** Maintain at least 48 hour buffer before stakeholder demos; prepare async Loom walkthroughs.
- **Streamlit DOM Drift:** Encapsulate overrides in `[data-theme="dip-docs"]`, keep `ENABLE_DIP_THEME` toggle documented, add automated smoke test to flag missing selectors.

## Exit Criteria for Phase 3
- 100 percent of Critical/High issues from Phase 1 resolved or re-specified with justification.
- Streamlit and Sphinx share token source plus style parity with documented override strategy.
- Updated artifacts (screenshots, metadata.json, regenerated tables) stored alongside revised documentation.
- Phase 4 regression checklist primed with new baselines and outstanding medium/low issues queued.

