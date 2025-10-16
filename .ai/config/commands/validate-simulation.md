---
description: Validate simulation results against control-theoretic criteria
tags: [validation, simulation, lyapunov, stability]
---

# Simulation Result Validation

I'll validate your simulation results against control-theoretic criteria, stability guarantees, and performance metrics.

## What I'll do:

1. **Load Simulation Data**
   - Read simulation output (JSON, CSV, or log file)
   - Extract state trajectory (x, θ₁, θ₂, velocities)
   - Extract control input trajectory
   - Parse configuration parameters

2. **Stability Analysis**
   - Verify Lyapunov function decreases monotonically
   - Check state convergence to equilibrium
   - Identify divergence or instability
   - Calculate settling time (±5% threshold)

3. **Performance Metrics**
   - Compute ISE (Integral Squared Error)
   - Compute ITAE (Integral Time-Absolute Error)
   - Calculate maximum overshoot
   - Measure control effort
   - Check chattering magnitude

4. **Control-Theoretic Validation**
   - Verify sliding surface convergence (SMC)
   - Check constraint satisfaction (MPC)
   - Validate adaptation rates (Adaptive SMC)
   - Verify boundary layer effectiveness

5. **Physical Feasibility**
   - Check state bounds (|θ₁| < π, |θ₂| < π)
   - Verify control saturation (|u| ≤ max_force)
   - Validate velocity limits
   - Detect numerical instabilities (NaN, Inf)

6. **Generate Report**
   - Pass/Fail verdict with justification
   - Performance metric summary
   - Stability analysis results
   - Recommendations for improvement

## Please provide:

1. **Simulation output path** (e.g., `results/sim_output.json`, `logs/simulation_20251006.csv`)
2. **Controller type** (e.g., "classical_smc", "mpc", "hybrid")
3. **Acceptance criteria** (optional: "ISE < 5.0", "settling_time < 3.0s")

## Examples:

```bash
# Validate recent simulation
/validate-simulation results/sim_classical_smc.json classical_smc

# Validate with criteria
/validate-simulation results/sim_output.json sta_smc "ISE < 10.0, settling_time < 2.5"

# Validate MPC simulation
/validate-simulation logs/mpc_sim_20251006.csv mpc

# Quick stability check
/validate-simulation *.json
```

## Validation Criteria

### Stability (Critical)
- ✅ **Pass**: All states converge to equilibrium
- ⚠️ **Warning**: Slow convergence (t > 5.0s)
- ❌ **Fail**: Divergence or oscillation without settling

### Performance (High Priority)
- ✅ **Pass**: ISE < threshold, overshoot < 10%
- ⚠️ **Warning**: Marginally acceptable performance
- ❌ **Fail**: Poor tracking, excessive overshoot

### Constraints (Critical)
- ✅ **Pass**: All constraints satisfied
- ⚠️ **Warning**: Occasional boundary violations
- ❌ **Fail**: Persistent constraint violations

### Numerical Robustness (High Priority)
- ✅ **Pass**: No NaN/Inf, condition numbers healthy
- ⚠️ **Warning**: High condition numbers (> 1e10)
- ❌ **Fail**: NaN/Inf detected, numerical failure

## Output Format

```
Simulation Validation Report
=============================
File: results/sim_classical_smc_20251006.json
Controller: Classical SMC
Duration: 5.0s (dt=0.01, 500 steps)

VERDICT: ✅ PASS

Stability Analysis:
  State Convergence: ✅ PASS (all states → 0)
  Lyapunov Function: ✅ PASS (monotonically decreasing)
  Settling Time: 2.34s (target: < 3.0s)

Performance Metrics:
  ISE: 4.23 (target: < 5.0) ✅
  ITAE: 6.78 ✅
  Max Overshoot: 8.2% (θ₁) ✅
  Control Effort: 245.3 J

Control-Theoretic Properties:
  Sliding Surface: Converged at t=1.8s ✅
  Chattering: Moderate (boundary_layer=0.01 effective)
  Boundary Layer: Effective (reduces chattering by 67%)

Physical Feasibility:
  State Bounds: ✅ (max |θ₁|=0.15 rad, max |θ₂|=0.22 rad)
  Control Saturation: ✅ (max |u|=85.2 N < 100 N)
  Numerical Stability: ✅ (no NaN/Inf detected)

Recommendations:
  1. ✅ Simulation valid for publication
  2. Consider reducing boundary_layer to 0.005 for smoother control
  3. Performance metrics within acceptable range

Next Steps:
  - Run Monte Carlo validation (100+ trials)
  - Compare against other controller types
  - Generate publication-quality plots
```

## Integration with MCP Servers

This command uses:
- **Filesystem Server**: Read simulation output files
- **Sequential Thinking**: Systematic validation workflow
- **GitHub Server** (optional): Compare against benchmark results in repository
