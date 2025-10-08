# Example from: docs\guides\api\README.md
# Index: 7
# Runnable: True
# Hash: 713f6114

from src.config import load_config
from src.controllers import create_controller
from src.core import SimulationRunner

# Load configuration
config = load_config('config.yaml')

# Create controller
controller = create_controller('classical_smc', config=config.controllers.classical_smc)

# Run simulation
runner = SimulationRunner(config)
result = runner.run(controller)

# Access results
print(f"ISE: {result['metrics']['ise']:.4f}")