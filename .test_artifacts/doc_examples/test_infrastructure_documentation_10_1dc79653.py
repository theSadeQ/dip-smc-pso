# Example from: docs\test_infrastructure_documentation.md
# Index: 10
# Runnable: False
# Hash: 1dc79653

# example-metadata:
# runnable: false

@pytest.mark.concurrent
@pytest.mark.xfail(reason="Thread safety validation in progress")
def test_parallel_pso_optimization():
    """Test PSO optimization with parallel fitness evaluation."""
    optimizer = PSOTuner(bounds=controller_bounds, n_jobs=4)
    results = []

    # Run multiple optimizations concurrently
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(optimizer.optimize, "classical_smc") for _ in range(4)]
        results = [f.result() for f in futures]

    # All optimizations should succeed without race conditions
    assert all(r.success for r in results)