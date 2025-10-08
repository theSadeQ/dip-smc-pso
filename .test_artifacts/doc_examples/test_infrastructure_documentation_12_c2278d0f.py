# Example from: docs\test_infrastructure_documentation.md
# Index: 12
# Runnable: False
# Hash: c2278d0f

@pytest.mark.statistical
def test_optimization_performance_distribution():
    """Statistical analysis of optimization performance distribution."""
    performance_samples = []

    for _ in range(50):
        optimizer = PSOTuner(bounds=controller_bounds)
        result = optimizer.optimize("adaptive_smc", n_particles=20, n_iterations=100)
        performance_samples.append(result.best_fitness)

    # Statistical tests
    mean_performance = np.mean(performance_samples)
    std_performance = np.std(performance_samples)

    # 95% confidence interval should indicate good performance
    confidence_interval = stats.norm.interval(0.95, mean_performance, std_performance)
    assert confidence_interval[1] < 10.0  # Upper bound on fitness cost