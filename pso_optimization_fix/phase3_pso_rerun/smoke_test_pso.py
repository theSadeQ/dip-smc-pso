"""
Smoke test PSO - 5 particles, 10 iterations (~5 minutes)
Verifies that cost function discriminates properly after fixes
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import numpy as np
import json
import datetime
from src.config import load_config
from src.controllers.factory import create_controller
from src.optimization.core.robust_cost_evaluator import RobustCostEvaluator

print("="*80)
print("SMOKE TEST PSO - 5 PARTICLES, 10 ITERATIONS")
print("="*80)
print()
print("Purpose: Verify cost function discriminates after removing floor/penalty")
print("Duration: ~5 minutes (500 simulations)")
print()
print("Gemini's recommendations:")
print("  1. Ensure costs are varying (not all 0.0)")
print("  2. Best cost not exactly 0.0 (unless perfect stabilization)")
print("  3. Gains not converging to zero")
print()
print("="*80)
print()

config = load_config("config.yaml")

# MT-8 baseline for warm-start
MT8_BASELINE = np.array([2.14, 3.36, 7.20, 0.34, 0.29])

def controller_factory(gains):
    return create_controller(
        'adaptive_smc',
        config=config.controllers.adaptive_smc.model_dump(),
        gains=gains.tolist() if isinstance(gains, np.ndarray) else gains
    )

# Create robust evaluator with FIXED cost function
print("[Configuration]")
print(f"  Particles: 5 (smoke test)")
print(f"  Iterations: 10 (smoke test)")
print(f"  Scenarios: 10")
print(f"  Duration: 10.0s per simulation")
print(f"  u_max: 150.0 (EXPLICIT)")
print(f"  Perturbations: +/-0.1, +/-0.3, +/-0.5 rad")
print(f"  Warm-start: 50% near MT-8 baseline")
print()

evaluator = RobustCostEvaluator(
    controller_factory=controller_factory,
    config=config,
    seed=42,
    u_max=150.0,              # EXPLICIT!
    n_scenarios=10,
    nominal_range=0.1,
    moderate_range=0.3,
    large_range=0.5,
    worst_case_weight=0.3
)

# Search bounds
bounds = np.array([
    [0.5, 15.0],   # K1
    [0.5, 10.0],   # K2
    [0.5, 15.0],   # K3
    [0.1, 5.0],    # lambda
    [0.05, 2.0]    # eta
])

print(f"[Starting smoke test PSO...]")
print(f"Start time: {datetime.datetime.now().strftime('%H:%M:%S')}")
print()

# Initialize swarm (5 particles)
swarm = []
for i in range(5):
    if i < 3:  # 60% warm-start (3 out of 5)
        particle = MT8_BASELINE + np.random.normal(0, 0.1, 5)
        particle = np.clip(particle, bounds[:, 0], bounds[:, 1])
    else:
        particle = np.random.uniform(bounds[:, 0], bounds[:, 1])
    swarm.append(particle)

swarm = np.array(swarm)

# PSO parameters
velocities = np.zeros_like(swarm)
personal_best = swarm.copy()
personal_best_cost = np.array([evaluator.evaluate_single_robust(p) for p in swarm])
global_best = swarm[np.argmin(personal_best_cost)]
global_best_cost = np.min(personal_best_cost)

print(f"[Initial State]")
print(f"  Particle costs: {personal_best_cost}")
print(f"  Initial best cost: {global_best_cost:.8f}")
print(f"  Initial best gains: {global_best}")
print()

# Track for analysis
cost_history = [global_best_cost]
all_costs = [personal_best_cost.copy()]

# Check Gemini's concern #1: Are costs varying?
if np.all(personal_best_cost == 0.0):
    print("[WARNING] All initial costs are 0.0 - scenarios too easy!")
elif np.std(personal_best_cost) < 1e-10:
    print("[WARNING] All initial costs are identical - no variation!")
else:
    print(f"[OK] Initial cost variation: std={np.std(personal_best_cost):.6f}")

print()
print("[Running 10 iterations...]")
print()

for iteration in range(10):
    # Adaptive inertia
    w = 0.9 - (0.9 - 0.4) * iteration / 10

    # Update velocities and positions
    r1, r2 = np.random.rand(2, 5, 5)
    velocities = (w * velocities +
                  2.0 * r1 * (personal_best - swarm) +
                  2.0 * r2 * (global_best - swarm))

    swarm = swarm + velocities
    swarm = np.clip(swarm, bounds[:, 0], bounds[:, 1])

    # Evaluate
    costs = np.array([evaluator.evaluate_single_robust(p) for p in swarm])

    # Track
    all_costs.append(costs.copy())

    # Update personal bests
    improved = costs < personal_best_cost
    personal_best[improved] = swarm[improved]
    personal_best_cost[improved] = costs[improved]

    # Update global best
    if np.min(costs) < global_best_cost:
        old_best = global_best_cost
        global_best = swarm[np.argmin(costs)]
        global_best_cost = np.min(costs)
        improvement = old_best - global_best_cost
        print(f"  Iter {iteration+1:2d}: New best! {global_best_cost:.8f} (improved by {improvement:.8f})")
    else:
        print(f"  Iter {iteration+1:2d}: Best = {global_best_cost:.8f}")

    cost_history.append(global_best_cost)

print()
print("="*80)
print("SMOKE TEST COMPLETE")
print("="*80)
print(f"End time: {datetime.datetime.now().strftime('%H:%M:%S')}")
print()

# Analyze results per Gemini's recommendations
print("[ANALYSIS - Gemini's Checks]")
print()

# Check 1: Are costs varying?
all_costs_flat = np.concatenate(all_costs)
unique_costs = np.unique(all_costs_flat)
print(f"1. Cost Variation Check:")
print(f"   Unique cost values encountered: {len(unique_costs)}")
print(f"   Cost range: [{all_costs_flat.min():.8f}, {all_costs_flat.max():.8f}]")
print(f"   Cost std dev: {all_costs_flat.std():.8f}")

if len(unique_costs) <= 2:
    print(f"   [ERROR] Very few unique costs - poor discrimination!")
    verdict_1 = "FAIL"
elif all_costs_flat.std() < 1e-10:
    print(f"   [WARNING] Costs not varying - scenarios too easy")
    verdict_1 = "FAIL"
else:
    print(f"   [OK] Costs are varying properly")
    verdict_1 = "PASS"

print()

# Check 2: Best cost not exactly 0.0?
print(f"2. Zero Cost Check:")
print(f"   Final best cost: {global_best_cost:.10f}")

if global_best_cost == 0.0:
    print(f"   [WARNING] Best cost is exactly 0.0")
    print(f"            This suggests perfect control or floor still active")
    verdict_2 = "WARNING"
elif global_best_cost < 1e-10:
    print(f"   [INFO] Best cost very small (<1e-10) but non-zero")
    print(f"         System may be very controllable")
    verdict_2 = "PASS"
else:
    print(f"   [OK] Best cost is measurable")
    verdict_2 = "PASS"

print()

# Check 3: Gains not converging to zero?
print(f"3. Zero Gains Check:")
print(f"   Final best gains: {global_best}")
print(f"   Minimum gain: {global_best.min():.4f}")
print(f"   Maximum gain: {global_best.max():.4f}")

if np.all(global_best < 0.1):
    print(f"   [ERROR] All gains < 0.1 - converging to trivial solution!")
    verdict_3 = "FAIL"
elif np.any(global_best < 0.05):
    print(f"   [WARNING] Some gains < 0.05 - may be too weak")
    verdict_3 = "WARNING"
else:
    print(f"   [OK] Gains are reasonable")
    verdict_3 = "PASS"

print()

# Overall verdict
print("="*80)
print("SMOKE TEST VERDICT")
print("="*80)
verdicts = [verdict_1, verdict_2, verdict_3]
print(f"Check 1 (Cost variation): {verdict_1}")
print(f"Check 2 (Non-zero cost): {verdict_2}")
print(f"Check 3 (Non-zero gains): {verdict_3}")
print()

if all(v == "PASS" for v in verdicts):
    print("[SUCCESS] All checks passed!")
    print()
    print("RECOMMENDATION: Proceed with full PSO run")
    print("  - 30 particles, 200 iterations")
    print("  - Expected runtime: 2-4 hours")
    final_verdict = "APPROVED"
elif "FAIL" in verdicts:
    print("[FAILURE] Critical issues detected!")
    print()
    print("RECOMMENDATION: Fix issues before full PSO run")
    print("  Possible fixes:")
    if verdict_1 == "FAIL":
        print("  - Increase scenario difficulty (longer duration, larger perturbations)")
        print("  - Add disturbances or parameter uncertainty")
    if verdict_2 == "WARNING":
        print("  - Verify cost floor actually removed")
        print("  - Check if scenarios allow any error accumulation")
    if verdict_3 == "FAIL":
        print("  - Re-enable passive penalty with lower threshold")
        print("  - Add minimum gain constraints to PSO")
    final_verdict = "NOT_APPROVED"
else:
    print("[PARTIAL SUCCESS] Some warnings but no failures")
    print()
    print("RECOMMENDATION: Proceed with caution")
    print("  - Monitor costs during full run")
    print("  - Stop if best cost hits 0.0 immediately")
    print("  - Consider slightly harder scenarios")
    final_verdict = "APPROVED_WITH_CAUTION"

print()
print("="*80)
print(f"FINAL VERDICT: {final_verdict}")
print("="*80)

# Save results
results = {
    'test_type': 'smoke_test',
    'particles': 5,
    'iterations': 10,
    'scenarios': 10,
    'best_cost': float(global_best_cost),
    'best_gains': global_best.tolist(),
    'cost_history': [float(c) for c in cost_history],
    'unique_costs': len(unique_costs),
    'cost_std': float(all_costs_flat.std()),
    'check_1': verdict_1,
    'check_2': verdict_2,
    'check_3': verdict_3,
    'final_verdict': final_verdict,
    'timestamp': datetime.datetime.now().isoformat()
}

output_file = 'pso_optimization_fix/phase3_pso_rerun/results/smoke_test_results.json'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print()
print(f"Results saved to: {output_file}")
