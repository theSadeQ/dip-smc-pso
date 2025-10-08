# Example from: docs\analysis\controller_memory_patterns.md
# Index: 6
# Runnable: True
# Hash: 83e6a9ff

# ✅ OPTIMAL (actual implementation)
def compute_control(self, state: np.ndarray):
    x, theta1, theta2 = state[0], state[1], state[2]  # Views