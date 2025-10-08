# Example from: docs\analysis\controller_memory_patterns.md
# Index: 2
# Runnable: True
# Hash: 02549a84

def _compute_equivalent_control(self, state: np.ndarray) -> float:
    # ✅ OPTIMAL: state[3:] returns a view
    q_dot = state[3:]

    # View is safe for read-only operations
    if getattr(C, "ndim", 1) == 2:
        rhs = C @ q_dot + G