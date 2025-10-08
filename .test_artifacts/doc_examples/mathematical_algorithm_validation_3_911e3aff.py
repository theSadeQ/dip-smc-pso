# Example from: docs\mathematical_algorithm_validation.md
# Index: 3
# Runnable: True
# Hash: 911e3aff

def update_parameters(self, state: np.ndarray, s: float) -> None:
    """Update adaptive parameters."""
    # Regressor vector Φ(x, ẋ)
    phi = self._compute_regressor(state)

    # Adaptive law: θ̇ = γ Φ(x, ẋ) s
    self.theta_hat += self.gamma * phi * s * self.dt

    # Parameter bounds enforcement
    self.theta_hat = np.clip(self.theta_hat, self.theta_min, self.theta_max)