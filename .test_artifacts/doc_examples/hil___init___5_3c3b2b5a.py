# Example from: docs\reference\interfaces\hil___init__.md
# Index: 5
# Runnable: True
# Hash: 3c3b2b5a

from src.interfaces import hil

# Create test suite
suite = hil.TestSuite(name="Controller_Validation")

# Add test cases
suite.add_test(
    name="stability",
    initial_state=[0.0, 0.1, -0.05, 0.0, 0.0, 0.0],
    pass_criteria={"settling_time": 3.0}
)

suite.add_test(
    name="robustness",
    initial_state=[0.0, 0.2, -0.1, 0.0, 0.0, 0.0],
    disturbance={"type": "step", "magnitude": 10.0},
    pass_criteria={"recovery_time": 2.0}
)

# Run all tests
results = suite.run_all()

# Generate report
suite.save_report("test_report.json")
print(f"Tests passed: {results.pass_count}/{results.total_count}")