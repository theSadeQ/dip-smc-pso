# Phase 2 Context Links - File Navigation Guide

> **Purpose**: Quick file path reference for Phase 2 enhancement work
>
> **For**: Rapid navigation to source files and data
>
> **Base Directory**: `D:\Projects\main\`

---

## This Package (Phase 2 Plan)

**Location**: `.codex/phase2_plan/`

| File | Purpose | Size | Priority |
|------|---------|------|----------|
| `README.md` | Mission brief & orientation | ~300 lines | ⭐ Start here |
| `PHASE2_COMPLETE_PLAN.md` | Full detailed Phase 2 plan | ~1000 lines | ⭐ Read second |
| `ENHANCEMENT_MISSION.md` | Deep-dive task instructions | ~600 lines | ⭐ Read third |
| `QUICK_REFERENCE.md` | TL;DR cheat sheet | ~150 lines | Use during work |
| `CONTEXT_LINKS.md` | This file - navigation guide | ~100 lines | Use for lookup |

---

## Phase 1 Audit Results (INPUT DATA)

**Location**: `.codex/phase1_audit/`

### Primary Documents (READ THESE FIRST)

| File | Description | Lines | Contains |
|------|-------------|-------|----------|
| `PHASE1_COMPLETION_REPORT.md` | Executive summary | ~100 | Stats, top 10 issues, quick wins, next steps |
| `phase1_issue_backlog.md` | Complete issue list | ~200 | All 34 issues with screenshots, locations, severity |
| `DESIGN_SYSTEM.md` | Current design tokens | ~150 | Colors, spacing, typography, effects extracted from CSS |
| `phase1_consistency_matrix.md` | Sphinx vs Streamlit gaps | ~50 | Cross-surface comparison table |

### Detailed Data Files

| File | Description | Format |
|------|-------------|--------|
| `phase1_component_inventory.csv` | 62 components catalogued | CSV (62 rows) |
| `phase1_design_tokens.json` | Machine-readable tokens | JSON |

**Full Paths**:
```
D:\Projects\main\.codex\phase1_audit\PHASE1_COMPLETION_REPORT.md
D:\Projects\main\.codex\phase1_audit\phase1_issue_backlog.md
D:\Projects\main\.codex\phase1_audit\phase1_component_inventory.csv
D:\Projects\main\.codex\phase1_audit\DESIGN_SYSTEM.md
D:\Projects\main\.codex\phase1_audit\phase1_consistency_matrix.md
D:\Projects\main\.codex\phase1_audit\phase1_design_tokens.json
```

---

## Existing Code (INSPECT THESE)

### Critical CSS Files (HIGH PRIORITY)

| File | Description | Lines | Key Content |
|------|-------------|-------|-------------|
| `docs/_static/custom.css` | Main custom styles | ~500 | Design tokens, hero, navigation, callouts |
| `docs/_static/code-collapse.css` | Interactive code blocks | ~200 | Collapse/expand logic, button styles |
| `docs/_static/css-themes/base-theme.css` | Theme foundation | ~800 | Furo theme customizations |

**Full Paths**:
```
D:\Projects\main\docs\_static\custom.css
D:\Projects\main\docs\_static\code-collapse.css
D:\Projects\main\docs\_static\css-themes\base-theme.css
```

**What to Check**:
- `custom.css:55` - `--color-text-muted` token (UI-002 Critical)
- `custom.css:145-150` - H1 styles (UI-020 High)
- `code-collapse.css:79` - Button opacity (UI-001 Medium)
- `code-collapse.css:177-183` - Collapsed notice (UI-004 High)

### JavaScript Files (CHECK DEPENDENCIES)

| File | Description | Check For |
|------|-------------|-----------|
| `docs/_static/js/code-collapse.js` | Code block collapse logic | Event listeners on buttons, ARIA state management |

**Full Path**:
```
D:\Projects\main\docs\_static\js\code-collapse.js
```

### Streamlit App (THEME 7)

| File | Description | Check For |
|------|-------------|-----------|
| `streamlit_app.py` | Main Streamlit application | Theme config, CSS injection, component usage |

**Full Path**:
```
D:\Projects\main\streamlit_app.py
```

---

## Screenshots (VISUAL EVIDENCE)

**Location**: `.codex/screenshots/`

### Critical Issue Screenshots

| Issue | Screenshot | Description |
|-------|------------|-------------|
| UI-002 | `01_documentation/index.png` | Muted text contrast failure on hero |
| UI-003 | `05_test_results/baseline/test_1_3_all_collapsed.png` | Collapsed code notice low contrast |
| UI-004 | `05_test_results/baseline/test_1_3_all_collapsed.png` | Screen reader accessibility issue |
| UI-020 | `05_test_results/baseline/test_6_1_mobile_320px.png` | Mobile H1 word-breaking |
| UI-022 | `05_test_results/baseline/test_6_1_mobile_320px.png` | Mobile visual nav 2-column squeeze |

### Responsive Test Screenshots

| Viewport | Screenshot | Dimensions |
|----------|------------|------------|
| Desktop | `05_test_results/baseline/test_6_1_desktop_1024px.png` | 1024px |
| Tablet | `05_test_results/baseline/test_6_1_tablet_768px.png` | 768px |
| Mobile | `05_test_results/baseline/test_6_1_mobile_320px.png` | 320px |

**Full Paths**:
```
D:\Projects\main\.codex\screenshots\01_documentation\index.png
D:\Projects\main\.codex\screenshots\05_test_results\baseline\test_1_3_all_collapsed.png
D:\Projects\main\.codex\screenshots\05_test_results\baseline\test_6_1_mobile_320px.png
```

### Screenshot Metadata

| File | Description | Format |
|------|-------------|--------|
| `.codex/screenshots/metadata.json` | Complete screenshot index | JSON (~820 screenshots) |

**Full Path**:
```
D:\Projects\main\.codex\screenshots\metadata.json
```

---

## Documentation Source (CONTEXT)

### Sphinx Configuration

| File | Description |
|------|-------------|
| `docs/conf.py` | Sphinx build configuration |
| `docs/_templates/` | Custom Sphinx templates |
| `docs/index.rst` | Main documentation entry point |

**Full Paths**:
```
D:\Projects\main\docs\conf.py
D:\Projects\main\docs\_templates\
D:\Projects\main\docs\index.rst
```

### Built Documentation

| Location | Description |
|----------|-------------|
| `docs/_build/html/` | Generated HTML documentation (~795 pages) |
| `docs/_build/html/_static/` | Copied static assets (CSS, JS, images) |

**Full Paths**:
```
D:\Projects\main\docs\_build\html\
D:\Projects\main\docs\_build\html\_static\
```

---

## Output Directory (CREATE YOUR WORK HERE)

**Location**: `.codex/phase2_audit/`

### Primary Deliverable

| File | Description | Estimated Size |
|------|-------------|----------------|
| `PHASE2_PLAN_ENHANCED.md` | Comprehensive enhanced Phase 2 plan | ~1200 lines |

### Supporting Deliverables

| File | Description | Estimated Size |
|------|-------------|----------------|
| `PHASE1_DEEP_DIVE_ANALYSIS.md` | Enhanced issue analysis with dependencies | ~400 lines |
| `ALTERNATIVE_APPROACHES.md` | Trade-off analysis for major decisions | ~300 lines |
| `RISK_ASSESSMENT_DETAILED.md` | Comprehensive risk matrix (15+ risks) | ~400 lines |
| `IMPLEMENTATION_SEQUENCING_OPTIMIZED.md` | Gantt chart, critical path | ~250 lines |
| `STREAMLIT_ALIGNMENT_SPECIFICATION.md` | Detailed technical spec | ~300 lines |
| `DECISION_LOG.md` | Rationale for each major decision | ~200 lines |
| `EFFORT_IMPACT_MATRIX.md` | All 34 issues scored for prioritization | ~150 lines |
| `BROWSER_COMPATIBILITY_MATRIX.md` | CSS feature support tables | ~200 lines |
| `VALIDATION_PROCEDURES.md` | Step-by-step testing guide | ~250 lines |

**Full Paths** (create these):
```
D:\Projects\main\.codex\phase2_audit\PHASE2_PLAN_ENHANCED.md
D:\Projects\main\.codex\phase2_audit\PHASE1_DEEP_DIVE_ANALYSIS.md
D:\Projects\main\.codex\phase2_audit\ALTERNATIVE_APPROACHES.md
D:\Projects\main\.codex\phase2_audit\RISK_ASSESSMENT_DETAILED.md
D:\Projects\main\.codex\phase2_audit\IMPLEMENTATION_SEQUENCING_OPTIMIZED.md
D:\Projects\main\.codex\phase2_audit\STREAMLIT_ALIGNMENT_SPECIFICATION.md
D:\Projects\main\.codex\phase2_audit\DECISION_LOG.md
D:\Projects\main\.codex\phase2_audit\EFFORT_IMPACT_MATRIX.md
D:\Projects\main\.codex\phase2_audit\BROWSER_COMPATIBILITY_MATRIX.md
D:\Projects\main\.codex\phase2_audit\VALIDATION_PROCEDURES.md
```

---

## Project Root Files (BACKGROUND CONTEXT)

### Project Documentation

| File | Description |
|------|-------------|
| `CLAUDE.md` | Project conventions, team memory, MCP integration |
| `README.md` | Project overview, installation, usage |
| `CHANGELOG.md` | Version history and release notes |

**Full Paths**:
```
D:\Projects\main\CLAUDE.md
D:\Projects\main\README.md
D:\Projects\main\CHANGELOG.md
```

### Configuration

| File | Description |
|------|-------------|
| `config.yaml` | Main simulation configuration |
| `requirements.txt` | Python dependencies |
| `.mcp.json` | MCP server configuration |

**Full Paths**:
```
D:\Projects\main\config.yaml
D:\Projects\main\requirements.txt
D:\Projects\main\.mcp.json
```

---

## Quick File Access (Copy-Paste Paths)

### Phase 1 Data (READ)
```
.codex/phase1_audit/PHASE1_COMPLETION_REPORT.md
.codex/phase1_audit/phase1_issue_backlog.md
.codex/phase1_audit/phase1_component_inventory.csv
.codex/phase1_audit/DESIGN_SYSTEM.md
.codex/phase1_audit/phase1_consistency_matrix.md
```

### Existing CSS (INSPECT)
```
docs/_static/custom.css
docs/_static/code-collapse.css
docs/_static/css-themes/base-theme.css
```

### Critical Issue Locations (QUICK LOOKUP)
```
custom.css:55        → UI-002 (muted text color)
custom.css:145-150   → UI-020 (H1 word-break)
code-collapse.css:79 → UI-001 (button opacity)
code-collapse.css:177-183 → UI-003, UI-004 (collapsed notice)
```

### Screenshots (VISUAL EVIDENCE)
```
.codex/screenshots/01_documentation/index.png
.codex/screenshots/05_test_results/baseline/test_1_3_all_collapsed.png
.codex/screenshots/05_test_results/baseline/test_6_1_mobile_320px.png
.codex/screenshots/05_test_results/baseline/test_6_1_tablet_768px.png
.codex/screenshots/05_test_results/baseline/test_6_1_desktop_1024px.png
```

### Output (CREATE)
```
.codex/phase2_audit/PHASE2_PLAN_ENHANCED.md
.codex/phase2_audit/PHASE1_DEEP_DIVE_ANALYSIS.md
.codex/phase2_audit/ALTERNATIVE_APPROACHES.md
.codex/phase2_audit/RISK_ASSESSMENT_DETAILED.md
.codex/phase2_audit/IMPLEMENTATION_SEQUENCING_OPTIMIZED.md
.codex/phase2_audit/STREAMLIT_ALIGNMENT_SPECIFICATION.md
.codex/phase2_audit/DECISION_LOG.md
.codex/phase2_audit/EFFORT_IMPACT_MATRIX.md
.codex/phase2_audit/BROWSER_COMPATIBILITY_MATRIX.md
.codex/phase2_audit/VALIDATION_PROCEDURES.md
```

---

## Tool Access Commands (If Needed)

### Read Files
```
Read: D:\Projects\main\.codex\phase1_audit\PHASE1_COMPLETION_REPORT.md
Read: D:\Projects\main\docs\_static\custom.css
```

### Search Content
```
Grep: pattern="color-text-muted" path="docs/_static/"
Grep: pattern="word-break" path="docs/_static/custom.css"
```

### List Directories
```
Glob: pattern="*.css" path="docs/_static/"
Glob: pattern="*.png" path=".codex/screenshots/05_test_results/baseline/"
```

---

## Directory Tree (High-Level)

```
D:\Projects\main\
├── .codex/
│   ├── phase1_audit/          # Phase 1 results (INPUT)
│   ├── phase2_plan/           # This package (REFERENCE)
│   ├── phase2_audit/          # Your work (OUTPUT - create this)
│   └── screenshots/           # Visual evidence (~820 images)
├── docs/
│   ├── _static/
│   │   ├── custom.css         # ⚠️ Main styles (UI-002, UI-020)
│   │   ├── code-collapse.css  # ⚠️ Interactive (UI-001, UI-003, UI-004)
│   │   └── css-themes/
│   │       └── base-theme.css # Theme foundation
│   ├── _build/html/           # Generated docs (~795 pages)
│   └── conf.py                # Sphinx config
├── streamlit_app.py           # Streamlit app (Theme 7)
├── CLAUDE.md                  # Project conventions
└── README.md                  # Project overview
```

---

## File Size Reference (Disk Space)

| Location | Approx Size | Content |
|----------|-------------|---------|
| `.codex/phase1_audit/` | ~500 KB | Text reports, CSV, JSON |
| `.codex/phase2_plan/` | ~400 KB | This handoff package (5 files) |
| `.codex/screenshots/` | ~150 MB | 820 PNG images |
| `docs/_static/` | ~5 MB | CSS, JS, images |
| `docs/_build/html/` | ~200 MB | Generated HTML docs |

---

## Related Tools & Resources

### Browser Extensions (For Validation)
- **axe DevTools** - Accessibility testing (free)
- **WebAIM Contrast Checker** - WCAG validation
- **BrowserStack** - Cross-browser testing

### Online Tools
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Can I Use**: https://caniuse.com/ (CSS feature support)
- **MDN Web Docs**: https://developer.mozilla.org/ (CSS reference)

### Documentation
- **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **Streamlit Theme Docs**: https://docs.streamlit.io/library/advanced-features/theming
- **Sphinx Theming**: https://www.sphinx-doc.org/en/master/theming.html

---

**This guide provides all file paths you need for Phase 2 enhancement work. Use it for quick navigation during analysis.**
