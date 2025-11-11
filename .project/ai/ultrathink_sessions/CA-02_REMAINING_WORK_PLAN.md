# CA-02 Remaining Work: Path to 100% Production-Ready

**Type**: Execution Plan (3 Priority Fixes)
**Duration**: 3.5-6.5 hours
**Date**: November 11, 2025
**Status**: READY TO EXECUTE

---

## Objectives

Complete remaining fixes from CA-02 memory audit to achieve 100% production-ready status across all 4 controllers.

**Current State**: 3/4 controllers production-ready (75% coverage)
**Target State**: 4/4 controllers production-ready (100% coverage)
**Blocker**: STA-SMC Numba JIT memory leak (2.42 KB/step)

---

## Priority Breakdown

| Priority | Issue | Severity | Effort | Blocker? | Impact |
|----------|-------|----------|--------|----------|--------|
| **P0** | STA-SMC Numba leak | CRITICAL | 2-4h | YES | 23.64 MB → <0.5 MB |
| **P1** | Nested component cleanup | MAJOR | 1-2h | NO | Complete cleanup |
| **P2** | SimulationRunner history | MINOR | 0.5h | NO | Batch safety |

**Total Effort**: 3.5-6.5 hours

---

## P0: Fix STA-SMC Numba JIT Memory Leak (2-4 hours) [CRITICAL]

### Problem Statement

**Symptom**: 23.64 MB memory growth over 10,000 simulation steps (2.42 KB/step)

**Root Cause**: Numba JIT compilation allocating memory without caching compiled functions

**Evidence**:
- 31,600 allocations in `<frozen importlib._bootstrap_external>:757` (3.71 MB)
- 9,181 allocations in `<frozen abc>:106` (2.98 MB)
- 1,971 allocations in `numba.core.typing.templates.py:1183` (0.54 MB)
- Memory growth occurs in first 100 cycles, then stabilizes (compilation phase)

**Impact**: Production blocker for STA controller

---

### Task Breakdown

#### Task 1.1: Audit All @njit Decorators (30 min)

**Goal**: Find all Numba decorators in sta_smc.py and check for cache=True

**Steps**:
```bash
# Search for all @njit decorators
rg "@njit|@jit" src/controllers/smc/sta_smc.py

# Expected locations:
# - Super-twisting algorithm functions
# - Numerical integration helpers
# - State computation functions
```

**Deliverable**: List of all @njit decorators with line numbers

---

#### Task 1.2: Add cache=True to All Decorators (30 min)

**Goal**: Enable Numba function caching to prevent recompilation

**Pattern**:
```python
# Before
@njit
def super_twisting_law(x, params):
    # ...

# After
@njit(cache=True)
def super_twisting_law(x, params):
    # ...
```

**Files to Update**:
- `src/controllers/smc/sta_smc.py` (primary target)
- Any helper modules imported by sta_smc.py

**Validation**:
- Code compiles without errors
- Tests still pass: `pytest tests/test_controllers/test_sta_smc.py -v`

**Deliverable**: Updated sta_smc.py with cache=True on all decorators

---

#### Task 1.3: Investigate Dynamic Function Generation (45 min)

**Goal**: Find and eliminate dynamic function generation that prevents caching

**Search Patterns**:
```bash
# Search for lambda functions
rg "lambda" src/controllers/smc/sta_smc.py

# Search for closures (functions returning functions)
rg "def.*\(.*\):.*def.*\(.*\):" src/controllers/smc/sta_smc.py

# Search for functools.partial
rg "partial" src/controllers/smc/sta_smc.py
```

**Common Issues**:
1. **Lambda functions**: Replace with named functions
2. **Closures**: Move inner functions to module level
3. **Dynamic parameters**: Use static configuration

**Example Fix**:
```python
# Before (dynamic, not cacheable)
def create_controller(k):
    @njit
    def control_law(x):
        return k * x  # Closure over k
    return control_law

# After (static, cacheable)
@njit(cache=True)
def control_law(x, k):
    return k * x  # k passed as parameter
```

**Deliverable**: Refactored code without dynamic function generation

---

#### Task 1.4: Pre-compile Functions on Module Load (30 min)

**Goal**: Force compilation at import time to avoid runtime compilation overhead

**Pattern**:
```python
# At end of sta_smc.py module

def _precompile_numba_functions():
    """Pre-compile Numba JIT functions to avoid runtime overhead."""
    # Create dummy inputs with representative types
    dummy_state = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1], dtype=float)
    dummy_params = np.array([1.0, 1.0, 1.0], dtype=float)

    # Call each @njit function once to trigger compilation
    try:
        super_twisting_law(dummy_state, dummy_params)
        # ... call other @njit functions ...
    except Exception:
        pass  # Ignore errors during pre-compilation

# Pre-compile on module import
_precompile_numba_functions()
```

**Deliverable**: Pre-compilation function added to sta_smc.py

---

#### Task 1.5: Test with Stress Test Script (30 min)

**Goal**: Validate leak is fixed using existing stress test

**Command**:
```bash
# Run stress test (10,000 steps)
python .artifacts/qa_audits/CA-02_MEMORY_MANAGEMENT_AUDIT/stress_test_memory.py

# Expected result BEFORE fix:
# sta_smc: LEAK DETECTED (2.42 KB/step, 23.64 MB total)

# Expected result AFTER fix:
# sta_smc: OK (<0.5 KB/step, <5 MB total)
```

**Success Criteria**:
- Memory growth < 0.5 KB/step
- Total growth < 5 MB over 10,000 steps
- Verdict changes from "LEAK DETECTED" to "OK"

**Deliverable**: Updated stress_test_results.json showing leak fixed

---

#### Task 1.6: Validate with Controller Creation Test (15 min)

**Goal**: Ensure fix works for repeated controller creation (1000 cycles)

**Command**:
```bash
# Run leak detection script
python .artifacts/qa_audits/CA-02_MEMORY_MANAGEMENT_AUDIT/detect_memory_leaks.py

# Expected result AFTER fix:
# sta_smc: OK (<1 KB/cycle, <1 MB total)
```

**Success Criteria**:
- Memory growth < 1 KB/cycle
- Total growth < 1 MB over 1000 cycles

**Deliverable**: Updated leak_detection_results.json

---

#### Task 1.7: Document Fix and Commit (15 min)

**Deliverables**:
1. Update CA-02_FINAL_MEMORY_AUDIT_REPORT.md (mark P0 as FIXED)
2. Create P0_STA_NUMBA_FIX_VALIDATION.md (validation report)
3. Commit changes with detailed message

**Commit Message Template**:
```
fix(sta-smc): Fix Numba JIT memory leak with cache=True decorators

P0 FIX (CA-02 AUDIT - 2-4 HOURS):
Fixed CRITICAL memory leak in STA-SMC controller (23.64 MB -> <0.5 MB).

ROOT CAUSE: Numba JIT compilation without caching
- 31,600 allocations in importlib._bootstrap_external
- 9,181 allocations in frozen abc
- Functions recompiled on every controller creation

SOLUTION:
1. Added cache=True to all @njit decorators (N decorators)
2. Eliminated dynamic function generation (closures, lambdas)
3. Added _precompile_numba_functions() for module-load compilation

VALIDATION:
- Stress test (10,000 steps): 23.64 MB -> X.XX MB (XX% reduction)
- Creation test (1000 cycles): 13.61 MB -> X.XX MB (XX% reduction)
- Growth rate: 2.42 KB/step -> X.XX KB/step

IMPACT: STA-SMC now production-ready
- Before: 2.42 KB/step (production blocker)
- After: X.XX KB/step (acceptable)
- Status: PRODUCTION-READY

[AI] Generated with Claude Code (https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### P0 Time Breakdown

| Task | Duration | Cumulative |
|------|----------|------------|
| 1.1: Audit decorators | 30 min | 0.5h |
| 1.2: Add cache=True | 30 min | 1.0h |
| 1.3: Investigate dynamic functions | 45 min | 1.75h |
| 1.4: Pre-compile functions | 30 min | 2.25h |
| 1.5: Stress test validation | 30 min | 2.75h |
| 1.6: Creation test validation | 15 min | 3.0h |
| 1.7: Document and commit | 15 min | 3.25h |
| **Total (Best Case)** | | **3.25h** |
| **Total (Worst Case)** | | **4.0h** (if refactoring complex) |

---

## P1: Add Nested Component Cleanup (1-2 hours) [MAJOR]

### Problem Statement

**Issue**: Nested components (SwitchingLogic, AdaptationLaw) lack explicit cleanup() methods

**Impact**:
- Parent controller cleanup() doesn't clean nested components
- Long-running applications may accumulate memory in nested objects

**Current Workaround**: Some nested components have reset() methods

---

### Task Breakdown

#### Task 2.1: Audit Nested Components (20 min)

**Goal**: Identify all nested components that need cleanup

**Components to Check**:
```python
# HybridAdaptiveSTASMC nested components
- switching_logic (SwitchingLogic class)
- transition_filter (if exists)

# AdaptiveSMC nested components
- adaptation_law (AdaptationLaw class)
- parameter_estimator (ParameterEstimator class)

# Other controllers
- Check for any nested objects with history/state
```

**Checklist**:
- [ ] Does component have history lists?
- [ ] Does component have cleanup() or reset() method?
- [ ] Is component cleaned by parent cleanup()?

**Deliverable**: List of components needing cleanup

---

#### Task 2.2: Add Cleanup to SwitchingLogic (30 min)

**Goal**: Add cleanup() method to clear all history lists

**File**: `src/controllers/smc/algorithms/hybrid/switching_logic.py`

**Pattern**:
```python
def cleanup(self) -> None:
    """Explicit memory cleanup for switching logic.

    Clears all history lists and resets state to allow proper
    garbage collection.
    """
    # Clear history lists (identified in Phase 1)
    if hasattr(self, 'switch_history'):
        self.switch_history.clear()

    # Clear performance history (dict of deques)
    if hasattr(self, 'performance_history'):
        for deque_obj in self.performance_history.values():
            deque_obj.clear()
        self.performance_history.clear()

    # Clear threshold adaptation history
    if hasattr(self, 'threshold_adaptation_history'):
        self.threshold_adaptation_history.clear()

    # Reset state
    self.last_switch_time = 0.0
```

**Test**:
```python
# Manual verification
logic = SwitchingLogic(config)
# ... use logic ...
logic.cleanup()
assert len(logic.switch_history) == 0
```

**Deliverable**: SwitchingLogic.cleanup() method

---

#### Task 2.3: Add Cleanup to AdaptationLaw (20 min)

**Goal**: Rename reset() to cleanup() or add cleanup() that calls reset()

**File**: `src/controllers/smc/algorithms/adaptive/adaptation_law.py`

**Pattern (Option 1 - Rename)**:
```python
# Rename reset() to cleanup()
def cleanup(self, initial_gain: Optional[float] = None) -> None:
    """Explicit memory cleanup (formerly reset)."""
    # ... existing reset() code ...
    self._adaptation_history.clear()
```

**Pattern (Option 2 - Add cleanup)**:
```python
# Add cleanup() that calls reset()
def cleanup(self) -> None:
    """Explicit memory cleanup."""
    self.reset()
```

**Deliverable**: AdaptationLaw.cleanup() method

---

#### Task 2.4: Update Parent Controller Cleanups (30 min)

**Goal**: Make parent controllers call nested component cleanup

**Files**:
- `src/controllers/smc/hybrid_adaptive_sta_smc.py`
- `src/controllers/smc/adaptive_smc.py`

**Pattern**:
```python
# In HybridAdaptiveSTASMC.cleanup()
def cleanup(self) -> None:
    """Explicit memory cleanup."""
    # Existing cleanup code...

    # NEW: Clean nested components
    if hasattr(self, 'switching_logic') and hasattr(self.switching_logic, 'cleanup'):
        self.switching_logic.cleanup()

    if hasattr(self, 'transition_filter') and hasattr(self.transition_filter, 'cleanup'):
        self.transition_filter.cleanup()
```

```python
# In AdaptiveSMC.cleanup()
def cleanup(self) -> None:
    """Explicit memory cleanup."""
    # Existing cleanup code...

    # NEW: Clean nested components
    if hasattr(self, 'adaptation_law') and hasattr(self.adaptation_law, 'cleanup'):
        self.adaptation_law.cleanup()

    if hasattr(self, 'parameter_estimator') and hasattr(self.parameter_estimator, 'cleanup'):
        self.parameter_estimator.cleanup()
```

**Deliverable**: Updated parent controller cleanup() methods

---

#### Task 2.5: Test Nested Cleanup (20 min)

**Goal**: Verify nested cleanup is called correctly

**Test Script**:
```python
# test_nested_cleanup.py
from src.controllers.factory import create_controller
from src.config import load_config

config = load_config("config.yaml")

# Test HybridAdaptiveSTASMC
gains = config.controller_defaults.hybrid_adaptive_sta_smc.gains
controller = create_controller("hybrid_adaptive_sta_smc", config, gains)

# Verify nested components exist
assert hasattr(controller, 'switching_logic')

# Use controller (populate history)
# ... run simulation ...

# Call cleanup
controller.cleanup()

# Verify nested cleanup worked
if hasattr(controller.switching_logic, 'switch_history'):
    assert len(controller.switching_logic.switch_history) == 0

print("[OK] Nested cleanup verified")
```

**Deliverable**: Test script + validation

---

#### Task 2.6: Document and Commit (10 min)

**Deliverable**: Commit with clear message

**Commit Message Template**:
```
feat(controllers): Add nested component cleanup methods (P1 fix)

P1 FIX (CA-02 AUDIT - 1-2 HOURS):
Added explicit cleanup() methods to nested components for complete memory cleanup.

CHANGES:
1. Added SwitchingLogic.cleanup() - clears switch_history, performance_history, threshold_adaptation_history
2. Added/renamed AdaptationLaw.cleanup() - clears _adaptation_history
3. Updated HybridAdaptiveSTASMC.cleanup() - calls switching_logic.cleanup()
4. Updated AdaptiveSMC.cleanup() - calls adaptation_law.cleanup()

IMPACT:
- Complete memory cleanup for long-running applications
- Prevents memory accumulation in nested components
- Follows best practice: explicit resource management

VALIDATION:
- Manual test script verifies nested cleanup works
- All history lists cleared after cleanup
- No impact on existing cleanup() behavior

[AI] Generated with Claude Code (https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### P1 Time Breakdown

| Task | Duration | Cumulative |
|------|----------|------------|
| 2.1: Audit nested components | 20 min | 0.33h |
| 2.2: Add SwitchingLogic.cleanup() | 30 min | 0.83h |
| 2.3: Add AdaptationLaw.cleanup() | 20 min | 1.17h |
| 2.4: Update parent cleanups | 30 min | 1.67h |
| 2.5: Test nested cleanup | 20 min | 2.0h |
| 2.6: Document and commit | 10 min | 2.17h |
| **Total** | | **2.17h** |

---

## P2: Monitor SimulationRunner History (0.5 hours) [MINOR]

### Problem Statement

**Issue**: `SimulationRunner.simulation_history` grows unbounded in batch simulations

**Impact**:
- Repeated simulations (PSO optimization, batch runs) accumulate results
- Each simulation adds ~10-50 KB to history list
- 1000 simulations = 10-50 MB memory growth

**Current Behavior**: No limit on simulation_history size

---

### Task Breakdown

#### Task 3.1: Add max_history_size Parameter (15 min)

**Goal**: Add configurable limit to simulation_history

**File**: `src/simulation/engines/simulation_runner.py`

**Pattern**:
```python
class SimulationRunner:
    def __init__(
        self,
        dynamics_model: Any,
        dt: float = 0.01,
        max_time: float = 10.0,
        max_history_size: int = 1000  # NEW PARAMETER
    ):
        """Initialize simulation runner.

        Parameters
        ----------
        ...
        max_history_size : int, default=1000
            Maximum number of simulation results to store in history.
            When exceeded, older results are discarded to prevent
            unbounded memory growth. Set to 0 for unlimited.
        """
        self.dynamics_model = dynamics_model
        self.dt = dt
        self.max_time = max_time
        self.max_history_size = max_history_size  # NEW
        self.current_time = 0.0
        self.step_count = 0
        self.simulation_history = []
```

**Deliverable**: Updated __init__ with max_history_size

---

#### Task 3.2: Add History Truncation Logic (15 min)

**Goal**: Truncate history when limit exceeded

**Pattern**:
```python
def run_simulation(self, ...):
    # ... existing simulation code ...

    # Store result
    self.simulation_history.append({
        'time': t_arr,
        'states': x_arr,
        'controls': u_arr
    })

    # NEW: Truncate history if exceeds limit
    if self.max_history_size > 0 and len(self.simulation_history) > self.max_history_size:
        # Keep most recent max_history_size // 2 entries
        self.simulation_history = self.simulation_history[-self.max_history_size // 2:]
```

**Deliverable**: Truncation logic added

---

#### Task 3.3: Document and Commit (10 min)

**Deliverable**: Commit with documentation

**Commit Message Template**:
```
feat(simulation): Add configurable history limit to SimulationRunner (P2 fix)

P2 FIX (CA-02 AUDIT - 0.5 HOURS):
Added max_history_size parameter to prevent unbounded memory growth in batch simulations.

CHANGES:
1. Added max_history_size parameter to SimulationRunner.__init__() (default: 1000)
2. Added automatic truncation when history exceeds limit (keeps most recent 50%)
3. Set to 0 for unlimited history (backward compatible)

IMPACT:
- Prevents memory growth in PSO optimization (1000+ simulations)
- Each simulation adds ~10-50 KB, now capped at 50 MB
- Backward compatible (default limit is generous)

EXAMPLE:
  runner = SimulationRunner(dynamics, max_history_size=100)  # Keep last 100 runs
  runner = SimulationRunner(dynamics, max_history_size=0)    # Unlimited (old behavior)

[AI] Generated with Claude Code (https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### P2 Time Breakdown

| Task | Duration |
|------|----------|
| 3.1: Add max_history_size parameter | 15 min |
| 3.2: Add truncation logic | 15 min |
| 3.3: Document and commit | 10 min |
| **Total** | **40 min** |

---

## Final Validation (30 min)

### Task 4.1: Re-run All CA-02 Tests (20 min)

**Goal**: Validate all fixes work correctly

**Commands**:
```bash
# Test 1: Leak detection (1000 cycles)
python .artifacts/qa_audits/CA-02_MEMORY_MANAGEMENT_AUDIT/detect_memory_leaks.py

# Test 2: History leak detection (1000 steps)
python .artifacts/qa_audits/CA-02_MEMORY_MANAGEMENT_AUDIT/detect_history_leaks.py

# Test 3: Stress test (10,000 steps)
python .artifacts/qa_audits/CA-02_MEMORY_MANAGEMENT_AUDIT/stress_test_memory.py
```

**Success Criteria**:
- STA-SMC verdict: "LEAK DETECTED" → "OK"
- STA-SMC growth: 2.42 KB/step → <0.5 KB/step
- All 4 controllers pass all 3 tests

---

### Task 4.2: Update Final Report (10 min)

**Goal**: Update CA-02 final report with fix results

**File**: `.artifacts/qa_audits/CA-02_MEMORY_MANAGEMENT_AUDIT/CA-02_FINAL_MEMORY_AUDIT_REPORT.md`

**Updates**:
1. Mark P0, P1, P2 as [FIXED]
2. Update overall score: 73.8/100 → XX/100
3. Update production status: 3/4 → 4/4 controllers ready
4. Add "Fixes Applied" section with validation results

**New Score Calculation**:
| Category | Weight | Before | After | Weighted After |
|----------|--------|--------|-------|----------------|
| Leak Detection | 25% | 25/100 | **100/100** | **25.0** (was 6.25) |
| (other categories unchanged) | | | | |
| **TOTAL** | 100% | **73.8** | **~92/100** | **PRODUCTION-READY** |

---

## Time Summary

| Priority | Tasks | Best Case | Worst Case | Status |
|----------|-------|-----------|------------|--------|
| **P0** | Fix STA-SMC Numba leak | 3.25h | 4.0h | PENDING |
| **P1** | Nested component cleanup | 2.17h | 2.17h | PENDING |
| **P2** | SimulationRunner history | 0.67h | 0.67h | PENDING |
| **Validation** | Re-test + update report | 0.5h | 0.5h | PENDING |
| **TOTAL** | | **6.6h** | **7.3h** | **READY** |

**Original Estimate**: 3.5-6.5 hours (conservative)
**Revised Estimate**: 6.6-7.3 hours (detailed breakdown)

---

## Deliverables Checklist

### P0 Deliverables
- [ ] Updated `src/controllers/smc/sta_smc.py` (cache=True on all decorators)
- [ ] Refactored code (no dynamic function generation)
- [ ] Pre-compilation function added
- [ ] P0_STA_NUMBA_FIX_VALIDATION.md (validation report)
- [ ] Updated stress_test_results.json
- [ ] Updated leak_detection_results.json
- [ ] Commit with detailed fix message

### P1 Deliverables
- [ ] `src/controllers/smc/algorithms/hybrid/switching_logic.py` (cleanup method)
- [ ] `src/controllers/smc/algorithms/adaptive/adaptation_law.py` (cleanup method)
- [ ] Updated `src/controllers/smc/hybrid_adaptive_sta_smc.py` (calls nested cleanup)
- [ ] Updated `src/controllers/smc/adaptive_smc.py` (calls nested cleanup)
- [ ] Test script for nested cleanup
- [ ] Commit with P1 fix message

### P2 Deliverables
- [ ] Updated `src/simulation/engines/simulation_runner.py` (max_history_size)
- [ ] Commit with P2 fix message

### Final Validation Deliverables
- [ ] Re-run all 3 CA-02 test scripts
- [ ] Updated CA-02_FINAL_MEMORY_AUDIT_REPORT.md (mark fixes complete)
- [ ] REMAINING_WORK_COMPLETION_SUMMARY.md (final summary)
- [ ] Commit with completion message

**Total Deliverables**: 15 items

---

## Success Criteria

### Overall Success
- [ ] All 4 controllers pass memory tests (≤0.5 KB/step)
- [ ] Memory management score: 73.8/100 → ≥90/100
- [ ] Production status: 3/4 → 4/4 controllers ready
- [ ] All commits pushed to main branch

### P0 Success
- [ ] STA-SMC memory growth: 2.42 KB/step → <0.5 KB/step
- [ ] Stress test verdict: "LEAK DETECTED" → "OK"
- [ ] Total growth over 10K steps: 23.64 MB → <5 MB

### P1 Success
- [ ] All nested components have cleanup() methods
- [ ] Parent cleanup() calls nested cleanup()
- [ ] Manual test verifies history lists cleared

### P2 Success
- [ ] SimulationRunner has max_history_size parameter
- [ ] History truncates when limit exceeded
- [ ] Backward compatible (default=1000)

---

## Execution Order

**Recommended Sequence**:
1. **P0 First** (3.25-4h) - Production blocker, highest impact
2. **Validation** (0.5h) - Confirm P0 fixed before moving on
3. **P1 Next** (2.17h) - Good practice, improves cleanup
4. **P2 Last** (0.67h) - Minor improvement, quick win
5. **Final Validation** (0.5h) - Comprehensive retest

**Alternative (Parallel)**:
- If multiple people available, P1 and P2 can be done in parallel with P0
- P0 is independent of P1/P2
- Final validation requires all fixes complete

---

## Risk Assessment

### P0 Risks
**Risk**: Numba cache issues persist even with cache=True
- **Mitigation**: Check Numba cache directory permissions, clear cache and retry
- **Fallback**: Pre-compile all functions on module load (Task 1.4)

**Risk**: Dynamic function generation is complex to refactor
- **Mitigation**: Allocate up to 4 hours for refactoring
- **Fallback**: Document workaround, defer to future optimization

### P1 Risks
**Risk**: Breaking existing code by changing reset() to cleanup()
- **Mitigation**: Keep both methods, cleanup() calls reset()
- **Fallback**: Add cleanup() as new method, leave reset() unchanged

### P2 Risks
**Risk**: Breaking backward compatibility
- **Mitigation**: Default max_history_size=1000 (generous)
- **Fallback**: Set max_history_size=0 for unlimited (old behavior)

---

## Post-Completion Actions

1. **Update Documentation**
   - Add "Memory Safety" section to README.md
   - Document max_history_size in SimulationRunner docs
   - Update production deployment guide

2. **Monitor in Production**
   - Track memory usage every 1000 steps
   - Alert if growth exceeds 1 MB per 10,000 steps
   - Periodic cleanup() every 100,000 steps

3. **Performance Testing**
   - Benchmark STA-SMC with/without cache=True
   - Verify no performance regression
   - Document Numba cache benefits

4. **Future Improvements**
   - Add memory profiling to CI/CD pipeline
   - Automated leak detection in nightly tests
   - Memory usage dashboard for production

---

## Ready to Execute?

**Prerequisites**:
- ✅ CA-01 + CA-02 audits complete
- ✅ Baseline measurements documented
- ✅ Test scripts validated and working
- ✅ Git repository clean (all changes committed)

**Next Command**:
```bash
# Start with P0 fix
# User says "GO" or "START P0"
```

---

**Plan Status**: [OK] READY TO EXECUTE
**Total Estimated Time**: 6.6-7.3 hours
**Expected Outcome**: 4/4 controllers production-ready, score 90-95/100
**Blocker Resolution**: STA-SMC memory leak fixed (23.64 MB → <5 MB)
