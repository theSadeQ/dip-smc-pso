# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 1
# Runnable: False
# Hash: 0b2e440d

# example-metadata:
# runnable: false

def total_energy(self, state):
    """
    Compute total mechanical energy.

    Returns:
        E = T(q̇) + V(q)  (scalar)
    """
    q = state[:3]   # [x, θ₁, θ₂]
    qdot = state[3:] # [ẋ, θ̇₁, θ̇₂]

    # Kinetic energy
    T = 0.5 * (
        m_c * qdot[0]**2 +
        I_1 * qdot[1]**2 +
        I_2 * qdot[2]**2 +
        # Cross terms from coupled dynamics
        ...
    )

    # Potential energy (gravity)
    V = (
        -m_1 * g * L_1 * np.cos(q[1]) +
        -m_2 * g * (L_1 * np.cos(q[1]) + L_2 * np.cos(q[2]))
    )

    return T + V