# Example from: docs\reference\controllers\smc_algorithms_adaptive_controller.md
# Index: 6
# Runnable: True
# Hash: 1dbaae5e

from src.controllers.smc.algorithms.adaptive import ModularAdaptiveSMC
from src.controllers.smc.algorithms.adaptive.config import AdaptiveSMCConfig

# Configure adaptive controller
config = AdaptiveSMCConfig(
    surface_gains=[10.0, 8.0, 15.0, 12.0],  # [k1, k2, λ1, λ2]
    initial_switching_gain=25.0,             # K₀
    adaptation_rate=5.0,                     # γ
    leakage_term=0.1,                        # σ
    max_force=100.0
)

controller = ModularAdaptiveSMC(config, dynamics=dynamics)