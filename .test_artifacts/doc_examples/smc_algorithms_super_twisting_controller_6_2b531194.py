# Example from: docs\reference\controllers\smc_algorithms_super_twisting_controller.md
# Index: 6
# Runnable: True
# Hash: 2b531194

from src.controllers.smc.algorithms.super_twisting import ModularSuperTwistingSMC
from src.controllers.smc.algorithms.super_twisting.config import SuperTwistingSMCConfig

# Configure super-twisting controller
config = SuperTwistingSMCConfig(
    surface_gains=[25.0, 10.0, 15.0, 12.0],  # Higher gains for robustness
    proportional_gain=20.0,                   # K₁
    integral_gain=15.0,                       # K₂
    derivative_gain=5.0,                      # kd
    max_force=100.0
)

controller = ModularSuperTwistingSMC(config, dynamics=dynamics)