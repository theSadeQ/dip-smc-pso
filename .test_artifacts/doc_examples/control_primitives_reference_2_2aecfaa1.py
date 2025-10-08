# Example from: docs\controllers\control_primitives_reference.md
# Index: 2
# Runnable: True
# Hash: 2aecfaa1

from src.utils.control import saturate

# Classical SMC control law
sigma = lambda1 * theta1 + lambda2 * theta2 + k1 * dtheta1 + k2 * dtheta2
u_switch = -K * saturate(sigma, epsilon=0.01, method='tanh', slope=3.0)
u_damping = -kd * saturate(sigma, epsilon=0.01, method='tanh', slope=3.0)
u = u_switch + u_damping