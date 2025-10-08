# Example from: docs\benchmarks\controller_performance_benchmarks.md
# Index: 4
# Runnable: True
# Hash: 5ee1c014

import time

def measure_instantiation(controller_class, gains, n_samples=5):
    times = []
    for _ in range(n_samples):
        t0 = time.perf_counter()
        controller = controller_class(gains=gains, max_force=100.0)
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000)  # Convert to milliseconds
    return {
        'avg_time_ms': np.mean(times),
        'std_time_ms': np.std(times),
        'p95_time_ms': np.percentile(times, 95)
    }