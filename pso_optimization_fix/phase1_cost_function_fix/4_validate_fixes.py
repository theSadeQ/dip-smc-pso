"""
Validate that cost function fixes work correctly
"""
import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import numpy as np
from src.config import load_config
from src.controllers.factory import create_controller
from src.optimization.core.cost_evaluator import ControllerCostEvaluator

print("="*80)
print("PHASE 1.4: VALIDATE COST FUNCTION FIXES")
print("="*80)
print()

config = load_config("config.yaml")

def adaptive_factory(gains):
    return create_controller(
        'adaptive_smc',
        config=config.controllers.adaptive_smc.model_dump(),
        gains=gains.tolist() if isinstance(gains, np.ndarray) else gains
    )

evaluator = ControllerCostEvaluator(
    controller_factory=adaptive_factory,
    config=config,
    seed=42,
    u_max=150.0
)

print("[Test 1] Very good gains (should have low cost)")
good_gains = np.array([2.14, 3.36, 7.20, 0.34, 0.29])
cost_good = evaluator.evaluate_single(good_gains)
print(f"  Cost: {cost_good:.8f}")

print()
print("[Test 2] Poor gains (should have higher cost)")
poor_gains = np.array([0.5, 0.5, 0.5, 0.1, 0.1])
cost_poor = evaluator.evaluate_single(poor_gains)
print(f"  Cost: {cost_poor:.8f}")

print()
print("[Test 3] Very poor gains (should have much higher cost)")
bad_gains = np.array([0.1, 0.1, 0.1, 0.01, 0.01])
cost_bad = evaluator.evaluate_single(bad_gains)
print(f"  Cost: {cost_bad:.8f}")

print()
print("="*80)
print("VALIDATION RESULTS")
print("="*80)

# Check discrimination
if cost_good < cost_poor < cost_bad:
    print("[OK] Cost function discriminates properly!")
    print(f"     Good: {cost_good:.6f} < Poor: {cost_poor:.6f} < Bad: {cost_bad:.6f}")
    discrimination_ok = True
else:
    print("[ERROR] Cost function NOT discriminating properly")
    print(f"        Good: {cost_good:.6f}, Poor: {cost_poor:.6f}, Bad: {cost_bad:.6f}")
    discrimination_ok = False

# Check for saturation
print()
if cost_good >= 1e-6:
    print(f"[WARNING] Good gains cost ({cost_good:.2e}) is at or above old floor (1e-06)")
    print("          Scenarios may need to be harder")
elif cost_good < 1e-6 and cost_poor > cost_good * 2:
    print("[OK] No cost saturation detected - costs can go below 1e-06")
    print(f"    Good cost: {cost_good:.2e} (below old floor)")
else:
    print("[INFO] Costs still close - may need harder scenarios for better discrimination")

# Check ratio
ratio = cost_poor / cost_good if cost_good > 0 else float('inf')
print()
print(f"Cost ratio (poor/good): {ratio:.2f}x")
if ratio > 10:
    print("[EXCELLENT] Very strong discrimination (>10x)")
elif ratio > 5:
    print("[OK] Strong discrimination (>5x)")
elif ratio > 2:
    print("[OK] Moderate discrimination (>2x)")
else:
    print("[WARNING] Weak discrimination (<2x) - may need harder scenarios")

print()
print("="*80)
print("FINAL VERDICT")
print("="*80)
if discrimination_ok and cost_good < 1e-6:
    print("[SUCCESS] Cost function fixes validated!")
    print("  - Costs can go below 1e-06 floor")
    print("  - Proper discrimination between gain sets")
elif discrimination_ok:
    print("[PARTIAL SUCCESS] Discrimination works, but costs still above old floor")
    print("  - Need harder scenarios to push costs lower")
else:
    print("[FAILURE] Cost function still not discriminating properly")

print()
print("Save output to: phase1_cost_function_fix/results/validation.txt")
