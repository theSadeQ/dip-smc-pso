# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 4
# Runnable: True
# Hash: f6ae5ddf

# Upright equilibrium
state_upright = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
G_upright = physics.compute_gravity_vector(state_upright)
assert np.allclose(G_upright, 0.0)

# Small perturbation
state_perturbed = np.array([0.0, 0.1, 0.05, 0.0, 0.0, 0.0])
G_perturbed = physics.compute_gravity_vector(state_perturbed)
assert G_perturbed[1] < 0  # Restoring torque on link 1
assert G_perturbed[2] < 0  # Restoring torque on link 2