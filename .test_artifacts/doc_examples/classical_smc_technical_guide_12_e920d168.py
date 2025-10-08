# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 12
# Runnable: True
# Hash: e920d168

from src.controllers import create_controller

# Create via factory (recommended for configurability)
controller = create_controller(
    'classical_smc',
    gains=[10, 8, 15, 12, 50, 5],
    max_force=100.0
)