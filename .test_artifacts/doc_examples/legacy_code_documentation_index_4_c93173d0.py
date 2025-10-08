# Example from: docs\implementation\legacy_code_documentation_index.md
# Index: 4
# Runnable: True
# Hash: c93173d0

from src.controllers.factory import create_controller
from src.core.dynamics import DoublePendulum
from src.core.simulation_runner import SimulationRunner

# Create system and controller using theory-based parameters
system = DoublePendulum()
controller = create_controller(
    'classical_smc',
    c=[5.0, 8.0, 7.0],     # From {eq}`linear_sliding_surface`
    eta=2.0,               # Satisfies {eq}`reaching_condition`
    epsilon=0.05           # Boundary layer for chattering reduction
)

# Run simulation with automatic validation
runner = SimulationRunner(system, controller)
results = runner.simulate(duration=10.0, dt=0.01)