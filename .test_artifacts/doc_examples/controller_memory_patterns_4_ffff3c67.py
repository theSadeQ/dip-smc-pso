# Example from: docs\analysis\controller_memory_patterns.md
# Index: 4
# Runnable: True
# Hash: ffff3c67

def compute_control(self, state: np.ndarray, state_vars, history):
    # ✅ OPTIMAL: Direct indexing for cart recentering
    x = state[0]
    xdot = state[3]

    # Efficient conditionals on scalar views
    if abs(x) > self.recenter_high_thresh:
        u_cart = -self.cart_p_gain * (xdot + self.cart_p_lambda * x)