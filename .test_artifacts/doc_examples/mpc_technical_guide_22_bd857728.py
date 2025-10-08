# Example from: docs\controllers\mpc_technical_guide.md
# Index: 22
# Runnable: True
# Hash: bd857728

from src.controllers.mpc import MPCController, MPCWeights
from src.core.dynamics import DoubleInvertedPendulum

# Load dynamics model
config = load_config("config.yaml")
dynamics = DoubleInvertedPendulum(config.physics)

# Configure MPC
weights = MPCWeights(
    q_x=1.0,
    q_theta=10.0,
    q_xdot=0.1,
    q_thetadot=0.5,
    r_u=1e-2
)

mpc = MPCController(
    dynamics_model=dynamics,
    horizon=20,
    dt=0.02,
    weights=weights,
    max_force=20.0,
    max_cart_pos=2.4,
    max_theta_dev=0.5
)