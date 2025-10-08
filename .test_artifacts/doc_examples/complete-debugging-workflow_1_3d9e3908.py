# Example from: docs\mcp-debugging\workflows\complete-debugging-workflow.md
# Index: 1
# Runnable: False
# Hash: 3d9e3908

# example-metadata:
# runnable: false

# Add to src/utils/numerical_stability.py

def safe_matrix_inverse(M: np.ndarray, eps: float = 1e-10) -> np.ndarray:
    """
    Compute matrix inverse with regularization for ill-conditioned matrices.

    Args:
        M: Input matrix
        eps: Regularization parameter

    Returns:
        Regularized inverse
    """
    cond_num = np.linalg.cond(M)
    if cond_num > 1e8:
        # Use SVD-based pseudo-inverse
        return np.linalg.pinv(M, rcond=eps)
    else:
        # Standard inversion with small ridge
        return np.linalg.inv(M + eps * np.eye(M.shape[0]))