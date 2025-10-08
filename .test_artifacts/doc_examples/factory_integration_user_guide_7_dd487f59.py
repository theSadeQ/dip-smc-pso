# Example from: docs\factory\factory_integration_user_guide.md
# Index: 7
# Runnable: True
# Hash: dd487f59

from src.controllers.smc.algorithms.hybrid.config import HybridMode

hybrid_config = {
    'gains': [18.0, 12.0, 10.0, 8.0],  # Surface gains only
    'hybrid_mode': HybridMode.CLASSICAL_ADAPTIVE,
    'max_force': 150.0,
    'dt': 0.001
}

controller = create_controller('hybrid_adaptive_sta_smc', **hybrid_config)