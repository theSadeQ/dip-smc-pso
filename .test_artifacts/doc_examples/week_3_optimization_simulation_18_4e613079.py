# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 18
# Runnable: True
# Hash: 4e613079

def compute_derivative(self, x, u):
    """Simplified linearized dynamics."""
    θ1, θ2, x_pos, ω1, ω2, v = x

    # Linearized equations (small angle approximation)
    ω1_dot = (g/L1) * θ1 + (u/I1) * x_pos
    ω2_dot = (g/L2) * θ2 + coupling_term
    v_dot = u / m_total

    return np.array([ω1, ω2, v, ω1_dot, ω2_dot, v_dot])