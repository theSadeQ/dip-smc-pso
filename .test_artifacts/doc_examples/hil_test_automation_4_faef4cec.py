# Example from: docs\reference\interfaces\hil_test_automation.md
# Index: 4
# Runnable: True
# Hash: faef4cec

from src.interfaces.hil.test_automation import CITestRunner

# CI test runner
ci_runner = CITestRunner(
    test_suite_path="tests/hil_tests.yaml",
    report_path="ci_report.json"
)

# Run tests
results = ci_runner.run()

# Check for regressions
if results.has_regressions():
    print("REGRESSION DETECTED!")
    for test in results.regressions:
        print(f"  {test.name}: {test.baseline_time:.2f}s -> {test.current_time:.2f}s")
    exit(1)

print("All tests passed, no regressions")
exit(0)