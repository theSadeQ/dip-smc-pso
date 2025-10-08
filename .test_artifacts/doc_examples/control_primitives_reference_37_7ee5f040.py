# Example from: docs\controllers\control_primitives_reference.md
# Index: 37
# Runnable: True
# Hash: 7ee5f040

# Efficient - no redundant computation
result = controller.compute_control(state, state_vars, history)
if abs(result.sigma) < 0.01:
    print("On sliding surface")

# Inefficient - re-computes sigma
result = controller.compute_control(state, state_vars, history)
sigma = recompute_sliding_surface(state)  # Redundant!