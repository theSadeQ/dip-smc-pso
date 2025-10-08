# Example from: docs\analysis\controller_memory_patterns.md
# Index: 5
# Runnable: True
# Hash: 7e1729f3

# ❌ ANTI-PATTERN (not found in our controllers)
def compute_control(self, state: np.ndarray):
    state_copy = state.copy()  # Unnecessary allocation
    x, theta1, theta2 = state_copy[0], state_copy[1], state_copy[2]