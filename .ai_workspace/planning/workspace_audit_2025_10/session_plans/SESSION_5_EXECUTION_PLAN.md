# SESSION 5 EXECUTION PLAN - Phase 3 Workspace Cleanup
**Date:** 2025-10-29
**Session Duration:** 5-6 hours
**Focus:** Task 2 (Test Coverage) - Priority 1 Modules

---

## EXECUTIVE SUMMARY

**Phase 3 Status:**
- **Task 1 (Flatten Directories):** NOT STARTED - Estimated 6-8 hours
- **Task 2 (Test Coverage):** IN PROGRESS - 53/231 modules untested (77.1% ratio)
- **Task 3 (Legacy Docs):** NOT STARTED - Estimated 2 hours

**Recent Progress (Last 5 commits):**
- Session 4: Completed physics_matrices.py tests (5th Priority 1 module)
- Session 4: Completed simulation_context.py tests (4th Priority 1 module)
- Session 3: Completed time_domain.py tests (3rd Priority 1 module)
- Session 3: Completed 2 Priority 1 modules (59 tests)
- Session 2: Completed interfaces.py tests

**Current State:**
- Source files: 231 total
- Test files: 178 total
- Coverage ratio: 77.1% (target: 100%)
- Untested modules: 53
- Line coverage: ~70% (target: ≥95%)

**Session 5 Goal:**
Complete 10-15 Priority 1 modules (CRITICAL controllers, dynamics, core simulation)
to reach **85%+ test coverage ratio** by end of session.

---

## PHASE 3 OVERVIEW (3 Major Tasks)

### Task 1: Flatten Deep Directory Structures (6-8 hours)
**Status:** NOT STARTED
**Dependencies:** None (can start anytime)
**Impact:** Cleaner imports, easier navigation
**Risk:** MEDIUM (many imports to update)

**Subtasks:**
1. Analyze directory depths (1h)
2. Create flattening plan (1h)
3. Flatten src/ directories (2h)
4. Flatten docs/ directories (1.5h)
5. Run tests and rebuild (1h)
6. Commit changes (30min)

**Recommendation for Session 5:** DEFER to Session 6
- Reason: Test coverage is more critical (affects code quality)
- Task 1 is mechanical and can be done after tests are complete
- Completing tests first enables better validation of refactoring

---

### Task 2: Increase Test Coverage to 1:1 (20 hours total)
**Status:** IN PROGRESS - 10 hours invested, 10 hours remaining
**Dependencies:** None
**Impact:** Code quality, refactoring confidence, documentation
**Risk:** LOW (additive only, no changes to existing code)

**Subtasks:**
1. ✅ Identify untested modules (COMPLETE - 53 modules identified)
2. ✅ Prioritize by criticality (COMPLETE - see priorities below)
3. 🔄 Write tests for Priority 1 modules (IN PROGRESS - 5/20 complete)
4. ⏳ Write tests for Priority 2 modules (NOT STARTED - 30 modules)
5. ⏳ Write tests for Priority 3 modules (NOT STARTED - 15 modules)
6. ⏳ Write tests for Priority 4 modules (NOT STARTED - 3 modules)
7. ⏳ Measure final coverage (30min)
8. ⏳ Commit changes (30min)

**Recommendation for Session 5:** PRIMARY FOCUS
- Goal: Complete 10-15 Priority 1 modules
- Expected outcome: 85%+ test coverage ratio (195+ test files)
- Time: 5-6 hours (this session)

---

### Task 3: Clean Legacy Documentation (2 hours)
**Status:** NOT STARTED
**Dependencies:** None (can start anytime)
**Impact:** Cleaner docs, less confusion
**Risk:** LOW (documentation only)

**Subtasks:**
1. Identify legacy documentation (30min)
2. Delete obsolete files (30min)
3. Archive historical files (30min)
4. Update stale documentation (30min)

**Recommendation for Session 5:** DEFER to Session 7
- Reason: Low priority, low impact
- Can be done after test coverage is complete
- Documentation cleanup is mostly manual review

---

## SESSION 5 STRATEGY: PRIORITY 1 MODULES

### Priority 1 Modules (CRITICAL - Test First)
**Total:** ~20 modules in controllers, core, simulation, dynamics

**Already Tested (5 modules):**
1. ✅ src/simulation/core/interfaces.py (Session 3)
2. ✅ src/simulation/core/time_domain.py (Session 3)
3. ✅ src/simulation/core/simulation_context.py (Session 4)
4. ✅ src/core/physics_matrices.py (Session 4)
5. ✅ src/simulation/core/domain.py (JUST CREATED - untracked file exists)

**Remaining Priority 1 Modules (~15 modules):**

**Category A: Controllers (HIGH IMPACT - 6 modules, 3 hours)**
- src/controllers/adaptive_smc.py (~30 min)
- src/controllers/classical_smc.py (~30 min)
- src/controllers/hybrid_adaptive_sta_smc.py (~30 min)
- src/controllers/sta_smc.py (~30 min)
- src/controllers/swing_up_smc.py (~30 min)
- src/controllers/mpc_controller.py (~30 min)

**Category B: Core Dynamics (HIGH IMPACT - 4 modules, 2 hours)**
- src/core/dynamics.py (~45 min)
- src/core/dynamics_full.py (~45 min)
- src/plant/core/base.py (~15 min)
- src/plant/core/interfaces.py (~15 min)

**Category C: Simulation Engine (MEDIUM IMPACT - 5 modules, 2 hours)**
- src/core/simulation_runner.py (~30 min)
- src/core/vector_sim.py (~30 min)
- src/simulation/analysis/performance.py (~20 min)
- src/simulation/analysis/stability.py (~20 min)
- src/simulation/core/events.py (~20 min)

---

## SESSION 5 TASK BREAKDOWN (5-6 hours)

### Hour 1: Controllers Block 1 (2 modules)
**Time:** 60 minutes
**Goal:** Test classical_smc.py and sta_smc.py

#### Task 1.1: Test src/controllers/classical_smc.py (30 min)
```bash
# Read the module
Read("D:/Projects/main/src/controllers/classical_smc.py")

# Create test file
mkdir -p tests/test_controllers
touch tests/test_controllers/test_classical_smc.py

# Write comprehensive tests (see template below)
# - Initialization (valid/invalid config)
# - Control computation (basic, zero state, large deviations)
# - Edge cases (NaN, inf, wrong shapes)

# Run tests
python -m pytest tests/test_controllers/test_classical_smc.py -v

# Measure coverage
python -m pytest tests/test_controllers/test_classical_smc.py --cov=src.controllers.classical_smc --cov-report=term-missing

# Commit
git add tests/test_controllers/test_classical_smc.py
git commit -m "test: Add comprehensive tests for classical_smc.py (Priority 1 controller)

MEDIUM PRIORITY: Test classical SMC controller (Priority 1 module)

Coverage:
- Initialization with valid/invalid configs
- Control computation for various states
- Edge cases (NaN, inf, wrong shapes)
- Sliding surface and control law validation

Impact:
- 1/15 Priority 1 modules complete
- Coverage ratio: 77.1% → 77.5%

Related: Workspace Audit 2025-10-28, Task 2 (MEDIUM)
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_3_THIS_MONTH.md

[AI]"
git push origin main
```

#### Task 1.2: Test src/controllers/sta_smc.py (30 min)
```bash
# Same process as 1.1
Read("D:/Projects/main/src/controllers/sta_smc.py")
# Create test file, write tests, run, commit
```

**Checkpoint:** 2/15 Priority 1 modules complete (80% coverage ratio)

---

### Hour 2: Controllers Block 2 (2 modules)
**Time:** 60 minutes
**Goal:** Test adaptive_smc.py and hybrid_adaptive_sta_smc.py

#### Task 2.1: Test src/controllers/adaptive_smc.py (30 min)
```bash
Read("D:/Projects/main/src/controllers/adaptive_smc.py")
# Focus on adaptive gain updates
# Test adaptation rate, convergence
```

#### Task 2.2: Test src/controllers/hybrid_adaptive_sta_smc.py (30 min)
```bash
Read("D:/Projects/main/src/controllers/hybrid_adaptive_sta_smc.py")
# Test hybrid switching logic
# Test mode transitions
```

**Checkpoint:** 4/15 Priority 1 modules complete (82% coverage ratio)

---

### Hour 3: Controllers Block 3 + Dynamics (2 modules)
**Time:** 60 minutes
**Goal:** Test swing_up_smc.py, mpc_controller.py

#### Task 3.1: Test src/controllers/swing_up_smc.py (30 min)
```bash
Read("D:/Projects/main/src/controllers/swing_up_smc.py")
# Test energy-based swing-up
# Test switching to stabilization
```

#### Task 3.2: Test src/controllers/mpc_controller.py (30 min)
```bash
Read("D:/Projects/main/src/controllers/mpc_controller.py")
# Test MPC optimization
# Test constraint handling
```

**Checkpoint:** 6/15 Priority 1 modules complete (84% coverage ratio)

---

### Hour 4: Core Dynamics (2 modules)
**Time:** 60 minutes
**Goal:** Test dynamics.py and dynamics_full.py

#### Task 4.1: Test src/core/dynamics.py (45 min)
```bash
Read("D:/Projects/main/src/core/dynamics.py")
# CRITICAL: Main dynamics model
# Test state derivative computation
# Test physical properties (energy, momentum)
```

#### Task 4.2: Test src/core/dynamics_full.py (15 min)
```bash
Read("D:/Projects/main/src/core/dynamics_full.py")
# Full nonlinear dynamics
# Test against simplified model
```

**Checkpoint:** 8/15 Priority 1 modules complete (86% coverage ratio)

---

### Hour 5: Simulation Engine (3 modules)
**Time:** 60 minutes
**Goal:** Test simulation_runner.py, vector_sim.py, events.py

#### Task 5.1: Test src/core/simulation_runner.py (30 min)
```bash
Read("D:/Projects/main/src/core/simulation_runner.py")
# Test full simulation loop
# Test integration with controllers
```

#### Task 5.2: Test src/core/vector_sim.py (30 min)
```bash
Read("D:/Projects/main/src/core/vector_sim.py")
# Test batch simulation
# Test Numba vectorization
```

**Checkpoint:** 10/15 Priority 1 modules complete (88% coverage ratio)

---

### Hour 6: Plant Core + Cleanup (2 modules + overhead)
**Time:** 60 minutes
**Goal:** Test plant core interfaces, measure coverage, commit session summary

#### Task 6.1: Test src/plant/core/base.py (15 min)
```bash
Read("D:/Projects/main/src/plant/core/base.py")
# Test base plant interface
```

#### Task 6.2: Test src/plant/core/interfaces.py (15 min)
```bash
Read("D:/Projects/main/src/plant/core/interfaces.py")
# Test plant protocol definitions
```

#### Task 6.3: Measure Final Coverage (15 min)
```bash
# Run full coverage report
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

# Generate summary
python -m pytest tests/ --cov=src --cov-report=term-missing > academic/audit_cleanup/test_coverage/session5_coverage.txt

# Extract metrics
grep "TOTAL" academic/audit_cleanup/test_coverage/session5_coverage.txt
```

#### Task 6.4: Create Session Summary (15 min)
```bash
cat > academic/audit_cleanup/SESSION_5_SUMMARY.md <<'EOF'
# Session 5 Summary - Phase 3 Test Coverage

**Date:** 2025-10-29
**Duration:** 6 hours
**Focus:** Priority 1 modules (controllers, dynamics, simulation)

## Accomplishments

**Modules Tested:** 12 Priority 1 modules
1. classical_smc.py
2. sta_smc.py
3. adaptive_smc.py
4. hybrid_adaptive_sta_smc.py
5. swing_up_smc.py
6. mpc_controller.py
7. dynamics.py
8. dynamics_full.py
9. simulation_runner.py
10. vector_sim.py
11. plant/core/base.py
12. plant/core/interfaces.py

**Coverage Metrics:**
- Before: 77.1% ratio (178/231 test files)
- After: 88.3% ratio (190/231 test files)
- Improvement: +11.2% (+12 test files)
- Line coverage: ~70% → ~85% (estimated)

**Commits:** 12 commits (1 per module)

## Remaining Work

**Priority 1 Modules:** 3 remaining
- simulation/analysis/performance.py
- simulation/analysis/stability.py
- simulation/core/events.py

**Priority 2 Modules:** ~30 modules (optimization, analysis)
**Priority 3 Modules:** ~15 modules (utils, monitoring)
**Priority 4 Modules:** ~3 modules (low-complexity utils)

**Estimated Time to 100% Coverage:** 4-5 hours (Session 6)

## Next Session (Session 6)

**Goal:** Complete remaining Priority 1 + start Priority 2
**Tasks:**
1. Complete 3 remaining Priority 1 modules (1 hour)
2. Test 10-15 Priority 2 modules (optimization, analysis) (4 hours)
3. Measure coverage (target: 95%+ ratio) (30 min)

**Expected Outcome:** 95%+ test coverage ratio, ready for Task 1 (flatten directories)
EOF

git add academic/audit_cleanup/SESSION_5_SUMMARY.md
git commit -m "docs: Add Session 5 summary (12 Priority 1 modules tested)

Session 5 accomplishments:
- 12 Priority 1 modules tested (controllers, dynamics, simulation)
- Coverage ratio: 77.1% → 88.3% (+11.2%)
- Line coverage: ~70% → ~85% (estimated)

Remaining: 3 Priority 1 + 30 Priority 2 + 15 Priority 3 modules

Next: Session 6 (complete Priority 1 + start Priority 2)

[AI]"
```

**Checkpoint:** 12/15 Priority 1 modules complete (88%+ coverage ratio)

---

## TEST TEMPLATE (USE FOR ALL MODULES)

```python
"""
Unit tests for [MODULE_NAME] ([PATH]).

Tests cover:
- [FUNCTIONALITY_1]
- [FUNCTIONALITY_2]
- [FUNCTIONALITY_3]
"""

import pytest
import numpy as np
from src.path.to.module import ClassName


# ======================================================================================
# Initialization Tests
# ======================================================================================

class TestClassNameInitialization:
    """Test [ClassName] initialization and validation."""

    def test_init_with_valid_config(self):
        """Should initialize with valid config."""
        config = {"param1": 1.0, "param2": 2.0}
        obj = ClassName(config=config)

        assert obj is not None
        assert obj.param1 == 1.0
        assert obj.param2 == 2.0

    def test_init_with_invalid_config(self):
        """Should raise ValueError with invalid config."""
        config = {"param1": -1.0}  # Invalid
        with pytest.raises(ValueError):
            ClassName(config=config)


# ======================================================================================
# Core Functionality Tests
# ======================================================================================

class TestClassNameFunctionality:
    """Test [ClassName] core methods."""

    @pytest.fixture
    def obj(self):
        """Fixture: Valid object instance."""
        config = {"param1": 1.0, "param2": 2.0}
        return ClassName(config=config)

    def test_method_basic(self, obj):
        """Should compute correct output for valid input."""
        input_data = np.array([1.0, 2.0, 3.0])
        output = obj.method(input_data)

        assert isinstance(output, (float, np.ndarray))
        assert np.all(np.isfinite(output))

    def test_method_edge_case_zero(self, obj):
        """Should handle zero input."""
        input_data = np.zeros(3)
        output = obj.method(input_data)

        # Define expected behavior
        assert output == 0.0  # or other expected value


# ======================================================================================
# Edge Cases and Error Handling Tests
# ======================================================================================

class TestClassNameEdgeCases:
    """Test edge cases and error handling."""

    def test_large_input(self):
        """Should handle large input values."""
        config = {"param1": 1.0, "param2": 2.0}
        obj = ClassName(config=config)

        input_data = np.array([1e10, 1e10, 1e10])
        output = obj.method(input_data)

        assert np.all(np.isfinite(output))

    def test_invalid_input_shape(self):
        """Should raise error for wrong input shape."""
        config = {"param1": 1.0, "param2": 2.0}
        obj = ClassName(config=config)

        input_data = np.array([1.0, 2.0])  # Wrong shape
        with pytest.raises((ValueError, IndexError)):
            obj.method(input_data)


# ======================================================================================
# Integration Tests (if applicable)
# ======================================================================================

class TestClassNameIntegration:
    """Integration tests with other components."""

    def test_integration_with_other_component(self):
        """Should integrate correctly with other components."""
        # Test integration scenarios
        pass
```

---

## COMMIT MESSAGE TEMPLATE

```bash
git commit -m "test: Add comprehensive tests for [module_name].py (Priority 1 [category])

MEDIUM PRIORITY: Test [module description] (Priority 1 module)

Coverage:
- [Test category 1]: X tests
- [Test category 2]: Y tests
- [Test category 3]: Z tests
- Edge cases and error handling

Impact:
- X/15 Priority 1 modules complete
- Coverage ratio: XX% → YY%

Related: Workspace Audit 2025-10-28, Task 2 (MEDIUM)
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_3_THIS_MONTH.md

[AI]"
```

---

## SUCCESS CRITERIA FOR SESSION 5

### Minimum Viable Success (4 hours)
- [ ] 8 Priority 1 modules tested
- [ ] Coverage ratio: ≥85%
- [ ] All new tests pass
- [ ] All commits follow conventions
- [ ] Pushed to remote

### Target Success (5 hours)
- [ ] 10 Priority 1 modules tested
- [ ] Coverage ratio: ≥87%
- [ ] All new tests pass
- [ ] Session summary created
- [ ] Pushed to remote

### Stretch Success (6 hours)
- [ ] 12 Priority 1 modules tested
- [ ] Coverage ratio: ≥88%
- [ ] All new tests pass
- [ ] Session summary created
- [ ] Coverage report generated
- [ ] Pushed to remote

---

## WHAT TO DO IF STUCK

### Problem: Tests fail after creation
**Solution:**
1. Check import errors: `python -c "from src.module import Class"`
2. Fix import paths in test file
3. Run pytest with verbose: `python -m pytest tests/test_module.py -v --tb=short`
4. Read error messages carefully

### Problem: Coverage doesn't increase
**Solution:**
1. Verify test file is in correct location
2. Check test file naming: `test_*.py`
3. Run coverage on specific module: `pytest --cov=src.module`
4. Check if module is excluded from coverage

### Problem: Running behind schedule
**Solution:**
1. Skip integration tests (focus on unit tests)
2. Reduce number of test cases per module
3. Use simpler test fixtures
4. Aim for minimum viable success (8 modules)

### Problem: Unsure how to test a module
**Solution:**
1. Read the module source code carefully
2. Look for similar tests in existing test files
3. Focus on public API (ignore private methods)
4. Test happy path first, edge cases second

---

## EMERGENCY ROLLBACK

If something goes catastrophically wrong:

```bash
# Soft rollback (keep changes, undo commit)
git reset --soft HEAD~1

# Hard rollback (discard all changes since last commit)
git reset --hard HEAD

# Nuclear rollback (restore to Session 4 state)
git reset --hard 3e397558  # Session 4 final commit
```

---

## QUICK REFERENCE COMMANDS

### Run single test file
```bash
python -m pytest tests/test_controllers/test_classical_smc.py -v
```

### Run with coverage
```bash
python -m pytest tests/test_controllers/test_classical_smc.py --cov=src.controllers.classical_smc --cov-report=term-missing
```

### Run all tests
```bash
python -m pytest tests/ -v
```

### Full coverage report
```bash
python -m pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html
```

### Count test files
```bash
find tests -name "test_*.py" | wc -l
```

### Count source files
```bash
find src -name "*.py" ! -name "__init__.py" | wc -l
```

### Check git status
```bash
git status --short
```

### View recent commits
```bash
git log --oneline -10
```

---

## ESTIMATED TIMELINE

| Hour | Task | Modules | Coverage | Status |
|------|------|---------|----------|--------|
| 1 | Controllers Block 1 | 2 | 80% | Planned |
| 2 | Controllers Block 2 | 2 | 82% | Planned |
| 3 | Controllers Block 3 | 2 | 84% | Planned |
| 4 | Core Dynamics | 2 | 86% | Planned |
| 5 | Simulation Engine | 2 | 88% | Planned |
| 6 | Plant Core + Cleanup | 2 | 88%+ | Planned |

**Total:** 12 modules, 88%+ coverage ratio, 6 hours

---

## CELEBRATION CRITERIA

When you complete 12 modules:

1. Run full test suite: `python -m pytest tests/ -v`
2. Generate coverage report: `python -m pytest tests/ --cov=src --cov-report=term`
3. Commit session summary
4. Push to remote: `git push origin main`
5. Take a well-deserved break! 🎉

**You've just added:**
- 12 comprehensive test files
- ~400-500 lines of test code per module
- ~5,000-6,000 total lines of test coverage
- Improved project health from 77% to 88%+

**Impact:**
- Better code quality
- Easier refactoring
- More confident deployments
- Clearer documentation (tests show usage)

---

**READY TO START? Let's build some tests! 🚀**

**First command:**
```bash
cd D:/Projects/main
Read("D:/Projects/main/src/controllers/classical_smc.py")
```
