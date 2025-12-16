"""
Diagnose what's happening in cost calculations
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import numpy as np
from src.config import load_config
from src.controllers.factory import create_controller
from src.plant.models.full.dynamics import FullDIPDynamics
from src.core.simulation_runner import SimulationRunner

print("="*80)
print("DIAGNOSTIC: COST CALCULATION ANALYSIS")
print("="*80)
print()

config = load_config("config.yaml")

# Test with good gains
gains = np.array([2.14, 3.36, 7.20, 0.34, 0.29])
print(f"Testing gains: {gains}")
print()

controller = create_controller(
    'adaptive_smc',
    config=config.controllers.adaptive_smc.model_dump(),
    gains=gains.tolist()
)

dynamics = FullDIPDynamics(config.physics)

# Run a single simulation with moderate perturbation
x0 = np.array([0.0, 0.0, 0.3, 0.0, 0.3, 0.0])  # +/-0.3 rad perturbation
print(f"Initial state: {x0}")
print()

runner = SimulationRunner(
    controller=controller,
    dynamics=dynamics,
    config=config,
    seed=42
)

result = runner.run(initial_state=x0, duration=10.0)

print("[Simulation Results]")
print(f"  Duration: {result.time[-1]:.2f}s")
print(f"  Steps: {len(result.time)}")
print(f"  Final state: {result.states[-1]}")
print(f"  Final state norm: {np.linalg.norm(result.states[-1]):.6f}")
print()

# Calculate ISE manually
ISE = np.sum(np.square(result.states)) * config.simulation.dt
print(f"[Cost Components]")
print(f"  ISE (state error): {ISE:.8f}")

# Control effort
control_effort = np.sum(np.square(result.controls)) * config.simulation.dt
print(f"  Control effort: {control_effort:.8f}")

# Control rate
if len(result.controls) > 1:
    du = np.diff(result.controls, axis=0) / config.simulation.dt
    control_rate = np.sum(np.square(du)) * config.simulation.dt
else:
    control_rate = 0.0
print(f"  Control rate: {control_rate:.8f}")

# Sliding variable (if available)
if hasattr(result, 'sigma') and result.sigma is not None:
    sliding = np.sum(np.square(result.sigma)) * config.simulation.dt
else:
    sliding = 0.0
print(f"  Sliding variable: {sliding:.8f}")

print()
print("[Weighted Cost]")
weights = config.cost_function.weights
print(f"  State error weight: {weights.state_error}")
print(f"  Control effort weight: {weights.control_effort}")
print(f"  Control rate weight: {weights.control_rate}")
print(f"  Sliding weight: {weights.sliding}")

total_cost = (
    weights.state_error * ISE +
    weights.control_effort * control_effort +
    weights.control_rate * control_rate +
    weights.sliding * sliding
)
print(f"\n  Total cost (weighted): {total_cost:.8f}")

print()
print("[Analysis]")
if total_cost < 1e-10:
    print("  [INFO] Cost is extremely small (<1e-10)")
    print("         This suggests PERFECT control")
elif total_cost < 1e-6:
    print("  [INFO] Cost is very small (<1e-06)")
    print("         System is well-controlled")
else:
    print(f"  [OK] Cost is measurable: {total_cost:.6f}")

# Check if states actually moved
max_angle = np.max(np.abs(result.states[:, 2:4]))
print(f"\n  Max angle deviation: {max_angle:.6f} rad ({np.degrees(max_angle):.2f} deg)")

if max_angle < 0.01:
    print("  [WARNING] Angles barely moved - may indicate simulation issue")
elif max_angle > 0.1:
    print("  [OK] Significant angle deviations - system is being tested")

print()
print("="*80)
print("CONCLUSION")
print("="*80)

if total_cost < 1e-10 and max_angle > 0.1:
    print("System achieves PERFECT control even with significant disturbances")
    print("This is GOOD for the controller, but BAD for cost discrimination")
    print("\nRecommendation:")
    print("  1. Add external disturbances during simulation")
    print("  2. Add model parameter uncertainty")
    print("  3. Use time-domain metrics (settling time, overshoot) instead of ISE")
elif total_cost < 1e-10 and max_angle < 0.01:
    print("Simulation may not be running correctly - angles barely changed")
    print("\nCheck:")
    print("  1. Initial conditions actually applied?")
    print("  2. Dynamics model working?")
    print("  3. Controller outputting non-zero control?")
else:
    print(f"Cost is measurable: {total_cost:.6f}")
    print("Cost function should be able to discriminate")
