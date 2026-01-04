# Architectural Standards & Invariants

**Version**: 1.0
**Date**: January 4, 2026
**Status**: ACTIVE - These patterns are INTENTIONAL architecture

This document contains the complete architectural standards for the DIP-SMC-PSO project. These patterns were established via comprehensive structural analysis on Dec 29, 2025 using Sequential-thinking MCP + 3 Explore agents + manual verification.

## Table of Contents

1. [Intentional Architectural Patterns](#intentional-architectural-patterns)
2. [Directory Placement Rules](#directory-placement-rules)
3. [Root Directory Standards](#root-directory-standards)
4. [Malformed Names](#malformed-names)
5. [Import Classification Rules](#import-classification-rules)
6. [Structural Analysis Protocol](#structural-analysis-protocol)
7. [Quality Gates](#quality-gates)
8. [Lessons Learned](#lessons-learned)
9. [Pre-commit Hook Requirements](#pre-commit-hook-requirements)
10. [Quick Reference Card](#quick-reference-card)

---

## Intentional Architectural Patterns

**CRITICAL**: These patterns may LOOK like issues but are CORRECT and serve specific purposes. DO NOT "fix" them.

### Pattern 1: Compatibility Layer (src/optimizer/ → src/optimization/)

**Structure**:
```
src/optimizer/          [53 KB, 5 files]   - Backward-compatibility shim
src/optimization/       [1.4 MB, 48 files] - Production modular architecture
```

**Purpose**: Enable gradual migration from legacy code without breaking existing imports

**Evidence**: `src/optimizer/pso_optimizer.py` re-exports from `src/optimization/algorithms/pso_optimizer.py`

**Status**: [OK] INTENTIONAL - Similar to Django, NumPy migration patterns

**Action**: NEVER consolidate these - backward compatibility required

### Pattern 2: Re-export Chain (simulation_context.py exists in 3 locations)

**Structure**:
```
src/core/simulation_context.py                [13 lines]  - Compat layer
src/simulation/context/simulation_context.py  [116 lines] - Secondary shim
src/simulation/core/simulation_context.py     [203 lines] - CANONICAL SOURCE
```

**Purpose**: Multiple import paths for flexibility (legacy + new architecture)

**Evidence**: All re-export to single canonical source (no duplication of logic)

**Status**: [OK] INTENTIONAL - Provides import path flexibility

**Action**: DO NOT consolidate unless migrating entire codebase

### Pattern 3: Model Variants (8 dynamics files)

**Structure**:
```
src/plant/models/simplified/dynamics.py  - SimplifiedDIPDynamics (fast, low accuracy)
src/plant/models/full/dynamics.py        - FullDIPDynamics (slow, high accuracy)
src/plant/models/lowrank/dynamics.py     - LowRankDIPDynamics (medium tradeoff)
src/plant/models/base/dynamics_interface.py - DynamicsInterface (abstract)
src/core/dynamics.py                      - Compatibility re-export
```

**Purpose**: Different physics accuracy/computational cost tradeoffs

**Evidence**: Each model serves different use cases (real-time vs research vs production)

**Status**: [OK] INTENTIONAL - Not duplication, legitimate variants

**Action**: NEVER consolidate - these are different implementations

### Pattern 4: Framework vs Test Files (test_automation.py)

**File**: `src/interfaces/hil/test_automation.py` (581 lines, 23 KB)

**Classification**: PRODUCTION CODE (HIL testing framework)

**NOT**: A test file (despite the confusing name)

**Evidence**:
- Exported in `src/interfaces/hil/__init__.py` as public API
- Used by production code in `enhanced_hil.py`
- Provides 8 framework classes: HILTestFramework, TestSuite, TestCase, etc.
- Similar to pytest (framework) vs test_*.py (actual tests)

**Status**: [OK] CORRECTLY PLACED in src/ - this IS production infrastructure

**Action**: NEVER move to tests/ - it's a framework, not tests

**Optional**: Consider renaming to `hil_test_framework.py` (cosmetic only)

---

## Directory Placement Rules

### src/ Directory (Production Code Only)

**Purpose**: Core library package (importable, distributable)

**Contents**:
- Controllers, plant models, optimization algorithms
- Utilities, configurations, interfaces
- Frameworks and infrastructure (test_automation.py)
- Re-export compatibility layers

**NEVER Put Here**:
- Actual pytest test files (test_*.py) → Use tests/
- Development scripts → Use scripts/
- Build artifacts → Use .cache/ or archive/
- Temporary files → Use .cache/

### scripts/ Directory (Development Tools)

**Purpose**: Automation scripts, utilities (executed, not imported)

**Contents**:
- Documentation generation tools
- Benchmark analysis scripts
- Migration utilities
- Quality validation tools

**NEVER Put Here**:
- Core library code → Use src/
- Test files → Use tests/
- Production entry points → Use project root (simulate.py, etc.)

### tests/ Directory (Pytest Test Files)

**Purpose**: Test suite (mirrors src/ structure)

**Contents**:
- test_*.py files (actual pytest tests)
- test_*/  directories (mirroring src/ structure)
- Fixtures, conftest.py, test utilities

**NEVER Put Here**:
- Testing frameworks → Use src/ (they're production infrastructure)
- Test automation infrastructure → Use src/
- Development scripts → Use scripts/

**Coverage Target**: 92.9% of core modules (13/14 validated)

---

## Root Directory Standards

**Target**: ≤19 visible items
**Current**: 14 visible items (26% under target) [OK]

### ALLOWED at Root

- Entry points: simulate.py, streamlit_app.py, setup.py
- Configs: config.yaml, requirements.txt, package.json
- Documentation: README.md, CHANGELOG.md, CLAUDE.md
- Directories: src/, scripts/, tests/, academic/

### NEVER at Root

- Backup files (.tar.gz, .zip) → Use .ai_workspace/archive/
- Build artifacts (.aux, .log, .pyc) → Use .cache/ or archive/
- Test files (test_*.py) → Use tests/
- Windows artifacts (nul) → Delete immediately
- Temporary files → Use .cache/

**Quality Gate**: If root exceeds 19 items, immediate cleanup required

---

## Malformed Names

### NEVER Create

- Directories with braces: `{core,data_exchange,...}/` [CRITICAL ERROR]
- Directories with spaces: `my folder/` [ERROR]
- Files named after devices: `nul`, `con`, `prn` (Windows) [ERROR]
- Unicode in Windows paths: Use ASCII only [ERROR]

### Detection

```bash
# Check for malformed names
find . -name "*{*}*" -o -name "*}*" -o -name "* *"
```

### Prevention

Add pre-commit hook to validate directory/file names (see section below)

---

## Import Classification Rules

### Before Moving ANY File, Check

1. **Is it exported in __init__.py?** → Production code, STAYS in src/
2. **Is it imported by production code?** → Production code, STAYS in src/
3. **Does it provide framework/infrastructure?** → Production code, STAYS in src/
4. **Does it have pytest imports?** → Test file, GOES to tests/
5. **Does filename match test_*.py?** → Probably test, but VERIFY first (see test_automation.py)

### False Positive Example

- `test_automation.py` LOOKS like test file (name pattern)
- Actually HIL testing framework (production infrastructure)
- STAYS in src/ because it's exported and used by production code

### Validation Checklist

```bash
# Check if file is exported
grep -r "from .filename import" src/*/__init__.py

# Check if production code imports it
grep -r "from src.path.filename import" src/

# Check for pytest usage
grep "import pytest" filename.py
grep "from pytest" filename.py
```

---

## Structural Analysis Protocol

### When to Analyze (MANDATORY triggers)

- After major refactoring (>50 files changed)
- Before release/publication
- Quarterly architectural reviews
- When root directory exceeds 19 items
- When unclear if file placement is correct

### Analysis Method (proven effective Dec 29, 2025)

1. **Sequential-thinking MCP**: Systematic breakdown of all areas
2. **3 Parallel Explore Agents**: Validate findings independently
   - Agent 1: src/ duplication check
   - Agent 2: Root directory audit
   - Agent 3: tests/ structure validation
3. **Manual Verification**: Cross-check agent findings with import analysis
4. **Quality Gates**: 6 gates (critical=0, high≤3, tests=100%, root≤19, malformed=0, empty=0)

### Documentation

- Create `.ai_workspace/planning/STRUCTURAL_ANALYSIS_YYYY-MM-DD.md`
- Include methodology, findings, corrections, quality gates
- Commit with `docs(analysis):` prefix

---

## Quality Gates

### Gates (ENFORCE STRICTLY)

| Gate | Target | Enforcement |
|------|--------|-------------|
| Critical issues | 0 | [MANDATORY] BLOCK commits if any exist |
| High-priority issues | ≤3 | [REQUIRED] Document exceptions |
| Test pass rate | 100% | [MANDATORY] All tests must pass |
| Root items (visible) | ≤19 | [REQUIRED] Cleanup if exceeded |
| Malformed names | 0 | [MANDATORY] BLOCK commits if any exist |
| Empty directories | 0 | [RECOMMENDED] Cleanup during reviews |

### Verification

```bash
# Before any major commit
ls -1 | wc -l                    # ≤19 visible
find . -name "*{*}*"             # 0 results
find tests/ -type d -empty       # 0 results
pytest tests/ --tb=short         # 100% pass
```

---

## Lessons Learned

### Dec 29, 2025 Analysis Corrections

**NEVER REPEAT these mistakes:**

1. **Filename alone is insufficient for classification**
   - test_automation.py LOOKED like test file
   - Actually production HIL framework
   - ALWAYS check imports and usage before moving

2. **Compatibility layers are intentional, not duplication**
   - optimizer/ → optimization/ enables gradual migration
   - DO NOT consolidate without full codebase migration plan

3. **Re-export chains serve a purpose**
   - Multiple import paths enable backward compatibility
   - Document rather than remove

4. **Parallel validation saves time but needs manual review**
   - 3 agents in 30 min vs 90 min sequential
   - Still caught 1 false positive (test_automation.py)
   - Final human verification is essential

---

## Pre-commit Hook Requirements

**Add to `.git/hooks/pre-commit`** (future implementation):

```bash
#!/bin/bash
# Enforce architectural standards

# Check root item count
ROOT_COUNT=$(ls -1 | wc -l)
if [ $ROOT_COUNT -gt 19 ]; then
  echo "[ERROR] Root has $ROOT_COUNT items (max 19)"
  exit 1
fi

# Check for malformed names
if find . -name "*{*}*" -o -name "*}*" | grep -q .; then
  echo "[ERROR] Malformed directory/file names detected"
  exit 1
fi

# Check for Windows device names
if find . -iname "nul" -o -iname "con" -o -iname "prn" | grep -q .; then
  echo "[ERROR] Windows device file names detected"
  exit 1
fi

# Verify tests pass
pytest tests/ --tb=short -q || exit 1
```

---

## Quick Reference Card

### When Classifying a File

1. Is filename `test_*.py`? → Probably test, but CHECK imports first
2. Exported in `__init__.py`? → Production code (src/)
3. Used by production code? → Production code (src/)
4. Framework/infrastructure? → Production code (src/)
5. Has pytest imports? → Test file (tests/)
6. Development tool? → Script (scripts/)

### When Creating Directories

- ✓ Use lowercase: `my_directory/`
- ✓ Use underscores: `my_long_directory_name/`
- ✗ NO braces: `{dir1,dir2}/`
- ✗ NO spaces: `my directory/`
- ✗ NO device names: `nul/`, `con/`, `prn/`

### When Moving Files

- ALWAYS use `git mv` (preserves history)
- ALWAYS check imports first (grep for usage)
- ALWAYS run tests after move
- NEVER batch moves without verification

### Root Directory Hygiene

- Target: ≤19 visible items (currently 14) [OK]
- Backups → .ai_workspace/archive/
- Build artifacts → .cache/ or archive/
- Temporary files → .cache/
- Check weekly: `ls -1 | wc -l`

---

## See Also

- `.ai_workspace/planning/STRUCTURAL_ANALYSIS_2025-12-29.md` - Complete analysis report
- `.ai_workspace/planning/CORRECTION_test_automation_20251229.md` - False positive analysis
- `.ai_workspace/planning/FINAL_SUMMARY_2025-12-29.md` - Comprehensive summary
- `CLAUDE.md` Section 25 - Quick reference version

---

**Last Updated**: January 4, 2026
**Next Review**: Quarterly (April 2026) or after major refactoring
