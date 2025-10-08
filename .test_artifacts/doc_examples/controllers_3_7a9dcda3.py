# Example from: docs\guides\api\controllers.md
# Index: 3
# Runnable: True
# Hash: 7a9dcda3

from src.config import load_config
from src.controllers import create_controller

# Load configuration
config = load_config('config.yaml')

# Create controller with full configuration
controller = create_controller(
    controller_type='classical_smc',
    config=config.controllers.classical_smc
)

# Alternatively, specify config inline
from src.config.schemas import ClassicalSMCConfig

controller = create_controller(
    controller_type='classical_smc',
    config=ClassicalSMCConfig(
        gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
        max_force=100.0,
        boundary_layer=0.01
    )
)