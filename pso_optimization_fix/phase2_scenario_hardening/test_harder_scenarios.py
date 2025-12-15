"""
Test that harder scenarios discriminate between gain sets
"""
import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import numpy as np
from src.config import load_config
from src.controllers.factory import create_controller
from src.optimization.core.robust_cost_evaluator import RobustCostEvaluator

print("="*80)
print("PHASE 2: TEST HARDER SCENARIOS")
print("="*80)
print()

config = load_config("config.yaml")

# Temporarily extend simulation duration
original_duration = config.simulation.duration
config.simulation.duration = 10.0  # 5s → 10s

def adaptive_factory(gains):
    return create_controller(
        'adaptive_smc',
        config=config.controllers.adaptive_smc.model_dump(),
        gains=gains.tolist() if isinstance(gains, np.ndarray) else gains
    )

print("[Configuration]")
print(f"  Simulation duration: {config.simulation.duration}s (was {original_duration}s)")
print(f"  Scenarios: 10 (was 5)")
print(f"  Perturbation ranges:")
print(f"    Nominal: ±0.1 rad (±5.7°) - was ±0.05 rad")
print(f"    Moderate: ±0.3 rad (±17.2°) - was ±0.15 rad")
print(f"    Large: ±0.5 rad (±28.6°) - was ±0.25 rad")
print()

# Create evaluator with HARDER scenarios
evaluator = RobustCostEvaluator(
    controller_factory=adaptive_factory,
    config=config,
    seed=42,
    u_max=150.0,
    n_scenarios=10,           # 5 → 10
    nominal_range=0.1,        # ±0.05 → ±0.1
    moderate_range=0.3,       # ±0.15 → ±0.3
    large_range=0.5,          # ±0.25 → ±0.5
    worst_case_weight=0.3
)

print("[Test 1] Good gains (MT-8 baseline)")
good_gains = np.array([2.14, 3.36, 7.20, 0.34, 0.29])
print(f"  Gains: {good_gains}")
cost_good = evaluator.evaluate_single_robust(good_gains)
print(f"  Cost: {cost_good:.8f}")

print()
print("[Test 2] Poor gains")
poor_gains = np.array([0.8, 0.8, 0.8, 0.2, 0.2])
print(f"  Gains: {poor_gains}")
cost_poor = evaluator.evaluate_single_robust(poor_gains)
print(f"  Cost: {cost_poor:.8f}")

print()
print("[Test 3] Very poor gains")
bad_gains = np.array([0.3, 0.3, 0.3, 0.05, 0.05])
print(f"  Gains: {bad_gains}")
cost_bad = evaluator.evaluate_single_robust(bad_gains)
print(f"  Cost: {cost_bad:.8f}")

print()
print("="*80)
print("DISCRIMINATION ANALYSIS")
print("="*80)

# Check ordering
if cost_good < cost_poor < cost_bad:
    print("[OK] Proper ordering: good < poor < bad")
elif cost_good < cost_poor:
    print("[PARTIAL] Good < Poor, but Poor not < Bad")
elif cost_good < cost_bad:
    print("[PARTIAL] Good < Bad, but not Poor < Bad")
else:
    print("[ERROR] No proper discrimination detected")

print()
print("Cost ratios:")
ratio_1 = cost_poor / cost_good if cost_good > 0 else float('inf')
ratio_2 = cost_bad / cost_good if cost_good > 0 else float('inf')
ratio_3 = cost_bad / cost_poor if cost_poor > 0 else float('inf')

print(f"  Poor/Good: {ratio_1:.2f}x")
print(f"  Bad/Good: {ratio_2:.2f}x")
print(f"  Bad/Poor: {ratio_3:.2f}x")

print()
if ratio_1 > 10:
    print("[EXCELLENT] Very strong discrimination (>10x)")
    verdict = "SUCCESS"
elif ratio_1 > 5:
    print("[OK] Strong discrimination (>5x)")
    verdict = "SUCCESS"
elif ratio_1 > 2:
    print("[OK] Moderate discrimination (>2x)")
    verdict = "PARTIAL"
elif ratio_1 > 1.2:
    print("[WARNING] Weak discrimination (1.2-2x)")
    verdict = "WEAK"
else:
    print("[ERROR] No discrimination (<1.2x)")
    verdict = "FAILURE"

print()
print("="*80)
print("FINAL VERDICT")
print("="*80)
print(f"Status: {verdict}")

if verdict == "SUCCESS":
    print("[OK] Harder scenarios provide strong cost discrimination!")
    print("     Ready to proceed to Phase 3 (PSO re-run)")
elif verdict == "PARTIAL":
    print("[OK] Moderate discrimination achieved")
    print("     Can proceed to Phase 3, may need even harder scenarios later")
elif verdict == "WEAK":
    print("[WARNING] Weak discrimination - may need even harder scenarios")
    print("     Consider: longer duration (15s), larger perturbations (±0.8 rad)")
else:
    print("[ERROR] No discrimination - scenarios still too easy")
    print("     Must increase difficulty before PSO re-run")

print()
print("Save output to: phase2_scenario_hardening/results/harder_scenarios_test.txt")

# Restore original duration
config.simulation.duration = original_duration
