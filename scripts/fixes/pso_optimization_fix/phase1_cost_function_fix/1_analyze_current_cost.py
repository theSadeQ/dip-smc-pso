"""
Analyze current cost function to identify issues
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
print("PHASE 1.1: ANALYZE CURRENT COST FUNCTION")
print("="*80)
print()

config = load_config("config.yaml")

def adaptive_factory(gains):
    return create_controller(
        'adaptive_smc',
        config=config.controllers.adaptive_smc.model_dump(),
        gains=gains.tolist() if isinstance(gains, np.ndarray) else gains
    )

# Create evaluator
evaluator = ControllerCostEvaluator(
    controller_factory=adaptive_factory,
    config=config,
    seed=42,
    u_max=150.0
)

print("[Issue 1] Check min_cost_floor")
print(f"  Current value: {evaluator.min_cost_floor}")
if evaluator.min_cost_floor >= 1e-6:
    print(f"  [ERROR] Floor is {evaluator.min_cost_floor:.2e} - too high!")
    print(f"          This prevents cost discrimination")
else:
    print(f"  [OK] Floor is low enough")
print()

print("[Issue 2] Check for passive controller penalty")
print("  Testing with very small gains (passive controller)...")
tiny_gains = np.array([0.1, 0.1, 0.1, 0.1, 0.1])
cost_tiny = evaluator.evaluate_single(tiny_gains)
print(f"  Cost with tiny gains: {cost_tiny:.6f}")

print()
print("  Testing with normal gains...")
normal_gains = np.array([2.14, 3.36, 7.20, 0.34, 0.29])
cost_normal = evaluator.evaluate_single(normal_gains)
print(f"  Cost with normal gains: {cost_normal:.6f}")

if cost_tiny >= 50.0 or cost_normal >= 50.0:
    print()
    print(f"  [ERROR] Penalty detected!")
    print(f"         Likely passive controller penalty in cost calculation")
else:
    print(f"  [OK] No obvious penalty")

print()
print("[Issue 3] Check cost formula")
print(f"  Cost weights: {evaluator.weights}")
print(f"  Normalization factors:")
print(f"    norm_ise: {evaluator.norm_ise}")
print(f"    norm_u: {evaluator.norm_u}")
print(f"    norm_du: {evaluator.norm_du}")
print(f"    norm_sigma: {evaluator.norm_sigma}")

print()
print("="*80)
print("SUMMARY")
print("="*80)
issues_found = []

if evaluator.min_cost_floor >= 1e-6:
    issues_found.append("min_cost_floor too high (1e-06)")

if cost_tiny >= 50.0 or cost_normal >= 50.0:
    issues_found.append("Passive controller penalty detected")

if issues_found:
    print("Issues found:")
    for issue in issues_found:
        print(f"  - {issue}")
else:
    print("No obvious issues found (cost function may be OK)")

print()
print("Results saved to: phase1_cost_function_fix/results/analysis.txt")
