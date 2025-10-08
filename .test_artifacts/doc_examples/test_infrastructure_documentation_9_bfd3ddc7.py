# Example from: docs\test_infrastructure_documentation.md
# Index: 9
# Runnable: True
# Hash: bfd3ddc7

@pytest.mark.memory
def test_simulation_memory_usage():
    """Test memory usage during extended simulation."""
    import psutil
    import gc

    process = psutil.Process()
    initial_memory = process.memory_info().rss

    # Run extended simulation
    for _ in range(100):
        simulate_system(controller, dynamics, sim_time=1.0)
        gc.collect()

    final_memory = process.memory_info().rss
    memory_growth = (final_memory - initial_memory) / initial_memory

    assert memory_growth < 0.10  # Less than 10% memory growth