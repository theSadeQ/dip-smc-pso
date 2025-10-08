# Example from: docs\reference\interfaces\hil_test_automation.md
# Index: 5
# Runnable: True
# Hash: c574f976

from src.interfaces.hil.test_automation import AdaptiveTester

# Adaptive tester
tester = AdaptiveTester(
    initial_difficulty=0.5,
    adjustment_rate=0.1
)

# Run adaptive tests
for i in range(20):
    test_case = tester.generate_test()
    result = run_hil_simulation(test_case)

    # Adjust difficulty based on result
    tester.update(result.passed)

    print(f"Test {i+1}: difficulty={tester.current_difficulty:.2f}, "
          f"result={'PASS' if result.passed else 'FAIL'}")

# Report final difficulty
print(f"Final difficulty: {tester.current_difficulty:.2f}")