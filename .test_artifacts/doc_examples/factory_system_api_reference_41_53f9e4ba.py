# Example from: docs\api\factory_system_api_reference.md
# Index: 41
# Runnable: True
# Hash: 53f9e4ba

# Factory auto-creates sub-configs:
from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig
from src.controllers.smc.algorithms.adaptive.config import AdaptiveSMCConfig
from src.controllers.smc.algorithms.hybrid.config import HybridMode

classical_config = ClassicalSMCConfig(
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    max_force=150.0,
    dt=0.001,
    boundary_layer=0.02
)

adaptive_config = AdaptiveSMCConfig(
    gains=[25.0, 18.0, 15.0, 10.0, 4.0],
    max_force=150.0,
    dt=0.001
)

# Maps to ModularHybridSMC initialization:
from src.controllers.smc.algorithms.hybrid.controller import ModularHybridSMC
controller = ModularHybridSMC(
    HybridAdaptiveSTASMCConfig(
        hybrid_mode=HybridMode.CLASSICAL_ADAPTIVE,
        dt=0.001,
        max_force=150.0,
        classical_config=classical_config,
        adaptive_config=adaptive_config,
        dynamics_model=None  # Hybrid uses sub-controller dynamics
    )
)