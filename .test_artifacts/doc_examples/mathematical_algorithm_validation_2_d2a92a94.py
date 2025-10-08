# Example from: docs\mathematical_algorithm_validation.md
# Index: 2
# Runnable: False
# Hash: d2a92a94

def compute_control(self, state: np.ndarray, target: np.ndarray) -> float:
    """Compute Super-Twisting control signal."""
    # Compute sliding surface
    s = self._compute_sliding_surface(state, target)

    # Super-Twisting control law
    # u₁ = -α₁|s|^(1/2) sign(s)
    u1 = -self.alpha1 * np.power(np.abs(s), 0.5) * np.sign(s)

    # u₂ = ∫(-α₂ sign(s)) dt
    self.integral_term += -self.alpha2 * np.sign(s) * self.dt

    return u1 + self.integral_term