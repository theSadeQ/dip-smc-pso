# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 8
# Runnable: False
# Hash: 0dc28dc1

# example-metadata:
# runnable: false

def compute_control(self, state, state_vars, history):
    # ... 674 lines of implementation ...

    # Comments about packaging outputs
    # MISSING: return statement

def reset(self) -> None:
    """Reset controller state."""
    # ... reset logic ...
    pass
    return HybridSTAOutput(u_sat, (k1_new, k2_new, u_int_new), history, float(s))
    # ^^^^ Out of scope variables ^^^^