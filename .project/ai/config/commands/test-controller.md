---
description: Run comprehensive controller test suite
tags: [testing, controllers, pytest, validation]
---

# Controller Test Suite Runner

I'll run comprehensive tests for a specific controller type with coverage analysis and validation.

## What I'll do:

1. **Execute pytest Suite**
   - Run tests for specified controller
   - Capture test output and failures
   - Generate coverage report
   - Track test execution time

2. **Analyze Results**
   - Count passed/failed/skipped tests
   - Identify failing test patterns
   - Review error messages
   - Check coverage percentage

3. **Property-Based Testing** (if applicable)
   - Run Hypothesis tests
   - Verify control-theoretic properties
   - Test boundary conditions
   - Validate numerical stability

4. **Generate Report**
   - Test summary (X/Y passed)
   - Coverage metrics (line/branch)
   - Failed test details
   - Recommendations for fixes

5. **Integration Tests** (optional)
   - End-to-end simulation tests
   - PSO integration tests
   - Factory instantiation tests

## Please provide:

1. **Controller type** (e.g., "classical_smc", "adaptive_smc", "mpc", "all")
2. **Test scope** (optional: "unit", "integration", "property", "all")
3. **Coverage target** (optional: "95%", default: show actual)

## Examples:

```bash
# Test specific controller
/test-controller classical_smc

# Test with coverage
/test-controller adaptive_smc --coverage

# Test all controllers
/test-controller all

# Integration tests only
/test-controller hybrid_adaptive_sta_smc integration

# Property-based tests
/test-controller sta_smc property
```

## Test Categories

### Unit Tests
```python
tests/test_controllers/smc/algorithms/classical/
tests/test_controllers/smc/algorithms/adaptive/
tests/test_controllers/smc/algorithms/sta/
tests/test_controllers/smc/algorithms/hybrid/
tests/test_controllers/mpc/
```

### Integration Tests
```python
tests/test_integration/test_controller_pso.py
tests/test_integration/test_controller_simulation.py
tests/test_integration/test_factory_controller.py
```

### Property-Based Tests
```python
tests/test_validation/test_control_properties.py
tests/test_validation/test_lyapunov_properties.py
tests/test_validation/test_numerical_stability.py
```

## Command Mapping

| Command | pytest Invocation |
|---------|-------------------|
| `classical_smc` | `pytest tests/test_controllers/smc/algorithms/classical/ -v` |
| `adaptive_smc` | `pytest tests/test_controllers/smc/algorithms/adaptive/ -v` |
| `sta_smc` | `pytest tests/test_controllers/smc/algorithms/sta/ -v` |
| `hybrid_adaptive_sta_smc` | `pytest tests/test_controllers/smc/algorithms/hybrid/ -v` |
| `mpc` | `pytest tests/test_controllers/mpc/ -v` |
| `all` | `pytest tests/test_controllers/ -v` |

## Output Format

```
Controller Test Report: Classical SMC
======================================
Test Scope: Unit + Integration
Execution Time: 12.3s

Results:
  Passed:  45/48 (93.8%)
  Failed:   2/48 (4.2%)
  Skipped:  1/48 (2.1%)

Coverage:
  Line Coverage: 94.2% (target: 95%)
  Branch Coverage: 89.1%

Failed Tests:
  1. test_classical_smc_boundary_layer_edge_case
     Error: AssertionError: boundary_layer=0 should raise ValueError
     Location: tests/test_controllers/smc/algorithms/classical/test_boundary_layer.py:45

  2. test_classical_smc_max_force_saturation
     Error: Control output exceeded max_force (101.2 > 100.0)
     Location: tests/test_controllers/smc/algorithms/classical/test_saturation.py:67

Recommendations:
  1. Fix boundary_layer=0 validation (add ValueError in __init__)
  2. Review saturation logic in compute_control() method
  3. Increase coverage by testing edge cases (0.8% to target)

Next Steps:
  1. Run: pytest tests/.../test_boundary_layer.py::test_classical_smc_boundary_layer_edge_case -vv
  2. Review: src/controllers/smc/algorithms/classical.py:123-145
  3. Fix and re-run test suite
```

## Integration with MCP Servers

This command uses:
- **Filesystem Server**: Read test files, analyze code coverage
- **Sequential Thinking**: Systematic test failure diagnosis
- **GitHub Server** (optional): Check if test failures match known issues
