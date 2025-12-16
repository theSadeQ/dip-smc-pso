# PSO Fix Pre-Run Review - Prompt for Gemini

**Copy this entire document and paste it to Gemini for review**

---

## Mission

Review the PSO optimization fix (Phases 1-2) before running the expensive 2-4 hour re-optimization. Verify the changes are correct and won't cause unintended side effects.

---

## Context

### Problem Identified
Independent verification (Dec 15, 2025) found:
- **Cost saturation**: Both "optimized" and baseline gains return cost = 1e-06
- **0% improvement**: PSO didn't actually improve anything
- **Root cause**: `min_cost_floor = 1e-06` prevents discrimination between controllers

### Solution Applied
**Phase 1**: Remove cost floor and passive penalty from cost evaluators
**Phase 2**: Analyze scenario difficulty (found system is very controllable)

---

## Changes Made - Please Review

### Change 1: ControllerCostEvaluator - Remove Floor (Location 1)

**File**: `src/optimization/core/cost_evaluator.py` (around line 219)

**BEFORE:**
```python
if nan_mask.any():
    J_valid[nan_mask] = self.instability_penalty

# Ensure no costs are exactly zero (double-check after _compute_cost_from_traj)
J_valid = np.maximum(J_valid, self.min_cost_floor)

# Merge valid and invalid costs
```

**AFTER:**
```python
if nan_mask.any():
    J_valid[nan_mask] = self.instability_penalty

# Cost floor removed - allow true discrimination between controllers
# Previous floor (1e-06) prevented proper cost discrimination
# J_valid = np.maximum(J_valid, self.min_cost_floor)

# Merge valid and invalid costs
```

**QUESTION FOR GEMINI:**
1. Is this change safe? Could removing the floor cause division by zero or other numerical issues?
2. Are there any downstream dependencies that expect costs >= 1e-06?

---

### Change 2: ControllerCostEvaluator - Remove Floor (Location 2)

**File**: `src/optimization/core/cost_evaluator.py` (around line 329)

**BEFORE:**
```python
# Apply minimum cost floor to prevent zero-cost solutions (PSO bug fix)
# Zero-cost solutions represent controllers with minimal activity that
# pass by inaction rather than active stabilization
cost = np.maximum(cost, self.min_cost_floor)

return cost
```

**AFTER:**
```python
# Cost floor removed - allow true zero cost if system achieves perfect control
# Previous floor (1e-06) prevented discrimination between excellent controllers
# This was causing saturation where both optimized and baseline hit the same floor
# cost = np.maximum(cost, self.min_cost_floor)

return cost
```

**QUESTION FOR GEMINI:**
1. Is it mathematically valid for cost to be exactly 0.0?
2. Could PSO handle zero costs properly, or will it cause optimization issues?

---

### Change 3: ControllerCostEvaluator - Remove Passive Penalty

**File**: `src/optimization/core/cost_evaluator.py` (around lines 308-318)

**BEFORE:**
```python
# Control activity validation (Priority 2 fix)
# Penalize "passive" controllers that avoid action rather than actively stabilizing
# This prevents PSO from converging to weak gains that pass by inaction
total_control_activity = np.sum(np.abs(u_b_trunc), axis=1)
min_activity = self.u_max * 0.01 * N  # At least 1% of max control per timestep

passive_mask = total_control_activity < min_activity
if np.any(passive_mask):
    # Penalize passive controllers with 10% of instability penalty
    # This is less severe than full instability but still discourages inaction
    cost[passive_mask] = cost[passive_mask] + 0.1 * self.instability_penalty
```

**AFTER:**
```python
# Passive controller penalty removed - was preventing proper cost discrimination
# The penalty was adding artificial costs that interfered with optimization
# Natural cost components (ISE, control effort) are sufficient to discriminate
# total_control_activity = np.sum(np.abs(u_b_trunc), axis=1)
# min_activity = self.u_max * 0.01 * N
# passive_mask = total_control_activity < min_activity
# if np.any(passive_mask):
#     cost[passive_mask] = cost[passive_mask] + 0.1 * self.instability_penalty
```

**QUESTION FOR GEMINI:**
1. Is removing the passive penalty safe? Could PSO now converge to near-zero gains?
2. Are the natural cost components (ISE, control effort, control rate) sufficient to prevent passive controllers?

---

### Change 4: RobustCostEvaluator - Remove Floor

**File**: `src/optimization/core/robust_cost_evaluator.py` (around line 251)

**BEFORE:**
```python
mean_cost = scenario_costs.mean(axis=1)
worst_cost = scenario_costs.max(axis=1)
robust_cost = mean_cost + self.worst_case_weight * worst_cost

# Apply minimum cost floor to prevent zero-cost solutions (PSO bug fix)
# This was the root cause of the zero-cost bug in RobustCostEvaluator!
robust_cost = np.maximum(robust_cost, self.min_cost_floor)

# Log statistics
```

**AFTER:**
```python
mean_cost = scenario_costs.mean(axis=1)
worst_cost = scenario_costs.max(axis=1)
robust_cost = mean_cost + self.worst_case_weight * worst_cost

# Cost floor removed - allow true cost discrimination
# Previous floor (1e-06) prevented discrimination between controllers
# Parent class (ControllerCostEvaluator) also had floor removed
# robust_cost = np.maximum(robust_cost, self.min_cost_floor)

# Log statistics
```

**QUESTION FOR GEMINI:**
1. Is it consistent to remove the floor from both the base class and this subclass?
2. Could this cause any issues with the robust cost calculation (mean + α*worst)?

---

## Phase 2 Finding

**Observation**: All gain sets (good, poor, bad) achieve cost ≈ 0 in isolated tests, even with:
- 15 second simulations (3x longer)
- ±1.0 rad (±57°) perturbations (4x larger)
- 15 scenarios

**Interpretation**: The double inverted pendulum with SMC is VERY controllable.

**Question for Gemini:**
1. Is this finding problematic for PSO optimization?
2. During PSO, will the swarm exploration create enough cost variation for discrimination?
3. Should we add disturbances or parameter uncertainty before re-running PSO?

---

## Verification Questions

Please review and answer:

### 1. Code Correctness
- [ ] Are all code changes syntactically correct?
- [ ] Are there any Python syntax errors or issues?
- [ ] Are commented-out lines safe to leave (for rollback)?

### 2. Mathematical Validity
- [ ] Can cost be exactly 0.0 without causing issues?
- [ ] Will PSO's swarm dynamics work with zero costs?
- [ ] Are the cost function weights properly normalized?

### 3. Potential Side Effects
- [ ] Could removing floors cause numerical instability?
- [ ] Are there any division-by-zero risks?
- [ ] Will other parts of the codebase break (logging, visualization, comparison)?

### 4. Optimization Impact
- [ ] Will PSO still discriminate between controllers after these changes?
- [ ] Could PSO now converge to degenerate solutions (zero gains)?
- [ ] Is the cost function still properly bounded?

### 5. Testing Strategy
- [ ] Should we test the changes on a smaller PSO run first (e.g., 5 particles, 10 iterations)?
- [ ] Are there any edge cases we should test before the full run?
- [ ] What monitoring should we add during PSO to detect issues early?

---

## Your Task, Gemini

1. **Review all 4 code changes** - Check for correctness and potential issues
2. **Answer all verification questions** - Be thorough and critical
3. **Identify risks** - What could go wrong with these changes?
4. **Recommend safeguards** - What should we monitor during PSO re-run?
5. **Give verdict**:
   - **APPROVED**: Safe to proceed with full PSO re-run (2-4 hours)
   - **APPROVED WITH CAUTION**: Proceed but monitor X, Y, Z carefully
   - **NOT APPROVED**: Fix issues A, B, C before re-running
   - **NEEDS TESTING**: Run small PSO test first (5 particles, 10 iterations)

---

## Expected PSO Configuration for Re-Run

If you approve, we'll run with:
```python
pso_config = {
    'controller': 'adaptive_smc',
    'particles': 30,
    'iterations': 200,
    'scenarios': 10,
    'duration': 10.0,  # seconds
    'u_max': 150.0,    # EXPLICIT (was bug with 20.0)
    'perturbations': {
        'nominal': 0.1,    # rad
        'moderate': 0.3,   # rad
        'large': 0.5       # rad
    },
    'warm_start': True,  # 50% particles near MT-8 baseline
    'seed': 42
}
```

Estimated runtime: **2-4 hours** (60,000 simulations)

**Final Question**: Is this configuration sensible given your review?

---

## Files to Review (If Needed)

**Changed files** (backups available):
- `src/optimization/core/cost_evaluator.py` (.backup exists)
- `src/optimization/core/robust_cost_evaluator.py` (.backup exists)

**Verification scripts** (if you want to see test results):
- `pso_optimization_fix/phase1_cost_function_fix/results/analysis.txt`
- `pso_optimization_fix/phase1_cost_function_fix/results/validation.txt`
- `pso_optimization_fix/phase2_scenario_hardening/results/extreme_scenarios_test.txt`

**Documentation**:
- `VERIFICATION_FINDINGS.md` - Original problem identification
- `pso_optimization_fix/PHASE1_2_SUMMARY.md` - Summary of changes
- `pso_optimization_fix/STATUS_AND_NEXT_STEPS.md` - Complete status

---

## How to Respond

Please provide:

1. **Executive Summary** (2-3 sentences)
   - Overall verdict: APPROVED / APPROVED WITH CAUTION / NOT APPROVED / NEEDS TESTING
   - Key concerns (if any)
   - Confidence level (High / Medium / Low)

2. **Detailed Review** (by change)
   - Change 1 (Floor removal location 1): [Assessment]
   - Change 2 (Floor removal location 2): [Assessment]
   - Change 3 (Passive penalty removal): [Assessment]
   - Change 4 (RobustCostEvaluator floor): [Assessment]

3. **Risk Assessment**
   - High risks (must address before PSO)
   - Medium risks (monitor during PSO)
   - Low risks (acceptable)

4. **Recommendations**
   - Should we do a small PSO test first? (5 particles, 10 iterations, 5 minutes)
   - What should we monitor during the full run?
   - Any config changes needed?

5. **Final Verdict**
   - [ ] APPROVED - Proceed with full PSO re-run
   - [ ] APPROVED WITH CAUTION - Proceed but watch for [X, Y, Z]
   - [ ] NOT APPROVED - Fix [issues] first
   - [ ] NEEDS TESTING - Run small test first

---

**Thank you for your review, Gemini! Your feedback will prevent wasted time if there are issues.**

---

**Generated**: December 15, 2025
**Reviewer**: Gemini (Google AI)
**Purpose**: Pre-flight check before 2-4 hour PSO optimization run
