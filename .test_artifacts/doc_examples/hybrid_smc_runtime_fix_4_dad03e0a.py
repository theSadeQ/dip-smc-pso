# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 4
# Runnable: False
# Hash: dad03e0a

# File: src/controllers/smc/hybrid_adaptive_sta_smc.py
# Lines: 690 total

class HybridAdaptiveSTASMC:
    def compute_control(self, state, state_vars, history):
        # Lines 483-674: Complete control algorithm implementation

        # Lines 675-677: Comments about return statement
        # Package the outputs into a structured named tuple...

        # MISSING: Actual return statement

    def reset(self) -> None:
        """Reset controller state."""
        # Lines 680-689: Reset logic

        # Line 690: INCORRECT return statement with out-of-scope variables
        return HybridSTAOutput(u_sat, (k1_new, k2_new, u_int_new), history, float(s))