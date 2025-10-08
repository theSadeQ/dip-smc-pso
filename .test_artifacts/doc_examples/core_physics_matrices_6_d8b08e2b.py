# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 6
# Runnable: True
# Hash: d8b08e2b

from src.plant.core import SimplifiedDIPPhysicsMatrices

simplified_physics = SimplifiedDIPPhysicsMatrices(config)
M_simp = simplified_physics.compute_inertia_matrix(state)

# Compare with full physics
M_full = physics.compute_inertia_matrix(state)
relative_error = np.linalg.norm(M_simp - M_full) / np.linalg.norm(M_full)
print(f"Inertia matrix error: {relative_error * 100:.2f}%")  # Typically 2-5%