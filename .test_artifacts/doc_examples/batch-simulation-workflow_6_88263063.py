# Example from: docs\guides\workflows\batch-simulation-workflow.md
# Index: 6
# Runnable: False
# Hash: 88263063

import numpy as np
from src.simulation.engines.vector_sim import simulate
from src.controllers.factory import create_controller

# Parameter sweep: vary k1 and k2 gains
k1_values = np.linspace(5, 30, 10)
k2_values = np.linspace(5, 30, 10)

# Create grid
k1_grid, k2_grid = np.meshgrid(k1_values, k2_values)
combinations = np.column_stack([k1_grid.ravel(), k2_grid.ravel()])
n_combinations = combinations.shape[0]  # 100 combinations

# Fixed initial condition
initial_state = np.array([0, 0.2, 0.15, 0, 0, 0])  # Significant perturbation
initial_states = np.tile(initial_state, (n_combinations, 1))

# For each combination, need to create controller and simulate
# (Simplified structure - actual implementation needs custom loop)

settling_times = np.zeros(n_combinations)
overshoot = np.zeros(n_combinations)

for i, (k1, k2) in enumerate(combinations):
    # Create controller with gains
    gains = [k1, k2, 10.0, 5.0, 20.0, 1.0]  # Example gains
    controller = create_controller('classical_smc', gains=gains)

    # Simulate (would need closed-loop control)
    # controls = ... (compute from controller)
    # result = simulate(initial_state, controls, 0.01, 500)

    # Compute metrics
    # settling_times[i] = compute_settling_time(result)
    # overshoot[i] = compute_overshoot(result)
    pass  # Placeholder

# Reshape for heatmap
settling_times_grid = settling_times.reshape(k1_grid.shape)

# Plot heatmap
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.contourf(k1_grid, k2_grid, settling_times_grid, levels=20, cmap='viridis')
plt.colorbar(label='Settling Time (s)')
plt.xlabel('k1 Gain')
plt.ylabel('k2 Gain')
plt.title('Controller Gain Sweep: Settling Time')
plt.savefig('parameter_sweep_heatmap.png', dpi=150)