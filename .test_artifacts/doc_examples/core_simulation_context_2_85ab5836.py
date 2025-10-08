# Example from: docs\reference\simulation\core_simulation_context.md
# Index: 2
# Runnable: True
# Hash: 85ab5836

from src.simulation.core import SimulationEngine
from src.simulation.engines import SimulationRunner

# Initialize simulation engine
runner = SimulationRunner(
    controller=controller,
    dynamics=dynamics,
    integrator='rk4',
    dt=0.01
)

# Run simulation
results = runner.simulate(
    x0=initial_state,
    duration=5.0
)

# Extract trajectories
t = results.time
x = results.states
u = results.controls