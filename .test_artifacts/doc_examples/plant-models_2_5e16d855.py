# Example from: docs\guides\api\plant-models.md
# Index: 2
# Runnable: True
# Hash: 5e16d855

from src.core.dynamics import SimplifiedDynamics
from src.config import load_config

config = load_config('config.yaml')
config.simulation.use_full_dynamics = False

dynamics = SimplifiedDynamics(config.dip_params)

# Compute state derivatives
state = np.array([0, 0, 0.1, 0, 0.15, 0])
control = 50.0
state_dot = dynamics.compute_dynamics(state, control)