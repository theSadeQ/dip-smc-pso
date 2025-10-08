# Example from: docs\controllers\control_primitives_reference.md
# Index: 29
# Runnable: True
# Hash: cc2c3928

from src.utils.numerical_stability import safe_norm, safe_normalize

# Gradient descent with safe normalization
gradient = compute_gradient(params)
gradient_norm = safe_norm(gradient, min_norm=1e-10)
unit_gradient = safe_normalize(gradient, min_norm=1e-10)

params_new = params - step_size * unit_gradient