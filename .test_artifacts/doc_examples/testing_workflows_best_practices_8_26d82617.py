# Example from: docs\testing\testing_workflows_best_practices.md
# Index: 8
# Runnable: False
# Hash: 26d82617

# example-metadata:
# runnable: false

# Metric 1: Test-to-Code Ratio
test_loc = count_lines_of_code('tests/')
src_loc = count_lines_of_code('src/')
ratio = test_loc / src_loc

# Target: 1.5-2.0 (150-200% test code)
assert ratio >= 1.5, f"Insufficient test coverage: ratio={ratio:.2f}"

# Metric 2: Average Test Execution Time
total_time = pytest_duration
test_count = pytest_test_count
avg_time = total_time / test_count

# Target: <100ms per test
assert avg_time < 0.1, f"Tests too slow: avg={avg_time*1000:.0f}ms"

# Metric 3: Test Flakiness
flaky_tests = count_flaky_tests()  # Tests that intermittently fail
total_tests = count_total_tests()
flakiness_rate = flaky_tests / total_tests

# Target: <1% flakiness
assert flakiness_rate < 0.01, f"Too many flaky tests: {flakiness_rate*100:.1f}%"