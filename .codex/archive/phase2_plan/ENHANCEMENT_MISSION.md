# Phase 2 Enhancement Mission - Detailed Instructions

> **For**: Claude Code instances enhancing the Phase 2 plan
> **Prerequisites**: Read `README.md` and `PHASE2_COMPLETE_PLAN.md` first
> **Output Directory**: `.codex/phase2_audit/`
> **Estimated Time**: 4-6 hours of deep analysis work

---

## Mission Overview

You have received a **drafted Phase 2 plan** with 7 themed remediation workstreams and material specifications. Your job is to **enhance this plan** through deep analysis to create **implementation-ready specifications** with zero ambiguity.

The current plan provides high-level material specs and CSS examples. You must:
1. Analyze issues at deeper level (dependencies, cascading impacts, edge cases)
2. Create implementation-ready specs (complete before/after code, browser compat, test procedures)
3. Evaluate alternative approaches with trade-off analysis
4. Assess comprehensive risks beyond the 6 identified
5. Optimize implementation sequencing (critical path, parallelization)
6. Specify Streamlit alignment technical details

---

## Six Enhancement Tasks

### Task 1: Enhanced Issue Analysis

**Current State**: 34 issues are grouped into 7 themes based on surface-level categories (spacing, typography, etc.)

**Your Enhancement**:

#### 1A. Root Cause Deep Dive
- **Analyze hidden dependencies**: Which issues share underlying root causes beyond their category?
- **Example**: Does UI-007 (4px rhythm) relate to UI-005 (duplicate bar spacing)? Are they both symptoms of no spacing system?
- **Challenge existing clustering**: Should UI-010 (red links) be in branding instead of color? Should UI-015 (warning text) be in accessibility?
- **Identify shared fixes**: Can one CSS change solve multiple issues?

**Deliverable Section**: Create dependency graph in `PHASE1_DEEP_DIVE_ANALYSIS.md`

#### 1B. Cascading Impact Analysis
- **Trace token changes**: If we update `--color-text-muted` from #9ca3af to #6c7280, what else needs adjustment?
- **Audit all usages**: Grep for token usage across all CSS files
- **Identify ripple effects**: Does UI-002 (muted text) fix require also updating UI-031 (callout contrast)?

**Deliverable Section**: Create cascading impact table

#### 1C. User Impact Quantification
- **Estimate affected users**: What % of users encounter each High/Critical issue?
- **Mobile traffic**: If 40% of users are mobile, UI-020 (mobile H1 break) affects 40% of all page views
- **Frequency scoring**: How often do users encounter each issue (every page vs. specific pages)?
- **Severity scoring**: Scale 1-10 for user frustration/blocker level

**Deliverable Section**: Create impact scoring matrix (frequency × severity)

#### 1D. Edge Case Examination
- **Non-English languages**: Does UI-020 (word-break) work for Arabic (RTL) or Chinese (no hyphens)?
- **Long user-generated content**: What happens to UI-022 (mobile nav) with 50-character labels?
- **Extreme viewports**: Test assumptions at 280px (iPhone SE) and 2560px (4K desktop)
- **Color-blind users**: Do UI fixes work for deuteranopia, protanopia, tritanopia?

**Deliverable Section**: Edge case validation checklist

---

**Expected Output**: `PHASE1_DEEP_DIVE_ANALYSIS.md` with:
- Refined issue clustering with dependency graph
- Cascading impact table (which fixes require coordinated changes)
- User impact scoring matrix (frequency × severity for all 34 issues)
- Edge case validation requirements

---

### Task 2: Material Spec Deep Dive

**Current State**: Material specs provide CSS examples but lack complete implementation details

**Your Enhancement**:

#### 2A. Complete Before/After Code
Current specs show only changed properties. You must provide:
- **Full selector context**: Not just `.button { color: blue; }` but complete rule with all properties
- **Specificity handling**: Will this rule be overridden? Check existing CSS specificity chains
- **State variations**: Show :hover, :focus, :active, :disabled states where relevant

**Example Enhancement Needed**:

Current spec says:
```css
/* UI-020: Mobile H1 hyphenation */
h1.page-title { hyphens: auto; }
```

Enhanced spec should say:
```css
/* ===================================================================
 * UI-020: Mobile H1 Word Breaking Fix
 * =================================================================== */

/* Problem Statement:
 * At 320px viewport, H1 breaks "Documentation" as "Documenta-tion"
 * Root cause: Aggressive word-break: break-all in base styles
 * Affects: ~795 pages (all documentation with H1 titles)
 * User impact: 40% of users (mobile traffic) see broken brand words
 */

/* BEFORE (docs/_static/custom.css:145-150) */
h1.page-title {
  word-break: break-all;      /* ❌ Too aggressive - breaks mid-word */
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 1rem;
}

/* AFTER (complete replacement) */
@media (max-width: 375px) {
  h1.page-title {
    /* Reset word breaking */
    word-break: normal;                /* Reset to default behavior */
    overflow-wrap: break-word;         /* Break only at word boundaries */

    /* Enable hyphenation */
    hyphens: auto;                     /* CSS hyphenation (requires lang attr) */
    -webkit-hyphens: auto;             /* Safari/iOS support */
    -ms-hyphens: auto;                 /* Legacy Edge support */
    hyphenate-limit-chars: 8 4 4;      /* Min 8 char word, leave 4 before/after hyphen */

    /* Ensure proper spacing */
    max-width: calc(100vw - 32px);     /* Respect 16px horizontal padding */

    /* Slightly reduce font size for mobile */
    font-size: 1.875rem;               /* 30px → 28px for better fit */

    /* Maintain other properties */
    font-weight: 700;
    color: var(--color-text-primary);
    margin-bottom: 1rem;
  }
}

/* PREREQUISITE: Ensure <html lang="en"> is set */
/* Without lang attribute, hyphens: auto won't work */

/* BROWSER SUPPORT:
 * ✓ Chrome 55+:   Full support for hyphens: auto
 * ✓ Firefox 43+:  Full support, may hyphenate aggressively
 * ✓ Safari 5.1+:  Requires -webkit- prefix
 * ✗ Edge <79:     Requires -ms- prefix (included above)
 * ✓ iOS Safari 4.2+: Works with -webkit- prefix
 */

/* TEST PROCEDURE:
 * 1. Open any page with H1 at 320px viewport (Chrome DevTools)
 * 2. Verify "Documentation" doesn't break mid-word (no "Documenta-tion")
 * 3. Test long words (e.g., "Characterization") hyphenate gracefully
 * 4. Test on real iPhone SE (Safari iOS 17)
 * 5. Test at 280px (iPhone 5S fallback - still readable?)
 * 6. Test non-English if <html lang> is dynamic (Spanish, German, French)
 */

/* POTENTIAL ISSUES:
 * - If <html lang> attribute missing, hyphens: auto silently fails
 * - Firefox may hyphenate too aggressively (consider hyphenate-limit-lines: 2)
 * - Some browsers don't respect hyphenate-limit-chars (gracefully degrades)
 * - Non-English content needs language-specific hyphenation rules
 * - Very long words (>20 chars) may still overflow on narrow viewports
 */

/* ROLLBACK PLAN:
 * If hyphenation causes issues, can revert to:
 * word-break: break-word;  /* Breaks between words only, no hyphens */
```

#### 2B. Browser Compatibility Details
For each CSS feature used:
- **Support table**: Chrome X+, Firefox Y+, Safari Z+, Edge W+
- **Polyfill requirements**: Does it need postcss-prefixer, autoprefixer?
- **Graceful degradation**: What happens in unsupported browsers?
- **Mobile-specific**: iOS Safari quirks, Android Chrome differences

#### 2C. Test Procedures
Specify exactly how to validate each change:
- **Unit test**: What to test (e.g., "H1 doesn't break mid-word at 320px")
- **Tools**: Chrome DevTools mobile emulator, BrowserStack, real devices
- **Success criteria**: Specific measurable outcome (e.g., "contrast ratio ≥4.5:1")
- **Regression check**: What could break (e.g., "H1 still fits at 1024px desktop")

#### 2D. Performance Impact
- **CSS size**: How many bytes does this add to the stylesheet?
- **Render performance**: Does this trigger layout recalculation?
- **Critical rendering path**: Is this CSS critical (above-fold) or deferrable?

---

**Expected Output**: Enhanced theme spec documents (`theme_01_accessibility.md` through `theme_07_streamlit.md`) with:
- Complete before/after code for every CSS change
- Browser compatibility tables
- Step-by-step test procedures
- Performance impact notes
- Specificity and cascade handling
- Zero ambiguity - implementers need no clarification

---

### Task 3: Alternative Approaches

**Current State**: Plan proposes single solution for each issue

**Your Enhancement**: Evaluate 2-4 alternatives for major decisions, analyze trade-offs

#### 3A. UI-002 Muted Text Color Alternatives

**Current Proposal**: #6c7280 (4.52:1 contrast)

**Alternatives to Evaluate**:
1. **#636975** (5.0:1 contrast) - Darker, safer margin above WCAG
2. **#707580** (4.8:1 contrast) - Middle ground
3. **#6c7280** (4.52:1 contrast) - Proposed (just above 4.5:1 minimum)
4. **#7b8794** (4.0:1 contrast) - Lighter, fails WCAG but better hierarchy

**Trade-Off Analysis**:
```markdown
| Option | Contrast | Visual Hierarchy | WCAG Pass | Trade-Off |
|--------|----------|------------------|-----------|-----------|
| #636975 | 5.0:1 | ⚠️ Too prominent, competes with primary text | ✅ AA+ | Sacrifices hierarchy for safety margin |
| #707580 | 4.8:1 | ✅ Good balance | ✅ AA | Optimal - small buffer + maintains hierarchy |
| #6c7280 | 4.52:1 | ✅ Clear hierarchy | ✅ AA (barely) | Risky - any change breaks WCAG |
| #7b8794 | 4.0:1 | ✅ Best hierarchy | ❌ Fail | Rejected - non-compliant |

**Recommendation**: #707580 - provides 6% buffer above WCAG minimum while maintaining clear visual hierarchy.
**Rationale**: #6c7280 (current proposal) is only 0.4% above minimum; any slight change in browser rendering or background color breaks compliance. #707580 provides safety margin without making muted text too prominent.
```

#### 3B. UI-001 Code Collapse Affordance Alternatives

**Current Proposal**: Increase opacity 0.3 → 0.6, add aria-expanded

**Alternatives to Evaluate**:
1. **Opacity increase** (current) - Simple, maintains minimalist aesthetic
2. **Different icon** - Replace caret with more obvious icon (e.g., chevron-down, plus/minus)
3. **Text label** - Add "Collapse" text next to icon
4. **Background highlight** - Add subtle background on hover to increase discoverability
5. **Animation hint** - Subtle pulse animation on page load (respecting prefers-reduced-motion)

**Trade-Off Matrix**: Create comparison table evaluating:
- Discoverability (1-10 score)
- Visual noise (1-10, lower is better)
- Implementation effort (hours)
- Maintenance complexity
- Screen reader friendliness
- Brand consistency

**Recommendation with Rationale**

#### 3C. Spacing System Baseline Grid

**Current Proposal**: 8px baseline grid

**Alternatives to Evaluate**:
1. **4px grid** - More granular, allows finer control
2. **6px grid** - Aligns with rem units (if root font-size is 16px, 6px = 0.375rem)
3. **8px grid** - Proposed (common in design systems)
4. **12px grid** - Simpler, fewer token values needed

**Research Questions**:
- What do major design systems use? (Material Design, Bootstrap, Tailwind, Ant Design)
- What's the smallest spacing gap currently used in the design? (If it's 4px, need 4px grid)
- How many unique spacing values exist currently? (If >15, may need finer grid)

#### 3D. Responsive Strategy

**Current Proposal**: Media queries (viewport-based)

**Alternatives**:
1. **Media queries** (current) - Universal browser support
2. **Container queries** - Modern, component-based, better isolation
3. **Hybrid** - Container queries with media query fallback

**Trade-Off Analysis**:
```markdown
| Approach | Browser Support | Maintainability | Future-Proof | Complexity |
|----------|----------------|-----------------|--------------|------------|
| Media queries | 100% (all browsers) | ⚠️ Global, affects all components | ❌ Legacy approach | Simple |
| Container queries | Chrome 105+, Safari 16+ (~85% users) | ✅ Component-scoped | ✅ Modern standard | Medium |
| Hybrid | 100% (graceful degradation) | ⚠️ Maintain both | ✅ Best of both | Complex |

**Recommendation**: [Your justified choice]
```

---

**Expected Output**: `ALTERNATIVE_APPROACHES.md` with:
- 3-5 alternatives evaluated for each major decision
- Trade-off comparison tables (quantitative where possible)
- Visual mockups comparing alternatives (optional but recommended)
- Clear recommendation with research-backed rationale
- References to industry standards and research

---

### Task 4: Enhanced Risk Assessment

**Current State**: 6 risks identified (breaking functionality, brand, performance, browser compat, Streamlit, timeline)

**Your Enhancement**: Identify 10+ additional risks, quantify with probability/impact matrix

#### 4A. Additional Risks to Analyze

1. **CSS Specificity Wars**
   - Risk: New token-based rules overridden by existing `!important` rules
   - Detection: Grep for `!important` in CSS, check specificity of new rules
   - Mitigation: Use `:where()` pseudo-class to reduce specificity, or increase specificity strategically

2. **JavaScript Event Handler Breakage**
   - Risk: Changing HTML structure breaks existing `.addEventListener()` selectors
   - Detection: Audit JS files for DOM selectors matching changed HTML
   - Mitigation: Use data attributes for JS hooks, not classes/IDs

3. **Third-Party Dependency Conflicts**
   - Risk: Sphinx Furo theme update overrides our customizations
   - Detection: Check Furo theme changelog, pin version
   - Mitigation: Fork Furo theme or use CSS `!important` sparingly

4. **Content Migration Needs**
   - Risk: 795 documentation pages need manual updates for new patterns
   - Detection: Grep for hardcoded styles in Markdown/RST files
   - Mitigation: Use Sphinx directives and templates, not inline styles

5. **SEO Impact**
   - Risk: Changing heading hierarchy affects search rankings
   - Detection: Compare H1/H2 usage before/after
   - Mitigation: Maintain semantic HTML structure, consult SEO specialist

6. **Analytics Blind Spots**
   - Risk: No baseline metrics to measure improvement
   - Detection: Check Google Analytics, Hotjar, or session recordings
   - Mitigation: Set up event tracking before Phase 3 implementation

7. **Internationalization (i18n)**
   - Risk: Fixes designed for English fail for RTL (Arabic) or CJK (Chinese) languages
   - Detection: Test with `<html lang="ar" dir="rtl">` and long CJK strings
   - Mitigation: Use logical properties (`padding-inline-start` not `padding-left`)

8. **Dark Mode (Future)**
   - Risk: Color changes assume light mode, break future dark mode
   - Detection: Check if dark mode is planned
   - Mitigation: Define both light + dark token values now

9. **Print Stylesheets**
   - Risk: Screen-optimized changes hurt print/PDF output
   - Detection: Generate PDF from documentation, check layout
   - Mitigation: Maintain separate `@media print` rules

10. **Accessibility Audit Failure**
    - Risk: Internal validation misses issues, external audit finds violations
    - Probability: Medium (internal testing often incomplete)
    - Mitigation: Hire WCAG certified auditor before Phase 3 completion

#### 4B. Probability/Impact Matrix

Create quantitative risk matrix:

```markdown
| Risk ID | Risk Description | Probability (%) | Impact (1-10) | Risk Score | Mitigation Cost |
|---------|-----------------|-----------------|---------------|------------|----------------|
| R01 | CSS specificity wars | 60% | 7 | 4.2 | 8hr |
| R02 | JS event breakage | 40% | 9 | 3.6 | 12hr |
| R03 | Furo theme conflict | 30% | 6 | 1.8 | 4hr |
| ... | ... | ... | ... | ... | ... |

Risk Score = Probability × Impact
Prioritize risks with score >3.0
```

#### 4C. Mitigation Strategies

For each high-risk item (score >3.0):
- **Detection method**: How to identify if risk materializes
- **Prevention**: Steps to reduce probability
- **Mitigation**: If risk occurs, how to fix quickly
- **Contingency**: Worst-case rollback plan

---

**Expected Output**: `RISK_ASSESSMENT_DETAILED.md` with:
- 15+ risks identified (6 existing + 10+ new)
- Probability/impact matrix with quantitative scores
- Detailed mitigation strategies for high-risk items (score >3.0)
- Detection methods and early warning signs
- Contingency plans and rollback procedures

---

### Task 5: Implementation Sequencing Optimization

**Current State**: 3-wave approach (Wave 1: Accessibility+Color+Spacing, Wave 2: Typography+Responsive, Wave 3: Interaction+Streamlit)

**Your Enhancement**: Optimize sequencing with critical path analysis, consider alternatives

#### 5A. Critical Path Analysis

**Questions to Answer**:
- What's the absolute minimum set of changes to ship Phase 2.1 early?
- Can we parallelize Wave 2 (Typography + Responsive)?
- Should we break Wave 1 into sub-waves (Accessibility first, then Color/Spacing)?
- Is 3 waves optimal, or should we consider 2 waves (faster) or 4 waves (safer)?

**Create Dependency Graph**:
```
UI-002 (muted text) ─────→ UI-031 (callout contrast)
                       ↘
UI-005 (spacing) ──────→ UI-020 (mobile responsive)
                       ↘
UI-001 (code collapse) ──→ UI-004 (screen reader)
```

#### 5B. Parallelization Opportunities

**Current**: Wave 2 runs Typography + Responsive sequentially
**Question**: Can Typography (Theme 4) and Responsive (Theme 3) run in parallel?
- **Dependency check**: Does responsive CSS depend on typography tokens? (Probably not)
- **Resource check**: Do we have 2 developers to work simultaneously?
- **Risk**: Merge conflicts if both touch same files

**Recommendation**: [Evaluate if parallel execution saves time vs. introduces risk]

#### 5C. Minimum Viable Phase 2.1

**Scenario**: Stakeholder requests early Phase 2 results in 1 week instead of 3

**Analysis**: What's the minimum set to demonstrate value?
- **Option 1**: Only Critical/High issues (UI-002, UI-003, UI-004, UI-020, UI-022) = 5 issues
- **Option 2**: Wave 1 only (Accessibility + Color + Spacing) = 16 issues
- **Option 3**: Quick wins only (3 issues, 14 hours) = Proof of concept

**Effort Estimate**:
- Option 1: ~30 hours (1 week, 1 developer)
- Option 2: ~60 hours (1.5 weeks, 1 developer)
- Option 3: ~14 hours (2 days, 1 developer)

**Trade-Off**: Shipping early shows progress but delivers incomplete design system (risky for Phase 3)

#### 5D. Testing Dependencies

**Question**: Which changes need full regression testing vs. spot checks?

**Create Testing Tiers**:
- **Tier 1**: Full regression (Playwright suite + visual regression on 20 pages) - for breaking changes
- **Tier 2**: Visual regression only - for CSS-only changes
- **Tier 3**: Spot check (manual QA on 5 key pages) - for low-risk changes

**Assign tiers to each theme**:
- Theme 1 (Accessibility): Tier 1 (HTML structure changes)
- Theme 2 (Spacing): Tier 2 (CSS tokens only)
- ...

#### 5E. Rollback Strategy

**Question**: How do we version design tokens so Phase 3 can rollback individual themes?

**Options**:
1. **Git tags per wave**: `phase2-wave1`, `phase2-wave2`, etc.
2. **Semantic versioning**: `design_tokens_v2.0.0`, `v2.1.0` (breaking changes bump minor)
3. **Feature flags**: CSS classes like `.theme-accessibility-v2` that can be toggled
4. **Branching**: Separate git branch per theme, merge only when validated

**Recommendation**: [Choose strategy with pros/cons]

---

**Expected Output**: `IMPLEMENTATION_SEQUENCING_OPTIMIZED.md` with:
- Critical path diagram (Gantt chart or dependency graph)
- Parallelization analysis (can Wave 2 run in parallel?)
- Minimum Viable Phase 2.1 definition (if early delivery needed)
- Testing tier assignments (which themes need full regression)
- Rollback strategy with git workflow
- Alternative wave structures (2-wave vs 3-wave vs 4-wave comparison)

---

### Task 6: Streamlit Alignment Deep Dive

**Current State**: Theme 7 has high-level Streamlit theming suggestions but lacks technical depth

**Your Enhancement**: Create detailed technical specification for Streamlit alignment

#### 6A. Streamlit Theme API Audit

**Research Questions**:
- What can actually be customized via `.streamlit/config.toml`?
- What requires CSS injection via `st.markdown()`?
- What's impossible to customize (hardcoded in Streamlit)?

**Audit Streamlit Theme API** (check Streamlit docs):
```toml
[theme]
primaryColor = "?"        # What elements does this affect?
backgroundColor = "?"      # What elements?
secondaryBackgroundColor = "?"  # What elements?
textColor = "?"           # What elements?
font = "?"                # Options: sans serif, serif, monospace
# What else is available?
```

**Document Coverage**:
- ✅ Customizable: Buttons, sidebar background, text color
- ⚠️ Partial: Metrics (can style but not structure)
- ❌ Not customizable: Navigation layout, header structure

#### 6B. CSS Injection Strategy

**For elements not customizable via config.toml:**

**Question**: How to inject custom CSS without breaking Streamlit updates?

**Options**:
1. **`st.markdown()` with `unsafe_allow_html=True`** (current proposal)
   - Pros: Simple, no build step
   - Cons: CSS in Python code (maintenance burden), no IDE support

2. **External CSS file loaded via `st.markdown()`**:
   ```python
   with open('streamlit_custom.css') as f:
       st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
   ```
   - Pros: Separate CSS file, easier to maintain
   - Cons: Still uses unsafe_allow_html

3. **Streamlit component** (custom React component):
   - Pros: Full control, proper encapsulation
   - Cons: High complexity, requires React knowledge

**Recommendation**: [Choose based on trade-offs]

**Version Compatibility Check**:
- Test with Streamlit 1.29+ (latest stable)
- Check changelog for breaking changes in CSS class names
- Document which CSS selectors are stable vs. likely to change

#### 6C. Component Mapping

**Create table mapping Sphinx components to Streamlit widgets**:

| Sphinx Documentation | Streamlit Widget | Customization Approach |
|---------------------|------------------|------------------------|
| Primary button (gradient blue) | `st.button()` | config.toml primaryColor + CSS injection for gradient |
| Sidebar navigation | `st.sidebar` | config.toml secondaryBackgroundColor + CSS for spacing |
| Code block (navy theme) | `st.code()` | CSS injection (theme not customizable via config) |
| Metric badge | `st.metric()` | CSS injection for gradient header |
| Download button | `st.download_button()` | CSS injection for pill shape + gradient |
| Data table | `st.dataframe()` | Limited - can style via pandas Styler |

**For each mapping**:
- Customization level: Full / Partial / None
- Recommended approach: config.toml / CSS injection / custom component
- Code example

#### 6D. Shared Token Strategy

**Question**: Should design tokens be CSS variables, SCSS variables, or Python constants?

**Options Analysis**:

1. **CSS Custom Properties** (CSS variables):
   ```css
   :root { --color-primary: #0b2763; }
   ```
   - Pros: Browser-native, runtime changes possible
   - Cons: Only works in browser (not available to Python/Streamlit config)

2. **SCSS Variables** (build-time):
   ```scss
   $color-primary: #0b2763;
   ```
   - Pros: Compile-time validation, can generate both CSS and Python
   - Cons: Requires build step, not runtime changeable

3. **Python Constants**:
   ```python
   # tokens.py
   COLOR_PRIMARY = "#0b2763"

   # Use in streamlit_app.py and generate CSS
   st.markdown(f"<style>:root {{ --color-primary: {COLOR_PRIMARY}; }}</style>")
   ```
   - Pros: Single source of truth accessible to both Python and CSS
   - Cons: Requires code generation for CSS

4. **JSON File** (current Phase 2 plan):
   ```json
   {"colors": {"primary": "#0b2763"}}
   ```
   - Pros: Language-agnostic, can be consumed by Python, CSS generator, docs
   - Cons: Requires parsing step

**Recommendation**: [Evaluate based on project constraints]

#### 6E. Update Resilience

**Question**: Will Streamlit 2.0 (future) break our customizations?

**Mitigation Strategies**:
- Pin Streamlit version in `requirements.txt` (e.g., `streamlit~=1.29.0`)
- Use stable CSS selectors (prefer data attributes over class names if available)
- Subscribe to Streamlit changelog/release notes
- Document which customizations are fragile (likely to break)
- Create upgrade testing checklist for future Streamlit versions

#### 6F. Theme 7 Implementation Effort

**Re-estimate effort** based on deep dive:

```markdown
| Task | Original Estimate | Revised Estimate | Notes |
|------|-------------------|------------------|-------|
| config.toml setup | 1hr | 1hr | No change |
| CSS injection | 2hr | 4hr | More complex than expected |
| Component mapping | 2hr | 6hr | Need custom styling for 6 widgets |
| Shared token generation | 1hr | 3hr | Build Python → CSS generator |
| Testing | 2hr | 4hr | Test with real data, edge cases |
| Documentation | 1hr | 2hr | Document maintenance procedures |
| **Total** | **9hr** | **20hr** | 2.2x increase |
```

---

**Expected Output**: `STREAMLIT_ALIGNMENT_SPECIFICATION.md` with:
- Streamlit theme API audit (what's customizable)
- CSS injection strategy with version compatibility notes
- Component mapping table (Sphinx → Streamlit)
- Shared token strategy recommendation (CSS vars / SCSS / Python / JSON)
- Update resilience plan (pinning versions, stable selectors)
- Revised effort estimate (may be higher than original 9hr)

---

## Ten Specific Questions to Answer

Your enhancement must answer these questions with research-backed recommendations:

### Q1: UI-002 Muted Text Color
**Question**: Is #6c7280 (4.52:1) the optimal choice? Should we target 5:1 for comfort buffer above WCAG AA 4.5:1 minimum?

**Research Required**:
- Compare 3-5 color alternatives visually
- Test on actual page screenshots
- Measure hierarchy impact (does it compete with primary text?)
- Check industry standards (what do major design systems use?)

**Answer Format**: Recommendation with visual comparison and rationale

---

### Q2: Quick Wins Priority
**Question**: Are these the 3 fastest wins? Could UI-021 (mobile button spacing) be faster than UI-005 (duplicate bar)?

**Research Required**:
- Create effort/impact matrix for top 10 issues
- Score on effort (hours) and impact (users affected × severity)
- Calculate ROI: impact / effort

**Answer Format**: Revised quick wins list with ROI justification

---

### Q3: Design Token Versioning
**Question**: How do we version tokens for breaking changes? Semantic versioning (v2.0.0 → v2.1.0)? Deprecation warnings in CSS comments? Token migration guide?

**Research Required**:
- Survey how major design systems version (Material Design, Bootstrap)
- Evaluate git-based vs. semantic versioning
- Consider backward compatibility needs

**Answer Format**: Recommended versioning strategy with example

---

### Q4: Mobile-First vs. Desktop-First
**Question**: Plan says "mobile-first" but project was built desktop-first. Should we refactor entire CSS architecture (expensive) or patch mobile breakpoints (pragmatic)?

**Research Required**:
- Estimate refactor effort (rewrite all CSS mobile-first)
- Estimate patch effort (add mobile media queries)
- Analyze technical debt of patch approach

**Answer Format**: Cost-benefit analysis with recommendation

---

### Q5: External Accessibility Audit
**Question**: Should we hire WCAG auditors ($2-5k) or is internal validation sufficient? What's the legal/compliance risk? Do we need VPAT certification?

**Research Required**:
- Understand organization's compliance requirements
- Research WCAG audit costs and deliverables
- Evaluate risk of non-compliance (lawsuits, reputation)

**Answer Format**: Risk assessment with recommendation

---

### Q6: Stakeholder Review Timing
**Question**: Plan assumes 2-3 days per review cycle. Is this realistic for busy stakeholders? Should we build in 5-day windows?

**Research Required**:
- Check stakeholder availability
- Review past project timelines (how long did reviews actually take?)
- Calculate impact of 5-day windows on overall timeline

**Answer Format**: Revised timeline with realistic windows

---

### Q7: Decision Documentation
**Question**: How do we ensure future maintainers understand WHY each decision was made? ADRs (Architecture Decision Records)? Inline CSS comments? Separate DECISION_LOG.md?

**Research Required**:
- Survey decision documentation best practices
- Evaluate maintenance burden of each approach
- Consider discoverability (where will future devs look?)

**Answer Format**: Recommended approach with template

---

### Q8: Phase 2 vs. Phase 3 Boundary
**Question**: Should quick wins be in Phase 2 (design) or Phase 3 (implementation)? The plan includes them in Phase 2 - is this optimal?

**Research Required**:
- Understand Phase 2/3 deliverables clearly
- Evaluate if quick wins demonstration requires implementation
- Consider stakeholder expectations

**Answer Format**: Recommendation with rationale

---

### Q9: Dark Mode Consideration
**Question**: Plan focuses on light mode. Should Phase 2 include dark mode tokens even if implementation is Phase 4? Future-proofing vs. scope creep?

**Research Required**:
- Check if dark mode is on roadmap
- Estimate effort to define dark tokens now (vs. later)
- Evaluate cost of not planning ahead

**Answer Format**: Recommendation (include now / defer / partial)

---

### Q10: Performance Budget
**Question**: Plan says "<5% bundle size increase acceptable". Is this the right threshold? Should we set byte budget (e.g., "+10KB max")?

**Research Required**:
- Measure current CSS bundle size
- Calculate 5% in absolute terms
- Research industry standards for CSS performance budgets

**Answer Format**: Specific byte budget with justification

---

## Deliverable Specifications

### Primary Deliverable: PHASE2_PLAN_ENHANCED.md

**Structure**:
```markdown
# Phase 2: Design Remediation Concepts - ENHANCED PLAN

## Executive Summary
- What changed from original plan
- Key insights from deep analysis
- Critical recommendations

## Issue Analysis Enhancement
- Refined clustering with dependency graph
- Cascading impact analysis
- User impact quantification
- Edge case considerations

## Material Specifications (Enhanced)
[For each theme, provide implementation-ready specs]

## Alternative Approaches Evaluated
[Trade-off analysis for major decisions]

## Comprehensive Risk Assessment
[15+ risks with mitigation strategies]

## Optimized Implementation Sequencing
[Critical path, parallelization opportunities]

## Streamlit Alignment Technical Spec
[Detailed implementation guide]

## Answers to 10 Specific Questions
[Each question answered with research]

## Updated Timeline
[Realistic timeline with buffer]

## Enhanced Success Criteria
[Measurable KPIs and validation procedures]

## Decision Log
[Why each major decision was made]
```

---

### Supporting Deliverables (9 documents)

Create in `.codex/phase2_audit/`:

1. **PHASE1_DEEP_DIVE_ANALYSIS.md** - Enhanced issue analysis
2. **ALTERNATIVE_APPROACHES.md** - Trade-off comparisons
3. **RISK_ASSESSMENT_DETAILED.md** - Comprehensive risk matrix
4. **IMPLEMENTATION_SEQUENCING_OPTIMIZED.md** - Gantt + critical path
5. **STREAMLIT_ALIGNMENT_SPECIFICATION.md** - Technical spec
6. **DECISION_LOG.md** - Rationale for decisions
7. **EFFORT_IMPACT_MATRIX.md** - All 34 issues scored
8. **BROWSER_COMPATIBILITY_MATRIX.md** - CSS feature support
9. **VALIDATION_PROCEDURES.md** - Step-by-step testing

---

## Workflow Instructions

### 1. Read Phase 1 Context (30 min)
- `.codex/phase1_audit/PHASE1_COMPLETION_REPORT.md`
- `.codex/phase1_audit/phase1_issue_backlog.md`
- `.codex/phase1_audit/phase1_component_inventory.csv`
- `.codex/phase1_audit/DESIGN_SYSTEM.md`
- `.codex/phase1_audit/phase1_consistency_matrix.md`

### 2. Inspect Existing Code (20 min)
- `docs/_static/custom.css` - Main styles (check specificity)
- `docs/_static/code-collapse.css` - Interactive features (check JS dependencies)
- `docs/_static/css-themes/base-theme.css` - Theme base
- `streamlit_app.py` - Streamlit app structure

### 3. Use Sequential Thinking (throughout)
- Tool: `mcp__sequential-thinking__sequentialthinking`
- For: Trade-off analysis, alternative evaluation, risk assessment
- Document: Reasoning process in enhanced specs

### 4. Create Enhanced Specs (3-4 hours)
- Start with Task 1 (Issue Analysis)
- Move to Task 2 (Material Specs)
- Continue through Tasks 3-6
- Answer 10 specific questions

### 5. Validate Completeness (30 min)
- Check all 10 deliverables created
- Verify all 10 questions answered
- Confirm no ambiguity in material specs
- Ensure trade-offs analyzed for major decisions

---

## Success Criteria

### Your enhancement succeeds if:

**Implementation Readiness** (Most Critical):
- ✓ Phase 3 implementers can execute with zero ambiguity
- ✓ All Critical + High issues have complete CSS/markup examples (not just changed properties)
- ✓ Material specs include browser compat tables + test procedures
- ✓ No assumptions or "figure it out later" gaps

**Analysis Depth**:
- ✓ Alternative approaches evaluated with quantitative trade-offs
- ✓ Risks quantified with probability/impact scores (not just listed)
- ✓ All 10 questions answered with research-backed recommendations
- ✓ Issue dependencies mapped with cascading impact analysis

**Quality Standards**:
- ✓ Timeline realistic with appropriate buffer (not overly optimistic)
- ✓ Decisions documented with clear rationale for future maintainers
- ✓ Code examples show complete before/after (including context)
- ✓ Validation criteria specific and measurable (not "test it works")

---

## Tips for Success

1. **Be Specific**: "Increase opacity" ❌ → "Change opacity from 0.3 to 0.6 in code-collapse.css:79" ✅

2. **Show Complete Code**: Not just changed properties, but full selector with all properties

3. **Quantify Trade-Offs**: Not "Option A is better", but "Option A: 5hr effort, 40% users affected. Option B: 8hr effort, 60% users affected. ROI: A = 8, B = 7.5. Choose A."

4. **Challenge Assumptions**: Don't accept the Phase 2 plan as gospel. If 8px baseline grid seems arbitrary, research alternatives.

5. **Think About Maintainers**: Future developers will read your specs. Make WHY decisions were made crystal clear.

6. **Use Real Data**: Not "many users", but "40% of users based on analytics from Oct 2024"

7. **Consider Edge Cases**: Test your assumptions at extremes (280px mobile, 2560px desktop, RTL languages)

8. **Document Risks**: Not just "this could break", but "25% probability of breaking, impact = 7/10, mitigation cost = 8hr"

---

**Now begin: Read Phase 1 files, inspect existing CSS, use sequential thinking, and create enhanced documentation.**
