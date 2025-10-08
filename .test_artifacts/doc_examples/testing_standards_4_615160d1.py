# Example from: docs\testing\standards\testing_standards.md
# Index: 4
# Runnable: True
# Hash: 615160d1

import pytest

@pytest.mark.benchmark(group="control_computation")
def test_classical_smc_performance(benchmark):
    """Benchmark classical SMC control computation performance."""
    controller = ClassicalSMC(gains=[10, 8, 15, 12, 50, 5])
    state = np.array([0.1, 0.05, 0.02, 0.0, 0.0, 0.0])

    result = benchmark(controller.compute_control, state, 0.0, {})

    # Performance requirements
    assert benchmark.stats.mean < 0.001  # Mean execution time < 1ms
    assert benchmark.stats.stddev < 0.0005  # Low variance

@pytest.mark.benchmark(group="batch_simulation")
def test_batch_simulation_scaling(benchmark):
    """Benchmark batch simulation scaling with number of trials."""
    controller_factory = lambda: ClassicalSMC(gains=[10, 8, 15, 12, 50, 5])

    def run_batch(n_trials=100):
        return run_multiple_trials(controller_factory, create_test_config(), n_trials)

    result = benchmark(run_batch)

    # Scaling requirements
    assert benchmark.stats.mean < 10.0  # 100 trials in < 10 seconds