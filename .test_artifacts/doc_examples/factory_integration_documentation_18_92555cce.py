# Example from: docs\factory_integration_documentation.md
# Index: 18
# Runnable: True
# Hash: 92555cce

from src.config import load_config
from src.controllers.factory import create_controller

# Load configuration
config = load_config("config.yaml")

# Create controller with configuration
controller = create_controller('classical_smc', config=config)