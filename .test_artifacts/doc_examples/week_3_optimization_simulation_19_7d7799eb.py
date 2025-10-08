# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 19
# Runnable: False
# Hash: 7d7799eb

def compute_mass_matrix(self, q):
    """
    M(q) ∈ ℝ³ˣ³ - Configuration-dependent mass matrix

    Derivation from kinetic energy:
    T = ½q̇ᵀM(q)q̇
    """
    θ1, θ2, x = q

    m1, m2, L1, L2 = self.params

    # Diagonal terms
    M11 = self.I1 + m1*L1**2 + m2*(L1**2 + L2**2 + 2*L1*L2*np.cos(θ2))
    M22 = self.I2 + m2*L2**2
    M33 = self.m_total

    # Off-diagonal coupling terms
    M12 = m2*(L2**2 + L1*L2*np.cos(θ2))
    M13 = (m1 + m2)*L1*np.cos(θ1) + m2*L2*np.cos(θ2)
    M23 = m2*L2*np.cos(θ2)

    M = np.array([
        [M11, M12, M13],
        [M12, M22, M23],
        [M13, M23, M33]
    ])

    return M