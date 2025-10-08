# Example from: docs\guides\tutorials\tutorial-01-first-simulation.md
# Index: 4
# Runnable: True
# Hash: b0141412

# Average error in last 20% of simulation
steady_state_region = x[int(0.8*len(x)):]
steady_state_error = np.mean(np.abs(steady_state_region - desired_state))