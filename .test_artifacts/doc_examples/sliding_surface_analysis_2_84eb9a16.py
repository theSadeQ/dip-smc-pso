# Example from: docs\mathematical_foundations\sliding_surface_analysis.md
# Index: 2
# Runnable: False
# Hash: 84eb9a16

# example-metadata:
# runnable: false

def compute(self, state: np.ndarray) -> float:
    """
    Compute linear sliding surface value.

    Args:
        state: [x, x_dot, theta1, theta1_dot, theta2, theta2_dot]

    Returns:
        Sliding surface value: s = lam1*theta1_dot + k1*theta1 + lam2*theta2_dot + k2*theta2
    """
    if len(state) < 6:
        raise ValueError("State must have at least 6 elements for double-inverted pendulum")

    # Extract joint angles and velocities (reference is upright: theta=0)
    theta1 = state[2]      # Joint 1 angle error
    theta1_dot = state[3]  # Joint 1 velocity error
    theta2 = state[4]      # Joint 2 angle error
    theta2_dot = state[5]  # Joint 2 velocity error

    # Linear sliding surface: s = λ₁ė₁ + c₁e₁ + λ₂ė₂ + c₂e₂
    s = (self.lam1 * theta1_dot + self.k1 * theta1 +
         self.lam2 * theta2_dot + self.k2 * theta2)

    return float(s)