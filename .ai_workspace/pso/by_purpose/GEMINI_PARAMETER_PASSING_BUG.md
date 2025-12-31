# Gemini's Parameter Passing Bug Discovery

**Date**: December 31, 2025
**Status**: CRITICAL BUG DISCOVERED - Affects ALL Phase 2 PSO optimizations
**Impact**: All 4 Hybrid STA optimization attempts (v1, v2, Set 1, Set 2) used WRONG parameters

---

## Executive Summary

Gemini discovered a **SECOND critical bug** in the Hybrid Adaptive STA-SMC controller factory that is INDEPENDENT of our emergency reset threshold bug. This parameter passing bug means that ALL our PSO optimizations were tuning parameters that weren't actually being used by the controller's sub-controllers.

**Two Separate Bugs**:
1. **Our bug** (Dec 30, fixed): Emergency reset at 0.9×k_max while clipping at k_max
2. **Gemini's bug** (Dec 31, discovered): Hybrid controller using hardcoded gains instead of passing tuned parameters

---

## The Parameter Passing Bug

### Root Cause

The `create_controller()` function in `src/controllers/factory/base.py` was creating the Hybrid Adaptive STA-SMC controller with **HARDCODED gains** for its sub-controllers, ignoring the gains passed from PSO optimization.

### Buggy Code (Lines 441-474)

```python
# BEFORE Gemini's fix
# Hybrid controllers - WRONG: uses hardcoded gains!
classical_config = ClassicalSMCConfig(
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0],  # HARDCODED!!!
    max_force=150.0,
    dt=0.001,
    boundary_layer=0.02
)

# Extract adaptive parameters from hybrid config
hybrid_gamma = controller_params.get('gamma1', 4.0)
hybrid_leak = controller_params.get('gain_leak', 0.01)

adaptive_config = AdaptiveSMCConfig(
    gains=[25.0, 18.0, 15.0, 10.0, hybrid_gamma],  # HARDCODED k1,k2,lam1,lam2!!!
    max_force=150.0,
    dt=0.001,
    leak_rate=hybrid_leak
)
```

**Problem**:
- Classical sub-controller always used [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
- Adaptive sub-controller always used [25.0, 18.0, 15.0, 10.0, gamma]
- PSO was optimizing `controller_gains[:4]` = `[c1, lambda1, c2, lambda2]` but they were NEVER passed to sub-controllers!

### Fixed Code (Gemini's fix)

```python
# AFTER Gemini's fix
# Use direct mapping for surface gains
k1_sub, k2_sub, lam1_sub, lam2_sub = controller_gains[:4]

# Sub-controller algorithmic gains (K, kd for classical; gamma for adaptive)
hybrid_gamma = controller_params.get('gamma1', 4.0)
hybrid_leak = controller_params.get('gain_leak', 0.01)

classical_sub_gains = [k1_sub, k2_sub, lam1_sub, lam2_sub, 35.0, 5.0]
adaptive_sub_gains = [k1_sub, k2_sub, lam1_sub, lam2_sub, hybrid_gamma]

# Create proper sub-configs with all required parameters
classical_config = ClassicalSMCConfig(
    gains=classical_sub_gains,  # NOW USES TUNED GAINS!
    max_force=150.0,
    dt=0.001,
    boundary_layer=0.02,
    dynamics_model=dynamics_model
)

adaptive_config = AdaptiveSMCConfig(
    gains=adaptive_sub_gains,  # NOW USES TUNED GAINS!
    max_force=150.0,
    dt=0.001,
    leak_rate=hybrid_leak,
    dynamics_model=dynamics_model
)
```

**Key Changes**:
1. Extract `k1, k2, lambda1, lambda2` from `controller_gains[:4]`
2. Use these for BOTH classical and adaptive sub-controllers
3. Adaptive sub-controller now uses tuned `k1, k2, lambda1, lambda2` with `gamma1` from controller_params
4. Added `dynamics_model` to both sub-configs for consistency

---

## Impact on Phase 2

### All 4 Optimization Attempts Were Ineffective

| Attempt | Parameters Optimized | Parameters Actually Used | Result |
|---------|---------------------|-------------------------|--------|
| v1 | sat_soft_width, dead_zone | HARDCODED [20, 15, 12, 8] | Chattering 56.22 ❌ |
| v2 | sat_soft_width, dead_zone (corrected) | HARDCODED [20, 15, 12, 8] | Chattering 56.21 ❌ (identical!) |
| Set 1 | gamma1, gamma2, adapt_rate_limit, gain_leak | HARDCODED [20, 15, 12, 8] + gamma from params | Chattering 58.40 ❌ (worse!) |
| Set 2 | gamma1, gamma2, adapt_rate_limit, gain_leak (narrower) | HARDCODED [20, 15, 12, 8] + gamma from params | Chattering 48.98 ❌ (still bad) |

**Evidence**: Set 1 and Set 2 DID use the optimized `gamma1` and `gain_leak` (from controller_params), but the surface gains `[k1, k2, lambda1, lambda2]` were always hardcoded!

---

## Gemini's Test Results

### Test Configuration

Gemini created `check_chattering.py` test script:
- Uses default gains [18.0, 12.0, 10.0, 8.0]
- Runs 10-second simulation with dt=0.001
- Computes chattering metrics after 1s transient
- Generates diagnostic plot

### Test Results (MISLEADING!)

```
Simulation failed at step 95 (t = 0.095s)
Simulation completed with 96 steps.

Chattering Metrics (after 1s transient):
  chattering_index: 0.000000
  control_rate_std: 0.000000
  zero_crossing_freq: 0.000000

SUCCESS: Chattering index is below 0.1!
```

**CRITICAL ISSUE**: The "SUCCESS" message is **MISLEADING**!
- Simulation crashed at step 95 (0.095 seconds into 10-second simulation)
- Chattering is 0.000 only because there's almost no control data to analyze (crashed before 1s transient)
- This is NOT a success - the controller is unstable!

**Conclusion**: Gemini's parameter passing fix is correct, but the controller is still unstable even with the fix.

---

## Files Modified by Gemini

**Total**: 9 files modified (92 insertions, 60 deletions)

1. **src/controllers/factory/base.py** (45 lines changed)
   - Fixed parameter passing bug for hybrid controller
   - Added dynamics_model to sub-configs

2. **src/controllers/smc/algorithms/adaptive/config.py** (9 lines changed)
   - Unknown (needs review)

3. **src/controllers/smc/algorithms/adaptive/controller.py** (5 lines changed)
   - Unknown (needs review)

4. **src/controllers/smc/algorithms/classical/controller.py** (6 lines changed)
   - Unknown (needs review)

5. **src/controllers/smc/algorithms/hybrid/controller.py** (3 lines changed)
   - Unknown (needs review)

6. **src/controllers/smc/algorithms/hybrid/switching_logic.py** (6 lines changed)
   - Unknown (needs review)

7. **src/controllers/smc/algorithms/super_twisting/controller.py** (28 lines changed)
   - Fixed indentation error (by us)
   - Unknown other changes (needs review)

8. **src/controllers/smc/core/equivalent_control.py** (8 lines changed)
   - Unknown (needs review)

9. **src/controllers/smc/core/sliding_surface.py** (42 lines changed)
   - Unknown (needs review - most lines changed)

---

## Three Bugs, Not One

### Bug 1: Emergency Reset Threshold (Our bug, Dec 30)

**Root Cause**: Threshold at 0.9×k_max while clipping at k_max
**Fix**: Changed threshold to 1.5×k_max (unreachable)
**Impact**: Emergency reset rate 91.04% → 89.38% (only 1.7% improvement)
**Conclusion**: Bug fix was necessary but NOT sufficient to solve chattering

### Bug 2: Parameter Passing (Gemini's bug, Dec 31)

**Root Cause**: Hybrid controller using hardcoded gains for sub-controllers
**Fix**: Extract and pass `k1, k2, lambda1, lambda2` from controller_gains[:4]
**Impact**: Unknown (needs testing with PSO re-run)
**Status**: Fix uncommitted, test shows controller still unstable

### Bug 3: Fundamental Controller-Plant Incompatibility (Suspected)

**Evidence**:
- Emergency reset rate 89.38% even after Bug 1 fix
- Gemini's test shows simulation failure at step 95 even after Bug 2 fix
- Emergency resets triggered by OTHER conditions (force saturation, integral windup, surface divergence, state explosion)

**Hypothesis**: Even with BOTH bug fixes, the Hybrid Adaptive STA-SMC controller has fundamental architectural issues with the double-inverted pendulum plant.

---

## Next Steps (Decision Required)

### Option 1: Test Combined Fixes

**Action**:
1. Commit Gemini's parameter passing fix
2. Re-run PSO optimization (Set 3) with BOTH fixes
3. Test if chattering <0.1 is achievable

**Pros**:
- Eliminates parameter passing bug entirely
- Gives Hybrid STA controller maximum chance of success
- Could change Phase 2 from PARTIAL to FULL SUCCESS

**Cons**:
- Gemini's test shows simulation still fails at step 95
- Additional 2-4 hours PSO optimization time
- May still fail due to fundamental incompatibility (Bug 3)

**Probability of Success**: ~20% (optimistic given Gemini's test results)

### Option 2: Accept Partial Phase 2 Success

**Action**:
1. Document Gemini's parameter passing bug discovery
2. Update Phase 2 summary with both bugs
3. Accept 2/3 controllers as PARTIAL SUCCESS
4. Proceed to publication with thorough investigation evidence

**Pros**:
- Demonstrates thoroughness (discovered 2 separate bugs)
- Valid negative result with strong evidence
- Stronger publication narrative (3 bugs found, 2 fixed, controller still fails)
- Saves 2-4 hours optimization time

**Cons**:
- Doesn't test if combined fixes solve the problem
- Leaves open question: "What if both bugs were fixed?"

**Probability of Success**: 100% (documentation always succeeds)

### Option 3: Investigate Gemini's Other Changes First

**Action**:
1. Review all 9 files Gemini modified (92 insertions, 60 deletions)
2. Understand scope of changes beyond parameter passing fix
3. Verify no new bugs introduced
4. Then decide between Option 1 or 2

**Pros**:
- Understand full scope of Gemini's work
- Avoid committing potentially buggy code
- Make informed decision

**Cons**:
- Additional investigation time (30-60 minutes)
- May reveal more complexity

**Recommendation**: Choose this option first, then decide between 1 or 2

---

## Questions for User

1. **Should we test combined fixes** (our emergency reset fix + Gemini's parameter passing fix)?
   - Requires Set 3 PSO optimization (2-4 hours)
   - Low probability of success (~20%) given Gemini's test results

2. **Should we review Gemini's other 8 file changes** before committing?
   - Some files have significant changes (sliding_surface.py: 42 lines)
   - Could reveal additional bugs or improvements

3. **Should we accept Phase 2 PARTIAL SUCCESS** and proceed to publication?
   - Already have strong evidence: 4 attempts + 2 bugs discovered + thorough investigation
   - Stronger publication narrative than before

---

## Comparison with Our Investigation

### Our Discovery (Emergency Reset Threshold Bug)

- **Found via**: Code review of emergency reset conditions
- **Impact**: 16% chattering reduction (58.40 → 48.98)
- **Root cause**: Safety threshold set too conservatively

### Gemini's Discovery (Parameter Passing Bug)

- **Found via**: Unknown (possibly prompted investigation of factory code)
- **Impact**: Unknown (needs testing)
- **Root cause**: Factory not propagating optimized gains to sub-controllers

### Combined Impact (Hypothesis)

**Scenario 1**: Both bugs were sabotaging controller independently
- **Prediction**: Fixing both → chattering drops to <0.1 ✅
- **Evidence**: None yet (needs Set 3 PSO test)

**Scenario 2**: Bugs interacted to create instability
- **Prediction**: Fixing both → controller still unstable ❌
- **Evidence**: Gemini's test shows simulation failure at step 95

**Scenario 3**: Fundamental incompatibility dominates
- **Prediction**: Fixing both → minimal improvement (chattering ~40-50) ❌
- **Evidence**: Emergency reset rate only improved 1.7% despite Bug 1 fix

---

## Timeline

| Date | Event |
|------|-------|
| Dec 29-30, 2025 | Phase 2: 3 failed Hybrid STA attempts (v1, v2, Set 1) |
| Dec 30, 2025 | We discovered emergency reset threshold bug |
| Dec 30, 2025 | Set 2 PSO launched with emergency reset fix |
| Dec 30-31, 2025 | Set 2 completed: chattering 48.98 (16% better but still failed) |
| Dec 31, 2025 | Gemini discovered parameter passing bug |
| Dec 31, 2025 | Gemini's test shows simulation failure at step 95 despite fix |
| Dec 31, 2025 | **Decision point**: Set 3 re-run vs accept partial success |

---

## Technical Details

### Parameter Mapping

**Hybrid Controller Gains** (4 parameters):
- `c1` = surface gain for pendulum 1
- `lambda1` = surface coefficient for pendulum 1
- `c2` = surface gain for pendulum 2
- `lambda2` = surface coefficient for pendulum 2

**Classical Sub-Controller Gains** (6 parameters):
- `[k1, k2, lambda1, lambda2, K, kd]`
- First 4 should come from hybrid controller gains
- Last 2 (K=35.0, kd=5.0) are algorithmic parameters

**Adaptive Sub-Controller Gains** (5 parameters):
- `[k1, k2, lambda1, lambda2, gamma]`
- First 4 should come from hybrid controller gains
- gamma comes from controller_params.gamma1

### What Was Actually Happening

**Before Fix**:
```python
# PSO optimizes controller_gains = [c1, lambda1, c2, lambda2]
controller_gains = [18.0, 12.0, 10.0, 8.0]  # Example optimized values

# Factory IGNORES these and uses hardcoded values:
classical_config.gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]  # WRONG
adaptive_config.gains = [25.0, 18.0, 15.0, 10.0, gamma]      # WRONG
```

**After Fix**:
```python
# PSO optimizes controller_gains = [c1, lambda1, c2, lambda2]
controller_gains = [18.0, 12.0, 10.0, 8.0]  # Example optimized values

# Factory CORRECTLY uses these:
k1, k2, lam1, lam2 = controller_gains[:4]  # Extract from PSO
classical_config.gains = [k1, k2, lam1, lam2, 35.0, 5.0]  # CORRECT [18, 12, 10, 8, 35, 5]
adaptive_config.gains = [k1, k2, lam1, lam2, gamma]        # CORRECT [18, 12, 10, 8, gamma]
```

---

## Unresolved Questions

1. **Why did Set 1 and Set 2 still use gamma?**
   - Answer: `hybrid_gamma = controller_params.get('gamma1', 4.0)` was already in code
   - So gamma1 WAS being used, but k1/k2/lambda1/lambda2 were NOT

2. **Why did chattering improve 16% in Set 2?**
   - Possible: Narrower gamma1 range (0.01-0.1) vs Set 1 (0.1-1.0) helped
   - But: Still using wrong surface gains [20, 15, 12, 8]

3. **Will combined fixes solve chattering?**
   - Unknown: Needs Set 3 PSO test
   - Skeptical: Gemini's test shows simulation failure

4. **What are Gemini's other 8 file changes?**
   - Unknown: Needs code review
   - sliding_surface.py: 42 lines changed (most significant)

---

**Status**: AWAITING DECISION
**Contact**: AI Workspace (Claude Code)
**Last Updated**: December 31, 2025

