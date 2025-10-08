# Documentation Coverage Implementation Plan
## Phase 1.3 Actionable Roadmap

**Plan Date:** 2025-10-07
**Baseline:** Phase 1.3 AST Analysis
**Target Completion:** 3 months (74 hours total effort)

---

## Executive Summary

Based on comprehensive AST analysis of 316 Python files:

- **Current State:**
  - Type Hint Coverage: 89.0% (target: 95%, gap: 6.0%)
  - Undocumented Classes: 52/712 (7.3%)
  - Undocumented Public Methods: 72/1,628 (4.4%) - **ALREADY PASSING <5% TARGET**

- **Critical Blockers:**
  - 2 core dynamics modules have 0% type hints (CRITICAL)
  - 15 P0 controller/factory classes undocumented
  - 14 P0 controller methods undocumented

- **Positive Findings:**
  - 164 modules (47%) already exceed 95% type hint coverage
  - 50 modules (14%) have 100% perfect type hints
  - Method documentation already meets <5% target

---

## Phase 1: Critical Blockers (Week 1, 14h)

**Objective:** Resolve CRITICAL type hint gaps and document P0 classes/methods

### Task 1.1: Core Dynamics Type Hints (8h)

**BLOCKING ISSUE:** Core dynamics modules have 0% type hint coverage

**Files:**
```
src/core/dynamics.py (0% → 95%)
src/core/dynamics_full.py (0% → 95%)
```

**Strategy:**
1. Run mypy strict mode to identify all missing annotations
   ```bash
   mypy src/core/dynamics.py --strict --show-error-codes > dynamics_type_errors.txt
   mypy src/core/dynamics_full.py --strict --show-error-codes > dynamics_full_type_errors.txt
   ```

2. Add type hints systematically:
   - Function parameters
   - Return types
   - Class attributes
   - Property return types

3. Use typing module generics where needed:
   ```python
# example-metadata:
# runnable: false

   from typing import Tuple, Optional, Callable, Dict, List
   import numpy.typing as npt

   def f(state: npt.NDArray[np.float64], u: float) -> npt.NDArray[np.float64]:
       ...
   ```

4. Validate with mypy until 0 errors
   ```bash
   mypy src/core/dynamics.py --strict  # Should pass
   ```

**Estimated Lines:** ~500 type annotations total

**Acceptance Criteria:**
- [ ] `mypy src/core/dynamics.py --strict` passes with 0 errors
- [ ] `mypy src/core/dynamics_full.py --strict` passes with 0 errors
- [ ] Type hint coverage ≥95% for both files

**Effort:** 8 hours (4h per file)

---

### Task 1.2: P0 Class Documentation (4h)

**Target:** 15 undocumented P0 classes (30 min each)

**Template (NumPy-style):**
```python
# example-metadata:
# runnable: false

class MPCConfig:
    """
    Configuration dataclass for Model Predictive Controller.

    Encapsulates MPC-specific parameters including prediction horizon,
    control horizon, and constraint matrices.

    Parameters
    ----------
    prediction_horizon : int
        Number of steps to predict ahead (N).
    control_horizon : int
        Number of control moves to optimize (M).
    Q : np.ndarray
        State cost matrix (n x n).
    R : np.ndarray
        Control cost matrix (m x m).

    Attributes
    ----------
    N : int
        Prediction horizon.
    M : int
        Control horizon.

    Examples
    --------
    >>> config = MPCConfig(prediction_horizon=10, control_horizon=5, Q=np.eye(4), R=np.eye(1))
    >>> print(config.N)
    10
    """
```

**Priority Order:**
1. `controllers/factory.py:MPCConfig` - User-facing factory config
2. `controllers/factory.py:UnavailableMPCConfig` - Fallback config
3. `controllers/factory/core/registry.py:ModularClassicalSMC` - Core registry
4. `controllers/factory/core/registry.py:ModularSuperTwistingSMC`
5. `controllers/factory/core/registry.py:ModularAdaptiveSMC`
6. `controllers/factory/core/registry.py:ModularHybridSMC`
7. `controllers/factory/smc_factory.py:ClassicalSMC` - Factory imports
8. `controllers/factory/smc_factory.py:AdaptiveSMC`
9. `controllers/factory/smc_factory.py:SuperTwistingSMC`
10. `controllers/factory/smc_factory.py:HybridAdaptiveSTASMC`
11. `controllers/mpc/mpc_controller.py:MPCWeights` - MPC weights dataclass
12. `controllers/smc/sta_smc.py:_DummyNumba` - Test dummy
13. `controllers/specialized/swing_up_smc.py:_History` - Internal history class
14. `controllers/factory/legacy_factory.py:_DummyDyn` - Test dummy
15. `controllers/factory/core/registry.py:MPCConfig` - Duplicate definition

**Checklist per class:**
- [ ] Brief description (1-2 sentences)
- [ ] Parameters section (if applicable)
- [ ] Attributes section
- [ ] Example usage (if public API)
- [ ] Cross-references to related classes

**Effort:** 4 hours (15 classes × 15-20 min average)

---

### Task 1.3: P0 Method Documentation (2h)

**Target:** 14 undocumented P0 controller methods

**Template:**
```python
# example-metadata:
# runnable: false

def compute_control(
    self,
    state: np.ndarray,
    state_vars: Dict[str, Any],
    history: Dict[str, np.ndarray]
) -> Tuple[float, Dict[str, Any], Dict[str, np.ndarray]]:
    """
    Compute control output using hybrid adaptive super-twisting SMC.

    Combines adaptive gain tuning with super-twisting algorithm for
    chattering reduction while maintaining robustness.

    Parameters
    ----------
    state : np.ndarray, shape (4,)
        Current system state [x, theta1, theta2, x_dot, theta1_dot, theta2_dot].
    state_vars : dict
        Controller internal state variables.
    history : dict
        Historical data for control computation.

    Returns
    -------
    u : float
        Control force in Newtons.
    updated_state_vars : dict
        Updated controller state variables.
    updated_history : dict
        Updated historical data.

    Notes
    -----
    The hybrid controller switches between adaptive and STA modes based on
    the magnitude of the sliding surface. See [1]_ for theoretical details.

    References
    ----------
    .. [1] Utkin, V., Guldner, J., & Shi, J. (2009). Sliding Mode Control
           in Electro-Mechanical Systems. CRC Press.

    Examples
    --------
    >>> controller = HybridAdaptiveSTASMC(gains=[...])
    >>> state = np.array([0.1, 0.05, 0.03, 0.0, 0.0, 0.0])
    >>> u, state_vars, history = controller.compute_control(state, {}, {})
    """
```

**Priority Methods:**
1. `HybridAdaptiveSTASMC.compute_control`
2. `HybridAdaptiveSTASMC.gains` (property)
3. `HybridAdaptiveSTASMC.initialize_history`
4. `HybridAdaptiveSTASMC.initialize_state`
5. `SuperTwistingSMC.compute_control`
6. `SuperTwistingSMC.initialize_history`
7. `SwingUpSMC.compute_control`
8. `SwingUpSMC.initialize_history`
9. `SwingUpSMC.initialize_state`
10. `SwingUpSMC.mode` (property)
11. `SwingUpSMC.switch_time` (property)

**Test Dummies (minimal docs):**
12. `_DummyDyn.f`
13. `_DummyDyn.step`
14. `_DummyNumba.njit`

**Effort:** 2 hours (14 methods × 8-10 min average)

---

**Phase 1 Deliverables:**
- [ ] Core dynamics modules: 95%+ type hints
- [ ] 15 P0 classes fully documented
- [ ] 14 P0 methods fully documented
- [ ] Type hint coverage improves from 89.0% → 91.5%

**Phase 1 Total Effort:** 14 hours

---

## Phase 2: High-Priority Modules (Weeks 2-3, 20h)

**Objective:** Complete type hints for high-priority modules and document P1/P2 classes

### Task 2.1: Legacy Factory Type Hints (4h)

**File:** `controllers/factory/legacy_factory.py`
**Current Coverage:** 19% (gap: -76%)
**Target:** 95%

**Strategy:**
- Large file (~1000 lines)
- Focus on public API functions first
- Use `TypedDict` for configuration dictionaries
- Add `Protocol` classes for duck typing

**Acceptance Criteria:**
- [ ] Type hint coverage ≥95%
- [ ] mypy --strict passes

---

### Task 2.2: Config Schemas Type Hints (2h)

**File:** `config/schemas.py`
**Current Coverage:** 46% (gap: -49%)
**Target:** 95%

**Strategy:**
- Pydantic models (many auto-typed)
- Add explicit `Field()` type annotations
- Document complex nested types

**Acceptance Criteria:**
- [ ] Type hint coverage ≥95%
- [ ] Pydantic validation tests pass

---

### Task 2.3: Registry Type Hints (3h)

**File:** `controllers/factory/core/registry.py`
**Current Coverage:** 33% (gap: -62%)
**Target:** 95%

**Strategy:**
- Registry pattern with dynamic lookups
- Use `Type[Controller]` for class references
- Generic types for factory returns

---

### Task 2.4: Cross-Validation Type Hints (2h)

**File:** `analysis/validation/cross_validation.py`
**Current Coverage:** 55% (gap: -40%)
**Target:** 95%

**Strategy:**
- Statistical validation classes
- Use `Iterator` and `Generator` types
- Add numpy array shape annotations

---

### Task 2.5: P1 Class Documentation (1.5h)

**Target:** 3 P1 classes

1. `interfaces/hil/plant_server.py:Model`
2. `interfaces/hil/plant_server.py:PlantServer`
3. `optimization/tuning/pso_hyperparameter_optimizer.py:FallbackResult`

**Template:** Same NumPy-style as P0 classes

---

### Task 2.6: P2 Class Documentation (2h)

**Target:** 4 P2 cross-validation classes

All in `analysis/validation/cross_validation.py`:
1. `KFold`
2. `LeaveOneOut`
3. `StratifiedKFold`
4. `TimeSeriesSplit`

**Special Focus:**
- Cross-reference sklearn documentation
- Add examples with controller validation
- Document usage in Monte Carlo validation

---

### Task 2.7: P1+P2 Method Documentation (5.5h)

**Target:** 13 methods

**HIL Methods (4 methods, 2h):**
- `Model.step`
- `PlantServer.close`
- `PlantServer.start`
- `PlantServer.stop`

**Plant Config Methods (8 methods, 3h):**
- `BasicControllerConfig.check_physical_consistency`
- `BasicControllerConfig.create_default`
- `BasicControllerConfig.from_dict`
- `BasicControllerConfig.get_numerical_parameters`
- `BasicControllerConfig.get_physical_parameters`
- `BasicControllerConfig.get_system_scales`
- `BasicControllerConfig.to_dict`
- `BasicControllerConfig.validate`

**Cross-Validation Methods (4 methods, 2h):**
- `KFold.split`
- `LeaveOneOut.split`
- `StratifiedKFold.split`
- `TimeSeriesSplit.split`

**Optimization Factory (1 method, 0.5h):**
- `create_pid_controller`

---

**Phase 2 Deliverables:**
- [ ] 4 high-priority modules: 95%+ type hints
- [ ] 3 P1 classes fully documented
- [ ] 4 P2 classes fully documented
- [ ] 13 P1+P2 methods fully documented
- [ ] Type hint coverage improves from 91.5% → 94.0%

**Phase 2 Total Effort:** 20 hours

---

## Phase 3: Medium-Priority Completion (Month 2, 30h)

**Objective:** Achieve 95%+ type hint coverage and document remaining classes

### Task 3.1: Medium-Priority Type Hints (15h)

**Target:** 25 modules with 10-30% gap to 95%

**Batch Strategy:**
- Group by domain (interfaces, optimization, simulation)
- Dedicate 30-45 min per module
- Use automated tools where possible

**Key Modules:**
- `utils/reproducibility/__init__.py` (25% → 95%)
- `analysis/__init__.py` (40% → 95%)
- `analysis/validation/cross_validation.py` (55% → 95%)
- `analysis/visualization/analysis_plots.py` (59% → 95%)
- `interfaces/hil/test_automation.py` (65% → 95%)
- ... (20 more modules)

**Automation:**
```bash
# Use MonkeyType for runtime type inference
pip install MonkeyType
monkeytype run -m pytest tests/
monkeytype apply module_name
```

---

### Task 3.2: P3 Class Documentation (15h)

**Target:** 30 P3 classes

**Config Schemas (20 classes, 10h):**
- Batch documentation using template generator
- Focus on parameter descriptions
- Cross-reference config.yaml

**Network Protocols (6 classes, 3h):**
- Brief protocol descriptions
- Reference implementation examples

**Miscellaneous (4 classes, 2h):**
- Edge cases and utilities

---

**Phase 3 Deliverables:**
- [ ] 25 medium-priority modules: 95%+ type hints
- [ ] 30 P3 classes fully documented
- [ ] Type hint coverage improves from 94.0% → 95.5%+
- [ ] Undocumented classes reduced from 52 → 22

**Phase 3 Total Effort:** 30 hours

---

## Phase 4: Polish and Automation (Month 3+, 10h)

**Objective:** Final touch-ups, automation, and quality gates

### Task 4.1: Type Hint Touch-Ups (5h)

**Target:** Remaining 118 modules with <10% gap

**Strategy:**
- Low-hanging fruit (mostly 1-2 missing annotations per file)
- Batch processing with automated tools
- Focus on public APIs

---

### Task 4.2: P3 Method Documentation (3h)

**Target:** 45 P3 utility methods

**Categories:**
- Property accessors (minimal docs)
- Serialization methods (format descriptions)
- Utility functions (one-liner descriptions)

---

### Task 4.3: Automation and Quality Gates (2h)

**Pre-commit Hooks:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        args: [--strict, --show-error-codes]
        additional_dependencies: [types-all]

  - repo: https://github.com/pycqa/pydocstyle
    rev: 6.3.0
    hooks:
      - id: pydocstyle
        args: [--convention=numpy]
```

**CI/CD Quality Gates:**
```yaml
# .github/workflows/documentation-quality.yml
name: Documentation Quality
on: [pull_request]
jobs:
  type-hints:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check Type Hint Coverage
        run: |
          python .dev_tools/analyze_documentation_coverage.py
          COVERAGE=$(jq '.summary.overall_type_hint_coverage' docs/DOCUMENTATION_COVERAGE_MATRIX.json)
          if (( $(echo "$COVERAGE < 95.0" | bc -l) )); then
            echo "Type hint coverage $COVERAGE% below 95% threshold"
            exit 1
          fi
```

**Documentation Templates:**
```bash
# Auto-generate docstring stubs
python -m pydocstyle --add-ignore=D100,D101,D102,D103 src/ > missing_docs.txt

# Use docstring generator
pip install pyment
pyment -w -o numpydoc src/module.py
```

---

**Phase 4 Deliverables:**
- [ ] Type hint coverage ≥95.5% (target achieved)
- [ ] All public classes documented (52 → 0)
- [ ] Pre-commit hooks enforcing quality
- [ ] CI/CD gates preventing regressions
- [ ] Automated docstring generation tooling

**Phase 4 Total Effort:** 10 hours

---

## Overall Timeline

```
Week 1:       Phase 1 - Critical Blockers (14h)
Weeks 2-3:    Phase 2 - High Priority (20h)
Weeks 4-8:    Phase 3 - Medium Priority (30h)
Weeks 9-12:   Phase 4 - Polish & Automation (10h)

Total: 3 months, 74 hours
```

---

## Success Metrics

### Quantitative Targets

| Metric | Baseline (Phase 1.3) | Target | Status |
|--------|---------------------|--------|--------|
| **Type Hint Coverage** | 89.0% | ≥95.0% | 🟡 In Progress |
| **Undocumented Classes** | 52/712 (7.3%) | 0/712 (0%) | 🟡 In Progress |
| **Undocumented Methods** | 72/1,628 (4.4%) | <5% | ✅ **PASSING** |
| **Modules at 95%+** | 164/316 (52%) | 250/316 (79%) | 🟡 In Progress |
| **Modules at 100%** | 50/316 (16%) | 100/316 (32%) | 🟡 In Progress |

### Qualitative Targets

- [ ] All public APIs have NumPy-style docstrings
- [ ] Examples included for major workflows
- [ ] Cross-references between related classes
- [ ] Type hints validated by mypy strict mode
- [ ] Pre-commit hooks prevent documentation debt
- [ ] CI/CD gates enforce quality standards

---

## Risk Mitigation

### Risk 1: Type Hint Complexity

**Risk:** Complex generic types may be difficult to annotate
**Mitigation:** Use `typing.cast()` and `# type: ignore` sparingly with justification
**Fallback:** Document type contracts in docstrings if static typing insufficient

### Risk 2: Legacy Code Compatibility

**Risk:** Adding type hints may break existing code
**Mitigation:** Run full test suite after each batch of annotations
**Fallback:** Use `if TYPE_CHECKING:` guards for import-only types

### Risk 3: Effort Underestimation

**Risk:** Actual effort may exceed 74h estimate
**Mitigation:** Track actual time spent per task, adjust subsequent estimates
**Fallback:** Prioritize P0/P1 items, defer P3 to future sprints

---

## Tooling and Resources

### Static Analysis
- **mypy** - Type hint validation
- **pydocstyle** - Docstring style checking
- **ruff** - Fast linting (already in use)

### Documentation Generators
- **pdoc** - Lightweight API documentation
- **sphinx** - Full documentation system (already configured)
- **pyment** - Automated docstring stub generation

### Type Hint Inference
- **MonkeyType** - Runtime type collection
- **pytype** - Google's static type inferencer
- **pyre** - Facebook's type checker

### Quality Monitoring
```bash
# Type hint coverage
python .dev_tools/analyze_documentation_coverage.py

# Docstring coverage
pydocstyle src/ --count

# Overall quality score
python .dev_tools/documentation_quality_score.py
```

---

## Appendix A: Quick Reference

### File Locations
- **Analysis Script:** `.dev_tools/analyze_documentation_coverage.py`
- **JSON Report:** `docs/DOCUMENTATION_COVERAGE_MATRIX.json`
- **Markdown Report:** `docs/DOCUMENTATION_COVERAGE_MATRIX.md`
- **Validation Report:** `docs/PHASE_1_2_VS_1_3_VALIDATION.md`
- **This Plan:** `docs/DOCUMENTATION_IMPLEMENTATION_PLAN.md`

### Commands
```bash
# Re-run analysis
python .dev_tools/analyze_documentation_coverage.py

# Check type hints for specific file
mypy src/core/dynamics.py --strict --show-error-codes

# Check docstring style
pydocstyle src/controllers/factory.py --convention=numpy

# Generate documentation
cd docs && make html
```

### Templates
- **Class Docstring:** See Task 1.2
- **Method Docstring:** See Task 1.3
- **Type Annotation Examples:** See Task 1.1

---

## Appendix B: Priority Matrix

| Priority | Classes | Methods | Type Hint Modules | Total Effort |
|----------|---------|---------|-------------------|--------------|
| **P0** | 15 | 14 | 2 (dynamics) | 14h |
| **P1** | 3 | 9 | 4 (factory, config) | 12h |
| **P2** | 4 | 4 | 25 (medium gap) | 20h |
| **P3** | 30 | 45 | 87 (low gap) | 28h |
| **TOTAL** | **52** | **72** | **118** | **74h** |

---

**Plan Owner:** Documentation Team
**Last Updated:** 2025-10-07
**Next Review:** After Phase 1 completion (Week 1)
