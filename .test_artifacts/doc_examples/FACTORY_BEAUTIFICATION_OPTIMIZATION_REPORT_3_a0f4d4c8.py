# Example from: docs\reports\FACTORY_BEAUTIFICATION_OPTIMIZATION_REPORT.md
# Index: 3
# Runnable: True
# Hash: a0f4d4c8

from numba import jit

   @jit(nopython=True)
   def validate_gains_vectorized(gains_array: np.ndarray) -> np.ndarray:
       # Vectorized validation for PSO operations