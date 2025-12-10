# PSO Algorithmic Efficiency Analysis

## Current Performance Bottlenecks (Ranked by Impact)

### 1. Sequential Particle Evaluation [FIXED] ✓
**Impact**: 10-20x slowdown
**Status**: FIXED with parallel evaluation
**Speedup**: 10-20x (hardware-dependent)

---

### 2. Full 10-Second Simulations (NO Early Termination)
**Impact**: 2-5x slowdown
**Current**: Every simulation runs full 10 seconds (1000 timesteps)
**Problem**: Unstable controllers diverge at t=2s, but we simulate until t=10s anyway

**Solution**: Early termination for unstable trajectories
```python
# Current: Always 1000 timesteps
for t in range(1000):
    x = step(x, u, dt)

# Optimized: Stop if diverged
for t in range(1000):
    x = step(x, u, dt)
    if np.linalg.norm(x) > 10:  # Clearly unstable
        return LARGE_COST  # Don't waste 8 more seconds
```

**Expected Speedup**: 2-3x (most bad particles diverge early)
**Implementation**: Add early stopping to RobustCostEvaluator
**Risk**: Low (unstable = high cost anyway)

---

### 3. Fixed 5 Scenarios Per Particle (No Adaptive Sampling)
**Impact**: 2x slowdown
**Current**: All particles evaluated with 5 scenarios
**Problem**: Early iterations don't need 5 scenarios (particles are random anyway)

**Solution**: Adaptive scenario count
```python
# Early iterations (0-50): 3 scenarios (fast exploration)
# Mid iterations (50-100): 4 scenarios (refining)
# Late iterations (100+): 5 scenarios (high precision)
```

**Expected Speedup**: 1.5-2x average
**Implementation**: Pass `iteration` to cost evaluator, adjust n_scenarios
**Risk**: Low (convergence might need 10 more iterations, but still net win)

---

### 4. PSO vs Better Algorithms
**Impact**: 2-10x slowdown (iteration count)
**Current**: PSO needs 150-200 iterations to converge
**Problem**: PSO is gradient-free, doesn't exploit structure

**Better Algorithms**:

| Algorithm | Iterations Needed | Speedup | Difficulty |
|-----------|------------------|---------|------------|
| **CMA-ES** | 80-100 | 1.5-2x | Easy (drop-in replacement) |
| **Bayesian Optimization** | 50-80 | 2-3x | Medium (needs surrogate model) |
| **BFGS (gradient)** | 20-40 | 4-5x | Hard (needs gradients via adjoint) |
| **Trust Region** | 30-50 | 3-4x | Hard (needs Hessian approximation) |

**Recommendation**: Try CMA-ES first (easy, 1.5-2x speedup)

```python
# Replace PySwarms with CMA-ES
import cma
es = cma.CMAEvolutionStrategy(x0, 0.5, {
    'popsize': 25,
    'maxiter': 100
})
```

**Expected Speedup**: 1.5-2x (fewer iterations)
**Implementation**: Replace PSO loop with CMA-ES
**Risk**: Medium (different convergence behavior)

---

### 5. Simulation Time: 10 Seconds Too Long?
**Impact**: 2x slowdown
**Current**: 10-second simulation (1000 timesteps at dt=0.01)
**Problem**: Most controllers stabilize by t=5s

**Solution**: Reduce to 5 seconds
```yaml
# config.yaml
simulation:
  duration: 5.0  # Was 10.0
```

**Expected Speedup**: 2x (half the timesteps)
**Implementation**: One-line config change
**Risk**: Medium (some controllers might need >5s to stabilize)

**Validation**: Plot convergence times first
```python
python scripts/analyze_convergence_time.py  # Check if 5s is enough
```

---

### 6. dt=0.01 Too Small (Over-Integration)
**Impact**: 2-5x slowdown
**Current**: dt=0.01 (1000 steps for 10 seconds)
**Problem**: Most dynamics are smooth, don't need such fine resolution

**Solution**: Adaptive dt or coarser timestep
```yaml
# config.yaml
simulation:
  dt: 0.02  # Was 0.01 (50% fewer steps)
  # OR
  dt: 0.05  # 80% fewer steps (risky for stiff dynamics)
```

**Expected Speedup**: 2x (dt=0.02) or 5x (dt=0.05)
**Implementation**: One-line config change
**Risk**: High (numerical stability, accuracy loss)

**Validation**: Compare trajectories before/after
```python
# Ensure dt=0.02 doesn't change results significantly
python scripts/validate_dt_sensitivity.py
```

---

### 7. Cost Function Overhead (Unnecessary Computation)
**Impact**: 1.2-1.5x slowdown
**Current**: Compute full cost metrics (position, velocity, control, sliding)
**Problem**: Some metrics redundant or dominated by others

**Solution**: Profile cost function, remove expensive redundant terms
```python
# Example: If position error dominates, skip control effort calculation
if position_error > 100:  # Already failed
    return position_error * 1000  # Don't compute other terms
```

**Expected Speedup**: 1.2-1.5x
**Implementation**: Profile with cProfile, optimize hot loops
**Risk**: Low (preserves cost ordering)

---

## Cumulative Speedup Potential

| Optimization | Speedup | Difficulty | Risk |
|--------------|---------|------------|------|
| 1. Parallel (DONE) | 10x | Easy | Low |
| 2. Early termination | 2-3x | Easy | Low |
| 3. Adaptive scenarios | 1.5x | Medium | Low |
| 4. CMA-ES | 1.5x | Easy | Medium |
| 5. Reduce sim time (10s→5s) | 2x | Trivial | Medium |
| 6. Increase dt (0.01→0.02) | 2x | Trivial | High |
| 7. Cost function optimization | 1.3x | Hard | Low |

**Total Combined** (if all work): 10 × 3 × 1.5 × 1.5 × 2 × 2 × 1.3 = **175x faster!**

**Realistic Stack** (low-risk only):
- Parallel (DONE): 10x
- Early termination: 2.5x
- Reduce sim time: 2x
- **Total: 10 × 2.5 × 2 = 50x faster than original**

---

## Recommended Next Steps (Priority Order)

### Immediate (30 minutes)
1. **Early termination**: Add `if norm(x) > 10: break` to simulation loop
2. **Reduce sim time**: Change `duration: 10.0` → `5.0` in config

**Expected**: 15 hours → **3 hours** (5x additional speedup on top of parallel)

### Short-term (2-4 hours)
3. **CMA-ES**: Replace PSO with CMA-ES (fewer iterations)
4. **Adaptive scenarios**: Reduce scenarios early, increase late

**Expected**: 3 hours → **1 hour** (3x additional speedup)

### Medium-term (1-2 days)
5. **Profile simulation**: Find exact bottleneck in timestep loop
6. **Validate dt increase**: Test if dt=0.02 maintains accuracy

**Expected**: 1 hour → **20-30 minutes** (2x additional speedup)

### Long-term (1-2 weeks)
7. **Bayesian Optimization**: Use GP surrogate model (50-80 evals vs 150-200)
8. **GPU acceleration**: Port simulation to CUDA (10-100x faster)

**Expected**: 20-30 min → **5-10 minutes** (3-5x additional speedup)

---

## Bottom Line

**Current** (with parallel): ~6 hours (10x faster than 15 hours original)

**With quick fixes (1-2)**: ~1.5-2 hours (5x faster than parallel alone)

**With full optimization (1-6)**: ~20-30 minutes (15-20x faster than parallel alone)

**Ultimate (1-8, GPU)**: ~5 minutes (200x faster than original)

---

## Verification

Before implementing, verify these hypotheses:

```bash
# 1. Check if simulations actually need 10 seconds
python scripts/analyze_convergence_time.py

# 2. Profile cost function
python -m cProfile -o pso_profile.prof scripts/phase2_bulletproof_pso_v2.py --iterations 5
python -c "import pstats; p = pstats.Stats('pso_profile.prof'); p.sort_stats('cumtime'); p.print_stats(20)"

# 3. Test dt sensitivity
python scripts/test_dt_sensitivity.py  # dt=0.01 vs 0.02 vs 0.05
```

**These 3 commands will reveal the EXACT bottlenecks on your system.**

---

**Created**: December 10, 2025
**Author**: Claude Code
**Status**: Analysis complete, awaiting implementation decisions
