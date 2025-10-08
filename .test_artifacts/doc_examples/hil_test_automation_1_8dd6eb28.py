# Example from: docs\reference\interfaces\hil_test_automation.md
# Index: 1
# Runnable: True
# Hash: 8dd6eb28

from src.interfaces.hil.test_automation import TestSuite

# Create test suite
suite = TestSuite(name="HIL_Controller_Tests")

# Define test cases
suite.add_test(
    name="stability_test",
    initial_state=[0.0, 0.1, -0.05, 0.0, 0.0, 0.0],
    duration=5.0,
    pass_criteria={"max_angle": 0.2, "settling_time": 3.0}
)

suite.add_test(
    name="disturbance_rejection",
    initial_state=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    disturbance={"type": "step", "magnitude": 10.0, "time": 2.0},
    pass_criteria={"recovery_time": 2.0}
)

# Run all tests
results = suite.run_all()

# Report
suite.print_report()