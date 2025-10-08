# Example from: docs\reference\simulation\engines_simulation_runner.md
# Index: 3
# Runnable: False
# Hash: 0cd3381f

# example-metadata:
# runnable: false

from numba import jit
from src.simulation.engines.simulation_runner import SimulationRunner

# Define JIT-compiled dynamics function
@jit(nopython=True)
def fast_dynamics_step(state, control, dt):
    # Simplified dynamics for speed
    # ... vectorized numpy operations ...
    return next_state

# Use in high-performance simulation
runner = SimulationRunner(
    dynamics_model=fast_dynamics_step,
    dt=0.001,  # High-frequency control (1kHz)
    max_time=100.0  # Long-duration test
)

result = runner.run_simulation(
    initial_state=x0,
    controller=controller,
    reference=None
)

print(f"Simulation completed in {result.computation_time:.2f}s")
print(f"Average step time: {result.computation_time / len(result.time):.6f}s")