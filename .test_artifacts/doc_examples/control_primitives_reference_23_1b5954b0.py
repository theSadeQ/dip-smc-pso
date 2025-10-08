# Example from: docs\controllers\control_primitives_reference.md
# Index: 23
# Runnable: True
# Hash: 1b5954b0

from src.utils.numerical_stability import safe_sqrt

# Finite-time STA control law: u = -K1 * sqrt(|σ|) * sign(σ)
u_proportional = -K1 * safe_sqrt(abs(sigma), min_value=1e-15) * smooth_sign(sigma)