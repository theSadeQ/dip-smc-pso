# Example from: docs\guides\api\simulation.md
# Index: 8
# Runnable: True
# Hash: f867daf4

from src.core.dynamics import SimplifiedDynamics
from src.config import load_config

config = load_config('config.yaml')
dynamics = SimplifiedDynamics(config.dip_params)

# Compute derivatives
state = np.array([0, 0, 0.1, 0, 0.15, 0])
control = 50.0
state_dot = dynamics.compute_dynamics(state, control)