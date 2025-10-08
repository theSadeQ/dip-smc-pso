# Example from: docs\reference\controllers\smc_algorithms_hybrid_controller.md
# Index: 6
# Runnable: True
# Hash: 6b53741f

from src.controllers.smc.algorithms.hybrid import ModularHybridSMC
from src.controllers.smc.algorithms.hybrid.config import HybridSMCConfig

# Configure hybrid controller
config = HybridSMCConfig(
    surface_gains=[15.0, 12.0, 18.0, 15.0],
    proportional_gain=25.0,
    integral_gain=18.0,
    derivative_gain=6.0,
    max_force=100.0,
    switching_threshold=0.05  # Mode switching sensitivity
)

controller = ModularHybridSMC(config, dynamics_model=dynamics)