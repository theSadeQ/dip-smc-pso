# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 18
# Runnable: True
# Hash: 867251c7

def profile_controller_creation(controller_type, n_iterations=100):
    """Profile controller creation performance."""

    import time
    import psutil
    import os

    process = psutil.Process(os.getpid())

    # Warmup
    controller = create_controller(controller_type)

    # Measure performance
    times = []
    memory_usage = []

    for i in range(n_iterations):
        # Measure memory before
        mem_before = process.memory_info().rss / 1024 / 1024  # MB

        # Time controller creation
        start_time = time.time()
        controller = create_controller(controller_type)
        end_time = time.time()

        # Measure memory after
        mem_after = process.memory_info().rss / 1024 / 1024  # MB

        times.append(end_time - start_time)
        memory_usage.append(mem_after - mem_before)

        # Cleanup
        del controller

    # Analysis
    import numpy as np

    print(f"Performance Profile for {controller_type}:")
    print(f"  Iterations: {n_iterations}")
    print(f"  Average time: {np.mean(times):.4f}s")
    print(f"  Std deviation: {np.std(times):.4f}s")
    print(f"  Min time: {np.min(times):.4f}s")
    print(f"  Max time: {np.max(times):.4f}s")
    print(f"  Average memory per creation: {np.mean(memory_usage):.2f}MB")

    # Performance thresholds
    if np.mean(times) > 0.1:
        print("⚠️  Controller creation is slow (>0.1s)")

    if np.mean(memory_usage) > 10:
        print("⚠️  High memory usage per controller (>10MB)")

    return {
        'mean_time': np.mean(times),
        'std_time': np.std(times),
        'mean_memory': np.mean(memory_usage)
    }

# Profile different controllers
for controller_type in ['classical_smc', 'adaptive_smc', 'sta_smc']:
    try:
        profile_controller_creation(controller_type)
        print()
    except Exception as e:
        print(f"Profiling failed for {controller_type}: {e}")