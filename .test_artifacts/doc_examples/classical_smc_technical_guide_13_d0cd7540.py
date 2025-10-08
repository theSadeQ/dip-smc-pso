# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 13
# Runnable: True
# Hash: d0cd7540

from src.plant.models.dynamics import DoubleInvertedPendulum
from src.controllers.smc import ClassicalSMC

# Create dynamics model
dynamics = DoubleInvertedPendulum(params=physics_params)

# Create controller with dynamics (enables equivalent control)
controller = ClassicalSMC(
    gains=[10, 8, 15, 12, 50, 5],
    max_force=100.0,
    boundary_layer=0.01,
    dynamics_model=dynamics  # Model-based u_eq
)