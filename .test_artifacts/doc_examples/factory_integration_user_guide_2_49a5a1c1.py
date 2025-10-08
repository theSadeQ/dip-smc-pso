# Example from: docs\factory\factory_integration_user_guide.md
# Index: 2
# Runnable: True
# Hash: 49a5a1c1

from src.config import load_config
from src.controllers.factory import create_controller

# Load configuration with enhanced validation
config = load_config("config.yaml")

# Create controller using configuration
controller = create_controller(
    controller_type='classical_smc',
    config=config  # Factory extracts parameters automatically
)