# Example from: docs\api\simulation_engine_api_reference.md
# Index: 42
# Runnable: True
# Hash: cb4e5778

import numpy as np
from src.plant.models.base import LinearDynamicsModel

# Define linearized DIP system
A = np.array([
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 14.7, 14.7, -0.1, 0, 0],
    [0, -29.4, 14.7, 0, -0.01, 0],
    [0, 14.7, -44.1, 0, 0, -0.01]
])

B = np.array([[0], [0], [0], [1], [0], [0]])

# Create linear dynamics
linear_dynamics = LinearDynamicsModel(A, B, parameters=config.plant)

# Use with simulation
t, x, u = run_simulation(
    controller=linear_controller,
    dynamics_model=linear_dynamics,
    sim_time=5.0,
    dt=0.01,
    initial_state=[0, 0.1, 0.1, 0, 0, 0]
)