"""
Test EXTREME scenarios to force cost discrimination
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import numpy as np
from src.config import load_config
from src.controllers.factory import create_controller
from src.optimization.core.robust_cost_evaluator import RobustCostEvaluator

print("="*80)
print("PHASE 2: TEST EXTREME SCENARIOS")
print("="*80)
print()

config = load_config("config.yaml")

# EXTREME settings
original_duration = config.simulation.duration
config.simulation.duration = 15.0  # 5s → 15s (3x longer!)

def adaptive_factory(gains):
    return create_controller(
        'adaptive_smc',
        config=config.controllers.adaptive_smc.model_dump(),
        gains=gains.tolist() if isinstance(gains, np.ndarray) else gains
    )

print("[EXTREME Configuration]")
print(f"  Simulation duration: {config.simulation.duration}s (was {original_duration}s)")
print(f"  Scenarios: 15")
print(f"  Perturbation ranges:")
print(f"    Nominal: +/-0.2 rad (+/-11.5 deg)")
print(f"    Moderate: +/-0.6 rad (+/-34.4 deg)")
print(f"    Large: +/-1.0 rad (+/-57.3 deg) [EXTREME!]")
print()

# Create evaluator with EXTREME scenarios
evaluator = RobustCostEvaluator(
    controller_factory=adaptive_factory,
    config=config,
    seed=42,
    u_max=150.0,
    n_scenarios=15,           # 5 → 15
    nominal_range=0.2,        # ±0.05 → ±0.2 rad
    moderate_range=0.6,       # ±0.15 → ±0.6 rad
    large_range=1.0,          # ±0.25 → ±1.0 rad [EXTREME]
    worst_case_weight=0.4     # Emphasize worst-case
)

print("[Test 1] Good gains (MT-8 baseline)")
good_gains = np.array([2.14, 3.36, 7.20, 0.34, 0.29])
print(f"  Gains: {good_gains}")
try:
    cost_good = evaluator.evaluate_single_robust(good_gains)
    print(f"  Cost: {cost_good:.8f}")
except Exception as e:
    print(f"  [ERROR] {e}")
    cost_good = float('inf')

print()
print("[Test 2] Poor gains")
poor_gains = np.array([0.8, 0.8, 0.8, 0.2, 0.2])
print(f"  Gains: {poor_gains}")
try:
    cost_poor = evaluator.evaluate_single_robust(poor_gains)
    print(f"  Cost: {cost_poor:.8f}")
except Exception as e:
    print(f"  [ERROR] {e}")
    cost_poor = float('inf')

print()
print("[Test 3] Very poor gains")
bad_gains = np.array([0.3, 0.3, 0.3, 0.05, 0.05])
print(f"  Gains: {bad_gains}")
try:
    cost_bad = evaluator.evaluate_single_robust(bad_gains)
    print(f"  Cost: {cost_bad:.8f}")
except Exception as e:
    print(f"  [ERROR] {e}")
    cost_bad = float('inf')

print()
print("="*80)
print("DISCRIMINATION ANALYSIS")
print("="*80)

# Check if any are non-zero
if cost_good > 0 or cost_poor > 0 or cost_bad > 0:
    print("[OK] At least one cost is non-zero!")
    print(f"    Good: {cost_good:.8f}")
    print(f"    Poor: {cost_poor:.8f}")
    print(f"    Bad: {cost_bad:.8f}")

    # Check ordering
    if cost_good < cost_poor < cost_bad:
        print("[OK] Proper ordering: good < poor < bad")
    elif cost_good < cost_poor or cost_good < cost_bad:
        print("[PARTIAL] Some discrimination detected")
    else:
        print("[WARNING] No proper ordering")

    # Ratios
    if cost_good > 0:
        ratio_1 = cost_poor / cost_good
        ratio_2 = cost_bad / cost_good
        print(f"\nCost ratios:")
        print(f"  Poor/Good: {ratio_1:.2f}x")
        print(f"  Bad/Good: {ratio_2:.2f}x")

        if ratio_1 > 5:
            verdict = "EXCELLENT"
        elif ratio_1 > 2:
            verdict = "GOOD"
        elif ratio_1 > 1.2:
            verdict = "OK"
        else:
            verdict = "WEAK"
    else:
        verdict = "ZERO_GOOD"
        print("\n[INFO] Good gains achieve zero cost")
        if cost_poor > 0 or cost_bad > 0:
            print("[OK] But poor/bad gains have non-zero cost!")
            print("     This is PERFECT discrimination!")
            verdict = "PERFECT"
else:
    print("[ERROR] All costs are zero - scenarios STILL too easy!")
    verdict = "FAILURE"

print()
print("="*80)
print("FINAL VERDICT")
print("="*80)
print(f"Status: {verdict}")

if verdict in ["EXCELLENT", "PERFECT"]:
    print("[SUCCESS] Extreme scenarios provide excellent discrimination!")
    print("           Ready for PSO re-run")
elif verdict in ["GOOD", "OK"]:
    print("[OK] Moderate discrimination - proceed to PSO")
elif verdict == "ZERO_GOOD":
    print("[PARTIAL] Good gains perfect, but others also zero")
    print("          Need to verify poor/bad gains are actually worse in practice")
else:
    print("[ERROR] Still no discrimination")
    print("        May need: disturbances, parameter uncertainty, or different test")

print()
print("Save output to: phase2_scenario_hardening/results/extreme_scenarios_test.txt")

# Restore
config.simulation.duration = original_duration
