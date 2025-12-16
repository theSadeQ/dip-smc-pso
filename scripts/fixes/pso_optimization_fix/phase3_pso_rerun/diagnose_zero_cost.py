"""
Diagnose why all costs are returning 0.0
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import numpy as np
from src.config import load_config
from src.controllers.factory import create_controller
from src.optimization.core.cost_evaluator import ControllerCostEvaluator

print("="*80)
print("DIAGNOSTIC: WHY ARE ALL COSTS 0.0?")
print("="*80)
print()

config = load_config("config.yaml")

# Test with MT-8 baseline gains
gains = np.array([2.14, 3.36, 7.20, 0.34, 0.29])
print(f"Testing gains: {gains}")
print()

def controller_factory(gains):
    return create_controller(
        'adaptive_smc',
        config=config.controllers.adaptive_smc.model_dump(),
        gains=gains.tolist() if isinstance(gains, np.ndarray) else gains
    )

# Create evaluator (single scenario for debugging)
evaluator = ControllerCostEvaluator(
    controller_factory=controller_factory,
    config=config,
    seed=42,
    u_max=150.0
)

print("[Evaluator Configuration]")
print(f"  u_max: {evaluator.u_max}")
print(f"  min_cost_floor: {evaluator.min_cost_floor}")
print(f"  instability_penalty: {evaluator.instability_penalty}")
print(f"  Weights: {evaluator.weights}")
print(f"  Normalization factors:")
print(f"    norm_ise: {evaluator.norm_ise}")
print(f"    norm_u: {evaluator.norm_u}")
print(f"    norm_du: {evaluator.norm_du}")
print(f"    norm_sigma: {evaluator.norm_sigma}")
print()

# Test with a moderate perturbation
print("[Test 1: Single evaluation with moderate perturbation]")
print("Initial condition: [0, 0, 0.3, 0, 0.3, 0] rad")

# Evaluate - this should give us insight
cost = evaluator.evaluate_single(gains)
print(f"Returned cost: {cost:.15f}")
print()

# Let's manually trace through the cost calculation
# We need to run a simulation and inspect the trajectories
print("[Test 2: Manual simulation trace]")

# Import simulation components
from src.plant.models.full.dynamics import FullDIPDynamics
from src.core.batch_sim import run_batch_vectorized

controller = controller_factory(gains)
dynamics_model = FullDIPDynamics

# Single initial condition
x0 = np.array([[0.0, 0.0, 0.3, 0.0, 0.3, 0.0]])  # Shape (1, 6)
t_span = (0.0, 10.0)
dt = config.simulation.dt

print(f"Running simulation...")
print(f"  Duration: {t_span[1]}s")
print(f"  dt: {dt}")
print(f"  Initial state: {x0[0]}")
print()

try:
    # Run batch simulation
    results = run_batch_vectorized(
        controller=controller,
        dynamics_model=dynamics_model,
        x0_batch=x0,
        t_span=t_span,
        dt=dt,
        config=config,
        u_max=evaluator.u_max
    )

    t_b, x_b, u_b, sigma_b = results

    print(f"[Simulation Results]")
    print(f"  Time steps: {len(t_b)}")
    print(f"  States shape: {x_b.shape}")  # Should be (B, N, 6)
    print(f"  Controls shape: {u_b.shape}")  # Should be (B, N)
    print(f"  Sigma shape: {sigma_b.shape}")  # Should be (B, N)
    print()

    # Check final state
    final_state = x_b[0, -1, :]
    print(f"  Final state: {final_state}")
    print(f"  Final state norm: {np.linalg.norm(final_state):.6f}")
    print()

    # Check if states moved
    max_theta1 = np.max(np.abs(x_b[0, :, 2]))
    max_theta2 = np.max(np.abs(x_b[0, :, 4]))
    print(f"  Max theta1: {max_theta1:.6f} rad ({np.degrees(max_theta1):.2f} deg)")
    print(f"  Max theta2: {max_theta2:.6f} rad ({np.degrees(max_theta2):.2f} deg)")
    print()

    # Calculate raw cost components
    print("[Raw Cost Components]")

    # ISE
    ISE = np.sum(np.square(x_b[0]), axis=0).sum() * dt
    print(f"  ISE (raw): {ISE:.15f}")

    # Control effort
    u_squared = np.sum(np.square(u_b[0])) * dt
    print(f"  Control effort (raw): {u_squared:.15f}")

    # Control rate
    if len(u_b[0]) > 1:
        du = np.diff(u_b[0]) / dt
        du_squared = np.sum(np.square(du)) * dt
    else:
        du_squared = 0.0
    print(f"  Control rate (raw): {du_squared:.15f}")

    # Sliding variable
    sigma_squared = np.sum(np.square(sigma_b[0])) * dt
    print(f"  Sliding variable (raw): {sigma_squared:.15f}")
    print()

    # Normalized
    print("[Normalized Cost Components]")
    ISE_norm = ISE / evaluator.norm_ise if evaluator.norm_ise > 0 else ISE
    u_norm = u_squared / evaluator.norm_u if evaluator.norm_u > 0 else u_squared
    du_norm = du_squared / evaluator.norm_du if evaluator.norm_du > 0 else du_squared
    sigma_norm = sigma_squared / evaluator.norm_sigma if evaluator.norm_sigma > 0 else sigma_squared

    print(f"  ISE (normalized): {ISE_norm:.15f}")
    print(f"  Control effort (normalized): {u_norm:.15f}")
    print(f"  Control rate (normalized): {du_norm:.15f}")
    print(f"  Sliding variable (normalized): {sigma_norm:.15f}")
    print()

    # Weighted
    print("[Weighted Cost]")
    w = evaluator.weights
    weighted_cost = (
        w.state_error * ISE_norm +
        w.control_effort * u_norm +
        w.control_rate * du_norm +
        w.sliding * sigma_norm
    )
    print(f"  Total weighted cost: {weighted_cost:.15f}")
    print()

    # Check if cost components are all tiny
    if ISE < 1e-15 and u_squared < 1e-15 and du_squared < 1e-15 and sigma_squared < 1e-15:
        print("[DIAGNOSIS]")
        print("  All raw cost components are < 1e-15 (essentially zero)")
        print("  This means:")
        print("    1. System achieves perfect stabilization (ISE ≈ 0)")
        print("    2. Controller uses negligible control effort")
        print("    3. Control input barely changes (smooth)")
        print("    4. Sliding variable stays near zero")
        print()
        print("  CONCLUSION: The system is TOO EASY to control!")
        print("  Even with +/-0.3 rad perturbations, SMC achieves perfect stabilization")
        print()
        print("  SOLUTIONS:")
        print("    A. Add external disturbances (force/torque)")
        print("    B. Add model parameter uncertainty")
        print("    C. Use time-domain metrics (settling time, overshoot)")
        print("    D. Increase perturbations to +/-π/2 (90 degrees)")
        print("    E. Shorten simulation time (less time to settle)")
    else:
        print("[DIAGNOSIS]")
        print("  Some cost components are non-zero, but final cost is still 0.0")
        print("  This suggests:")
        print("    1. Normalization factors are too large")
        print("    2. Weights are too small")
        print("    3. There's still a floor operation somewhere")
        print()
        print(f"  Check normalization: norm_ise={evaluator.norm_ise}, norm_u={evaluator.norm_u}")
        print(f"  Check weights: state_error={w.state_error}, control_effort={w.control_effort}")

except Exception as e:
    print(f"[ERROR] Simulation failed: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*80)
print("END DIAGNOSTIC")
print("="*80)
