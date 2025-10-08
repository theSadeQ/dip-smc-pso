# Example from: docs\guides\api\controllers.md
# Index: 19
# Runnable: True
# Hash: 51f9a47d

from src.config import load_config
from src.controllers import create_controller
from src.core import SimulationRunner

config = load_config('config.yaml')
controller = create_controller('classical_smc', config=config.controllers.classical_smc)
runner = SimulationRunner(config)

result = runner.run(controller)
print(f"ISE: {result['metrics']['ise']:.4f}")