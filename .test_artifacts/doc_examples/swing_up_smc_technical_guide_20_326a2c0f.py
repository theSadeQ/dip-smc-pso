# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 20
# Runnable: True
# Hash: 326a2c0f

from src.controllers.smc import ClassicalSMC
from src.controllers.specialized import SwingUpSMC
from src.core.dynamics import DoubleInvertedPendulum

# Load dynamics model
config = load_config("config.yaml")
dynamics = DoubleInvertedPendulum(config.physics)

# Create stabilizing controller
stabilizer = ClassicalSMC(
    gains=[10, 8, 15, 12, 50, 5],
    max_force=20.0,
    boundary_layer=0.01,
    dynamics_model=dynamics
)

# Create swing-up controller
swing_up = SwingUpSMC(
    dynamics_model=dynamics,
    stabilizing_controller=stabilizer,
    energy_gain=50.0,
    switch_energy_factor=0.95,
    exit_energy_factor=0.90,
    switch_angle_tolerance=0.35,
    dt=0.01,
    max_force=20.0
)