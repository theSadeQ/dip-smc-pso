# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 21
# Runnable: False
# Hash: a8bf3c95

# example-metadata:
# runnable: false

def compute_gravity(self, q):
    """
    G(q) - Potential energy gradient

    V = -m₁gL₁cosθ₁ - m₂g(L₁cosθ₁ + L₂cosθ₂)
    Gᵢ = ∂V/∂qᵢ
    """
    θ1, θ2, x = q

    G1 = -(m1 + m2)*g*L1*np.sin(θ1) - m2*g*L2*np.sin(θ2)
    G2 = -m2*g*L2*np.sin(θ2)
    G3 = 0.0

    return np.array([G1, G2, G3])