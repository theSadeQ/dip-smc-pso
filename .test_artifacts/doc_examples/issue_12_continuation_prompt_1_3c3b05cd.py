# Example from: docs\issue_12_continuation_prompt.md
# Index: 1
# Runnable: False
# Hash: 3c3b05cd

# example-metadata:
# runnable: false

# Multi-objective fitness function
fitness = tracking_error_rms + 10.0 * max(0, chattering_index - 2.0)

# Chattering metric (matches validation test)
chattering_index = 0.7 * RMS(du/dt) + 0.3 * FFT_high_freq_power

# PSO parameters
n_particles = 30
iters = 150
seed = 42
c1 = 2.0  # cognitive
c2 = 2.0  # social
w = 0.7   # inertia

# Simulation config
dt = 0.01
t_final = 10.0
initial_state = [0.0, 0.1, 0.1, 0.0, 0.0, 0.0]