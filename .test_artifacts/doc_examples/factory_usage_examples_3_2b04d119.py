# Example from: docs\technical\factory_usage_examples.md
# Index: 3
# Runnable: True
# Hash: 2b04d119

from src.config import load_config
from src.controllers.factory import create_controller

# Load global configuration
config = load_config("config.yaml")

# Create controller using configuration defaults
controller = create_controller(
    controller_type='classical_smc',
    config=config  # Gains automatically extracted from config
)

# Override specific parameters while using config
controller_custom = create_controller(
    controller_type='classical_smc',
    config=config,
    gains=[10.0, 8.0, 6.0, 4.0, 20.0, 3.0]  # Override config gains
)