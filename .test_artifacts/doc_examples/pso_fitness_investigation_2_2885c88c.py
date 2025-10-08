# Example from: docs\testing\reports\2025-09-30\pso_fitness_investigation.md
# Index: 2
# Runnable: False
# Hash: 2885c88c

# State error integration
ise = np.sum((x_b[:, :-1, :] ** 2 * dt_b) * time_mask, axis=(1, 2))
ise_n = self._normalise(ise, self.norm_ise)  # ⚠️  Division by large baseline

# Control effort
u_sq = np.sum((u_b_trunc ** 2 * dt_b) * time_mask, axis=1)
u_n = self._normalise(u_sq, self.norm_u)

# Control slew
du_sq = np.sum((du_trunc ** 2 * dt_b) * time_mask, axis=1)
du_n = self._normalise(du_sq, self.norm_du)

# Sliding variable energy
sigma_sq = np.sum((sigma_b_trunc ** 2 * dt_b) * time_mask, axis=1)
sigma_n = self._normalise(sigma_sq, self.norm_sigma)

# Weighted cost
J = (
    self.weights.state_error * ise_n      # 50.0 * (tiny value)
    + self.weights.control_effort * u_n   # 0.2 * (tiny value)
    + self.weights.control_rate * du_n    # 0.1 * (tiny value)
    + self.weights.stability * sigma_n    # 0.1 * (tiny value)
) + penalty