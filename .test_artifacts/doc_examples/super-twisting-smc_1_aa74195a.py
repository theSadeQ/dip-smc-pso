# Example from: docs\reference\controllers\super-twisting-smc.md
# Index: 1
# Runnable: True
# Hash: aa74195a

from src.controllers.factory import create_controller
from src.config import load_config

# Load configuration
config = load_config('config.yaml')

# Create controller
controller = create_controller('sta_smc', config)

# Compute control (in simulation loop)
u = controller.compute_control(state, reference, time)