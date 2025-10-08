# Example from: docs\testing\guides\performance_benchmarking.md
# Index: 6
# Runnable: True
# Hash: b5c2ecc9

import line_profiler

@profile  # Use kernprof -lv script.py
def slow_function():
    # Line-by-line profiling
    for i in range(1000):
        expensive_operation(i)