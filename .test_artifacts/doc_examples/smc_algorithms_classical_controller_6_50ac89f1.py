# Example from: docs\reference\controllers\smc_algorithms_classical_controller.md
# Index: 6
# Runnable: True
# Hash: 50ac89f1

from src.controllers.smc.algorithms.classical import ClassicalSMC
from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig

# Configure controller
config = ClassicalSMCConfig(
    surface_gains=[10.0, 8.0, 15.0, 12.0],  # [k1, k2, λ1, λ2]
    switching_gain=50.0,                     # K
    derivative_gain=5.0,                     # kd
    max_force=100.0,
    boundary_layer=0.01
)

# Create controller
controller = ClassicalSMC(config)