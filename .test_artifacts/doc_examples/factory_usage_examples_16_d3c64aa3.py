# Example from: docs\technical\factory_usage_examples.md
# Index: 16
# Runnable: True
# Hash: d3c64aa3

from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig
from src.controllers.factory import create_controller

# Create configuration once
base_config = ClassicalSMCConfig(
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
    max_force=150.0,
    boundary_layer=0.02,
    dt=0.001
)

# Reuse configuration for multiple controllers
controllers = []
for i in range(10):
    controller = create_controller('classical_smc', config=base_config)
    controllers.append(controller)

print(f"Created {len(controllers)} controllers efficiently")