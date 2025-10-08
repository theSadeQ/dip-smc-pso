# Example from: docs\factory_integration_documentation.md
# Index: 40
# Runnable: True
# Hash: 8a948ebc

# Benchmark factory performance
def benchmark_factory_performance():
    import time

    start_time = time.time()
    for _ in range(1000):
        controller = create_controller('classical_smc')
    end_time = time.time()

    avg_time = (end_time - start_time) / 1000
    assert avg_time < 0.005, f"Factory too slow: {avg_time:.6f}s"