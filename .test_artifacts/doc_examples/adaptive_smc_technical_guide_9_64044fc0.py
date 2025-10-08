# Example from: docs\controllers\adaptive_smc_technical_guide.md
# Index: 9
# Runnable: True
# Hash: 64044fc0

from src.controllers import create_controller

# Create via factory
controller = create_controller(
    'adaptive_smc',
    gains=[10, 8, 15, 12, 0.5],
    dt=0.01,
    max_force=100.0
)