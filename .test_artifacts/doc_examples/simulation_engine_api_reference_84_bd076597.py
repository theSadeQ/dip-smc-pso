# Example from: docs\api\simulation_engine_api_reference.md
# Index: 84
# Runnable: True
# Hash: bd076597

"""
Example 1: Basic DIP Simulation
Demonstrates standard workflow: load config → create controller → create dynamics → simulate → plot
"""

import numpy as np
import matplotlib.pyplot as plt
from src.config import load_config
from src.controllers import create_controller
from src.plant.models import LowRankDIPDynamics
from src.simulation import run_simulation

# ============================================================================
# STEP 1: Load Configuration
# ============================================================================
config = load_config('config.yaml')

# ============================================================================
# STEP 2: Create Controller
# ============================================================================
controller = create_controller(
    'classical_smc',
    config=config,
    gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0]  # [k1, k2, λ1, λ2, K, kd]
)

# ============================================================================
# STEP 3: Create Dynamics Model
# ============================================================================
dynamics = LowRankDIPDynamics(
    config=config.plant,
    enable_monitoring=True,
    enable_validation=True
)

# ============================================================================
# STEP 4: Run Simulation
# ============================================================================
initial_state = np.array([
    0.0,   # x: cart position
    0.1,   # theta1: pole 1 angle (small perturbation)
    0.1,   # theta2: pole 2 angle (small perturbation)
    0.0,   # x_dot: cart velocity
    0.0,   # theta1_dot: pole 1 angular velocity
    0.0    # theta2_dot: pole 2 angular velocity
])

t, x, u = run_simulation(
    controller=controller,
    dynamics_model=dynamics,
    sim_time=5.0,      # 5 seconds
    dt=0.01,           # 10ms timestep
    initial_state=initial_state,
    u_max=100.0,       # 100N force limit
    seed=42            # Reproducibility
)

# ============================================================================
# STEP 5: Analyze Results
# ============================================================================
print("=" * 70)
print("SIMULATION RESULTS")
print("=" * 70)
print(f"Simulation steps: {len(t)-1}")
print(f"Final time: {t[-1]:.2f}s")
print(f"Final state: {x[-1]}")
print(f"Max control: {np.max(np.abs(u)):.2f}N")
print(f"Mean |control|: {np.mean(np.abs(u)):.2f}N")

# Compute performance metrics
settling_time_idx = np.where(np.all(np.abs(x[:, :3]) < 0.02, axis=1))[0]
if len(settling_time_idx) > 0:
    settling_time = t[settling_time_idx[0]]
    print(f"Settling time (2% threshold): {settling_time:.3f}s")

# ============================================================================
# STEP 6: Plot Results
# ============================================================================
fig, axes = plt.subplots(4, 1, figsize=(10, 10))

# Cart position
axes[0].plot(t, x[:, 0], 'b-', linewidth=2)
axes[0].set_ylabel('Cart Position (m)', fontsize=12)
axes[0].grid(True, alpha=0.3)
axes[0].axhline(0, color='r', linestyle='--', alpha=0.5)

# Pole angles
axes[1].plot(t, x[:, 1] * 180/np.pi, 'r-', linewidth=2, label='Pole 1')
axes[1].plot(t, x[:, 2] * 180/np.pi, 'g-', linewidth=2, label='Pole 2')
axes[1].set_ylabel('Angles (deg)', fontsize=12)
axes[1].grid(True, alpha=0.3)
axes[1].legend(loc='upper right')
axes[1].axhline(0, color='k', linestyle='--', alpha=0.5)

# Velocities
axes[2].plot(t, x[:, 3], 'b-', linewidth=2, label='Cart')
axes[2].plot(t, x[:, 4], 'r-', linewidth=2, label='Pole 1')
axes[2].plot(t, x[:, 5], 'g-', linewidth=2, label='Pole 2')
axes[2].set_ylabel('Velocities', fontsize=12)
axes[2].grid(True, alpha=0.3)
axes[2].legend(loc='upper right')

# Control input
axes[3].plot(t[:-1], u, 'm-', linewidth=2)
axes[3].set_xlabel('Time (s)', fontsize=12)
axes[3].set_ylabel('Control Force (N)', fontsize=12)
axes[3].grid(True, alpha=0.3)
axes[3].axhline(100, color='r', linestyle='--', alpha=0.5, label='Limit')
axes[3].axhline(-100, color='r', linestyle='--', alpha=0.5)
axes[3].legend(loc='upper right')

plt.tight_layout()
plt.savefig('results/basic_simulation.png', dpi=150)
plt.show()

print("\nPlot saved to: results/basic_simulation.png")