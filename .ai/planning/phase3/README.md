# Phase 3 Plan README

## Purpose
This README explains how to execute and maintain the implementation plan stored in `./plan.md`. Phase 3 turns the Phase 2 remediation specs into production-ready updates across documentation and Streamlit while retiring the Phase 1 backlog.

**Wave Status:** Wave 0 completed 2025-10-14 (`phase3-wave0-complete`). Wave 1 tagged (`phase3-wave1-complete`); automated axe + baseline updates are done, Lighthouse/NVDA manual audits remain before Wave 2 kickoff.

## Folder Layout
- `plan.md` - Wave-by-wave execution plan with backlog translation and exit criteria.
- `changelog.md` - Day-to-day implementation log that links commits to Phase 1 issue IDs.
- `dependency_graph.md` - Sequencing map that highlights blockers and parallel workstreams.
- `team_roster.md` - Role assignments, capacity planning, and communication cadence for the team.
- `artifact_verification.md` - Checklist for confirming Phase 2 references and baseline assets.
- `rollback_procedures.md` - Playbook for halting or reversing changes when exit criteria fail.
- `completion_summary.md` - Final report template for Phase 3 delivery outcomes.
- `baselines/` - Storage for Wave 0 screenshots and automation assets (see `baselines/tokens/` for checksums and diffs).
- `validation/` - Folder for accessibility, Lighthouse, Percy, and manual QA reports.

## Using the Plan
1. Review the "Execution Waves" section to stage work in the suggested order (Kickoff, Foundations, Responsive, Interaction/Streamlit, Consolidation).
2. Translate each wave into backlog tickets that reference the originating Phase 1 issue IDs and the supporting Phase 2 specs listed under "Inputs & References".
3. Log all progress in `./changelog.md` using the `YYYY-MM-DD | UI-### | Summary | Owner | Evidence` format and capture test artifacts per `VALIDATION_PROCEDURES.md`.
4. Keep `DESIGN_SYSTEM.md`, Streamlit theme files, and regenerated assets aligned with the token updates called out in Wave 1.

## Coordination & Reviews
- Schedule weekly demos or async walkthroughs to satisfy stakeholder checkpoints from Phase 2 (`DECISION_LOG.md`).
- Pair QA with accessibility for each wave: run axe, Lighthouse, responsive matrix, and keyboard paths before closing tasks.
- Document risk changes in `RISK_ASSESSMENT_DETAILED.md` and surface blockers during the daily stand-up noted in the Phase 2 sequencing doc.

## Exit Checklist Snapshot
- Critical and High issues from Phase 1 (UI-002/3/4/20/22) closed with evidence.
- Sphinx and Streamlit share the design tokens v2 baseline and ship aligned theming.
- Updated screenshots, metadata, and docs uploaded to `.codex` ahead of Phase 4 verification work.

## Related Artifacts
- `.codex/phase1_audit/` for original findings and tokens.
- `.codex/phase2_audit/` for specs, sequencing, and validation procedures.
- `.codex/phase3/plan.md` (this plan) and `.codex/phase3/changelog.md` for ongoing status tracking.




