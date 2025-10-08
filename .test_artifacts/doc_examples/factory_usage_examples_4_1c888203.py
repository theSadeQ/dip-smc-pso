# Example from: docs\technical\factory_usage_examples.md
# Index: 4
# Runnable: True
# Hash: 1c888203

from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig
from src.controllers.factory import create_controller

# Create validated configuration
config = ClassicalSMCConfig(
    gains=[15.0, 12.0, 8.0, 6.0, 25.0, 4.0],
    max_force=150.0,
    boundary_layer=0.02,
    dt=0.001,
    switch_method="tanh",
    boundary_layer_slope=1.0,
    regularization=1e-8
)

# Create controller with validated configuration
controller = create_controller('classical_smc', config=config)