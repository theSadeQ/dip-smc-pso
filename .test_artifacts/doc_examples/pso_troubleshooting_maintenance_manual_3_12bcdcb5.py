# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 3
# Runnable: False
# Hash: 12bcdcb5

# Profile optimization performance
import time
import psutil
import os

def profile_pso_iteration():
    """Profile single PSO iteration."""
    process = psutil.Process(os.getpid())

    # Baseline measurements
    start_time = time.time()
    start_memory = process.memory_info().rss / 1024 / 1024  # MB

    # Run minimal PSO test
    # ... PSO code here ...

    end_time = time.time()
    end_memory = process.memory_info().rss / 1024 / 1024  # MB

    print(f"Iteration time: {end_time - start_time:.2f}s")
    print(f"Memory usage: {end_memory:.1f}MB (Δ{end_memory - start_memory:.1f}MB)")
    print(f"CPU count: {psutil.cpu_count()}")
    print(f"CPU usage: {psutil.cpu_percent()}%")

profile_pso_iteration()