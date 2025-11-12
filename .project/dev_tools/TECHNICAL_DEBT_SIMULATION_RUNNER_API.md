# Technical Debt: SimulationRunner API Mismatch

**Date**: 2025-11-12
**Status**: BLOCKED - Requires architectural decision
**Priority**: HIGH - Blocks baseline benchmark generation

## Problem Statement

Test files and tutorials use a non-existent `SimulationRunner` API, causing all integration tests and tutorials to fail.

## Current State

### Expected API (Used in Tests/Tutorials)
```python
runner = SimulationRunner(controller, dynamics, config)
result = runner.run()
```

### Actual API (Implemented in src/simulation/engines/simulation_runner.py)
```python
runner = SimulationRunner(dynamics_model, dt=0.01, max_time=10.0)
result = runner.run_simulation(initial_state, controller=controller)
```

## Root Cause

The `SimulationRunner` class was written as a wrapper around the functional `run_simulation()` API but:
1. ❌ Has NO `.run()` method - only `.run_simulation()` exists
2. ❌ `__init__` signature doesn't match usage: expects `(dynamics_model, dt, max_time)` not `(controller, dynamics, config)`

## Files Affected

1. **Tests**:
   - `tests/test_integration/test_cross_component.py` - Lines 380, 382, 490

2. **Tutorials**:
   - `scripts/tutorials/tutorial_06_robustness.py` - Lines 123, 292
   - `scripts/tutorials/tutorial_07_multi_objective.py` - Lines 119, 233

3. **Working Reference**:
   - `simulate.py` - Uses functional `run_simulation()` directly (WORKS)

## Fixes Already Applied (Commit c1bd6b72)

✅ Fixed controller factory to pass gains explicitly
✅ Fixed DIPDynamics to use `config.physics` subsection
✅ Fixed SimulationRunner calls to use positional arguments

❌ BLOCKED: Cannot fix `.run()` vs `.run_simulation()` without architectural decision

## Proposed Solutions

### Option A: Add Compatibility Method (Quick Fix - 15 min)
Add `.run()` method alias to `SimulationRunner` class:

```python
# In src/simulation/engines/simulation_runner.py
class SimulationRunner:
    def __init__(self, controller_or_dynamics, dynamics=None, config=None):
        if dynamics is None:
            # Old API: SimulationRunner(dynamics_model, dt, max_time)
            self.dynamics_model = controller_or_dynamics
            self.dt = 0.01
            self.max_time = 10.0
        else:
            # New API: SimulationRunner(controller, dynamics, config)
            self.controller = controller_or_dynamics
            self.dynamics_model = dynamics
            self.config = config
            self.dt = config.simulation.dt if config else 0.01
            self.max_time = config.simulation.duration if config else 10.0

    def run(self, **kwargs):
        """Alias for run_simulation() for backward compatibility."""
        initial_state = kwargs.pop('initial_state', self.config.simulation.initial_state if hasattr(self, 'config') else None)
        controller = kwargs.pop('controller', getattr(self, 'controller', None))
        return self.run_simulation(initial_state, controller=controller, **kwargs)
```

**Pros**: Quick, maintains backward compatibility
**Cons**: Messy dual-API, technical debt

### Option B: Update Tests/Tutorials to Use Correct API (Clean Fix - 30 min)
Update all test/tutorial calls to use functional `run_simulation()` like `simulate.py`:

```python
from src.core.simulation_runner import run_simulation

# Replace:
runner = SimulationRunner(controller, dynamics, config)
result = runner.run()

# With:
t_arr, x_arr, u_arr = run_simulation(
    controller=controller,
    dynamics_model=dynamics,
    sim_time=config.simulation.duration,
    dt=config.simulation.dt,
    initial_state=config.simulation.initial_state
)
result = {'time': t_arr, 'states': x_arr, 'controls': u_arr}
```

**Pros**: Clean, uses official API, matches simulate.py
**Cons**: More changes required (8 locations)

### Option C: Create New Wrapper Class (Architectural Fix - 1 hour)
Create `TestSimulationRunner` with expected API in `tests/conftest.py`:

```python
# In tests/conftest.py
class TestSimulationRunner:
    """Test-friendly wrapper around run_simulation()."""
    def __init__(self, controller, dynamics, config):
        self.controller = controller
        self.dynamics = dynamics
        self.config = config

    def run(self):
        from src.core.simulation_runner import run_simulation
        t_arr, x_arr, u_arr = run_simulation(
            controller=self.controller,
            dynamics_model=self.dynamics,
            sim_time=self.config.simulation.duration,
            dt=self.config.simulation.dt,
            initial_state=self.config.simulation.initial_state
        )
        return {'time': t_arr, 'states': x_arr, 'controls': u_arr}
```

**Pros**: Isolated to tests, doesn't pollute production code
**Cons**: Doesn't fix tutorials, requires import changes

## Recommendation

**Option B (Update to Functional API)** is recommended because:
1. Matches working reference implementation (simulate.py)
2. No technical debt or dual-API maintenance
3. Clean, explicit, and documented
4. Fixes both tests AND tutorials permanently

## Implementation Checklist

- [ ] Choose solution approach (A, B, or C)
- [ ] Update 8 locations (3 test + 4 tutorial + 1 benchmark generation)
- [ ] Verify all tests pass
- [ ] Run tutorial scripts end-to-end
- [ ] Update factory migration guide with SimulationRunner patterns
- [ ] Re-enable baseline benchmark generation

## Impact Assessment

**Blocked Functionality**:
- ❌ Integration tests (test_cross_component.py)
- ❌ Tutorial execution (tutorial_06, tutorial_07)
- ❌ Baseline benchmark generation (required for regression detection)

**Working Functionality**:
- ✅ simulate.py CLI (uses functional API)
- ✅ Unit tests (don't use SimulationRunner class)
- ✅ Controller factory (fixed in c1bd6b72)
- ✅ DIPDynamics initialization (fixed in c1bd6b72)

## References

- Working implementation: `simulate.py:739-740` (functional `run_simulation()`)
- Actual class: `src/simulation/engines/simulation_runner.py:367-466`
- Broken tests: `tests/test_integration/test_cross_component.py:380,382,490`
- Broken tutorials: `scripts/tutorials/tutorial_{06,07}_*.py`

---

**Next Steps**: Review options and decide on approach before proceeding with baseline benchmark generation.
