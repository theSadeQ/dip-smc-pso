# Example from: docs\analysis\HYBRID_SMC_FIX_TECHNICAL_DOCUMENTATION.md
# Index: 2
# Runnable: False
# Hash: 665f779b

def compute_control(self, state, state_vars, history):
    # ... 674 lines of complex control algorithm implementation ...

    # Calculate final control values
    u_sat = float(np.clip(u_total, -self.max_force, self.max_force))
    k1_new = max(0.0, min(k1_new, self.k1_max))
    k2_new = max(0.0, min(k2_new, self.k2_max))
    u_int_new = float(np.clip(u_int_new, -self.u_int_max, self.u_int_max))

    # ✅ CRITICAL FIX: Proper return statement with correct variable scope
    return HybridSTAOutput(u_sat, (k1_new, k2_new, u_int_new), history, float(s))

def reset(self) -> None:
    """Reset controller state."""
    # ... reset logic only ...
    # ✅ CORRECT: No return statement (method should return None)
    pass