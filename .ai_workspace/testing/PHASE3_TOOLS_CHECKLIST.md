# Phase 3: Test Quality Audit - Tools Installation Checklist

**Purpose**: Install all required tools before starting Phase 3
**Estimated Time**: 15 minutes
**When to Run**: After Phase 2 completion, before starting Phase 3 Task 3.1

---

## Required Tools

### 1. radon - Code Complexity Analysis
**Purpose**: Cyclomatic complexity and maintainability index measurement

**Installation**:
```bash
pip install radon
```

**Verification**:
```bash
radon --version
radon cc --help
radon mi --help
```

**Expected**: Version information displayed, help text shows

**Usage in Phase 3**:
- Task 3.2: Analyze test complexity with radon

---

### 2. interrogate - Docstring Coverage
**Purpose**: Measure docstring coverage across test files

**Installation**:
```bash
pip install interrogate
```

**Verification**:
```bash
interrogate --version
interrogate --help
```

**Expected**: Version information displayed

**Usage in Phase 3**:
- Task 3.3: Audit docstring coverage

---

### 3. pytest-json-report - Structured Test Results
**Purpose**: Generate JSON reports of test runs for analysis

**Installation**:
```bash
pip install pytest-json-report
```

**Verification**:
```bash
python -m pytest --help | grep -i json-report
```

**Expected**: `--json-report` and `--json-report-file` options shown

**Usage in Phase 3**:
- Task 3.5: Identify flaky tests (requires 3 test runs with JSON reports)
- Task 3.6: Identify slow tests

---

### 4. pytest-timeout (Optional)
**Purpose**: Set timeouts for slow tests

**Installation**:
```bash
pip install pytest-timeout
```

**Verification**:
```bash
python -m pytest --help | grep -i timeout
```

**Expected**: `--timeout` option shown

**Usage in Phase 3**:
- Task 3.6: Identify slow tests (optional enforcement)

---

### 5. pylint (Optional - for enhanced quality checks)
**Purpose**: Additional code quality metrics

**Installation**:
```bash
pip install pylint
```

**Verification**:
```bash
pylint --version
```

**Expected**: Version information displayed

**Usage in Phase 3**:
- Optional: Enhanced code quality scoring

---

## Installation Script

**Run all at once**:
```bash
pip install radon interrogate pytest-json-report pytest-timeout pylint
```

**Verify all**:
```bash
echo "[INFO] Checking radon..."
radon --version

echo "[INFO] Checking interrogate..."
interrogate --version

echo "[INFO] Checking pytest-json-report..."
python -m pytest --help | grep json-report

echo "[INFO] Checking pytest-timeout..."
python -m pytest --help | grep timeout

echo "[INFO] Checking pylint..."
pylint --version

echo "[OK] All tools installed and verified"
```

---

## Checklist

Before starting Phase 3, verify:

- [ ] **radon installed** (for complexity analysis)
- [ ] **interrogate installed** (for docstring coverage)
- [ ] **pytest-json-report installed** (for flaky test detection)
- [ ] **pytest-timeout installed** (optional, for slow test handling)
- [ ] **pylint installed** (optional, for enhanced quality checks)
- [ ] All tools verified with `--version` or `--help` commands
- [ ] Test run with pytest-json-report:
  ```bash
  python -m pytest tests/test_core/test_core_dynamics.py --json-report --json-report-file=test_verify.json
  ls -lh test_verify.json  # Should exist
  rm test_verify.json      # Cleanup
  ```

---

## Troubleshooting

### Issue: `radon` command not found
**Solution**:
```bash
pip install --upgrade radon
# Or if using virtual environment:
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install radon
```

### Issue: `interrogate` command not found
**Solution**:
```bash
pip install --upgrade interrogate
```

### Issue: `pytest-json-report` not recognized
**Solution**:
```bash
pip install --upgrade pytest-json-report
# Verify pytest can see it:
python -m pytest --version
python -c "import pytest_jsonreport; print('OK')"
```

### Issue: Import errors during pytest
**Solution**:
```bash
# Ensure all test dependencies installed:
pip install -r requirements.txt
pip install radon interrogate pytest-json-report
```

---

## Post-Installation Test

**Quick functionality test**:

```bash
# Test radon
radon cc tests/test_core/test_core_dynamics.py -a -s
# Expected: Complexity report displayed

# Test interrogate
interrogate tests/test_core/ -v
# Expected: Docstring coverage report

# Test pytest-json-report
python -m pytest tests/test_core/ --json-report --json-report-file=academic/test_verify.json -q
ls -lh academic/test_verify.json
rm academic/test_verify.json
# Expected: JSON file created and removed

echo "[OK] All tools working correctly"
```

---

## Tool Versions (Tested)

- **radon**: ≥5.1.0 (latest)
- **interrogate**: ≥1.5.0 (latest)
- **pytest-json-report**: ≥1.5.0 (latest)
- **pytest-timeout**: ≥2.1.0 (latest)
- **pylint**: ≥2.17.0 (latest)

---

## Ready for Phase 3?

**All tools installed and verified?** → Proceed to Phase 3 Task 3.1

**Issues encountered?** → See Troubleshooting section above

---

**Checklist Created**: 2025-11-14
**Last Updated**: 2025-11-14
**Status**: Ready for use