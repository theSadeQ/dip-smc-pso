# Example from: docs\guides\api\simulation.md
# Index: 17
# Runnable: True
# Hash: dbaa6e66

from src.core.vector_sim import run_batch_simulation
import numpy as np

# Define multiple initial conditions
n_trials = 100
initial_conditions = np.random.uniform(
    low=[-0.1, 0, -0.2, 0, -0.25, 0],
    high=[0.1, 0, 0.2, 0, 0.25, 0],
    size=(n_trials, 6)
)

# Run batch simulation (Numba-accelerated)
batch_results = run_batch_simulation(
    controller=controller,
    dynamics=dynamics,
    initial_conditions=initial_conditions,
    sim_params={
        'duration': 5.0,
        'dt': 0.01,
        'max_force': 100.0
    }
)

# Results shape: (n_trials, n_timesteps, n_states)
print(f"Batch results shape: {batch_results.shape}")