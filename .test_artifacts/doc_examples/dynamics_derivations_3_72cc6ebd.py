# Example from: docs\mathematical_foundations\dynamics_derivations.md
# Index: 3
# Runnable: False
# Hash: 72cc6ebd

# example-metadata:
# runnable: false

# Bad: Recompute sin/cos multiple times
M11 = ... + m2 * L1 * L2 * np.cos(theta2 - theta1)
C12 = -m2 * L1 * L2 * np.sin(theta2 - theta1) * dtheta2

# Good: Cache trigonometric values
s1, c1 = np.sin(theta1), np.cos(theta1)
s2, c2 = np.sin(theta2), np.cos(theta2)
s12, c12 = np.sin(theta2 - theta1), np.cos(theta2 - theta1)

M11 = ... + m2 * L1 * L2 * c12
C12 = -m2 * L1 * L2 * s12 * dtheta2