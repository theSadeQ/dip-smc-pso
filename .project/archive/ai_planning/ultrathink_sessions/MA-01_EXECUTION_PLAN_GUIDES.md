# MA-01 Execution Plan: docs/guides/ Category Audit

**Date**: November 10, 2025
**Target**: docs/guides/ (User Guides Category)
**Auditor**: Claude Code (Sequential Thinking MCP)
**Duration**: 5 hours
**Priority**: CRITICAL (Primary user-facing documentation)

---

## Rationale

**Why docs/guides/?**
- Primary user-facing documentation category
- 62 markdown files, 23,085 total lines
- Critical for user adoption and onboarding
- Contains tutorials, API docs, workflows, theory
- Referenced in all 5 learning paths (Path 0-4)
- Includes getting-started.md (first touchpoint for new users)
- Multiple validation reports already exist (quality-conscious)
- Project in maintenance/publication phase - needs publication-ready docs

**Audit Objectives:**
1. Verify completeness across 8 subcategories (api, features, how-to, interactive, theory, tutorials, workflows)
2. Validate accuracy of technical content (code examples, commands, file paths)
3. Ensure consistency of terminology, style, and structure across 62 files
4. Check navigation integrity (INDEX.md, cross-references, toctrees)
5. Identify gaps and prioritize improvements for publication readiness

---

## Category Baseline Metrics

**Structure:**
```
docs/guides/
├── api/             (7 files)
├── features/        (9 files, includes code-collapse/)
├── how-to/          (5 files)
├── interactive/     (6 files)
├── theory/          (4 files)
├── tutorials/       (6 files)
├── workflows/       (16 files)
└── root files/      (9 files, includes INDEX.md)
```

**Files:**
- Total markdown files: 62
- Total lines: 23,085
- Average lines per file: ~372
- Largest subcategory: workflows/ (16 files)
- Smallest subcategory: theory/ (4 files)

**Critical Files:**
- INDEX.md (category hub)
- getting-started.md (Path 1 entry point)
- tutorial-01-first-simulation.md (Path 1-4 entry point)
- QUICK_REFERENCE.md (quick lookup)
- README.md (subcategory overviews)

**Context:**
- Last modified: Multiple recent updates (Oct-Nov 2025)
- Phase: Maintenance/Publication (Phase 5 Research complete)
- Audience: Mixed (beginners to researchers)
- Expected standards: Completeness ≥80%, Accuracy ≥95%, Readability ≥60%

---

## Customized MA-01 Prompt

```
CATEGORY DOCUMENTATION AUDIT
WHAT: Analyze all documentation in docs/guides/ for quality and consistency
WHY:  Ensure category meets documentation standards before publication
HOW:  Aggregate metrics across files, check consistency, verify navigation
WIN:  Category quality report + prioritized improvement roadmap
TIME: 5 hours

TARGET CATEGORY: guides

INPUTS:
- Category directory: docs/guides/
- Number of files: 62 markdown files, 23,085 lines
- Expected standards: Completeness ≥80%, Accuracy ≥95%, Readability ≥60%
- Subcategories: api, features, how-to, interactive, theory, tutorials, workflows
- Context: Maintenance/Publication phase, research complete, LT-7 paper submission-ready

ANALYSIS TASKS:

1. INVENTORY (30 min)
   - List all 62 files with line counts
   - Verify file types (.md only, no orphaned files)
   - Document subdirectory structure (8 subdirs validated)
   - Identify file categories (tutorial vs reference vs workflow)
   - Check for backup files (.bak) - INDEX.md.bak found
   - Verify file naming conventions (kebab-case, descriptive)
   - Export inventory to JSON

2. AGGREGATE METRICS (1.5 hours)
   - For each file:
     * Completeness: Has intro, body, examples, summary? (0-100%)
     * Accuracy: Commands work, paths exist, code runs? (0-100%)
     * Readability: Flesch score, sentence length, jargon? (0-100%)
   - Calculate per-file scores
   - Calculate subcategory averages (api/, tutorials/, etc.)
   - Calculate category average (overall guides/ score)
   - Identify outliers:
     * Best 5 files (use as quality templates)
     * Worst 5 files (prioritize for fixes)
   - Rank all 62 files by quality
   - Export metrics to JSON

3. CONSISTENCY CHECK (1.5 hours)
   - Terminology consistency:
     * "simulation" vs "sim" vs "experiment"
     * "controller" vs "control algorithm" vs "control law"
     * "PSO" vs "Particle Swarm Optimization" (first use)
     * "DIP" vs "Double Inverted Pendulum" (first use)
     * Check 20+ key terms across all files
   - Style consistency:
     * Heading levels (H1 title only, H2 sections, H3 subsections)
     * Code block language tags (python, bash, yaml)
     * Command formatting (inline `code` vs blocks)
     * File path format (relative vs absolute)
     * List formatting (-, *, numbered)
   - Structure consistency:
     * Tutorial structure: Overview -> Prerequisites -> Steps -> Validation -> Next Steps
     * API doc structure: Description -> Parameters -> Returns -> Examples
     * Workflow structure: Goal -> Prerequisites -> Steps -> Troubleshooting
   - Cross-reference consistency:
     * Link format: [text](path) vs [text](url)
     * Internal links use relative paths
     * External links include domain
   - Document inconsistencies with:
     * File pairs showing discrepancy
     * Specific line numbers
     * Recommendation for standard

4. NAVIGATION VERIFICATION (1 hour)
   - INDEX.md completeness:
     * All 62 files linked from INDEX.md or subcategory READMEs
     * All subcategories have descriptions
     * All learning paths referenced
     * All personas have entry points
   - Cross-reference validation:
     * Extract all internal links (est. 200+ links)
     * Verify file paths exist (no 404s)
     * Check for circular references
     * Verify external links respond (HTTP 200)
   - Breadcrumb validation:
     * Can navigate: INDEX.md -> subcategory -> file -> back
     * Every file has "parent" link or breadcrumb
   - Sphinx toctree verification:
     * Check docs/index.rst references guides/
     * Verify all files appear in Sphinx build
     * No orphaned files (not in any toctree)
   - Document navigation issues:
     * Broken links (file, line number, target)
     * Missing links (file not referenced anywhere)
     * Dead ends (no "next steps" or "related")

5. GAP ANALYSIS (30 min)
   - Missing topics:
     * Compare INDEX.md sections to actual files
     * Check CLAUDE.md for documented features without guides
     * Verify all 7 controllers have documentation
     * Check all tutorials 01-05 exist (01, 02, 03, 04, 05)
   - Incomplete files:
     * Files with TODO, FIXME, TBD markers
     * Files with empty sections
     * Files shorter than 50 lines (likely stubs)
   - Outdated content:
     * References to deprecated features
     * Outdated version numbers
     * Screenshots from old UI (pre-Phase 3)
   - Prioritize gaps:
     * P0 Critical: Blocks user from completing basic tasks
     * P1 Major: Confuses users, reduces trust
     * P2 Minor: Nice-to-have, improves polish

VALIDATION REQUIREMENTS:
1. Manually verify metrics for 10+ random files (sample each subcategory)
2. Click all cross-reference links in INDEX.md (verify no 404s)
3. Read 3-4 files end-to-end for coherence (1 tutorial, 1 API doc, 1 workflow, 1 theory)
4. Execute code examples from 5+ files (verify commands work)
5. Check getting-started.md and tutorial-01 (critical path for new users)
6. Verify no Unicode emoji violations (ASCII-only per CLAUDE.md)

DELIVERABLES:
1. Category quality scorecard (aggregate metrics)
   - Overall guides/ score (0-100)
   - Per-subcategory scores (api/, tutorials/, etc.)
   - Per-file scores (62 files ranked)
   - Completeness, Accuracy, Readability breakdowns
2. File ranking (best to worst)
   - Top 5 (quality templates)
   - Bottom 5 (fix priority)
   - Full ranked list (CSV/JSON)
3. Consistency issues list (with examples)
   - Terminology inconsistencies (20+ terms checked)
   - Style inconsistencies (headings, code, lists)
   - Structure inconsistencies (tutorial vs API vs workflow)
4. Navigation issues list (broken links, missing entries)
   - Broken links (file, line, target)
   - Missing links (files not in INDEX.md)
   - Dead ends (no navigation to related content)
5. Gap analysis (missing topics, incomplete files)
   - Missing topics (not documented)
   - Incomplete files (stubs, TODOs)
   - Outdated content (deprecated features)
6. Improvement roadmap (prioritized, with effort)
   - P0 Critical (fix immediately, 0-2 hours each)
   - P1 Major (fix before publication, 2-4 hours each)
   - P2 Minor (nice-to-have, 30min-1hr each)
   - Total effort estimate
   - Recommended sequence

SUCCESS CRITERIA:
- [ ] All 62 files in category analyzed
- [ ] Aggregate metrics calculated (per-file, per-subcategory, overall)
- [ ] 10+ files manually verified
- [ ] All cross-reference links tested (INDEX.md + 5+ other files)
- [ ] 5+ code examples executed and validated
- [ ] Consistency issues documented with file pairs and line numbers
- [ ] Improvement roadmap prioritized by impact and effort
- [ ] Can answer: "Is this category ready for publication?"
- [ ] Can answer: "Will users successfully complete tutorial-01?"
- [ ] Can answer: "Are all 7 controllers documented?"
```

---

## Pre-Audit Validation

### File Structure Verification
```bash
# Verify directory exists
stat docs/guides/

# Confirm file count
find docs/guides -type f -name "*.md" | wc -l
# Expected: 62

# Confirm line count
find docs/guides -type f -name "*.md" -exec wc -l {} + | tail -1
# Expected: ~23,085 total

# List subdirectories
find docs/guides -type d | sort
# Expected: 9 directories (root + 8 subdirs)
```

### Critical Files Check
```bash
# Verify critical files exist
ls -lh docs/guides/INDEX.md
ls -lh docs/guides/getting-started.md
ls -lh docs/guides/QUICK_REFERENCE.md
ls -lh docs/guides/tutorials/tutorial-01-first-simulation.md

# Check for backup files (.bak)
find docs/guides -name "*.bak"
# Expected: INDEX.md.bak (should this be kept or removed?)
```

### Baseline Metrics
```bash
# Word count per subcategory
for dir in api features how-to interactive theory tutorials workflows; do
  echo "=== $dir ==="
  find docs/guides/$dir -name "*.md" -exec wc -w {} + | tail -1
done

# File count per subcategory
for dir in api features how-to interactive theory tutorials workflows; do
  echo "$dir: $(find docs/guides/$dir -name "*.md" | wc -l) files"
done
```

### Critical Dependencies
- [ ] sequential-thinking MCP server operational
- [ ] File read access to docs/guides/ directory
- [ ] Python available for metrics scripts
- [ ] Git history accessible (for last modified dates)
- [ ] Sphinx build working (for toctree verification)

---

## Execution Workflow

### Phase 1: Setup (30 min - INVENTORY)

**1.1 Inventory Collection (15 min)**
1. List all 62 files with metadata (path, lines, words, last modified)
2. Categorize by subdirectory (api, features, how-to, etc.)
3. Categorize by type (tutorial, reference, workflow, theory)
4. Identify backup files (.bak) and orphans
5. Export to `guides_inventory.json`

**1.2 Baseline Metrics (15 min)**
1. Calculate per-subcategory counts (files, lines, words)
2. Identify largest/smallest files
3. Check file naming conventions
4. Document subdirectory structure
5. Export to `guides_baseline.json`

### Phase 2: Analysis (3 hours)

**2.1 Aggregate Metrics (1.5 hours)**

For each of 62 files, calculate:
- **Completeness (0-100):**
  * Has H1 title (10 points)
  * Has introduction/overview (15 points)
  * Has main content sections (30 points)
  * Has examples (20 points)
  * Has summary/conclusion (10 points)
  * Has navigation links (15 points)

- **Accuracy (0-100):**
  * Code blocks have language tags (20 points)
  * File paths exist (30 points)
  * Commands are syntactically valid (30 points)
  * Version info matches current version (10 points)
  * No TODO/FIXME/TBD markers (10 points)

- **Readability (0-100):**
  * Flesch Reading Ease 60-70 (30 points)
  * Average sentence length <25 words (20 points)
  * Paragraph length <5 sentences (20 points)
  * Headings clear and descriptive (15 points)
  * Code-to-text ratio appropriate (15 points)

**Automation:**
- Write `calculate_file_metrics.py` (scores 1 file)
- Write `batch_metrics.py` (scores all 62 files)
- Export to `guides_metrics.json`

**Manual Validation:**
- Manually score 10+ random files (2 per subcategory minimum)
- Compare manual vs automated scores (verify ≥90% agreement)
- Adjust automation if discrepancies found

**Aggregation:**
- Calculate per-subcategory averages
- Calculate overall guides/ average
- Identify top 5 and bottom 5 files
- Rank all 62 files
- Export to `guides_ranked.csv`

**2.2 Consistency Check (1.5 hours)**

**Terminology Audit:**
1. Extract all instances of key terms (simulation, controller, PSO, DIP, etc.)
2. Check for consistent usage (first use spelled out, abbreviations after)
3. Identify conflicting terminology (e.g., "sim" vs "simulation")
4. Document recommended standard terms
5. List files violating standards

**Style Audit:**
1. Check heading hierarchy (no H1 → H3 skips)
2. Verify code block language tags (all have ```python, ```bash, etc.)
3. Check command formatting (inline vs block consistency)
4. Verify list formatting (consistent markers)
5. Document style violations with line numbers

**Structure Audit:**
1. Define standard structures for each file type:
   - Tutorial: Overview → Prerequisites → Steps → Validation → Next
   - API: Description → Parameters → Returns → Examples → See Also
   - Workflow: Goal → Prerequisites → Steps → Troubleshooting → Related
2. Check 5+ files of each type for structure compliance
3. Document structure violations

**Cross-reference Audit:**
1. Check link format consistency ([text](path) format)
2. Verify relative vs absolute path usage (internal = relative)
3. Check external link format (includes domain)
4. Document format violations

**Outputs:**
- `guides_terminology_report.md`
- `guides_style_violations.csv`
- `guides_structure_compliance.json`

**2.3 Navigation Verification (1 hour)**

**INDEX.md Audit:**
1. Read guides/INDEX.md
2. Extract all file links
3. Verify all 62 files linked (directly or via subcategory READMEs)
4. Check for dead links (linked but file doesn't exist)
5. Check for orphans (file exists but not linked)

**Cross-reference Validation:**
1. Extract all internal links from all 62 files (est. 200+ links)
2. Verify each target file exists
3. Check for circular references (A → B → C → A)
4. Verify external links respond (HTTP 200)
5. Document broken links with file and line number

**Breadcrumb Validation:**
1. Test navigation path: INDEX.md → api/README.md → api/controllers.md
2. Test navigation path: INDEX.md → tutorials/tutorial-01 → tutorials/tutorial-02
3. Verify each file has "back" or "up" links
4. Verify each file has "next" or "related" links

**Sphinx Toctree Audit:**
1. Check docs/index.rst includes guides/
2. Build Sphinx docs: `sphinx-build -M html docs docs/_build`
3. Check for orphan warnings
4. Verify all 62 files appear in build output
5. Test search functionality (search for "tutorial")

**Outputs:**
- `guides_navigation_issues.md`
- `guides_broken_links.csv`
- `guides_orphaned_files.txt`

### Phase 3: Gap Analysis & Validation (1 hour)

**3.1 Gap Analysis (30 min)**

**Missing Topics:**
1. Check INDEX.md for promised but missing content
2. Verify all 7 controllers documented:
   - classical_smc ✓
   - sta_smc ✓
   - adaptive_smc ✓
   - hybrid_adaptive_sta_smc ✓
   - swing_up_smc ✓
   - mpc_controller ✓
   - factory pattern ✓
3. Verify tutorial sequence complete (01, 02, 03, 04, 05)
4. Check CLAUDE.md for features needing user docs

**Incomplete Files:**
1. Search for TODO, FIXME, TBD markers: `grep -r "TODO\|FIXME\|TBD" docs/guides/`
2. Find files <50 lines (likely stubs): `find docs/guides -name "*.md" -exec wc -l {} \; | awk '$1 < 50'`
3. Find files with empty sections (## Heading with no content before next ##)
4. Document incomplete files with specific missing sections

**Outdated Content:**
1. Search for version numbers: `grep -r "v0\|v1\|version" docs/guides/`
2. Search for deprecated terms: `grep -r "deprecated\|legacy\|old" docs/guides/`
3. Check for UI screenshots (may be pre-Phase 3)
4. Document outdated content with recommended updates

**Prioritization:**
- P0 Critical: getting-started.md, tutorial-01, INDEX.md issues
- P1 Major: Incomplete tutorials, missing API docs, broken workflows
- P2 Minor: Typos, formatting, nice-to-have improvements

**Outputs:**
- `guides_gap_analysis.md`
- `guides_incomplete_files.csv`
- `guides_outdated_content.csv`

**3.2 Final Validation (30 min)**

1. **Manual File Review:**
   - Read tutorial-01 end-to-end (validate new user experience)
   - Read api/controllers.md end-to-end (validate API reference quality)
   - Read workflows/pso-optimization-workflow.md (validate workflow clarity)
   - Read theory/smc-theory.md (validate theory accuracy)

2. **Code Example Execution:**
   - Execute getting-started.md commands (simulate.py --help, etc.)
   - Execute tutorial-01 commands (first simulation)
   - Execute api/configuration.md examples (config loading)
   - Execute workflows/pso-optimization-workflow.md commands
   - Execute how-to/running-simulations.md commands
   - Document any failing commands

3. **Critical Path Validation:**
   - Simulate new user: README.md → NAVIGATION.md → getting-started.md → tutorial-01
   - Check for blockers (missing prerequisites, unclear steps, broken commands)
   - Document user experience issues

4. **Unicode Emoji Check:**
   - Search for Unicode violations: `grep -r "[emoji pattern]" docs/guides/`
   - Verify ASCII-only markers: [OK], [ERROR], [INFO], [WARNING]
   - Document any violations (critical per CLAUDE.md)

**Outputs:**
- `guides_validation_report.md`
- `guides_failed_commands.txt`
- `guides_user_experience_issues.md`

---

## Expected Outputs

### 1. Category Quality Scorecard (markdown)

```markdown
# docs/guides/ Quality Scorecard

**Audit Date:** November 10, 2025
**Auditor:** Claude Code (Sequential Thinking MCP)
**Files Analyzed:** 62 markdown files (23,085 lines)

## Overall Scores

| Metric          | Score | Grade | Issues | Status              |
|-----------------|-------|-------|--------|---------------------|
| Completeness    | XX/100| [A-F] | XX     | [PASS/NEEDS WORK]   |
| Accuracy        | XX/100| [A-F] | XX     | [PASS/NEEDS WORK]   |
| Readability     | XX/100| [A-F] | XX     | [PASS/NEEDS WORK]   |
| Consistency     | XX/100| [A-F] | XX     | [PASS/NEEDS WORK]   |
| Navigation      | XX/100| [A-F] | XX     | [PASS/NEEDS WORK]   |
| **OVERALL**     | XX/100| [A-F] | XX     | [PUBLICATION READY] |

**Publication Ready If:** Overall ≥85, no P0 issues, all critical files ≥90

## Per-Subcategory Scores

| Subcategory     | Files | Lines | Completeness | Accuracy | Readability | Overall |
|-----------------|-------|-------|--------------|----------|-------------|---------|
| api/            | 7     | ~XXX  | XX/100       | XX/100   | XX/100      | XX/100  |
| features/       | 9     | ~XXX  | XX/100       | XX/100   | XX/100      | XX/100  |
| how-to/         | 5     | ~XXX  | XX/100       | XX/100   | XX/100      | XX/100  |
| interactive/    | 6     | ~XXX  | XX/100       | XX/100   | XX/100      | XX/100  |
| theory/         | 4     | ~XXX  | XX/100       | XX/100   | XX/100      | XX/100  |
| tutorials/      | 6     | ~XXX  | XX/100       | XX/100   | XX/100      | XX/100  |
| workflows/      | 16    | ~XXX  | XX/100       | XX/100   | XX/100      | XX/100  |
| root/           | 9     | ~XXX  | XX/100       | XX/100   | XX/100      | XX/100  |

## Top 5 Files (Quality Templates)

1. [file path] - XX/100 - [reason for high score]
2. [file path] - XX/100 - [reason]
3. [file path] - XX/100 - [reason]
4. [file path] - XX/100 - [reason]
5. [file path] - XX/100 - [reason]

## Bottom 5 Files (Fix Priority)

1. [file path] - XX/100 - [critical issues]
2. [file path] - XX/100 - [critical issues]
3. [file path] - XX/100 - [critical issues]
4. [file path] - XX/100 - [critical issues]
5. [file path] - XX/100 - [critical issues]

## Critical Findings

**P0 Critical (Blocks Users):**
- [Number] issues found
- [List most severe 3-5 issues]

**P1 Major (Reduces Trust):**
- [Number] issues found
- [List most impactful 3-5 issues]

**P2 Minor (Polish):**
- [Number] issues found
- [Summary]

## Recommendations

**Immediate Actions (Before Publication):**
1. [Action] - Effort: [time] - Impact: [HIGH/MED/LOW]
2. [Action] - Effort: [time] - Impact: [HIGH/MED/LOW]
3. [Action] - Effort: [time] - Impact: [HIGH/MED/LOW]

**Short-Term Improvements (Next Month):**
1. [Action] - Effort: [time]
2. [Action] - Effort: [time]

**Long-Term Goals (Next Quarter):**
1. [Action] - Effort: [time]
2. [Action] - Effort: [time]

## Answer to Success Criteria

**Is this category ready for publication?** [YES/NO with reason]

**Will users successfully complete tutorial-01?** [YES/NO with blockers if any]

**Are all 7 controllers documented?** [YES/NO with missing if any]
```

### 2. File Ranking (CSV)

```csv
rank,file_path,overall_score,completeness,accuracy,readability,issues,priority
1,docs/guides/tutorials/tutorial-01-first-simulation.md,95,98,95,92,2,P2
2,docs/guides/getting-started.md,93,95,94,90,3,P2
...
62,docs/guides/[worst-file].md,45,40,50,45,12,P0
```

### 3. Consistency Issues List (markdown)

```markdown
# docs/guides/ Consistency Issues

**Audit Date:** November 10, 2025

## Terminology Inconsistencies (XX found)

### Issue 1: "Simulation" vs "Sim"
- **Standard:** Use "simulation" in formal docs, "sim" only in variable names
- **Violations:**
  - docs/guides/how-to/running-simulations.md:45 - Uses "sim" in prose
  - docs/guides/workflows/batch-simulation-workflow.md:78 - Inconsistent usage
- **Impact:** Confuses new users (is "sim" different from "simulation"?)
- **Fix:** Global find-replace in prose, keep in code
- **Effort:** 30 minutes

### Issue 2: [Next issue]
...

## Style Inconsistencies (XX found)

### Issue 1: Code Block Language Tags
- **Standard:** All code blocks must have language tag (```python, ```bash)
- **Violations:**
  - docs/guides/api/controllers.md:120 - No language tag on code block
  - docs/guides/workflows/pso-hil-tuning.md:89 - No language tag
- **Impact:** No syntax highlighting, harder to read
- **Fix:** Add appropriate language tags
- **Effort:** 15 minutes

### Issue 2: [Next issue]
...

## Structure Inconsistencies (XX found)

### Issue 1: Tutorial Structure
- **Standard:** Overview → Prerequisites → Steps → Validation → Next Steps
- **Violations:**
  - docs/guides/tutorials/tutorial-04-custom-controller.md - Missing "Next Steps"
  - docs/guides/tutorials/tutorial-05-research-workflow.md - Missing "Validation"
- **Impact:** Users don't know what to do next or how to verify success
- **Fix:** Add missing sections
- **Effort:** 1 hour per file

### Issue 2: [Next issue]
...
```

### 4. Navigation Issues List (markdown)

```markdown
# docs/guides/ Navigation Issues

**Audit Date:** November 10, 2025

## Broken Links (XX found)

| File | Line | Link Text | Target | Severity | Fix |
|------|------|-----------|--------|----------|-----|
| docs/guides/api/controllers.md | 45 | "See configuration" | ../config/params.md | CRITICAL | Update to ../api/configuration.md |
| docs/guides/tutorials/tutorial-02.md | 120 | "Previous tutorial" | tutorial-01.md | MAJOR | Add ../tutorials/ prefix |
...

## Missing Links (Orphaned Files) (XX found)

| File | Size | Last Modified | Severity | Recommendation |
|------|------|---------------|----------|----------------|
| docs/guides/features/advanced-feature.md | 450 lines | 2025-10-15 | MAJOR | Add to INDEX.md features section |
| docs/guides/workflows/deprecated-workflow.md | 120 lines | 2024-09-20 | MINOR | Delete or move to archive |
...

## Dead Ends (No Next Steps) (XX found)

| File | Issue | Impact | Fix |
|------|-------|--------|-----|
| docs/guides/tutorials/tutorial-03.md | No "Next Steps" section | Users don't know to proceed to tutorial-04 | Add Next Steps linking to tutorial-04 |
| docs/guides/how-to/result-analysis.md | No "Related" section | Users miss workflows/monte-carlo-validation | Add Related section |
...

## INDEX.md Issues (XX found)

| Issue | Severity | Fix |
|-------|----------|-----|
| Missing link to workflows/robust-pso-optimization.md | MAJOR | Add to Workflows section |
| Dead link to api/deprecated.md | MINOR | Remove or update |
...
```

### 5. Gap Analysis (markdown)

```markdown
# docs/guides/ Gap Analysis

**Audit Date:** November 10, 2025

## Missing Topics (XX found)

| Topic | Expected Location | Priority | Reason | Effort |
|-------|-------------------|----------|--------|--------|
| MPC Controller Guide | docs/guides/api/mpc-controller.md | P1 | Controller exists but undocumented | 3 hours |
| Hybrid SMC Theory | docs/guides/theory/hybrid-smc.md | P1 | Used in research but not explained | 4 hours |
| PSO Troubleshooting | docs/guides/how-to/pso-troubleshooting.md | P0 | Users frequently ask about PSO failures | 2 hours |
...

## Incomplete Files (XX found)

| File | Size | Issues | Priority | Fix |
|------|------|--------|----------|-----|
| docs/guides/workflows/pso-vs-grid-search.md | 45 lines | Has TODO for benchmark results | P1 | Add benchmark data from LT-7 | 1 hour |
| docs/guides/api/plant-models.md | 120 lines | Missing examples section | P2 | Add 2-3 code examples | 1.5 hours |
...

## Outdated Content (XX found)

| File | Issue | Last Updated | Priority | Fix |
|------|-------|--------------|----------|-----|
| docs/guides/getting-started.md | References v1.0 config format | 2024-08-15 | P0 | Update to v2.0 format | 30 min |
| docs/guides/tutorials/tutorial-01.md | Uses old UI screenshots | 2024-09-10 | P1 | Replace with Phase 3 UI | 1 hour |
...
```

### 6. Improvement Roadmap (markdown)

```markdown
# docs/guides/ Improvement Roadmap

**Audit Date:** November 10, 2025
**Total Issues:** XX (P0: XX, P1: XX, P2: XX)
**Total Effort:** XX hours
**Recommended Timeline:** X weeks

## Phase 1: Critical Fixes (BEFORE PUBLICATION)
**Duration:** X hours over X days
**Deadline:** Before LT-7 publication announcement

### P0 Critical Issues (Must Fix)
1. **Fix broken links in getting-started.md** (30 min)
   - Files: docs/guides/getting-started.md:45, 67, 89
   - Impact: New users cannot navigate to next steps
   - Fix: Update links to current paths

2. **Add PSO troubleshooting guide** (2 hours)
   - File: NEW - docs/guides/how-to/pso-troubleshooting.md
   - Impact: Users frequently blocked by PSO failures
   - Fix: Document common PSO issues from GitHub issues

3. **Update tutorial-01 for current config format** (1 hour)
   - File: docs/guides/tutorials/tutorial-01-first-simulation.md
   - Impact: Tutorial fails for new users
   - Fix: Update code examples to config v2.0

[Continue for all P0 issues]

**Total Phase 1 Effort:** XX hours

## Phase 2: Major Improvements (BEFORE WIDER RELEASE)
**Duration:** XX hours over X weeks
**Deadline:** Within 1 month of publication

### P1 Major Issues (Should Fix)
1. **Document MPC controller** (3 hours)
   - File: NEW - docs/guides/api/mpc-controller.md
   - Impact: Users can't use experimental MPC feature
   - Fix: Write API doc with examples

2. **Standardize tutorial structure** (4 hours)
   - Files: All tutorials/ (6 files)
   - Impact: Inconsistent user experience
   - Fix: Add missing sections per standard template

[Continue for all P1 issues]

**Total Phase 2 Effort:** XX hours

## Phase 3: Polish & Enhancement (ONGOING)
**Duration:** XX hours over X months
**Deadline:** Next quarter

### P2 Minor Issues (Nice to Have)
1. **Improve readability scores** (3 hours)
   - Files: [list files with Flesch <60]
   - Impact: Harder to read for non-experts
   - Fix: Simplify complex sentences, add definitions

2. **Add more examples to API docs** (5 hours)
   - Files: api/configuration.md, api/simulation.md, api/utilities.md
   - Impact: Users learn faster with examples
   - Fix: Add 2-3 examples per file

[Continue for all P2 issues]

**Total Phase 3 Effort:** XX hours

## Recommended Sequence

**Week 1 (Pre-Publication):**
- Day 1: Fix all broken links (P0)
- Day 2-3: Add PSO troubleshooting, update tutorial-01 (P0)
- Day 4: Verify fixes, test critical path
- Day 5: Buffer for unexpected issues

**Weeks 2-4 (Post-Publication):**
- Week 2: Document missing controllers (P1)
- Week 3: Standardize tutorial structure (P1)
- Week 4: Fix incomplete files (P1)

**Month 2-3 (Ongoing):**
- Improve readability (P2)
- Add examples (P2)
- Polish formatting (P2)

## Success Metrics

**Phase 1 Complete When:**
- [ ] Zero P0 issues remaining
- [ ] All broken links fixed
- [ ] getting-started.md and tutorial-01 tested end-to-end
- [ ] Overall category score ≥85/100

**Phase 2 Complete When:**
- [ ] Zero P1 issues remaining
- [ ] All 7 controllers documented
- [ ] All tutorials follow standard structure
- [ ] Overall category score ≥90/100

**Phase 3 Complete When:**
- [ ] Zero P2 issues remaining
- [ ] Average readability score ≥70
- [ ] All files have examples
- [ ] Overall category score ≥95/100
```

### 7. Raw Metrics (JSON)

```json
{
  "audit_metadata": {
    "category": "docs/guides/",
    "audit_date": "2025-11-10",
    "auditor": "Claude Code (Sequential Thinking MCP)",
    "duration_hours": 5,
    "files_analyzed": 62,
    "total_lines": 23085
  },
  "inventory": {
    "subdirectories": ["api", "features", "how-to", "interactive", "theory", "tutorials", "workflows"],
    "file_types": {
      "markdown": 62,
      "backup": 1
    },
    "per_subcategory": {
      "api": {"files": 7, "lines": 0, "words": 0},
      "features": {"files": 9, "lines": 0, "words": 0},
      "how-to": {"files": 5, "lines": 0, "words": 0},
      "interactive": {"files": 6, "lines": 0, "words": 0},
      "theory": {"files": 4, "lines": 0, "words": 0},
      "tutorials": {"files": 6, "lines": 0, "words": 0},
      "workflows": {"files": 16, "lines": 0, "words": 0},
      "root": {"files": 9, "lines": 0, "words": 0}
    }
  },
  "overall_scores": {
    "completeness": 0,
    "accuracy": 0,
    "readability": 0,
    "consistency": 0,
    "navigation": 0,
    "overall": 0
  },
  "per_subcategory_scores": {
    "api": {"completeness": 0, "accuracy": 0, "readability": 0, "overall": 0},
    "features": {"completeness": 0, "accuracy": 0, "readability": 0, "overall": 0},
    "how-to": {"completeness": 0, "accuracy": 0, "readability": 0, "overall": 0},
    "interactive": {"completeness": 0, "accuracy": 0, "readability": 0, "overall": 0},
    "theory": {"completeness": 0, "accuracy": 0, "readability": 0, "overall": 0},
    "tutorials": {"completeness": 0, "accuracy": 0, "readability": 0, "overall": 0},
    "workflows": {"completeness": 0, "accuracy": 0, "readability": 0, "overall": 0},
    "root": {"completeness": 0, "accuracy": 0, "readability": 0, "overall": 0}
  },
  "file_rankings": {
    "top_5": [],
    "bottom_5": [],
    "all_files_ranked": []
  },
  "issues": {
    "p0_critical": [],
    "p1_major": [],
    "p2_minor": []
  },
  "consistency": {
    "terminology": {
      "checked_terms": [],
      "violations": []
    },
    "style": {
      "heading_hierarchy_violations": [],
      "code_block_violations": [],
      "list_formatting_violations": []
    },
    "structure": {
      "tutorial_structure_violations": [],
      "api_structure_violations": [],
      "workflow_structure_violations": []
    }
  },
  "navigation": {
    "broken_links": [],
    "orphaned_files": [],
    "dead_ends": [],
    "index_md_issues": []
  },
  "gaps": {
    "missing_topics": [],
    "incomplete_files": [],
    "outdated_content": []
  },
  "validation": {
    "manual_files_reviewed": [],
    "code_examples_tested": [],
    "critical_path_validated": false,
    "unicode_violations_found": 0
  }
}
```

---

## Automation Scripts (To Be Created)

### 1. Inventory Collector (`collect_guides_inventory.py`)
```python
"""
Collects inventory of all files in docs/guides/
Outputs: guides_inventory.json
"""
# Usage: python .artifacts/scripts/collect_guides_inventory.py
```

### 2. File Metrics Calculator (`calculate_file_metrics.py`)
```python
"""
Calculates completeness, accuracy, readability for a single file
Outputs: file_metrics.json
"""
# Usage: python .artifacts/scripts/calculate_file_metrics.py docs/guides/getting-started.md
```

### 3. Batch Metrics Runner (`batch_guides_metrics.py`)
```python
"""
Runs calculate_file_metrics.py on all 62 files
Outputs: guides_metrics.json, guides_ranked.csv
"""
# Usage: python .artifacts/scripts/batch_guides_metrics.py
```

### 4. Link Validator (`validate_guides_links.py`)
```python
"""
Extracts all links from all files, validates targets exist
Outputs: guides_broken_links.csv
"""
# Usage: python .artifacts/scripts/validate_guides_links.py
```

### 5. Terminology Checker (`check_guides_terminology.py`)
```python
"""
Checks for consistent terminology across all files
Outputs: guides_terminology_report.md
"""
# Usage: python .artifacts/scripts/check_guides_terminology.py
```

### 6. Gap Analyzer (`analyze_guides_gaps.py`)
```python
"""
Finds missing topics, incomplete files, outdated content
Outputs: guides_gap_analysis.md
"""
# Usage: python .artifacts/scripts/analyze_guides_gaps.py
```

---

## Post-Audit Actions

### If Overall Score ≥ 85 (Publication Ready)
- [AI] Commit all deliverables to `.artifacts/qa_audits/MA-01_GUIDES_AUDIT_2025-11-10/`
- [AI] Update `.project/ai/planning/CURRENT_STATUS.md` with audit results
- [AI] Create summary report for user
- [USER] Review P1/P2 recommendations for post-publication improvements
- [USER] Approve publication timeline

### If Overall Score 70-84 (Needs Work)
- [AI] Generate automated fix scripts for P0 issues
- [AI] Create GitHub issues for P0 and P1 fixes
- [AI] Estimate time to publication readiness
- [USER] Review and approve fix plan
- [USER] Decide: delay publication or proceed with known issues

### If Overall Score < 70 (Critical Issues)
- [AI] Flag as CRITICAL in project tracking
- [AI] Generate detailed recovery plan with timeline
- [AI] Identify blocking issues preventing publication
- [USER] IMMEDIATE review required
- [USER] Decide: major rework or scope reduction

### Commit Strategy
```bash
# After audit complete
git add .artifacts/qa_audits/MA-01_GUIDES_AUDIT_2025-11-10/
git add .project/ai/ultrathink_sessions/MA-01_EXECUTION_PLAN_GUIDES.md
git commit -m "qa(MA-01): Complete docs/guides/ category audit (62 files, 23,085 lines)

- Overall score: XX/100 (PUBLICATION READY/NEEDS WORK)
- Identified XX issues (P0: XX, P1: XX, P2: XX)
- Total fix effort: XX hours over X weeks
- Deliverables: scorecard, rankings, consistency report, navigation issues, gap analysis, improvement roadmap

[AI] Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin main
```

---

## Success Indicators

**Audit Complete When:**
- [ ] All 6 todos marked complete
- [ ] All 62 files analyzed with metrics
- [ ] 10+ files manually verified
- [ ] All cross-reference links tested
- [ ] 5+ code examples executed
- [ ] Quality scorecard exported (markdown + JSON)
- [ ] File rankings exported (CSV)
- [ ] Consistency issues documented
- [ ] Navigation issues documented
- [ ] Gap analysis completed
- [ ] Improvement roadmap prioritized and estimated
- [ ] All deliverables committed to `.artifacts/qa_audits/MA-01_GUIDES_AUDIT_2025-11-10/`

**Can Answer:**
- [ ] "Is this category ready for publication?" (YES/NO with specific blockers)
- [ ] "Will users successfully complete tutorial-01?" (YES/NO with failure points)
- [ ] "Are all 7 controllers documented?" (YES/NO with missing list)
- [ ] "What's the total effort to reach publication readiness?" (X hours over X weeks)
- [ ] "What are the top 3 most critical issues blocking publication?" (Specific with line numbers)

**Publication Ready If:**
- [ ] Overall score ≥ 85/100
- [ ] Zero P0 critical issues
- [ ] All critical files (getting-started.md, tutorial-01, INDEX.md) score ≥90
- [ ] No broken links in critical navigation paths
- [ ] All code examples in getting-started and tutorial-01 tested and working
- [ ] Zero Unicode emoji violations
- [ ] All 7 controllers have user-facing documentation
- [ ] Tutorial sequence 01-05 complete and validated
- [ ] WCAG 2.1 Level AA maintained (if web-rendered)

---

## Timeline

**Estimated Audit Duration:** 5 hours

**Breakdown:**
- Phase 1 (Setup/Inventory): 30 minutes
- Phase 2 (Analysis): 3 hours
  - Aggregate Metrics: 1.5 hours
  - Consistency Check: 1.5 hours
  - Navigation Verification: 1 hour (overlaps with consistency)
- Phase 3 (Gap Analysis & Validation): 1 hour
- Deliverables Export & Documentation: 30 minutes

**Buffer:** +1 hour for unexpected complexity (total 6 hours safe estimate)

---

**Execution Plan Created:** November 10, 2025
**Target Audit Start:** TBD (awaiting user approval)
**Expected Audit Completion:** Start date + 1 day (6 hours of focused work)
