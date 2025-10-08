# Example from: docs\controllers\adaptive_smc_technical_guide.md
# Index: 4
# Runnable: True
# Hash: 152b0efd

def compute_sliding_surface(state):
    """σ = k₁(θ̇₁ + λ₁θ₁) + k₂(θ̇₂ + λ₂θ₂)"""
    x, theta1, theta2, x_dot, theta1_dot, theta2_dot = state

    sigma = (self.k1 * (theta1_dot + self.lam1 * theta1) +
             self.k2 * (theta2_dot + self.lam2 * theta2))

    return sigma