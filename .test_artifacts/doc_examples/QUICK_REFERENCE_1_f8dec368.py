# Example from: docs\guides\QUICK_REFERENCE.md
# Index: 1
# Runnable: True
# Hash: f8dec368

from src.controllers.factory import create_controller
from src.core.simulation_runner import SimulationRunner
from src.config import load_config

# Load configuration
config = load_config('config.yaml')

# Create controller
controller = create_controller(
    'classical_smc',
    config=config.controllers.classical_smc
)

# Run simulation
runner = SimulationRunner(config)
result = runner.run(controller)

# Access results
print(f"ISE: {result['metrics']['ise']:.4f}")
print(f"Settling Time: {result['metrics']['settling_time']:.2f}s")