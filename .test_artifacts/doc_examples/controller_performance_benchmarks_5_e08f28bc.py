# Example from: docs\benchmarks\controller_performance_benchmarks.md
# Index: 5
# Runnable: False
# Hash: e08f28bc

# example-metadata:
# runnable: false

def measure_computation(controller, state, n_samples=100):
    times = []
    for _ in range(n_samples):
        t0 = time.perf_counter()
        control = controller.compute_control(state)
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000)
    return {
        'avg_time_ms': np.mean(times),
        'p95_time_ms': np.percentile(times, 95)
    }