---
description: Launch PSO optimization workflow with monitoring
tags: [pso, optimization, tuning, workflow]
---

# PSO Controller Optimization Workflow

I'll launch a PSO optimization workflow for controller gain tuning with real-time monitoring and result validation.

## What I'll do:

1. **Pre-Flight Validation**
   - Verify controller type is supported
   - Check PSO configuration validity
   - Validate parameter bounds
   - Confirm dependencies available

2. **PSO Execution**
   - Launch PSO optimization
   - Monitor convergence progress
   - Track iteration logs
   - Detect premature termination

3. **Real-Time Monitoring**
   - Display fitness vs iteration
   - Report global best updates
   - Track swarm diversity
   - Estimate time remaining

4. **Result Validation**
   - Verify gains are within bounds
   - Test optimized gains via simulation
   - Compare against baseline performance
   - Check stability guarantees

5. **Save & Document**
   - Save optimized gains to JSON
   - Generate optimization report
   - Create convergence plots
   - Update configuration (optional)

6. **Post-Optimization Analysis**
   - Run validation simulation
   - Compare ISE improvement
   - Generate recommendation report

## Please provide:

1. **Controller type** (e.g., "classical_smc", "adaptive_smc", "sta_smc", "hybrid_adaptive_sta_smc")
2. **PSO config** (optional: custom swarm_size, iterations, bounds)
3. **Save location** (optional: default `optimized_gains_{controller}_{timestamp}.json`)

## Examples:

```bash
# Optimize with defaults
/optimize-controller classical_smc

# Optimize with custom PSO params
/optimize-controller adaptive_smc --swarm_size 50 --iterations 100

# Optimize and save
/optimize-controller sta_smc --save gains_sta_optimized.json

# Optimize with custom bounds
/optimize-controller classical_smc --bounds "k1:[5,15], k2:[3,10], lambda1:[8,20]"

# Quick optimization (fewer iterations)
/optimize-controller hybrid_adaptive_sta_smc --quick
```

## PSO Configuration Defaults

| Parameter | Default | Description |
|-----------|---------|-------------|
| `swarm_size` | 30 | Number of particles |
| `iterations` | 50 | Maximum iterations |
| `w` | 0.7298 | Inertia weight |
| `c1` | 1.49618 | Cognitive coefficient |
| `c2` | 1.49618 | Social coefficient |

## Controller-Specific Bounds

### Classical SMC
```python
{
  "k1": [5.0, 20.0],      # Position gain (pendulum 1)
  "k2": [3.0, 12.0],      # Velocity gain (pendulum 1)
  "lambda1": [8.0, 25.0], # Position gain (pendulum 2)
  "lambda2": [5.0, 15.0], # Velocity gain (pendulum 2)
  "k_reach": [30.0, 80.0],# Reaching law gain
  "boundary_layer": [0.005, 0.05] # Chattering reduction
}
```

### Adaptive SMC
```python
{
  # Classical SMC gains +
  "gamma1": [0.1, 2.0],   # Adaptation rate 1
  "gamma2": [0.1, 2.0]    # Adaptation rate 2
}
```

### STA SMC
```python
{
  "k1": [5.0, 20.0],
  "k2": [3.0, 12.0],
  "lambda1": [8.0, 25.0],
  "lambda2": [5.0, 15.0],
  "k_sta": [10.0, 40.0],  # Super-twisting gain
  "alpha": [0.3, 0.7]     # Super-twisting exponent
}
```

## Workflow Steps

### 1. Initialization
```
Initializing PSO Optimization
==============================
Controller: Classical SMC
Swarm Size: 30 particles
Iterations: 50 (max)
Parameter Bounds: 6 gains
Cost Function: ISE (Integral Squared Error)
Baseline ISE: 12.45 (default gains)
```

### 2. Progress Monitoring
```
Iteration 10/50: Global Best = 8.23 (33.9% improvement)
Iteration 20/50: Global Best = 6.81 (45.3% improvement)
Iteration 30/50: Global Best = 5.94 (52.3% improvement)
Iteration 40/50: Global Best = 5.87 (52.9% improvement)
Iteration 50/50: Global Best = 5.85 (53.0% improvement) ✅ CONVERGED
```

### 3. Result Validation
```
Optimized Gains Found
=====================
k1: 12.34  (bounds: [5.0, 20.0])
k2: 7.89   (bounds: [3.0, 12.0])
lambda1: 18.56 (bounds: [8.0, 25.0])
lambda2: 9.45  (bounds: [5.0, 15.0])
k_reach: 52.31 (bounds: [30.0, 80.0])
boundary_layer: 0.012 (bounds: [0.005, 0.05])

Validation Simulation:
  ISE: 5.85 (baseline: 12.45) → 53.0% improvement ✅
  Settling Time: 2.1s (baseline: 3.4s) → 38.2% faster ✅
  Stability: Verified (Lyapunov decreasing) ✅

VERDICT: ✅ OPTIMIZATION SUCCESSFUL
```

### 4. Save Results
```
Saved To: optimized_gains_classical_smc_20251006_143022.json
Updated: config.yaml (controllers.classical_smc.gains)

Next Steps:
  1. Test optimized gains: python simulate.py --load optimized_gains_classical_smc_20251006_143022.json
  2. Compare performance: python simulate.py --compare-controllers classical_smc
  3. Commit gains: git add optimized_gains_classical_smc_20251006_143022.json
```

## Error Handling

### Common Issues
- **Swarm Stagnation**: Increase swarm_size or iterations
- **Bound Violations**: Check parameter bounds are reasonable
- **Poor Performance**: Try different cost function or initial conditions
- **Numerical Instability**: Enable numerical stability fixes

### Automatic Recovery
- Retry with increased iterations if no improvement
- Adjust bounds if particles hit boundaries repeatedly
- Switch to alternative cost function if fitness diverges

## Integration with MCP Servers

This command uses:
- **Filesystem Server**: Read config, save optimized gains
- **Sequential Thinking**: Systematic optimization workflow
- **GitHub Server** (optional): Check for previous optimization runs in history
