# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 15
# Runnable: False
# Hash: d3cdd49e

def monitor_hybrid_controller(controller, state, result):
    """Monitor hybrid controller performance indicators."""

    # Extract monitoring data
    k1, k2, u_int = result.state_vars
    s = result.sliding_surface

    # Performance indicators
    adaptation_rate = (k1 + k2) / (controller.k1_max + controller.k2_max)
    surface_distance = abs(s)
    integral_usage = abs(u_int) / controller.u_int_max

    # Warning conditions
    if adaptation_rate > 0.8:
        print(f"WARNING: High adaptation rate: {adaptation_rate:.3f}")

    if surface_distance > 1.0:
        print(f"WARNING: Large sliding surface: {surface_distance:.3f}")

    if integral_usage > 0.9:
        print(f"WARNING: Integral near saturation: {integral_usage:.3f}")

    return {
        'adaptation_rate': adaptation_rate,
        'surface_distance': surface_distance,
        'integral_usage': integral_usage
    }