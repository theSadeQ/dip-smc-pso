# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 3
# Runnable: False
# Hash: 5dc1ac93

def _compute_sliding_surface(self, state: np.ndarray) -> float:
    """Compute unified sliding surface with dual formulation support.

    Mathematical Implementation:
    s = c1*(θ̇₁ + λ₁*θ₁) + c2*(θ̇₂ + λ₂*θ₂) + cart_term

    or (relative mode):
    s = c1*(θ̇₁ + λ₁*θ₁) + c2*((θ̇₂-θ̇₁) + λ₂*(θ₂-θ₁)) + cart_term
    """
    x, th1, th2, xdot, th1dot, th2dot = state

    if self.use_relative_surface:
        rel_dot = th2dot - th1dot
        rel_ang = th2 - th1
        pendulum_term = self.c1 * (th1dot + self.lambda1 * th1) + \
                       self.c2 * (rel_dot + self.lambda2 * rel_ang)
    else:
        pendulum_term = self.c1 * (th1dot + self.lambda1 * th1) + \
                       self.c2 * (th2dot + self.lambda2 * th2)

    cart_term = self.cart_gain * (xdot + self.cart_lambda * x)
    return float(-(pendulum_term - cart_term))