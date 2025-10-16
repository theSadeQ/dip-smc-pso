# Decision Log

Records of significant choices made while enhancing the Phase 2 plan. Use ISO dates; update status if later revisited.

| ID | Date | Decision | Context | Rationale | Status | References |
|----|------|----------|---------|-----------|--------|------------|
| D-001 | 2025-10-14 | Adopt `#6c7280` for muted text (Option A) | UI-002 contrast remediation | Provides 4.52:1 contrast with minimal visual drift; quick win deliverable achievable within 2 hours. | Approved | PHASE2_PLAN_ENHANCED.md §Theme 1, ALTERNATIVE_APPROACHES.md §1 |
| D-002 | 2025-10-14 | Implement DOM-based code collapse notice | Accessibility fix for UI-003/004 | Aligns with WAI-ARIA disclosure pattern; resolves SR announcement gap. | Approved | PHASE2_PLAN_ENHANCED.md §Theme 1, ALTERNATIVE_APPROACHES.md §3 |
| D-003 | 2025-10-14 | Standardize on 8px baseline spacing utilities | Themes 2 & 3 foundation | Simplifies responsive math; shared baseline between docs and Streamlit. | Approved | PHASE2_PLAN_ENHANCED.md §Theme 2, IMPLEMENTATION_SEQUENCING_OPTIMIZED.md |
| D-004 | 2025-10-14 | Use hybrid tokenized responsive approach | Responsive backlog (UI-020–025) | Balances sustainability with effort; avoids full architectural refactor. | Approved | ALTERNATIVE_APPROACHES.md §2 |
| D-005 | 2025-10-14 | Keep quick wins inside Phase 2 timeline | Validate design direction early | Demonstrates accessibility improvements, derisks stakeholder buy-in before Phase 3. | Approved | PHASE2_PLAN_ENHANCED.md §Quick Wins |
| D-006 | 2025-10-14 | Deliver tokens as JSON + CSS custom properties | Design system distribution | Minimal tooling overhead, works across Sphinx + Streamlit; versionable. | Approved | ALTERNATIVE_APPROACHES.md §5 |
| D-007 | 2025-10-14 | Schedule bi-weekly stakeholder reviews with 4-day windows | Review cadence realism | Stakeholders requested more buffer; ensures decisions stay timely without blocking critical path. | Approved | PHASE2_PLAN_ENHANCED.md §Stakeholder Plan |
| D-008 | 2025-10-14 | Defer dark mode enhancements to Phase 4 roadmap | Scope management | Avoids scope creep; document future requirements while focusing on light-mode parity. | Approved | PHASE2_PLAN_ENHANCED.md §Future Considerations |
| D-009 | 2025-10-14 | Maintain <+10KB CSS budget (not % threshold) | Performance KPI | Absolute byte target easier to monitor; aligns with risk mitigation. | Approved | PHASE2_PLAN_ENHANCED.md §Success Metrics |

Update this log when new trade-offs arise or prior decisions are reversed.

