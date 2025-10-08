# Example from: docs\reference\plant\models_base_dynamics_interface.md
# Index: 3
# Runnable: True
# Hash: 263c649a

# Simplified for development
dynamics = SimplifiedDIPDynamics(config)

# Full for validation
dynamics = FullNonlinearDIPDynamics(config)

# Controller code unchanged!
controller.set_dynamics(dynamics)