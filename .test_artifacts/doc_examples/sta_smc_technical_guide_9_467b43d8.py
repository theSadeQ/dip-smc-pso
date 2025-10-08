# Example from: docs\controllers\sta_smc_technical_guide.md
# Index: 9
# Runnable: False
# Hash: 467b43d8

# example-metadata:
# runnable: false

def monitor_sta_performance(controller, result, history):
    """Monitor STA-specific performance indicators."""

    z_current = result.state_vars[0]
    sigma = result.state_vars[1]

    # Convergence indicators
    near_surface = abs(sigma) < controller.boundary_layer
    integral_active = abs(z_current) > 0.01

    # Performance metrics
    metrics = {
        'z': z_current,
        'sigma': sigma,
        'near_surface': near_surface,
        'integral_active': integral_active,
        'convergence_estimate': 2*abs(sigma)**0.5 / controller.alg_gain_K1**0.5
    }

    # Warning conditions
    if abs(z_current) > controller.max_force * 0.9:
        print(f"WARNING: Integrator near saturation: z = {z_current:.2f}")

    if not near_surface and t > 5.0:
        print(f"WARNING: Not converged after 5s: |σ| = {abs(sigma):.3f}")

    return metrics