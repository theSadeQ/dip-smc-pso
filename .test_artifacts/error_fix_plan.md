# RUFF Error Fix Plan - Phase 5 Round 3

**Date**: 2025-10-07
**Total Errors**: 75 (reduced from 76 after auto-fix)
**MCP Workflow**: Multi-server debugging validation

---

## Error Breakdown by Type

### 1. E722: Bare except (23 errors) - HIGH PRIORITY
**Pattern**: `except:` → `except Exception:`

**Affected Files:**
- src/analysis/core/metrics.py:266
- src/analysis/fault_detection/fdi_system.py:572, 598, 643
- src/analysis/performance/robustness.py:463, 471, 539
- src/analysis/performance/stability_analysis.py:589, 614, 872, 985
- src/analysis/visualization/analysis_plots.py:383, 596, 763, 777
- src/interfaces/network/udp_interface_deadlock_free.py:206
- src/optimization/algorithms/evolutionary/genetic.py:574
- src/optimization/algorithms/gradient_based/bfgs.py:397, 442, 457
- src/optimization/algorithms/gradient_based/nelder_mead.py:458
- src/optimization/objectives/multi/pareto.py:457
- src/optimization/validation/pso_bounds_validator.py:367

**Fix Strategy**: Replace bare except with specific exception type

---

### 2. F401: Unused import (20 errors) - MEDIUM PRIORITY
**Pattern**: Remove unused imports or add to `__all__`

**Affected Files:**
- src/integration/compatibility_matrix.py:469, 470
- src/integration/production_readiness.py:28, 29
- src/interfaces/hardware/daq_systems.py:24 (2 imports)
- src/interfaces/hil/real_time_sync.py:30
- src/interfaces/network/udp_interface_deadlock_free.py:32, 33 (4 imports)
- src/optimization/__init__.py:35, 42, 43 (4 imports)
- src/optimization/objectives/control/stability.py:17, 18
- src/simulation/__init__.py:68, 69, 70

**Fix Strategy**:
1. Check if import is used elsewhere in module
2. Remove if truly unused
3. Add to `__all__` if part of public API

---

### 3. E402: Module import not at top (19 errors) - MEDIUM PRIORITY
**Pattern**: Move imports to top of file (after docstring/copyright)

**Affected Files:**
- src/analysis/fault_detection/fdi_system.py:1043, 1044
- src/analysis/validation/cross_validation.py:86
- src/analysis/visualization/analysis_plots.py:26, 27, 29
- src/analysis/visualization/statistical_plots.py:26, 27
- src/interfaces/hardware/serial_devices.py:14-19 (7 imports)
- src/optimization/tuning/pso_hyperparameter_optimizer.py:32-35 (4 imports)

**Fix Strategy**: Move imports to top, preserve conditional imports if necessary

---

### 4. E741: Ambiguous variable name (7 errors) - LOW PRIORITY
**Pattern**: Rename `l`, `I`, `O` to descriptive names

**Affected Files:**
- src/analysis/fault_detection/residual_generators.py:341 (`O`)
- src/analysis/performance/control_analysis.py:39, 41 (`O`)
- src/optimization/algorithms/gradient_based/bfgs.py:244 (`I`)
- src/optimization/validation/pso_bounds_optimizer.py:258, 263, 281 (`l`)

**Fix Strategy**: Rename to descriptive variable names

---

### 5. F811: Redefined while unused (3 errors) - CRITICAL
**Pattern**: Remove duplicate definition or rename

**Affected Files:**
- src/analysis/core/__init__.py:23 (`AnalysisConfiguration`)
- src/analysis/fault_detection/threshold_adapters.py:579 (`update`)
- src/simulation/__init__.py:58 (`SimulationContext`)

**Fix Strategy**: Remove duplicate import/definition

---

### 6. F403: Import star (3 errors) - LOW PRIORITY
**Pattern**: Replace `from module import *` with explicit imports

**Affected Files:**
- src/fault_detection/__init__.py:17
- src/fault_detection/fdi.py:17
- src/utils/control_analysis.py:14

**Fix Strategy**: Make imports explicit or suppress if intentional re-export

---

## Execution Order (Priority-based)

1. **F811** (3 errors) - Critical duplicates
2. **E722** (23 errors) - Code quality and error handling
3. **F401** (20 errors) - Clean up unused imports
4. **E402** (19 errors) - Organize import structure
5. **E741** (7 errors) - Improve readability
6. **F403** (3 errors) - Make imports explicit

---

## Validation Checklist

- [ ] All 75 errors resolved
- [ ] No new errors introduced
- [ ] Test suite passes
- [ ] Git diff reviewed
- [ ] Commit with detailed summary
