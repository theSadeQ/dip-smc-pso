# Example from: docs\testing\guides\performance_benchmarking.md
# Index: 13
# Runnable: False
# Hash: ad4f4784

# example-metadata:
# runnable: false

@pytest.mark.benchmark(
    disable_gc=True,  # Disable garbage collector
    min_rounds=10,    # Ensure statistical significance
    timer=time.perf_counter  # High-resolution timer
)
def test_precise_benchmark():
    ...