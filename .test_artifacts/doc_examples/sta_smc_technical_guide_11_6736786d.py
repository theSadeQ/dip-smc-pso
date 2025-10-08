# Example from: docs\controllers\sta_smc_technical_guide.md
# Index: 11
# Runnable: False
# Hash: 6736786d

# example-metadata:
# runnable: false

def diagnose_sta_health(controller, history):
    """Diagnose STA SMC health."""

    z_history = np.array(history['z'])
    sigma_history = np.array(history['sigma'])

    diagnostics = {
        'z_max': np.max(np.abs(z_history)),
        'z_saturated': np.any(np.abs(z_history) >= controller.max_force * 0.99),
        'sigma_final': sigma_history[-1],
        'converged': np.all(np.abs(sigma_history[-100:]) < controller.boundary_layer),
        'chattering': np.std(np.diff(history['u']))
    }

    # Warnings
    if diagnostics['z_saturated']:
        print("WARNING: Integrator saturated - consider anti-windup")

    if not diagnostics['converged']:
        print("WARNING: Not converged - increase K1 or check stability")

    return diagnostics