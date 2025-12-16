"""Diagnostic script to verify PSO uses configured initial_state."""

import numpy as np
from src.config import load_config
from src.controllers.factory import create_controller
from src.simulation.engines.vector_sim import simulate_system_batch

# Load config
config = load_config("config.yaml")

# Create controller factory for classical_smc
def controller_factory(gains):
    return create_controller(
        'classical_smc',
        config=config.controllers.classical_smc,
        gains=gains
    )

# Test particles (just 2 for quick test)
particles = np.array([
    [10.0, 5.0, 8.0, 3.0, 15.0, 2.0],
    [15.0, 7.0, 10.0, 4.0, 20.0, 3.0]
])

# Extract initial state from config
initial_state = np.array(config.simulation.initial_state, dtype=float)

print("=" * 80)
print("PSO Initial State Diagnostic")
print("=" * 80)
print(f"Configured initial_state: {initial_state}")
print(f"Expected: [0.0, 0.05, -0.03, 0.0, 0.0, 0.0]")
print()

# Run simulation WITH initial_state
print("Running simulation WITH initial_state...")
print(f"sim_time={config.simulation.duration}, dt={config.simulation.dt}")
print(f"Expected steps H = {int(round(config.simulation.duration / config.simulation.dt))}")
t1, x_b1, u_b1, sigma_b1 = simulate_system_batch(
    controller_factory=controller_factory,
    particles=particles,
    sim_time=config.simulation.duration,
    dt=config.simulation.dt,
    u_max=150.0,  # Standard max_force value
    initial_state=initial_state
)
print(f"Actual steps: {len(t1)-1}")

print(f"First state (WITH initial_state): {x_b1[0, 0, :]}")
print(f"State trajectory shape: {x_b1.shape}")
print(f"Control trajectory shape: {u_b1.shape}")
if u_b1.shape[1] > 0:
    print(f"First 10 control values: {u_b1[0, :min(10, u_b1.shape[1])]}")
    print(f"Control min/max: {np.min(u_b1[0, :]):.4f} / {np.max(u_b1[0, :]):.4f}")
    print(f"Control effort: {np.sum(u_b1[0, :]**2):.6e}")
else:
    print("[ERROR] Control trajectory has ZERO steps!")
print(f"State error magnitude: {np.linalg.norm(x_b1[0, :, :]):.6e}")
print()

# Run simulation WITHOUT initial_state (should default to zero)
print("Running simulation WITHOUT initial_state (zero default)...")
t2, x_b2, u_b2, sigma_b2 = simulate_system_batch(
    controller_factory=controller_factory,
    particles=particles,
    sim_time=config.simulation.duration,
    dt=config.simulation.dt,
    u_max=150.0,  # Standard max_force value
    initial_state=None  # Should default to zero
)

print(f"First state (WITHOUT initial_state): {x_b2[0, 0, :]}")
print(f"State error magnitude: {np.linalg.norm(x_b2[0, :, :]):.6e}")
print(f"Control effort: {np.sum(u_b2[0, :]**2):.6e}")
print()

# Compare
print("=" * 80)
print("Analysis:")
print("=" * 80)
if np.allclose(x_b1[0, 0, :], initial_state, atol=1e-10):
    print("[OK] WITH initial_state: Simulation starts from configured state")
else:
    print(f"[ERROR] WITH initial_state: Expected {initial_state}, got {x_b1[0, 0, :]}")

if np.allclose(x_b2[0, 0, :], 0, atol=1e-10):
    print("[OK] WITHOUT initial_state: Simulation starts from zero")
else:
    print(f"[ERROR] WITHOUT initial_state: Expected zeros, got {x_b2[0, 0, :]}")

# Check if costs would be different
ise1 = np.sum(x_b1[0, :, :]**2)
ise2 = np.sum(x_b2[0, :, :]**2)
print()
print(f"Integrated state error WITH initial_state: {ise1:.6e}")
print(f"Integrated state error WITHOUT initial_state: {ise2:.6e}")

if ise1 > 100 * ise2:
    print("[OK] ISE is much larger with initial_state (good!)")
else:
    print(f"[WARNING] ISE ratio is only {ise1/ise2:.2f}x - should be much larger!")
