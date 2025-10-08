# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 16
# Runnable: True
# Hash: a6237f90

import time
import psutil
import os

class OptimizationProfiler:
    """Profile PSO optimization performance."""

    def __init__(self):
        self.start_time = None
        self.memory_samples = []
        self.cpu_samples = []

    def start_profiling(self):
        """Start performance profiling."""
        self.start_time = time.time()
        self.process = psutil.Process(os.getpid())

    def sample_performance(self):
        """Sample current performance metrics."""
        if self.start_time:
            self.memory_samples.append(self.process.memory_info().rss / 1024 / 1024)  # MB
            self.cpu_samples.append(self.process.cpu_percent())

    def get_summary(self):
        """Get performance summary."""
        total_time = time.time() - self.start_time

        return {
            'total_time': total_time,
            'peak_memory_mb': max(self.memory_samples) if self.memory_samples else 0,
            'avg_cpu_percent': np.mean(self.cpu_samples) if self.cpu_samples else 0,
            'memory_trend': np.polyfit(range(len(self.memory_samples)),
                                     self.memory_samples, 1)[0] if len(self.memory_samples) > 1 else 0
        }

# Usage in optimization
profiler = OptimizationProfiler()
profiler.start_profiling()

# Optimization with profiling callback
def profiling_callback(iteration, **kwargs):
    profiler.sample_performance()
    return False

results = pso_tuner.optimize(
    bounds=bounds,
    callback=profiling_callback,
    n_particles=50,
    n_iterations=100
)

performance_summary = profiler.get_summary()
print(f"Optimization completed in {performance_summary['total_time']:.1f} seconds")
print(f"Peak memory usage: {performance_summary['peak_memory_mb']:.1f} MB")