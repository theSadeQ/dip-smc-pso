# Example from: docs\pso_factory_integration_patterns.md
# Index: 10
# Runnable: True
# Hash: 84c99852

def statistical_validation_of_pso_results(controller_type: SMCType,
                                        optimized_gains: np.ndarray,
                                        n_trials: int = 50) -> Dict[str, Any]:
    """Statistical validation of PSO optimization results."""

    # Multiple independent evaluations
    performance_samples = []

    for trial in range(n_trials):
        # Add small random perturbations to test robustness
        perturbed_gains = optimized_gains * (1 + 0.01 * np.random.randn(len(optimized_gains)))

        # Create controller with perturbed gains
        controller = create_smc_for_pso(controller_type, perturbed_gains)

        # Evaluate performance
        metrics = evaluate_controller_performance(controller)
        performance_samples.append(metrics['total_cost'])

    # Statistical analysis
    performance_array = np.array(performance_samples)

    validation_stats = {
        'mean_performance': np.mean(performance_array),
        'std_performance': np.std(performance_array),
        'coefficient_variation': np.std(performance_array) / np.mean(performance_array),
        'confidence_interval_95': np.percentile(performance_array, [2.5, 97.5]),
        'worst_case_performance': np.max(performance_array),
        'best_case_performance': np.min(performance_array),
        'robustness_score': 1.0 / (1.0 + np.std(performance_array))
    }

    # Statistical significance tests
    from scipy import stats

    # Test for normality
    _, normality_p_value = stats.shapiro(performance_array)
    validation_stats['performance_distribution_normal'] = normality_p_value > 0.05

    # Compare with default gains
    default_gains = get_default_gains(controller_type.value)
    default_controller = create_smc_for_pso(controller_type, default_gains)
    default_performance = evaluate_controller_performance(default_controller)['total_cost']

    # Statistical improvement test
    improvement_ratio = default_performance / np.mean(performance_array)
    validation_stats['improvement_ratio'] = improvement_ratio
    validation_stats['significant_improvement'] = improvement_ratio > 1.1  # 10% improvement threshold

    return validation_stats