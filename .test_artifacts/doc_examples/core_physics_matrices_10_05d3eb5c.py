# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 10
# Runnable: False
# Hash: 05d3eb5c

def verify_inertia_matrix_properties(physics, state):
    """Verify mathematical properties of M(q)."""
    M = physics.compute_inertia_matrix(state)

    # 1. Symmetry
    symmetry_error = np.linalg.norm(M - M.T)
    print(f"Symmetry error: {symmetry_error:.2e}")

    # 2. Positive definiteness
    eigenvalues = np.linalg.eigvals(M)
    min_eigenvalue = np.min(eigenvalues)
    print(f"Minimum eigenvalue: {min_eigenvalue:.6f}")
    assert min_eigenvalue > 0, "M(q) must be positive definite"

    # 3. Condition number
    cond = np.linalg.cond(M)
    print(f"Condition number: {cond:.2e}")
    if cond > 1e10:
        print("Warning: Ill-conditioned matrix, consider regularization")

verify_inertia_matrix_properties(physics, state)