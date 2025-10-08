# Example from: docs\controllers\factory_system_guide.md
# Index: 24
# Runnable: True
# Hash: 75354416

# Hybrid controller requires special handling - sub-configs
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

controller = create_controller(
    controller_type='hybrid_adaptive_sta_smc',
    config=None,  # Not used for hybrid
    gains=[18.0, 12.0, 10.0, 8.0]  # [k1, k2, λ1, λ2]
)