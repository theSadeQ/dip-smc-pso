---
description: Analyze PSO optimization convergence logs
tags: [pso, optimization, convergence, analysis]
---

# PSO Convergence Analysis

I'll analyze your PSO optimization logs to diagnose convergence issues and identify optimal parameters.

## What I'll do:

1. **Parse PSO Log File**
   - Extract iteration numbers
   - Read global best fitness per iteration
   - Identify particle positions
   - Track swarm diversity

2. **Convergence Analysis**
   - Plot fitness vs iteration
   - Detect premature convergence
   - Identify stuck particles
   - Calculate convergence rate
   - Measure final improvement

3. **Identify Issues**
   - Stagnation patterns (fitness plateau)
   - Swarm diversity collapse
   - Parameter bound violations
   - Cost function failures
   - Numerical instabilities

4. **Generate Recommendations**
   - Adjust swarm size (current vs recommended)
   - Modify iteration count
   - Update PSO parameters (w, c1, c2)
   - Revise parameter bounds
   - Suggest alternative cost functions

5. **Create Report**
   - Convergence plot description
   - Issue summary with severity
   - Parameter recommendations
   - Next steps for optimization

## Please provide:

1. **Log file path** (e.g., `pso_lyapunov_run.log`, `logs/pso_classical_smc.log`)
2. **Controller type** (e.g., "classical_smc", "adaptive_smc", "sta_smc")
3. **Expected behavior** (optional: "should converge below 5.0", "oscillating around 8.2")

## Examples:

```bash
# Analyze recent PSO run
/analyze-pso-logs pso_lyapunov_run_v2.log sta_smc

# Analyze with expected outcome
/analyze-pso-logs logs/pso_optimization.log classical_smc "expect ISE < 5.0"

# Quick convergence check
/analyze-pso-logs pso_*.log
```

## What I'll check:

### Convergence Criteria
- ✅ **Good**: Steady fitness improvement, final plateau
- ⚠️ **Warning**: Slow convergence, high variance
- ❌ **Problem**: No improvement, premature stagnation

### Common Issues
- **Premature Convergence**: All particles clustered, no diversity
- **Slow Convergence**: Iterations >> 100 without improvement
- **Oscillation**: Fitness fluctuating without settling
- **Divergence**: Fitness increasing over time

### Output Format
```
PSO Convergence Analysis Report
================================
File: pso_lyapunov_run_v2.log
Controller: STA SMC
Iterations: 50
Final Fitness: 8.2431

Convergence: ⚠️ SLOW (50% improvement in 50 iterations)
Issue: Swarm diversity collapsed at iteration 22
Recommendation: Increase swarm_size from 30 to 50

Next Steps:
1. Run PSO with swarm_size=50, iterations=100
2. Consider relaxing gain bounds (current may be too restrictive)
3. Test alternative cost function (ISE + control effort)
```

## Integration with MCP Servers

This command uses:
- **Filesystem Server**: Read log files, parse PSO output
- **Sequential Thinking**: Systematic convergence diagnosis
- **GitHub Server** (optional): Search for similar convergence issues in issue tracker
