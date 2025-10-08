# Example from: docs\issue_11_lyapunov_robustness_resolution.md
# Index: 7
# Runnable: False
# Hash: ceffc7c2

# example-metadata:
# runnable: false

def _solve_lyapunov_svd(self, A, Q, regularizer):
    # Vectorize: (I ⊗ A^T + A^T ⊗ I) vec(P) = -vec(Q)
    n = A.shape[0]
    I_n = np.eye(n)
    K = np.kron(I_n, A.T) + np.kron(A.T, I_n)

    # Regularize Kronecker matrix
    K_reg = regularizer.regularize_matrix(K)

    # Solve and reshape
    q_vec = -Q.flatten()
    p_vec = np.linalg.solve(K_reg, q_vec)  # or lstsq as ultimate fallback
    P = p_vec.reshape((n, n))

    return 0.5 * (P + P.T)  # Symmetrize