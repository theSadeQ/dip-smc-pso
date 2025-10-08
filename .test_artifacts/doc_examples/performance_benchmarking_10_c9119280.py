# Example from: docs\testing\guides\performance_benchmarking.md
# Index: 10
# Runnable: True
# Hash: c9119280

from pytest_benchmark.utils import format_time

def test_with_custom_metrics(benchmark):
    """Track custom metrics beyond time"""
    def func_with_metrics():
        result = expensive_function()
        # Custom metrics
        return {
            'result': result,
            'memory_mb': get_memory_usage(),
            'cache_misses': get_cache_misses()
        }

    output = benchmark(func_with_metrics)
    print(f"Memory: {output['memory_mb']:.2f} MB")