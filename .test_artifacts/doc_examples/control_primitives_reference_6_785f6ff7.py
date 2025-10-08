# Example from: docs\controllers\control_primitives_reference.md
# Index: 6
# Runnable: True
# Hash: 785f6ff7

from src.utils.control import dead_zone

# Adaptive gain update with dead zone
sigma = compute_sliding_surface(state)

if abs(sigma) <= self.dead_zone:
    dK = 0.0  # Freeze adaptation
else:
    sigma_active = dead_zone(sigma, self.dead_zone)
    dK = self.gamma * abs(sigma_active) - self.leak_rate * (K - K_init)