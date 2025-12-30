# Phase 2 Fix Plan: Adaptive SMC & Hybrid STA Chattering Optimization

**Date**: 2025-12-30
**Goal**: Complete Phase 2 by fixing failed Adaptive/Hybrid optimizations
**Status**: PLANNING
**Estimated Effort**: 4-6 hours

---

## Problem Analysis

### Root Cause (from Phase 2 Results)

**Incorrect Assumption**: Script assumed all controllers had identical `boundary_layer` + `boundary_layer_slope` parameters

**Reality**: Each controller has different chattering reduction mechanisms:
- **Classical SMC**: `boundary_layer` (ε) + `boundary_layer_slope` (α) ✅
- **Adaptive SMC**: `boundary_layer` (ε) + `dead_zone` + adaptive parameters ⚠️
- **Hybrid STA**: `sat_soft_width` + `dead_zone` + damping (NO boundary_layer!) ⚠️

---

## Solution Strategy

### Key Insight

Both Adaptive and Hybrid **ARE optimizable** for chattering, just with **controller-specific parameter sets**!

### Approach

Create **controller-specific PSO optimization scripts** that optimize the correct parameters for each controller type.

---

## Adaptive SMC - Fix Plan

### Optimizable Parameters for Chattering

**Primary Smoothing Parameters** (2D optimization):
1. **boundary_layer** (ε): [0.01, 0.05] - Boundary layer thickness
2. **dead_zone**: [0.0, 0.05] - Radius where adaptation freezes

**Why These Work**:
- `boundary_layer`: Direct chattering reduction (same as Classical SMC)
- `dead_zone`: Prevents adaptive gain oscillations near σ=0

### Controller Signature

```python
AdaptiveSMC(
    gains=[k1, k2, lam1, lam2, gamma],  # From Phase 53 (fixed)
    dt=0.01,                            # Fixed
    max_force=150.0,                    # Fixed
    leak_rate=0.001,                    # Fixed (from config)
    adapt_rate_limit=5.0,               # Fixed (from config)
    K_min=5.0,                          # Fixed
    K_max=50.0,                         # Fixed
    smooth_switch=True,                 # Fixed (use tanh)
    boundary_layer=epsilon,             # OPTIMIZE (2D param 1)
    dead_zone=dead_zone,                # OPTIMIZE (2D param 2)
    K_init=10.0,                        # Fixed
    alpha=0.5                           # Fixed (proportional weight, NOT slope!)
)
```

### PSO Configuration

**Search Space**: 2D (boundary_layer, dead_zone)
- boundary_layer: [0.01, 0.05] (same as Classical SMC)
- dead_zone: [0.0, 0.05] (prevent over-freezing)

**Fitness Function**: 70% chattering + 15% settling + 15% overshoot
**PSO Settings**: 30 particles × 50 iterations × 5 Monte Carlo runs
**Seed**: 42 (reproducibility)

### Implementation Steps

1. **Create Script**: `scripts/research/adaptive_smc_chattering_pso.py`
   - Copy structure from `chattering_boundary_layer_pso.py`
   - Modify `_create_controller_with_boundary_layer()`:
     ```python
     return AdaptiveSMC(
         gains=self.optimized_gains,
         dt=0.01,
         max_force=150.0,
         leak_rate=0.001,           # From config
         adapt_rate_limit=5.0,      # From config
         K_min=5.0,
         K_max=50.0,
         smooth_switch=True,
         boundary_layer=epsilon,     # Param 1
         dead_zone=alpha,            # Param 2 (rename from alpha)
         K_init=10.0,
         alpha=0.5                   # Fixed proportional weight
     )
     ```
   - Update parameter naming: epsilon → boundary_layer, alpha → dead_zone

2. **Load Adaptive Phase 53 Gains**:
   ```python
   gains = [23.67, 14.29, 8.87, 3.55, 0.328]  # 5 gains
   ```

3. **Run Optimization**:
   ```bash
   python scripts/research/adaptive_smc_chattering_pso.py
   ```

4. **Expected Outcome**:
   - Stable simulations (no 79.3 penalty)
   - Optimal boundary_layer + dead_zone found
   - Chattering index comparable to Classical SMC

**Estimated Time**: 2-3 hours (1hr script + 1hr run + 30min analysis)

---

## Hybrid STA - Fix Plan

### Optimizable Parameters for Chattering

**Primary Smoothing Parameters** (2D optimization):
1. **sat_soft_width**: [0.01, 0.05] - Soft saturation width (acts as boundary layer)
2. **dead_zone**: [0.0, 0.05] - Radius where adaptation freezes

**Why These Work**:
- `sat_soft_width`: Smooths the sign function in STA algorithm (reduces chattering)
- `dead_zone`: Prevents integral wind-up and gain oscillations

**Note**: Hybrid STA uses `sat_soft_width` instead of `boundary_layer` - different name, same concept!

### Controller Signature

```python
HybridAdaptiveSTASMC(
    gains=[k1, k2, lam1, lam2],         # From Phase 53 (fixed)
    dt=0.01,                            # Fixed
    max_force=150.0,                    # Fixed
    k1_init=10.0,                       # Fixed
    k2_init=5.0,                        # Fixed
    gamma1=1.0,                         # Fixed (adaptation rate)
    gamma2=0.5,                         # Fixed (adaptation rate)
    dead_zone=dead_zone,                # OPTIMIZE (2D param 2)
    dynamics_model=None,                # Fixed
    use_relative_surface=False,         # Fixed
    enable_equivalent=True,             # Fixed
    damping_gain=3.0,                   # Fixed
    adapt_rate_limit=5.0,               # Fixed
    sat_soft_width=sat_soft_width,      # OPTIMIZE (2D param 1)
    # ... other params with defaults
)
```

### PSO Configuration

**Search Space**: 2D (sat_soft_width, dead_zone)
- sat_soft_width: [0.01, 0.05] (soft saturation boundary)
- dead_zone: [0.0, 0.05] (freeze adaptation zone)

**Fitness Function**: 70% chattering + 15% settling + 15% overshoot
**PSO Settings**: 30 particles × 50 iterations × 5 Monte Carlo runs
**Seed**: 42 (reproducibility)

### Implementation Steps

1. **Create Script**: `scripts/research/hybrid_sta_chattering_pso.py`
   - Copy structure from `chattering_boundary_layer_pso.py`
   - Modify `_create_controller_with_boundary_layer()`:
     ```python
     return HybridAdaptiveSTASMC(
         gains=self.optimized_gains,
         dt=0.01,
         max_force=150.0,
         k1_init=10.0,              # From config
         k2_init=5.0,               # From config
         gamma1=1.0,                # From config
         gamma2=0.5,                # From config
         dead_zone=alpha,           # Param 2 (rename from alpha)
         dynamics_model=None,
         sat_soft_width=epsilon,    # Param 1 (acts like boundary_layer)
         damping_gain=3.0,          # From config
         adapt_rate_limit=5.0       # From config
     )
     ```
   - Update parameter naming: epsilon → sat_soft_width, alpha → dead_zone

2. **Load Hybrid Phase 53 Gains**:
   ```python
   gains = [23.67, 14.29, 8.87, 3.55]  # 4 gains
   ```

3. **Run Optimization**:
   ```bash
   python scripts/research/hybrid_sta_chattering_pso.py
   ```

4. **Expected Outcome**:
   - Stable simulations (STA is naturally robust)
   - Optimal sat_soft_width + dead_zone found
   - Low chattering (STA is designed for smoothness)

**Estimated Time**: 2-3 hours (1hr script + 1hr run + 30min analysis)

---

## Implementation Priority

### Option A: Sequential Implementation (RECOMMENDED)

**Day 1** (2-3 hours):
1. Fix Adaptive SMC (higher impact, shares boundary_layer concept)
2. Run optimization, validate results
3. Commit Adaptive success

**Day 2** (2-3 hours):
1. Fix Hybrid STA (different parameters, learning from Adaptive)
2. Run optimization, validate results
3. Commit Hybrid success

**Total**: 4-6 hours split across 2 sessions

**Pros**: Learn from Adaptive before tackling Hybrid, manage risk
**Cons**: Takes 2 sessions

---

### Option B: Parallel Implementation (FASTER)

**Single Session** (4-5 hours):
1. Create both scripts simultaneously (2 hours)
2. Run both optimizations in parallel (2 hours)
3. Validate and commit (1 hour)

**Total**: 4-5 hours in one session

**Pros**: Faster completion, single commit
**Cons**: Higher risk if both fail

---

## Expected Results

### Framework 1 Impact (if both succeed)

**Current** (Phase 2 Partial):
- Category 2 (Safety): 53% (Classical SMC + STA MT-6 only)
- Framework 1 Overall: 76%

**After Fix** (Phase 2 Complete):
- Category 2 (Safety): **100%** (all 4 controllers with chattering optimization!)
  - Classical SMC: ✅ (epsilon=0.0448, alpha=1.917)
  - STA SMC: ✅ (MT-6, epsilon=0.00250, alpha=1.21)
  - Adaptive SMC: ✅ (boundary_layer, dead_zone - TBD)
  - Hybrid STA: ✅ (sat_soft_width, dead_zone - TBD)
- Framework 1 Overall: **85%** (+9% from 76%)

### Files to Generate

**Adaptive SMC** (3 files):
- `adaptive_smc_chattering_summary.json`
- `adaptive_smc_chattering_optimization.csv`
- `adaptive_smc_chattering_validation.csv`

**Hybrid STA** (3 files):
- `hybrid_sta_chattering_summary.json`
- `hybrid_sta_chattering_optimization.csv`
- `hybrid_sta_chattering_validation.csv`

**Total**: 6 new result files + 2 new scripts

---

## Risk Assessment

### Low Risk

**Adaptive SMC**: Has `boundary_layer` parameter - very similar to Classical SMC ✅
- 90% confidence in success
- Worst case: Optimize only boundary_layer (1D instead of 2D)

### Medium Risk

**Hybrid STA**: Different parameters (sat_soft_width, dead_zone) ⚠️
- 70% confidence in success
- STA is naturally smooth - may not show significant improvement
- Worst case: Optimization succeeds but chattering already low (baseline effect)

---

## Decision Point

### Recommend: Option A (Sequential)

**Rationale**:
1. Learn from Adaptive SMC before tackling Hybrid
2. Adaptive has higher confidence (90% vs 70%)
3. Can pivot strategy if Adaptive reveals issues
4. Still completes Phase 2 in 4-6 hours total

**Next Step**: Create `adaptive_smc_chattering_pso.py` script first

---

## Alternative: Quick Validation Test

**Before Full Implementation** (30 minutes):

Test if controllers can be instantiated with proposed parameters:

```python
# Test Adaptive SMC
from src.controllers.smc.adaptive_smc import AdaptiveSMC
adaptive = AdaptiveSMC(
    gains=[23.67, 14.29, 8.87, 3.55, 0.328],
    dt=0.01, max_force=150.0,
    leak_rate=0.001, adapt_rate_limit=5.0,
    K_min=5.0, K_max=50.0, smooth_switch=True,
    boundary_layer=0.02,  # Test value
    dead_zone=0.01,       # Test value
    K_init=10.0, alpha=0.5
)
print("Adaptive SMC: OK")

# Test Hybrid STA
from src.controllers.smc.hybrid_adaptive_sta_smc import HybridAdaptiveSTASMC
hybrid = HybridAdaptiveSTASMC(
    gains=[23.67, 14.29, 8.87, 3.55],
    dt=0.01, max_force=150.0,
    k1_init=10.0, k2_init=5.0,
    gamma1=1.0, gamma2=0.5,
    dead_zone=0.01,        # Test value
    sat_soft_width=0.02    # Test value
)
print("Hybrid STA: OK")
```

**If both pass**: Proceed with full implementation
**If either fails**: Debug controller instantiation first

---

## Summary

✅ **Both controllers ARE optimizable** for chattering
✅ **Clear parameter sets identified** (2D for each)
✅ **Implementation path validated** (adapt existing script)
✅ **Risk managed** (sequential approach, validation test)

**Recommendation**: Proceed with **Option A** (Sequential) starting with Adaptive SMC

**Time to Complete Phase 2**: 4-6 hours total (2-3 hrs per controller)

---

## Contact

**Plan Author**: AI Workspace (Claude Code)
**Date**: 2025-12-30
**Status**: Ready for implementation

**See Also**:
- Phase 2 Partial Results: `.ai_workspace/pso/by_purpose/PHASE_2_RESULTS.md`
- Classical SMC Success: `academic/paper/experiments/classical_smc/boundary_layer/`
