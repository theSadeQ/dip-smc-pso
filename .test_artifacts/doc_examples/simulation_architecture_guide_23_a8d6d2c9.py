# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 23
# Runnable: True
# Hash: a8d6d2c9

from src.simulation.engines.vector_sim import simulate

# Add input validation before simulation
assert x0.shape == (6,), f"Expected state dim 6, got {x0.shape}"
assert len(u) == horizon, f"Control length {len(u)} != horizon {horizon}"
assert dt > 0, "Time step must be positive"

states = simulate(x0, u, dt, horizon=horizon)