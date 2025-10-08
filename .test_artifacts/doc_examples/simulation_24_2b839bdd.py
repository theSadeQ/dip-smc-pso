# Example from: docs\guides\api\simulation.md
# Index: 24
# Runnable: True
# Hash: 2b839bdd

# Test sensitivity to initial conditions
theta1_values = np.linspace(0.05, 0.3, 20)
ise_results = []

for theta1 in theta1_values:
    ic = np.array([0, 0, theta1, 0, theta1*1.5, 0])
    result = runner.run(controller, initial_state=ic)
    ise_results.append(result['metrics']['ise'])

# Plot sensitivity
import matplotlib.pyplot as plt
plt.plot(np.degrees(theta1_values), ise_results)
plt.xlabel('Initial θ₁ (degrees)')
plt.ylabel('ISE')
plt.title('Controller Sensitivity to Initial Conditions')
plt.show()