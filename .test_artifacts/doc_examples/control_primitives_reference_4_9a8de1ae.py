# Example from: docs\controllers\control_primitives_reference.md
# Index: 4
# Runnable: True
# Hash: 9a8de1ae

from src.utils.control import smooth_sign

# Continuous sign approximation
sigma = compute_sliding_surface(state)
switch_signal = -K * smooth_sign(sigma, epsilon=0.02)