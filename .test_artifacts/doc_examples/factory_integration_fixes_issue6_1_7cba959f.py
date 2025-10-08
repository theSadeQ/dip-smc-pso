# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 1
# Runnable: True
# Hash: 7cba959f

from src.controllers.factory import create_controller

# Simple creation with default configuration
controller = create_controller(
    controller_type='classical_smc',
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0]
)

# Advanced creation with custom configuration
from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig

config = ClassicalSMCConfig(
    gains=[10.0, 8.0, 6.0, 4.0, 20.0, 3.0],
    max_force=150.0,
    boundary_layer=0.02,
    dt=0.001,
    switch_method="tanh"
)

controller = create_controller(
    controller_type='classical_smc',
    config=config
)