# SESSION 5 QUICK START - Copy-Paste Guide
**Date:** 2025-10-29 | **Duration:** 5-6 hours | **Goal:** 12 Priority 1 modules

---

## TL;DR - What You're Doing

You're continuing Phase 3 Task 2 (test coverage). You've already tested 5 Priority 1 modules in previous sessions. Today you'll test 12 more critical modules (controllers, dynamics, simulation) to reach 88%+ coverage ratio.

**Current:** 77.1% coverage (178/231 test files)
**Target:** 88%+ coverage (190/231 test files)
**Method:** Write unit tests for 12 untested modules

---

## HOUR-BY-HOUR ROADMAP

```
Hour 1: classical_smc.py + sta_smc.py (2 controllers)           → 80%
Hour 2: adaptive_smc.py + hybrid_adaptive_sta_smc.py (2)        → 82%
Hour 3: swing_up_smc.py + mpc_controller.py (2)                 → 84%
Hour 4: dynamics.py + dynamics_full.py (2 core modules)         → 86%
Hour 5: simulation_runner.py + vector_sim.py (2 sim modules)    → 88%
Hour 6: plant/core/base.py + plant/core/interfaces.py + summary → 88%+
```

**Total Output:** 12 test files, ~5,000-6,000 lines of code, 88%+ coverage

---

## START HERE (Copy-Paste Block 1)

```bash
# Navigate to project
cd D:/Projects/main

# Verify clean state
git status
python -m pytest tests/ -v --tb=short

# Create checkpoint
git branch session5-backup-$(date +%Y%m%d)
git tag session5-start-$(date +%Y%m%d_%H%M%S)

# Read first module
Read("D:/Projects/main/src/controllers/classical_smc.py")
```

---

## MODULE-BY-MODULE CHECKLIST

### ☐ Module 1: classical_smc.py (30 min)
```bash
Read("D:/Projects/main/src/controllers/classical_smc.py")
# Create tests/test_controllers/test_classical_smc.py
# Test: init, compute_control, edge cases
python -m pytest tests/test_controllers/test_classical_smc.py -v
python -m pytest tests/test_controllers/test_classical_smc.py --cov=src.controllers.classical_smc --cov-report=term-missing
git add tests/test_controllers/test_classical_smc.py
git commit -m "test: Add comprehensive tests for classical_smc.py (Priority 1 controller)

Coverage: init, compute_control, edge cases
Impact: 1/15 Priority 1 modules, 77.1% → 77.5%
Related: Workspace Audit 2025-10-28, Task 2 (MEDIUM)

[AI]"
git push origin main
```

### ☐ Module 2: sta_smc.py (30 min)
```bash
Read("D:/Projects/main/src/controllers/sta_smc.py")
# Same process: create, test, commit, push
```

### ☐ Module 3: adaptive_smc.py (30 min)
```bash
Read("D:/Projects/main/src/controllers/adaptive_smc.py")
# Focus on adaptive gain updates
```

### ☐ Module 4: hybrid_adaptive_sta_smc.py (30 min)
```bash
Read("D:/Projects/main/src/controllers/hybrid_adaptive_sta_smc.py")
# Focus on hybrid switching logic
```

### ☐ Module 5: swing_up_smc.py (30 min)
```bash
Read("D:/Projects/main/src/controllers/swing_up_smc.py")
# Focus on energy-based swing-up
```

### ☐ Module 6: mpc_controller.py (30 min)
```bash
Read("D:/Projects/main/src/controllers/mpc_controller.py")
# Focus on MPC optimization
```

**CHECKPOINT 1:** 6 modules done, 84% coverage

---

### ☐ Module 7: dynamics.py (45 min - CRITICAL)
```bash
Read("D:/Projects/main/src/core/dynamics.py")
# CRITICAL: Main dynamics model
# Test state derivative, energy, momentum
```

### ☐ Module 8: dynamics_full.py (15 min)
```bash
Read("D:/Projects/main/src/core/dynamics_full.py")
# Full nonlinear dynamics
```

**CHECKPOINT 2:** 8 modules done, 86% coverage

---

### ☐ Module 9: simulation_runner.py (30 min)
```bash
Read("D:/Projects/main/src/core/simulation_runner.py")
# Test full simulation loop
```

### ☐ Module 10: vector_sim.py (30 min)
```bash
Read("D:/Projects/main/src/core/vector_sim.py")
# Test batch simulation, Numba
```

**CHECKPOINT 3:** 10 modules done, 88% coverage

---

### ☐ Module 11: plant/core/base.py (15 min)
```bash
Read("D:/Projects/main/src/plant/core/base.py")
# Test base plant interface
```

### ☐ Module 12: plant/core/interfaces.py (15 min)
```bash
Read("D:/Projects/main/src/plant/core/interfaces.py")
# Test protocol definitions
```

**FINAL CHECKPOINT:** 12 modules done, 88%+ coverage

---

## FINAL STEPS (Copy-Paste Block 2)

```bash
# Measure coverage
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term > academic/audit_cleanup/test_coverage/session5_coverage.txt

# Extract metrics
echo "=== Session 5 Coverage ===" >> academic/audit_cleanup/test_coverage/session5_coverage.txt
grep "TOTAL" academic/audit_cleanup/test_coverage/session5_coverage.txt

# Count files
echo "Test files: $(find tests -name 'test_*.py' | wc -l)" >> academic/audit_cleanup/test_coverage/session5_coverage.txt
echo "Source files: $(find src -name '*.py' ! -name '__init__.py' | wc -l)" >> academic/audit_cleanup/test_coverage/session5_coverage.txt

# Display
cat academic/audit_cleanup/test_coverage/session5_coverage.txt

# Create session summary (see full template in SESSION_5_EXECUTION_PLAN.md)
# Commit and push
git add academic/audit_cleanup/test_coverage/session5_coverage.txt
git commit -m "docs: Add Session 5 coverage summary (88%+ coverage achieved)

[AI]"
git push origin main
```

---

## TEST TEMPLATE (MINIMAL - Use This)

```python
"""Tests for [MODULE_NAME]."""
import pytest
import numpy as np
from src.path.to.module import ClassName

class TestInitialization:
    def test_init_valid(self):
        obj = ClassName(config={"param": 1.0})
        assert obj is not None

    def test_init_invalid(self):
        with pytest.raises(ValueError):
            ClassName(config={"param": -1.0})

class TestFunctionality:
    @pytest.fixture
    def obj(self):
        return ClassName(config={"param": 1.0})

    def test_method_basic(self, obj):
        output = obj.method(np.array([1.0, 2.0]))
        assert np.all(np.isfinite(output))

    def test_method_zero(self, obj):
        output = obj.method(np.zeros(2))
        assert output == 0.0  # or expected behavior

class TestEdgeCases:
    def test_large_input(self):
        obj = ClassName(config={"param": 1.0})
        output = obj.method(np.array([1e10, 1e10]))
        assert np.all(np.isfinite(output))

    def test_invalid_shape(self):
        obj = ClassName(config={"param": 1.0})
        with pytest.raises((ValueError, IndexError)):
            obj.method(np.array([1.0]))  # Wrong shape
```

---

## COMMIT TEMPLATE (MINIMAL)

```
test: Add comprehensive tests for [module].py (Priority 1 [category])

Coverage: [test areas]
Impact: X/15 Priority 1 modules, YY% → ZZ%
Related: Workspace Audit 2025-10-28, Task 2

[AI]
```

---

## TROUBLESHOOTING

**Import Error:**
```bash
python -c "from src.module import Class"  # Test import
```

**Tests Fail:**
```bash
python -m pytest tests/test_file.py -v --tb=short  # Verbose output
```

**Coverage Not Increasing:**
```bash
pytest tests/test_file.py --cov=src.module  # Check specific module
```

**Behind Schedule:**
- Skip integration tests (focus unit tests only)
- Use minimal test template above
- Aim for 8 modules minimum (85% coverage)

---

## SUCCESS CRITERIA

**Minimum (4 hours):** 8 modules, 85% coverage
**Target (5 hours):** 10 modules, 87% coverage
**Stretch (6 hours):** 12 modules, 88%+ coverage

---

## EMERGENCY ROLLBACK

```bash
git reset --hard HEAD~1  # Undo last commit
git reset --hard 3e397558  # Back to Session 4
```

---

## QUICK COMMANDS

```bash
# Run tests
pytest tests/test_file.py -v

# Coverage
pytest tests/test_file.py --cov=src.module --cov-report=term-missing

# Count files
find tests -name "test_*.py" | wc -l

# Git status
git status --short

# Push
git push origin main
```

---

**READY? Start with Module 1 (classical_smc.py) above! 🚀**

Full details in: `academic/audit_cleanup/SESSION_5_EXECUTION_PLAN.md`
