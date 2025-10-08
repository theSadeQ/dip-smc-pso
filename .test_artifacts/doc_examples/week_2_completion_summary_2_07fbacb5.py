# Example from: docs\plans\documentation\week_2_completion_summary.md
# Index: 2
# Runnable: True
# Hash: 07fbacb5

if abs(sigma) <= self.dead_zone:
    dK = 0.0  # Freeze inside dead zone
else:
    dK = self.gamma * abs(sigma) - self.leak_rate * (K_prev - self.K_init)

K_new = K_prev + dK * self.dt
K_new = np.clip(K_new, self.K_min, self.K_max)