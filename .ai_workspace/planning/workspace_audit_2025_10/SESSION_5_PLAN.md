# SESSION 5: PHASE 3 WORKSPACE CLEANUP - EXECUTION PLAN

**Session Date:** 2025-10-29
**Duration:** 5-6 hours
**Focus:** Phase 3 (Comprehensive Cleanup) Task 2 - Test Coverage Improvement
**Status:** Ready to Execute

---

## CONTEXT & OBJECTIVES

You are executing **Phase 3** of the workspace audit cleanup after completing Phases 1-2. This session focuses on **Test Coverage Improvement** (Task 2), which is:

- **Highest impact** (improves code quality, enables safe refactoring)
- **Lowest risk** (additive changes only)
- **Most critical** (un blocks directory flattening work in future sessions)

### Session 5 Target

Complete testing for **12-15 Priority 1 modules**, bringing coverage ratio from **77.1% (178/231)** to **≥88% (203/231)**.

### Priority 1 Modules (CRITICAL - Controllers & Dynamics)

**Category A: SMC Controllers (6 modules)**
1. ✓ `src/controllers/smc/classic_smc.py` - Classical SMC (already 24 tests)
2. `src/controllers/smc/sta_smc.py` - Super-twisting SMC
3. `src/controllers/smc/adaptive_smc.py` - Adaptive SMC
4. `src/controllers/smc/hybrid_adaptive_sta_smc.py` - Hybrid adaptive
5. `src/controllers/specialized/swing_up_smc.py` - Swing-up controller
6. `src/controllers/mpc/mpc_controller.py` - Model Predictive Control

**Category B: Core Dynamics (2 modules - CRITICAL)**
7. `src/core/dynamics.py` - Simplified dynamics (CRITICAL)
8. `src/core/dynamics_full.py` - Full nonlinear dynamics (CRITICAL)

**Category C: Simulation Engine (2 modules)**
9. `src/core/simulation_runner.py` - Main simulation loop
10. `src/core/vector_sim.py` - Vectorized batch simulator

**Category D: Plant Core (2 modules)**
11. `src/plant/core/base.py` - Base plant class
12. `src/plant/core/interfaces.py` - Plant interfaces

---

## SESSION 5 HOUR-BY-HOUR ROADMAP

### Hour 1: STA SMC + Adaptive SMC (2 modules)
- **Module 2:** `src/controllers/smc/sta_smc.py` (30 min)
  - Read module (10 min) → understand super-twisting control law
  - Write comprehensive tests (20 min) → init, compute_control, dynamics checking
  - Run tests & verify passing (5 min)
  - Commit with message template (5 min)

- **Module 3:** `src/controllers/smc/adaptive_smc.py` (30 min)
  - Same workflow
  - Focus on adaptation law, parameter updates, uncertainty estimation
  - Expected tests: init, adaptation_law, control_with_adaptation, edge_cases

**Output:** 2/12 modules complete | Coverage: ~78%

---

### Hour 2: Hybrid Adaptive + Swing-up (2 modules)
- **Module 4:** `src/controllers/smc/hybrid_adaptive_sta_smc.py` (30 min)
  - Hybrid control switching logic
  - Tests: initialization, mode switching, control computation, adaptation

- **Module 5:** `src/controllers/specialized/swing_up_smc.py` (30 min)
  - Swing-up phase controller (before stabilization)
  - Tests: phase detection, swing control, transition to stabilization

**Output:** 4/12 modules complete | Coverage: ~80%

---

### Hour 3: MPC + Dynamics (Core) (2 modules)
- **Module 6:** `src/controllers/mpc/mpc_controller.py` (30 min)
  - Model predictive control optimization
  - Tests: initialization, QP solver calls, constraint handling, control output

- **Module 7:** `src/core/dynamics.py` (45 min) ⭐ CRITICAL
  - Simplified pendulum dynamics (key for all simulations!)
  - Tests: initialization, state update, physics validation, numerical stability
  - Focus on: `compute_state_derivatives()`, `_compute_physics_matrices()`

**Output:** 5/12 modules complete | Coverage: ~83%

---

### Hour 4: Full Dynamics + Simulation Runner (2 modules)
- **Module 8:** `src/core/dynamics_full.py` (15 min)
  - Full nonlinear dynamics (extension of simplified)
  - Tests: initialization, state update, energy conservation (if applicable)

- **Module 9:** `src/core/simulation_runner.py` (45 min)
  - Main simulation loop & orchestration
  - Tests: runner initialization, step execution, history tracking, final state computation
  - Focus on: `run_simulation()`, `run_batch_simulations()`, result aggregation

**Output:** 7/12 modules complete | Coverage: ~85%

---

### Hour 5: Vector Simulator + Plant Core (2 modules)
- **Module 10:** `src/core/vector_sim.py` (30 min)
  - Numba-vectorized batch simulator
  - Tests: initialization, vectorized state updates, Numba JIT compilation, result format

- **Module 11:** `src/plant/core/base.py` (30 min)
  - Base plant class (parent for all plants)
  - Tests: initialization, property access, state bounds, dynamics selection

**Output:** 9/12 modules complete | Coverage: ~87%

---

### Hour 6: Plant Interfaces + Measurement + Wrap-up (3 modules + overhead)
- **Module 12:** `src/plant/core/interfaces.py` (15 min)
  - Interface definitions (if not already tested)
  - Check: are these abstract classes, protocols, or concrete implementations?
  - Write minimal tests if concrete

- **Coverage Measurement:** (15 min)
  - Run full test suite: `python -m pytest tests/ -q`
  - Generate coverage report
  - Extract before/after metrics

- **Session Summary:** (15 min)
  - Document modules tested
  - Record coverage metrics (177 → 203+ test files)
  - Note any blockers for next session
  - Create `academic/audit_cleanup/SESSION_5_SUMMARY.md`

- **Final Commit:** (5 min)
  - Commit summary document
  - Push to remote

**Output:** 10-12 modules complete | Coverage: ≥88% | Session documented

---

## TEST WRITING GUIDELINES

### Minimal Test Template (Copy-Paste)

```python
# tests/test_controllers/smc/test_STA_SMC.py

import pytest
import numpy as np
from src.controllers.smc.sta_smc import SuperTwistingSMC

class TestSuperTwistingSMCInitialization:
    """Test controller initialization and parameter validation."""

    def test_valid_initialization(self):
        """Test controller initializes with valid gains."""
        gains = [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
        controller = SuperTwistingSMC(
            gains=gains,
            max_force=100.0,
            boundary_layer=0.01
        )
        assert len(controller.gains) == 6
        assert controller.max_force == 100.0

    def test_invalid_gain_count_raises(self):
        """Test that wrong gain count raises ValueError."""
        with pytest.raises(ValueError):
            SuperTwistingSMC(
                gains=[1.0, 2.0, 3.0],  # Wrong count!
                max_force=100.0,
                boundary_layer=0.01
            )

class TestSuperTwistingSMCComputation:
    """Test control computation logic."""

    def test_compute_control_returns_valid_output(self):
        """Test control output is finite and bounded."""
        gains = [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
        controller = SuperTwistingSMC(
            gains=gains,
            max_force=100.0,
            boundary_layer=0.01
        )
        state = np.array([0.1, 0.05, 0.03, 0.2, 0.1, 0.05])  # [x, θ1, θ2, ẋ, θ̇1, θ̇2]
        output = controller.compute_control(state, (), {})

        assert np.isfinite(output.control)
        assert abs(output.control) <= 100.0
```

**Fill in 5-7 more tests per module following this pattern:**
- Initialization tests (valid/invalid configs)
- Basic computation tests (zero state, typical state, large errors)
- Edge cases (NaN, inf, boundary conditions)
- Integration tests (multiple calls, state trajectory)

### Key Points
- **Test per file:** 15-25 tests per module (typically)
- **Coverage goal:** 80%+ line coverage per module
- **Time per module:** 30-45 minutes (including running tests)
- **Don't test:** Private methods (start with `_`), abstract methods, external libraries

---

## COMMIT MESSAGE TEMPLATE

```bash
git commit -m "test: Add comprehensive tests for [MODULE_NAME] (Priority 1 [CATEGORY])

Medium priority test coverage improvement for [BRIEF DESCRIPTION].

Coverage:
- Initialization: X tests (valid/invalid configs, parameter validation)
- Computation: Y tests (basic functionality, edge cases)
- Integration: Z tests (realistic scenarios)

Impact:
- [N]/15 Priority 1 modules complete
- Coverage ratio: XX.X% → YY.Y% ([N]/231 test files)

Related: Workspace Audit 2025-10-28, Task 2 (Test Coverage)
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_3_THIS_MONTH.md

[AI]"
```

### Example
```bash
git commit -m "test: Add comprehensive tests for sta_smc.py (Priority 1 controller)

Medium priority test coverage for super-twisting SMC controller.

Coverage:
- Initialization: 6 tests (valid configs, gain validation, parameter bounds)
- Super-twisting law: 8 tests (basic computation, adaptation, dynamics)
- Edge cases: 4 tests (NaN, inf, boundary conditions, zero gains)
- Integration: 3 tests (control trajectory, reference tracking)

Impact:
- 2/15 Priority 1 modules complete
- Coverage ratio: 77.1% → 77.5% (180/231 test files)

Related: Workspace Audit 2025-10-28, Task 2 (Test Coverage)
Refs: .ai_workspace/planning/workspace_audit_2025_10/PHASE_3_THIS_MONTH.md

[AI]"
```

---

## COMMAND REFERENCE

### Pre-Session Setup
```bash
cd D:/Projects/main
git status                    # Verify clean state
git branch                    # Verify on refactor/phase3-comprehensive-cleanup
```

### For Each Module
```bash
# 1. Read the source module
Read("D:/Projects/main/src/path/to/module.py")

# 2. Create test file (use minimal template above)
# Write to: tests/test_path/test_module_name.py

# 3. Run your tests
python -m pytest tests/test_path/test_module_name.py -v

# 4. Commit
git add tests/test_path/test_module_name.py
git commit -m "test: Add comprehensive tests for module.py (Priority 1 category)

  ... (use template from above)

  [AI]"

# 5. Push
git push origin refactor/phase3-comprehensive-cleanup
```

### After Session
```bash
# Run full test suite
python -m pytest tests/ -q 2>&1 | tail -5

# Get coverage metrics
find tests -name "test_*.py" | wc -l        # Should be 190+ after session
find src -name "*.py" ! -name "__init__.py" | wc -l  # Should still be 231

# Check what's been added
git log --oneline -10

# Create session summary
cat > academic/audit_cleanup/SESSION_5_SUMMARY.md << EOF
# Session 5 Summary

- **Modules completed:** [LIST]
- **Tests written:** [NUMBER]
- **Coverage ratio:** 178/231 → ?/231
- **Next steps:** [Module list for Session 6]

EOF

git add academic/audit_cleanup/SESSION_5_SUMMARY.md
git commit -m "docs: Add Session 5 completion summary [AI]"
git push origin refactor/phase3-comprehensive-cleanup
```

---

## SUCCESS CRITERIA

### Minimum (4 hours)
- ✅ 8 modules tested (controllers + core dynamics)
- ✅ Test file count: 178 → 186+ (8 new files)
- ✅ All new tests pass
- ✅ All commits follow conventions with [AI] footer
- ✅ Pushed to remote

### Target (5 hours)
- ✅ 10 modules tested
- ✅ Test file count: 178 → 188+ (10 new files)
- ✅ Coverage ratio: 77.1% → 83%+
- ✅ Session summary created
- ✅ Pushed to remote

### Stretch (6 hours)
- ✅ 12-15 modules tested
- ✅ Test file count: 178 → 193+ (15 new files)
- ✅ Coverage ratio: 77.1% → 88%+
- ✅ Coverage report generated
- ✅ Session summary with metrics
- ✅ Pushed to remote

---

## TROUBLESHOOTING

### "Module not found" when importing
```bash
# Check if module exists
ls src/path/to/module.py

# Test import manually
python -c "from src.path.to.module import ClassName"

# If pytest fails, check sys.path in conftest.py
cat tests/conftest.py
```

### "Test file location wrong"
- Tests go in: `tests/test_path/test_module.py`
- Must start with `test_`
- Must mirror source structure

### "Running behind schedule"
- Focus on **unit tests only** (happy path + edge cases)
- Skip complex integration tests for now
- Aim for **minimum viable success** (8-10 modules)

### "Unsure how to test a module"
1. Read the module docstrings (understand public API)
2. Look for similar tests in existing code
3. Test **public methods only** (no private `_` methods)
4. Use the template above and adapt

---

## NEXT STEPS AFTER SESSION 5

### Session 6 (Next 5-6 hours)
- Continue Priority 1 modules (finish remaining 3-5)
- Start Priority 2 modules (optimization, analysis, utils)
- Target: 90%+ coverage ratio

### Session 7 (Following 5-6 hours)
- Complete Priority 2 (30 modules)
- Complete Priority 3 (15 modules)
- **Target: 95%+ coverage ratio** (Task 2 COMPLETE)

### Session 8+
- Task 1: Flatten directory structures (6-8 hours)
- Task 3: Clean legacy documentation (2 hours)
- **Phase 3 COMPLETE: Health 8.5/10**

---

## IMPORTANT NOTES

1. **You're on the right track:** Classical SMC already has 24 tests. Build on that pattern.

2. **Modules matter most:** Focus on **controllers** and **dynamics** first (most critical).

3. **Tests enable refactoring:** Once you have 95%+ test coverage, directory flattening becomes much safer.

4. **Commits are permanent:** Your work survives token limits because it's committed to git.

5. **Don't overthink:** 15-20 tests per module is sufficient. Quality > Quantity.

---

**Ready to start?** Pick Module 2 (sta_smc.py) and begin!

Good luck! You've got this! 🚀
