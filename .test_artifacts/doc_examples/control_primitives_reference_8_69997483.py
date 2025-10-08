# Example from: docs\controllers\control_primitives_reference.md
# Index: 8
# Runnable: True
# Hash: 69997483

from src.controllers.classic_smc import ClassicalSMC

controller = ClassicalSMC(gains=[10, 8, 15, 12, 50, 5], max_force=100, boundary_layer=0.01)
result = controller.compute_control(state, (), {})

# Access via attributes
control_input = result.u
controller_state = result.state
debug_info = result.history

# Backwards-compatible tuple unpacking
u, state, history = result