# Example from: docs\guides\api\simulation.md
# Index: 21
# Runnable: False
# Hash: 43170c6f

# example-metadata:
# runnable: false

# Too small: Compilation overhead dominates
run_batch_simulation(..., n_trials=10)  # Not efficient

# Optimal: Amortize compilation cost
run_batch_simulation(..., n_trials=100)  # Good

# Too large: Memory issues
run_batch_simulation(..., n_trials=10000)  # May run out of RAM