# Example from: docs\testing\reports\2025-09-30\technical_analysis.md
# Index: 9
# Runnable: False
# Hash: 76b09bb0

# example-metadata:
# runnable: false

def verify_lyapunov_stability(A, Q):
    """Verify Lyapunov stability with robust numerical methods."""

    # Standard Lyapunov equation: A^T P + P A + Q = 0
    try:
        P = scipy.linalg.solve_lyapunov(A.T, -Q)
    except LinAlgError:
        # Fallback to regularized solution
        A_reg = A + np.eye(A.shape[0]) * 1e-8
        P = scipy.linalg.solve_lyapunov(A_reg.T, -Q)

    # Verify positive definiteness
    eigenvals = np.linalg.eigvals(P)
    if np.any(eigenvals <= 0):
        return False, f"Non-positive eigenvalues: {eigenvals[eigenvals <= 0]}"

    # Verify stability condition
    stability_matrix = A.T @ P + P @ A + Q
    max_eigenval = np.max(np.real(np.linalg.eigvals(stability_matrix)))

    if max_eigenval > 1e-10:  # Numerical tolerance
        return False, f"Stability violated: max eigenvalue {max_eigenval}"

    return True, "Stable"