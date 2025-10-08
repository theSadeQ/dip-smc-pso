# Example from: docs\reference\interfaces\hil_test_automation.md
# Index: 2
# Runnable: True
# Hash: 1bd6b2ac

from src.interfaces.hil.test_automation import GridTestGenerator

# Generate test cases on grid
generator = GridTestGenerator()

# Define parameter ranges
theta1_values = np.linspace(-0.2, 0.2, 5)
theta2_values = np.linspace(-0.2, 0.2, 5)

test_cases = generator.generate(
    theta1=theta1_values,
    theta2=theta2_values,
    x=[0.0],  # Fixed cart position
    velocities=[0.0, 0.0, 0.0]  # Zero initial velocity
)

print(f"Generated {len(test_cases)} test cases")

# Run all generated tests
for i, test_case in enumerate(test_cases):
    result = run_hil_simulation(initial_state=test_case)
    print(f"Test {i+1}: {'PASS' if result.stable else 'FAIL'}")