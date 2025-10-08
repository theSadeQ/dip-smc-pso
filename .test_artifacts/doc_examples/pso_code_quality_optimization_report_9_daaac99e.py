# Example from: docs\reports\pso_code_quality_optimization_report.md
# Index: 9
# Runnable: True
# Hash: daaac99e

from numba import jit, njit

@njit(parallel=True)
def _vectorized_cost_computation(states, controls, dt_array):
    """High-performance cost computation with Numba."""
    # Parallelized inner loops for large batch processing