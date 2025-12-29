# CA-02 Execution Plan: Cross-Cutting Memory Management Audit

**Type**: Comprehensive Audit
**Duration**: 8 hours
**Date**: November 11, 2025
**Status**: IN PROGRESS
**Scope**: Memory management across all controllers, core simulation engine, and integration points

---

## Objectives

Verify memory safety across the entire controller-simulation system to ensure:
1. No memory leaks in long-running simulations (1000+ cycles)
2. Proper cleanup of controller resources (weakref, explicit cleanup)
3. Bounded memory growth under stress testing
4. Production-ready memory management patterns

**Success Criteria**: Memory management score 85/100 → 95/100, achieving full production-ready status.

---

## Scope Definition

### Target Components (Priority Order)

1. **All 4 Controllers** (highest priority)
   - `src/controllers/classic_smc.py` (ClassicalSMC)
   - `src/controllers/sta_smc.py` (STASMC)
   - `src/controllers/adaptive_smc.py` (AdaptiveSMC)
   - `src/controllers/hybrid_adaptive_sta_smc.py` (HybridAdaptiveSTASMC)

2. **Core Simulation Engine**
   - `src/simulation/engines/simulation_runner.py` (run_simulation function)
   - `src/simulation/context/simulation_context.py` (SimulationContext)
   - `src/simulation/engines/vector_sim.py` (batch simulation)

3. **Integration Points**
   - `src/controllers/factory.py` (SMCFactory, create_controller)
   - `src/optimizer/pso_optimizer.py` (PSOTuner, PSO wrappers)
   - `src/orchestration/orchestrator.py` (if exists)

4. **Test Infrastructure**
   - `tests/test_integration/test_memory_management/` (existing tests)
   - `tests/test_integration/test_thread_safety/` (memory safety tests)

---

## Phase 1: Code Review for Memory Patterns (2 hours)

### Tasks

#### 1.1 Circular Reference Analysis (45 min)
- [ ] Search for `self.callback = callback` patterns (creates strong refs)
- [ ] Search for `self.parent = parent` patterns (parent-child cycles)
- [ ] Search for `self.history = []` patterns (unbounded lists)
- [ ] Search for `self.observers = []` patterns (observer leaks)
- [ ] Document all potential circular references with line numbers

**Tool**: Grep for patterns like `self\.\w+ = .*\bself\b`, `callback`, `parent`, `history`, `observers`

#### 1.2 Weakref Usage Verification (30 min)
- [ ] Verify all callbacks use `weakref.ref()` or `weakref.WeakMethod()`
- [ ] Check all parent references use `weakref.proxy()` or `weakref.ref()`
- [ ] Verify weakref cleanup handlers exist where needed
- [ ] Document weakref patterns (good examples)

**Tool**: Grep for `weakref`, `WeakMethod`, `proxy`, `ref()`

#### 1.3 Cleanup Method Audit (30 min)
- [ ] Verify all 4 controllers implement `cleanup()` method
- [ ] Check cleanup methods actually release resources (set to None, clear lists)
- [ ] Verify factory calls cleanup when needed
- [ ] Test cleanup methods (manual verification)
- [ ] Document cleanup patterns and gaps

**Tool**: Grep for `def cleanup`, `def __del__`, manual code review

#### 1.4 __del__ Implementation Review (15 min)
- [ ] Search for `__del__` methods (anti-pattern in Python)
- [ ] Document any `__del__` usage and whether it's safe
- [ ] Recommend replacing `__del__` with explicit cleanup

**Tool**: Grep for `def __del__`

**Deliverable**: `PHASE1_MEMORY_PATTERNS.md` (memory patterns report)

---

## Phase 2: Leak Detection (2 hours)

### Tasks

#### 2.1 Create Leak Detection Script (30 min)
- [ ] Create `detect_memory_leaks.py` script using tracemalloc
- [ ] Track memory before/after 1000 simulation cycles
- [ ] Test all 4 controller types
- [ ] Log memory snapshots at intervals (100, 500, 1000 cycles)
- [ ] Calculate memory growth rate (MB/cycle)

**Script Template**:
```python
import tracemalloc
import gc
from src.controllers.factory import create_controller
from src.config import load_config

def detect_leaks(controller_type, num_cycles=1000):
    tracemalloc.start()
    config = load_config("config.yaml")
    gains = config.controller_defaults[controller_type].gains

    # Baseline
    snapshot_start = tracemalloc.take_snapshot()

    # Simulate cycles
    for i in range(num_cycles):
        controller = create_controller(controller_type, config, gains)
        # ... run simulation ...
        del controller
        gc.collect()

        if i in [100, 500, 1000]:
            snapshot = tracemalloc.take_snapshot()
            # Log memory diff

    snapshot_end = tracemalloc.take_snapshot()
    # Analyze diff
```

#### 2.2 Run Leak Detection (1 hour)
- [ ] Run script for `classical_smc` (1000 cycles)
- [ ] Run script for `sta_smc` (1000 cycles)
- [ ] Run script for `adaptive_smc` (1000 cycles)
- [ ] Run script for `hybrid_adaptive_sta_smc` (1000 cycles)
- [ ] Collect memory snapshots at 0, 100, 500, 1000 cycles

#### 2.3 Identify Leaking Objects (30 min)
- [ ] Analyze tracemalloc diff output
- [ ] Identify top 10 memory allocations
- [ ] Trace leaking objects back to source code
- [ ] Document confirmed leaks with line numbers
- [ ] Categorize leaks by severity (critical, major, minor)

**Deliverable**: `PHASE2_LEAK_DETECTION_RESULTS.md` (leak detection report)

---

## Phase 3: Stress Testing (2 hours)

### Tasks

#### 3.1 Create Stress Test Script (30 min)
- [ ] Create `stress_test_memory.py` script
- [ ] Test 1000+ simulation cycles per controller
- [ ] Monitor memory using `psutil` (RSS, VMS)
- [ ] Generate memory usage plot (matplotlib)
- [ ] Log peak memory, average memory, memory growth rate

**Script Template**:
```python
import psutil
import os
import matplotlib.pyplot as plt
from src.controllers.factory import create_controller
from src.simulation.engines.simulation_runner import run_simulation

def stress_test(controller_type, num_cycles=1000):
    process = psutil.Process(os.getpid())
    memory_samples = []

    for i in range(num_cycles):
        # Create controller
        controller = create_controller(...)

        # Run simulation
        t, x, u = run_simulation(...)

        # Measure memory
        mem_info = process.memory_info()
        memory_samples.append(mem_info.rss / 1024 / 1024)  # MB

        # Cleanup
        del controller

    # Plot memory usage
    plt.plot(memory_samples)
    plt.xlabel("Cycle")
    plt.ylabel("Memory (MB)")
    plt.title(f"Memory Usage: {controller_type}")
    plt.savefig(f"memory_{controller_type}.png")
```

#### 3.2 Run Stress Tests (1 hour)
- [ ] Run stress test for `classical_smc` (1000 cycles)
- [ ] Run stress test for `sta_smc` (1000 cycles)
- [ ] Run stress test for `adaptive_smc` (1000 cycles)
- [ ] Run stress test for `hybrid_adaptive_sta_smc` (1000 cycles)
- [ ] Generate memory usage plots for each controller

#### 3.3 Analyze Stress Test Results (30 min)
- [ ] Calculate memory growth rate for each controller (MB/cycle)
- [ ] Identify unbounded memory growth (linear, quadratic)
- [ ] Compare controllers (which is most memory-efficient?)
- [ ] Document stress test results with plots
- [ ] Flag any controller with >10 MB growth over 1000 cycles

**Deliverable**: `PHASE3_STRESS_TEST_RESULTS.md` (stress test report + plots)

---

## Phase 4: Cleanup Verification (1.5 hours)

### Tasks

#### 4.1 Manual Cleanup Testing (45 min)
- [ ] Test ClassicalSMC.cleanup() (verify all attrs set to None)
- [ ] Test STASMC.cleanup() (verify all attrs set to None)
- [ ] Test AdaptiveSMC.cleanup() (verify all attrs set to None)
- [ ] Test HybridAdaptiveSTASMC.cleanup() (verify all attrs set to None)
- [ ] Verify weakref cleanup handlers trigger correctly

**Test Template**:
```python
def test_cleanup_manual():
    controller = create_controller("classical_smc", ...)

    # Verify attributes exist
    assert hasattr(controller, 'gains')
    assert hasattr(controller, '_callbacks')

    # Call cleanup
    controller.cleanup()

    # Verify cleanup
    assert controller.gains is None
    assert controller._callbacks == []
```

#### 4.2 Orphaned Object Detection (30 min)
- [ ] Run gc.get_objects() before/after controller creation
- [ ] Count objects by type (dict, list, function, etc.)
- [ ] Identify orphaned objects (objects that should be deleted but aren't)
- [ ] Document orphaned objects with types and counts

#### 4.3 Reset Functionality Testing (15 min)
- [ ] Test reset functionality (if exists)
- [ ] Verify reset clears history but keeps gains
- [ ] Document reset behavior

**Deliverable**: `PHASE4_CLEANUP_VERIFICATION.md` (cleanup verification report)

---

## Phase 5: Fix Recommendations and Validation (30 min)

### Tasks

#### 5.1 Prioritize Leaks by Severity (10 min)
- [ ] Categorize leaks: CRITICAL (>50 MB), MAJOR (10-50 MB), MINOR (<10 MB)
- [ ] Prioritize by impact on production use
- [ ] Estimate effort per fix (1-8 hours)

#### 5.2 Design Fixes (15 min)
- [ ] For each confirmed leak, design fix:
  - Circular reference → Use weakref
  - Unbounded list growth → Add max_size limit or periodic cleanup
  - Missing cleanup → Add cleanup() method
  - __del__ usage → Replace with explicit cleanup
- [ ] Document fix recommendations with code examples

#### 5.3 Update Final Report (5 min)
- [ ] Compile all phase reports into `CA-02_FINAL_MEMORY_AUDIT_REPORT.md`
- [ ] Calculate memory management score (0-100)
- [ ] Document production-readiness status
- [ ] Provide actionable recommendations

**Deliverable**: `CA-02_FINAL_MEMORY_AUDIT_REPORT.md` (comprehensive memory audit report)

---

## Validation Requirements

### Before Audit Complete:
1. [ ] All 4 controllers reviewed for memory patterns
2. [ ] Leak detection run for ≥1000 cycles per controller
3. [ ] Stress test run for ≥1000 cycles per controller
4. [ ] Cleanup methods manually tested for 4 controllers
5. [ ] All confirmed leaks documented with line numbers
6. [ ] Fix recommendations prioritized by severity
7. [ ] Memory usage plots generated for all controllers
8. [ ] Final report compiled and committed

### Success Criteria:
- [ ] Can answer: "Is the system memory-safe for long-running use?"
- [ ] Memory growth rate <5 MB per 1000 cycles for all controllers
- [ ] No critical memory leaks (>50 MB growth)
- [ ] All cleanup methods verified to work
- [ ] Production deployment memory guidelines documented

---

## Deliverables Checklist

1. [ ] `PHASE1_MEMORY_PATTERNS.md` - Memory pattern report
2. [ ] `PHASE2_LEAK_DETECTION_RESULTS.md` - Leak detection results
3. [ ] `PHASE3_STRESS_TEST_RESULTS.md` - Stress test results with plots
4. [ ] `PHASE4_CLEANUP_VERIFICATION.md` - Cleanup verification results
5. [ ] `CA-02_FINAL_MEMORY_AUDIT_REPORT.md` - Comprehensive final report
6. [ ] `detect_memory_leaks.py` - Leak detection script
7. [ ] `stress_test_memory.py` - Stress test script
8. [ ] `memory_*.png` - Memory usage plots (4 files)

---

## Time Tracking

| Phase | Task | Estimated | Actual | Status |
|-------|------|-----------|--------|--------|
| **Phase 1** | Circular reference analysis | 45 min | - | PENDING |
| | Weakref usage verification | 30 min | - | PENDING |
| | Cleanup method audit | 30 min | - | PENDING |
| | __del__ review | 15 min | - | PENDING |
| **Phase 2** | Create leak detection script | 30 min | - | PENDING |
| | Run leak detection | 1 hour | - | PENDING |
| | Identify leaking objects | 30 min | - | PENDING |
| **Phase 3** | Create stress test script | 30 min | - | PENDING |
| | Run stress tests | 1 hour | - | PENDING |
| | Analyze stress test results | 30 min | - | PENDING |
| **Phase 4** | Manual cleanup testing | 45 min | - | PENDING |
| | Orphaned object detection | 30 min | - | PENDING |
| | Reset functionality testing | 15 min | - | PENDING |
| **Phase 5** | Prioritize leaks | 10 min | - | PENDING |
| | Design fixes | 15 min | - | PENDING |
| | Update final report | 5 min | - | PENDING |
| **TOTAL** | | **8 hours** | **0 hours** | **IN PROGRESS** |

---

## Notes

- Use `tracemalloc` for leak detection (built-in Python module)
- Use `psutil` for stress testing (may need pip install)
- Use `matplotlib` for plotting (already in requirements.txt)
- Follow CA-01 audit structure for consistency
- Commit deliverables incrementally (phase by phase)
- Use existing tests in `tests/test_integration/test_memory_management/` as reference

---

## References

- CA-01 Audit: `academic/qa_audits/CA-01_CONTROLLER_SIMULATION_AUDIT/CA-01_FINAL_AUDIT_REPORT.md`
- Memory Management Config: `.ai_workspace/config/controller_memory.md`
- Thread Safety Tests: `tests/test_integration/test_thread_safety/test_production_thread_safety.py`
- Existing Memory Tests: `tests/test_integration/test_memory_management/`
