# Example from: docs\factory\README.md
# Index: 1
# Runnable: True
# Hash: 61017573

from src.controllers.factory import create_controller

# Classical SMC
controller = create_controller(
    'classical_smc',
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
)

# Adaptive SMC
controller = create_controller(
    'adaptive_smc',
    gains=[25.0, 18.0, 15.0, 10.0, 4.0]
)

# Super-Twisting SMC
controller = create_controller(
    'sta_smc',
    gains=[25.0, 15.0, 20.0, 12.0, 8.0, 6.0]
)