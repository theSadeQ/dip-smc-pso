# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 6
# Runnable: False
# Hash: 9f46a4a8

# example-metadata:
# runnable: false

   import gc

   def cleanup_callback(iteration, **kwargs):
       if iteration % 20 == 0:
           gc.collect()  # Force garbage collection
       return False

   results = pso_tuner.optimize(callback=cleanup_callback, ...)