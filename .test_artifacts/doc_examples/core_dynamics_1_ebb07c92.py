# Example from: docs\reference\plant\core_dynamics.md
# Index: 1
# Runnable: True
# Hash: ebb07c92

from src.plant.core.dynamics import *
import numpy as np

# Basic initialization
# Create dynamics model with standard parameters
from src.plant.models.simplified import SimplifiedDIPDynamics
from src.plant.configurations import get_default_config

config = get_default_config()
dynamics = SimplifiedDIPDynamics(config)

# Compute state derivative
state = np.array([0.0, 0.1, 0.05, 0.0, 0.0, 0.0])  # [x, θ1, θ2, ẋ, θ̇1, θ̇2]
control = np.array([5.0])  # Force in Newtons
state_dot = dynamics.step(state, control, t=0.0)
print(f"State derivative: {state_dot}")