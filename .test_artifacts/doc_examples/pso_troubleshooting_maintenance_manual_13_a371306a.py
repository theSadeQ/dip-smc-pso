# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 13
# Runnable: False
# Hash: a371306a

class MemoryEfficientPSO:
    """PSO implementation optimized for memory usage."""

    def __init__(self, max_memory_mb=1000):
        self.max_memory_mb = max_memory_mb
        self.memory_monitor = psutil.Process()

    def optimize_with_memory_management(self, *args, **kwargs):
        """Run optimization with active memory management."""

        def memory_callback(iteration, **cb_kwargs):
            current_memory = self.memory_monitor.memory_info().rss / 1024 / 1024

            if current_memory > self.max_memory_mb:
                print(f"⚠️  Memory limit exceeded: {current_memory:.1f}MB > {self.max_memory_mb}MB")

                # Force garbage collection
                import gc
                gc.collect()

                # Reduce particle count if memory still high
                new_memory = self.memory_monitor.memory_info().rss / 1024 / 1024
                if new_memory > self.max_memory_mb * 0.9:
                    self.n_particles = max(10, int(self.n_particles * 0.8))
                    print(f"🔽 Reduced particle count to {self.n_particles}")

            return False

        # Add memory callback to optimization
        kwargs['callback'] = memory_callback
        return self.base_optimize(*args, **kwargs)

# Usage
memory_efficient_pso = MemoryEfficientPSO(max_memory_mb=2000)
results = memory_efficient_pso.optimize_with_memory_management(...)