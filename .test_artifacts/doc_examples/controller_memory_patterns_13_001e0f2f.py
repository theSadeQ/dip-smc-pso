# Example from: docs\analysis\controller_memory_patterns.md
# Index: 13
# Runnable: True
# Hash: 001e0f2f

# ✅ EXCELLENT: Numba-compiled core
@numba.njit(cache=True)
def _compute_control_core(state, gains):
    # Automatic optimization of array operations
    return control_output