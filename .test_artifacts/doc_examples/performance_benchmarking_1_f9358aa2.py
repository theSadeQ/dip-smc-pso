# Example from: docs\testing\guides\performance_benchmarking.md
# Index: 1
# Runnable: True
# Hash: f9358aa2

import pytest
from pytest_benchmark.fixture import BenchmarkFixture

def test_classical_smc_benchmark(benchmark: BenchmarkFixture):
    """Benchmark classical SMC control computation"""
    controller = ClassicalSMC(gains=[10, 5, 8, 3, 15, 2])
    state = np.array([0.1, -0.2, 0.5, -0.3])

    result = benchmark(controller.compute_control, state)

    # Performance requirements
    assert benchmark.stats['mean'] < 50e-6  # <50µs mean
    assert benchmark.stats['stddev'] < 5e-6  # <5µs std dev