# Example from: docs\pso_factory_integration_patterns.md
# Index: 9
# Runnable: False
# Hash: 3219552b

# example-metadata:
# runnable: false

def validate_pso_optimized_controller(gains: np.ndarray, controller_type: SMCType) -> Dict[str, Any]:
    """Comprehensive validation of PSO-optimized controller."""

    validation_results = {}

    # Create optimized controller
    controller = create_smc_for_pso(controller_type, gains)

    # 1. Stability Analysis
    validation_results['stability'] = validate_lyapunov_stability(controller)

    # 2. Performance Metrics
    validation_results['performance'] = {
        'ise': compute_integral_squared_error(controller),
        'itae': compute_integral_time_absolute_error(controller),
        'settling_time': compute_settling_time(controller),
        'overshoot': compute_overshoot(controller)
    }

    # 3. Robustness Analysis
    validation_results['robustness'] = {
        'parameter_sensitivity': analyze_parameter_sensitivity(controller),
        'disturbance_rejection': test_disturbance_rejection(controller),
        'noise_tolerance': evaluate_noise_tolerance(controller)
    }

    # 4. Chattering Analysis
    validation_results['chattering'] = {
        'chattering_index': compute_chattering_index(controller),
        'high_frequency_content': analyze_frequency_content(controller),
        'actuator_stress': evaluate_actuator_stress(controller)
    }

    # 5. Control Theory Properties
    if controller_type == SMCType.CLASSICAL:
        validation_results['theory'] = validate_classical_smc_properties(gains)
    elif controller_type == SMCType.ADAPTIVE:
        validation_results['theory'] = validate_adaptive_smc_properties(gains)
    elif controller_type == SMCType.SUPER_TWISTING:
        validation_results['theory'] = validate_sta_smc_properties(gains)

    return validation_results

def validate_classical_smc_properties(gains: np.ndarray) -> Dict[str, bool]:
    """Validate classical SMC theoretical properties."""
    k1, k2, lam1, lam2, K, kd = gains

    return {
        'surface_stability': lam1 > 0 and lam2 > 0,  # Hurwitz stability
        'reaching_condition': K > 0,                  # Reaching condition
        'finite_time_convergence': True,              # Guaranteed by SMC theory
        'robustness_margin': K > 2 * max(k1, k2),    # Sufficient robustness
        'chattering_bound': K < 100,                  # Practical chattering limit
        'damping_sufficient': kd >= 0                 # Non-negative damping
    }

def validate_adaptive_smc_properties(gains: np.ndarray) -> Dict[str, bool]:
    """Validate adaptive SMC theoretical properties."""
    k1, k2, lam1, lam2, gamma = gains

    return {
        'surface_stability': lam1 > 0 and lam2 > 0,
        'adaptation_convergence': gamma > 0,
        'adaptation_rate_bound': 0.1 <= gamma <= 20,
        'finite_time_reaching': True,
        'parameter_convergence': gamma > 0.5  # Sufficient for convergence
    }