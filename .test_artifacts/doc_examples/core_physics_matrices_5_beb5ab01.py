# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 5
# Runnable: True
# Hash: beb5ab01

state = np.array([0.1, 0.05, -0.03, 0.2, 0.1, -0.05])
M, C, G = physics.compute_all_matrices(state)

# Verify dynamics equation: M⁻¹(τ - C·q̇ - G) = q̈
tau = np.array([10.0, 0.0, 0.0])  # Control force
q_dot = state[3:]
q_ddot = np.linalg.solve(M, tau - C @ q_dot - G)