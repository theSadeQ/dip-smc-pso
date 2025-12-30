# Gemini Prompt: Hybrid STA Emergency Reset Analysis

**Copy the content below and paste into Google Gemini (Gemini 1.5 Pro or Gemini 2.0 recommended)**

---

## Executive Summary

I'm working on chattering reduction for a double-inverted pendulum (DIP) control system. I've successfully optimized 2 out of 3 controllers, but the Hybrid Adaptive STA-SMC has **catastrophic failure across THREE different optimization approaches**.

**Successful Controllers**:
- Classical SMC: chattering 0.066 ✅
- Adaptive SMC: chattering 0.036 ✅ (BEST RESULT)

**Failed Controller**:
- Hybrid STA v1 (boundary layer): chattering 56.22 ❌
- Hybrid STA v2 (corrected ranges): chattering 56.21 ❌ (identical!)
- Hybrid STA Set 1 (adaptation dynamics): chattering 58.40 ❌ (worse!)

**Critical Finding**: Emergency reset triggered in **91.04% of runs** (91 out of 100 validation runs)

---

## The Core Question

**Is this a parameter tuning problem OR a fundamental controller-plant incompatibility?**

If parameter tuning: What parameter set should I try next? (I have 4-6 hours budget for one more attempt)

If fundamental incompatibility: Should I accept partial Phase 2 success (2/3 controllers) and document Hybrid STA as unfixable?

---

## System Overview

**Plant**: Double-Inverted Pendulum (DIP)
- 4 state variables: [theta1, theta1_dot, theta2, theta2_dot]
- Control input: Force applied to cart (max 150N)
- Simulation: 10 seconds, dt=0.01, 1000 timesteps

**Chattering Index**: Total Variation of control signal / simulation time
- Target: <1 (ideally <0.1)
- Classical SMC: 0.066 ✅
- Adaptive SMC: 0.036 ✅
- Hybrid STA: 56-58 ❌ (1600x worse!)

---

## Controller Details: HybridAdaptiveSTASMC

### Initialization (from Phase 53 RMSE optimization)

```python
HybridAdaptiveSTASMC(
    gains=[23.67, 14.29, 8.87, 3.55],  # k1, k2, lam1, lam2 (FIXED)
    dt=0.01,
    max_force=150.0,
    k1_init=10.0,                      # Initial STA gain 1
    k2_init=5.0,                       # Initial STA gain 2
    gamma1=<VARIES>,                   # Adaptation rate for k1
    gamma2=<VARIES>,                   # Adaptation rate for k2
    dead_zone=<VARIES>,                # Dead zone for adaptation freeze
    sat_soft_width=<VARIES>,           # Soft saturation width
    damping_gain=3.0,
    adapt_rate_limit=<VARIES>,         # Max adaptation rate
    gain_leak=<VARIES>,                # Gain leak rate
    k1_max=50.0,                       # Max adaptive gain k1
    k2_max=50.0,                       # Max adaptive gain k2
    u_int_max=50.0,                    # Integral term limit
    # ... (cart control parameters omitted for brevity)
)
```

### Control Law Structure

```
u = u_eq + u_sta + u_cart + u_int

Where:
- u_eq: Equivalent control (model-based)
- u_sta: Super-Twisting Algorithm term
- u_cart: Cart position feedback
- u_int: Integral term
```

### STA Algorithm (Super-Twisting)

```python
u_sta = -k1 * |sigma|^0.5 * sign(sigma) + u_aux
u_aux_dot = -k2 * sign(sigma)

# Adaptive gains
k1_dot = gamma1 * |sigma| if |sigma| > dead_zone else 0
k2_dot = gamma2 * |sigma| if |sigma| > dead_zone else 0
```

---

## Emergency Reset Logic (KEY FINDING)

### Conditions

```python
emergency_reset = (
    not np.isfinite(u_sat) or abs(u_sat) > self.max_force * 2 or          # Force > 300N
    not np.isfinite(k1_new) or k1_new > self.k1_max * 0.9 or              # k1 > 45
    not np.isfinite(k2_new) or k2_new > self.k2_max * 0.9 or              # k2 > 45
    not np.isfinite(u_int_new) or abs(u_int_new) > self.u_int_max * 1.5 or  # |u_int| > 75
    not np.isfinite(s) or abs(s) > 100.0 or                               # |surface| > 100
    state_norm > 10.0 or velocity_norm > 50.0                             # State explosion
)
```

### Response When Triggered

```python
if emergency_reset:
    u_sat = 0.0                                                # Emergency stop
    k1_new = max(0.0, min(self.k1_init * 0.05, self.k1_max * 0.05))  # Reduce to 5%
    k2_new = max(0.0, min(self.k2_init * 0.05, self.k2_max * 0.05))  # Reduce to 5%
    u_int_new = 0.0                                            # Reset integral
```

**Frequency**: 91.04% of runs (91 out of 100)

---

## Optimization Attempts (ALL FAILED)

### Attempt v1: Boundary Layer Optimization

**Method**: 2D PSO optimization of soft saturation + dead zone

**Parameters**:
- `sat_soft_width` (alpha): [0.05, 0.10]
- `dead_zone` (epsilon): [0.0, 0.05]

**PSO**: 30 particles × 50 iterations × 5 Monte Carlo = 7,500 simulations

**Result**:
- Chattering: 56.22 ± 15.94 ❌
- Best params: sat_soft_width=0.0927, dead_zone=0.0
- Emergency reset rate: ~92%

**Issue**: Search space excluded controller default (0.03)

---

### Attempt v2: Corrected Boundary Layer Ranges

**Method**: Same 2D PSO with corrected ranges

**Parameters**:
- `sat_soft_width` (epsilon): [0.01, 0.05] ← Includes default
- `dead_zone` (alpha): [0.0, 0.05]

**PSO**: 30 particles × 50 iterations × 5 Monte Carlo = 7,500 simulations

**Result**:
- Chattering: 56.21 ± 15.95 ❌ (IDENTICAL to v1!)
- Best params: sat_soft_width=0.05, dead_zone=0.0046
- Emergency reset rate: ~92%

**Critical Discovery**: Completely different parameters produced IDENTICAL catastrophic results!

---

### Attempt Set 1: Adaptation Dynamics (ChatGPT Recommendation)

**ChatGPT Analysis**:
> "The chattering is almost certainly dominated by the adaptive STA dynamics (k1/k2 growth + rate limits + damping) rather than the boundary-layer pair."

**Method**: 4D PSO optimization of adaptation parameters

**Parameters Optimized**:
- `gamma1`: [0.05, 0.8] (adaptation rate for k1)
- `gamma2`: [0.02, 0.4] (adaptation rate for k2)
- `adapt_rate_limit`: [0.5, 5.0] (max gain change per step)
- `gain_leak`: [1e-4, 5e-3] (gain decay rate)

**Fixed Parameters**:
- `sat_soft_width=0.03` (default)
- `dead_zone=0.0`
- `damping_gain=3.0`
- `k1_init=10.0`, `k2_init=5.0`

**Fitness Enhancement**: Added emergency reset penalty (5.0 × reset_rate)

**PSO**: 30 particles × 50 iterations × 5 Monte Carlo = 7,500 simulations

**Result**:
- Chattering: 58.40 ± 12.06 ❌ (WORSE than v1/v2!)
- Best params: gamma1=0.8, gamma2=0.40, adapt_rate_limit=4.44, gain_leak=0.0028
- **Emergency reset rate: 91.04%** (catastrophic!)
- Settling time: 9.90 ± 0.99s
- Overshoot: 10.02 ± 2.52 rad

**Conclusion**: ChatGPT's hypothesis was partially correct (adaptation parameters DO matter), but the fundamental issue remains: 91% emergency reset rate indicates controller-plant incompatibility.

---

## Bimodal Behavior Observation

Across all 3 attempts, validation runs exhibited:

- **3% of runs**: chattering=0.0, control_energy=0.0 (controller shutdown - emergency stop triggered immediately)
- **97% of runs**: chattering~60 (controller saturating/oscillating before emergency shutdown)

This is NOT normal optimization behavior. It suggests the controller cannot stabilize the plant without hitting safety limits.

---

## Comparison to Successful Controllers

### Classical SMC (SUCCESS)

**Parameters Optimized**: boundary_layer, boundary_layer_slope

**PSO**: 2D optimization, same setup (30×50×5 = 7,500 sims)

**Result**: Chattering 0.066 ± 0.069 ✅

**Method**: Boundary layer smoothing

---

### Adaptive SMC (BEST SUCCESS)

**Parameters Optimized**: boundary_layer, dead_zone

**PSO**: 2D optimization, same setup (30×50×5 = 7,500 sims)

**Result**: Chattering 0.036 ± 0.006 ✅ (45% better than Classical!)

**Method**: Boundary layer + dead zone to prevent adaptive gain oscillations

---

## Analysis Questions for Gemini

### 1. Root Cause Hypothesis

**Which hypothesis is most likely?**

A) **Parameter Tuning Problem**: There exists a parameter set that can reduce emergency reset rate to <10% and chattering to <1
   - Likelihood estimate?
   - Which parameter set should I try?

B) **Controller Design Flaw**: Hybrid STA's architecture is fundamentally incompatible with double-inverted pendulum dynamics
   - Why does emergency reset occur in 91% of runs?
   - Is this fixable without controller redesign?

C) **STA Gains Too Aggressive**: The baseline Phase 53 gains [23.67, 14.29, 8.87, 3.55] are optimized for RMSE, not chattering
   - Should I re-optimize these 4 gains for low chattering instead?
   - Would this conflict with the "fix baseline, optimize smoothing" methodology (MT-6)?

D) **Adaptation Rate Instability**: Adaptive gains k1, k2 growing too fast, hitting safety limits
   - Why didn't Set 1 fix this?
   - Are there other adaptation parameters to tune?

E) **Cart Control Interference**: Cart position feedback interfering with pendulum stabilization
   - Should I disable cart control (cart_gain=0, cart_p_gain=0)?
   - Test this hypothesis?

### 2. Parameter Set Recommendations

**If you believe this IS solvable via parameter tuning**, please provide:

**Set 2 (Your Recommendation)**:
- Parameter names: [?, ?, ?, ?]
- Search ranges: [?, ?] × [?, ?] × [?, ?] × [?, ?]
- Fixed parameters: ?
- Rationale: Why this set should work
- Expected chattering reduction: ?
- Success probability: ?%

**Set 3 (Alternative Approach)**:
- Parameter names: [?, ?, ?, ?]
- Search ranges: [?, ?] × [?, ?] × [?, ?] × [?, ?]
- Rationale: ?
- Success probability: ?%

### 3. Diagnostic Tests

**What ablation studies should I run to isolate the root cause?**

Proposed tests (prioritize 1-3):

1. **Disable Adaptation**: Set gamma1=0, gamma2=0 (freeze k1, k2 at initial values)
   - Expected outcome if adaptation is the problem?

2. **Disable STA**: Use only classical SMC portion (remove STA term)
   - Expected outcome if STA is the problem?

3. **Disable Cart Control**: Set cart_gain=0, cart_p_gain=0
   - Expected outcome if cart control interferes?

4. **Disable Equivalent Control**: Set enable_equivalent=False
   - Expected outcome?

5. **Baseline Test**: Run with ALL default parameters (no optimization)
   - What would this tell us?

6. **Re-optimize Phase 53 Gains**: Optimize [k1, k2, lam1, lam2] for chattering instead of RMSE
   - Pros/cons vs MT-6 methodology?

### 4. Emergency Reset Analysis

**Why does emergency reset occur in 91% of runs?**

Which condition is triggered most frequently?
- Force saturation (u > 300N)?
- Gain saturation (k1 or k2 > 45)?
- Integral windup (|u_int| > 75)?
- State explosion (state_norm > 10.0)?
- Surface divergence (|s| > 100.0)?

**How can I log which condition triggers most often?**

### 5. Success Probability Estimate

**Given 3 failed attempts and 91% emergency reset rate, what is the probability that:**

A) Set 2 (your recommendation) reduces chattering to <1? ___%
B) Set 3 (alternative) reduces chattering to <1? ___%
C) ANY parameter tuning can fix this? ___%

**If probability <30%, should I accept partial Phase 2 success (2/3 controllers) and document Hybrid STA as unfixable?**

---

## Constraints

**Time Budget**: 4-6 hours for ONE more PSO attempt
- Each 2D PSO: ~2 hours
- Each 4D PSO: ~2.5 hours
- Diagnostic tests: ~1 hour total

**Computational Cost**: 7,500 simulations per attempt (30 particles × 50 iterations × 5 Monte Carlo)

**Critical Constraint**: `sat_soft_width >= dead_zone` MUST hold, otherwise controller initialization fails

**Acceptance Criteria**:
- SUCCESS: chattering <1 (ideally <0.1)
- FAILURE: If unfixable, document why and move on (partial success acceptable)

---

## What I Need From You

1. **Root Cause Verdict**: Parameter tuning problem OR controller design flaw? (with confidence level)

2. **Actionable Recommendation**:
   - **If solvable**: Specific parameter set (Set 2) with exact ranges and rationale
   - **If unfixable**: Explanation of fundamental incompatibility

3. **Diagnostic Priority**: Which 2-3 tests should I run first? (ordered by diagnostic value)

4. **Success Probability**: Realistic estimate for Set 2 achieving chattering <1

5. **Time Estimate**: Hours required for recommended approach

---

## Expected Output Format

### Root Cause Analysis
**Verdict**: [Parameter Tuning / Controller Design Flaw / Re-optimize Baseline Gains]
**Confidence**: [High / Medium / Low]
**Reasoning**: [2-3 sentences]

### Recommended Action
**Option A** (if solvable):
- **Parameter Set**: [param1, param2, param3, param4]
- **Search Ranges**: [min1, max1] × [min2, max2] × ...
- **Fixed Parameters**: [param=value, ...]
- **Rationale**: [Why this should work]
- **Expected Chattering**: [range]
- **Success Probability**: [X%]
- **Time Estimate**: [X hours]

**Option B** (if unfixable):
- **Reason**: [Why controller is fundamentally incompatible]
- **Evidence**: [Emergency reset conditions analysis]
- **Recommendation**: Accept partial Phase 2 success (2/3 controllers)

### Diagnostic Tests (Priority Order)
1. **Test Name**: [Expected outcome if hypothesis correct]
2. **Test Name**: [Expected outcome]
3. **Test Name**: [Expected outcome]

### Emergency Reset Breakdown
**Most Likely Trigger**: [Force/Gain/Integral/State/Surface saturation]
**Why**: [Explanation]
**Logging Strategy**: [How to instrument code to verify]

---

## Files Available (if you need implementation details)

I can provide:
- `src/controllers/smc/hybrid_adaptive_sta_smc.py` (controller source code)
- `scripts/research/chattering_boundary_layer_pso.py` (optimization script)
- `academic/paper/experiments/hybrid_adaptive_sta/boundary_layer/hybrid_adaptive_sta_smc_boundary_layer_validation.csv` (100 validation runs)
- `PHASE_2_COMPLETE_SUMMARY.md` (comprehensive summary of all attempts)

**Just ask which files you need!**

---

## Context: Why This Matters

**Framework 1 Category 2 (Safety)** measures chattering reduction coverage:
- **Current**: 67% (2/3 controllers with chattering <1)
- **Goal**: 100% (all 3 controllers)
- **Gap**: Hybrid STA unfixable

**Publication Impact**: Still publishable! Two successful optimizations validate MT-6 methodology. Hybrid STA failure documents controller limitation (valid negative result).

**But**: I want to exhaust all reasonable approaches before accepting partial success.

---

**Thank you for your analysis! Please be specific with parameter names, ranges, and success probability estimates.**
