# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 5
# Runnable: False
# Hash: 5f5a7ad6

# example-metadata:
# runnable: false

import gc
import psutil
import matplotlib.pyplot as plt

def monitor_memory_usage():
    """Monitor memory usage during optimization."""
    memory_samples = []
    process = psutil.Process()

    # Sample memory every 10 iterations (add to PSO callback)
    def memory_callback(iteration, **kwargs):
        if iteration % 10 == 0:
            memory_mb = process.memory_info().rss / 1024 / 1024
            memory_samples.append(memory_mb)
            print(f"Iteration {iteration}: Memory usage = {memory_mb:.1f}MB")

            # Force garbage collection
            gc.collect()

    return memory_callback, memory_samples

# Use in optimization
callback, samples = monitor_memory_usage()
# results = pso_tuner.optimize(callback=callback, ...)

# Plot memory usage
plt.plot(samples)
plt.title('Memory Usage During Optimization')
plt.xlabel('Sample')
plt.ylabel('Memory (MB)')
plt.show()