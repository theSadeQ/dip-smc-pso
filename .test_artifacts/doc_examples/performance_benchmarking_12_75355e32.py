# Example from: docs\testing\guides\performance_benchmarking.md
# Index: 12
# Runnable: True
# Hash: 75355e32

def test_with_warmup(benchmark):
    """Include warm-up for JIT-compiled code"""
    benchmark.pedantic(
        function,
        rounds=10,
        iterations=100,
        warmup_rounds=2  # Warm up JIT compiler
    )