# Example from: docs\issue_11_lyapunov_robustness_resolution.md
# Index: 5
# Runnable: True
# Hash: d7e7dce2

P_sym = 0.5 * (P + P.T)  # Symmetrize
try:
    np.linalg.cholesky(P_sym)  # Definitive positive definiteness test
    is_positive_definite = True
except np.linalg.LinAlgError:
    # Fallback to eigenvalue check with tolerance
    eigenvals_P = linalg.eigvals(P_sym)
    min_eigval = np.min(np.real(eigenvals_P))
    is_positive_definite = (min_eigval > -tolerance)