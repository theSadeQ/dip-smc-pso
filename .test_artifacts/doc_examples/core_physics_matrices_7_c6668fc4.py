# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 7
# Runnable: True
# Hash: c6668fc4

import numpy as np
from src.plant.core import DIPPhysicsMatrices
from src.plant.configurations import UnifiedDIPConfig

# Setup
config = UnifiedDIPConfig()
physics = DIPPhysicsMatrices(config)

# Define state: [x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂]
state = np.array([0.0, 0.1, -0.05, 0.0, 0.2, -0.1])

# Compute physics matrices
M = physics.compute_inertia_matrix(state)
C = physics.compute_coriolis_matrix(state)
G = physics.compute_gravity_vector(state)

print(f"Inertia Matrix M:\n{M}")
print(f"\nCoriolis Matrix C:\n{C}")
print(f"\nGravity Vector G:\n{G}")