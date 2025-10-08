# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 17
# Runnable: False
# Hash: 0fdc3776

def monitor_classical_smc(controller, state, result):
    """Monitor classical SMC performance indicators."""

    sigma = result.history['sigma'][-1]
    u_eq = result.history['u_eq'][-1]
    u_robust = result.history['u_robust'][-1]
    eps_eff = result.history['epsilon_eff'][-1]

    # Performance indicators
    surface_distance = abs(sigma)
    eq_ratio = abs(u_eq) / controller.max_force if controller.max_force > 0 else 0
    robust_ratio = abs(u_robust) / controller.max_force if controller.max_force > 0 else 0

    # Warning conditions
    if surface_distance > 1.0:
        print(f"WARNING: Large sliding surface: {surface_distance:.3f}")

    if eq_ratio > 0.9:
        print(f"WARNING: Equivalent control near saturation: {eq_ratio:.3f}")

    if abs(result.control) >= controller.max_force * 0.99:
        print(f"WARNING: Control saturated: {result.control:.2f} N")

    return {
        'surface_distance': surface_distance,
        'eq_ratio': eq_ratio,
        'robust_ratio': robust_ratio,
        'boundary_layer': eps_eff
    }