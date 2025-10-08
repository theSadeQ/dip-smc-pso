# Example from: docs\analysis\controller_memory_patterns.md
# Index: 7
# Runnable: True
# Hash: a10c3bbd

# ❌ ANTI-PATTERN (not found in our controllers)
def _compute_equivalent_control(self, state: np.ndarray):
    q_dot_copy = state[3:].copy()  # Unnecessary
    result = M @ q_dot_copy