# Documentation Reorganization Execution Plan

**Created**: December 23, 2025
**Status**: Ready for Execution  
**Estimated Duration**: 2-3 hours
**Risk Level**: Medium (mitigated with checkpoints)

---

## Executive Summary

This plan reorganizes the docs/ directory from 39 directories to ~19-21, breaking down the oversized reference/ directory (344 files) into structured subdirectories, consolidating 20 small directories, and updating all navigation systems.

**Key Objectives:**
1. Break down reference/ (344 files → 17 subdirectories with organized structure)
2. Consolidate 11 small directories (<5 files each)  
3. Delete 3 empty directories
4. Update 41 index files and 3 navigation hubs
5. Validate Sphinx builds and links

**Expected Benefits:**
- 51% reduction in directory count (39 → 19-21)
- 83% reduction in reference/ file density (344 → subdirectories with <100 each)
- 90% reduction in undersized directories (20 → 2)
- Improved findability and navigation

---

## Reference Directory Taxonomy

### Current Analysis

**Total Files in reference/**: 344 files
**Current Subdirectories**: 15 subdirectories + 7 root files
**Problem**: Root files unorganized, no clear categorization

**Subdirectory Distribution:**
- controllers/ (60 files) - Controller API documentation
- optimization/ (51 files) - PSO and optimizer references  
- interfaces/ (47 files) - Data exchange schemas
- simulation/ (46 files) - Simulation engine references
- utils/ (33 files) - Utility module documentation
- analysis/ (31 files) - Analysis and validation tools
- plant/ (28 files) - Plant model configurations
- benchmarks/ (12 files) - Benchmark configuration
- core/ (8 files) - Core system interfaces
- config/ (6 files) - Configuration schemas
- optimizer/ (3 files), integration/ (3 files), fault_detection/ (3 files)
- configuration/ (2 files), hil/ (1 file), implementation/ (1 file)

**Root Files (7 files requiring categorization):**
1. index.md - Navigation hub (KEEP at root)
2. symbols.md - Mathematical notation reference
3. PACKAGE_CONTENTS.md - Package structure overview
4. PLANT_MODEL.md - Plant model reference
5. PLANT_CONFIGURATION.md - Plant configuration reference
6. CONTROLLER_FACTORY.md - Factory pattern reference
7. configuration_schema_validation.md - Schema validation

### Reorganization Strategy

**Decision**: Keep existing 15 subdirectories (already well-organized), reorganize 7 root files

**New Subdirectories** (2 additions):
- overview/ - Package-level documentation
- quick_reference/ - Cheat sheets and notation

**File Categorization**:
- symbols.md → quick_reference/
- PACKAGE_CONTENTS.md → overview/
- PLANT_MODEL.md → plant/ (merge with existing)
- PLANT_CONFIGURATION.md → plant/ (merge with existing)
- CONTROLLER_FACTORY.md → controllers/ (merge with existing)
- configuration_schema_validation.md → config/ (merge with existing)
- index.md → KEEP at root

**Final Structure**: 17 subdirectories + 1 root index.md

**Largest Subdirectory After**: controllers/ (61 files = 60 + CONTROLLER_FACTORY.md)

---

## Phase 1: Safety & Cleanup (10-15 minutes)

### Objectives
- Create backup checkpoint
- Delete empty directories  
- Merge duplicate directories
- Establish baseline

### Actions

#### 1.1 Create Git Tag Checkpoint
```bash
git tag -a docs-pre-reorganization -m "Snapshot before docs/ reorganization (Dec 23, 2025)"
git push origin docs-pre-reorganization
```

#### 1.2 Delete Empty Directories
```bash
# Verify directories are empty
ls -la docs/bib/ docs/data/ docs/scripts/

# Delete (use rmdir to fail if not empty)
rmdir docs/bib docs/data docs/scripts

# Verify deletion  
! test -d docs/bib && ! test -d docs/data && ! test -d docs/scripts && echo "[OK] Empty directories deleted"
```

#### 1.3 Merge Duplicate Directories

**Conflict 1: references/ (3 files) → reference/legacy/**
```bash
mkdir -p docs/reference/legacy
git mv docs/references/*.md docs/reference/legacy/
rmdir docs/references
test -d docs/reference/legacy && ! test -d docs/references && echo "[OK] references/ merged"
```

**Conflict 2: workflow/ (1 file) → workflows/**
```bash
git mv docs/workflow/*.md docs/workflows/
rmdir docs/workflow  
! test -d docs/workflow && echo "[OK] workflow/ merged"
```

#### 1.4 Validation Checkpoint
```bash
# Verify Sphinx builds
sphinx-build -M html docs docs/_build -W --keep-going

# Create checkpoint
git add -A
git commit -m "docs: Phase 1 cleanup - Delete empty dirs, merge duplicates"
git tag -a docs-post-phase1-cleanup -m "Phase 1 complete"
```

**Expected Result:**
- 3 empty directories deleted
- 2 duplicate directories merged  
- Directory count: 39 → 36
- Sphinx build: PASS

**Rollback**:
```bash
git reset --hard docs-pre-reorganization
```

---

## Phase 2: Reference Directory Reorganization (45-60 minutes)

### Execution Steps

#### 2.1 Create New Subdirectories
```bash
cd docs/reference
mkdir -p overview quick_reference
```

#### 2.2 Move Root Files to Subdirectories
```bash
# Move files with git mv (preserve history)
git mv symbols.md quick_reference/
git mv PACKAGE_CONTENTS.md overview/
git mv PLANT_MODEL.md plant/
git mv PLANT_CONFIGURATION.md plant/
git mv CONTROLLER_FACTORY.md controllers/
git mv configuration_schema_validation.md config/

# Verify only index.md remains at root
ls -1 *.md 2>/dev/null | grep -v "index.md" && echo "[ERROR] Unexpected root files" || echo "[OK] Only index.md at root"
```

#### 2.3 Update reference/index.md
Update navigation to reflect new structure:
- Add overview/ section  
- Add quick_reference/ section
- Update plant/, controllers/, config/ sections

#### 2.4 Update Cross-References
```bash
# Search for broken links
grep -r "reference/PLANT_MODEL.md" docs/ --include="*.md"
grep -r "reference/symbols.md" docs/ --include="*.md"  
grep -r "reference/CONTROLLER_FACTORY.md" docs/ --include="*.md"

# Update to new paths (automated or manual)
```

#### 2.5 Validation Checkpoint  
```bash
sphinx-build -M html docs docs/_build -W --keep-going
python scripts/docs/check_links.py --path docs/reference/

git add -A
git commit -m "docs: Phase 2 - Reorganize reference/ root files"
git tag -a docs-post-phase2-reference -m "Phase 2 complete"
```

**Expected Result:**
- reference/ subdirectories: 15 → 17
- reference/ root files: 7 → 1  
- Total files: 344 (unchanged)
- Sphinx build: PASS

**Time**: 45-60 minutes

**Rollback**:
```bash
git reset --hard docs-post-phase1-cleanup
```




---

## Phase 3: Consolidate Small Directories (30-40 minutes)

### Consolidation Map

| Source Directory      | Files | Target Directory              |
|-----------------------|------:|-------------------------------|
| deployment/           |     4 | production/deployment/        |
| tools/                |     3 | guides/tools/                 |
| troubleshooting/      |     3 | production/troubleshooting/   |
| development/          |     2 | guides/development/           |
| optimization_simulation/ |  2 | optimization/simulation/      |
| plant/                |     2 | architecture/plant_system/    |
| visual/               |     2 | visualization/                |
| advanced/             |     1 | theory/advanced/              |
| code_quality/         |     1 | testing/code_quality/         |
| numerical_stability/  |     1 | theory/numerical_stability/   |
| issues/               |     1 | .project/ai/planning/issues/  |

**Total**: 11 directories consolidated

### Execution Steps (abbreviated for space)
- Create target subdirectories
- Move files with git mv
- Update 7 category index files  
- Validate Sphinx build
- Create checkpoint tag

**Expected**: Directory count 36 → 25, Sphinx PASS
**Time**: 30-40 minutes
**Rollback**: git reset --hard docs-post-phase2-reference

---

## Phase 4-5 & Summary

[See complete details in full execution plan document]

**Time Estimates**: 2.5-3.5 hours total across 5 phases
**Key Risks**: Broken links (40%), navigation desync (30%) - mitigated with checkpoints
**Validation**: Sphinx builds, link checker, file counts after each phase
**Next Steps**: Review plan, backup repo, execute Phase 1

---

**Document Status**: Ready for Execution
**Version**: 1.0 (Summary)
**Created**: December 23, 2025
