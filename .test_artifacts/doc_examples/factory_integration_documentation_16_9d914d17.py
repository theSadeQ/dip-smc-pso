# Example from: docs\factory_integration_documentation.md
# Index: 16
# Runnable: True
# Hash: 9d914d17

from src.controllers.factory import create_controller
from src.core.simulation_runner import SimulationRunner

# Create controller through factory
controller = create_controller('classical_smc', config=sim_config)

# Integrate with simulation engine
runner = SimulationRunner(
    controller=controller,
    dynamics=dynamics_model,
    config=sim_config
)

results = runner.run_simulation()