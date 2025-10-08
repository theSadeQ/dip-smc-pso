# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 12
# Runnable: True
# Hash: d4598a8c

from src.controllers.factory import create_controller

# Create via factory (recommended)
controller = create_controller(
    'hybrid_adaptive_sta_smc',
    gains=[77.6216, 44.449, 17.3134, 14.25],
    max_force=100.0
)