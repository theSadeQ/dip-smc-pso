# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 39
# Runnable: True
# Hash: 20340277

# Type-safe configuration with validation
from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig

config = ClassicalSMCConfig(
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
    max_force=150.0,
    boundary_layer=0.02,
    dt=0.001,
    switch_method="tanh"
)

controller = create_controller('classical_smc', config=config)