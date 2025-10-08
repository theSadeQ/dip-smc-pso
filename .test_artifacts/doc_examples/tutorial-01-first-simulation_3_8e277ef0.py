# Example from: docs\guides\tutorials\tutorial-01-first-simulation.md
# Index: 3
# Runnable: True
# Hash: 8e277ef0

# For first pendulum angle θ₁:
final_angle = theta1[-1]  # ~0 rad
peak_angle = np.max(np.abs(theta1))
overshoot = (peak_angle - abs(final_angle)) / abs(final_angle) * 100