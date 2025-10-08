# Example from: docs\factory\factory_api_reference.md
# Index: 26
# Runnable: True
# Hash: c67c621f

from src.controllers.factory import SMCConfig

config = SMCConfig(
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    max_force=150.0,
    boundary_layer=0.02
)