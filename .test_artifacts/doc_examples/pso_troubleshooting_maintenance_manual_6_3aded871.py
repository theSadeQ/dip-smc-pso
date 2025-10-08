# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 6
# Runnable: False
# Hash: 3aded871

import gc

   def cleanup_callback(iteration, **kwargs):
       if iteration % 20 == 0:
           gc.collect()  # Force garbage collection
       return False

   results = pso_tuner.optimize(callback=cleanup_callback, ...)