# Example from: docs\testing\guides\performance_benchmarking.md
# Index: 2
# Runnable: True
# Hash: aff08b8f

@pytest.mark.benchmark(group="dynamics")
def test_full_dynamics_performance(benchmark):
    """Benchmark full nonlinear dynamics"""
    dynamics = FullDynamics()
    state = np.array([0.1, 0.1, 0.0, 0.0])
    u = 1.0

    result = benchmark(dynamics.compute_derivatives, state, u)

    # Requirement: 1000 steps in <1ms
    assert benchmark.stats['mean'] < 1e-6  # <1µs per step