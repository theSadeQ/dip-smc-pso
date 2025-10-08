# Example from: docs\plans\documentation\week_2_completion_summary.md
# Index: 1
# Runnable: True
# Hash: c6afe63a

from src.controllers.factory import create_controller

controller = create_controller(
    'classical_smc',
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    config=config
)

result = controller.compute_control(state, (), {})
u = result.u  # Saturated control input