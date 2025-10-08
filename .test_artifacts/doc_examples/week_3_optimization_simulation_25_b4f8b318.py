# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 25
# Runnable: True
# Hash: b4f8b318

from src.core.vector_sim import batch_simulate

# Generate initial conditions
x0_batch = np.random.randn(30, 6) * 0.1

# Swarm positions (gains)
gains_batch = swarm.positions  # (30, 6)

# Batch fitness evaluation
metrics_batch = batch_simulate(x0_batch, gains_batch, 5.0, 0.01)

# Extract fitness values
fitness = np.sum(metrics_batch * weights, axis=1)