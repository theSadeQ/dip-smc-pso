# Example from: docs\guides\api\plant-models.md
# Index: 3
# Runnable: True
# Hash: 0262ccd8

from src.core.dynamics_full import FullDynamics

config.simulation.use_full_dynamics = True
dynamics = FullDynamics(config.dip_params)

state_dot = dynamics.compute_dynamics(state, control)