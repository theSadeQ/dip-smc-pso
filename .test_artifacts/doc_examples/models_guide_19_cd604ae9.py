# Example from: docs\plant\models_guide.md
# Index: 19
# Runnable: True
# Hash: cd604ae9

from src.plant.models.lowrank import LowRankDIPDynamics, LowRankDIPConfig

# Use low-rank model for fast linearization
config = LowRankDIPConfig.create_default()
dynamics = LowRankDIPDynamics(config)

# Get linearized system around upright equilibrium
A, B = dynamics.get_linearized_system(equilibrium_point="upright")

# Analyze controllability
from scipy.linalg import ctrb
C = ctrb(A, B)
rank = np.linalg.matrix_rank(C)

if rank == A.shape[0]:
    print("System is controllable ✓")
else:
    print(f"System rank deficient: {rank}/{A.shape[0]}")

# Compute eigenvalues
eigenvalues = np.linalg.eigvals(A)
print(f"Open-loop poles: {eigenvalues}")

# Check for unstable modes
unstable = np.any(np.real(eigenvalues) > 0)
print(f"Unstable: {unstable}")