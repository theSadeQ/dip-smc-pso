# Example from: docs\guides\workflows\batch-simulation-workflow.md
# Index: 1
# Runnable: True
# Hash: 10648a23

from src.simulation.engines.vector_sim import simulate
import numpy as np

# Single simulation
initial_state = np.array([0, 0.1, 0.05, 0, 0, 0])  # Small perturbation
controls = np.zeros(500)  # Zero control, 5 seconds
result = simulate(initial_state, controls, dt=0.01, horizon=500)
# Shape: (501, 6) - includes initial state

# Batch simulation (10 trials)
batch_size = 10
initial_states = np.zeros((batch_size, 6))
initial_states[:, 1] = np.linspace(-0.1, 0.1, batch_size)  # Vary theta1
initial_states[:, 2] = np.linspace(-0.05, 0.05, batch_size)  # Vary theta2

controls_batch = np.zeros((batch_size, 500))  # Zero control for all

results_batch = simulate(initial_states, controls_batch, dt=0.01, horizon=500)
# Shape: (10, 501, 6) - batch dimension first