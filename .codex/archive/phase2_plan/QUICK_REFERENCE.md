# Phase 2 Quick Reference - TL;DR

> **Purpose**: Rapid orientation cheat sheet for Phase 2 enhancement mission
>
> **For**: Quick lookups during deep analysis work
>
> **Read First**: `README.md` for full context

---

## Phase 1 Stats

| Metric | Value | Details |
|--------|-------|---------|
| **Components Catalogued** | 62 | Navigation (9), Typography (18), Layout (15), Interactive (10), Responsive (10) |
| **Issues Logged** | 34 | 1 Critical, 4 High, 16 Medium, 13 Low |
| **Category Distribution** | 7 | Spacing (7), Typography (7), Responsiveness (7), Color (5), Interactivity (3), Accessibility (3), Branding (2) |
| **Evidence Set** | 40+ | Screenshots referenced, 15 CSS/JS source locations |
| **Documentation Pages** | ~795 | Sphinx HTML pages affected by issues |
| **Code Blocks** | 234 | Across API guides, tutorials, workflows |

---

## Top 5 Critical/High Issues

| ID | Severity | Description | Impact | Location |
|----|----------|-------------|--------|----------|
| **UI-002** | CRITICAL | Muted text #9ca3af = 2.54:1 contrast (WCAG fail) | 200+ pages, low-vision users can't read | `custom.css:55` |
| **UI-003** | High | Collapsed code notice 3:1 contrast (below 4.5:1) | Status text illegible | `code-collapse.css:178-182` |
| **UI-004** | High | Screen readers miss ::after pseudo-element | SR users never know content hidden | `code-collapse.css:177-183` |
| **UI-020** | High | Mobile H1 breaks "Documenta-tion" at 320px | 40% of users (mobile) see brand break | `test_6_1_mobile_320px.png` |
| **UI-022** | High | Visual nav 2-column on 320px, 4-line labels | Mobile navigation unusable | `test_6_1_mobile_320px.png` |

---

## Phase 2 Themes (7 Workstreams)

| # | Theme | Issues | Priority | Root Cause | Dependencies |
|---|-------|--------|----------|------------|--------------|
| **1** | Accessibility Critical | 4 | IMMEDIATE | Insufficient WCAG compliance | None - start first |
| **2** | Spacing System | 7 | Foundation | No unified spacing scale, magic numbers | None - parallel with #1 |
| **3** | Responsive Mobile-First | 7 | High | Desktop-first CSS approach | Depends on Theme 2 (spacing tokens) |
| **4** | Typography Hierarchy | 7 | Medium | Weak differentiation | Independent - can parallel with #2 |
| **5** | Interaction Patterns | 3 | Medium | Low-visibility affordances | Depends on Themes 1+2+6 |
| **6** | Color System Compliance | 5 | Foundation | Semantic color misuse | None - parallel with #1+2 |
| **7** | Streamlit Alignment | Matrix | Low | No shared design system | Depends on all others |

---

## Three-Wave Implementation

### Wave 1: Foundations (Parallel)
- **Themes**: Accessibility (1), Color (6), Spacing (2)
- **Duration**: Week 1 (Days 1-5)
- **Rationale**: No dependencies, can work in parallel
- **Deliverables**: Updated tokens, WCAG fixes, 8px baseline grid

### Wave 2: Typography & Responsive (Sequential)
- **Themes**: Typography (4), Responsive (3)
- **Duration**: Week 2 (Days 6-10)
- **Rationale**: Both depend on Wave 1 spacing tokens
- **Deliverables**: Type scale, mobile/tablet/desktop responsive

### Wave 3: Interactions & Streamlit (Final)
- **Themes**: Interaction (5), Streamlit (7)
- **Duration**: Week 3 (Days 11-15)
- **Rationale**: Requires stable design system from Waves 1-2
- **Deliverables**: Enhanced interactions, cross-surface consistency

---

## Quick Wins (14 hours, resolves 4 issues)

| # | Issue | Effort | Impact | Change |
|---|-------|--------|--------|--------|
| **1** | UI-002 (Critical) | 2hr | Resolves Critical WCAG fail | Update `--color-text-muted: #6c7280` in `custom.css:55` |
| **2** | UI-001 + UI-004 (Med+High) | 5hr | Improves accessibility | Button opacity 0.3→0.6 + aria-expanded + DOM element |
| **3** | UI-005 (Medium) | 7hr | Recovers 48px space | Remove duplicate control bar (template change) |

**Total**: 14 hours resolves 1C + 1H + 2M = proof of concept

---

## Timeline (3 Weeks)

| Week | Days | Focus | Milestone |
|------|------|-------|-----------|
| **1** | 1-5 | Foundation | Token system + 7 theme specs complete |
| **2** | 6-10 | Visualization + Proof | Mockups + quick wins live on staging |
| **3** | 11-15 | Validation + Roadmap | Stakeholder approval + Phase 3 ready |

**Critical Path**: Theme specs → Mockups → Stakeholder validation → Roadmap

---

## Resources (110-150 hours)

| Role | Hours | Responsibilities |
|------|-------|------------------|
| **UX Designer (Lead)** | 60-80 | Token system, specs (7), mockups, stakeholder comms |
| **Frontend Developer** | 20-30 | Quick wins (14hr), feasibility review, validation tooling |
| **Accessibility Specialist** | 10-15 | WCAG validation, screen reader testing, contrast checks |
| **Stakeholder/Owner** | 15-20 | Review cycles, brand verification, approvals |
| **Optional: Visual Designer** | 10-15 | Polish mockups, templates |
| **Optional: Tech Writer** | 5-10 | Spec clarity, documentation standards |

**Peak Load**: Week 2 (mockups + quick wins)

---

## Key Files (Where to Find Things)

### Phase 1 Input (READ THESE)
```
.codex/phase1_audit/
├── PHASE1_COMPLETION_REPORT.md     # Executive summary - start here
├── phase1_issue_backlog.md         # All 34 issues detailed
├── phase1_component_inventory.csv  # 62 components
├── DESIGN_SYSTEM.md                # Current design tokens
└── phase1_consistency_matrix.md    # Sphinx vs Streamlit gaps
```

### Existing Code (INSPECT THESE)
```
docs/_static/
├── custom.css                      # ⚠️ CRITICAL - Main styles
├── code-collapse.css               # ⚠️ CRITICAL - Interactive features
└── css-themes/base-theme.css       # Theme foundation

streamlit_app.py                    # Streamlit app (Theme 7)
```

### Phase 2 Output (CREATE HERE)
```
.codex/phase2_audit/
├── PHASE2_PLAN_ENHANCED.md              # PRIMARY deliverable
├── PHASE1_DEEP_DIVE_ANALYSIS.md         # Enhanced issue analysis
├── ALTERNATIVE_APPROACHES.md            # Trade-off comparisons
├── RISK_ASSESSMENT_DETAILED.md          # Comprehensive risks
├── IMPLEMENTATION_SEQUENCING_OPTIMIZED.md  # Gantt + critical path
├── STREAMLIT_ALIGNMENT_SPECIFICATION.md # Technical spec
├── DECISION_LOG.md                      # Why decisions made
├── EFFORT_IMPACT_MATRIX.md              # Issues scored
├── BROWSER_COMPATIBILITY_MATRIX.md      # CSS support
└── VALIDATION_PROCEDURES.md             # Testing guide
```

---

## Success Criteria Checklist

### Quantitative (All must pass)
- [ ] All 34 issues have remediation concepts
- [ ] 100% of Critical + High (5 issues) have implementation-ready specs
- [ ] Design token system covers 15+ categories
- [ ] Minimum 15 annotated mockups created
- [ ] All colors pass WCAG AA (4.5:1 normal, 3:1 large)
- [ ] Quick wins show measurable improvement
- [ ] Stakeholder sign-off received

### Qualitative (All must pass)
- [ ] Design decisions traceable to Phase 1 issues
- [ ] Material specs have zero ambiguity
- [ ] Mockups clearly show problem → solution
- [ ] Brand consistency maintained (#0b2763 preserved)
- [ ] Token system extensible
- [ ] Root causes addressed (not symptoms)
- [ ] Cross-surface consistency achievable

### Deliverables (All must be created)
- [ ] design_tokens_v2.{json, css, md}
- [ ] 7 theme spec documents
- [ ] 15+ annotated mockups
- [ ] QUICK_WINS_REPORT.md
- [ ] IMPLEMENTATION_ROADMAP.md
- [ ] PHASE2_COMPLETION_REPORT.md

**Gate**: No Phase 3 until all ✓

---

## Enhancement Mission (6 Tasks)

| # | Task | Output | Time |
|---|------|--------|------|
| **1** | Enhanced Issue Analysis | PHASE1_DEEP_DIVE_ANALYSIS.md | 1hr |
| **2** | Material Spec Deep Dive | Enhanced theme docs (7 files) | 2hr |
| **3** | Alternative Approaches | ALTERNATIVE_APPROACHES.md | 1hr |
| **4** | Enhanced Risk Assessment | RISK_ASSESSMENT_DETAILED.md | 1hr |
| **5** | Sequencing Optimization | IMPLEMENTATION_SEQUENCING_OPTIMIZED.md | 30min |
| **6** | Streamlit Deep Dive | STREAMLIT_ALIGNMENT_SPECIFICATION.md | 1hr |

**Plus**: Answer 10 specific questions (30min)

**Total**: 6-7 hours

---

## Ten Questions (Must Answer)

1. UI-002 muted text: Is #6c7280 optimal or target 5:1 for buffer?
2. Quick wins priority: Are these 3 fastest? Effort/impact matrix?
3. Token versioning: How to version for breaking changes?
4. Mobile vs desktop-first: Refactor all CSS or patch?
5. External WCAG audit: Hire auditors ($2-5k) or internal?
6. Stakeholder timing: 2-3 days realistic or need 5-day windows?
7. Decision docs: ADRs? Inline CSS comments? DECISION_LOG.md?
8. Phase boundary: Quick wins in Phase 2 (design) or Phase 3 (impl)?
9. Dark mode: Include tokens now or defer to Phase 4?
10. Performance budget: <5% bundle increase correct threshold?

---

## Risks (6 Identified, Find 10+ More)

### Existing Risks
1. **Breaking functionality** - Visual regression tests, Playwright
2. **Brand dilution** - Maintain #0b2763, stakeholder review
3. **Performance degradation** - Bundle size <5%, Lighthouse ≥90
4. **Cross-browser compat** - Test Chrome/Firefox/Safari/Edge
5. **Streamlit conflicts** - Test isolation, scoped CSS
6. **Timeline slippage** - 15 work days, extend Week 3 if needed

### Find More Risks
- CSS specificity wars?
- JS event handler breakage?
- Third-party dependency conflicts?
- Content migration needs?
- SEO impact?
- Analytics blind spots?
- Internationalization (RTL, CJK)?
- Dark mode future?
- Print stylesheets?
- Accessibility audit failure?

---

## Design Token System v2 (Preview)

```json
{
  "version": "2.0.0",
  "colors": {
    "primary": "#0b2763",
    "text_muted": "#6c7280"  // Was #9ca3af (2.54:1 fail)
  },
  "spacing": {
    "xs": "4px", "sm": "8px", "md": "12px",
    "lg": "16px", "xl": "24px", "2xl": "32px"
  },
  "breakpoints": {
    "mobile": "320px", "tablet": "768px", "desktop": "1024px"
  }
}
```

**8px Baseline Grid**: All spacing follows 4/8/12/16/24/32/48px scale

---

## CSS Before/After Pattern

### ❌ Current (Inadequate)
```css
/* UI-020: Mobile H1 hyphenation */
h1.page-title { hyphens: auto; }
```

### ✅ Enhanced (Implementation-Ready)
```css
/* ===================================================================
 * UI-020: Mobile H1 Word Breaking Fix
 * Problem: Breaks "Documenta-tion" at 320px
 * Root cause: word-break: break-all in base
 * Affects: ~795 pages, 40% of users (mobile)
 * =================================================================== */

/* BEFORE (docs/_static/custom.css:145-150) */
h1.page-title {
  word-break: break-all;      /* ❌ Too aggressive */
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 1rem;
}

/* AFTER (complete replacement) */
@media (max-width: 375px) {
  h1.page-title {
    word-break: normal;
    overflow-wrap: break-word;
    hyphens: auto;
    -webkit-hyphens: auto;
    -ms-hyphens: auto;
    max-width: calc(100vw - 32px);
    font-size: 1.875rem;
    /* Keep other properties same */
  }
}

/* Browser support: Chrome 55+, Firefox 43+, Safari 5.1+ */
/* Test: Open at 320px, verify no mid-word breaks */
/* Risk: Requires <html lang="en"> for hyphenation */
```

**Key Differences**:
- Complete before/after (not just changed properties)
- Browser support documented
- Test procedure specified
- Risk/prerequisite noted

---

## Workflow (8 Steps)

1. **Read Phase 1** (30min) - Audit reports, issue backlog, design system
2. **Inspect CSS** (20min) - custom.css, code-collapse.css, base-theme.css
3. **Use Sequential Thinking** (throughout) - Trade-offs, alternatives, risks
4. **Analyze Issues** (1hr) - Dependencies, cascading impacts, edge cases
5. **Enhance Specs** (2hr) - Implementation-ready CSS, browser compat, tests
6. **Evaluate Alternatives** (1hr) - Trade-off matrices for major decisions
7. **Assess Risks** (1hr) - 15+ risks with probability/impact scores
8. **Optimize Sequencing** (30min) - Critical path, parallelization

**Total**: 6-7 hours

---

## Tools to Use

- **Sequential Thinking**: `mcp__sequential-thinking__sequentialthinking`
- **File Reading**: Read Phase 1 files, inspect existing CSS
- **Contrast Checker**: WebAIM or Chrome DevTools for WCAG validation
- **Analysis**: Dependency graphs, trade-off matrices, risk matrices
- **Documentation**: Markdown with code blocks, tables, diagrams

---

## Common Pitfalls (Avoid These)

❌ **Don't**: Provide only changed CSS properties
✅ **Do**: Show complete before/after with full context

❌ **Don't**: Say "Option A is better"
✅ **Do**: "Option A: 5hr, 40% users, ROI=8. Option B: 8hr, 60% users, ROI=7.5"

❌ **Don't**: Assume existing Phase 2 plan is perfect
✅ **Do**: Challenge assumptions, propose alternatives

❌ **Don't**: List risks without quantification
✅ **Do**: Risk = 60% probability × 7/10 impact = 4.2 score

❌ **Don't**: Say "test it works"
✅ **Do**: "Open at 320px, verify no mid-word breaks in H1 titles"

---

**This is your rapid lookup guide. Return here during analysis when you need quick facts.**
