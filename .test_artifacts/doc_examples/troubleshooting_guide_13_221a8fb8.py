# Example from: docs\factory\troubleshooting_guide.md
# Index: 13
# Runnable: True
# Hash: 221a8fb8

import psutil
import os
from src.controllers.factory import create_controller

def diagnose_memory_usage():
    print("Diagnosing memory usage")

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

    print(f"Initial memory usage: {initial_memory:.2f} MB")

    controllers = []
    memory_measurements = []

    for i in range(100):
        controller = create_controller('classical_smc', gains=[10]*6)
        controllers.append(controller)

        if i % 10 == 0:
            current_memory = process.memory_info().rss / 1024 / 1024
            memory_measurements.append(current_memory)
            print(f"After {i+1} controllers: {current_memory:.2f} MB")

    final_memory = process.memory_info().rss / 1024 / 1024
    memory_increase = final_memory - initial_memory

    print(f"Final memory usage: {final_memory:.2f} MB")
    print(f"Memory increase: {memory_increase:.2f} MB")
    print(f"Memory per controller: {memory_increase/100:.3f} MB")

    # Check for memory leaks
    if memory_increase > 50:  # More than 50MB for 100 controllers
        print("⚠ Possible memory leak detected")
    else:
        print("✓ Memory usage within acceptable limits")

# Run memory diagnostic
diagnose_memory_usage()