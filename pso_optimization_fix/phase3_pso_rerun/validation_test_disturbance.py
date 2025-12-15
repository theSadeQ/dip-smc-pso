"""
Quick Validation Test - Disturbance Injection (Gemini's Recommendation)
Tests if adding disturbances creates cost discrimination (< 30 minutes)
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
print("QUICK VALIDATION TEST - DISTURBANCE INJECTION")
print("="*80)
print()
print("Purpose: Validate that disturbances create cost discrimination")
print("Duration: ~5 minutes (250 simulations)")
print("Test design: Add simple sinusoidal force to control input")
print()
print("Gemini's prediction: 90% success probability")
print("Pass condition: Particles show different non-zero costs")
print()
print("="*80)
print()

config = load_config("config.yaml")

# MT-8 baseline for warm-start
MT8_BASELINE = np.array([2.14, 3.36, 7.20, 0.34, 0.29])

# CRITICAL: We need to inject disturbances at the simulation level
# Since we can't easily modify the simulation runner, we'll create a wrapper
# that adds disturbance to the controller output

class DisturbedController:
    """Wrapper that adds sinusoidal disturbance to controller output"""
    def __init__(self, base_controller, disturbance_magnitude=5.0, frequency=0.5):
        self.base_controller = base_controller
        self.magnitude = disturbance_magnitude
        self.frequency = frequency
        self.time = 0.0

    def compute_control(self, state, last_control=None, history=None):
        # Get base control
        u_base = self.base_controller.compute_control(state, last_control, history)

        # Add sinusoidal disturbance
        disturbance = self.magnitude * np.sin(2 * np.pi * self.frequency * self.time)

        # Update time (approximate - will be corrected by actual simulation)
        self.time += 0.01

        return u_base + disturbance

    def reset(self):
        self.base_controller.reset()
        self.time = 0.0

    def __getattr__(self, name):
        # Delegate other attributes to base controller
        return getattr(self.base_controller, name)

def disturbed_controller_factory(gains):
    """Factory that creates controllers with disturbances"""
    base_controller = create_controller(
        'adaptive_smc',
        config=config.controllers.adaptive_smc.model_dump(),
        gains=gains.tolist() if isinstance(gains, np.ndarray) else gains
    )
    # Wrap with disturbance
    return DisturbedController(base_controller, disturbance_magnitude=5.0, frequency=0.5)

print("[Configuration]")
print(f"  Particles: 5 (validation test)")
print(f"  Iterations: 5 (validation test)")
print(f"  Scenarios: 10")
print(f"  Duration: 10.0s per simulation")
print(f"  u_max: 150.0 N")
print(f"  Disturbance: 5.0 * sin(2*pi*0.5*t) N")
print(f"  Frequency: 0.5 Hz (2-second period)")
print()

# Create robust evaluator with DISTURBED controller
evaluator = RobustCostEvaluator(
    controller_factory=disturbed_controller_factory,  # Use disturbed version
    config=config,
    seed=42,
    u_max=150.0,
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

print(f"[Starting validation test...]")
print(f"Start time: {datetime.datetime.now().strftime('%H:%M:%S')}")
print()

# Initialize swarm (5 particles)
swarm = []
for i in range(5):
    if i < 3:  # 60% warm-start
        particle = MT8_BASELINE + np.random.normal(0, 0.2, 5)
        particle = np.clip(particle, bounds[:, 0], bounds[:, 1])
    else:
        particle = np.random.uniform(bounds[:, 0], bounds[:, 1])
    swarm.append(particle)

swarm = np.array(swarm)

print("[Evaluating particles with disturbances...]")
print()

# Evaluate all particles
costs = []
for i, particle in enumerate(swarm):
    print(f"  Particle {i+1}/5: Gains = {particle}")
    try:
        cost = evaluator.evaluate_single_robust(particle)
        costs.append(cost)
        print(f"                Cost = {cost:.8f}")
    except Exception as e:
        print(f"                [ERROR] {e}")
        costs.append(float('inf'))
    print()

costs = np.array(costs)

print("="*80)
print("VALIDATION TEST RESULTS")
print("="*80)
print(f"End time: {datetime.datetime.now().strftime('%H:%M:%S')}")
print()

print("[Cost Summary]")
for i, cost in enumerate(costs):
    print(f"  Particle {i+1}: {cost:.8f}")
print()

# Analysis
unique_costs = len(np.unique(costs[np.isfinite(costs)]))
cost_std = np.std(costs[np.isfinite(costs)])
min_cost = np.min(costs[np.isfinite(costs)]) if np.any(np.isfinite(costs)) else float('inf')
max_cost = np.max(costs[np.isfinite(costs)]) if np.any(np.isfinite(costs)) else float('inf')
all_zero = np.all(costs[np.isfinite(costs)] == 0.0)
all_nonzero = np.all(costs[np.isfinite(costs)] > 0.0)

print("[Analysis]")
print(f"  Unique cost values: {unique_costs}")
print(f"  Cost range: [{min_cost:.8f}, {max_cost:.8f}]")
print(f"  Cost std dev: {cost_std:.8f}")
print(f"  All costs zero? {all_zero}")
print(f"  All costs non-zero? {all_nonzero}")
print()

# Gemini's pass condition
print("="*80)
print("GEMINI'S PASS CONDITION")
print("="*80)
print()
print("Condition: Particles show different non-zero costs")
print()

# Check 1: Are costs non-zero?
if all_zero:
    print("[FAIL] All costs are zero - disturbances didn't help")
    check1 = False
elif all_nonzero:
    print("[PASS] All costs are non-zero!")
    check1 = True
else:
    print("[PARTIAL] Some costs non-zero, some zero")
    check1 = False

print()

# Check 2: Are costs different?
if unique_costs >= 4:  # At least 4 out of 5 different
    print(f"[PASS] Costs are varying ({unique_costs} unique values)")
    check2 = True
elif unique_costs >= 2:
    print(f"[PARTIAL] Some variation ({unique_costs} unique values)")
    check2 = False
else:
    print(f"[FAIL] No variation ({unique_costs} unique value)")
    check2 = False

print()

# Check 3: Reasonable magnitude?
if min_cost > 0 and max_cost < 1000:
    print(f"[PASS] Costs in reasonable range (0 < cost < 1000)")
    check3 = True
elif max_cost >= 1000:
    print(f"[INFO] Some costs hit instability penalty (>= 1000)")
    print(f"       This is OK - shows discrimination between stable/unstable")
    check3 = True
else:
    print(f"[FAIL] Costs not in expected range")
    check3 = False

print()
print("="*80)
print("FINAL VERDICT")
print("="*80)

if check1 and check2 and check3:
    verdict = "SUCCESS"
    print("[SUCCESS] Validation test PASSED!")
    print()
    print("Disturbances successfully created cost discrimination!")
    print()
    print("RECOMMENDATION: Proceed with full Option 2 implementation")
    print("  - Implement disturbance module (1-2 hours)")
    print("  - Implement parameter uncertainty (1-2 hours)")
    print("  - Run full smoke test (10 particles, 10 iterations)")
    print("  - If successful -> Full PSO (30 particles, 200 iterations)")
    print()
    print("Expected total time: 4-6 hours")
    print("Expected success probability: 90% (per Gemini)")
elif check1 or check2:
    verdict = "PARTIAL"
    print("[PARTIAL SUCCESS] Some discrimination detected")
    print()
    print("Disturbances helped, but may need tuning:")
    print("  - Increase magnitude (5.0 -> 10.0 N)")
    print("  - Try different frequency (0.5 -> 1.0 Hz)")
    print("  - Add random component")
    print()
    print("RECOMMENDATION: Quick tuning (30 min) then re-test")
else:
    verdict = "FAILURE"
    print("[FAILURE] Validation test FAILED")
    print()
    print("Disturbances did NOT create discrimination")
    print()
    print("This is unexpected given Gemini's 90% prediction.")
    print("Possible issues:")
    print("  - Disturbance too small (increase magnitude)")
    print("  - Controller wrapper not working correctly")
    print("  - SMC is even more robust than expected")
    print()
    print("RECOMMENDATION: Debug or fall back to Option 1")

print()
print("="*80)
print(f"VERDICT: {verdict}")
print("="*80)

# Save results
results = {
    'test_type': 'disturbance_validation',
    'disturbance_magnitude': 5.0,
    'disturbance_frequency': 0.5,
    'particles': 5,
    'scenarios': 10,
    'costs': [float(c) if np.isfinite(c) else None for c in costs],
    'unique_costs': int(unique_costs),
    'cost_std': float(cost_std),
    'cost_min': float(min_cost),
    'cost_max': float(max_cost),
    'all_zero': bool(all_zero),
    'all_nonzero': bool(all_nonzero),
    'check1_nonzero': check1,
    'check2_varying': check2,
    'check3_reasonable': check3,
    'verdict': verdict,
    'timestamp': datetime.datetime.now().isoformat()
}

output_file = 'pso_optimization_fix/phase3_pso_rerun/results/disturbance_validation.json'
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print()
print(f"Results saved to: {output_file}")
