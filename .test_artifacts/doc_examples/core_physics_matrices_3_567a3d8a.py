# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 3
# Runnable: True
# Hash: 567a3d8a

state = np.array([0.1, 0.05, -0.03, 0.2, 0.1, -0.05])
C = physics.compute_coriolis_matrix(state)

# Extract velocity-dependent terms
theta1, theta2 = state[1], state[2]
theta1_dot, theta2_dot = state[4], state[5]

# Verify friction is on diagonal
assert C[0, 0] == config.cart_friction
assert C[1, 1] >= config.joint1_friction  # May include velocity terms