# Example from: docs\test_infrastructure_documentation.md
# Index: 8
# Runnable: True
# Hash: 4b60a407

@pytest.mark.benchmark
def test_pso_optimization_performance(benchmark):
    """Benchmark PSO optimization performance."""
    def optimize_classical_smc():
        optimizer = PSOTuner(bounds=controller_bounds)
        return optimizer.optimize("classical_smc", n_particles=30, n_iterations=100)

    result = benchmark(optimize_classical_smc)
    # Regression detection: should complete within 60 seconds
    assert benchmark.stats.mean < 60.0