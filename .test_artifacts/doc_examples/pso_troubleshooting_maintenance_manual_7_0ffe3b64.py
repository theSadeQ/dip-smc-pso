# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 7
# Runnable: True
# Hash: 0ffe3b64

# Use smaller data types
   import numpy as np

   # In PSO configuration
   pso_config = {
       'n_particles': 30,  # Reduce from 50
       'store_history': False,  # Don't store full history
       'dtype': np.float32  # Use 32-bit floats
   }