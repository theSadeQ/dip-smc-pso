# Example from: docs\controllers\mpc_technical_guide.md
# Index: 12
# Runnable: False
# Hash: 8810793e

# example-metadata:
# runnable: false

def _discretize_exact(Ac, Bc, dt):
    """
    Zero-order hold discretization via matrix exponential.

    Mathematical Foundation:
        x(t+Δt) = exp(A Δt) x(t) + [∫₀^Δt exp(A τ) dτ] B u(t)

    Block Matrix Trick:
        exp([A, B; 0, 0] Δt) = [A_d, B_d; 0, I]
    """
    n = Ac.shape[0]
    M = np.zeros((n+1, n+1))
    M[:n, :n] = Ac          # Top-left: A
    M[:n, n:] = Bc          # Top-right: B
    # Bottom row remains zero

    Md = expm(M * dt)       # scipy.linalg.expm

    Ad = Md[:n, :n]         # Extract A_d
    Bd = Md[:n, n:].reshape(n, 1)  # Extract B_d

    return Ad, Bd