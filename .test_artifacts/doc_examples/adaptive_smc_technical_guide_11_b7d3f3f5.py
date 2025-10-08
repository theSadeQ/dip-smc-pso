# Example from: docs\controllers\adaptive_smc_technical_guide.md
# Index: 11
# Runnable: False
# Hash: b7d3f3f5

# example-metadata:
# runnable: false

def monitor_adaptive_smc(controller, state, result):
    """Monitor adaptive SMC performance and gain evolution."""

    K_current = result.state_vars[0]
    sigma = result.sliding_surface
    dK = result.history['dK'][-1] if result.history['dK'] else 0.0

    # Performance indicators
    gain_utilization = K_current / controller.K_max
    adaptation_active = abs(sigma) > controller.dead_zone
    near_bounds = (K_current >= controller.K_max * 0.9 or
                   K_current <= controller.K_min * 1.1)

    # Warning conditions
    if near_bounds:
        print(f"WARNING: Gain near bounds: K = {K_current:.2f}")

    if adaptation_active and abs(dK) < 0.01:
        print(f"WARNING: Slow adaptation despite large error: |σ| = {abs(sigma):.3f}")

    if K_current < 1.0:
        print(f"WARNING: Very low adaptive gain: K = {K_current:.2f}")

    return {
        'K_current': K_current,
        'gain_utilization': gain_utilization,
        'adaptation_active': adaptation_active,
        'near_bounds': near_bounds,
        'dK': dK
    }