# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 4
# Runnable: True
# Hash: 1c427829

# Complex hybrid controller with sub-configurations
controller = create_controller(
    controller_type='hybrid_adaptive_sta_smc',
    gains=[8.0, 6.0, 4.0, 3.0]  # Surface gains only
)

# Advanced hybrid configuration with mode specification
from src.controllers.smc.algorithms.hybrid.config import HybridSMCConfig, HybridMode

hybrid_config = HybridSMCConfig(
    hybrid_mode=HybridMode.CLASSICAL_ADAPTIVE,
    dt=0.001,
    max_force=150.0,
    k1_init=4.0,
    k2_init=0.4,
    gamma1=2.0,
    gamma2=0.5,
    dead_zone=0.05
)

controller = create_controller('hybrid_adaptive_sta_smc', config=hybrid_config)