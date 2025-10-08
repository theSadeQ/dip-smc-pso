# Example from: docs\technical\controller_factory_integration.md
# Index: 20
# Runnable: False
# Hash: aad633da

# example-metadata:
# runnable: false

def benchmark_factory_performance():
    """Benchmark factory instantiation performance."""

    controller_types = ['classical_smc', 'sta_smc', 'adaptive_smc']
    results = {}

    for controller_type in controller_types:
        times = []
        for _ in range(100):
            start = time.perf_counter()
            controller = create_controller(controller_type)
            end = time.perf_counter()
            times.append(end - start)

        results[controller_type] = {
            'mean': np.mean(times),
            'std': np.std(times),
            'max': np.max(times),
            'p95': np.percentile(times, 95)
        }

    return results