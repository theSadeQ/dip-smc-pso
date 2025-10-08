# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 21
# Runnable: False
# Hash: f7ecfedc

# example-metadata:
# runnable: false

def diagnose_classical_smc(controller, state, result):
    """Comprehensive controller diagnostics."""

    diagnostics = {}

    # Extract current values
    sigma = result.history['sigma'][-1]
    u_eq = result.history['u_eq'][-1]
    u_robust = result.history['u_robust'][-1]
    eps_eff = result.history['epsilon_eff'][-1]

    # Surface distance
    diagnostics['surface_distance'] = abs(sigma)
    diagnostics['within_boundary'] = abs(sigma) < eps_eff

    # Control component analysis
    diagnostics['eq_magnitude'] = abs(u_eq)
    diagnostics['robust_magnitude'] = abs(u_robust)
    diagnostics['eq_dominant'] = abs(u_eq) > abs(u_robust)

    # Saturation checks
    diagnostics['control_saturated'] = abs(result.control) >= controller.max_force * 0.99
    diagnostics['eq_saturated'] = abs(u_eq) >= 5.0 * controller.max_force * 0.99

    return diagnostics