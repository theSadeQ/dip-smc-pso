# Example from: docs\testing\guides\performance_benchmarking.md
# Index: 3
# Runnable: False
# Hash: 2990e853

# example-metadata:
# runnable: false

def test_pso_optimization_benchmark(benchmark):
    """Benchmark PSO convergence speed"""
    tuner = PSOTuner(
        n_particles=30,
        iterations=50,
        bounds=[(1, 100)] * 6
    )

    def run_pso():
        return tuner.optimize(fitness_function)

    result = benchmark.pedantic(run_pso, iterations=5, rounds=3)

    # Requirements
    assert benchmark.stats['mean'] < 60.0  # <60s for 50 iterations
    assert result['cost'] < 0.1  # Converges to good solution