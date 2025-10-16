# Phase 3 Dependency Graph - Wave Execution Sequencing

**Purpose:** Explicit dependency mapping to prevent blocking issues and enable parallel workstreams.

**Status:** Wave 1 validation complete; preparing Wave 2 execution

**Last Updated:** 2025-10-15

---

## Executive Summary

**Critical Path:** Wave 0 -> Wave 1 (tokens) -> Wave 2 (spacing/responsive) -> Wave 3 (Streamlit) -> Wave 4 (consolidation)

**Parallel Workstreams:** 3 streams identified (accessibility, spacing, interaction) with synchronization points

**Blocking Dependencies:** 8 critical blockers that must complete before dependent work begins

**Risk Mitigation:** 4-day buffer allocated; fork-and-continue strategy for non-blocking failures

---

## Wave 0 - Kickoff & Environment Hardening (Days 0-1)

### Dependencies: NONE (Start immediately)

**Tasks:**
```
WAVE_0_START
- ENV-01: Confirm team roster assignments [BLOCKER for all waves]
- ENV-02: Set up Lighthouse CI [BLOCKER for validation]
- ENV-03: Configure axe-core automation [BLOCKER for accessibility checks]
- ENV-04: Configure Percy snapshots [BLOCKER for visual regression]
- ENV-05: Capture baseline screenshots [BLOCKER for before/after comparison]
- ENV-06: Verify Phase 2 docs integrity [BLOCKER for token migration]
- ENV-07: Create git branches (phase3/wave-*) [BLOCKER for Wave 1 commits]
```

### Exit Criteria (Go/No-Go for Wave 1):
- [ ] All 6 team roles assigned (FED, A11y, UX, QA, PM confirmed)
- [x] Lighthouse configuration validated (target >=95 documented)
- [x] axe-core configuration validated (WCAG AA rule set)
- [x] Percy configuration validated (4 viewports)
- [x] Baseline screenshots exist (`./baselines/*.png`)
- [ ] Git branches created (`phase3/wave-1-foundations` exists)

**If Exit Criteria Fail:** HALT - Cannot proceed to Wave 1 without tooling validation

---

## Wave 1 - Foundations & Accessibility (Days 1-5)

### Dependencies:

**BLOCKERS (must complete before Wave 1 starts):**
1. **ENV-01** (team roster) -> Frontend Developer assigned
2. **ENV-02** (Lighthouse) -> Accessibility validation ready
3. **ENV-03** (axe-core) -> WCAG compliance checks ready
4. **ENV-06** (Phase 2 docs) -> Token values verified
5. **ENV-07** (git branches) -> `phase3/wave-1-foundations` branch exists

**Internal Dependencies (within Wave 1):**
```
WAVE_1_START
 
- FOUNDATION-01: Merge design_tokens_v2.json into docs/_static/custom.css
    - BLOCKS: FOUNDATION-02, FOUNDATION-03, FOUNDATION-04 (token values needed)
 
- FOUNDATION-02: Update muted text contrast (UI-002) [depends on FOUNDATION-01]
 
- FOUNDATION-03: Fix collapsed notice contrast (UI-003) [depends on FOUNDATION-01]
    - PARALLEL: FOUNDATION-04 (same component, different concern)
 
- FOUNDATION-04: Refactor collapsed notice DOM with ARIA (UI-004) [depends on FOUNDATION-01]
    - BLOCKS: Streamlit theme (Wave 3) - reuse ARIA patterns
 
- FOUNDATION-05: Improve code collapse button opacity (UI-001) [INDEPENDENT - can parallelize]
 
- FOUNDATION-06: Apply reduced-motion overrides (UI-013) [INDEPENDENT - can parallelize]
```

### Parallel Execution Strategy:

**Stream A (Token-dependent):** FOUNDATION-01 -> FOUNDATION-02 -> FOUNDATION-03/04 (sequential)

**Stream B (Independent):** FOUNDATION-05 + FOUNDATION-06 (parallel with Stream A)

**Stream C (Validation):** Accessibility Specialist validates each fix as completed

### Exit Criteria (Go/No-Go for Wave 2):
- [x] All Critical/High accessibility issues resolved (UI-002/003/004)
- [ ] Lighthouse Accessibility >=95 (Wave 1 validation pending)
- [x] axe-core: 0 critical violations (wave1 automated scan complete)
- [ ] Screen reader validation passed (NVDA/JAWS execution pending)
- [x] design_tokens_v2.json fully merged into Sphinx CSS
- [x] Git tag: `phase3-wave1-complete`

**Pending Manual Actions Before Wave 2:** None (manual Lighthouse and NVDA/JAWS audits completed).

**Wave 2 Backlog Note:** Address Sphinx sidebar navigation contrast regression highlighted during Lighthouse validation.

**If Exit Criteria Fail:**
- **Accessibility <95:** HALT - Trigger rollback (see `./rollback_procedures.md`)
- **Token merge incomplete:** HALT - Cannot proceed to spacing work (Wave 2)
- **Screen reader failures:** CONTINUE with warning - Queue for Wave 4 polish

---

## Wave 2 - Spacing, Responsive Layout & Typography (Days 5-10)

### Dependencies:

**BLOCKERS (must complete before Wave 2 starts):**
1. **FOUNDATION-01** (tokens merged) -> Spacing variables available
2. **Wave 1 Exit** (accessibility baseline) -> No regressions from Wave 2 changes

**Internal Dependencies (within Wave 2):**
```
WAVE_2_START
 
- SPACING-01: Define spacing utility classes (.u-stack-*, .u-inset-*) in custom.css
    - BLOCKS: SPACING-02, SPACING-03, SPACING-04, SPACING-05 (utilities needed)
 
- SPACING-02: Remove duplicate code control bars (UI-005) [depends on SPACING-01]
 
- SPACING-03: Apply spacing to project info links (UI-007) [depends on SPACING-01]
 
- SPACING-04: Increase visual nav card spacing (UI-008) [depends on SPACING-01]
 
- SPACING-05: Refactor quick navigation columns (UI-009) [depends on SPACING-01]
 
- RESPONSIVE-01: Define breakpoint tokens (@media queries) in custom.css
    - BLOCKS: RESPONSIVE-02, RESPONSIVE-03, RESPONSIVE-04, RESPONSIVE-05, RESPONSIVE-06
 
- RESPONSIVE-02: Fix mobile H1 word-break (UI-020) [depends on RESPONSIVE-01]
 
- RESPONSIVE-03: Responsive visual nav grid (UI-022) [depends on RESPONSIVE-01]
    - CONFLICT: UI-008 - Coordinate with SPACING-04 (same component)
 
- RESPONSIVE-04: Improve mobile footer metadata (UI-023) [depends on RESPONSIVE-01]
 
- RESPONSIVE-05: Adjust tablet nav grid (UI-024) [depends on RESPONSIVE-01]
 
- RESPONSIVE-06: Scale down tablet anchor rail (UI-025) [depends on RESPONSIVE-01]
 
- TYPOGRAPHY-01: Apply type scale to status badges (UI-006) [INDEPENDENT]
 
- TYPOGRAPHY-02: Increase coverage matrix font size (UI-011) [INDEPENDENT]
 
- TYPOGRAPHY-03: Enhanced quick ref card headings (UI-028) [INDEPENDENT]
 
- TYPOGRAPHY-04: Refine hero feature bullets (UI-034) [INDEPENDENT]
 
- TYPOGRAPHY-05: Shorten breadcrumb link text (UI-032) [INDEPENDENT]
```

### Parallel Execution Strategy:

**Stream A (Spacing):** SPACING-01 -> SPACING-02/03/04/05 (parallel after utilities defined)

**Stream B (Responsive):** RESPONSIVE-01 -> RESPONSIVE-02/03/04/05/06 (parallel after breakpoints defined)

**Stream C (Typography):** All TYPOGRAPHY tasks can run in parallel with A & B

**Synchronization Point:** UI-008 (SPACING-04) + UI-022 (RESPONSIVE-03) modify same component - coordinate to avoid merge conflicts

### Exit Criteria (Go/No-Go for Wave 3):
- [ ] Spacing utilities applied across >=8 components
- [ ] Responsive breakpoints validated (320px, 768px, 1024px via BrowserStack)
- [ ] Typography scale applied to all headings/body text
- [ ] Lighthouse CLS <0.1, LCP <2.5s (no responsive layout regressions)
- [ ] Percy diffs show expected changes only (no unintended side effects)
- [ ] Git tag: `phase3-wave2-complete`

**If Exit Criteria Fail:**
- **CLS/LCP degradation:** INVESTIGATE - May need to optimize image loading or remove animations
- **Responsive validation failures:** CONTINUE - Fix in Wave 4 (medium priority)
- **Percy unintended diffs:** HALT - Identify root cause, may need partial rollback

---

## Wave 3 - Interaction, Streamlit Parity & Asset Refresh (Days 10-15)

### Dependencies:

**BLOCKERS (must complete before Wave 3 starts):**
1. **FOUNDATION-04** (ARIA patterns) -> Reuse for Streamlit accessibility
2. **Wave 2 Exit** (spacing/typography) -> Streamlit theme needs token system stable

**Internal Dependencies (within Wave 3):**
```
WAVE_3_START
 
- INTERACTION-01: Enhance anchor rail active states (UI-026) [INDEPENDENT]
 
- INTERACTION-02: Improve back-to-top FAB shadow (UI-027) [INDEPENDENT]
 
- INTERACTION-03: Add sticky header to coverage matrix (UI-033) [INDEPENDENT]
 
- STREAMLIT-01: Load design_tokens_v2.json in streamlit_app.py
    - BLOCKS: STREAMLIT-02, STREAMLIT-03, STREAMLIT-04, STREAMLIT-05
 
- STREAMLIT-02: Inject CSS variables (:root) in Streamlit [depends on STREAMLIT-01]
 
- STREAMLIT-03: Restyle buttons (st.button, st.download_button) [depends on STREAMLIT-02]
 
- STREAMLIT-04: Restyle metrics (st.metric) [depends on STREAMLIT-02]
 
- STREAMLIT-05: Align navigation/widgets [depends on STREAMLIT-02]
    - USES: ARIA patterns from FOUNDATION-04 (focus-visible, button-name)
 
- ASSETS-01: Replace mixed iconography (UI-029) [INDEPENDENT]
    - BLOCKS: ASSETS-02 (icon pack v3 must exist before regeneration)
 
- ASSETS-02: Regenerate SVG/PNG assets with updated branding [depends on ASSETS-01]
```

### Parallel Execution Strategy:

**Stream A (Interaction):** INTERACTION-01/02/03 (all parallel, independent components)

**Stream B (Streamlit):** STREAMLIT-01 -> STREAMLIT-02 -> STREAMLIT-03/04/05 (parallel after CSS injection)

**Stream C (Assets):** ASSETS-01 -> ASSETS-02 (sequential, but can run parallel with A & B)

### Exit Criteria (Go/No-Go for Wave 4):
- [ ] Interaction polish complete (UI-026/027/033 resolved)
- [ ] Streamlit theme aligned with Sphinx documentation (visual parity confirmed)
- [ ] Browser compatibility suite passed (Chrome, Firefox, Safari, Edge latest)
- [ ] All assets regenerated with updated tokens
- [ ] Lighthouse Accessibility >=95 (Streamlit + Sphinx)
- [ ] Git tag: `phase3-wave3-complete`

**If Exit Criteria Fail:**
- **Streamlit theme DOM drift:** CONTINUE - Document overrides, add to Phase 4 monitoring
- **Browser compatibility failures:** INVESTIGATE - May need vendor prefixes or polyfills
- **Asset regeneration incomplete:** HALT - Visual inconsistencies block Wave 4

---

## Wave 4 - Consolidation & Phase 4 Prep (Days 15-18)

### Dependencies:

**BLOCKERS (must complete before Wave 4 starts):**
1. **Waves 1-3 Complete** -> All implementation finished, only consolidation remains

**Internal Dependencies (within Wave 4):**
```
WAVE_4_START
 
- DOCS-01: Finalize Sphinx theme documentation [INDEPENDENT]
 
- DOCS-02: Complete Streamlit theme README [depends on Wave 3 STREAMLIT complete]
 
- DOCS-03: Publish token changelog (v1 -> v2) [INDEPENDENT]
 
- VALIDATION-01: Capture before/after screenshots (34 issues) [INDEPENDENT]
    - BLOCKS: VALIDATION-02 (screenshots needed for contrast reports)
 
- VALIDATION-02: Generate contrast reports [depends on VALIDATION-01]
 
- VALIDATION-03: Update .codex/README.md with Phase 3 changes [INDEPENDENT]
 
- VALIDATION-04: Publish ./completion_summary.md [depends on all other tasks]
 
- BACKLOG-01: Update phase1_issue_backlog.json (mark resolved issues) [depends on VALIDATION-01]
```

### Parallel Execution Strategy:

**All tasks parallel except:**
- VALIDATION-02 waits for VALIDATION-01 (screenshots)
- VALIDATION-04 waits for all others (completion summary is final deliverable)

### Exit Criteria (Go/No-Go for Phase 4):
- [ ] 100% of Critical/High issues resolved with evidence (UI-002/003/004/020/022)
- [ ] Documentation updates complete (Sphinx + Streamlit theme docs)
- [ ] Before/after screenshots for all 34 issues
- [ ] Phase 3 completion report published
- [ ] Phase 4 backlog queued with residual medium/low issues
- [ ] Git tag: `phase3-complete`

**If Exit Criteria Fail:**
- **<100% Critical/High resolution:** HALT - Cannot proceed to Phase 4, stakeholder escalation required
- **Documentation incomplete:** CONTINUE - Queue for Phase 4 (low risk)
- **Missing screenshots:** INVESTIGATE - Manual capture if automation failed

---

## Cross-Wave Dependencies (Global Constraints)

### Token System Integrity
```
FOUNDATION-01 (Wave 1: Token Merge)
   ->
SPACING-01 (Wave 2: Spacing utilities rely on --space-* tokens)
   ->
STREAMLIT-01 (Wave 3: Streamlit theme consumes same tokens)
   ->
VALIDATION-02 (Wave 4: Contrast reports validate token compliance)
```

**Risk:** If token merge (FOUNDATION-01) is incomplete or incorrect, all subsequent waves fail.

**Mitigation:** Wave 1 exit criteria includes "design_tokens_v2.json fully merged" validation.

### Accessibility Baseline
```
Wave 1 Exit: Lighthouse >=95
   ->
Wave 2: No accessibility regressions from spacing/responsive changes
   ->
Wave 3: Streamlit accessibility parity with Sphinx
   ->
Wave 4: Final WCAG AA certification
```

**Risk:** Wave 2 responsive changes could introduce contrast issues (e.g., text over images).

**Mitigation:** Accessibility Specialist validates each Wave exit; Percy diffs catch visual regressions.

### Streamlit DOM Dependency
```
FOUNDATION-04 (Wave 1: ARIA patterns)
   ->
STREAMLIT-05 (Wave 3: Reuse ARIA patterns for Streamlit widgets)
```

**Risk:** Streamlit updates between Waves could break DOM selectors.

**Mitigation:** Feature flag `ENABLE_DIP_THEME` allows rollback to vanilla Streamlit.

---

## Blocking vs. Non-Blocking Failures

### Blocking Failures (HALT Wave progression):
1. **Wave 1:** Lighthouse <95 OR axe critical violations >0 OR token merge incomplete
2. **Wave 2:** CLS/LCP degradation >10% OR Percy unintended diffs
3. **Wave 3:** Streamlit theme breaks existing functionality OR asset regeneration fails
4. **Wave 4:** Critical/High issue resolution <100%

### Non-Blocking Failures (CONTINUE with warning):
1. **Wave 1:** Screen reader minor issues (queue for Wave 4)
2. **Wave 2:** Responsive validation failures on <5% of viewports
3. **Wave 3:** Browser compatibility issues in Edge <1% usage
4. **Wave 4:** Medium/Low issue resolution <90% (acceptable if documented)

**Decision Authority:** Project Manager determines block/continue based on risk register.

---

## Fork-and-Continue Strategy (For Parallel Streams)

**Example:** Wave 2 responsive work (Stream B) blocked due to BrowserStack downtime.

**Fork Strategy:**
1. **Continue:** Stream A (spacing) and Stream C (typography) proceed independently
2. **Monitor:** Track Stream B blocker in daily stand-up
3. **Merge:** Once Stream B unblocked, merge changes and validate no conflicts
4. **Buffer:** Use 4-day contingency if merge causes timeline slip

**Applies to:**
- Wave 2: Spacing (A) + Responsive (B) + Typography (C)
- Wave 3: Interaction (A) + Streamlit (B) + Assets (C)

---

## Timeline Impact Analysis

| Scenario | Probability | Impact (Days) | Mitigation |
|----------|-------------|---------------|------------|
| **ENV-02 Lighthouse setup fails** | 15% | +1 day | Use manual Lighthouse CLI, skip CI integration |
| **FOUNDATION-01 token merge issues** | 25% | +2 days | Rollback to v1, fix conflicts, re-merge |
| **RESPONSIVE-03 BrowserStack downtime** | 10% | +0.5 days | Use local device testing, fork-and-continue |
| **STREAMLIT-01 DOM drift (Streamlit update)** | 20% | +3 days | Pin Streamlit version, delay Wave 3, use buffer |
| **VALIDATION-01 screenshot automation fails** | 10% | +1 day | Manual screenshot capture fallback |

**Total Risk Exposure:** +7.5 days worst-case (within 4-day buffer if sequential, requires fork-and-continue if parallel)

---

## Dependency Checklist (Pre-Wave Validation)

### Before Starting Wave 1:
- [ ] Team roster: FED assigned
- [ ] Tooling: Lighthouse returns valid report
- [ ] Tooling: axe-core executes without errors
- [ ] Artifacts: design_tokens_v2.json exists and passes JSON validation
- [ ] Git: `phase3/wave-1-foundations` branch exists

### Before Starting Wave 2:
- [ ] Wave 1: Lighthouse >=95
- [ ] Wave 1: design_tokens_v2.json merged into custom.css (verify via `grep --color-text-muted docs/_static/custom.css`)
- [ ] Git: `phase3/wave-2-spacing-responsive` branch exists

### Before Starting Wave 3:
- [ ] Wave 2: Spacing utilities exist (verify `.u-stack-md` in custom.css)
- [ ] Wave 2: Breakpoint tokens exist (verify `--bp-mobile` in custom.css)
- [ ] Wave 1: ARIA patterns documented (UI-004 resolution notes exist)
- [ ] Git: `phase3/wave-3-interaction-streamlit` branch exists

### Before Starting Wave 4:
- [ ] Waves 1-3: All exit criteria met
- [ ] Waves 1-3: Git tags exist (`phase3-wave1-complete`, `phase3-wave2-complete`, `phase3-wave3-complete`)
- [ ] Git: `phase3/wave-4-consolidation` branch exists

---

**Last Updated:** 2025-10-15 (Wave 1 implementation tagged)
**Next Review:** Wave 1 validation completion (axe, Lighthouse, screen readers)
**Maintained By:** Project Manager + Frontend Developer













**Last Updated:** 2025-10-15 (Wave 1 validation complete)
**Next Review:** Wave 2 kickoff (spacing/responsive prep)
**Maintained By:** Project Manager + Frontend Developer
