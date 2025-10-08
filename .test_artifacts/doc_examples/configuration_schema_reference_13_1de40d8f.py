# Example from: docs\technical\configuration_schema_reference.md
# Index: 13
# Runnable: True
# Hash: 1de40d8f

from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig
from src.controllers.smc.algorithms.adaptive.config import AdaptiveSMCConfig
from src.controllers.smc.algorithms.hybrid.config import HybridSMCConfig, HybridMode

# Create sub-configurations
classical_sub = ClassicalSMCConfig(
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
    max_force=150.0,
    boundary_layer=0.02,
    dt=0.001
)

adaptive_sub = AdaptiveSMCConfig(
    gains=[12.0, 10.0, 6.0, 5.0, 2.5],
    max_force=150.0,
    leak_rate=0.01,
    dead_zone=0.05,
    dt=0.001
)

# Create hybrid configuration
research_hybrid_config = HybridSMCConfig(
    hybrid_mode=HybridMode.FULL_HYBRID,
    dt=0.001,
    max_force=150.0,
    classical_config=classical_sub,
    adaptive_config=adaptive_sub,
    k1_init=4.0,
    k2_init=0.4,
    gamma1=2.0,
    gamma2=0.5,
    dead_zone=0.05,
    enable_equivalent=True,  # Enable model-based control
    damping_gain=3.0,
    adapt_rate_limit=5.0
)