# PHASE 2: THIS WEEK - CODE ORGANIZATION IMPROVEMENTS
**Estimated Time:** 6.5 hours
**Priority:** HIGH
**Target Completion:** Within 7 days of Phase 1 completion
**Risk Level:** MEDIUM (code refactoring involved)

---

## CONTEXT & BACKGROUND

Phase 1 resolved 5 CRITICAL workspace issues (nested directories, gitignore violations, root bloat). Phase 2 focuses on **code organization improvements** to eliminate technical debt and improve maintainability:

1. **Deprecate duplicate optimizer module** (confusion between `src/optimizer/` vs `src/optimization/`)
2. **Refactor god object** (`src/controllers/factory.py` at 1,435 lines)
3. **Update documentation** (clarify config consolidation policy)

**Dependencies:**
- Phase 1 must be completed first
- All tests must pass before starting
- Clean git working tree required

**Audit Report:** `.ai_workspace/planning/workspace_audit_2025_10/AUDIT_SUMMARY.md`

---

## PRE-FLIGHT CHECKLIST

```bash
# 1. Verify Phase 1 completion
[ -f academic/audit_cleanup/phase1_validation.txt ] && echo "[OK] Phase 1 complete" || echo "[ERROR] Run Phase 1 first"

# 2. Verify clean git state
git status  # Should be clean

# 3. Run full test suite
python -m pytest tests/ -v
# All tests must pass before proceeding

# 4. Create Phase 2 backup
git branch phase2-backup-$(date +%Y%m%d)
git tag phase2-start-$(date +%Y%m%d_%H%M%S)

# 5. Create working branch (optional)
git checkout -b refactor/phase2-code-organization

# 6. Verify Python environment
python --version  # Should be 3.9+
python -c "import src; print(src.__file__)"  # Should resolve correctly
```

**STOP HERE** if tests fail or git is dirty.

---

## TASK 1: DEPRECATE src/optimizer/ MODULE

**Time Estimate:** 1 hour
**Risk:** LOW (adding warnings, no removal yet)
**Severity:** HIGH

### Problem Description

Two optimizer modules exist with confusing naming:

```
src/
├── optimizer/          # LEGACY (2 files, 905 lines)
│   ├── __init__.py
│   └── pso_optimizer.py
└── optimization/       # CURRENT (40+ files, comprehensive)
    ├── algorithms/
    │   └── pso_optimizer.py
    └── ...
```

**Impact:**
- Import confusion: `from src.optimizer import` vs `from src.optimization.algorithms import`
- Maintenance burden: Two places to update
- Unclear which is canonical

**Strategy:** Deprecate `src/optimizer/`, migrate users to `src/optimization/`

### Step-by-Step Fix

#### Step 1.1: Analyze Current Usage (15 minutes)

```bash
# Find all imports of src.optimizer
echo "=== Searching for src.optimizer imports ===" > academic/audit_cleanup/optimizer_usage.txt
grep -rn "from src.optimizer" src/ tests/ >> academic/audit_cleanup/optimizer_usage.txt || echo "None in src/tests" >> academic/audit_cleanup/optimizer_usage.txt
grep -rn "import src.optimizer" src/ tests/ >> academic/audit_cleanup/optimizer_usage.txt || echo "None in src/tests" >> academic/audit_cleanup/optimizer_usage.txt

# Check root scripts
grep -n "from src.optimizer" simulate.py streamlit_app.py >> academic/audit_cleanup/optimizer_usage.txt || echo "None in root scripts" >> academic/audit_cleanup/optimizer_usage.txt

# Display results
cat academic/audit_cleanup/optimizer_usage.txt
```

#### Step 1.2: Add Deprecation Warnings (20 minutes)

**File:** `src/optimizer/__init__.py`

```python
# src/optimizer/__init__.py
"""
DEPRECATED: This module is deprecated and will be removed in v2.0.0

Use src.optimization.algorithms.pso_optimizer instead:

    OLD:
        from src.optimizer.pso_optimizer import PSOTuner

    NEW:
        from src.optimization.algorithms.pso_optimizer import PSOTuner

Migration Guide: docs/migration/optimizer_deprecation.md
"""
import warnings

warnings.warn(
    "src.optimizer is deprecated and will be removed in v2.0.0. "
    "Use src.optimization.algorithms.pso_optimizer instead. "
    "See docs/migration/optimizer_deprecation.md for migration guide.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export from new location for backward compatibility
from src.optimization.algorithms.pso_optimizer import PSOTuner

__all__ = ["PSOTuner"]
```

**File:** `src/optimizer/pso_optimizer.py` (add header warning)

```python
# src/optimizer/pso_optimizer.py
"""
DEPRECATED: Use src.optimization.algorithms.pso_optimizer instead

This file is maintained for backward compatibility only.
"""
import warnings

warnings.warn(
    "src.optimizer.pso_optimizer is deprecated. "
    "Use src.optimization.algorithms.pso_optimizer instead.",
    DeprecationWarning,
    stacklevel=2
)

# Import everything from new location
from src.optimization.algorithms.pso_optimizer import *
```

#### Step 1.3: Create Migration Guide (15 minutes)

**File:** `docs/migration/optimizer_deprecation.md`

```bash
mkdir -p docs/migration
```

```markdown
# Migration Guide: src.optimizer → src.optimization

**Status:** DEPRECATED as of 2025-10-28
**Removal Date:** v2.0.0 (estimated Q1 2026)

## Why This Change?

- `src/optimizer/` - Legacy module (2 files, limited functionality)
- `src/optimization/` - Comprehensive framework (40+ files, future-proof)

## Migration Steps

### 1. Update Imports

**OLD:**
\`\`\`python
from src.optimizer.pso_optimizer import PSOTuner
\`\`\`

**NEW:**
\`\`\`python
from src.optimization.algorithms.pso_optimizer import PSOTuner
\`\`\`

### 2. Update Configuration

No configuration changes needed - API is identical.

### 3. Run Tests

\`\`\`bash
python -m pytest tests/test_optimization/ -v
\`\`\`

## What If I Don't Migrate?

- v1.x: Deprecation warnings (current behavior)
- v2.0.0: Import errors (src.optimizer removed)

## Need Help?

- Check examples: `examples/optimization/`
- Read docs: `docs/optimization/`
- Report issues: GitHub Issues
```

#### Step 1.4: Update Documentation (10 minutes)

Find and update all docs that reference `src.optimizer`:

```bash
# Find documentation references
grep -rn "src.optimizer" docs/ > academic/audit_cleanup/optimizer_doc_refs.txt

# Update each reference (manual review required)
# For each file, change:
#   from src.optimizer → from src.optimization.algorithms
```

**Key files to check:**
- `README.md`
- `docs/guides/getting-started.md`
- `CLAUDE.md` (if mentioned)
- Any tutorial files

#### Step 1.5: Commit Changes (5 minutes)

```bash
# Stage changes
git add src/optimizer/ docs/migration/

# Commit
git commit -m "$(cat <<'EOF'
refactor(optimizer): Deprecate src.optimizer module

HIGH PRIORITY: Add deprecation warnings for legacy optimizer module

Problem:
- Two optimizer modules: src/optimizer/ (legacy) vs src/optimization/ (current)
- Unclear which is canonical
- Maintenance burden

Solution:
- Add DeprecationWarning to src.optimizer/__init__.py
- Re-export from src.optimization for backward compatibility
- Created migration guide: docs/migration/optimizer_deprecation.md
- Updated documentation references

Migration Path:
- v1.x: Warnings (current)
- v2.0.0: Removal (Q1 2026)

Impact:
- Users see deprecation warnings on import
- No breaking changes yet (backward compatible)
- Clear migration path documented

Related: Workspace Audit 2025-10-28, Issue H3 (HIGH)
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_2_THIS_WEEK.md

[AI]
EOF
)"

# Verify warnings appear
python -c "from src.optimizer import PSOTuner" 2>&1 | grep -i deprecation
```

### Success Criteria

- [ ] Deprecation warnings added to `src/optimizer/`
- [ ] Migration guide created at `docs/migration/optimizer_deprecation.md`
- [ ] All documentation updated
- [ ] Imports still work (backward compatibility)
- [ ] Warning appears when importing from `src.optimizer`
- [ ] Tests still pass

---

## TASK 2: REFACTOR src/controllers/factory.py

**Time Estimate:** 5 hours
**Risk:** MEDIUM (affects many imports)
**Severity:** HIGH

### Problem Description

`src/controllers/factory.py` is 1,435 lines - a "god object" anti-pattern.

**Impact:**
- Hard to maintain (find specific code)
- Difficult to test (too many responsibilities)
- Merge conflicts likely

**Strategy:** Split into focused modules:

```
src/controllers/
├── factory/
│   ├── __init__.py          # Public API (re-exports)
│   ├── core.py              # Core factory logic (~400 lines)
│   ├── validation.py        # Input validation (~300 lines)
│   ├── registration.py      # Controller registration (~200 lines)
│   └── utils.py             # Helper functions (~200 lines)
└── factory.py               # Thin wrapper (imports from factory/)
```

### Step-by-Step Fix

#### Step 2.1: Analyze factory.py Structure (30 minutes)

```bash
# Create analysis directory
mkdir -p academic/audit_cleanup/factory_analysis

# Count lines by section
echo "=== factory.py Structure Analysis ===" > academic/audit_cleanup/factory_analysis/structure.txt
grep -n "^def \|^class " src/controllers/factory.py >> academic/audit_cleanup/factory_analysis/structure.txt

# Count functions
echo -e "\n=== Function Count ===" >> academic/audit_cleanup/factory_analysis/structure.txt
grep -c "^def " src/controllers/factory.py >> academic/audit_cleanup/factory_analysis/structure.txt

# Count classes
echo -e "\n=== Class Count ===" >> academic/audit_cleanup/factory_analysis/structure.txt
grep -c "^class " src/controllers/factory.py >> academic/audit_cleanup/factory_analysis/structure.txt

# Identify dependencies
echo -e "\n=== Imports ===" >> academic/audit_cleanup/factory_analysis/structure.txt
grep "^import \|^from " src/controllers/factory.py >> academic/audit_cleanup/factory_analysis/structure.txt

cat academic/audit_cleanup/factory_analysis/structure.txt
```

#### Step 2.2: Read Current factory.py (15 minutes)

```bash
# Read the entire file to understand structure
head -100 src/controllers/factory.py > academic/audit_cleanup/factory_analysis/header.txt
tail -100 src/controllers/factory.py > academic/audit_cleanup/factory_analysis/footer.txt
```

**Action:** Use Read tool to examine full file:

```python
# Read the file
Read("D:/Projects/main/src/controllers/factory.py")
```

**Identify sections:**
- Public API functions (e.g., `create_controller`)
- Validation functions
- Registration logic
- Helper utilities

#### Step 2.3: Create factory/ Directory Structure (15 minutes)

```bash
# Create directory
mkdir -p src/controllers/factory

# Create empty files
touch src/controllers/factory/__init__.py
touch src/controllers/factory/core.py
touch src/controllers/factory/validation.py
touch src/controllers/factory/registration.py
touch src/controllers/factory/utils.py
```

#### Step 2.4: Split factory.py by Responsibility (2 hours)

**This is the most complex step - requires careful analysis**

**General Strategy:**

1. **core.py** - Main factory functions:
   - `create_controller()`
   - `_instantiate_controller()`
   - Core factory logic

2. **validation.py** - Input validation:
   - `validate_controller_config()`
   - `validate_gains()`
   - All `_validate_*()` helper functions

3. **registration.py** - Controller registry:
   - `CONTROLLER_REGISTRY` dict
   - `register_controller()`
   - `get_available_controllers()`

4. **utils.py** - Helper utilities:
   - Any utility functions that don't fit above
   - Type conversions
   - Data transformations

**Example Split:**

**File:** `src/controllers/factory/core.py`

```python
"""
Core factory logic for creating controller instances.

Extracted from legacy factory.py (1,435 lines) during Phase 2 refactor.
"""
from typing import Dict, Any, Optional
from .validation import validate_controller_config, validate_gains
from .registration import CONTROLLER_REGISTRY

def create_controller(
    controller_type: str,
    config: Dict[str, Any],
    gains: Optional[list] = None
):
    """
    Create controller instance.

    Migrated from src/controllers/factory.py:123-456
    """
    # Validate inputs
    validate_controller_config(config)
    if gains:
        validate_gains(gains, controller_type)

    # Get controller class from registry
    controller_class = CONTROLLER_REGISTRY.get(controller_type)
    if not controller_class:
        raise ValueError(f"Unknown controller: {controller_type}")

    # Instantiate
    return controller_class(config=config, gains=gains)

# ... rest of core logic
```

**File:** `src/controllers/factory/__init__.py`

```python
"""
Controller factory - modular architecture.

Refactored from monolithic factory.py (1,435 lines) into focused modules:
- core.py: Main factory logic
- validation.py: Input validation
- registration.py: Controller registry
- utils.py: Helper utilities

Public API (backward compatible):
- create_controller()
- register_controller()
- get_available_controllers()
"""
from .core import create_controller
from .registration import register_controller, get_available_controllers
from .validation import validate_controller_config, validate_gains

__all__ = [
    "create_controller",
    "register_controller",
    "get_available_controllers",
    "validate_controller_config",
    "validate_gains",
]
```

**File:** `src/controllers/factory.py` (new thin wrapper)

```python
"""
Controller factory - backward compatibility wrapper.

DEPRECATED: Import from src.controllers.factory/ submodules instead.

This file maintained for backward compatibility with existing code that imports:
    from src.controllers.factory import create_controller

New code should import from submodules:
    from src.controllers.factory.core import create_controller
"""
import warnings

warnings.warn(
    "Importing from src.controllers.factory (single file) is deprecated. "
    "Use src.controllers.factory.core or src.controllers.factory subpackage instead.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export everything from factory/ subpackage
from src.controllers.factory import *
```

**IMPORTANT:** This step requires reading factory.py and carefully splitting code. Use judgment to group related functions.

#### Step 2.5: Update Imports Across Codebase (1 hour)

```bash
# Find all imports of factory
echo "=== Finding factory imports ===" > academic/audit_cleanup/factory_imports.txt
grep -rn "from src.controllers.factory import" src/ tests/ >> academic/audit_cleanup/factory_imports.txt
grep -rn "import src.controllers.factory" src/ tests/ >> academic/audit_cleanup/factory_imports.txt

# Update each import (manual review)
# Most imports can stay the same due to __init__.py re-exports
# Only update if specific submodule is needed
```

**No changes needed if using public API** (thanks to `__init__.py` re-exports):

```python
# This still works (backward compatible)
from src.controllers.factory import create_controller
```

#### Step 2.6: Run Tests (30 minutes)

```bash
# Run controller tests
python -m pytest tests/test_controllers/ -v

# Run factory-specific tests
python -m pytest tests/test_controllers/test_factory.py -v

# Run integration tests
python -m pytest tests/test_integration/ -v

# If failures, debug and fix
```

#### Step 2.7: Commit Changes (15 minutes)

```bash
# Stage changes
git add src/controllers/factory/
git add src/controllers/factory.py

# Commit
git commit -m "$(cat <<'EOF'
refactor(controllers): Split factory.py into modular subpackage

HIGH PRIORITY: Refactor god object (1,435 lines) into focused modules

Problem:
- factory.py: 1,435 lines (god object anti-pattern)
- Hard to maintain, difficult to test, merge conflict prone

Solution:
- Split into factory/ subpackage:
  - core.py: Main factory logic (~400 lines)
  - validation.py: Input validation (~300 lines)
  - registration.py: Controller registry (~200 lines)
  - utils.py: Helper utilities (~200 lines)
- factory.py: Thin backward-compat wrapper
- Public API unchanged (backward compatible)

Migration:
- Existing imports still work (no breaking changes)
- New code can import from submodules for clarity
- Deprecation warning for direct factory.py imports

Testing:
- All controller tests pass
- Integration tests pass
- Backward compatibility verified

Impact:
- Improved maintainability (focused files ~200-400 lines)
- Easier testing (isolated responsibilities)
- Reduced merge conflicts

Related: Workspace Audit 2025-10-28, Issue H5 (HIGH)
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_2_THIS_WEEK.md

[AI]
EOF
)"
```

### Success Criteria

- [ ] `factory/` subpackage created with 4-5 modules
- [ ] Each module <500 lines
- [ ] Public API unchanged (backward compatible)
- [ ] All tests pass
- [ ] Imports still work from `src.controllers.factory`
- [ ] Deprecation warning for direct `factory.py` imports

---

## TASK 3: UPDATE CLAUDE.MD CONFIG POLICY

**Time Estimate:** 30 minutes
**Risk:** LOW (documentation only)
**Severity:** MEDIUM

### Problem Description

CLAUDE.md §14 states:
> Use `.ai_workspace/` for ALL AI/dev configs

But some tools (pytest, coverage, pre-commit) conventionally expect root configs. This creates confusion.

**Strategy:** Clarify policy with explicit exceptions.

### Step-by-Step Fix

#### Step 3.1: Read Current CLAUDE.md §14 (5 minutes)

```bash
# Extract section 14
sed -n '/## 14)/,/## 15)/p' CLAUDE.md > academic/audit_cleanup/claude_section14_before.txt

cat academic/audit_cleanup/claude_section14_before.txt
```

#### Step 3.2: Update CLAUDE.md (15 minutes)

Find this section in CLAUDE.md:

```markdown
## 14) Workspace Organization & Hygiene

**Target:** ≤19 visible root items (8 dirs + 9 files + 2 runtime dirs) | ≤7 hidden dirs (.git, .github, .project, .artifacts, .cache, .vscode, .pytest_cache)
```

Add clarification after the directory rules:

```markdown
**Directory Rules (Single Source of Truth):**
- **Config consolidation**: Use `.ai_workspace/` for ALL AI/dev configs (NOT `.ai/`, `.claude/`, `.config/`, `.ai_workspace/dev_tools/`, `.mcp_servers/`)
  - `.ai_workspace/` - AI planning, education, collaboration docs
  - `.ai_workspace/claude/` - Claude Code settings
  - `.ai_workspace/config/` - Linting, commit rules, pytest configs
  - `.ai_workspace/dev_tools/` - Development scripts, automation
  - `.ai_workspace/mcp_servers/` - MCP server configurations
  - `.ai_workspace/archive/` - Archived experiments and old artifacts

**EXCEPTION - Tool-Expected Configs:**
Some tools conventionally expect configs at repository root. These are ALLOWED at root:
- `.pytest.ini` - Pytest expects root-level config
- `.coveragerc` - Coverage.py expects root-level config
- `.pre-commit-config.yaml` - Pre-commit expects root-level config
- `.gitignore` - Git expects root-level config
- `.gitattributes` - Git expects root-level config
- `.readthedocs.yaml` - ReadTheDocs expects root-level config

**RULE:** If a tool's documentation specifically requires root-level config, it's allowed. All other configs → `.ai_workspace/config/`
```

#### Step 3.3: Verify Against Current Structure (5 minutes)

```bash
# List current root configs
echo "=== Current Root Configs ===" > academic/audit_cleanup/root_configs_audit.txt
ls -la | grep "^\." | grep -E "\.(yaml|yml|ini|cfg|rc|json|toml)$" >> academic/audit_cleanup/root_configs_audit.txt

# Categorize each
echo -e "\n=== Classification ===" >> academic/audit_cleanup/root_configs_audit.txt
echo "Tool-expected (ALLOWED):" >> academic/audit_cleanup/root_configs_audit.txt
echo "  - .pytest.ini" >> academic/audit_cleanup/root_configs_audit.txt
echo "  - .coveragerc" >> academic/audit_cleanup/root_configs_audit.txt
echo "  - .pre-commit-config.yaml" >> academic/audit_cleanup/root_configs_audit.txt
echo "  - .gitignore" >> academic/audit_cleanup/root_configs_audit.txt
echo -e "\nShould be in .ai_workspace/ (REVIEW):" >> academic/audit_cleanup/root_configs_audit.txt
echo "  - .gitmessage (custom, not tool-required)" >> academic/audit_cleanup/root_configs_audit.txt

cat academic/audit_cleanup/root_configs_audit.txt
```

#### Step 3.4: Update Audit Report (5 minutes)

Update `.ai_workspace/planning/workspace_audit_2025_10/AUDIT_SUMMARY.md` to reflect this clarification:

```markdown
**Issue M6: Config File Sprawl** - RESOLVED

Original Issue: 6 configs at root should be in .ai_workspace/
Resolution: Clarified CLAUDE.md §14 with tool-expected config exceptions
Status: WORKING AS DESIGNED
```

#### Step 3.5: Commit Changes (5 minutes)

```bash
# Stage changes
git add CLAUDE.md
git add .ai_workspace/planning/workspace_audit_2025_10/

# Commit
git commit -m "$(cat <<'EOF'
docs(claude): Clarify config consolidation policy exceptions

MEDIUM PRIORITY: Update CLAUDE.md §14 with tool-expected config rules

Problem:
- CLAUDE.md §14 says "ALL configs in .ai_workspace/"
- But pytest, coverage, pre-commit expect root-level configs
- Confusion over which configs belong where

Solution:
- Added EXCEPTION section to CLAUDE.md §14
- Listed tools that require root configs (pytest, coverage, etc.)
- Rule: If tool docs require root config → allowed at root
- All other configs → .ai_workspace/config/

Impact:
- Clearer guidance for config placement
- Resolves apparent contradiction
- Aligns policy with best practices

Related: Workspace Audit 2025-10-28, Issue M6 (MEDIUM)
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_2_THIS_WEEK.md

[AI]
EOF
)"
```

### Success Criteria

- [ ] CLAUDE.md §14 includes exception rules
- [ ] Tool-expected configs listed explicitly
- [ ] Rule clearly stated (tool docs require root → allowed)
- [ ] Audit report updated
- [ ] Committed with proper message

---

## POST-PHASE VALIDATION

```bash
# 1. Verify all tests pass
echo "=== Running Full Test Suite ===" > academic/audit_cleanup/phase2_validation.txt
python -m pytest tests/ -v --tb=short 2>&1 | tee -a academic/audit_cleanup/phase2_validation.txt

# 2. Verify deprecation warnings work
echo -e "\n=== Testing Deprecation Warnings ===" >> academic/audit_cleanup/phase2_validation.txt
python -c "from src.optimizer import PSOTuner" 2>&1 | grep -i deprecation >> academic/audit_cleanup/phase2_validation.txt

# 3. Verify factory imports still work
echo -e "\n=== Testing Factory Imports ===" >> academic/audit_cleanup/phase2_validation.txt
python -c "from src.controllers.factory import create_controller; print('OK')" >> academic/audit_cleanup/phase2_validation.txt

# 4. Check file sizes
echo -e "\n=== Factory Module Sizes ===" >> academic/audit_cleanup/phase2_validation.txt
find src/controllers/factory -name "*.py" -exec wc -l {} \; >> academic/audit_cleanup/phase2_validation.txt

# 5. Verify CLAUDE.md update
echo -e "\n=== CLAUDE.md Config Policy ===" >> academic/audit_cleanup/phase2_validation.txt
grep -A5 "EXCEPTION" CLAUDE.md >> academic/audit_cleanup/phase2_validation.txt

# Display results
cat academic/audit_cleanup/phase2_validation.txt

# Summary
echo -e "\n=== PHASE 2 COMPLETION SUMMARY ==="
echo "Validation report: academic/audit_cleanup/phase2_validation.txt"
echo "Total commits: $(git log --oneline --since='7 days ago' --grep='Phase 2\|refactor' | wc -l)"
echo "Next phase: .ai_workspace/planning/workspace_audit_2025_10/PHASE_3_THIS_MONTH.md"
```

### Final Checklist

- [ ] `src/optimizer/` deprecated with warnings
- [ ] Migration guide created
- [ ] `src/controllers/factory.py` split into subpackage
- [ ] All modules <500 lines
- [ ] All tests pass
- [ ] CLAUDE.md §14 updated with exceptions
- [ ] All commits follow conventions
- [ ] Ready for Phase 3

---

## PUSH TO REMOTE

```bash
# Review all commits
git log --oneline --since="7 days ago" --author="Claude"

# Push to main
git push origin main

# Or merge feature branch
git checkout main
git merge refactor/phase2-code-organization
git push origin main
```

---

## TROUBLESHOOTING

### Issue: Tests fail after factory refactor

**Solution:** Check import paths. Ensure `__init__.py` re-exports all public functions.

```bash
# Verify public API
python -c "from src.controllers.factory import create_controller, register_controller, get_available_controllers"
```

### Issue: Circular import errors

**Solution:** Move shared types/constants to separate module:

```bash
# Create types module
touch src/controllers/factory/types.py

# Move shared types there
# Update imports to use relative imports
```

### Issue: Deprecation warnings in tests

**Solution:** Suppress warnings in test configuration:

```python
# pytest.ini
[tool.pytest.ini_options]
filterwarnings = [
    "ignore::DeprecationWarning:src.optimizer",
]
```

---

## SUCCESS METRICS

**Before Phase 2:**
- Duplicate modules: 2 (optimizer/optimization)
- God objects: 5 files >1000 lines
- Config policy: Unclear (contradictions)
- Code maintainability: 6/10

**After Phase 2:**
- Duplicate modules: 1 (optimizer deprecated)
- God objects: 4 files >1000 lines (factory fixed)
- Config policy: Clear (documented exceptions)
- Code maintainability: 7.5/10

---

## HANDOFF TO PHASE 3

**Phase 2 Complete!** 🎉

Next steps: `.ai_workspace/planning/workspace_audit_2025_10/PHASE_3_THIS_MONTH.md`

**Phase 3 Preview:**
1. Flatten deep directory structures (6-8h)
2. Increase test coverage to 1:1 (20h)
3. Clean legacy documentation (2h)

**Estimated Phase 3 Time:** 28-30 hours
