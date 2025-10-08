# Example from: docs\plant\models_guide.md
# Index: 10
# Runnable: False
# Hash: 0e9ba108

# example-metadata:
# runnable: false

def compute_dynamics_rhs(
    self,
    state: np.ndarray,
    control_input: np.ndarray
) -> np.ndarray:
    """Compute ẍ = M⁻¹(u - C·ẋ - G)."""

    # Extract state components
    position = state[:3]   # [x, theta1, theta2]
    velocity = state[3:]   # [x_dot, theta1_dot, theta2_dot]

    # Compute physics matrices
    M, C, G = self.get_physics_matrices(state)

    # Control vector (force on cart only)
    u = np.array([control_input[0], 0.0, 0.0])

    # Forcing term
    forcing = u - C @ velocity - G

    # Solve for accelerations: M·q̈ = forcing
    accelerations = self.matrix_inverter.solve_linear_system(M, forcing)

    # Construct state derivative
    return np.concatenate([velocity, accelerations])