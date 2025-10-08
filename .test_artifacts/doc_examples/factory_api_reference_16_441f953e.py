# Example from: docs\factory\factory_api_reference.md
# Index: 16
# Runnable: True
# Hash: 441f953e

from src.controllers.smc.algorithms.hybrid.config import HybridMode

controller = create_controller(
    'hybrid_adaptive_sta_smc',
    gains=[18.0, 12.0, 10.0, 8.0],
    hybrid_mode=HybridMode.CLASSICAL_ADAPTIVE,
    max_force=150.0,
    dt=0.001
)