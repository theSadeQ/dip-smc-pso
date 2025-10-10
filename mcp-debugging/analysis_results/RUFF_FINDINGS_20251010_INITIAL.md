# RUFF Analysis Report - Initial Scan
**Generated:** 2025-10-10
**Total Issues:** 21

## Summary by Rule

| Rule | Description | Count | Auto-fixable |
|------|-------------|-------|--------------|
| E402 | Module import not at top of file | 8 | No |
| E722 | Do not use bare `except` | 1 | No |
| F541 | f-string missing placeholders | 7 | Yes* |
| F401 | Unused imports | 3 | Yes* |
| F841 | Unused variables | ~2 | Yes* |

**Note:** Statistics shown earlier (68 auto-fixable) may have been from prior run.

## Critical Issues (Manual Review Required)

### E402: Module Import Not at Top (8 instances)

**Files:**
- `tests/debug/test_lyap_fresh.py` (lines 17-21)
- `tests/debug/test_minimal_import.py` (lines 5, 9, 13)

**Impact:** Violates PEP 8, may cause import issues
**Action:** Move imports to top or add `# noqa: E402` if intentional

### E722: Bare Except (1 instance)

**File:** `tests/test_documentation/test_cross_references.py:46`

```python
try:
    ...
except:  # E722: Do not use bare `except`
    ...
```

**Impact:** May hide unexpected errors
**Action:** Specify exception type (e.g., `except Exception:`)

## Auto-fixable Issues (Low Risk)

The following can be fixed with `ruff check --fix`:
- F541: f-string placeholders
- F401: Unused imports
- F841: Unused variables

## Files Affected

```
tests/debug/test_lyap_fresh.py
tests/debug/test_minimal_import.py
tests/test_documentation/test_cross_references.py
```

## Next Steps

1. **Immediate:** Fix E722 bare except manually
2. **Auto-fix:** Run `ruff check --fix` on remaining issues
3. **Review:** Verify E402 imports are intentional (debug tests)
4. **Validate:** Run test suite after fixes
