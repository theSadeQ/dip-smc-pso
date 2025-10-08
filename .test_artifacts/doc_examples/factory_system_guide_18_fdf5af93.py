# Example from: docs\controllers\factory_system_guide.md
# Index: 18
# Runnable: True
# Hash: fdf5af93

# 1. Direct parameter passing
controller = create_controller(
    'classical_smc',
    config=None,
    gains=[10, 8, 15, 12, 50, 5]
)

# 2. Configuration object
from src.config import load_config
config = load_config('config.yaml')
controller = create_controller('classical_smc', config=config)

# 3. Configuration with gain override
controller = create_controller(
    'classical_smc',
    config=config,
    gains=[20, 15, 12, 8, 35, 5]  # Overrides config
)