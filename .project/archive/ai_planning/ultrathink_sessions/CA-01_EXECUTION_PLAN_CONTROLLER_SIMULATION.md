# CA-01 Execution Plan: Controller Factory ↔ Simulation Runner Integration Audit

**Status**: [READY] Ready to Execute
**Date**: November 11, 2025
**Duration**: 7 hours
**Auditor**: Claude Code (Autonomous Execution)

---

## Executive Summary

### Target Integration
**Component A**: Controller Factory (`src/controllers/factory/`)
- Primary: `smc_factory.py` - SMC controller creation
- Secondary: `pso_integration.py` - PSO wrapper integration
- Tertiary: `factory_new/` - New factory implementation

**Component B**: Simulation Runner (`src/simulation/engines/simulation_runner.py`)
- Primary: `run_simulation()` function
- Secondary: Dynamics model dispatcher (`get_step_fn()`)
- Tertiary: Integration with HIL and monitoring

### Why This Integration is Critical
This is the **most critical integration** in the entire system:
1. Every simulation depends on it working correctly
2. PSO optimization relies on it for controller tuning
3. All research results flow through this pipeline
4. Production deployments require bulletproof integration
5. 4 controller types × 2 dynamics models = 8 integration paths

### Current Integration Tests
Located in `tests/test_integration/`:
- `test_end_to_end/` - Full pipeline validation
- `test_error_recovery/` - Error handling
- `test_memory_management/` - Resource cleanup
- `test_numerical_stability/` - Stability validation
- `test_thread_safety/` - Concurrent operations
- `test_production_readiness.py` - Production validation

---

## Phase 1: Interface Discovery (1 hour)

### Task 1.1: Controller Factory Interface (20 min)
**Goal**: Document all interaction points between factory and simulation

**Actions**:
1. Map `create_controller()` → simulation runner flow
2. Document controller protocol requirements:
   - `compute_control(state, state_vars, history)` signature
   - `initialize_state()` hook
   - `initialize_history()` hook
   - `max_force` property
3. Identify PSO wrapper interface (`EnhancedPSOControllerWrapper`)
4. Extract type requirements from `SMCProtocol`

**Validation**:
```bash
# Verify controller creation for all 4 types
python -c "
from src.controllers.factory.smc_factory import create_controller, SMCType
for ctrl_type in SMCType:
    controller = create_controller(ctrl_type.value, gains=[1.0]*6)
    print(f'{ctrl_type.value}: {type(controller).__name__}')
    assert hasattr(controller, 'compute_control')
    assert hasattr(controller, 'initialize_state')
    assert hasattr(controller, 'initialize_history')
"
```

**Deliverable**: Interface contract document (signatures, types, protocols)

### Task 1.2: Simulation Runner Interface (20 min)
**Goal**: Document simulation runner expectations

**Actions**:
1. Extract `run_simulation()` signature and parameters
2. Document controller interface requirements:
   - What methods does simulation runner call?
   - What does it expect to receive back?
   - How does it handle initialization?
3. Map dynamics model interaction (`step(x, u, dt)`)
4. Identify optional hooks (latency monitoring, fallback controller)

**Validation**:
```bash
# Verify simulation runner accepts all controller types
python -c "
from src.controllers.factory.smc_factory import create_controller, SMCType
from src.simulation.engines.simulation_runner import run_simulation
from src.plant.models.dip_lowrank import DIPDynamics
import numpy as np

dynamics = DIPDynamics()
for ctrl_type in SMCType:
    controller = create_controller(ctrl_type.value, gains=[10.0, 5.0, 8.0, 3.0, 15.0, 2.0])
    t, x, u = run_simulation(
        controller=controller,
        dynamics_model=dynamics,
        sim_time=1.0,
        dt=0.01,
        initial_state=np.array([0.0, 0.1, 0.1, 0.0, 0.0, 0.0])
    )
    print(f'{ctrl_type.value}: {len(t)} steps, final state norm = {np.linalg.norm(x[-1])}')
"
```

**Deliverable**: Simulation runner interface requirements document

### Task 1.3: Data Contract Mapping (20 min)
**Goal**: Define expected data shapes and types

**Actions**:
1. Controller output format:
   - Return type: `float` or `np.ndarray`?
   - Scalar vs vector control?
   - Units and bounds?
2. State vector format:
   - Shape: `(6,)` for `[x, θ1, θ2, ẋ, θ̇1, θ̇2]`
   - Data type: `np.ndarray` with `dtype=float64`
   - Valid ranges for each component
3. History/state_vars format:
   - Dictionary structure
   - Required keys
   - Type expectations

**Validation**:
```python
# Create validation script: validate_data_contract.py
import numpy as np
from src.controllers.factory.smc_factory import create_controller, SMCType

def validate_data_contract():
    """Validate data contract between factory and simulation."""
    results = {}

    for ctrl_type in SMCType:
        controller = create_controller(ctrl_type.value, gains=[10.0]*6)

        # Test state initialization
        state_vars = controller.initialize_state()
        history = controller.initialize_history()

        # Test control computation
        state = np.array([0.0, 0.1, 0.1, 0.0, 0.0, 0.0])
        control = controller.compute_control(state, state_vars, history)

        results[ctrl_type.value] = {
            'state_vars_type': type(state_vars).__name__,
            'history_type': type(history).__name__,
            'control_type': type(control).__name__,
            'control_shape': getattr(control, 'shape', 'scalar'),
            'control_value': float(control) if np.isscalar(control) else control.tolist()
        }

    return results

if __name__ == '__main__':
    import json
    results = validate_data_contract()
    print(json.dumps(results, indent=2))
```

**Deliverable**: Data contract specification document

---

## Phase 2: Data Flow Analysis (1.5 hours)

### Task 2.1: Trace Full Simulation Loop (30 min)
**Goal**: Understand complete data flow from factory → simulation → results

**Actions**:
1. Create data flow tracing script:
   ```python
   # trace_data_flow.py
   # Insert logging at each integration point
   # Track: controller creation → initialization → control loop → output
   ```
2. Execute trace for each controller type
3. Generate flow diagram (ASCII or Mermaid)
4. Document data transformations at each step

**Validation**:
```bash
# Run with verbose logging
python trace_data_flow.py --controller classical_smc --verbose
python trace_data_flow.py --controller adaptive_smc --verbose
python trace_data_flow.py --controller sta_smc --verbose
python trace_data_flow.py --controller hybrid_adaptive_sta_smc --verbose
```

**Deliverable**: Data flow diagram with annotations

### Task 2.2: PSO Integration Data Flow (30 min)
**Goal**: Trace PSO wrapper → controller → simulation flow

**Actions**:
1. Map `EnhancedPSOControllerWrapper` transformations
2. Trace parameter injection: `gains` → controller initialization
3. Document wrapper's role:
   - Performance monitoring
   - Saturation handling
   - Error recovery
4. Verify wrapper doesn't corrupt data

**Validation**:
```python
# Compare wrapped vs unwrapped controller outputs
from src.controllers.factory.pso_integration import EnhancedPSOControllerWrapper
from src.controllers.factory.smc_factory import create_controller
import numpy as np

controller = create_controller('classical_smc', gains=[10.0]*6)
wrapped = EnhancedPSOControllerWrapper(
    controller=controller,
    controller_type='classical_smc',
    enable_monitoring=True
)

state = np.array([0.0, 0.1, 0.1, 0.0, 0.0, 0.0])
state_vars = controller.initialize_state()
history = controller.initialize_history()

# Direct call
direct_output = controller.compute_control(state, state_vars, history)

# Wrapped call
wrapped_output = wrapped(state)

print(f"Direct: {direct_output}, Wrapped: {wrapped_output}")
assert np.allclose(direct_output, wrapped_output, rtol=1e-6)
```

**Deliverable**: PSO integration data flow analysis

### Task 2.3: Type Consistency Verification (30 min)
**Goal**: Ensure no type mismatches across integration boundary

**Actions**:
1. Create type checker script using `mypy` or runtime checks
2. Verify controller output matches simulation input expectations
3. Check state_vars and history types across boundaries
4. Document any type coercions or conversions

**Validation**:
```bash
# Run mypy on integration modules
mypy src/controllers/factory/smc_factory.py
mypy src/simulation/engines/simulation_runner.py
mypy src/controllers/factory/pso_integration.py

# Runtime type validation
python -m pytest tests/test_integration/test_end_to_end/ -v --tb=short
```

**Deliverable**: Type consistency report with identified issues

---

## Phase 3: Error Handling Verification (1.5 hours)

### Task 3.1: Controller Failure Scenarios (30 min)
**Goal**: Verify simulation handles controller failures gracefully

**Actions**:
1. Test scenarios:
   - Controller raises exception during initialization
   - Controller returns NaN/Inf during computation
   - Controller violates force limits
   - Controller times out (if latency monitoring enabled)
2. Verify simulation runner's response:
   - Does it catch exceptions?
   - Does it truncate output safely?
   - Does it cleanup resources?
3. Check error messages clarity

**Validation**:
```python
# Create failing controller test
class FailingController:
    """Test controller that fails in various ways."""
    def initialize_state(self):
        return {}
    def initialize_history(self):
        return {}
    def compute_control(self, state, state_vars, history):
        if state[1] > 0.5:  # Fail when angle exceeds threshold
            raise RuntimeError("Controller instability detected")
        return 0.0

from src.simulation.engines.simulation_runner import run_simulation
from src.plant.models.dip_lowrank import DIPDynamics
import numpy as np

try:
    t, x, u = run_simulation(
        controller=FailingController(),
        dynamics_model=DIPDynamics(),
        sim_time=5.0,
        dt=0.01,
        initial_state=np.array([0.0, 0.6, 0.1, 0.0, 0.0, 0.0])  # Will trigger failure
    )
    print(f"Simulation completed {len(t)} steps before failure")
except Exception as e:
    print(f"Exception caught: {e}")
```

**Deliverable**: Controller failure handling report

### Task 3.2: Dynamics Failure Scenarios (30 min)
**Goal**: Verify controller handles dynamics failures gracefully

**Actions**:
1. Test scenarios:
   - Dynamics returns NaN/Inf
   - Dynamics raises exception
   - Dynamics module missing (full dynamics unavailable)
2. Verify simulation runner's response
3. Check if controllers are notified of failures

**Validation**:
```python
# Test dynamics failure handling
class FailingDynamics:
    """Test dynamics that fail."""
    def step(self, x, u, dt):
        if abs(u) > 100:  # Fail on excessive control
            return np.array([np.nan] * 6)
        # Normal dynamics
        return x + dt * np.random.randn(6) * 0.01

from src.controllers.factory.smc_factory import create_controller
controller = create_controller('classical_smc', gains=[10.0]*6)

try:
    t, x, u = run_simulation(
        controller=controller,
        dynamics_model=FailingDynamics(),
        sim_time=5.0,
        dt=0.01,
        initial_state=np.array([0.0, 0.1, 0.1, 0.0, 0.0, 0.0])
    )
    print(f"Handled dynamics failure: {len(t)} steps completed")
    assert np.all(np.isfinite(x[:len(t)])), "Should only return finite states"
except Exception as e:
    print(f"Exception: {e}")
```

**Deliverable**: Dynamics failure handling report

### Task 3.3: Cross-Boundary Error Propagation (30 min)
**Goal**: Verify errors propagate correctly across integration boundaries

**Actions**:
1. Map error propagation paths:
   - Factory → Controller → Simulation
   - PSO → Factory → Simulation
   - Simulation → Controller (via callbacks)
2. Verify error messages preserved (not swallowed)
3. Check cleanup performed on all error paths
4. Document error handling gaps

**Validation**:
```bash
# Run error recovery integration tests
python -m pytest tests/test_integration/test_error_recovery/ -v --tb=short

# Check for memory leaks on error paths
python -m pytest tests/test_integration/test_memory_management/ -v
```

**Deliverable**: Error propagation analysis with recommendations

---

## Phase 4: Integration Testing (2 hours)

### Task 4.1: Review Existing Integration Tests (30 min)
**Goal**: Assess current integration test coverage

**Actions**:
1. Inventory all integration tests:
   ```bash
   find tests/test_integration/ -name "*.py" | xargs wc -l
   ```
2. Categorize tests by integration aspect:
   - End-to-end (full pipeline)
   - Error recovery
   - Memory management
   - Numerical stability
   - Thread safety
   - Production readiness
3. Identify test coverage gaps
4. Document test execution times

**Validation**:
```bash
# Run all integration tests with coverage
python -m pytest tests/test_integration/ -v --durations=20

# Generate coverage report for integration modules
python -m pytest tests/test_integration/ --cov=src.controllers.factory --cov=src.simulation.engines --cov-report=html
```

**Deliverable**: Integration test coverage report

### Task 4.2: Execute Critical Path Tests (45 min)
**Goal**: Verify all controller types work with both dynamics models

**Actions**:
1. Create test matrix:
   ```
   4 controllers × 2 dynamics × 3 scenarios = 24 tests
   Controllers: Classical, Adaptive, STA, Hybrid
   Dynamics: Low-rank, Full
   Scenarios: Stabilization, Disturbance, Large initial error
   ```
2. Execute each combination
3. Collect performance metrics:
   - Simulation time
   - Control effort
   - Stabilization time
   - Peak errors
4. Document failures or anomalies

**Validation**:
```python
# Create comprehensive test matrix script
# File: integration_test_matrix.py
from src.controllers.factory.smc_factory import create_controller, SMCType
from src.simulation.engines.simulation_runner import run_simulation
from src.plant.models.dip_lowrank import DIPDynamics as LowRank
from src.plant.models.dip_full import DIPDynamics as FullDynamics
import numpy as np
import pandas as pd
from itertools import product

def run_test_matrix():
    results = []

    controllers = [ct.value for ct in SMCType]
    dynamics_models = [
        ('lowrank', LowRank()),
        ('full', FullDynamics()) if module_exists('src.plant.models.dip_full') else None
    ]
    dynamics_models = [dm for dm in dynamics_models if dm is not None]

    scenarios = [
        ('stabilization', np.array([0.0, 0.1, 0.1, 0.0, 0.0, 0.0])),
        ('disturbance', np.array([0.2, 0.2, 0.2, 0.1, 0.1, 0.1])),
        ('large_error', np.array([0.5, 0.5, 0.5, 0.0, 0.0, 0.0]))
    ]

    for ctrl_name, (dyn_name, dynamics), (scenario_name, initial_state) in product(
        controllers, dynamics_models, scenarios
    ):
        try:
            controller = create_controller(ctrl_name, gains=[10.0, 5.0, 8.0, 3.0, 15.0, 2.0])
            t, x, u = run_simulation(
                controller=controller,
                dynamics_model=dynamics,
                sim_time=5.0,
                dt=0.01,
                initial_state=initial_state
            )

            results.append({
                'controller': ctrl_name,
                'dynamics': dyn_name,
                'scenario': scenario_name,
                'status': 'PASS',
                'steps': len(t),
                'final_error': np.linalg.norm(x[-1]),
                'control_effort': np.sqrt(np.mean(u**2))
            })
        except Exception as e:
            results.append({
                'controller': ctrl_name,
                'dynamics': dyn_name,
                'scenario': scenario_name,
                'status': 'FAIL',
                'error': str(e)
            })

    return pd.DataFrame(results)

def module_exists(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

if __name__ == '__main__':
    df = run_test_matrix()
    print(df.to_string())
    df.to_csv('integration_test_matrix_results.csv', index=False)
```

**Deliverable**: Test matrix results with pass/fail analysis

### Task 4.3: Identify Missing Test Scenarios (45 min)
**Goal**: Find integration scenarios not covered by existing tests

**Actions**:
1. Review interface contract from Phase 1
2. Check if all interface methods tested
3. Identify edge cases not covered:
   - Zero gains
   - Negative gains
   - Extremely large gains
   - Empty history/state_vars
   - State vector with NaN elements
4. Write test plan for gaps
5. Estimate implementation effort

**Validation**:
Create test plan document with:
- Scenario description
- Expected behavior
- Current test status (covered/not covered)
- Priority (P0/P1/P2)
- Estimated effort (hours)

**Deliverable**: Gap analysis report with prioritized test plan

---

## Phase 5: Performance Validation (1 hour)

### Task 5.1: Measure Integration Overhead (30 min)
**Goal**: Quantify performance cost of integration layer

**Actions**:
1. Benchmark direct controller calls vs simulation runner calls
2. Measure PSO wrapper overhead
3. Profile hot paths:
   ```bash
   python -m cProfile -o profile.stats simulate.py --ctrl classical_smc --sim-time 10.0
   python -m pstats profile.stats
   ```
4. Identify bottlenecks at integration boundaries

**Validation**:
```python
# Benchmark integration overhead
import time
import numpy as np
from src.controllers.factory.smc_factory import create_controller
from src.simulation.engines.simulation_runner import run_simulation
from src.plant.models.dip_lowrank import DIPDynamics

def benchmark_overhead():
    controller = create_controller('classical_smc', gains=[10.0]*6)
    dynamics = DIPDynamics()
    state = np.array([0.0, 0.1, 0.1, 0.0, 0.0, 0.0])

    # Direct controller benchmark
    state_vars = controller.initialize_state()
    history = controller.initialize_history()

    start = time.perf_counter()
    for _ in range(10000):
        u = controller.compute_control(state, state_vars, history)
    direct_time = time.perf_counter() - start

    # Simulation runner benchmark
    start = time.perf_counter()
    t, x, u = run_simulation(
        controller=controller,
        dynamics_model=dynamics,
        sim_time=1.0,
        dt=0.01,
        initial_state=state
    )
    simulation_time = time.perf_counter() - start

    print(f"Direct calls (10k): {direct_time*1000:.2f} ms")
    print(f"Simulation (100 steps): {simulation_time*1000:.2f} ms")
    print(f"Overhead per step: {(simulation_time/100 - direct_time/10000)*1000:.3f} ms")

benchmark_overhead()
```

**Deliverable**: Performance overhead analysis report

### Task 5.2: Memory Leak Detection (30 min)
**Goal**: Verify no memory leaks across integration boundary

**Actions**:
1. Run long simulations with memory monitoring
2. Test all controller types
3. Check for growth in:
   - Controller state size
   - History dictionary size
   - Dynamics model state
4. Verify cleanup on simulation end

**Validation**:
```bash
# Run memory leak tests
python -m pytest tests/test_integration/test_memory_management/test_memory_resource_deep.py -v

# Profile memory usage
python -m memory_profiler simulate.py --ctrl classical_smc --sim-time 100.0
```

**Deliverable**: Memory leak analysis report

---

## Final Deliverables Checklist

### 1. Interface Contract Document
- [ ] Controller factory interface signatures
- [ ] Simulation runner interface requirements
- [ ] Data contract specification (shapes, types, ranges)
- [ ] PSO wrapper interface documentation

### 2. Data Flow Diagram
- [ ] ASCII or Mermaid diagram showing full flow
- [ ] Annotations for data transformations
- [ ] PSO integration flow included
- [ ] Error propagation paths marked

### 3. Error Handling Report
- [ ] Controller failure scenarios tested
- [ ] Dynamics failure scenarios tested
- [ ] Error propagation paths verified
- [ ] Identified gaps with recommendations

### 4. Integration Test Plan
- [ ] Current test coverage assessment
- [ ] Test matrix results (24+ combinations)
- [ ] Gap analysis with priorities
- [ ] Implementation effort estimates

### 5. Performance Validation Results
- [ ] Integration overhead measurements
- [ ] Memory leak analysis
- [ ] Bottleneck identification
- [ ] Recommendations for optimization

### 6. Integration Quality Scorecard
- [ ] Interface completeness score (0-100)
- [ ] Error handling score (0-100)
- [ ] Test coverage score (0-100)
- [ ] Performance score (0-100)
- [ ] Overall integration quality (0-100)
- [ ] Production readiness assessment

---

## Success Criteria

- [x] Target components identified: Controller Factory ↔ Simulation Runner
- [ ] All interaction points documented (factory, PSO, simulation)
- [ ] Data flow traced for all 4 controller types
- [ ] Error handling verified (controller failures, dynamics failures)
- [ ] Integration tests executed (24+ test matrix combinations)
- [ ] Performance validated (overhead < 1ms/step, no memory leaks)
- [ ] Test plan covers all identified gaps
- [ ] Can answer: "Is this integration production-ready?"

---

## Execution Timeline

**Total**: 7 hours

| Phase | Duration | Tasks | Key Output |
|-------|----------|-------|------------|
| 1. Interface Discovery | 1h | 3 tasks | Interface contract |
| 2. Data Flow Analysis | 1.5h | 3 tasks | Flow diagram |
| 3. Error Handling | 1.5h | 3 tasks | Error handling report |
| 4. Integration Testing | 2h | 3 tasks | Test plan + results |
| 5. Performance | 1h | 2 tasks | Performance report |

---

## Next Steps After Audit

1. **Immediate Actions** (P0 issues from audit)
2. **Short-term Improvements** (P1 issues, < 1 week)
3. **Long-term Enhancements** (P2 issues, roadmap)
4. **Documentation Updates** (based on findings)
5. **Test Implementation** (fill identified gaps)

---

## Automation Scripts to Create

1. `validate_data_contract.py` - Runtime type/shape validation
2. `trace_data_flow.py` - Data flow logger with visualization
3. `integration_test_matrix.py` - Comprehensive test matrix runner
4. `benchmark_integration.py` - Performance overhead measurement
5. `check_memory_leaks.py` - Memory growth detector

---

## References

**Source Code**:
- `src/controllers/factory/smc_factory.py` - Controller creation
- `src/controllers/factory/pso_integration.py` - PSO wrapper
- `src/simulation/engines/simulation_runner.py` - Simulation engine

**Tests**:
- `tests/test_integration/test_end_to_end/` - E2E validation
- `tests/test_integration/test_error_recovery/` - Error handling
- `tests/test_integration/test_memory_management/` - Memory validation

**Documentation**:
- `.project/ai/config/controller_memory.md` - Memory management
- `.project/ai/config/testing_standards.md` - Test requirements
- `docs/guides/how-to/testing-validation.md` - Testing guide

---

**[READY TO EXECUTE]** - All prerequisites identified, plan validated, ready for systematic execution.
