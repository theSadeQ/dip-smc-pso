# Example from: docs\api\factory_system_api_reference.md
# Index: 7
# Runnable: True
# Hash: db93b447

from src.controllers.factory import create_controller
from src.config import load_config

# Load configuration
config = load_config("config.yaml")

# Create controller with config defaults
controller = create_controller('classical_smc', config)

# Use controller in simulation
state = np.array([0.0, 0.1, 0.05, 0.0, 0.0, 0.0])
control_output = controller.compute_control(state, 0.0, {})
print(f"Control force: {control_output.u:.3f} N")