# Example from: docs\api\factory_system_api_reference.md
# Index: 40
# Runnable: False
# Hash: 188b0a5f

# Maps to AdaptiveSMC initialization:
controller = AdaptiveSMC(
    gains=[28.0, 20.0, 16.0, 12.0, 5.0],
    max_force=150.0,
    dt=0.001,
    leak_rate=0.01,
    dead_zone=0.05,
    adapt_rate_limit=10.0,  # Default
    K_min=0.1,  # Default
    K_max=100.0,  # Default
    K_init=10.0,  # Default
    alpha=0.5,  # Default
    boundary_layer=0.01,  # Default
    smooth_switch=True,
    dynamics_model=<DIPDynamics instance>
)