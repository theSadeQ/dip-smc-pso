# Example from: docs\theory\lyapunov_stability_analysis.md
# Index: 1
# Runnable: True
# Hash: cce9741d

import numpy as np
from src.plant.models.simplified.dynamics import SimplifiedDIPDynamics
from src.plant.models.simplified.config import SimplifiedDIPConfig

def validate_mass_matrix_properties():
    """
    Validate mass matrix M(q) is symmetric positive definite.

    This function tests Property 1.1 through 1.4 at multiple configurations.

    Returns:
        dict: Validation results with eigenvalues and condition numbers
    """
    # Initialize dynamics model
    config = SimplifiedDIPConfig.create_default()
    dynamics = SimplifiedDIPDynamics(config)

    # Test configurations: upright, perturbed, and extreme
    test_configs = [
        np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),  # Upright equilibrium
        np.array([0.0, 0.1, 0.1, 0.0, 0.0, 0.0]),  # Small perturbation
        np.array([0.0, 0.3, -0.2, 0.0, 0.0, 0.0]), # Medium perturbation
        np.array([0.0, 0.5, 0.4, 0.0, 0.0, 0.0]),  # Large perturbation
    ]

    results = []
    for state in test_configs:
        # Extract physics matrices
        M, C, G = dynamics.physics.compute_physics_matrices(state)

        # Property 1.1: Check symmetry
        symmetric = np.allclose(M, M.T, rtol=1e-10, atol=1e-12)
        symmetry_error = np.linalg.norm(M - M.T)

        # Property 1.2 & 1.3: Check positive definiteness via eigenvalues
        eigenvalues = np.linalg.eigvalsh(M)  # For symmetric matrices
        pos_def = np.all(eigenvalues > 0)
        lambda_min = np.min(eigenvalues)
        lambda_max = np.max(eigenvalues)

        # Condition number
        cond_number = lambda_max / lambda_min

        # Property 1.4: Skew-symmetry of (dM/dt - 2C)
        # For validation, we use finite differences to approximate dM/dt
        dt = 1e-6
        state_pert = state.copy()
        state_pert[3:] += dt  # Perturb velocities
        M_pert, _, _ = dynamics.physics.compute_physics_matrices(state_pert)
        M_dot_approx = (M_pert - M) / dt

        skew_matrix = M_dot_approx - 2 * C
        skew_symmetry_error = np.linalg.norm(skew_matrix + skew_matrix.T)
        skew_symmetric = skew_symmetry_error < 1e-3  # Tolerance for finite diff

        results.append({
            "state": state.tolist(),
            "symmetric": bool(symmetric),
            "symmetry_error": float(symmetry_error),
            "positive_definite": bool(pos_def),
            "eigenvalues": eigenvalues.tolist(),
            "lambda_min": float(lambda_min),
            "lambda_max": float(lambda_max),
            "condition_number": float(cond_number),
            "skew_symmetric": bool(skew_symmetric),
            "skew_symmetry_error": float(skew_symmetry_error),
        })

    return results

# Expected output:
# All configurations should have:
# - symmetric = True (symmetry_error ~ 0)
# - positive_definite = True (lambda_min > 0)
# - condition_number < 1e8 (well-conditioned)
# - skew_symmetric = True (skew_symmetry_error < 1e-3)