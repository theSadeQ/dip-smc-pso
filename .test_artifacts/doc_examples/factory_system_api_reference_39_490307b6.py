# Example from: docs\api\factory_system_api_reference.md
# Index: 39
# Runnable: False
# Hash: 490307b6

# Maps to SuperTwistingSMC initialization:
controller = SuperTwistingSMC(
    gains=[30.0, 18.0, 22.0, 14.0, 9.0, 7.0],
    max_force=150.0,
    dt=0.001,
    boundary_layer=0.3,
    switch_method='tanh',
    damping_gain=0.0,  # Default
    power_exponent=0.5,  # Default
    dynamics_model=<DIPDynamics instance>
)