# Example from: docs\factory\troubleshooting_guide.md
# Index: 12
# Runnable: True
# Hash: 2752cad0

import time
import statistics
from src.controllers.factory import create_controller, get_default_gains

def profile_factory_performance():
    print("Profiling factory performance")

    controller_types = ['classical_smc', 'adaptive_smc', 'sta_smc']
    results = {}

    for controller_type in controller_types:
        print(f"\nTesting {controller_type}:")

        gains = get_default_gains(controller_type)
        creation_times = []

        # Warmup
        for _ in range(5):
            create_controller(controller_type, gains=gains)

        # Actual measurements
        for i in range(20):
            start_time = time.perf_counter()
            controller = create_controller(controller_type, gains=gains)
            end_time = time.perf_counter()

            creation_time = (end_time - start_time) * 1000  # Convert to ms
            creation_times.append(creation_time)

        # Statistics
        mean_time = statistics.mean(creation_times)
        std_time = statistics.stdev(creation_times)
        min_time = min(creation_times)
        max_time = max(creation_times)

        results[controller_type] = {
            'mean': mean_time,
            'std': std_time,
            'min': min_time,
            'max': max_time
        }

        print(f"  Mean: {mean_time:.2f} ms")
        print(f"  Std:  {std_time:.2f} ms")
        print(f"  Min:  {min_time:.2f} ms")
        print(f"  Max:  {max_time:.2f} ms")

        # Performance assessment
        if mean_time > 10:
            print(f"  ⚠ Slow creation time (>{10}ms)")
        else:
            print(f"  ✓ Acceptable creation time")

    return results

# Run performance profiling
profile_results = profile_factory_performance()