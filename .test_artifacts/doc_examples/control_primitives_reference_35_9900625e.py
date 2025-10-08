# Example from: docs\controllers\control_primitives_reference.md
# Index: 35
# Runnable: True
# Hash: 9900625e

# Clear and self-documenting
result = controller.compute_control(state, state_vars, history)
control_input = result.u
sliding_surface = result.sigma  # Adaptive/Hybrid SMC only