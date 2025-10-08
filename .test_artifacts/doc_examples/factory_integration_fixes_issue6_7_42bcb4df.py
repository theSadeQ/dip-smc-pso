# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 7
# Runnable: True
# Hash: 42bcb4df

from src.config import load_config
from src.controllers.factory import create_controller

# Load global configuration
config = load_config("config.yaml")

# Create controller using configuration defaults
controller = create_controller(
    controller_type='classical_smc',
    config=config
)

# Gains will be automatically extracted from:
# config.controller_defaults.classical_smc.gains or
# config.controllers.classical_smc.gains