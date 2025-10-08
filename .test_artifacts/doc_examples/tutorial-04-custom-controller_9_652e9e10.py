# Example from: docs\guides\tutorials\tutorial-04-custom-controller.md
# Index: 9
# Runnable: True
# Hash: 652e9e10

# Bad: Division by zero
term = dtheta ** alpha

# Good: Add small epsilon
term = np.sign(dtheta) * (np.abs(dtheta) + 1e-6) ** alpha