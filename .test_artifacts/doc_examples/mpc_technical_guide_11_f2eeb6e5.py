# Example from: docs\controllers\mpc_technical_guide.md
# Index: 11
# Runnable: False
# Hash: f2eeb6e5

# example-metadata:
# runnable: false

def _numeric_linearize_continuous(dyn, x_eq, u_eq, eps=1e-6):
    """
    Central finite difference Jacobian computation.

    Key Innovation: Adaptive perturbation prevents numerical issues.
    """
    x_eq = np.asarray(x_eq, dtype=float)
    n = x_eq.size
    f0 = _call_f(dyn, x_eq, u_eq)
    A = np.zeros((n, n))

    for i in range(n):
        # Adaptive step: δ ∝ |x_eq[i]| with floor
        delta = max(eps, 1e-4 * max(abs(x_eq[i]), 1.0))
        delta = max(delta, 1e-12)  # Critical: prevent division by zero

        dx = np.zeros(n)
        dx[i] = delta

        f_plus = _call_f(dyn, x_eq + dx, u_eq)
        f_minus = _call_f(dyn, x_eq - dx, u_eq)

        # Central difference: O(δ²) accuracy
        A[:, i] = (f_plus - f_minus) / (2.0 * delta)

    # Input Jacobian B
    du = max(eps, 1e-4 * max(abs(u_eq), 1.0))
    du = max(du, 1e-12)

    f_plus = _call_f(dyn, x_eq, u_eq + du)
    f_minus = _call_f(dyn, x_eq, u_eq - du)
    B = ((f_plus - f_minus) / (2.0 * du)).reshape(n, 1)

    return A, B