# Example from: docs\test_infrastructure_validation_report.md
# Index: 6
# Runnable: True
# Hash: a128734d

@pytest.mark.benchmark(group="controller.compute_control")
def test_classical_smc_performance(benchmark):
    """Benchmark classical SMC computation time."""
    # Target: <1ms per control computation
    # Regression threshold: +5% from baseline