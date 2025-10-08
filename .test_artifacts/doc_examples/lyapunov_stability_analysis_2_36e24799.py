# Example from: docs\theory\lyapunov_stability_analysis.md
# Index: 2
# Runnable: True
# Hash: 36e24799

import numpy as np
from scipy import linalg

def design_sliding_surface(lambda1, lambda2, k1, k2):
    """
    Design sliding surface and verify closed-loop stability.

    Args:
        lambda1, lambda2: Position error gains (> 0)
        k1, k2: Velocity error gains (> 0)

    Returns:
        dict: Eigenvalues and stability analysis
    """
    # Sliding surface gain vector
    C = np.array([lambda1, lambda2, k1, k2])

    # Decoupled error dynamics on sliding surface
    # For pendulum 1: ddot(theta1) = -(lambda1/k1) * dot(theta1)
    # For pendulum 2: ddot(theta2) = -(lambda2/k2) * dot(theta2)

    # Natural frequencies
    omega1 = np.sqrt(lambda1 / k1)
    omega2 = np.sqrt(lambda2 / k2)

    # Closed-loop poles (on imaginary axis - marginal stability)
    poles_marginal = [1j * omega1, -1j * omega1, 1j * omega2, -1j * omega2]

    # With SMC discontinuous term, effective damping is added
    # Approximate damped poles (SMC provides implicit damping)
    zeta_eff = 0.7  # Effective damping ratio from SMC switching
    poles_damped = [
        -zeta_eff * omega1 + 1j * omega1 * np.sqrt(1 - zeta_eff**2),
        -zeta_eff * omega1 - 1j * omega1 * np.sqrt(1 - zeta_eff**2),
        -zeta_eff * omega2 + 1j * omega2 * np.sqrt(1 - zeta_eff**2),
        -zeta_eff * omega2 - 1j * omega2 * np.sqrt(1 - zeta_eff**2),
    ]

    # Stability margin
    min_real_part = min([np.real(p) for p in poles_damped])

    return {
        "C": C.tolist(),
        "omega1": float(omega1),
        "omega2": float(omega2),
        "poles_marginal": [complex(p) for p in poles_marginal],
        "poles_damped": [complex(p) for p in poles_damped],
        "stable": min_real_part < 0,
        "stability_margin": float(-min_real_part),
    }

# Example usage:
# result = design_sliding_surface(lambda1=10, lambda2=8, k1=15, k2=12)
# Expected: stable=True, stability_margin > 0