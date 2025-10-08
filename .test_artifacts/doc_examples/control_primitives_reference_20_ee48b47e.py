# Example from: docs\controllers\control_primitives_reference.md
# Index: 20
# Runnable: True
# Hash: ee48b47e

from src.utils.numerical_stability import safe_divide

# Compute inertia matrix inverse safely
det_M = np.linalg.det(M)
inv_M = safe_divide(1.0, det_M, epsilon=1e-12, fallback=0.0)

# Safe derivative computation
velocity = safe_divide(position - prev_position, dt, epsilon=1e-12)