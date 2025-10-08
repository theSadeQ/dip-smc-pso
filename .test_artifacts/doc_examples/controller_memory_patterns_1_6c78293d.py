# Example from: docs\analysis\controller_memory_patterns.md
# Index: 1
# Runnable: True
# Hash: 6c78293d

def compute_control(self, state: np.ndarray, state_vars, history):
    # ✅ OPTIMAL: Direct unpacking creates views, not copies
    x, theta1, theta2, x_dot, theta1_dot, theta2_dot = state

    # Use elements directly
    sigma = self.k1 * (theta1_dot + self.lam1 * theta1) + \
            self.k2 * (theta2_dot + self.lam2 * theta2)