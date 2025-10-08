# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 5
# Runnable: False
# Hash: 0d3d0659

# Basic controller creation with explicit gains
controller = create_controller(
    'classical_smc',
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
)

# With full configuration object
from src.config import load_config
config = load_config("config.yaml")
controller = create_controller('adaptive_smc', config=config)

# Using controller type aliases
controller = create_controller('classic_smc', gains=[...])  # Alias for classical_smc