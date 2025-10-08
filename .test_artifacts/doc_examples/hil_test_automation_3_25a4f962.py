# Example from: docs\reference\interfaces\hil_test_automation.md
# Index: 3
# Runnable: True
# Hash: 25a4f962

from src.interfaces.hil.test_automation import MonteCarloTester

# Monte Carlo test generator
tester = MonteCarloTester(n_trials=100)

# Define parameter distributions
tester.set_distribution(
    "theta1", distribution="normal", mean=0.0, std=0.1
)
tester.set_distribution(
    "theta2", distribution="normal", mean=0.0, std=0.1
)
tester.set_distribution(
    "noise", distribution="uniform", low=0.0, high=0.05
)

# Run Monte Carlo tests
results = tester.run()

# Analyze results
success_rate = sum(r.passed for r in results) / len(results)
print(f"Success rate: {success_rate * 100:.1f}%")