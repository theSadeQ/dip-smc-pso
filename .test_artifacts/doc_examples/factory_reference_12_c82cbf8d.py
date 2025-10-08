# Example from: docs\api\factory_reference.md
# Index: 12
# Runnable: True
# Hash: c82cbf8d

from src.controllers.factory import create_controller
from src.core.simulation_runner import SimulationRunner

# Create controller via factory
controller = create_controller('adaptive_smc')

# Use in simulation
runner = SimulationRunner(controller=controller, dynamics=dynamics)
results = runner.run(initial_state=[0.1, 0.0, 0.05, 0.0, 0.1, 0.0], duration=2.0)