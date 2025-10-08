# Example from: docs\controllers\index.md
# Index: 1
# Runnable: True
# Hash: c196c1d2

from src.controllers.factory import create_controller

controller = create_controller(
    'classical_smc',
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    config=config
)