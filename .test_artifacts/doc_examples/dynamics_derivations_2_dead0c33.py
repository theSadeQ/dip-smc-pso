# Example from: docs\mathematical_foundations\dynamics_derivations.md
# Index: 2
# Runnable: False
# Hash: dead0c33

def safe_invert_mass_matrix(M, regularization=1e-10):
    """Invert mass matrix with regularization."""
    # Add small diagonal term for numerical stability
    M_reg = M + regularization * np.eye(M.shape[0])

    # Condition number check
    cond = np.linalg.cond(M_reg)
    if cond > 1e6:
        raise ValueError(f"Ill-conditioned mass matrix: κ = {cond:.2e}")

    # Solve using Cholesky (M is symmetric positive definite)
    try:
        M_inv = np.linalg.inv(M_reg)
    except np.linalg.LinAlgError:
        # Fallback: pseudo-inverse
        M_inv = np.linalg.pinv(M_reg)

    return M_inv