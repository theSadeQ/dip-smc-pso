# Example from: docs\guides\api\simulation.md
# Index: 9
# Runnable: True
# Hash: 62fb0f60

from src.core.dynamics_full import FullDynamics

dynamics = FullDynamics(config.dip_params)
state_dot = dynamics.compute_dynamics(state, control)

# Full dynamics includes:
# - Exact sin(θ), cos(θ)
# - Full Coriolis and centrifugal terms
# - Nonlinear inertia matrix