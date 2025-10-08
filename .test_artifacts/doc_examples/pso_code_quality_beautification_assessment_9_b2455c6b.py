# Example from: docs\reports\pso_code_quality_beautification_assessment.md
# Index: 9
# Runnable: True
# Hash: b2455c6b

from numba import jit

@jit(nopython=True)
def _compute_cost_from_traj_numba(t, x_b, u_b, sigma_b, weights, norms):
    """Numba-optimized cost computation for CPU-intensive operations."""
    # Move inner computation loops to compiled function