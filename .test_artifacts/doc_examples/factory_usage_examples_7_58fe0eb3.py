# Example from: docs\technical\factory_usage_examples.md
# Index: 7
# Runnable: True
# Hash: 58fe0eb3

from src.controllers.smc.algorithms.hybrid.config import HybridSMCConfig, HybridMode
from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig
from src.controllers.smc.algorithms.adaptive.config import AdaptiveSMCConfig

# Create sub-configurations
classical_sub = ClassicalSMCConfig(
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
    max_force=150.0,
    dt=0.001,
    boundary_layer=0.02
)

adaptive_sub = AdaptiveSMCConfig(
    gains=[12.0, 10.0, 6.0, 5.0, 2.5],
    max_force=150.0,
    dt=0.001,
    leak_rate=0.01,
    dead_zone=0.05
)

# Create hybrid configuration
hybrid_config = HybridSMCConfig(
    hybrid_mode=HybridMode.CLASSICAL_ADAPTIVE,
    dt=0.001,
    max_force=150.0,
    classical_config=classical_sub,
    adaptive_config=adaptive_sub,
    k1_init=4.0,
    k2_init=0.4,
    gamma1=2.0,
    gamma2=0.5,
    dead_zone=0.05
)

controller = create_controller('hybrid_adaptive_sta_smc', config=hybrid_config)