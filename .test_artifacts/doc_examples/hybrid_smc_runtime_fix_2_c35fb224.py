# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 2
# Runnable: False
# Hash: c35fb224

# example-metadata:
# runnable: false

def compute_control(...) -> HybridSTAOutput:
    # ... 674 lines of control logic ...
    # MISSING: return statement
    # Implicit return None

def reset(self) -> None:
    # ...
    return HybridSTAOutput(u_sat, state_vars, history, s)
    # ^^^^ Variables not in scope! ^^^^