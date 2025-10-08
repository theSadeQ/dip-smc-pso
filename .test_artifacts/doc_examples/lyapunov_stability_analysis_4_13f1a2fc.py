# Example from: docs\theory\lyapunov_stability_analysis.md
# Index: 4
# Runnable: True
# Hash: 13f1a2fc

import numpy as np

def validate_super_twisting_gains(K1, K2, L, lambda_min):
    """
    Validate super-twisting gain selection for finite-time stability.

    Args:
        K1: First algorithmic gain (continuous term)
        K2: Second algorithmic gain (discontinuous term)
        L: Lipschitz constant of disturbance derivative
        lambda_min: Minimum eigenvalue of the system

    Returns:
        dict: Gain validation results
    """
    # Stability condition 1: K1 > L / lambda_min
    condition1 = K1 > (L / lambda_min)

    # Stability condition 2: K2 > K1 * L / (2 * (lambda_min - L))
    if lambda_min > L:
        K2_min = (K1 * L) / (2 * (lambda_min - L))
        condition2 = K2 > K2_min
    else:
        K2_min = np.inf
        condition2 = False

    # Additional robustness condition: K1 > K2 for practical implementations
    condition3 = K1 > K2

    # Lyapunov matrix P positive definiteness
    # P = [[2*K2, -1], [-1, rho]] > 0
    # Requires: 2*K2 > 0 and det(P) = 2*K2*rho - 1 > 0
    # Choose rho = 1/(K2) gives det = 1 > 0
    rho = 1.0 / K2 if K2 > 0 else 0
    P = np.array([[2*K2, -1], [-1, rho]])

    try:
        eigs_P = np.linalg.eigvalsh(P)
        P_positive_definite = np.all(eigs_P > 0)
    except:
        eigs_P = [np.nan, np.nan]
        P_positive_definite = False

    all_conditions_met = condition1 and condition2 and condition3 and P_positive_definite

    return {
        "K1": float(K1),
        "K2": float(K2),
        "L": float(L),
        "lambda_min": float(lambda_min),
        "K2_min_required": float(K2_min),
        "condition1_K1_sufficiently_large": bool(condition1),
        "condition2_K2_sufficiently_large": bool(condition2),
        "condition3_K1_greater_K2": bool(condition3),
        "Lyapunov_matrix_P": P.tolist(),
        "P_eigenvalues": [float(e) for e in eigs_P],
        "P_positive_definite": bool(P_positive_definite),
        "all_stability_conditions_met": bool(all_conditions_met),
    }

# Example usage:
# result = validate_super_twisting_gains(K1=15, K2=10, L=2.0, lambda_min=5.0)
# Expected: all_stability_conditions_met=True