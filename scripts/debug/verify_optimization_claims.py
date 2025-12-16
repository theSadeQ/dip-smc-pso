"""
Independent Verification of PSO Optimization Claims

This script tests whether the "optimized" gains actually improve performance
compared to baseline/default gains.

Questions we're answering:
1. Does Adaptive SMC with "optimized" gains really have cost = 1e-06?
2. Is that better than the default/MT-8 baseline gains?
3. Does STA-SMC with cost=92.52 perform worse than Adaptive?
4. Can we trust these results?
"""

import json
import numpy as np
from src.config import load_config
from src.controllers.factory import create_controller
from src.optimization.core.cost_evaluator import ControllerCostEvaluator

print("="*80)
print("INDEPENDENT VERIFICATION OF PSO OPTIMIZATION CLAIMS")
print("="*80)
print()

# Load config
config = load_config("config.yaml")

# ============================================================================
# TEST 1: Verify Adaptive SMC "optimized" gains
# ============================================================================
print("[1/5] Testing Adaptive SMC optimized gains...")
print()

# Load optimized gains
with open('optimization_results/phase2_pso_results/adaptive_smc_gains.json', 'r') as f:
    adaptive_opt = json.load(f)

claimed_cost = adaptive_opt['cost']
opt_gains = np.array(adaptive_opt['gains'])

print(f"  Claimed cost from PSO: {claimed_cost}")
print(f"  Optimized gains: {opt_gains}")
print()

# Create controller factory
def adaptive_factory(gains):
    return create_controller(
        'adaptive_smc',
        config=config.controllers.adaptive_smc.model_dump(),
        gains=gains.tolist() if isinstance(gains, np.ndarray) else gains
    )

# Create cost evaluator WITH EXPLICIT u_max=150.0
evaluator = ControllerCostEvaluator(
    controller_factory=adaptive_factory,
    config=config,
    seed=42,
    u_max=150.0  # CRITICAL: Pass explicitly to avoid bug
)

print(f"  Cost evaluator u_max: {evaluator.u_max} N")
print(f"  Instability penalty: {evaluator.instability_penalty}")
print()

# Re-evaluate the optimized gains independently
print("  Re-evaluating optimized gains independently...")
verified_cost = evaluator.evaluate_single(opt_gains)
print(f"  Independently calculated cost: {verified_cost}")
print()

if abs(verified_cost - claimed_cost) < 0.01:
    print(f"  [OK] Cost matches claim! (diff = {abs(verified_cost - claimed_cost):.6f})")
else:
    print(f"  [WARNING] Cost mismatch! (diff = {abs(verified_cost - claimed_cost):.6f})")
print()

# ============================================================================
# TEST 2: Compare to MT-8 baseline gains
# ============================================================================
print("[2/5] Comparing to MT-8 baseline gains...")
print()

# MT-8 baseline gains from the PSO warm-start
mt8_gains = np.array([2.14, 3.36, 7.20, 0.34, 0.29])
print(f"  MT-8 baseline gains: {mt8_gains}")

mt8_cost = evaluator.evaluate_single(mt8_gains)
print(f"  MT-8 baseline cost: {mt8_cost:.6f}")
print()

improvement = (mt8_cost - verified_cost) / mt8_cost * 100
print(f"  Improvement: {improvement:.2f}%")

if verified_cost < mt8_cost:
    print(f"  [OK] Optimized gains ARE better than MT-8 baseline!")
else:
    print(f"  [WARNING] Optimized gains are NOT better than baseline!")
print()

# ============================================================================
# TEST 3: Compare to config default gains
# ============================================================================
print("[3/5] Comparing to config default gains...")
print()

# Get default gains from config
try:
    default_gains = np.array(config.controllers.adaptive_smc.gains)
    print(f"  Config default gains: {default_gains}")

    default_cost = evaluator.evaluate_single(default_gains)
    print(f"  Config default cost: {default_cost:.6f}")
    print()

    improvement_vs_default = (default_cost - verified_cost) / default_cost * 100
    print(f"  Improvement over defaults: {improvement_vs_default:.2f}%")

    if verified_cost < default_cost:
        print(f"  [OK] Optimized gains ARE better than config defaults!")
    else:
        print(f"  [WARNING] Optimized gains are NOT better than defaults!")
except Exception as e:
    print(f"  [SKIP] Could not load default gains: {e}")
print()

# ============================================================================
# TEST 4: Verify STA-SMC claims
# ============================================================================
print("[4/5] Testing STA-SMC optimized gains...")
print()

with open('optimization_results/phase2_pso_results/sta_smc_gains.json', 'r') as f:
    sta_opt = json.load(f)

sta_claimed_cost = sta_opt['cost']
sta_opt_gains = np.array(sta_opt['gains'])

print(f"  Claimed cost from PSO: {sta_claimed_cost:.2f}")
print(f"  Optimized gains: {sta_opt_gains}")
print()

# Create STA-SMC evaluator
def sta_factory(gains):
    return create_controller(
        'sta_smc',
        config=config.controllers.sta_smc.model_dump(),
        gains=gains.tolist() if isinstance(gains, np.ndarray) else gains
    )

sta_evaluator = ControllerCostEvaluator(
    controller_factory=sta_factory,
    config=config,
    seed=42,
    u_max=150.0
)

print("  Re-evaluating STA-SMC optimized gains...")
sta_verified_cost = sta_evaluator.evaluate_single(sta_opt_gains)
print(f"  Independently calculated cost: {sta_verified_cost:.2f}")
print()

if abs(sta_verified_cost - sta_claimed_cost) < 1.0:
    print(f"  [OK] STA-SMC cost matches claim!")
else:
    print(f"  [WARNING] STA-SMC cost mismatch! (diff = {abs(sta_verified_cost - sta_claimed_cost):.2f})")
print()

# ============================================================================
# TEST 5: Summary and interpretation
# ============================================================================
print("[5/5] Summary of findings...")
print()

print("="*80)
print("VERIFICATION RESULTS SUMMARY")
print("="*80)
print()

print(f"Adaptive SMC:")
print(f"  Claimed cost:   {claimed_cost:.6f}")
print(f"  Verified cost:  {verified_cost:.6f}")
print(f"  MT-8 baseline:  {mt8_cost:.6f}")
print(f"  Improvement:    {improvement:.2f}%")
print()

print(f"STA-SMC:")
print(f"  Claimed cost:   {sta_claimed_cost:.2f}")
print(f"  Verified cost:  {sta_verified_cost:.2f}")
print()

print("Interpretation:")
if verified_cost < 0.01:
    print("  [OK] Adaptive SMC achieves near-perfect performance (cost < 0.01)")
else:
    print(f"  [WARNING] Adaptive SMC cost is {verified_cost:.4f}, not near-zero")

if verified_cost < mt8_cost:
    print("  [OK] PSO optimization improved over MT-8 baseline")
else:
    print("  [WARNING] PSO did not improve over baseline")

if sta_verified_cost > 10.0:
    print(f"  [WARNING] STA-SMC cost is high ({sta_verified_cost:.2f}), may need re-optimization")
else:
    print(f"  [OK] STA-SMC cost is reasonable ({sta_verified_cost:.2f})")

print()
print("Next step: Run 'python verify_optimization_claims.py' and review results")
