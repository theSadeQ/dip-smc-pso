# Example from: docs\theory\pso_algorithm_foundations.md
# Index: 2
# Runnable: True
# Hash: fdfa48b0

import numpy as np

def analyze_pso_stability(w: float, c1: float, c2: float) -> dict:
    """
    Analyze stability of PSO parameters via eigenvalue analysis.

    Validates Theorem 2.1 by computing eigenvalues of the system matrix
    and checking if they lie inside the unit circle.

    Parameters
    ----------
    w : float
        Inertia weight
    c1 : float
        Cognitive coefficient
    c2 : float
        Social coefficient

    Returns
    -------
    dict
        Stability analysis results with eigenvalues and stability status
    """
    # 1D system matrix for deterministic PSO (r1=r2=1)
    # A = [[1 - (c1+c2), 1], [-(c1+c2), w]]
    phi = c1 + c2

    A = np.array([
        [1 - phi, 1],
        [-phi, w]
    ])

    # Compute eigenvalues
    eigenvalues = np.linalg.eigvals(A)
    eigenvalue_magnitudes = np.abs(eigenvalues)

    # Stability check: all |lambda| < 1
    stable = np.all(eigenvalue_magnitudes < 1.0)

    # Theoretical stability condition
    condition1 = (0 < w < 1)
    condition2 = (0 < phi < 2 * (1 + w))

    theoretical_stable = condition1 and condition2

    # Constriction factor (if applicable)
    if phi > 4:
        chi = 2.0 / abs(2 - phi - np.sqrt(phi**2 - 4*phi))
        constriction_stable = True
    else:
        chi = None
        constriction_stable = False

    return {
        "w": float(w),
        "c1": float(c1),
        "c2": float(c2),
        "phi": float(phi),
        "eigenvalues": eigenvalues.tolist(),
        "eigenvalue_magnitudes": eigenvalue_magnitudes.tolist(),
        "max_eigenvalue_magnitude": float(np.max(eigenvalue_magnitudes)),
        "stable_empirical": bool(stable),
        "stable_theoretical": bool(theoretical_stable),
        "stability_condition_w": bool(condition1),
        "stability_condition_phi": bool(condition2),
        "constriction_factor": float(chi) if chi is not None else None,
        "constriction_stable": bool(constriction_stable),
    }

# Example usage - test typical PSO parameters:
# result1 = analyze_pso_stability(w=0.7, c1=2.0, c2=2.0)
# Expected: stable_empirical=False (oscillatory), stable_theoretical=False
#
# result2 = analyze_pso_stability(w=0.5, c1=1.5, c2=1.5)
# Expected: stable_empirical=True, stable_theoretical=True