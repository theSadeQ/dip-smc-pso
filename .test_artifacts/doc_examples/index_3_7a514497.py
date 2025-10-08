# Example from: docs\controllers\index.md
# Index: 3
# Runnable: True
# Hash: 7a514497

from src.utils.control import saturate, smooth_sign, dead_zone

# Chattering reduction
u_switch = -K * saturate(sigma, epsilon=0.01, method='tanh', slope=3.0)

# Adaptive gain freeze inside dead zone
if abs(sigma) <= dead_zone_threshold:
    dK = 0.0
else:
    dK = gamma * abs(sigma) - leak_rate * (K - K_init)