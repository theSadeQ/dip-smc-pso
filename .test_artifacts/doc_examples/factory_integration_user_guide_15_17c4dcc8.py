# Example from: docs\factory\factory_integration_user_guide.md
# Index: 15
# Runnable: True
# Hash: 17c4dcc8

from typing import List
from dataclasses import dataclass

@dataclass
class ControllerConfig:
    gains: List[float]
    max_force: float = 150.0
    dt: float = 0.001
    boundary_layer: float = 0.02

# Type-safe configuration
config = ControllerConfig(
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
)