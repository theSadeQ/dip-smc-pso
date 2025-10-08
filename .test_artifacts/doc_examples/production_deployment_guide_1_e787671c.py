# Example from: docs\deployment\production_deployment_guide.md
# Index: 1
# Runnable: True
# Hash: e787671c

# Production optimization settings
import os
import numpy as np
from numba import set_num_threads

# Configure Numba for production
os.environ['NUMBA_CACHE_DIR'] = '/tmp/numba_cache'
os.environ['NUMBA_NUM_THREADS'] = str(os.cpu_count())
set_num_threads(os.cpu_count())

# NumPy optimizations
np.seterr(all='raise')  # Raise on numerical errors
os.environ['OMP_NUM_THREADS'] = str(os.cpu_count())
os.environ['OPENBLAS_NUM_THREADS'] = str(os.cpu_count())