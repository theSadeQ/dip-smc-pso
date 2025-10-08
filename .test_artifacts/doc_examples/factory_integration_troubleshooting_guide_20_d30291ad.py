# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 20
# Runnable: True
# Hash: d30291ad

class MemoryMonitor:
    """Monitor memory usage during controller operations."""

    def __init__(self):
        import psutil
        import os
        self.process = psutil.Process(os.getpid())
        self.baseline_memory = self.get_memory_usage()
        self.peak_memory = self.baseline_memory
        self.measurements = []

    def get_memory_usage(self):
        """Get current memory usage in MB."""
        return self.process.memory_info().rss / 1024 / 1024

    def record_measurement(self, operation_name):
        """Record memory measurement."""
        current_memory = self.get_memory_usage()
        self.peak_memory = max(self.peak_memory, current_memory)

        measurement = {
            'operation': operation_name,
            'memory_mb': current_memory,
            'delta_mb': current_memory - self.baseline_memory
        }

        self.measurements.append(measurement)

        if measurement['delta_mb'] > 100:  # Alert if >100MB growth
            print(f"⚠️  Memory alert: {operation_name} - {current_memory:.1f}MB (+{measurement['delta_mb']:.1f}MB)")

    def print_summary(self):
        """Print memory usage summary."""
        current_memory = self.get_memory_usage()
        total_growth = current_memory - self.baseline_memory

        print(f"Memory Usage Summary:")
        print(f"  Baseline: {self.baseline_memory:.1f}MB")
        print(f"  Current: {current_memory:.1f}MB")
        print(f"  Peak: {self.peak_memory:.1f}MB")
        print(f"  Total growth: {total_growth:.1f}MB")

        if total_growth > 50:
            print("⚠️  Significant memory growth detected")

# Usage with memory monitoring
monitor = MemoryMonitor()

# Monitor PSO operation
factory = create_pso_controller_factory(SMCType.CLASSICAL)
monitor.record_measurement("Factory creation")

for i in range(1000):
    gains = np.random.uniform(1, 50, 6)
    controller = factory(gains)

    if i % 100 == 0:
        monitor.record_measurement(f"Iteration {i}")

    # Explicit cleanup
    del controller

monitor.record_measurement("PSO complete")
monitor.print_summary()