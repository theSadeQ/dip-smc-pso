# Example from: docs\controllers\mpc_technical_guide.md
# Index: 2
# Runnable: False
# Hash: 04bf4b8c

# example-metadata:
# runnable: false

def _numeric_linearize_continuous(dyn, x_eq, u_eq, eps=1e-6):
    """
    Compute Jacobian matrices A, B around (x_eq, u_eq).

    Returns:
        A: ∂f/∂x ∈ ℝⁿˣⁿ
        B: ∂f/∂u ∈ ℝⁿˣᵐ
    """
    n = x_eq.size
    A = np.zeros((n, n))

    for i in range(n):
        δ = max(eps, 1e-4 * max(abs(x_eq[i]), 1.0))
        δ = max(δ, 1e-12)  # Prevent division by zero

        f_plus = dyn.f(x_eq + δ*e_i, u_eq)
        f_minus = dyn.f(x_eq - δ*e_i, u_eq)
        A[:, i] = (f_plus - f_minus) / (2*δ)

    δ_u = max(eps, 1e-4 * max(abs(u_eq), 1.0))
    δ_u = max(δ_u, 1e-12)

    B = (dyn.f(x_eq, u_eq + δ_u) - dyn.f(x_eq, u_eq - δ_u)) / (2*δ_u)
    return A, B