# Example from: docs\guides\tutorials\tutorial-02-controller-comparison.md
# Index: 3
# Runnable: True
# Hash: 72cbf137

# Example verification
alpha = 20.0
beta = 15.0
L_max = 10.0  # Estimated maximum disturbance gradient

assert alpha > L_max, "α must exceed disturbance Lipschitz constant"
assert beta > (5 * L_max**2) / (4 * alpha), "β violates stability condition"