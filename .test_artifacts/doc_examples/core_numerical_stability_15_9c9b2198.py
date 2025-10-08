# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 15
# Runnable: True
# Hash: 9c9b2198

from src.plant.core import MatrixInverter, DIPPhysicsMatrices
from src.plant.configurations import UnifiedDIPConfig

config = UnifiedDIPConfig()
physics = DIPPhysicsMatrices(config)
inverter = MatrixInverter()

# State and control
state = np.array([0.1, 0.05, -0.03, 0.2, 0.1, -0.05])
tau = np.array([10.0, 0.0, 0.0])

# Compute physics matrices
M, C, G = physics.compute_all_matrices(state)
q_dot = state[3:]

# Solve M(q)q̈ = τ - C·q̇ - G for q̈
forcing = tau - C @ q_dot - G
q_ddot = inverter.solve_linear_system(M, forcing)

print(f"Accelerations: {q_ddot}")