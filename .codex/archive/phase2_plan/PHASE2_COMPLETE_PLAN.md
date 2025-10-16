# Phase 2: Design Remediation Concepts - COMPLETE PLAN

> **Version**: 1.0
> **Date**: 2025-10-14
> **Status**: Draft for enhancement
> **Based on**: Phase 1 audit results (34 issues, 62 components)

---

## Executive Summary

Transform 34 documented UI/UX issues (1 Critical, 4 High, 16 Medium, 13 Low) into actionable design specifications through **7 themed remediation workstreams**. Deliver design token system v2, detailed material specs, annotated visual mockups, and prioritized implementation roadmap over **3 weeks** (~110-150 hours).

**Key Innovation**: Execute 3 "quick wins" (Critical accessibility fix + 2 usability improvements) during Phase 2 to demonstrate value and validate approach before full Phase 3 implementation.

---

## Table of Contents

1. [Strategic Approach: 7 Themed Workstreams](#strategic-approach)
2. [Three-Wave Implementation Strategy](#three-wave-strategy)
3. [Four Major Deliverables](#deliverables)
4. [Quick Wins Strategy](#quick-wins)
5. [3-Week Timeline](#timeline)
6. [Resource Requirements](#resources)
7. [Risk Mitigation Framework](#risks)
8. [Stakeholder Communication Plan](#communication)
9. [Success Criteria](#success-criteria)

---

<a name="strategic-approach"></a>
## Strategic Approach: 7 Themed Workstreams

### Issue Clustering Analysis

34 issues grouped into themes by root cause:

| Theme | Issues | Root Cause | Priority |
|-------|--------|------------|----------|
| 1. Accessibility Critical | 4 | Insufficient WCAG compliance | IMMEDIATE |
| 2. Spacing System | 7 | No unified spacing scale | Foundation |
| 3. Responsive Mobile-First | 7 | Desktop-first CSS approach | Depends on Theme 2 |
| 4. Typography Hierarchy | 7 | Weak differentiation | Independent |
| 5. Interaction Patterns | 3 | Low-visibility affordances | Wave 3 |
| 6. Color System Compliance | 5 | Semantic color misuse | Wave 1 |
| 7. Streamlit Alignment | Matrix | No shared design system | Wave 3 |

---

### THEME 1: ACCESSIBILITY CRITICAL FIXES

**Issues**: UI-002, UI-003, UI-004, UI-013

**Root Cause**: Insufficient attention to WCAG standards during initial design

**Issues Detailed**:
- **UI-002 (Critical)**: Muted text #9ca3af (2.54:1) fails WCAG AA
- **UI-003 (High)**: Collapsed notice #94a3b8 (3:1) below 4.5:1 requirement
- **UI-004 (High)**: Screen readers miss ::after content announcements
- **UI-013 (Low)**: Animation pulses with no prefers-reduced-motion override

**User Impact**: Critical - affects users with low vision, screen reader users, motion sensitivity

**Target State**:
- All text passes WCAG AA (4.5:1 for normal, 3:1 for large text)
- All interactive elements keyboard accessible with proper ARIA
- All dynamic content announced to screen readers
- No motion for users with `prefers-reduced-motion: reduce`

**Material Specifications**:

```css
/* ===================================================================
 * UI-002: Muted Text Contrast Fix (CRITICAL)
 * =================================================================== */

/* Problem: #9ca3af = 2.54:1 contrast on white (WCAG fail) */
/* Solution: #6c7280 = 4.52:1 contrast (WCAG AA pass) */

:root {
  --color-text-muted: #6c7280; /* Was #9ca3af (2.54:1), now 4.52:1 */
}

/* Affected selectors */
.muted-text,
.footer-metadata,
.timestamp,
.project-info a {
  color: var(--color-text-muted);
}

/* Location: docs/_static/custom.css:55 */
/* Impact: ~200 pages (hero paragraphs, footer text, timestamps) */


/* ===================================================================
 * UI-003: Collapsed Code Notice Contrast (HIGH)
 * =================================================================== */

.highlight-collapsed .collapsed-notice {
  color: #6b7280; /* Was #94a3b8 (3:1), now 4.52:1 */
  font-size: 0.9375rem; /* Was 0.85rem for better legibility */
}

/* Location: docs/_static/code-collapse.css:178-182 */


/* ===================================================================
 * UI-004: Screen Reader Accessibility (HIGH)
 * =================================================================== */

/* REMOVE: ::after pseudo-element approach */
.highlight-collapsed .collapsed-notice::after {
  /* DELETE THIS - screen readers can't access pseudo-elements */
}

/* ADD: Real DOM element with proper ARIA */
/* Template change required in Sphinx */

/* New accessible pattern: */
<div class="collapsed-notice" role="status" aria-live="polite">
  <span class="status-text">Code block collapsed.</span>
  <button
    class="expand-button"
    aria-expanded="false"
    aria-controls="code-block-{id}"
    aria-label="Expand code block">
    Expand to view
  </button>
</div>

/* JavaScript to manage aria-expanded state: */
/*
button.addEventListener('click', function() {
  const isExpanded = this.getAttribute('aria-expanded') === 'true';
  this.setAttribute('aria-expanded', !isExpanded);
  this.textContent = isExpanded ? 'Expand to view' : 'Collapse';
});
*/

/* Location: docs/_static/code-collapse.css:177-183 + JS changes */


/* ===================================================================
 * UI-013: Motion Preferences (LOW)
 * =================================================================== */

@media (prefers-reduced-motion: reduce) {
  .admonition-icon-badge {
    animation: none !important;
  }

  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Location: docs/_static/custom.css (add at end) */
```

**Validation Criteria**:
- ✓ Run axe DevTools automated scan (0 violations target)
- ✓ Test with NVDA screen reader (all status changes announced)
- ✓ WebAIM contrast checker on all affected pages (all ≥4.5:1)
- ✓ Manual keyboard navigation test (all interactive elements reachable)
- ✓ Test with prefers-reduced-motion enabled (no animations)

---

### THEME 2: SPACING SYSTEM STANDARDIZATION

**Issues**: UI-005, UI-007, UI-008, UI-009, UI-014, UI-019, UI-030

**Root Cause**: No unified spacing scale; magic numbers (4px, 8px, 12px) used inconsistently

**Issues Detailed**:
- UI-005: Duplicate control bars (48px dead space)
- UI-007: Project info list 4px rhythm (sections blur)
- UI-008: Visual nav cards 12px from Quick Start (modules merge)
- UI-009: Controller nav 60+ links no gutter (overwhelming)
- UI-014: Admonition icon 42px padding (steals 60px horizontal space)
- UI-019: H1 zero leading (first sentence collides)
- UI-030: Pager arrows 8px from text (misaligned affordance)

**User Impact**: Medium - reduces scanability, creates visual clutter, hurts hierarchy

**Target State**:
- Consistent 8px baseline grid throughout
- Tokenized spacing scale: 4/8/12/16/24/32/48px
- Vertical rhythm: H1/H2 24px bottom, paragraphs 16px, lists 8px
- Component spacing uses tokens, zero magic numbers

**Material Specifications**:

```css
/* ===================================================================
 * SPACING SCALE DEFINITION
 * =================================================================== */

:root {
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 12px;
  --spacing-lg: 16px;
  --spacing-xl: 24px;
  --spacing-2xl: 32px;
  --spacing-3xl: 48px;
}


/* ===================================================================
 * UI-005: Remove Duplicate Control Bar (MEDIUM)
 * =================================================================== */

/* TEMPLATE CHANGE: Modify Sphinx template to render master controls once */
/* File: docs/_templates/page.html or docs/conf.py */

.code-blocks-controls {
  margin-bottom: var(--spacing-xl); /* 24px */
}

/* Remove duplicate rendering logic in template */


/* ===================================================================
 * UI-007: Project Information List Spacing (MEDIUM)
 * =================================================================== */

.project-info ul {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm); /* 8px between items */
}

.project-info li + li {
  margin-top: var(--spacing-md); /* 12px between groups */
}

/* Location: docs/_static/custom.css (hero section) */


/* ===================================================================
 * UI-008: Visual Navigation Card Spacing (LOW)
 * =================================================================== */

.visual-nav-cards {
  margin-top: var(--spacing-xl); /* 24px from Quick Start */
}


/* ===================================================================
 * UI-009: Controllers Navigation Columns (MEDIUM)
 * =================================================================== */

.controller-quick-nav {
  column-count: 2;
  column-gap: var(--spacing-xl); /* 24px gutter */
}


/* ===================================================================
 * UI-014: Admonition Icon Padding (LOW)
 * =================================================================== */

.admonition {
  padding-left: var(--spacing-lg); /* 16px instead of 42px */
}

.admonition-icon-badge {
  left: calc(var(--spacing-lg) * -0.5); /* Position relative to new padding */
}


/* ===================================================================
 * UI-019: H1 Leading (LOW)
 * =================================================================== */

h1 {
  margin-bottom: var(--spacing-xl); /* 24px */
}


/* ===================================================================
 * UI-030: Pager Arrow Spacing (LOW)
 * =================================================================== */

.footer-pager a {
  display: flex;
  align-items: center;
  gap: var(--spacing-md); /* 12px between arrow and text */
}


/* ===================================================================
 * VERTICAL RHYTHM BASELINE GRID (8px)
 * =================================================================== */

h1, h2, h3, h4, h5, h6 {
  margin-bottom: var(--spacing-xl); /* 24px (3 × 8px) */
}

p, ul, ol {
  margin-bottom: var(--spacing-lg); /* 16px (2 × 8px) */
}

li {
  margin-bottom: var(--spacing-xs); /* 4px (0.5 × 8px) */
}
```

**Validation Criteria**:
- ✓ All spacing values use tokens (grep for `px` values, should only be in token definitions)
- ✓ Vertical rhythm follows 8px grid (measure with browser devtools)
- ✓ Visual regression test (compare before/after screenshots)
- ✓ No duplicate control bars (test on pages with code blocks)

---

### THEME 3: RESPONSIVE MOBILE-FIRST OVERHAUL

**Issues**: UI-018, UI-020, UI-021, UI-022, UI-023, UI-024, UI-025

**Root Cause**: Desktop-first CSS approach with insufficient mobile optimization

**Issues Detailed**:
- UI-020: H1 word-break at 320px ("Documenta-tion")
- UI-021: Collapse/Expand buttons stack 0px gap (malformed appearance)
- UI-022: Visual nav 2-column at 320px (4-line labels)
- UI-023: Footer metadata 3-line wrap, zero leading
- UI-024: Tablet icon grid 3-column (collision with margin)
- UI-025: Tablet anchor list desktop font-size (dominates mid-page)
- UI-018: Controllers nav full viewport width (>120 char horizontal travel)

**User Impact**: High - 40%+ of users on mobile devices get degraded experience

**Target State**:
- 320px mobile: Single column, readable text, no word breaks, stacked controls
- 768px tablet: Optimized two-column, collapsible sidebar, adjusted typography
- 1024px+ desktop: Full three-column with anchor rail

**Material Specifications**:

```css
/* ===================================================================
 * BREAKPOINT DEFINITIONS
 * =================================================================== */

:root {
  --breakpoint-mobile: 320px;
  --breakpoint-tablet: 768px;
  --breakpoint-desktop: 1024px;
}


/* ===================================================================
 * UI-020: Mobile H1 Hyphenation (HIGH)
 * =================================================================== */

@media (max-width: 375px) {
  h1.page-title {
    word-break: normal;              /* Reset aggressive breaking */
    overflow-wrap: break-word;       /* Break only at word boundaries */
    hyphens: auto;                   /* Prefer hyphenation */
    -webkit-hyphens: auto;           /* Safari support */
    -ms-hyphens: auto;               /* Legacy Edge support */
    max-width: calc(100vw - var(--spacing-2xl)); /* 32px total padding */
    font-size: 1.875rem;             /* 30px - slightly smaller on mobile */
  }
}

/* Prerequisite: Ensure <html lang="en"> is set for hyphenation dictionary */


/* ===================================================================
 * UI-021: Mobile Button Stack Spacing (MEDIUM)
 * =================================================================== */

@media (max-width: 480px) {
  .code-controls {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm); /* 8px between buttons */
  }
}


/* ===================================================================
 * UI-022: Mobile Visual Navigation Single Column (HIGH)
 * =================================================================== */

@media (max-width: 480px) {
  .visual-nav-cards {
    grid-template-columns: 1fr; /* Single column */
    gap: var(--spacing-lg); /* 16px between cards */
  }
}


/* ===================================================================
 * UI-023: Mobile Footer Metadata Spacing (MEDIUM)
 * =================================================================== */

@media (max-width: 480px) {
  .footer-metadata {
    line-height: 1.5; /* Was ~1.1 */
    margin-bottom: var(--spacing-md); /* 12px */
  }
}


/* ===================================================================
 * UI-024: Tablet Icon Grid 2-Column (MEDIUM)
 * =================================================================== */

@media (max-width: 768px) {
  .visual-nav-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-lg); /* 16px gutter */
    padding: 0 var(--spacing-lg); /* Prevent margin collision */
  }
}


/* ===================================================================
 * UI-025: Tablet Anchor Rail Font Size (LOW)
 * =================================================================== */

@media (max-width: 1023px) {
  .page-toc {
    font-size: 0.875rem; /* 14px instead of 16px */
  }
}


/* ===================================================================
 * UI-018: Controllers Navigation Max-Width (MEDIUM)
 * =================================================================== */

.controller-quick-nav {
  max-width: 80ch; /* ~120 characters */
  column-count: 2;
}

@media (max-width: 768px) {
  .controller-quick-nav {
    column-count: 1; /* Single column on tablet */
  }
}
```

**Validation Criteria**:
- ✓ Test on real devices (iPhone SE 320px, iPad 768px, desktop 1024px+)
- ✓ Visual regression at all 3 breakpoints
- ✓ No word-breaking on mobile H1 titles
- ✓ Readable labels on mobile navigation cards (max 2 lines)
- ✓ No horizontal scroll at any breakpoint

---

### THEME 4: TYPOGRAPHY HIERARCHY REFINEMENT

**Issues**: UI-006, UI-011, UI-016, UI-017, UI-028, UI-032, UI-034

**Root Cause**: Weak typographic hierarchy, insufficient differentiation between levels

**Issues Detailed**:
- UI-006: Status badge uppercase + 0.8px letter-spacing (drops legibility)
- UI-011: Coverage table 11px text (requires zoom)
- UI-016: Step numbers plain paragraphs (ordered workflow hard to follow)
- UI-017: Bullets wrap flush under glyph (ragged left edge)
- UI-028: Quick ref cards rely on underlines alone (titles disappear)
- UI-032: Controllers breadcrumb full sentence titles (3-line wrap)
- UI-034: Hero bullets mix bold + body on same line (awkward breaks)

**User Impact**: Medium - reduces scanability, increases cognitive load

**Material Specifications**:

```css
/* ===================================================================
 * UI-006: Status Badge Readability (MEDIUM)
 * =================================================================== */

.status-badge {
  text-transform: none; /* Remove uppercase */
  font-size: 0.875rem; /* Was 0.75rem */
  letter-spacing: normal; /* Remove 0.8px spacing */
  font-weight: 500; /* Add medium weight for emphasis */
}


/* ===================================================================
 * UI-011: Coverage Table Legibility (MEDIUM)
 * =================================================================== */

.coverage-matrix table {
  font-size: 0.9375rem; /* 15px instead of 11px */
}


/* ===================================================================
 * UI-016: Enumerated Instruction Steps (LOW)
 * =================================================================== */

.instruction-step {
  font-weight: 700;
  font-size: 1.125rem; /* Larger than body */
  margin-bottom: var(--spacing-sm);
  display: block; /* Force line break after number */
}


/* ===================================================================
 * UI-017: Hanging Bullet Indent (MEDIUM)
 * =================================================================== */

.content ul {
  list-style-position: outside;
  padding-left: 1.5em;
}

.content li {
  text-indent: -1.5em;
  padding-left: 1.5em;
}


/* ===================================================================
 * UI-028: Quick Reference Card Headings (LOW)
 * =================================================================== */

.quick-ref-card h3 {
  font-weight: 700;
  border-bottom: 2px solid var(--color-primary);
  padding-bottom: var(--spacing-xs);
  margin-bottom: var(--spacing-md);
}


/* ===================================================================
 * UI-032: Breadcrumb Title Truncation (LOW)
 * =================================================================== */

.footer-pager a {
  max-width: 40ch; /* Limit to ~60 characters */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}


/* ===================================================================
 * UI-034: Hero Feature Bullets Separation (LOW)
 * =================================================================== */

.hero-features li strong {
  display: block; /* Force label to own line */
  margin-bottom: var(--spacing-xs);
}
```

**Validation Criteria**:
- ✓ Visual hierarchy clear (H1 > H2 > H3 > body > caption)
- ✓ Table text readable without zoom (test at 100% browser zoom)
- ✓ Bullets align properly (hanging indent visible)
- ✓ Status badges readable on mobile

---

### THEME 5: INTERACTION PATTERNS IMPROVEMENT

**Issues**: UI-001, UI-026, UI-033

**Root Cause**: Low-visibility affordances, missing state indicators

**Issues Detailed**:
- UI-001: Code collapse button 30% opacity (nearly invisible)
- UI-026: Anchor rail active section only changes weight (can't quickly locate)
- UI-033: Coverage table no sticky header or filters (scroll without context)

**User Impact**: Medium - reduces discoverability, hurts navigation

**Material Specifications**:

```css
/* ===================================================================
 * UI-001: Code Collapse Affordance (MEDIUM)
 * =================================================================== */

.code-collapse-button {
  opacity: 0.6; /* Was 0.3 */
  transition: opacity 0.2s ease;
}

.code-collapse-button:hover,
.code-collapse-button:focus {
  opacity: 1.0;
}

/* Add text label for clarity */
.code-collapse-button::before {
  content: "Collapse";
  font-size: 0.75rem;
  margin-right: var(--spacing-xs);
}

.highlight-collapsed .code-collapse-button::before {
  content: "Expand";
}


/* ===================================================================
 * UI-026: Anchor Rail Active State (MEDIUM)
 * =================================================================== */

.page-toc a.active {
  color: var(--color-primary);
  font-weight: 700;
  border-left: 3px solid var(--color-primary);
  padding-left: calc(var(--spacing-sm) - 3px); /* Compensate for border */
  background-color: var(--color-primary-light);
}


/* ===================================================================
 * UI-033: Coverage Table Sticky Header (MEDIUM)
 * =================================================================== */

.coverage-matrix table thead {
  position: sticky;
  top: 0;
  z-index: 10;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

**Validation Criteria**:
- ✓ Code collapse button visible before hover (opacity ≥0.6)
- ✓ Active anchor highlighted with color + border (not just weight)
- ✓ Table header stays visible when scrolling

---

### THEME 6: COLOR SYSTEM COMPLIANCE

**Issues**: UI-003, UI-010, UI-012, UI-027, UI-031

**Root Cause**: Inconsistent semantic color usage, insufficient contrast

**Issues Detailed**:
- UI-003: Collapsed notice contrast (covered in Theme 1)
- UI-010: Quick nav uses brand red for neutral links (palette conflict)
- UI-012: Table header 4% luminance difference (boundaries disappear)
- UI-027: Back-to-top button shadow too subtle (blends with background)
- UI-031: Gradient callouts white text on pastel (3.3:1 contrast)

**User Impact**: Medium - affects readability, creates confusion

**Material Specifications**:

```css
/* ===================================================================
 * UI-010: Quick Navigation Link Color (MEDIUM)
 * =================================================================== */

.controller-quick-nav a {
  color: var(--color-primary); /* Use primary blue, not error red */
}


/* ===================================================================
 * UI-012: Table Header Contrast (LOW)
 * =================================================================== */

.coverage-matrix table thead {
  background: #e5e7eb; /* Was #f3f4f6 */
  border-bottom: 2px solid #d1d5db; /* Stronger separator */
}

.coverage-matrix table tbody tr:nth-child(even) {
  background: #f9fafb; /* Increase zebra stripe contrast */
}


/* ===================================================================
 * UI-027: Back-to-Top Button Shadow (LOW)
 * =================================================================== */

.back-to-top {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* Was 0 2px 10px rgba(0,0,0,0.3) */
}


/* ===================================================================
 * UI-031: Callout Accessible Contrast (MEDIUM)
 * =================================================================== */

.callout-info {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: #ffffff; /* Ensure 4.5:1 on darkest gradient point */
}

/* Alternative: Use dark text on light background */
.callout-info-alt {
  background: #e6ebf5;
  color: #1e40af; /* 7:1 contrast ratio */
}
```

**Validation Criteria**:
- ✓ All semantic colors used consistently (error=red, warning=orange, success=green, info=blue)
- ✓ All color combinations pass WCAG AA (WebAIM checker)
- ✓ Links use primary color, not error red
- ✓ Table boundaries visible with 4%+ luminance difference

---

### THEME 7: STREAMLIT ALIGNMENT

**Issues**: Consistency matrix findings

**Root Cause**: Streamlit uses default theme; no shared design system with Sphinx docs

**Issues from Consistency Matrix**:
- Primary buttons: Sphinx uses gradient blue, Streamlit uses grey
- Sidebar: Different spacing rhythm and hover states
- Code theme: Sphinx navy theme, Streamlit default light
- Metrics: Sphinx gradient badges, Streamlit default white cards
- Downloads: Sphinx branded pill buttons, Streamlit standard grey
- Spacing: Sphinx 4/8/12/16/24px, Streamlit default ~12/16px

**User Impact**: Low (separate surfaces) but hurts brand consistency

**Material Specifications**:

**1. Create `.streamlit/config.toml`**:

```toml
[theme]
primaryColor = "#0b2763"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f9fafb"
textColor = "#111827"
font = "sans serif"
```

**2. Create `streamlit_custom.css` and inject**:

```python
# streamlit_app.py
import streamlit as st

def load_custom_css():
    """Inject custom CSS to match Sphinx documentation styling"""
    css = """
    <style>
    /* Match Sphinx spacing scale */
    :root {
        --spacing-xs: 4px;
        --spacing-sm: 8px;
        --spacing-md: 12px;
        --spacing-lg: 16px;
        --spacing-xl: 24px;
    }

    /* Primary button styling to match docs */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        border: none;
        font-weight: 500;
        transition: transform 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
    }

    /* Sidebar spacing to match docs */
    .css-1d391kg {
        padding-top: var(--spacing-sm);
        padding-bottom: var(--spacing-sm);
    }

    /* Metric tiles with gradient headers */
    .stMetric {
        background: white;
        border-radius: 8px;
        padding: var(--spacing-lg);
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .stMetric label {
        background: linear-gradient(135deg, #0b2763 0%, #08204d 100%);
        color: white;
        padding: var(--spacing-xs) var(--spacing-sm);
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        border: none;
        font-weight: 500;
    }

    /* Code blocks to match Sphinx navy theme */
    .stCodeBlock {
        background: #1e293b;
        border-radius: 8px;
    }

    .stCodeBlock code {
        color: #e2e8f0;
        font-family: 'SFMono-Regular', Menlo, Consolas, monospace;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Call at app initialization
if __name__ == "__main__":
    load_custom_css()
    # Rest of Streamlit app...
```

**Validation Criteria**:
- ✓ Streamlit primary color matches Sphinx (#0b2763)
- ✓ Button gradients match across surfaces
- ✓ Spacing follows same 4/8/12/16/24px scale
- ✓ Code blocks use similar dark theme
- ✓ Metrics styled consistently with documentation badges

---

<a name="three-wave-strategy"></a>
## Three-Wave Implementation Strategy

### Wave 1: Foundations (Parallel Execution)

**Themes**: Accessibility (1), Color (6), Spacing (2)

**Rationale**: These are foundational - no dependencies, can work in parallel

**Tasks**:
- Update design tokens (colors, spacing)
- Implement WCAG fixes
- Establish spacing scale

**Duration**: Week 1 (Days 1-5)

**Deliverables**:
- Updated design tokens
- WCAG compliant colors
- 8px baseline grid implemented

---

### Wave 2: Typography & Responsive (Sequential)

**Themes**: Typography (4), Responsive (3)

**Rationale**: Both depend on Wave 1 spacing tokens

**Tasks**:
- Implement type scale
- Create responsive breakpoints
- Test across viewports

**Duration**: Week 2 (Days 6-10)

**Deliverables**:
- Typography hierarchy clear
- Mobile/tablet/desktop responsive
- Visual regression tests passing

---

### Wave 3: Interactions & Streamlit (Final Integration)

**Themes**: Interaction (5), Streamlit (7)

**Rationale**: Requires stable design system from Waves 1-2

**Tasks**:
- Enhanced interaction patterns
- Streamlit theme alignment
- Cross-surface validation

**Duration**: Week 3 (Days 11-15)

**Deliverables**:
- Interaction improvements live
- Streamlit matches Sphinx brand
- Complete design system validated

---

<a name="deliverables"></a>
## Four Major Deliverables

### Deliverable 1: Design Token System v2

**Files**: `.codex/phase2_remediation/design_tokens_v2.{json,css,md}`

**JSON Structure**:
```json
{
  "version": "2.0.0",
  "colors": {
    "primary": "#0b2763",
    "primary_hover": "#08204d",
    "primary_light": "#e6ebf5",
    "text_primary": "#111827",
    "text_secondary": "#6b7280",
    "text_muted": "#6c7280",
    "text_muted_accessible": "#6c7280",
    "background_primary": "#ffffff",
    "background_secondary": "#f9fafb",
    "border": "#e5e7eb",
    "info": "#3b82f6",
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444"
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "12px",
    "lg": "16px",
    "xl": "24px",
    "2xl": "32px",
    "3xl": "48px"
  },
  "typography": {
    "family_body": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "family_mono": "'SFMono-Regular', Menlo, Consolas, monospace",
    "scale": {
      "h1": { "size": "2.25rem", "weight": 700, "line_height": 1.2 },
      "h2": { "size": "1.75rem", "weight": 700, "line_height": 1.3 },
      "h3": { "size": "1.5rem", "weight": 700, "line_height": 1.4 },
      "body": { "size": "1rem", "weight": 400, "line_height": 1.6 },
      "small": { "size": "0.875rem", "weight": 400, "line_height": 1.5 }
    }
  },
  "breakpoints": {
    "mobile": "320px",
    "tablet": "768px",
    "desktop": "1024px"
  },
  "shadows": {
    "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1)"
  },
  "motion": {
    "duration_fast": "150ms",
    "duration_normal": "250ms",
    "duration_slow": "350ms",
    "easing_default": "cubic-bezier(0.4, 0.0, 0.2, 1)"
  }
}
```

**CSS Custom Properties**:
```css
:root {
  /* Colors */
  --color-primary: #0b2763;
  --color-primary-hover: #08204d;
  --color-primary-light: #e6ebf5;
  --color-text-primary: #111827;
  --color-text-secondary: #6b7280;
  --color-text-muted: #6c7280;
  --color-background-primary: #ffffff;
  --color-background-secondary: #f9fafb;
  --color-border: #e5e7eb;

  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 12px;
  --spacing-lg: 16px;
  --spacing-xl: 24px;
  --spacing-2xl: 32px;
  --spacing-3xl: 48px;

  /* Breakpoints */
  --breakpoint-mobile: 320px;
  --breakpoint-tablet: 768px;
  --breakpoint-desktop: 1024px;
}
```

---

### Deliverable 2: Theme Remediation Specs (7 Documents)

Each spec document includes:
- Problem Statement (issue IDs, user impact, metrics)
- Design Rationale (why this solution, alternatives, trade-offs)
- Material Specifications (exact CSS/markup)
- Validation Criteria (test methods, success metrics)
- Future Considerations (limitations, enhancements)

**Files**:
- `theme_01_accessibility.md`
- `theme_02_spacing.md`
- `theme_03_responsive.md`
- `theme_04_typography.md`
- `theme_05_interaction.md`
- `theme_06_color.md`
- `theme_07_streamlit.md`

---

### Deliverable 3: Annotated Visual Mockups (15-20 images)

For each theme, create 2-3 annotated screenshots:

**Annotation Strategy**:
- Red overlays = problems (with measurements, ratios)
- Green overlays = solutions (with corrected values)
- Side-by-side before/after comparisons

**Example Mockups**:
- Accessibility: Contrast ratio overlays (#9ca3af 2.54:1 ✗ → #6c7280 4.52:1 ✓)
- Spacing: Measurement overlays (4px blur → 8px rhythm)
- Responsive: Mobile 2-column squeeze → single column readable
- Typography: Hierarchy weak → clear differentiation
- Interaction: Invisible button (30% opacity) → visible (60% opacity)
- Color: Red links → blue primary color
- Streamlit: Grey buttons → gradient blue

**Tools**: Python + Pillow for automated overlays, manual Figma for complex annotations

---

### Deliverable 4: Implementation Roadmap

**File**: `.codex/phase2_remediation/IMPLEMENTATION_ROADMAP.md`

**Structure**:

```markdown
# Phase 3 Implementation Roadmap

## Priority 1: Critical Fixes (Week 1)
- [ ] UI-002: Muted text contrast (2hr) - WCAG compliance
- [ ] UI-003: Collapsed notice contrast (1hr)
- [ ] UI-004: Screen reader accessibility (3hr)

## Priority 2: High-Impact Fixes (Week 2)
- [ ] UI-020: Mobile H1 word-break (2hr)
- [ ] UI-022: Mobile visual nav single column (2hr)
- [ ] UI-001: Code collapse affordance (3hr)

## Priority 3: Medium Fixes (Week 3-4)
- [ ] UI-005: Duplicate control bar (4hr)
- [ ] UI-007: Project info spacing (1hr)
- [ ] UI-009: Controller nav columns (2hr)
- [ ] ... (remaining medium issues)

## Priority 4: Low-Priority Polish (Week 5+)
- [ ] UI-008: Visual nav card spacing (1hr)
- [ ] UI-013: Motion preferences (1hr)
- [ ] ... (remaining low issues)

## Dependencies
- Responsive theme depends on spacing system completion
- Streamlit alignment depends on Sphinx design system stabilization

## Validation Gates
- After Priority 1: WCAG audit (all Critical + High pass)
- After Priority 2: Mobile device testing (real devices)
- After Priority 3: Visual regression suite (20 key pages)
- After Priority 4: Stakeholder final approval

## Rollback Strategy
- Git tags for each priority level
- Individual theme rollback capability
- Token versioning for breaking changes
```

---

<a name="quick-wins"></a>
## Quick Wins Strategy (Proof of Concept)

Execute during Week 2 to demonstrate value:

### Quick Win 1: Muted Text Contrast (UI-002 Critical)

**Effort**: 1hr implementation + 1hr testing = 2hr total

**Change**: Update `--color-text-muted: #6c7280` in `custom.css:55`

**Validation**:
- WebAIM contrast checker (before: 2.54:1 → after: 4.52:1)
- Screenshot comparison of hero text

**Risk**: Low - simple CSS variable change

**Impact**: Resolves Critical accessibility issue immediately

---

### Quick Win 2: Code Collapse Affordance (UI-001, UI-004)

**Effort**: 3hr implementation + 2hr testing = 5hr total

**Changes**:
1. Increase button opacity 0.3 → 0.6 in `code-collapse.css:79`
2. Add `aria-expanded="false"` to button element
3. Replace ::after pseudo-element with visible DOM element
4. Add JavaScript for ARIA state management

**Validation**:
- NVDA screen reader test
- Keyboard navigation test
- Visual check on 234 code blocks

**Risk**: Medium - requires JavaScript changes

**Impact**: Resolves 1 Medium + 1 High issue, improves accessibility significantly

---

### Quick Win 3: Duplicate Control Bar (UI-005)

**Effort**: 4hr implementation + 3hr testing = 7hr total

**Change**: Modify Sphinx template logic to render master controls once

**Validation**:
- Visual regression test on all 234 code blocks
- Screenshots showing recovered 48px space

**Risk**: Medium - affects critical interactive feature

**Impact**: Improves above-fold space, cleaner UX

---

**Total Quick Wins**: 14 hours resolves 1 Critical + 1 High + 2 Medium (4 of 34 issues)

---

<a name="timeline"></a>
## 3-Week Timeline

### Week 1: Foundation (Days 1-5)

**Day 1-2**: Develop design token system v2
- Output: `design_tokens_v2.{json,css,md}`
- Milestone: Token system ready for review

**Day 3-4**: Write theme specs 1-4
- Accessibility, Spacing, Responsive, Typography
- Milestone: 4 of 7 theme specs completed

**Day 5**: Write theme specs 5-7
- Interaction, Color, Streamlit
- Milestone: All 7 specs documented
- Deliverable: `.codex/phase2_remediation/theme_specs/` complete

---

### Week 2: Visualization + Proof (Days 6-10)

**Day 6-8**: Create annotated mockups
- 2-3 per theme (~18 total)
- Automate with Python + Pillow
- Manual Figma for complex annotations
- Milestone: All mockups ready for review

**Day 9-10**: Implement 3 quick wins on staging
- Quick Win 1: Muted text contrast (2hr)
- Quick Win 2: Code collapse affordance (5hr)
- Quick Win 3: Duplicate control bar (7hr)
- Milestone: Quick wins live, evidence collected
- Deliverable: `QUICK_WINS_REPORT.md`

---

### Week 3: Validation + Roadmap (Days 11-15)

**Day 11-13**: Stakeholder review cycles (parallel)
- Design tokens review (2-day window)
- Theme specs review (2-day window)
- Mockups visual review (2-day window)
- Quick wins demonstration (live walkthrough)
- Collect feedback, iterate as needed

**Day 14-15**: Finalize implementation roadmap
- Incorporate stakeholder feedback
- Prioritize tasks (Critical → High → Medium → Low)
- Estimate effort (S/M/L per task)
- Map dependencies and critical path
- Define Phase 3 success criteria
- Deliverable: `IMPLEMENTATION_ROADMAP.md` complete

---

**Total Duration**: 15 work days (3 calendar weeks with buffer)

**Critical Path**: Theme specs → Mockups → Stakeholder validation → Roadmap

---

<a name="resources"></a>
## Resource Requirements

### Primary Team

**1. UX Designer (Lead)** - 60-80 hours
- Design token system architecture
- Material spec authoring (all 7 themes)
- Mockup creation and annotation
- Stakeholder communication
- Required skills: Design systems, WCAG accessibility, responsive design

**2. Frontend Developer** - 20-30 hours
- Quick wins implementation (14hr)
- Feasibility review of CSS/JS changes
- Validation tooling setup
- Risk assessment
- Required skills: CSS, JavaScript, Sphinx theming, Streamlit

**3. Accessibility Specialist** - 10-15 hours (can be consultant)
- Review accessibility theme specs
- WCAG compliance validation
- Screen reader testing recommendations
- Color contrast verification
- Required skills: WCAG 2.1 AA standards, assistive technology

**4. Stakeholder/Product Owner** - 15-20 hours
- Review cycles for all deliverables
- Brand consistency verification
- Priority decisions and trade-offs
- Final approval authority

---

### Optional Support

**5. Visual Designer** - 10-15 hours
- Polish annotated mockups
- Create branded documentation templates

**6. Technical Writer** - 5-10 hours
- Review theme spec clarity
- Ensure documentation standards

---

**Total Effort**: 110-150 hours across 3 weeks

**Peak Load**: Week 2 (mockup creation + quick wins)

**Budget**: $0 tooling, optional $2-5k for external WCAG audit

---

<a name="risks"></a>
## Risk Mitigation Framework

### Risk 1: Breaking Existing Functionality

**Concern**: CSS/JS changes break code collapse, navigation, search

**Mitigation**:
- Automated visual regression tests (20 key pages before/after)
- Playwright end-to-end tests for interactive features
- Test across 3 viewports (320px, 768px, 1024px)
- Manual QA checklist for critical paths

**Validation**: All existing Playwright tests must pass + new regression suite

**Rollback**: Git tags for each wave, ability to revert individual themes

---

### Risk 2: Brand Identity Dilution

**Concern**: Color/typography changes weaken brand recognition

**Mitigation**:
- Maintain primary brand color #0b2763 for all key elements
- Adjust only secondary/supporting colors for accessibility
- Keep logo, main navigation, hero consistently branded
- Stakeholder visual review at Week 3 Day 11

**Validation**: Brand guidelines checklist, stakeholder sign-off

---

### Risk 3: Performance Degradation

**Concern**: Additional CSS/JS increases page load time

**Mitigation**:
- Minify and combine CSS files
- Lazy-load non-critical features
- Monitor bundle size (target: <5% increase)
- Use CSS containment for layout

**Validation**: Lighthouse performance score must remain ≥90

**Monitoring**: Track Core Web Vitals (LCP, FID, CLS)

---

### Risk 4: Cross-Browser Compatibility

**Concern**: Modern CSS features fail in older browsers

**Mitigation**:
- Test in Chrome, Firefox, Safari, Edge (latest 2 versions)
- Use CSS fallbacks for grid/flexbox edge cases
- Verify mobile Safari rendering (iOS-specific issues)
- Progressive enhancement approach

**Validation**: Manual testing matrix across 4 browsers × 3 viewports

**Tools**: BrowserStack for automated screenshots

---

### Risk 5: Streamlit Alignment Breaking

**Concern**: Shared tokens create conflicts in Streamlit app

**Mitigation**:
- Test Streamlit theme changes in isolation first
- Use scoped CSS to avoid conflicts
- Fallback to Streamlit defaults if issues arise
- Document which tokens are shared vs. surface-specific

**Validation**: Streamlit app functional testing after each theme

**Escape Hatch**: Theme 7 is optional, can defer to later phase

---

### Risk 6: Timeline Slippage

**Concern**: 3 weeks may be optimistic for 7 themes + validation

**Mitigation**:
- Built-in buffer: 15 work days = 3 calendar weeks allows weekends
- Stakeholder review windows: 2-3 days each (realistic)
- Quick wins parallel to mockup creation (don't block critical path)
- Defer Theme 7 (Streamlit) if schedule pressure

**Monitoring**: Daily standup to track progress vs. plan

**Contingency**: Extend Week 3 by 2-3 days if needed (acceptable slippage)

---

<a name="communication"></a>
## Stakeholder Communication Plan

### Week 1 Kickoff (Day 1)

**Medium**: Email + project management tool

**Content**:
- Phase 2 objectives
- 3-week timeline
- Team roles
- Deliverables preview

**Call to Action**: Set expectations for review cycles (2-3 days each)

---

### Week 1 Check-in (Day 3)

**Medium**: Slack + shared design doc

**Content**: Early design token draft for preliminary feedback

**Purpose**: Surface concerns before deep work invested

**Duration**: 15-minute sync call

---

### Week 2 Major Review (Day 8)

**Medium**: Video walkthrough + written documentation package

**Content**:
- Complete design tokens
- All 7 theme specs
- First mockup drafts

**Format**: 30-minute recorded walkthrough + 3-day async review window

**Request**: Technical feasibility (developers), visual/brand review (stakeholders)

---

### Week 2 Quick Wins Demo (Day 10)

**Medium**: Live staging environment demo

**Content**: 3 quick wins with before/after evidence

**Purpose**: Proof that approach works, build confidence

**Format**: 15-minute live demo + Q&A

---

### Week 3 Final Review (Day 13)

**Medium**: Presentation meeting (in-person or video)

**Content**: All final deliverables, implementation roadmap

**Decision**: Phase 3 go/no-go

**Format**: 60-minute presentation + Q&A + decision

---

### Week 3 Handoff (Day 15)

**Medium**: Documentation package + transition meeting

**Content**: Formal handoff to Phase 3 team

**Deliverables**: Complete documentation, success criteria, support plan

**Retrospective**: What worked, what to improve

---

**Change Management Messaging**:
- **Frame**: "User-centered improvements backed by data (34 documented issues)"
- **Address concerns**: "Quick wins prove approach, comprehensive risk mitigation"
- **Build buy-in**: "Accessibility compliance protects organization legally and ethically"

---

<a name="success-criteria"></a>
## Success Criteria

### Quantitative Metrics

1. ✓ All 34 issues have documented remediation concepts
2. ✓ 100% of Critical (1) + High (4) issues have implementation-ready material specs
3. ✓ Design token system covers all 15+ token categories
4. ✓ Minimum 15 annotated mockups created (2+ per major theme)
5. ✓ All proposed color changes pass WCAG AA (4.5:1 normal, 3:1 large)
6. ✓ Quick wins demonstrate measurable improvement (contrast ratios documented)
7. ✓ Stakeholder sign-off received on all deliverables

---

### Qualitative Criteria

1. ✓ Design decisions traceable to specific Phase 1 issues
2. ✓ Material specs specific enough for Phase 3 (no ambiguity)
3. ✓ Mockups clearly communicate problem → solution
4. ✓ Design system maintains brand consistency
5. ✓ Token system extensible for future components
6. ✓ Remediation addresses root causes, not symptoms
7. ✓ Cross-surface consistency (Sphinx + Streamlit) achievable

---

### Deliverable Completeness Checklist

- [ ] `design_tokens_v2.json` (machine-readable)
- [ ] `design_tokens_v2.css` (CSS custom properties)
- [ ] `design_tokens_v2.md` (human documentation)
- [ ] `theme_specs/theme_01_accessibility.md`
- [ ] `theme_specs/theme_02_spacing.md`
- [ ] `theme_specs/theme_03_responsive.md`
- [ ] `theme_specs/theme_04_typography.md`
- [ ] `theme_specs/theme_05_interaction.md`
- [ ] `theme_specs/theme_06_color.md`
- [ ] `theme_specs/theme_07_streamlit.md`
- [ ] 15+ annotated mockup images in `mockups/`
- [ ] `QUICK_WINS_REPORT.md` with evidence
- [ ] `IMPLEMENTATION_ROADMAP.md` with prioritized tasks
- [ ] `PHASE2_COMPLETION_REPORT.md` summarizing decisions

---

**Gate**: No progression to Phase 3 until:
- All checklist items complete
- All quantitative metrics met
- All qualitative criteria satisfied
- Stakeholder approval received (documented sign-off)

---

## Appendix: File Locations

### Phase 1 Input
- `.codex/phase1_audit/PHASE1_COMPLETION_REPORT.md`
- `.codex/phase1_audit/phase1_issue_backlog.md`
- `.codex/phase1_audit/phase1_component_inventory.csv`
- `.codex/phase1_audit/DESIGN_SYSTEM.md`
- `.codex/phase1_audit/phase1_consistency_matrix.md`

### Existing Code
- `docs/_static/custom.css`
- `docs/_static/code-collapse.css`
- `docs/_static/css-themes/base-theme.css`
- `streamlit_app.py`

### Phase 2 Output
- `.codex/phase2_remediation/` (all deliverables)

---

**This plan provides a strategic, phased approach to UI/UX remediation with clear deliverables, timeline, and success criteria.**
