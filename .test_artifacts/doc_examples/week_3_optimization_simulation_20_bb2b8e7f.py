# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 20
# Runnable: False
# Hash: bb2b8e7f

def compute_coriolis(self, q, qdot):
    """
    C(q,q̇)q̇ - Velocity-dependent forces

    Christoffel symbols of second kind:
    Cᵢⱼₖ = ½(∂Mᵢⱼ/∂qₖ + ∂Mᵢₖ/∂qⱼ - ∂Mⱼₖ/∂qᵢ)
    """
    θ1, θ2, x = q
    ω1, ω2, v = qdot

    # Centrifugal force from θ2 rotation
    C12 = -m2*L1*L2*np.sin(θ2)*ω2
    C21 = m2*L1*L2*np.sin(θ2)*ω1

    # Coupling terms
    C13 = -(m1 + m2)*L1*np.sin(θ1)*ω1 - m2*L2*np.sin(θ2)*ω2

    C = np.array([
        [0, C12, C13],
        [C21, 0, 0],
        [0, 0, 0]
    ])

    return C @ qdot