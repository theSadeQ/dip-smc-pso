# Example from: docs\plant\models_guide.md
# Index: 5
# Runnable: True
# Hash: d9bbdee1

from src.plant.models.lowrank import LowRankDIPDynamics, LowRankDIPConfig

# Create lightweight configuration
config = LowRankDIPConfig.create_default()

# Initialize for fast computation
dynamics = LowRankDIPDynamics(
    config=config,
    enable_monitoring=False,    # Disable for maximum speed
    enable_validation=True
)

# Use linearized dynamics for control design
A, B = dynamics.get_linearized_system(equilibrium_point="upright")

# Or compute full nonlinear dynamics
result = dynamics.compute_dynamics(state, control)

# Simple Euler integration step
next_state = dynamics.step(state, control, dt=0.01)