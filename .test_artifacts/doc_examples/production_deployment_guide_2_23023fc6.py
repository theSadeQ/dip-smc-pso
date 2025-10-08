# Example from: docs\deployment\production_deployment_guide.md
# Index: 2
# Runnable: False
# Hash: 23023fc6

#!/usr/bin/env python3
"""
Production performance benchmark script.
Validates system performance under production load.
"""

import time
import statistics
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from src.controllers.factory import create_controller

def benchmark_controller_performance():
    """Benchmark controller performance under load."""

    controllers = ['classical_smc', 'adaptive_smc', 'sta_smc', 'hybrid_adaptive_sta_smc']
    results = {}

    for controller_type in controllers:
        print(f"Benchmarking {controller_type}...")

        # Create controller
        controller = create_controller(controller_type)

        # Benchmark parameters
        n_iterations = 10000
        state = np.array([0.1, 0.1, 0.0, 0.0, 0.0, 0.0])

        # Single-threaded performance
        start_time = time.time()
        for _ in range(n_iterations):
            result = controller.compute_control(state)
        single_thread_time = time.time() - start_time

        # Multi-threaded performance
        def compute_batch():
            for _ in range(n_iterations // 4):
                result = controller.compute_control(state)

        start_time = time.time()
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(compute_batch) for _ in range(4)]
            for future in futures:
                future.result()
        multi_thread_time = time.time() - start_time

        results[controller_type] = {
            'single_thread_time': single_thread_time,
            'multi_thread_time': multi_thread_time,
            'single_thread_rate': n_iterations / single_thread_time,
            'multi_thread_rate': n_iterations / multi_thread_time,
            'speedup': single_thread_time / multi_thread_time
        }

    return results

def validate_production_readiness():
    """Validate system meets production performance requirements."""

    requirements = {
        'min_control_rate': 100,  # Hz
        'max_latency': 0.01,      # seconds
        'min_throughput': 1000,   # computations/second
    }

    results = benchmark_controller_performance()

    print("\nProduction Readiness Validation:")
    print("=" * 50)

    all_pass = True
    for controller_type, metrics in results.items():
        control_rate = metrics['single_thread_rate']
        latency = 1.0 / control_rate

        rate_pass = control_rate >= requirements['min_control_rate']
        latency_pass = latency <= requirements['max_latency']
        throughput_pass = metrics['multi_thread_rate'] >= requirements['min_throughput']

        status = "PASS" if all([rate_pass, latency_pass, throughput_pass]) else "FAIL"
        if status == "FAIL":
            all_pass = False

        print(f"{controller_type:25} | {status:4} | "
              f"Rate: {control_rate:6.1f} Hz | "
              f"Latency: {latency*1000:5.2f} ms | "
              f"Throughput: {metrics['multi_thread_rate']:6.1f} ops/s")

    print("=" * 50)
    overall_status = "PRODUCTION READY" if all_pass else "NEEDS OPTIMIZATION"
    print(f"Overall Status: {overall_status}")

    return all_pass

if __name__ == "__main__":
    validation_result = validate_production_readiness()
    exit(0 if validation_result else 1)