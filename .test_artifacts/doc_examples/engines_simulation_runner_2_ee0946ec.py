# Example from: docs\reference\simulation\engines_simulation_runner.md
# Index: 2
# Runnable: False
# Hash: ee0946ec

# example-metadata:
# runnable: false

from src.simulation.engines.vector_sim import simulate_system_batch
import numpy as np

# Test multiple initial conditions in parallel
initial_conditions = np.array([
    [0.1, 0.05, 0, 0, 0, 0],
    [0.2, 0.1, 0, 0, 0, 0],
    [0.15, -0.05, 0, 0, 0, 0],
    # ... 100 conditions
])

# Batch simulation (Numba accelerated)
results = simulate_system_batch(
    controller=controller,
    dynamics=dynamics,
    initial_states=initial_conditions,
    duration=5.0,
    dt=0.01
)

# Analyze batch results
settling_times = [compute_settling_time(r.states) for r in results]
print(f"Mean settling time: {np.mean(settling_times):.2f}s")