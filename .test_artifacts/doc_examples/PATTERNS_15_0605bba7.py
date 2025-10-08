# Example from: docs\PATTERNS.md
# Index: 15
# Runnable: True
# Hash: 0605bba7

# src/utils/monitoring/memory_monitor.py

from contextlib import contextmanager

@contextmanager
def memory_tracking(threshold_mb: float = 500.0):
    """Context manager for tracking memory usage."""
    import psutil
    import gc

    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024

    try:
        yield process
    finally:
        final_memory = process.memory_info().rss / 1024 / 1024
        delta = final_memory - initial_memory

        if delta > threshold_mb:
            gc.collect()  # Force garbage collection
            logging.warning(f"Memory increased by {delta:.1f}MB")

# Usage
with memory_tracking(threshold_mb=100.0) as process:
    # Run memory-intensive operation
    results = run_pso_optimization(n_iterations=1000)
# Automatic cleanup and memory check