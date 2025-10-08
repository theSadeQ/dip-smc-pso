# Example from: docs\technical\factory_usage_examples.md
# Index: 5
# Runnable: True
# Hash: 62e7c586

from src.controllers.smc.algorithms.super_twisting.config import SuperTwistingSMCConfig

# Configuration for reduced overshoot (Issue #2 resolution)
sta_config = SuperTwistingSMCConfig(
    gains=[8.0, 4.0, 12.0, 6.0, 4.85, 3.43],  # Optimized surface coefficients
    max_force=150.0,
    K1=8.0,              # Proportional-like STA gain
    K2=4.0,              # Integral-like STA gain (reduced for damping)
    power_exponent=0.5,   # Standard STA exponent
    dt=0.001,
    damping_gain=0.0,
    regularization=1e-6
)

controller = create_controller('sta_smc', config=sta_config)

# Verify configuration properties
print(f"K1 gain: {sta_config.K1}")
print(f"Surface gains: {sta_config.get_surface_gains()}")