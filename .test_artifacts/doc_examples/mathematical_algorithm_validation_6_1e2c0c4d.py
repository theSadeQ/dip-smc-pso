# Example from: docs\mathematical_algorithm_validation.md
# Index: 6
# Runnable: False
# Hash: 1e2c0c4d

# example-metadata:
# runnable: false

def monte_carlo_validation(n_trials: int = 10000) -> Dict[str, float]:
    """Monte Carlo validation of algorithm robustness."""
    success_rate = 0
    performance_metrics = []

    for trial in range(n_trials):
        # Random parameter perturbation
        perturbed_params = add_random_perturbation(base_params)

        # Run simulation
        result = run_simulation(perturbed_params)

        if result.stability_achieved:
            success_rate += 1
            performance_metrics.append(result.performance_index)

    return {
        'success_rate': success_rate / n_trials,
        'mean_performance': np.mean(performance_metrics),
        'std_performance': np.std(performance_metrics)
    }