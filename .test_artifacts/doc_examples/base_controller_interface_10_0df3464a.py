# Example from: docs\reference\controllers\base_controller_interface.md
# Index: 10
# Runnable: False
# Hash: 0df3464a

# example-metadata:
# runnable: false

from src.controllers.base.controller_interface import ControllerProtocol
import numpy as np

def simulate(controller: ControllerProtocol, duration: float):
    """Simulate with any controller implementing the protocol."""

    # Initialize
    state_vars = {}
    history = controller.initialize_history()

    # Simulation loop
    state = np.array([0.1, 0.0, 0.05, 0.1, 0.02, 0.05])

    for t in np.arange(0, duration, 0.01):
        u, state_vars, history = controller.compute_control(
            state, state_vars, history
        )
        # ... integrate dynamics

    return history

# Works with ANY controller implementing ControllerProtocol
from src.controllers import ClassicalSMC, AdaptiveSMC

classical = ClassicalSMC(gains=[10, 8, 15, 12, 50, 0.01])
adaptive = AdaptiveSMC(gains=[10, 8, 15, 12, 0.5])

result_classical = simulate(classical, duration=5.0)
result_adaptive = simulate(adaptive, duration=5.0)