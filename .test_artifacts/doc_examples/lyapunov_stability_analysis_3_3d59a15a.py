# Example from: docs\theory\lyapunov_stability_analysis.md
# Index: 3
# Runnable: True
# Hash: 3d59a15a

import numpy as np

def validate_reaching_time_bound(s0, eta, D_max, L, M_inv, B):
    """
    Validate finite-time reaching bound for classical SMC.

    Args:
        s0: Initial sliding surface value
        eta: Switching gain
        D_max: Maximum disturbance magnitude
        L: Sliding surface gain vector [0, k1, k2]
        M_inv: Inverse mass matrix
        B: Control input matrix [1, 0, 0]

    Returns:
        dict: Reaching time bound validation
    """
    # Controllability scalar
    b = float(L.T @ M_inv @ B)

    # Disturbance bound in control direction
    L_M_inv_norm = np.linalg.norm(L.T @ M_inv)

    # Reaching law parameter
    gamma = b * eta - L_M_inv_norm * D_max

    # Theoretical reaching time bound
    if gamma > 0:
        t_r_bound = abs(s0) / gamma
        valid = True
    else:
        t_r_bound = np.inf
        valid = False

    # Lyapunov function initial value
    V0 = 0.5 * s0**2

    return {
        "s0": float(s0),
        "b_controllability": float(b),
        "L_M_inv_norm": float(L_M_inv_norm),
        "gamma": float(gamma),
        "t_r_bound": float(t_r_bound),
        "V0": float(V0),
        "valid_reaching_condition": valid,
        "eta_required": float(L_M_inv_norm * D_max / b),
    }

# Example usage:
# M_inv = np.linalg.inv(M)  # From dynamics
# L = np.array([0, 15, 12])
# B = np.array([1, 0, 0])
# result = validate_reaching_time_bound(s0=0.5, eta=50, D_max=5, L=L, M_inv=M_inv, B=B)
# Expected: valid_reaching_condition=True, t_r_bound < 1.0 second