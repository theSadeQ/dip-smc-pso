# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 9
# Runnable: False
# Hash: 093ce541

# example-metadata:
# runnable: false

def compute_control(self, state, state_vars, history):
    # ... 674 lines of implementation ...

    # Package the outputs into a structured named tuple
    return HybridSTAOutput(u_sat, (k1_new, k2_new, u_int_new), history, float(s))
    # ^^^^ Properly scoped variables ^^^^

def reset(self) -> None:
    """Reset controller state."""
    # ... reset logic only ...
    pass