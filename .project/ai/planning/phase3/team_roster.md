# Phase 3 Team Roster & Capacity Allocation

**Project:** DIP SMC PSO Documentation - Phase 3 Implementation
**Duration:** 22 days (18 base + 4 contingency buffer)
**Start Date:** TBD (Wave 0 kickoff)
**Status:** Team structure defined, awaiting member assignment

---

## Team Structure

| Role | Primary Owner | Backup | Hours/Week | Allocation % | Waves |
|------|---------------|--------|------------|--------------|-------|
| **Frontend Developer** | TBD | TBD | 40 hrs | 100% | All Waves |
| **Accessibility Specialist** | TBD | TBD | 20 hrs | 50% | Waves 0, 1, 2, 4 |
| **UX Designer** | TBD | TBD | 16 hrs | 40% | Waves 0, 1, 2, 3 |
| **QA Engineer** | TBD | TBD | 24 hrs | 60% | All Waves |
| **Project Manager** | TBD | TBD | 8 hrs | 20% | All Waves |
| **DevOps/Tooling** | TBD | TBD | 4 hrs | 10% | Wave 0 only |

**Total Team FTE:** ~2.8 FTE across 22 days

---

## Role Responsibilities

### Frontend Developer
**Primary:** Token implementation, CSS updates, Sphinx template modifications, Streamlit theme integration

**Waves 0-4 Tasks:**
- Merge design_tokens_v2.json into Sphinx CSS
- Refactor code collapse controls (UI-001/003/004)
- Implement spacing utilities (UI-005/007/008/009)
- Apply responsive breakpoints (UI-020/021/022/023/024/025)
- Streamlit theme wrapper development
- Icon/asset replacement (UI-029)
- Browser compatibility testing

**Skills Required:**
- CSS custom properties & utility frameworks
- Sphinx templating (Jinja2)
- Streamlit theming & DOM inspection
- Responsive design (mobile-first)
- Git branch management

**Deliverables:**
- Updated `docs/_static/custom.css` (all 7 themes)
- Streamlit theme module (`streamlit_theme.py`)
- Updated Sphinx templates for ARIA compliance
- Asset pack v3 (SVG/PNG regeneration)

---

### Accessibility Specialist
**Primary:** WCAG AA compliance, screen reader testing, contrast validation, ARIA patterns

**Wave 0 Tasks:**
- Run baseline Lighthouse & axe audits
- Document current violations (Critical/Serious)
- Validate design_tokens_v2.json contrast ratios

**Wave 1 Tasks:**
- UI-002 muted text contrast validation (4.52:1)
- UI-003 collapsed notice contrast fix verification
- UI-004 ARIA live region testing (NVDA + JAWS)
- UI-013 reduced-motion override validation
- UI-015 warning copy accessibility check

**Wave 2 & 4 Tasks:**
- Responsive typography accessibility (text zoom 200%)
- Final WCAG AA certification sweep
- Generate compliance report for stakeholders

**Skills Required:**
- WCAG 2.1 AA/AAA expertise
- Screen reader testing (NVDA, JAWS, VoiceOver)
- axe-core, Lighthouse CLI proficiency
- Color contrast analysis (WebAIM, Stark)

**Deliverables:**
- Baseline accessibility report (Wave 0)
- Wave 1 exit accessibility audit (>=95 Lighthouse)
- Final WCAG AA compliance certificate (Wave 4)

---

### UX Designer
**Primary:** Visual design, type scale, spacing system, before/after validation

**Wave 0-1 Tasks:**
- Validate token values align with design intent
- Create typography scale specimen page
- Review collapsed code notice visual treatment (UI-003)
- Approve spacing utilities grid (4/8/12/16/24/32/48px)

**Wave 2 Tasks:**
- Responsive layout approval (320/768/1024px)
- Mobile H1 word-break fix validation (UI-020)
- Visual navigation grid spacing review (UI-022/024)
- Coverage matrix typography validation (UI-011)

**Wave 3 Tasks:**
- Iconography replacement approval (UI-029)
- Back-to-top FAB visual polish (UI-027)
- Streamlit theme parity review

**Wave 4 Tasks:**
- Before/after screenshot review for all 34 issues
- Final visual QA across all themes
- Brand compliance validation

**Skills Required:**
- Design systems & token management
- Figma or equivalent design tools
- Responsive design principles
- Brand guidelines enforcement

**Deliverables:**
- Type scale documentation
- Approved spacing utilities
- Before/after visual diff reports (34 issues)
- Brand usage notes update

---

### QA Engineer
**Primary:** Test execution, regression validation, browser compatibility, Percy snapshots

**Wave 0 Tasks:**
- Set up Lighthouse CI integration
- Configure Percy baselines
- Run baseline screenshots (`.codex/capture_baseline_screenshots.py`)
- Validate tooling configs (Lighthouse, axe, Percy)

**All Waves Tasks:**
- Execute VALIDATION_PROCEDURES.md checklists per theme
- Capture before/after Percy diffs
- Cross-browser testing (Chrome, Firefox, Safari, Edge)
- Responsive matrix validation (iPhone 13, Pixel 5, iPad Mini)
- Keyboard navigation testing
- Lighthouse performance monitoring (CLS, LCP)

**Wave 4 Tasks:**
- Final regression sweep (all pages, all browsers)
- Validate all 34 issues resolved with evidence
- Generate QA sign-off report

**Skills Required:**
- Playwright or Puppeteer proficiency
- BrowserStack or similar device testing
- Percy visual regression workflows
- Lighthouse & axe CLI usage
- Manual accessibility testing

**Deliverables:**
- Percy baseline snapshots (Wave 0)
- Wave exit validation reports (Waves 1-4)
- Browser compatibility matrix
- Final QA certification

---

### Project Manager
**Primary:** Timeline tracking, risk mitigation, stakeholder coordination, changelog maintenance

**Ongoing Tasks:**
- Update `./changelog.md` daily
- Track Wave progress against timeline
- Coordinate weekly stakeholder demos
- Manage risk register (RISK_ASSESSMENT_DETAILED.md)
- Decision log updates (DECISION_LOG.md)
- Buffer allocation (22-day timeline management)

**Wave Exit Reviews:**
- Validate exit criteria met (accessibility scores, issue resolution)
- Approve/reject Wave progression
- Trigger rollback if exit criteria fail
- Capture lessons learned

**Skills Required:**
- Agile/Kanban project management
- Risk mitigation frameworks
- Stakeholder communication (async Loom demos)
- Documentation & changelog discipline

**Deliverables:**
- Phase 3 completion report
- Updated RISK_ASSESSMENT (Wave 4)
- Stakeholder demo recordings (Waves 1-4)
- Lessons learned document

---

### DevOps/Tooling (Wave 0 Only)
**Primary:** Lighthouse CI setup, GitHub Actions integration, Percy environment config

**Wave 0 Tasks:**
- Install & configure Lighthouse CI
- Set up axe-core automation
- Configure Percy snapshots pipeline
- Create GitHub Actions workflow (optional)
- Validate tooling smoke tests

**Skills Required:**
- Node.js & npm package management
- GitHub Actions or CI/CD pipelines
- Lighthouse & axe-core CLI
- Percy configuration

**Deliverables:**
- Working Lighthouse CI (local or GitHub Actions)
- axe-core automation script
- Percy baseline captured
- Tooling documentation

---

## Capacity Allocation by Wave

| Wave | Duration | FED | A11y | UX | QA | PM | DevOps | Total hrs/week |
|------|----------|-----|------|----| ---|----| -------|----------------|
| Wave 0 | 1 day | 8 | 8 | 4 | 8 | 2 | 4 | 34 hrs |
| Wave 1 | 4 days | 40 | 20 | 12 | 24 | 8 | - | 104 hrs |
| Wave 2 | 5 days | 40 | 12 | 16 | 24 | 8 | - | 100 hrs |
| Wave 3 | 5 days | 40 | 4 | 16 | 24 | 8 | - | 92 hrs |
| Wave 4 | 3 days | 24 | 16 | 12 | 24 | 8 | - | 84 hrs |
| **Buffer** | 4 days | 0 | 0 | 0 | 16 | 4 | - | 20 hrs |
| **Total** | **22 days** | **152** | **60** | **60** | **120** | **38** | **4** | **434 hrs** |

**Estimated Cost:** ~$43,400 @ $100/hr blended rate (adjust for actual rates)

---

## Communication Plan

| Cadence | Meeting | Attendees | Duration | Purpose |
|---------|---------|-----------|----------|---------|
| **Daily** | Stand-up | FED, A11y, QA, PM | 15 min | Progress, blockers, daily priorities |
| **Weekly** | Stakeholder Demo | All + Stakeholders | 30 min | Show progress, gather feedback (can be async Loom) |
| **Per Wave** | Exit Review | All | 45 min | Validate exit criteria, approve Wave progression |
| **Ad-hoc** | Risk Triage | PM + affected role | 15 min | Address blockers, trigger rollback if needed |

**Communication Tools:**
- Slack: Daily updates + async questions
- Zoom: Weekly demos (or Loom for async)
- GitHub: Issue linking (UI-###), PR reviews
- Changelog: `./changelog.md` (single source of truth)

---

## Escalation Path

| Issue Type | First Contact | Escalation (if unresolved in 4 hrs) |
|------------|---------------|-------------------------------------|
| Technical blocker | Frontend Developer | DevOps or external consultant |
| Accessibility violation | Accessibility Specialist | UX Designer + external WCAG auditor |
| Timeline slippage | Project Manager | Stakeholder + adjust buffer allocation |
| Scope creep | Project Manager | Stakeholder approval required |
| Tooling failure | DevOps (Wave 0 only) | Project Manager + manual testing fallback |
| Stakeholder feedback conflict | UX Designer | Project Manager + DECISION_LOG entry |

---

## Backup Plan (If Key Person Unavailable)

| Role | Primary Backup | Secondary Fallback |
|------|----------------|--------------------|
| Frontend Developer | **CRITICAL** - External contractor or delay | - |
| Accessibility Specialist | QA Engineer (basic checks only) | External WCAG consultant |
| UX Designer | Project Manager (documented approvals) | Stakeholder visual review |
| QA Engineer | Frontend Developer (manual testing) | Extended buffer window |
| Project Manager | UX Designer (changelog + tracking) | - |

**Note:** Frontend Developer is single point of failure (SPOF). If unavailable >2 days, trigger 48-hour pause + stakeholder escalation.

---

## Onboarding Checklist (New Team Members)

- [ ] Read `./README.md` (execution framework)
- [ ] Review Phase 1 backlog: `phase1_issue_backlog.json` (34 issues)
- [ ] Review Phase 2 specs: `PHASE2_PLAN_ENHANCED.md` (7 themes)
- [ ] Study design tokens: `design_tokens_v2.json` (token system v2)
- [ ] Read validation procedures: `VALIDATION_PROCEDURES.md` (testing checklists)
- [ ] Access tooling: Lighthouse (.lighthouse/), axe (.axe/), Percy (package.json)
- [ ] Clone repo + set up local Sphinx server (http://localhost:9000)
- [ ] Run baseline screenshot capture script (Wave 0 evidence)
- [ ] Attend Wave 0 kickoff + assigned Wave orientation

---

## Success Metrics (Team Performance)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **On-time Wave exits** | 100% (all 4 Waves) | Actual vs planned dates |
| **Buffer utilization** | <=50% (2 of 4 days) | Days used from contingency |
| **Critical issue resolution rate** | 100% (5/5 Critical/High issues) | Resolved vs total |
| **Accessibility score** | >=95 Lighthouse, 0 critical axe violations | Automated reports |
| **Team velocity** | >=90% planned hours utilized | Actual hours / planned hours |
| **Stakeholder satisfaction** | >=4/5 rating per Wave demo | Feedback survey |

---

## Notes & Open Questions

| Date | Question | Answer | Owner |
|------|----------|--------|-------|
| 2025-10-14 | Who fills FED role? | **TBD** - Assign before Wave 0 | PM |
| 2025-10-14 | Can we get external A11y consultant if needed? | **TBD** - Budget approval required | PM |
| 2025-10-14 | Streamlit theme complexity - need extra dev time? | **Monitor Wave 3** - May extend buffer | FED |

---

**Last Updated:** 2025-10-14 (Wave 0 setup)
**Next Review:** Wave 0 kickoff (team assignments finalized)
**Maintained By:** Project Manager

