# Example from: docs\api\phase_4_1_completion_report.md
# Index: 4
# Runnable: False
# Hash: e91b1d0e

# example-metadata:
# runnable: false

Examples
--------
>>> from src.controllers.smc import ClassicalSMC
>>> import numpy as np
>>>
>>> # Create controller
>>> controller = ClassicalSMC(
...     gains=[10, 8, 15, 12, 50, 5],
...     max_force=100,
...     boundary_layer=0.05
... )
>>>
>>> # Initialize
>>> state_vars = controller.initialize_state()
>>> history = controller.initialize_history()
>>>
>>> # Compute control
>>> state = np.array([0, 0.1, 0.05, 0, 0, 0])
>>> output = controller.compute_control(state, state_vars, history)
>>> assert -100 <= output.u <= 100  # Force saturation
>>> assert 'sigma' in output.history  # Telemetry