# Example from: docs\api\factory_reference.md
# Index: 9
# Runnable: True
# Hash: 7015ba5f

from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig

config = ClassicalSMCConfig(
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    max_force=150.0,
    dt=0.001,
    boundary_layer=0.02
)

controller = create_controller('classical_smc', config=config)