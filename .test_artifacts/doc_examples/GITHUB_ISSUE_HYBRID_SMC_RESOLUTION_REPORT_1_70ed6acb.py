# Example from: docs\reports\GITHUB_ISSUE_HYBRID_SMC_RESOLUTION_REPORT.md
# Index: 1
# Runnable: False
# Hash: 70ed6acb

# example-metadata:
# runnable: false

# File: src/controllers/smc/hybrid_adaptive_sta_smc.py
class HybridAdaptiveSTASMC:
    def compute_control(self, state, state_vars, history):
        """Compute hybrid adaptive STA-SMC control action."""

        # ... 674 lines of complex control algorithm implementation ...

        # Calculate control outputs
        u_sat = float(np.clip(u_total, -self.max_force, self.max_force))
        k1_new = max(0.0, min(k1_new, self.k1_max))
        k2_new = max(0.0, min(k2_new, self.k2_max))
        u_int_new = float(np.clip(u_int_new, -self.u_int_max, self.u_int_max))
        s = float(s)

        # Comments about packaging outputs...
        # Package the outputs into a structured named tuple. Returning a
        # named tuple formalises the contract and allows clients to
        # access fields by name while retaining tuple compatibility.

        # ❌ CRITICAL BUG: Missing return statement!
        # Function implicitly returns None instead of HybridSTAOutput

    def reset(self) -> None:
        """Reset controller state."""
        # ... reset logic ...

        # ❌ WRONG: Return statement with out-of-scope variables
        return HybridSTAOutput(u_sat, (k1_new, k2_new, u_int_new), history, float(s))
        # Variables u_sat, k1_new, k2_new, u_int_new, history, s are NOT in scope here!