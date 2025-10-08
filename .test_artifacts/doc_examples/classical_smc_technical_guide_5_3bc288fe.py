# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 5
# Runnable: True
# Hash: 3bc288fe

def _compute_sliding_surface(self, state: np.ndarray) -> float:
    """Compute σ = λ₁θ₁ + λ₂θ₂ + k₁θ̇₁ + k₂θ̇₂"""
    _, theta1, theta2, _, dtheta1, dtheta2 = state
    return (self.lam1 * theta1 + self.lam2 * theta2 +
            self.k1 * dtheta1 + self.k2 * dtheta2)