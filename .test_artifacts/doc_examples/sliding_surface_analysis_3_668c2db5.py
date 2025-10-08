# Example from: docs\mathematical_foundations\sliding_surface_analysis.md
# Index: 3
# Runnable: False
# Hash: 668c2db5

def compute_derivative(self, state: np.ndarray, state_dot: np.ndarray) -> float:
    """
    Compute sliding surface derivative ds/dt.

    Args:
        state: Current state vector
        state_dot: State derivative vector

    Returns:
        Surface derivative: ṡ = λ₁θ̈₁ + c₁θ̇₁ + λ₂θ̈₂ + c₂θ̇₂
    """
    if len(state_dot) < 6:
        raise ValueError("State derivative must have at least 6 elements")

    # Extract joint accelerations and velocities
    theta1_dot = state[3]     # Joint 1 velocity
    theta1_ddot = state_dot[3] # Joint 1 acceleration
    theta2_dot = state[5]     # Joint 2 velocity
    theta2_ddot = state_dot[5] # Joint 2 acceleration

    # Surface derivative
    s_dot = (self.lam1 * theta1_ddot + self.k1 * theta1_dot +
             self.lam2 * theta2_ddot + self.k2 * theta2_dot)

    return float(s_dot)