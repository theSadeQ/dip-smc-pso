# Example from: docs\guides\tutorials\tutorial-01-first-simulation.md
# Index: 2
# Runnable: True
# Hash: a0a4662f

# For each state variable:
final_value = x[-1]
threshold = 0.02 * abs(final_value)
settling_idx = np.where(abs(x - final_value) > threshold)[0]
settling_time = t[settling_idx[-1]] if len(settling_idx) > 0 else 0