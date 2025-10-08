# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 27
# Runnable: True
# Hash: dbd5c650

# Hybrid controllers require special handling - factory handles this automatically
controller = create_controller(
    controller_type='hybrid_adaptive_sta_smc',
    gains=[8.0, 6.0, 4.0, 3.0]  # Surface gains only
)

# For advanced configuration:
from src.controllers.smc.algorithms.hybrid.config import HybridSMCConfig, HybridMode
from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig
from src.controllers.smc.algorithms.adaptive.config import AdaptiveSMCConfig

classical_sub = ClassicalSMCConfig(
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
    max_force=150.0,
    dt=0.001,
    boundary_layer=0.02
)

adaptive_sub = AdaptiveSMCConfig(
    gains=[12.0, 10.0, 6.0, 5.0, 2.5],
    max_force=150.0,
    dt=0.001
)

hybrid_config = HybridSMCConfig(
    hybrid_mode=HybridMode.CLASSICAL_ADAPTIVE,
    dt=0.001,
    max_force=150.0,
    classical_config=classical_sub,
    adaptive_config=adaptive_sub
)

controller = create_controller('hybrid_adaptive_sta_smc', config=hybrid_config)