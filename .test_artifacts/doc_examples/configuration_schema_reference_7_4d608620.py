# Example from: docs\technical\configuration_schema_reference.md
# Index: 7
# Runnable: True
# Hash: 4d608620

# Reduced overshoot configuration (Issue #2 resolution)
optimized_sta_config = SuperTwistingSMCConfig(
    gains=[8.0, 4.0, 12.0, 6.0, 4.85, 3.43],  # Optimized λ₁, λ₂ coefficients
    max_force=150.0,
    dt=0.001,
    power_exponent=0.5,
    boundary_layer=0.01,
    switch_method="tanh"
)