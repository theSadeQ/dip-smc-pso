# Example from: docs\plant\index.md
# Index: 1
# Runnable: True
# Hash: d0e69b42

from src.plant.models.simplified import SimplifiedDIPDynamics, SimplifiedDIPConfig

# Create configuration
config = SimplifiedDIPConfig.create_default()

# Initialize dynamics
dynamics = SimplifiedDIPDynamics(
    config,
    enable_fast_mode=True,
    enable_monitoring=True
)

# Compute dynamics
state = [0.1, 0.05, -0.03, 0.0, 0.0, 0.0]
control = [5.0]
result = dynamics.compute_dynamics(state, control)