# Example from: docs\guides\api\controllers.md
# Index: 7
# Runnable: True
# Hash: b2fc45f4

from src.controllers import create_controller

controller = create_controller(
    'classical_smc',
    config=config.controllers.classical_smc
)