# Example from: docs\reports\GITHUB_ISSUE_HYBRID_SMC_RESOLUTION_REPORT.md
# Index: 2
# Runnable: False
# Hash: 0cce747a

# example-metadata:
# runnable: false

# FIXED IMPLEMENTATION
class HybridAdaptiveSTASMC:
    def compute_control(self, state, state_vars, history):
        """Compute hybrid adaptive STA-SMC control action."""

        # ... 674 lines of control algorithm implementation ...

        # Calculate final control values
        u_sat = float(np.clip(u_total, -self.max_force, self.max_force))
        k1_new = max(0.0, min(k1_new, self.k1_max))
        k2_new = max(0.0, min(k2_new, self.k2_max))
        u_int_new = float(np.clip(u_int_new, -self.u_int_max, self.u_int_max))

        # ✅ CRITICAL FIX: Proper return statement with correct variable scope
        return HybridSTAOutput(u_sat, (k1_new, k2_new, u_int_new), history, float(s))

    def reset(self) -> None:
        """Reset controller state to initial conditions."""
        self.k1 = self.k1_init
        self.k2 = self.k2_init
        self.u_int = 0.0
        self.last_s = 0.0

        # ✅ CORRECT: No return statement (method returns None as intended)
        pass