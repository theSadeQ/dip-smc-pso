# Example from: docs\api\factory_system_api_reference.md
# Index: 38
# Runnable: False
# Hash: f0953c6e

# Maps to ClassicalSMC initialization:
controller = ClassicalSMC(
    gains=[25.0, 18.0, 14.0, 10.0, 42.0, 6.0],
    max_force=150.0,
    boundary_layer=0.3,
    dt=0.001,
    regularization_alpha=1e-4,  # Default
    min_regularization=1e-10,    # Default
    max_condition_number=1e14,   # Default
    use_adaptive_regularization=True,  # Default
    dynamics_model=<DIPDynamics instance>  # Auto-created from config.physics
)