# Scripts Directory - Testing Infrastructure

This directory contains testing and quality assurance scripts for the DIP-SMC-PSO project.

---

## Coverage Quality Gates

### check_coverage_gates.py

**Purpose:** Validates test coverage against 3-tier quality gates.

**Usage:**
```bash
# Run with default settings (coverage.xml)
python scripts/check_coverage_gates.py

# Specify custom coverage report
python scripts/check_coverage_gates.py --xml path/to/coverage.xml

# Strict mode (fail on any gate violation)
python scripts/check_coverage_gates.py --strict

# Quiet mode (summary only)
python scripts/check_coverage_gates.py --quiet
```

**Quality Gates:**

**Tier 1 - MINIMUM:**
- Overall coverage >= 85%

**Tier 2 - CRITICAL:**
- Core simulation engine >= 95%
- PSO optimizer >= 95%

**Tier 3 - SAFETY-CRITICAL:**
- Controllers >= 95%
- Plant models >= 95%

**Exit Codes:**
- `0` - All required gates passed
- `1` - One or more gates failed
- `2` - Coverage report not found

**CI/CD Integration:**
```yaml
- name: Validate coverage gates
  run: python scripts/check_coverage_gates.py
```

---

## Unicode Encoding Diagnostics

### diagnose_pytest_unicode.py

**Purpose:** Diagnoses pytest Unicode encoding issues on Windows.

**Usage:**
```bash
python scripts/diagnose_pytest_unicode.py
```

**Output:**
- Platform and locale information
- Environment variable status (PYTHONIOENCODING, PYTHONUTF8)
- Stream encoding configuration
- Unicode character compatibility test
- Recommendations for fixing encoding issues

**When to Use:**
- Setting up development environment on Windows
- Debugging pytest output errors
- Verifying UTF-8 encoding configuration

**Documentation:** See `scripts/pytest_unicode_diagnosis.md` for complete analysis.

---

## Related Documentation

- **Testing Standards:** `.ai/config/testing_standards.md`
- **Coverage Configuration:** `.coveragerc`
- **Pytest Configuration:** `.pytest.ini`
- **Measurement Infrastructure:** `.artifacts/checkpoints/L1P1_MEASUREMENT/`

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2025-11-11 | Created coverage gates validator | Agent 1 (Measurement Infrastructure) |
| 2025-11-11 | Added Unicode diagnostic tool | Agent 1 |
| 2025-11-11 | Initial README for scripts directory | Agent 1 |
