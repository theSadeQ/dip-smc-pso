# Example from: docs\reference\controllers\adaptive-smc.md
# Index: 1
# Runnable: True
# Hash: 4acb2114

from src.controllers.factory import create_controller
from src.config import load_config

# Load configuration
config = load_config('config.yaml')

# Create controller
controller = create_controller('adaptive_smc', config)

# Simulation loop
for t, state in simulation:
    u = controller.compute_control(state, reference, t)

    # Monitor adaptive gains
    current_gain = controller.get_adaptive_gain()
    print(f"Adaptive gain: {current_gain:.3f}")