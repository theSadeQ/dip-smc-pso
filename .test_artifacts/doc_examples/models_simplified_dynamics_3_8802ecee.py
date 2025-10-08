# Example from: docs\reference\plant\models_simplified_dynamics.md
# Index: 3
# Runnable: False
# Hash: 8802ecee

# example-metadata:
# runnable: false

# Linearize around upright equilibrium
equilibrium_state = [0, 0, 0, 0, 0, 0]  # Upright, stationary
equilibrium_control = 0.0

A, B = dynamics.compute_linearization(equilibrium_state, equilibrium_control)

print("A matrix (state dynamics):")
print(A)
print("
B matrix (control influence):")
print(B)

# Analyze stability of linearized system
eigenvalues = np.linalg.eigvals(A)
print(f"
Eigenvalues: {eigenvalues}")
print(f"Unstable modes: {sum(np.real(eigenvalues) > 0)}")