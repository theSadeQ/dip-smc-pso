# Example from: docs\analysis\controller_memory_patterns.md
# Index: 8
# Runnable: True
# Hash: d9ddf980

# ✅ OPTIMAL (actual implementation)
def _compute_equivalent_control(self, state: np.ndarray):
    q_dot = state[3:]  # View is sufficient for read-only ops
    result = M @ q_dot