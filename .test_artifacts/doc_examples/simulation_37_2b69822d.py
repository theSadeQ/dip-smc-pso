# Example from: docs\guides\api\simulation.md
# Index: 37
# Runnable: False
# Hash: 2b69822d

# example-metadata:
# runnable: false

   # Instead of 10000 trials
   batch_size = 1000
   results = run_batch_simulation(..., initial_conditions=ic[:batch_size])