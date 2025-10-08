# Example from: docs\guides\api\simulation.md
# Index: 20
# Runnable: False
# Hash: 059d42ff

# example-metadata:
# runnable: false

# First call compiles the function (slow)
batch_results = run_batch_simulation(...)  # ~2 seconds

# Subsequent calls use compiled code (fast)
batch_results = run_batch_simulation(...)  # ~0.1 seconds