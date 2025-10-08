# Example from: docs\analysis\view_conversion_recommendations.md
# Index: 9
# Runnable: True
# Hash: c32f882a

# tests/test_benchmarks/test_memory_regression.py
def test_simulation_memory_overhead():
    """Verify memory overhead remains < 1.5x of theoretical minimum."""
    baseline = 6 * 500 * 8  # 6 states × 500 steps × 8 bytes
    actual = measure_simulation_memory()
    assert actual < baseline * 1.5, f"Memory overhead too high: {actual/baseline:.2f}x"