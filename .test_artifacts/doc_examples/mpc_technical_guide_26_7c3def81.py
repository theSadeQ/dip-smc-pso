# Example from: docs\controllers\mpc_technical_guide.md
# Index: 26
# Runnable: True
# Hash: 7c3def81

# Direct instantiation provides full parameter control
from src.controllers.mpc.mpc_controller import MPCController

mpc = MPCController(
    dynamics_model=dynamics,
    horizon=20,
    dt=0.02,
    weights=MPCWeights(),
    max_force=20.0,
    fallback_smc_gains=[10, 8, 15, 12, 50, 5]
)