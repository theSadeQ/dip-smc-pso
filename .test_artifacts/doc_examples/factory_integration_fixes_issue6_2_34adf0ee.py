# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 2
# Runnable: True
# Hash: 34adf0ee

# Optimized configuration for reduced overshoot (Issue #2 resolution)
controller = create_controller(
    controller_type='sta_smc',
    gains=[8.0, 4.0, 12.0, 6.0, 4.85, 3.43]  # Tuned surface coefficients
)

# Custom STA configuration
from src.controllers.smc.algorithms.super_twisting.config import SuperTwistingSMCConfig

sta_config = SuperTwistingSMCConfig(
    gains=[8.0, 4.0, 12.0, 6.0, 4.85, 3.43],
    max_force=150.0,
    K1=4.0,
    K2=0.4,
    power_exponent=0.5,
    dt=0.001
)

controller = create_controller('sta_smc', config=sta_config)