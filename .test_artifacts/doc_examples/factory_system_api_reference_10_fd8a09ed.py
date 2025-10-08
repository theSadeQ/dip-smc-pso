# Example from: docs\api\factory_system_api_reference.md
# Index: 10
# Runnable: True
# Hash: fd8a09ed

from src.controllers.factory import create_controller
from src.config import load_config

config = load_config("config.yaml")

# Override specific controller parameters
custom_gains = [30.0, 20.0, 15.0, 12.0, 45.0, 7.0]
controller = create_controller(
    'classical_smc',
    config,
    gains=custom_gains
)

# Verify custom gains applied
assert controller.gains == custom_gains
print(f"Controller created with custom gains: {controller.gains}")