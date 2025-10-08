# Example from: docs\reference\controllers\classical-smc.md
# Index: 1
# Runnable: True
# Hash: a9482c59

from src.controllers.factory import create_controller
from src.config import load_config

# Load configuration
config = load_config('config.yaml')

# Create controller
controller = create_controller('classical_smc', config)

# Compute control (in simulation loop)
u = controller.compute_control(state, reference, time)