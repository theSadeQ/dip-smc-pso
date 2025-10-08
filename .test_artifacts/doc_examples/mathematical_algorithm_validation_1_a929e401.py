# Example from: docs\mathematical_algorithm_validation.md
# Index: 1
# Runnable: False
# Hash: a929e401

# example-metadata:
# runnable: false

def compute_control(self, state: np.ndarray, target: np.ndarray) -> float:
    """Compute SMC control signal."""
    # Extract state variables
    theta1, theta2, x, theta1_dot, theta2_dot, x_dot = state

    # Compute errors
    e1 = theta1 - target[0]  # Position error pendulum 1
    e2 = theta2 - target[1]  # Position error pendulum 2
    e1_dot = theta1_dot - target[3]  # Velocity error pendulum 1
    e2_dot = theta2_dot - target[4]  # Velocity error pendulum 2

    # Sliding surface: s = λ₁e₁ + λ₂e₂ + ė₁ + ė₂
    s = self.lambda1 * e1 + self.lambda2 * e2 + e1_dot + e2_dot

    # Control law: u = u_eq + u_sw
    u_equivalent = self._compute_equivalent_control(state, target)
    u_switching = -self.K * np.sign(s)

    return u_equivalent + u_switching