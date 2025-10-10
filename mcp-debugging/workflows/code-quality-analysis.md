# Code Quality Analysis Workflow

**RUFF + VULTURE Comprehensive Code Quality Checks**

This workflow uses RUFF (linting) and VULTURE (dead code detection) MCP servers to systematically improve code quality.

## Quick Start

```bash
# Run complete workflow
python -m ruff check src/ tests/ --statistics
python -m vulture src/ tests/ --min-confidence 80
```

## Workflow Steps

### Step 1: RUFF Analysis (10 min)

**Goal:** Identify PEP 8 violations, style issues, and auto-fixable problems

```bash
# Get statistics
python -m ruff check src/ tests/ --statistics

# Generate JSON report
python -m ruff check src/ tests/ --output-format=json > ruff_analysis.json

# Check specific rule categories
python -m ruff check src/ tests/ --select E,F,W  # Errors, pyflakes, warnings
```

**Common Issues:**
- `E402` - Module import not at top of file
- `E722` - Bare except clause
- `F401` - Unused imports
- `F541` - f-string missing placeholders
- `F841` - Unused local variable

### Step 2: VULTURE Detection (10 min)

**Goal:** Find unused code (variables, functions, classes, imports)

```bash
# Standard scan (80% confidence)
python -m vulture src/ tests/ --min-confidence 80

# High-confidence only (fewer false positives)
python -m vulture src/ tests/ --min-confidence 90

# Exclude test fixtures
python -m vulture src/ --min-confidence 80
```

**Common Findings:**
- Pytest fixtures (false positives)
- Exception handler variables (`exc_type`, `exc_val`, `exc_tb`)
- Protocol stub variables (intentional placeholders)
- Dead calculations (true positives - critical)

### Step 3: Prioritize Issues (5 min)

**Critical (Fix Immediately):**
- Bare except clauses (security risk)
- Dead calculations (wasted computation)
- Unused imports (dependency bloat)

**High Priority:**
- Module import order violations
- Unused variables in production code
- Missing f-string placeholders

**Medium Priority:**
- Exception handler vars (add `_` prefix)
- Protocol stubs (document intent)

**Low Priority (False Positives):**
- Pytest fixture parameters
- Context manager protocol vars
- Abstract method parameters

### Step 4: Auto-Fix Safe Issues (10 min)

```bash
# Preview auto-fixes
python -m ruff check src/ tests/ --fix --diff

# Apply auto-fixes
python -m ruff check src/ tests/ --fix

# Apply with unsafe fixes (use cautiously)
python -m ruff check src/ tests/ --fix --unsafe-fixes
```

**Safe to Auto-fix:**
- `F401` - Remove unused imports
- `F541` - Remove f-string placeholders
- `E231` - Add missing whitespace

**Review Manually:**
- `E402` - Import location (may be intentional)
- `E722` - Bare except (need specific exception type)
- `F841` - Unused variables (may be placeholders)

### Step 5: Manual Fixes (15 min)

**E722: Bare Except**
```python
# Before
try:
    ...
except:  # BAD: catches everything including KeyboardInterrupt
    ...

# After
try:
    ...
except Exception:  # GOOD: catches normal exceptions only
    ...
```

**E402: Module Import Not at Top**
```python
# If intentional (e.g., after sys.path manipulation)
import sys
sys.path.insert(0, '...')

import my_module  # noqa: E402  # Intentional: after path setup
```

**F841: Unused Variable**
```python
# Document placeholder
def __exit__(self, exc_type, exc_val, exc_tb):  # noqa: F841
    """Context manager exit."""
    _ = exc_type  # Intentionally unused (protocol requirement)
    pass
```

### Step 6: Validate Fixes (5 min)

```bash
# Verify RUFF clean
python -m ruff check src/ tests/  # Should show 0 errors

# Run smoke tests
python -m pytest tests/ -k "test_initialization" -v

# Check imports work
python -c "from src.controllers import create_controller; print('OK')"
```

## Analysis Report Template

```markdown
# Code Quality Analysis Report
**Date:** YYYY-MM-DD
**Project:** DIP-SMC-PSO
**Tools:** RUFF + VULTURE

## Summary

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| RUFF Errors | X | 0 | -X (-100%) |
| VULTURE Issues | Y | Z | -W (-N%) |
| Critical Issues | A | 0 | -A |

## RUFF Findings

### Critical (Manual Review Required)
- [ ] E722: Bare except in `file.py:XX` - Security risk
- [ ] E402: Late import in `file.py:YY` - Review intent

### Auto-Fixed
- ✅ F401: Removed X unused imports
- ✅ F541: Removed Y f-string placeholders
- ✅ F841: Removed Z unused variables

## VULTURE Findings

### True Dead Code (Fixed)
- ✅ `function_name` (file.py:XXX) - Removed
- ✅ `unused_var` (file.py:YYY) - Removed

### False Positives (Documented)
- Pytest fixtures: X instances (ignored)
- Protocol stubs: Y instances (documented)
- Exception handlers: Z instances (prefixed with `_`)

## Actions Taken

1. Fixed E722 bare except → `except Exception:`
2. Added `# noqa: E402` to intentional late imports
3. Documented placeholder variables with `# noqa`
4. Applied RUFF auto-fixes (F401, F541, F841)
5. Validated changes with smoke tests

## Remaining Issues

- [ ] Review 3 protocol stub variables for implementation
- [ ] Consider removing 2 deprecated functions
- [ ] Update tests for 1 refactored method

## Next Steps

1. Run full test suite for validation
2. Commit changes with detailed message
3. Create GitHub issue for manual review items
```

## Common Patterns

### Pattern 1: Intentional Late Import

**Use Case:** Conditional imports, circular dependency breaking

```python
# At module top
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from my_module import MyType  # Type checking only

def my_function():
    import expensive_module  # noqa: E402  # Imported only when needed
    ...
```

### Pattern 2: Protocol Stub Variables

**Use Case:** Interface compliance without implementation

```python
class MyProtocol(Protocol):
    def method(self, param: int) -> None:
        """Protocol method."""
        _ = param  # noqa: F841  # Protocol requirement, not used in stub
        ...
```

### Pattern 3: Context Manager Unused Vars

**Use Case:** `__exit__` method signature

```python
def __exit__(
    self,
    _exc_type: type[BaseException] | None,  # Prefix with _ to show intent
    _exc_val: BaseException | None,
    _exc_tb: TracebackType | None,
) -> bool | None:
    """Exit context manager."""
    return None  # Don't suppress exceptions
```

## Best Practices

### Before Running Workflow

1. ✅ Commit current changes (`git add -A && git commit -m "..."`)
2. ✅ Create feature branch if making significant changes
3. ✅ Read through RUFF/VULTURE output completely first

### During Workflow

1. ✅ Fix critical issues manually (don't auto-fix)
2. ✅ Review each auto-fix before applying
3. ✅ Run tests after each batch of fixes
4. ✅ Commit incrementally (per issue type)

### After Workflow

1. ✅ Run full test suite (`pytest tests/ -v`)
2. ✅ Check test coverage (`pytest --cov=src`)
3. ✅ Generate final report
4. ✅ Push changes to GitHub

## Integration with CI/CD

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
```

### GitHub Actions

```yaml
# .github/workflows/code-quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install ruff vulture
      - run: ruff check src/ tests/
      - run: vulture src/ tests/ --min-confidence 80
```

## Troubleshooting

### Issue: Too Many False Positives

**Solution:** Increase VULTURE confidence threshold or create whitelist

```python
# .vulture_whitelist.py
# Whitelist for false positives

# Pytest fixtures
_.mock_controller
_.mock_dynamics
_.mock_safety_guards

# Protocol stubs
_.connection_id
_.stream_id
```

### Issue: RUFF Auto-fix Breaks Code

**Solution:** Revert and apply fixes manually

```bash
git checkout -- path/to/file.py
# Review RUFF suggestion
# Apply fix with understanding
```

### Issue: Import Errors After Fixes

**Solution:** Check for circular dependencies or missing `__init__.py`

```bash
# Test imports
python -c "from src import *; print('OK')"

# Check __init__.py files
find src/ -name "__init__.py" -exec echo {} \;
```

## Quick Reference Commands

```bash
# Full analysis
python -m ruff check src/ tests/ --statistics | tee ruff_summary.txt
python -m vulture src/ tests/ --min-confidence 80 | tee vulture_summary.txt

# Auto-fix (safe)
python -m ruff check src/ tests/ --fix

# Check specific files
python -m ruff check src/controllers/classic_smc.py
python -m vulture src/controllers/classic_smc.py --min-confidence 90

# Verify clean
python -m ruff check src/ tests/  # Should show "All checks passed!"
```

---

**Version:** 1.0.0
**Last Updated:** 2025-10-10
**Estimated Duration:** 45 minutes
