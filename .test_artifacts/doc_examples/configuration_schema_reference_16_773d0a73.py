# Example from: docs\technical\configuration_schema_reference.md
# Index: 16
# Runnable: True
# Hash: 773d0a73

from src.controllers.factory import create_controller
from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig
from src.controllers.smc.algorithms.super_twisting.config import SuperTwistingSMCConfig
from src.controllers.smc.algorithms.adaptive.config import AdaptiveSMCConfig

# Classical SMC - Production configuration
classical_config = ClassicalSMCConfig(
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
    max_force=150.0,
    boundary_layer=0.02,
    dt=0.001,
    switch_method="tanh",
    regularization=1e-8
)

# STA SMC - Issue #2 optimized configuration
sta_config = SuperTwistingSMCConfig(
    gains=[8.0, 4.0, 12.0, 6.0, 4.85, 3.43],
    max_force=150.0,
    dt=0.001,
    power_exponent=0.5,
    boundary_layer=0.01,
    damping_gain=0.0
)

# Adaptive SMC - Robust configuration
adaptive_config = AdaptiveSMCConfig(
    gains=[12.0, 10.0, 6.0, 5.0, 2.5],
    max_force=150.0,
    dt=0.001,
    leak_rate=0.01,
    dead_zone=0.05,
    adapt_rate_limit=10.0,
    K_min=0.1,
    K_max=100.0,
    boundary_layer=0.01
)

# Create controllers with validated configurations
classical_controller = create_controller('classical_smc', config=classical_config)
sta_controller = create_controller('sta_smc', config=sta_config)
adaptive_controller = create_controller('adaptive_smc', config=adaptive_config)