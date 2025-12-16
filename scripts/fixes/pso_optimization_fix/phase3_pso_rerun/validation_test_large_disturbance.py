"""
Validation Test - LARGE Disturbance (20N - 4x larger)
Tests if much larger disturbance creates discrimination
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import numpy as np
import json
from src.config import load_config
from src.controllers.factory import create_controller
from src.optimization.core.cost_evaluator import ControllerCostEvaluator

print("="*80)
print("LARGE DISTURBANCE TEST - 20N (4x original)")
print("="*80)
print()

config = load_config("config.yaml")

class DisturbedController:
    """Controller with LARGE sinusoidal disturbance"""
    def __init__(self, base_controller, magnitude=20.0):
        self.base_controller = base_controller
        self.magnitude = magnitude
        self.time = 0.0

    def compute_control(self, state, last_control=None, history=None):
        u_base = self.base_controller.compute_control(state, last_control, history)
        disturbance = self.magnitude * np.sin(2 * np.pi * 0.5 * self.time)
        self.time += 0.01
        return u_base + disturbance

    def reset(self):
        self.base_controller.reset()
        self.time = 0.0

    def __getattr__(self, name):
        return getattr(self.base_controller, name)

def disturbed_factory(gains):
    base = create_controller(
        'adaptive_smc',
        config=config.controllers.adaptive_smc.model_dump(),
        gains=gains.tolist() if isinstance(gains, np.ndarray) else gains
    )
    return DisturbedController(base, magnitude=20.0)  # 20N disturbance!

# Test 3 different gain sets
test_gains = [
    ("MT-8 baseline", np.array([2.14, 3.36, 7.20, 0.34, 0.29])),
    ("Moderate", np.array([1.0, 1.0, 3.0, 0.3, 0.3])),
    ("Weak", np.array([0.5, 0.5, 1.0, 0.1, 0.1]))
]

evaluator = ControllerCostEvaluator(
    controller_factory=disturbed_factory,
    config=config,
    seed=42,
    u_max=150.0
)

print(f"[Testing with 20N disturbance...]")
print(f"  Disturbance: 20.0 * sin(2*pi*0.5*t)")
print(f"  This is 4x larger than initial test (5.0N)")
print()

costs = []
for name, gains in test_gains:
    print(f"Testing {name}: {gains}")
    cost = evaluator.evaluate_single(gains)
    costs.append(cost)
    print(f"  Cost: {cost:.8f}")
    print()

print("="*80)
print("RESULTS")
print("="*80)
print(f"Unique costs: {len(np.unique(costs))}")
print(f"Cost range: [{min(costs):.8f}, {max(costs):.8f}]")
print(f"All zero: {all(c == 0.0 for c in costs)}")
print()

if all(c == 0.0 for c in costs):
    print("[FAIL] Even 20N disturbance returns 0 cost")
    print()
    print("Conclusion:")
    print("  1. SMC is EXTREMELY robust (rejects 20N disturbance perfectly)")
    print("  2. OR controller wrapper not working correctly")
    print("  3. OR disturbance needs to be in dynamics, not control")
    print()
    print("RECOMMENDATION: Fall back to Option 1 (Accept findings)")
    print("  Gemini's 90% prediction was overly optimistic for this system")
else:
    print("[SUCCESS] Large disturbance created discrimination!")
    print()
    print("Can proceed with Option 2 using larger disturbances")

# Save
results = {
    'disturbance_magnitude': 20.0,
    'test_gains': [name for name, _ in test_gains],
    'costs': [float(c) for c in costs],
    'verdict': 'FAIL' if all(c == 0.0 for c in costs) else 'SUCCESS'
}

with open('pso_optimization_fix/phase3_pso_rerun/results/large_disturbance_test.json', 'w') as f:
    json.dump(results, f, indent=2)

print()
print("Results saved to: pso_optimization_fix/phase3_pso_rerun/results/large_disturbance_test.json")
