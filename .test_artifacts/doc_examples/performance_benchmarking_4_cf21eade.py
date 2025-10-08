# Example from: docs\testing\guides\performance_benchmarking.md
# Index: 4
# Runnable: True
# Hash: cf21eade

from pytest_benchmark.stats import welch_ttest

def test_optimization_comparison(benchmark):
    """Compare two implementations with statistical significance"""
    # Run baseline
    baseline_times = benchmark_baseline()

    # Run optimized version
    optimized_times = benchmark_optimized()

    # Welch's t-test for significance
    t_stat, p_value = welch_ttest(baseline_times, optimized_times)

    assert p_value < 0.05, "No statistically significant improvement"
    assert np.mean(optimized_times) < np.mean(baseline_times), \
        "Optimized version is slower"