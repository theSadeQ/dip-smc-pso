# Example from: docs\optimization_simulation\guide.md
# Index: 6
# Runnable: True
# Hash: e8486c7e

from src.simulation.engines.vector_sim import simulate_system_batch
from src.controllers import create_smc_for_pso, SMCType
import numpy as np

# Define controller factory
def factory(gains):
    return create_smc_for_pso(SMCType.CLASSICAL, gains, max_force=100.0)

# Generate particle swarm (10 particles, 6 gains each)
particles = np.random.uniform(
    low=[0.1, 0.1, 0.1, 0.1, 1.0, 0.0],
    high=[50.0, 50.0, 50.0, 50.0, 200.0, 50.0],
    size=(10, 6)
)

# Batch simulate
t, x_batch, u_batch, sigma_batch = simulate_system_batch(
    controller_factory=factory,
    particles=particles,
    sim_time=5.0,
    dt=0.01,
    u_max=100.0
)

# Analyze batch results
print(f"Batch shape: {x_batch.shape}")  # (10, 501, 6)
print(f"Time steps: {len(t)}")

# Compute ISE for each particle
ise = np.sum(x_batch[:, :-1, :3]**2 * dt, axis=(1, 2))
best_particle_idx = np.argmin(ise)
print(f"Best particle: {best_particle_idx}, ISE: {ise[best_particle_idx]:.4f}")