# Example from: docs\controllers\mpc_technical_guide.md
# Index: 3
# Runnable: False
# Hash: 892346ad

def _discretize_exact(A_c, B_c, dt):
    """
    Exact ZOH discretization via matrix exponential.

    Theory:
        x(t+Δt) = exp(A_c Δt) x(t) + [∫₀^Δt exp(A_c τ) dτ] B_c u(t)

    Implementation:
        M = [A_c, B_c; 0, 0]
        exp(M Δt) = [A_d, B_d; 0, I]
    """
    n = A_c.shape[0]
    M = np.zeros((n+1, n+1))
    M[:n, :n] = A_c
    M[:n, n:] = B_c

    M_exp = expm(M * dt)  # scipy.linalg.expm

    A_d = M_exp[:n, :n]
    B_d = M_exp[:n, n:].reshape(n, 1)
    return A_d, B_d