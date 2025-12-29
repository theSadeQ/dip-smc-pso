# QA-02: Main Entry Points Quality Audit - Execution Plan

**Status**: PLANNING
**Created**: 2025-11-09
**Target**: Achieve 100/100 QA score for all 4 main entry point files
**Methodology**: Adapted from QA-01 (NAVIGATION.md) success

---

## Executive Summary

QA-02 systematically audits and improves the 4 main entry points to the documentation ecosystem, ensuring first-time users encounter publication-quality content.

**Target Files** (4):
1. `docs/index.md` - Sphinx homepage (primary web docs entry)
2. `guides/INDEX.md` - User guides hub (379 lines, 43 files coordinator)
3. `README.md` - GitHub entry point (project first impression)
4. `CLAUDE.md` - Team memory (project conventions, 1000+ lines)

**Success Criteria**: 100/100 QA score for ALL 4 files (20 category scores total)

---

## Scope Definition

### Why These 4 Files?

1. **High Visibility**: Users encounter these first when entering the documentation
2. **Strategic Importance**: Referenced in NAVIGATION.md as "Main Entry Points"
3. **Diverse Types**: Cover Sphinx (RST), Markdown guides, GitHub standards, internal docs
4. **Manageable Scope**: 4 files achievable in 3-4 hours (vs 44 indexes = 15+ hours)
5. **Natural Progression**: Logical next step after NAVIGATION.md (the master hub)

### File Profiles

#### 1. docs/index.md (Sphinx Homepage)
- **Type**: ReStructuredText (RST) / Markdown hybrid
- **Size**: ~200-300 lines (estimated)
- **Purpose**: Primary entry point for web documentation
- **Key Sections**: Welcome, toctrees (11 total), quick links, getting started
- **Expected Baseline**: 75-85/100
- **Priority**: HIGH
- **Challenges**: RST syntax, multiple toctrees, Sphinx directives

#### 2. guides/INDEX.md (User Guides Hub)
- **Type**: Markdown
- **Size**: 379 lines (known)
- **Purpose**: Coordinates all 43 user guide files (12,525 lines total)
- **Key Sections**: Learning paths, quick reference, guide categories
- **Expected Baseline**: 70-80/100
- **Priority**: CRITICAL (most complex)
- **Challenges**: Large file, many bullet lists, coordinates 43 files

#### 3. README.md (GitHub Entry Point)
- **Type**: Markdown (GitHub Flavored)
- **Size**: ~400-500 lines (estimated)
- **Purpose**: Project overview, installation, quick start
- **Key Sections**: Badges, features, installation, usage, contributing, license
- **Expected Baseline**: 65-75/100
- **Priority**: CRITICAL (first impression)
- **Challenges**: Marketing language, installation commands, external links

#### 4. CLAUDE.md (Team Memory)
- **Type**: Markdown
- **Size**: 1000+ lines (this file!)
- **Purpose**: Project conventions, session continuity, AI instructions
- **Key Sections**: 23 sections covering all project aspects
- **Expected Baseline**: 80-90/100
- **Priority**: MEDIUM (internal, but we maintain it)
- **Challenges**: Very large, many bullet lists, frequent updates

---

## QA-02 Audit Criteria

### 5-Category Scoring Model (Same as QA-01)

#### 1. Completeness (20 points)
**File-Specific Checks**:
- **docs/index.md**: All 11 toctrees present, major sections linked, version info current
- **guides/INDEX.md**: All 43 guides referenced, all 5 learning paths documented, time estimates present
- **README.md**: Standard sections (Install, Usage, Contributing, License, Citations), badges present
- **CLAUDE.md**: All 23 sections complete, phase status current, file counts accurate

**Scoring**:
- 100/100: All required sections present, no gaps
- 80-99/100: 1-2 minor omissions
- 60-79/100: 3-5 omissions
- <60/100: Major sections missing

#### 2. Accuracy (20 points)
**File-Specific Checks**:
- **docs/index.md**: Toctree paths valid, Sphinx config matches claims
- **guides/INDEX.md**: File counts match reality (43 files, 12,525 lines), time estimates reasonable
- **README.md**: Installation commands work, version numbers current, links resolve
- **CLAUDE.md**: Phase statuses match project state, file counts accurate, dates current

**Scoring**:
- 100/100: All claims verified accurate
- 80-99/100: 1-2 minor inaccuracies (outdated dates, off-by-1 counts)
- 60-79/100: 3-5 inaccuracies
- <60/100: Major factual errors

#### 3. Readability (20 points)
**Consistent Across All Files**:
- Long sentences: 0 (≤40 words per sentence)
- Dense paragraphs: ≤3 (≤5 lines per paragraph, excluding code/tables/diagrams)
- Avg sentence length: 7-10 words
- Passive voice: <10%
- Flesch Reading Ease: ≥60
- Undefined jargon: 0 (all acronyms defined on first use)

**Scoring Formula** (same as QA-01):
```
score = 100 - (long_sentences * 15) - (dense_paragraphs > 3 ? 15 : 0) - (other_issues * 15)
```

#### 4. Accessibility (20 points)
**Consistent Across All Files**:
- Heading hierarchy: No skips (H1→H2→H3, no H1→H3)
- Unicode emojis: 0 violations (Windows terminal compatibility)
- Code blocks: All labeled with language tags
- Link text: Descriptive (no "click here", "here", "link")
- Tables: All have header rows with separators

**Scoring**:
- 100/100: Perfect accessibility
- 80-99/100: 1-2 minor issues (unlabeled code blocks)
- 60-79/100: 3-5 issues
- <60/100: Critical violations (Unicode emojis, broken hierarchy)

#### 5. Link Validation (20 points)
**File-Specific Scope**:
- **docs/index.md**: First 20 links (mostly internal toctree paths)
- **guides/INDEX.md**: First 30 links (guide references)
- **README.md**: First 20 links (mix of internal + external)
- **CLAUDE.md**: First 20 links (mostly internal references)

**Scoring**:
```
score = max(0, 100 - broken_links * 10)
```

### Overall QA-02 Score

**Per-File Score**:
```
file_score = (completeness + accuracy + readability + accessibility + link_validation) / 5
```

**Overall QA-02 Score** (average of 4 files):
```
qa02_score = (docs_index + guides_index + readme + claude) / 4
```

**Target**: ≥100/100 overall (requires 100/100 for ALL 4 files)

---

## Audit Script Design

### Architecture

```
academic/qa_audits/
├── qa_02_audit_script.py          # Main multi-file audit script
├── qa_02_audit_results.json       # Batch results (all 4 files)
├── qa_02_report.md                # Human-readable report
├── individual_results/            # Per-file detailed results
│   ├── docs_index_results.json
│   ├── guides_INDEX_results.json
│   ├── README_results.json
│   └── CLAUDE_results.json
└── QA-02_EXECUTION_PLAN.md        # This file
```

### Script Features (Enhanced from QA-01)

**New Capabilities**:
1. **Multi-file batch processing** - Audit all 4 files in one run
2. **File-type detection** - RST vs Markdown, apply appropriate rules
3. **Comparative analysis** - Rank files by score, identify worst offenders
4. **Aggregated reporting** - Overall QA-02 score with per-file breakdown
5. **Priority recommendations** - Which file to fix first based on impact

**Reused from QA-01**:
- Prose filtering (exclude code blocks, tables, Mermaid diagrams)
- Sentence analysis (length, passive voice, Flesch score)
- Paragraph density detection
- Link validation with path resolution
- JSON + Markdown dual output

### Script Workflow

```python
# Pseudocode

def audit_qa02():
    """Main QA-02 audit function"""

    # Define target files
    files = [
        ("D:/Projects/main/docs/index.md", "sphinx_index"),
        ("D:/Projects/main/docs/guides/INDEX.md", "guides_hub"),
        ("D:/Projects/main/README.md", "github_readme"),
        ("D:/Projects/main/CLAUDE.md", "team_memory")
    ]

    # Audit each file
    results = []
    for filepath, file_type in files:
        print(f"[INFO] Auditing {filepath}...")
        result = audit_single_file(filepath, file_type)
        results.append(result)

        # Save individual result
        save_individual_result(result, file_type)

    # Generate comparative report
    overall_score = sum(r['overall_score'] for r in results) / len(results)

    # Rank files by score (worst first = highest priority)
    ranked = sorted(results, key=lambda r: r['overall_score'])

    # Generate reports
    save_json_report(results, overall_score)
    save_markdown_report(results, overall_score, ranked)

    print(f"\n[SUMMARY] QA-02 Overall Score: {overall_score:.1f}/100")
    print(f"[PRIORITY] Fix {ranked[0]['file']} first (score: {ranked[0]['overall_score']}/100)")

    return results, overall_score

def audit_single_file(filepath, file_type):
    """Audit one file with type-specific rules"""

    content, lines = read_file(filepath)

    # Run 5 category checks
    completeness = check_completeness(content, lines, file_type)
    accuracy = check_accuracy(content, lines, file_type)
    readability = check_readability(content, lines)  # Same for all types
    accessibility = check_accessibility(content, lines)  # Same for all types
    link_validation = check_links(content, filepath, file_type)

    # Calculate scores
    overall = (completeness['score'] + accuracy['score'] +
               readability['score'] + accessibility['score'] +
               link_validation['score']) / 5

    return {
        'file': filepath,
        'type': file_type,
        'completeness': completeness,
        'accuracy': accuracy,
        'readability': readability,
        'accessibility': accessibility,
        'link_validation': link_validation,
        'overall_score': overall
    }
```

---

## Execution Timeline

### Phase 1: Setup & Baseline (15-20 minutes)

**Tasks**:
1. Create `qa_02_audit_script.py` based on QA-01 script
2. Add multi-file support and file-type detection
3. Add comparative reporting
4. Run baseline audit on all 4 files
5. Analyze results and prioritize fixes

**Deliverables**:
- `qa_02_audit_script.py` (functional)
- `qa_02_audit_results.json` (baseline scores)
- `qa_02_report.md` (initial assessment)
- Priority list (which file to fix first)

### Phase 2: Systematic Fixes (2-3 hours)

**Strategy**: Fix files in priority order (worst score first)

**Per-File Workflow** (30-45 min each):
1. Review issues from audit report
2. Fix readability issues first (mechanical: periods, spacing)
3. Fix accuracy issues (update counts, dates, links)
4. Fix completeness issues (add missing sections)
5. Fix accessibility issues (heading hierarchy, code tags)
6. Validate links (fix broken paths)
7. Re-audit file
8. Repeat until 100/100

**Expected Order** (based on estimated baselines):
1. **README.md** (65-75/100) - Likely worst, highest priority
2. **guides/INDEX.md** (70-80/100) - Second worst, critical
3. **docs/index.md** (75-85/100) - Third priority
4. **CLAUDE.md** (80-90/100) - Easiest, fix last

### Phase 3: Verification & Reporting (15-20 minutes)

**Tasks**:
1. Run final audit on all 4 files
2. Verify 100/100 for each file
3. Verify 100/100 overall QA-02 score
4. Generate final completion report
5. Commit all changes with detailed message
6. Push to remote
7. Update project status docs

**Deliverables**:
- All 4 files at 100/100
- `QA-02_COMPLETION_REPORT.md`
- Git commit with summary
- Updated CURRENT_STATUS.md (if needed)

**Total Timeline**: 3-4 hours (can split across sessions if needed)

---

## Risk Analysis & Mitigation

### Potential Blockers

**1. CLAUDE.md Size (1000+ lines)**
- **Risk**: May have 50+ dense paragraphs, hundreds of long sentences
- **Impact**: Could take 1-2 hours to fix alone
- **Mitigation**:
  - Use automated tooling to add periods to bullet lists
  - Break large sections into subsections with blank lines
  - Consider splitting into multiple files (CLAUDE.md + CLAUDE_REFERENCE.md)

**2. README.md Marketing Language**
- **Risk**: May have "powerful framework", "seamless integration", "cutting-edge"
- **Impact**: Requires content rewriting, not just mechanical fixes
- **Mitigation**:
  - Focus on factual, technical language
  - Replace adjectives with metrics ("supports 7 controllers", not "powerful")
  - Keep fixes minimal (publication-ready, not perfect prose)

**3. guides/INDEX.md Complexity (379 lines, 43 files)**
- **Risk**: Coordinates many files, may have outdated info, many bullet lists
- **Impact**: Accuracy checks may reveal cascading issues in referenced files
- **Mitigation**:
  - Limit scope to guides/INDEX.md only (don't fix all 43 guides)
  - Verify file counts with automated script
  - Flag issues in other files for QA-03

**4. docs/index.md RST Syntax**
- **Risk**: ReStructuredText may need different parsing than Markdown
- **Impact**: Audit script may miscount sentences/paragraphs
- **Mitigation**:
  - Add RST-aware parsing (detect `.. toctree::`, `.. note::` directives)
  - Test on small RST sample first
  - Manual review if automated scores seem off

### Contingency Plans

**If Overall QA-02 Score <100/100**:
- **Acceptable**: ≥95/100 (19/20 categories at 100, 1 at 80-99)
- **Action**: Document why, commit as "QA-02 NEAR-PERFECT" with explanation
- **Example**: "docs/index.md Link Validation 90/100 due to Sphinx auto-generated links"

**If One File Blocks Progress** (e.g., CLAUDE.md too large):
- **Action**: Skip to next file, circle back later
- **Partial Success**: Commit 3/4 files at 100/100 as "QA-02 PHASE 1"
- **Defer**: Create QA-02B for problematic file

---

## Success Metrics

### Target Scores

| File | Completeness | Accuracy | Readability | Accessibility | Links | Overall |
|------|--------------|----------|-------------|---------------|-------|---------|
| docs/index.md | 100 | 100 | 100 | 100 | 100 | **100/100** |
| guides/INDEX.md | 100 | 100 | 100 | 100 | 100 | **100/100** |
| README.md | 100 | 100 | 100 | 100 | 100 | **100/100** |
| CLAUDE.md | 100 | 100 | 100 | 100 | 100 | **100/100** |
| **QA-02 Overall** | 100 | 100 | 100 | 100 | 100 | **100/100** |

### Minimum Acceptable Scores

| File | Minimum Overall | Reason |
|------|----------------|--------|
| docs/index.md | 95/100 | Sphinx auto-generation may have quirks |
| guides/INDEX.md | 100/100 | CRITICAL - user-facing hub |
| README.md | 100/100 | CRITICAL - first impression |
| CLAUDE.md | 90/100 | Internal, less critical than user-facing |
| **QA-02 Overall** | **97/100** | (sum of 100+100+95+90)/4 = 96.25 |

---

## Next Steps After QA-02

### If QA-02 Succeeds (100/100 Overall)

**Immediate Next Tasks**:
1. **QA-03**: Category Indexes (prioritize top 10 most-accessed)
2. **QA-04**: Tutorials (all 5 tutorial files)
3. **QA-05**: Theory Documentation (4 theory guides)
4. **QA-06**: API Reference (7 API modules)

**Alternative Approaches**:
- **Data-Driven**: Audit files by web analytics (most visited first)
- **Risk-Based**: Audit files by criticality (safety-critical > core > nice-to-have)
- **Comprehensive**: Audit all 3,708 files systematically (long-term project)

### If QA-02 Identifies Systemic Issues

**Example Findings**:
- "80% of bullet lists lack periods" → Create automated fix script
- "All installation commands untested" → Add CI/CD validation
- "Link rot in 30% of files" → Add link checker to pre-commit hook

**Actions**:
- Document patterns in QA-02 report
- Create automated tooling to prevent recurrence
- Consider QA-FOUNDATIONS project to fix root causes

---

## Automation Potential

### Post-QA-02 Tooling

**1. Pre-Commit Hook**:
```bash
# .git/hooks/pre-commit
python academic/qa_audits/qa_audit_staged_files.py
# Blocks commit if any staged file scores <80/100
```

**2. CI/CD Integration**:
```yaml
# .github/workflows/qa-audit.yml
- name: QA Audit on PR
  run: python academic/qa_audits/qa_audit_pr_files.py
  # Comments on PR with scores for changed files
```

**3. Documentation Dashboard**:
```python
# Generate real-time quality dashboard
python academic/qa_audits/generate_qa_dashboard.py
# Outputs: docs/_static/qa_dashboard.html
```

**4. Automated Fixes**:
```python
# Auto-fix common issues
python academic/qa_audits/auto_fix_readability.py --file README.md
# Adds periods to bullet lists, fixes spacing, no manual edits needed
```

---

## Appendix: Audit Script Enhancements

### Improvements Over QA-01

**QA-01 Script** (single-file):
- Hardcoded NAVIGATION.md path
- Single file output
- Manual interpretation of results

**QA-02 Script** (multi-file):
- Configurable file list
- Batch processing with parallel execution (optional)
- Comparative analysis
- Automated prioritization
- Per-file + aggregated reporting
- File-type aware parsing (RST vs Markdown)
- Link validation with external URL checking (optional)

### Code Structure

```python
# qa_02_audit_script.py (skeleton)

import json
from pathlib import Path
from typing import Dict, List, Tuple

# Configuration
QA02_FILES = [
    ("docs/index.md", "sphinx_index"),
    ("docs/guides/INDEX.md", "guides_hub"),
    ("README.md", "github_readme"),
    ("CLAUDE.md", "team_memory")
]

# Reuse from QA-01
from navigation_audit_script import (
    analyze_readability,
    analyze_accessibility,
    validate_file_links
)

# New functions for QA-02
def analyze_completeness_multi(content, lines, file_type):
    """File-type specific completeness checks"""
    pass

def analyze_accuracy_multi(content, lines, file_type):
    """File-type specific accuracy checks"""
    pass

def audit_single_file(filepath, file_type):
    """Audit one file"""
    pass

def audit_all_files(file_list):
    """Batch audit all QA-02 files"""
    pass

def generate_comparative_report(results):
    """Generate QA-02 report with rankings"""
    pass

def main():
    """Main entry point"""
    results, overall_score = audit_all_files(QA02_FILES)
    generate_comparative_report(results)
    print(f"[SUMMARY] QA-02 Overall: {overall_score:.1f}/100")

if __name__ == "__main__":
    main()
```

---

## Conclusion

QA-02 represents a systematic, data-driven approach to documentation quality, building on the proven QA-01 methodology. By targeting the 4 main entry points, we ensure users encounter publication-quality content from their first interaction with the project.

**Expected Outcome**: 4/4 files at 100/100, overall QA-02 score 100/100, ready for publication.

**Timeline**: 3-4 hours total (can split across sessions)

**Next Step**: Create `qa_02_audit_script.py` and run baseline audit.

---

**END OF PLAN**
