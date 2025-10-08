# Example from: docs\guides\workflows\batch-simulation-workflow.md
# Index: 4
# Runnable: True
# Hash: f8747ed6

import numpy as np
from src.simulation.engines.vector_sim import simulate
from src.controllers.factory import create_controller

# Monte Carlo setup
n_trials = 1000
dt = 0.01
duration = 10.0
horizon = int(duration / dt)

# Random initial conditions (normal distribution)
initial_states = np.zeros((n_trials, 6))
initial_states[:, 0] = np.random.normal(0, 0.05, n_trials)     # x
initial_states[:, 1] = np.random.normal(0, 0.1, n_trials)      # theta1
initial_states[:, 2] = np.random.normal(0, 0.1, n_trials)      # theta2
initial_states[:, 3] = np.random.normal(0, 0.01, n_trials)     # xdot
initial_states[:, 4] = np.random.normal(0, 0.05, n_trials)     # theta1dot
initial_states[:, 5] = np.random.normal(0, 0.05, n_trials)     # theta2dot

# Controller (classical SMC)
controller = create_controller('classical_smc')

# Generate control inputs (requires custom loop for closed-loop)
# Note: For true closed-loop batch, need custom implementation
# This example shows structure

# Simplified: open-loop control for demonstration
controls = np.zeros((n_trials, horizon))  # Would compute from feedback

# Run batch simulation
results = simulate(initial_states, controls, dt, horizon,
                   energy_limits=100.0,  # Energy guard
                   state_bounds=([-5, -np.pi, -np.pi, -10, -10, -10],
                                 [5, np.pi, np.pi, 10, 10, 10]))

# Statistical analysis
final_states = results[:, -1, :]  # (n_trials, 6)
final_theta1 = final_states[:, 1]
final_theta2 = final_states[:, 2]

print(f"Monte Carlo Results ({n_trials} trials):")
print(f"  Final theta1 - Mean: {final_theta1.mean():.4f}, Std: {final_theta1.std():.4f}")
print(f"  Final theta2 - Mean: {final_theta2.mean():.4f}, Std: {final_theta2.std():.4f}")
print(f"  Success rate (|theta| < 0.1): {(np.abs(final_theta1) < 0.1).mean()*100:.1f}%")