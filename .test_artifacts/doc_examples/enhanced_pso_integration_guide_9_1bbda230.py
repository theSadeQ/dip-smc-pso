# Example from: docs\factory\enhanced_pso_integration_guide.md
# Index: 9
# Runnable: False
# Hash: 1bbda230

def get_optimized_pso_bounds(controller_type: str, plant_params: Dict[str, Any]) -> Tuple[List[float], List[float]]:
    """
    Compute optimized PSO bounds based on plant parameters and control theory.

    Uses stability margins and performance requirements to derive tight bounds.
    """

    if controller_type == 'classical_smc':
        # Classical SMC bounds based on stability analysis
        # Pole placement considerations for closed-loop stability

        max_damping = plant_params.get('max_damping_requirement', 0.7)
        settling_time = plant_params.get('settling_time_requirement', 2.0)

        # Derive bounds from desired closed-loop characteristics
        lambda_min = 4.0 / settling_time  # Natural frequency requirement
        lambda_max = 20.0  # Upper bound to prevent excessive control effort

        k_min = lambda_min / 2.0  # Position gain lower bound
        k_max = lambda_max * 2.0  # Position gain upper bound

        K_min = estimate_min_switching_gain(plant_params)
        K_max = plant_params.get('max_force', 150.0) * 0.8  # Conservative upper bound

        bounds_lower = [k_min, k_min, lambda_min, lambda_min, K_min, 0.0]
        bounds_upper = [k_max, k_max, lambda_max, lambda_max, K_max, 10.0]

    elif controller_type == 'sta_smc':
        # Super-Twisting bounds with stability constraint K1 > K2

        # Lyapunov-based design bounds
        L0 = estimate_lipschitz_constant(plant_params)

        K1_min = math.sqrt(L0) * 1.1  # Safety margin
        K1_max = math.sqrt(L0) * 5.0  # Conservative upper bound

        K2_min = L0 / (2 * math.sqrt(L0 - K1_min**2)) * 1.1
        K2_max = K1_max * 0.8  # Ensure K1 > K2 constraint

        bounds_lower = [K1_min, K2_min, 2.0, 2.0, 5.0, 5.0]
        bounds_upper = [K1_max, K2_max, 30.0, 30.0, 20.0, 20.0]

    elif controller_type == 'adaptive_smc':
        # Adaptive SMC bounds based on adaptation rate limits

        # Stability-preserving adaptation rate bounds
        gamma_min = 0.1  # Minimum for reasonable adaptation speed
        gamma_max = estimate_max_adaptation_rate(plant_params)  # Stability limit

        bounds_lower = [2.0, 2.0, 5.0, 5.0, gamma_min]
        bounds_upper = [40.0, 40.0, 25.0, 25.0, gamma_max]

    else:  # hybrid_adaptive_sta_smc
        # Hybrid controller bounds (conservative surface parameters)
        bounds_lower = [2.0, 2.0, 5.0, 5.0]
        bounds_upper = [30.0, 30.0, 20.0, 20.0]

    return bounds_lower, bounds_upper

def estimate_min_switching_gain(plant_params: Dict[str, Any]) -> float:
    """Estimate minimum switching gain based on disturbance bounds."""

    # Extract disturbance characteristics
    max_model_uncertainty = plant_params.get('model_uncertainty', 0.2)
    max_external_disturbance = plant_params.get('external_disturbance', 5.0)
    safety_margin = plant_params.get('safety_margin', 1.5)

    # Conservative estimate
    return (max_model_uncertainty + max_external_disturbance) * safety_margin

def estimate_lipschitz_constant(plant_params: Dict[str, Any]) -> float:
    """Estimate Lipschitz constant for STA design."""

    # Based on system nonlinearity and uncertainty bounds
    max_nonlinearity = plant_params.get('max_nonlinearity', 10.0)
    uncertainty_bound = plant_params.get('uncertainty_bound', 5.0)

    return max_nonlinearity + uncertainty_bound

def estimate_max_adaptation_rate(plant_params: Dict[str, Any]) -> float:
    """Estimate maximum stable adaptation rate."""

    # Based on parameter variation speed and system bandwidth
    system_bandwidth = plant_params.get('system_bandwidth', 10.0)  # rad/s
    parameter_variation_rate = plant_params.get('parameter_variation_rate', 0.1)  # Hz

    # Conservative bound: adaptation much slower than system dynamics
    return min(system_bandwidth / 10.0, 1.0 / parameter_variation_rate)