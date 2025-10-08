# Example from: docs\guides\workflows\batch-simulation-workflow.md
# Index: 9
# Runnable: True
# Hash: bfbd753a

# Warm-up run (trigger Numba JIT)
_ = simulate(np.zeros((10, 6)), np.zeros((10, 100)), 0.01, 100)

# Then run actual simulation
results = simulate(initial_states, controls, dt, horizon)