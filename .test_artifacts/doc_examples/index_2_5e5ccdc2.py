# Example from: docs\optimization_simulation\index.md
# Index: 2
# Runnable: True
# Hash: 5e5ccdc2

from src.simulation.engines.vector_sim import simulate_system_batch
import numpy as np

# Define controller configurations
particles = np.array([
    [10.0, 8.0, 15.0, 12.0, 50.0, 5.0],   # Conservative gains
    [20.0, 15.0, 25.0, 20.0, 80.0, 10.0],  # Aggressive gains
    [5.0, 4.0, 10.0, 8.0, 30.0, 2.0],      # Gentle gains
])

# Batch simulate
t, x_batch, u_batch, sigma_batch = simulate_system_batch(
    controller_factory=factory,
    particles=particles,
    sim_time=5.0,
    dt=0.01,
    u_max=100.0
)

# Compute metrics
for i in range(len(particles)):
    ise = np.sum(x_batch[i, :-1, :3]**2 * 0.01, axis=1).sum()
    print(f"Controller {i+1} ISE: {ise:.4f}")