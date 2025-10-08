# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 2
# Runnable: True
# Hash: e89472f4

from src.plant.core import DIPPhysicsMatrices
from src.plant.configurations import UnifiedDIPConfig

config = UnifiedDIPConfig()
physics = DIPPhysicsMatrices(config)

state = np.array([0.1, 0.05, -0.03, 0.0, 0.0, 0.0])
M = physics.compute_inertia_matrix(state)

# Verify symmetry
assert np.allclose(M, M.T)

# Verify positive definiteness
eigenvalues = np.linalg.eigvals(M)
assert np.all(eigenvalues > 0)