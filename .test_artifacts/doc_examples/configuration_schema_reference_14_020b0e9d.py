# Example from: docs\technical\configuration_schema_reference.md
# Index: 14
# Runnable: True
# Hash: 020b0e9d

from src.config import load_config
from src.controllers.factory import create_controller

# Load global configuration
config = load_config("config.yaml")

# Factory automatically extracts parameters from config structure
controller = create_controller(
    controller_type='classical_smc',
    config=config
    # Gains and parameters automatically loaded from config
)