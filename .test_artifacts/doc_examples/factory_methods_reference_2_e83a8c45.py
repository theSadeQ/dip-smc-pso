# Example from: docs\api\factory_methods_reference.md
# Index: 2
# Runnable: True
# Hash: e83a8c45

# Basic usage with default parameters
controller = create_controller('classical_smc')

# With explicit gains
controller = create_controller(
    'classical_smc',
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
)

# With configuration object
from src.config import load_config
config = load_config("config.yaml")
controller = create_controller('adaptive_smc', config=config)

# Combined parameters (gains override config)
controller = create_controller(
    'sta_smc',
    config=config,
    gains=[25.0, 15.0, 20.0, 12.0, 8.0, 6.0]  # Takes priority
)